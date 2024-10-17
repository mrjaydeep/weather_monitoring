import requests
import time
from datetime import datetime
import json

# Constants
API_KEY = '7a22c7478b91cd1fe676fafbc0943b5f'  # Replace this with your OpenWeatherMap API key
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
API_URL = 'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

# Convert Kelvin to Celsius
def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

# Fetch weather data from OpenWeatherMap API for a city
def fetch_weather(city):
    try:
        url = API_URL.format(city=city, api_key=API_KEY)
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching weather data for {city}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Exception during API call for {city}: {e}")
        return None

# Process and store daily weather summary (mock)
def process_weather_data():
    daily_summary = {}
    for city in CITIES:
        data = fetch_weather(city)
        if data:
            temp = kelvin_to_celsius(data['main']['temp'])
            feels_like = kelvin_to_celsius(data['main']['feels_like'])
            weather_condition = data['weather'][0]['main']
            timestamp = datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')
            
            print(f"City: {city}, Temp: {temp:.2f}C, Feels Like: {feels_like:.2f}C, Weather: {weather_condition}, Time: {timestamp}")
            
            daily_summary[city] = {
                'temp': temp,
                'feels_like': feels_like,
                'weather': weather_condition,
                'time': timestamp
            }

    return daily_summary

# Continuously fetch data every 5 minutes
def start_weather_monitoring():
    while True:
        daily_summary = process_weather_data()
        save_summary(daily_summary)
        time.sleep(300)  # Sleep for 5 minutes

# Save daily summary to a file (mock storage)
def save_summary(summary):
    with open('daily_weather_summary.json', 'w') as f:
        json.dump(summary, f)

# Sample run
process_weather_data()