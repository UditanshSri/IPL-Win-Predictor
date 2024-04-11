import pickle
import streamlit as st
import pandas as pd

model = pickle.load(open('pipe.pkl', 'rb'))

teams = [
    'Sunrisers Hyderabad',
    'Mumbai Indians',
    'Royal Challengers Bangalore',
    'Kolkata Knight Riders',
    'Delhi Capitals',
    'Chennai Super Kings',
    'Rajasthan Royals',
    'Punjab Kings'
]

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
          'Chandigarh', 'Jaipur', 'Chennai','Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
          'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
          'Sharjah', 'Mohali', 'Bengaluru']

col1, col2 = st.columns(2)
with col1:
    batting_team = st.selectbox('Select the batting team', teams)
with col2:
    bowling_team = st.selectbox('Select the bowling team', teams)

target = st.number_input('Target Score')

selected_city = st.selectbox('Select host city', cities)

col3, col4, col5 = st.columns(3)
with col3:
    score = st.number_input('Current Score')

with col4:
    overs = st.number_input('Overs completed')
with col5:
    wickets = st.number_input('Wickets Left')

if st.button('Predict Probability'):
    runs_left = target - score
    balls_left = 120 - (overs * 6)
    crr = score / overs
    rrr = (runs_left * 6) / balls_left

    input_df = pd.DataFrame({'batting_team': [batting_team],
                             'bowling_team': [bowling_team],
                             'city': [selected_city],
                             'runs left': [runs_left],
                             'balls left': [balls_left],
                             'wickets left': [wickets],
                             'total_runs_x': [target],
                             'crr': [crr],
                             'rrr': [rrr]})

    result = model.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    st.header(batting_team + "- " + str(round(win * 100)) + "%")
    st.header(bowling_team + "- " + str(round(loss * 100)) + "%")
