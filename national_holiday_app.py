import requests
import json
import os
import pandas as pd
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

holidays = requests.get(f"https://calendarific.com/api/v2/holidays?&api_key={KEY}&country={country_code}&year=2023").text

#0 get list of countries and save it as csv

# read json
# KEY = os.getenv("KEY")
# #rq = requests.get(f"https://calendarific.com/api/v2/countries?&api_key={KEY}").text
# js = json.loads(rq)
# print(js)
#
# # keep only json data that is of interest
# data = js['response']['countries']
#
# # convert it into dataframe
# df=pd.DataFrame.from_records(data)
# print(df)
#
# df.to_csv('country_list.csv')

#1 get data from csv and save in dataframe for data processing at a later stage and save country_list as a list
df=pd.read_csv('country_list.csv')
print(df)

# get country names for dropdown
list_of_rows = df["country_name"].tolist()
print(list_of_rows)

#2 app layout
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], prevent_initial_callbacks=True, suppress_callback_exceptions=True)

app.layout = html.Div([
     html.H3("Holidays around the world for year 2023", style={'text-align': 'center'}),
     html.Br(),
     dcc.Dropdown(id="slct_country", options=[{"label":k, "value":k} for k in list_of_rows],
                  placeholder="Enter/Search country"),
     html.Br(),
     dbc.Button('View national holidays', id='btn', n_clicks=0, className='justify-content-center'),
     html.Br(),
     html.Br(),
     html.Div(id='results')
])

#3 callback to show results
@app.callback(
    Output('results', 'children'),
    Input('btn', 'n_clicks'),
    State('slct_country', 'value')
)

def data(click, country):
    if country is None:
        result = dbc.Alert("Please enter a country", color="danger")
        return result

    # get api key
    KEY = os.getenv("KEY")

    #find corresponding country code for country typed in by user
    for index, row in df.iterrows():
        if (df.at[index, 'country_name'] == country):
            country_code = df.at[index, 'iso-3166']
            print(country_code)

    # api call
    # api documentation
    # https://calendarific.com/api-documentation
    #holidays = requests.get(f"https://calendarific.com/api/v2/holidays?&api_key=e29d32829e75335679077296cb0fae4e5f0e2e0e8dab56f267c29917bc9d6faf&country=US&year=2023").text
    holidays = requests.get(f"https://calendarific.com/api/v2/holidays?&api_key={KEY}&country={country_code}&year=2023").text
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

    # show dataframe in dbc table
    result = dbc.Table.from_dataframe(df_result, striped=True, bordered=True, hover=True)
    #result = html.Br()
    return result

if __name__ == '__main__':
    app.run_server(debug=True)
