import pandas as pd
from covid_data_handler import parse_csv_data
from covid_data_handler import process_covid_csv_data
import requests
import pytest


def test_parse_csv_data(file):
    data = parse_csv_data(file)
    assert len (data) == 639


def test_process_covid_csv_data(file):
    last7days_cases, current_hospital_cases, total_deaths = process_covid_csv_data(parse_csv_data(file))
    assert last7days_cases == 240299
    assert current_hospital_cases == 7019
    assert total_deaths == 141544 


def test_flask_app():
    response = requests.get('127.0.0.1/')
    assert str(response) == '<Response [200]>'
