# Coronavirus (COVID-19) in the UK
This is a simple personalised covid dashboard.\
Dashboard application will coordinate information about the COVID infection rates from the Public Health England API and news stories about Covid from a given news API.
# Installation
Firstly you need to clone this repository\
`git clone `\
Once the project is cloned, you also need to install the dependencies using the command pip install -r requirements.txt from the root folder of the project\
`pip install -r requirements.txt`
# Launching
`python user_interface.py`
# Functions
- parse_csv_data()\
This function takes an argument called df_name and returns a list of strings for the rows in the file.
```python 
def parse_csv_data(df_name):
    data = pd.read_csv(df_name)
    products_list = data.values.tolist()
    return products_list
```
- process_covid_csv_data()\
This function takes a list of data from an argument called covid_csv_data, as would be returned from the function
above, and returns three variables; the number of cases in the last 7 days, the current number
of hospital cases and the cumulative number of deaths, as contained in the given csv file.
```python
def process_covid_csv_data(covid_csv_data):
    last7days_cases = 0
    current_hospital_cases = 0
    total_deaths = 0
    for i in range(7):
        last7days_cases += covid_csv_data[i][5] + covid_csv_data[i][6]
    current_hospital_cases = covid_csv_data[0][5]
    total_deaths = covid_csv_data[13][4]
    return last7days_cases, current_hospital_cases, total_deaths
```
- covid_API_request()\
This function takes two arguments called location and location_type with the default values of "Exeter" and "ltla" and
returns up-to-date Covid data as a dictionary.
```python
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
```
- news_API_request()\
This function takes an argument called covid_terms with a default value of "Covid COVID-19 coronavirus".
```python
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
```
- schedule_covid_updates()\
This function takes two arguments called update_interval and update_name and updates covid data at the given time interval
using the sched module.
```python
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
```
- update_news()\
This function uses the news API request within the function and
is able to update a data structure containing news articles.
```python
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
```
