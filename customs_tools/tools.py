from langchain.tools import tool
from currency_converter import CurrencyConverter
from typing import List, Dict, Any
import requests
import os

class UtilityTools:
    required_weather_keys = [
        'datetime', 'tempmax', 'tempmin', 'feelslike', 'precip', 'precipprob',
        'preciptype', 'conditions', 'description', 'humidity', 'windgust',
        'cloudcover', 'sunrise', 'sunset', 'uvindex', 'visibility', 'severerisk'
    ]

    @tool
    def currency_converter(amount: float, currency: str) -> float:
        """
        Currency converter to convert a given currency to Indian Rupees (INR).

        Args:
            amount (float): Amount of money.
            currency (str): Currency code (e.g., 'USD', 'SGD').

        Returns:
            float: Converted amount in INR.
        """
        c = CurrencyConverter()
        return c.convert(amount, currency, 'INR')

    @tool
    def weather_forecast(city: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """
        Provides weather forecast for a given city between start and end dates.

        Args:
            city (str): City name.
            start_date (str): Start date (YYYY-MM-DD).
            end_date (str): End date (YYYY-MM-DD).

        Returns:
            List[Dict[str, Any]]: Daily weather data with relevant keys.
        """
        api_key = os.getenv('WEATHER_API')
        url = (
            f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'
            f'{city}/{start_date}/{end_date}?key={api_key}'
        )
        response = requests.get(url)
        data = response.json()

        filtered_info = []
        for day in data.get('days', []):
            filtered_info.append({
                k: v for k, v in day.items()
                if k in UtilityTools.required_weather_keys
            })

        return filtered_info
