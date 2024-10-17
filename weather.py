import unittest
from unittest.mock import patch, Mock
import json
import requests

# Change this import based on your actual file name
from play import kelvin_to_celsius, fetch_weather, process_weather_data, save_summary

class TestWeatherMonitoring(unittest.TestCase):

    def test_kelvin_to_celsius(self):
        self.assertAlmostEqual(kelvin_to_celsius(273.15), 0.0)
        self.assertAlmostEqual(kelvin_to_celsius(300), 26.85)

    @patch('requests.get')
    def test_fetch_weather(self, mock_get):
        # Mock the response from the OpenWeatherMap API
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'main': {'temp': 300, 'feels_like': 295},
            'weather': [{'main': 'Clear'}],
            'dt': 1618309800,
            'name': 'Delhi'
        }
        mock_get.return_value = mock_response
        
        data = fetch_weather('Delhi')
        self.assertIsNotNone(data)
        self.assertEqual(data['name'], 'Delhi')
        self.assertAlmostEqual(kelvin_to_celsius(data['main']['temp']), 26.85, places=2)

    @patch('play.fetch_weather')
    def test_process_weather_data(self, mock_fetch):
        
        # Mock the weather data for multiple cities
        mock_fetch.side_effect = [
            {
                'main': {'temp': 300, 'feels_like': 295},
                'weather': [{'main': 'Clear'}],
                'dt': 1618309800,
                'name': 'Delhi'
            },
            {
                'main': {'temp': 310, 'feels_like': 305},
                'weather': [{'main': 'Sunny'}],
                'dt': 1618309801,
                'name': 'Mumbai'
            },
            {
                'main': {'temp': 290, 'feels_like': 285},
                'weather': [{'main': 'Mist'}],
                'dt': 1618309802,
                'name': 'Chennai'
            },
            {
                'main': {'temp': 280, 'feels_like': 278},
                'weather': [{'main': 'Clouds'}],
                'dt': 1618309803,
                'name': 'Bangalore'
            },
            {
                'main': {'temp': 320, 'feels_like': 315},
                'weather': [{'main': 'Haze'}],
                'dt': 1618309804,
                'name': 'Kolkata'
            },
            {
                'main': {'temp': 295, 'feels_like': 290},
                'weather': [{'main': 'Haze'}],
                'dt': 1618309805,
                'name': 'Hyderabad'
            },
        ]
        
        daily_summary = process_weather_data()
        self.assertEqual(len(daily_summary), 6)  # Change to 6 based on the cities
        self.assertIn('Delhi', daily_summary)
        self.assertIn('Mumbai', daily_summary)
        self.assertIn('Chennai', daily_summary)
        self.assertIn('Bangalore', daily_summary)
        self.assertIn('Kolkata', daily_summary)
        self.assertIn('Hyderabad', daily_summary)

    def test_save_summary(self):
        summary = {
            'Delhi': {
                'temp': 26.85,
                'feels_like': 22.85,
                'weather': 'Clear',
                'time': '2021-04-10 10:30:00'
            }
        }
        save_summary(summary)
        with open('daily_weather_summary.json') as f:
            loaded_summary = json.load(f)
            self.assertEqual(loaded_summary, summary)

if __name__ == '__main__':
    unittest.main()
