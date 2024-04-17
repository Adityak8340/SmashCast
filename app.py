import streamlit as st
import joblib
import numpy as np
import pandas as pd
import requests
import datetime
from dotenv import load_dotenv
import os
from datetime import datetime


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
            
            # Debugging print statements
            print("Forecast Date:", forecast_date)
            print("Weather Description:", weather_description)
            print("Temperature:", temperature)
            print("Humidity:", humidity)
            print("Wind Speed:", wind_speed)
            
            forecasts.append((forecast_date, weather_description, temperature, humidity, wind_speed))
        return forecasts
    else:
        st.error("Failed to fetch weather forecast. Please check your API key and try again.")
        return None



# Streamlit app layout
st.title('SmashCast')
st.text('Your Weather-Driven Badminton Outside Play Predictor')

st.image('badmin_img.png', width=200)

# Text input for location for real-time prediction
location = st.selectbox('Enter your city name', ['Lucknow', 'Mumbai', 'Agra', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Surat', 'Kanpur', 'Nagpur', 'Visakhapatnam', 'Indore', 'Thane', 'Bhopal', 'Patna', 'Vadodara', 'Ghaziabad','Kottayam'])
# User input fields for custom date and time
custom_date = st.date_input('Select a date')
custom_time = st.time_input('Select a time')



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
st.image('badgy.png')
