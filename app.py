import streamlit as st
import pandas as pd
import requests

st.set_page_config(layout="wide")

#Access the API. I'll need to hide this when deploying
AUTH_HEADER =  st.secrets['API_AUTH_STRING']

#Function for making requests to cfb data api
def get_cfb_data_response(url, auth_string):
    response = requests.get(url, headers={'Authorization': auth_string})
    return response.json()

#Fetch data
@st.cache
def fetch_data():
    data = get_cfb_data_response(f'https://api.collegefootballdata.com/player/portal?year=2021', AUTH_HEADER)
    data = data + get_cfb_data_response(f'https://api.collegefootballdata.com/player/portal?year=2022', AUTH_HEADER)
    return data

data_from_api = fetch_data()

#Get list of all unique teams in api response. Ignore nulls
teams = [transfer['origin'] for transfer in data_from_api if transfer['origin']] 
teams = teams + [transfer['destination'] for transfer in data_from_api if transfer['destination']] 

#Get unique teams sorted alphabetically
unique_teams = sorted(set(teams))

#Allow user to select team of interest
team = st.selectbox('Pick a Team', unique_teams)

#Filter data from api according to user selection
filtered_data = list(filter(lambda d: d['origin'] == team or d['destination'] == team, data_from_api))

st.title("Team Transfer Data From API")

team_departing_transfers = list(filter(lambda d:d['origin'] == team, filtered_data))
team_arriving_transfers = list(filter(lambda d:d['destination'] == team, filtered_data))


row1_space1, row1_1, row1_space2, row1_2, row1_space3 = st.columns((.1, 1, .1, 1, .1))

with row1_1:
	st.image('pics/departures.png')
	st.metric("# Players", len(team_departing_transfers))
	st.dataframe(pd.DataFrame(team_departing_transfers))
with row1_2:
	st.image('pics/arrivals.png')
	st.metric("# Players", len(team_arriving_transfers))
	st.dataframe(pd.DataFrame(team_arriving_transfers))