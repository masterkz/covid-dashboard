import pandas as pd
from uk_covid19 import Cov19API
import json
import sched
import time
from datetime import datetime


# get list of data from .csv file
def parse_csv_data(df_name):
    data = pd.read_csv(df_name)
    products_list = data.values.tolist()
    return products_list


# get cases for last 7 days, hospital cases and total number of deaths from csv file
def process_covid_csv_data(covid_csv_data):
    last7days_cases = 0
    current_hospital_cases = 0
    total_deaths = 0
    for i in range(7):
        last7days_cases += covid_csv_data[i][5] + covid_csv_data[i][6]
    current_hospital_cases = covid_csv_data[0][5]
    total_deaths = covid_csv_data[13][4]
    return last7days_cases, current_hospital_cases, total_deaths


# get json objects with covid data by parameters
def covid_api_request(location, location_type):
    england_only = [
        f'areaType={location_type}',
        f'areaName={location}'
    ]
    cases_and_deaths = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "cumCasesByPublishDate": "cumCasesByPublishDate",
        "newDeaths28DaysByDeathDate": "newDeaths28DaysByDeathDate",
        "cumDeaths28DaysByDeathDate": "cumDeaths28DaysByDeathDate",
        "hospitalCases": "hospitalCases",
        "daily": "newCasesBySpecimenDate"
    }
    api = Cov19API(filters=england_only, structure=cases_and_deaths)
    data = api.get_json()
    return data


# updating covid_api_request function with sched module
def schedule_covid_updates(update_interval, update_name):
    global scheduler
    dt = datetime.today()
    date_info = str(dt).split()
    date = date_info[0].split('-')
    interval = update_interval.split(':')
    hours = interval[0]
    minutes = interval[1]
    d_req = datetime(int(date[0]), int(date[1]), int(date[2]), hours, minutes)
    tm = d_req.timestamp()
    schedule_time = tm - time.time()
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(schedule_time, 1, covid_api_request)
    scheduler.run()
