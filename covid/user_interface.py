from flask import Flask
from flask import render_template
from flask import request
import threading
from covid_news_handling import news_Api_request, update_news
from covid_data_handler import covid_api_request, schedule_covid_updates
import json
import logging


# loading configuration parameters
with open('config.json', 'r') as file:
    config = json.load(file)


secret_key = config['secret_key']
title = config['title']
path_to_image = config['path_to_image'] + config['image']
location = config['local_location']
nation_location = config['nation_location']
local = config['local_type']
nation = config['nation_type']
file_log = config['file_log']
news_articles = news_Api_request()['articles']
updates = []
local_7day_infections = 0
national_7day_infections = 0
deaths_total = 0
hospital_cases = 0
FORMAT = f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'


# creating flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
logging.basicConfig(filename=file_log, level=logging.DEBUG, format=FORMAT)


# main page
@app.route('/', methods=['GET', 'POST'])
def main():
    global updates, national_7day_infections, local_7day_infections
    global deaths_total, hospital_cases
    app.logger.info('Info level log')
    app.logger.warning('Warning level log')
    if request.method == 'POST':
        update_time = request.form['update']
        update_title = request.form['two']
        try:
            checkbox_repeat = request.form['repeat']
        except KeyError:
            checkbox_repeat = 0
        try:
            checkbox_update_covid_data = request.form['covid-data']
        except KeyError:
            checkbox_update_covid_data = 0
        try:
            checkbox_update_news = request.form['news']
        except KeyError:
            checkbox_update_news = 0
        if checkbox_update_covid_data != 0:
            updates.append({'title': f'{update_title} - {update_time}',
                            'content': 'Covid data'})
            if checkbox_repeat != 0:
                pass
            else:
                schedule_covid_updates(update_time, update_title)
        if checkbox_update_news != 0:
            updates.append({'title': f'{update_title} - {update_time}',
                            'content': 'News'})
            if checkbox_repeat != 0:
                pass
            else:
                update_news(update_time, update_title)
        return render_template('index.html',
                                title=title,
                                path_to_image=path_to_image,
                                location=location,
                                nation_location=nation_location,
                                news_articles=news_articles,
                                updates=updates,
                                local_7day_infections=local_7day_infections,
                                national_7day_infections=national_7day_infections,
                                hospital_cases=hospital_cases,
                                deaths_total=deaths_total)
    daily = []
    local_daily = []
    c = 0
    c_local = 0
    for d in covid_api_request(nation_location, nation)['data']:
        if d['cumDeaths28DaysByDeathDate'] is not None:
            deaths_total = d['cumDeaths28DaysByDeathDate']
            break
    for d in covid_api_request(nation_location, nation)['data']:
        if d['hospitalCases'] is not None:
            hospital_cases = d['hospitalCases']
            break
    for d in covid_api_request(nation_location, nation)['data']:
        if d['daily'] is not None:
            daily.append(d['daily'])
        c += 1
        if c >= 7:
            if len(daily) != 0:
                break
            else:
                if d['daily'] is not None:
                    daily.append(d['daily'])
                if len(daily) != 0:
                    break
    for d in covid_api_request(location, local)['data']:
        if d['daily'] is not None:
            local_daily.append(d['daily'])
        c_local += 1
        if c_local >= 7:
            if len(local_daily) != 0:
                break
            else:
                if d['daily'] is not None:
                    local_daily.append(d['daily'])
                if len(local_daily) != 0:
                    break
    national_7day_infections = int(sum(daily)/7)
    local_7day_infections = int(sum(local_daily)/7)
    return render_template('index.html',
                            title=title,
                            path_to_image=path_to_image,
                            location=location,
                            nation_location=nation_location,
                            news_articles=news_articles,
                            updates=updates,
                            local_7day_infections=local_7day_infections,
                            national_7day_infections=national_7day_infections,
                            hospital_cases=hospital_cases,
                            deaths_total=deaths_total)


# launch flask app
if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
