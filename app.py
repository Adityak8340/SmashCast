import streamlit as st
import joblib
import numpy as np
import pandas as pd
import requests
import datetime
from dotenv import load_dotenv
import os

load_dotenv()
# Load your machine learning model
model = joblib.load('my_model_file.pkl')

# Function to make predictions
def predict(a):
    # Perform prediction using the loaded model
    prediction = model.predict(a)
    return prediction

def classify_weather(description, temperature, humidity, wind_speed):
    # Initialize the dictionary to store the classified weather parameters
    weather_classification = {
        'Outlook_Overcast': [0],
        'Outlook_Rain': [0],
        'Outlook_Sunny': [0],
        'Temperature_Cool': [0],
        'Temperature_Hot': [0],
        'Temperature_Mild': [0],
        'Humidity_High': [0],
        'Humidity_Normal': [0],
        'Wind_Strong': [0],
        'Wind_Weak': [0],        
    }
    
    # Classify based on weather description
    if 'haze' in description.lower():
        weather_classification['Outlook_Overcast'] = [1]
    elif 'rain' in description.lower():
        weather_classification['Outlook_Rain'] = [1]
    else:
        weather_classification['Outlook_Sunny'] = [1]
    
    # Classify based on temperature
    if temperature < 290:
        weather_classification['Temperature_Cool'] = [1]
    elif temperature > 303:
        weather_classification['Temperature_Hot'] = [1]
    else:
        weather_classification['Temperature_Mild'] = [1]
    
    # Classify based on humidity
    if humidity > 50:
        weather_classification['Humidity_High'] = [1]
    else:
        weather_classification['Humidity_Normal'] = [1]
    
    # Classify based on wind speed
    if wind_speed > 2.5:
        weather_classification['Wind_Strong'] = [1]
    else:
        weather_classification['Wind_Weak'] = [1]
    
    return weather_classification

# Function to get real-time weather data from OpenWeatherMap API
def get_weather_data(city):
    country_code = 'IN'
    api_key = os.environ.get("api_key")  # Replace with your API key from OpenWeatherMap
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        return weather_description, temperature, humidity, wind_speed
    else:
        return None, None, None, None

# Streamlit app layout
st.title('SmashCast')
st.text('Your Weather-Driven Badminton Outside Play Predictor')

st.image('badmin_img.png', width=200)

# Text input for location for real-time prediction
location = st.selectbox('Enter your city name', ['Mumbai', 'Agra', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Surat', 'Lucknow', 'Kanpur', 'Nagpur', 'Visakhapatnam', 'Indore', 'Thane', 'Bhopal', 'Patna', 'Vadodara', 'Ghaziabad','Kottayam'])
# User input fields for custom date and time
custom_date = st.date_input('Select a date')
custom_time = st.time_input('Select a time')
# Button for real-time prediction
if st.button('Real-time Prediction'):
    # Get real-time weather data
    weather_desc, temp, hum, wind_spd = get_weather_data(location)
    if weather_desc is not None:
        st.write(f"Today's Weather: {weather_desc}")
        st.write(f"Temperature: {temp} K")
        st.write(f"Humidity: {hum}%")
        st.write(f"Wind Speed: {wind_spd} m/s")
        
        # Classify weather parameters for real-time prediction
        classification_result = classify_weather(weather_desc, temp, hum, wind_spd)
        current_weather = pd.DataFrame(classification_result)
    
        # Make prediction based on custom weather parameters
        prediction = predict(current_weather)
        st.write(f'Real-Time Prediction: {"Yes, you can play Badminton." if prediction[0] == 1 else "No, you cannot play Badminton."}')
        if prediction[0] == 1:
            st.balloons()

st.image('badgy.png')
