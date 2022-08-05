import requests
import sched
import time
from datetime import datetime
import json


# loading configuration parameters
with open('config.json', 'r') as file:
    config = json.load(file)


covid_terms = config['covid_terms']
news_link = config['news_link']
apiKey = config['api_key']


# get json object with covid news
def news_Api_request(covid_terms=covid_terms):
    link = news_link
    params = {'q': f'{covid_terms}',
              'category': 'health',
              'language': 'en',
              'country': 'gb',
              'apiKey': f'{apiKey}'}
    response = requests.get(link, params)
    data = response.json()
    return data


# updating news_Api_request function with sched module
def update_news(update_interval, update_name):
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
    scheduler.enter(schedule_time, 1, news_Api_request)
    scheduler.run()
