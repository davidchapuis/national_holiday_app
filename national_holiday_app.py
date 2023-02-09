import requests
import json
import os
import pandas as pd
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

def national_holidays(country, api_key):
     """ Returns national holidays in a dataframe (with name, description and date) for a given country."""

     #1 get data from csv and save in dataframe for data processing at a later stage and save country_list as a list
     df=pd.read_csv('country_list.csv')

    #if country is None:
    #    result = dbc.Alert("Please enter a country", color="danger")
    #    return result

    # get api key
    #KEY = os.getenv("KEY")

    #find corresponding country code for country typed in by user
    for index, row in df.iterrows():
        if (df.at[index, 'country_name'] == country):
            country_code = df.at[index, 'iso-3166']
            print(country_code)

    # api call
    # api documentation
    # https://calendarific.com/api-documentation
    #holidays = requests.get(f"https://calendarific.com/api/v2/holidays?&api_key=e29d32829e75335679077296cb0fae4e5f0e2e0e8dab56f267c29917bc9d6faf&country=US&year=2023").text
    holidays = requests.get(f"https://calendarific.com/api/v2/holidays?&api_key={api_key}&country={country_code}&year=2023").text
    #print(holidays)

    # get json with results
    results_js = json.loads(holidays)
    print(results_js)

    # keep only json data that is of interest
    data2 = results_js['response']['holidays']

    # convert it into dataframe
    # full dataframe
    df_full_results = pd.DataFrame.from_records(data2)
    print(df_full_results['date'])
    # dataframe with only name and description columns
    df_selected_results = df_full_results[['name', 'description']]
    print(df_selected_results)
    # issue with date format, making a dataframe with iso date only
    df_dates=pd.DataFrame.from_records(df_full_results['date'])
    df_dates.rename(columns={'iso': 'date'},inplace=True)
    print(df_dates)
    df_date=df_dates['date']
    # print(df_ok)
    # rename column
    #df_date.columns=['date']
    #print(df_date)

    # final dataframe with name, desc and date
    df_result = pd.concat([df_selected_results, df_date], axis=1)

    return df_result
