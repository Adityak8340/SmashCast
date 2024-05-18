import streamlit as st
import joblib
import numpy as np
import pandas as pd
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import pytz

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
    if wind_speed > 3:
        weather_classification['Wind_Strong'] = [1]
    else:
        weather_classification['Wind_Weak'] = [1]
    
    return weather_classification

def get_weather_forecast(city):
    country_code = 'IN'
    api_key = os.getenv("api_key")  # Use os.getenv to fetch environment variables
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city},{country_code}&appid={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        forecasts = []
        for forecast in data.get('list', []):
            forecast_date = forecast.get('dt_txt', 'N/A')
            weather_description = forecast.get('weather', [{}])[0].get('description', 'N/A')
            temperature = forecast.get('main', {}).get('temp', 'N/A')
            humidity = forecast.get('main', {}).get('humidity', 'N/A')
            wind_speed = forecast.get('wind', {}).get('speed', 'N/A')
            
            forecasts.append((forecast_date, weather_description, temperature, humidity, wind_speed))
        return forecasts
    else:
        st.error("Failed to fetch weather forecast. Please check your API key and try again.")
        return None

# Function to find suitable time slots for playing badminton
def find_suitable_time_slots(forecasts):
    suitable_time_slots = []
    for forecast in forecasts:
        forecast_datetime_str, weather_description, temp, hum, wind_spd = forecast
        classification_result = classify_weather(weather_description, temp, hum, wind_spd)
        current_weather = pd.DataFrame(classification_result)
        prediction = predict(current_weather)
        if prediction[0] == 1:
            suitable_time_slots.append((forecast_datetime_str, weather_description, temp, hum, wind_spd))
    return suitable_time_slots

# Function to get current time in a specific time zone
def get_current_time(timezone='Asia/Kolkata'):  # Default to Indian Standard Time
    tz = pytz.timezone(timezone)
    current_time = datetime.now(tz)
    return current_time

# Get the current time
current_time = get_current_time()

# Streamlit app layout
st.title('SmashCast')
st.text('Your Weather-Driven Badminton Outside Play Predictor')

st.image('badmin_img.png', width=200)

# Text input for location for real-time prediction
location = st.selectbox('Enter your city name', ['Lucknow', 'Mumbai', 'Agra', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Surat', 'Kanpur', 'Nagpur', 'Visakhapatnam', 'Indore', 'Thane', 'Bhopal', 'Patna', 'Vadodara', 'Ghaziabad','Kottayam'])
# User input fields for custom date and time
custom_date = st.date_input('Select a date')
custom_time = st.time_input('Select a time', value=current_time)

# Function to display suitable time slots
def display_time_slots(time_slots):
    for slot in time_slots:
        slot_datetime, slot_description, slot_temp, slot_hum, slot_wind = slot
        slot_info = f"""
            <div style="border: 2px solid #4CAF50; padding: 5px; margin: 2px; border-radius: 5px; background-color: #000000; display: inline-block; width: 250px;">
                <h4>{slot_datetime}</h4>
                <p>Weather: {slot_description}</p>
                <p>Temperature: {slot_temp} K</p>
                <p>Humidity: {slot_hum}%</p>
                <p>Wind Speed: {slot_wind} m/s</p>
            </div>
        """
        st.markdown(slot_info, unsafe_allow_html=True)

# Button for real-time prediction
if st.button('Make Prediction'):
    # Get forecasted weather data
    forecasts = get_weather_forecast(location)
    if forecasts is not None:
        selected_datetime = datetime.combine(custom_date, custom_time)
        closest_forecast = None
        min_time_difference = float('inf')
        
        # Find the closest forecasted datetime to the selected datetime
        for forecast in forecasts:
            forecast_datetime_str, _, _, _, _ = forecast
            forecast_datetime = datetime.strptime(forecast_datetime_str, '%Y-%m-%d %H:%M:%S')
            time_difference = abs((forecast_datetime - selected_datetime).total_seconds())
            if time_difference < min_time_difference:
                closest_forecast = forecast
                min_time_difference = time_difference
        
        if closest_forecast is not None:
            forecast_datetime, weather_description, temp, hum, wind_spd = closest_forecast
            st.write(f"Forecast Weather: {weather_description}")
            st.write(f"Temperature: {temp} K")
            st.write(f"Humidity: {hum}%")
            st.write(f"Wind Speed: {wind_spd} m/s")

            # Classify weather parameters for real-time prediction
            classification_result = classify_weather(weather_description, temp, hum, wind_spd)
            current_weather = pd.DataFrame(classification_result)

            # Make prediction based on custom weather parameters
            prediction = predict(current_weather)
            st.write(f'Real-Time Prediction: {"Yes, you can play Badminton." if prediction[0] == 1 else "No, you cannot play Badminton."}')
            if prediction[0] == 1:
                st.balloons()
        else:
            st.error("No forecast data found for the selected datetime.")

# Button to get suitable time slots for today
if st.button('Today time-slots'):
    # Get forecasted weather data
    forecasts = get_weather_forecast(location)
    if forecasts is not None:
        today = datetime.today().date()
        today_forecasts = [f for f in forecasts if datetime.strptime(f[0], '%Y-%m-%d %H:%M:%S').date() == today]
        if today_forecasts:
            # Find and display suitable time slots for playing badminton
            suitable_time_slots = find_suitable_time_slots(today_forecasts)
            if suitable_time_slots:
                st.write("Suitable time slots for playing badminton today:")
                display_time_slots(suitable_time_slots)
            else:
                st.write("No suitable time slots found for playing badminton today.")
        else:
            st.write("No forecast data found for today.")

# Button to get suitable time slots for tomorrow
if st.button('Tomorrow time-slots'):
    # Get forecasted weather data
    forecasts = get_weather_forecast(location)
    if forecasts is not None:
        tomorrow = (datetime.today() + timedelta(days=1)).date()
        tomorrow_forecasts = [f for f in forecasts if datetime.strptime(f[0], '%Y-%m-%d %H:%M:%S').date() == tomorrow]
        if tomorrow_forecasts:
            # Find and display suitable time slots for playing badminton
            suitable_time_slots = find_suitable_time_slots(tomorrow_forecasts)
            if suitable_time_slots:
                st.write("Suitable time slots for playing badminton tomorrow:")
                display_time_slots(suitable_time_slots)
            else:
                st.write("No suitable time slots found for playing badminton tomorrow.")
        else:
            st.write("No forecast data found for tomorrow.")


# Button to get suitable time slots
if st.button('All time-slots'):
    # Get forecasted weather data
    forecasts = get_weather_forecast(location)
    if forecasts is not None:
        # Find and display suitable time slots for playing badminton
        suitable_time_slots = find_suitable_time_slots(forecasts)
        if suitable_time_slots:
            st.write("Suitable time slots for playing badminton:")
            display_time_slots(suitable_time_slots)
        else:
            st.write("No suitable time slots found for playing badminton.")



st.image('badgy.png')
