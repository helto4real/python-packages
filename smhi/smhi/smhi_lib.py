"""
Module smhi_lib contains the code to get forecasts from
the Swedish weather institute (SMHI) through the open
API:s
"""
from typing import List
import abc
import json
from urllib.request import urlopen
import aiohttp

class SmhiForecast():
    """
    Class to hold forecast data
    """
    # pylint: disable=R0913
    def __init__(
            self, temperature: int, humidity: int, pressure: int,
            thunder: int, cloudiness: int, symbol: int) -> None:
        """Constructor"""

        self._temperature = temperature
        self._humidity = humidity
        self._pressure = pressure
        self._thunder = thunder
        self._cloudiness = cloudiness
        self._symbol = symbol

    @property
    def temperature(self) -> int:
        """Air temperature (Celcius)"""
        return self._temperature
    @property
    def humidity(self) -> int:
        """Air humidity (Percent)"""
        return self._humidity
    @property
    def pressure(self) -> int:
        """Air pressure (hPa)"""
        return self._pressure
    @property
    def thunder(self) -> int:
        """Chance of thunder (Percent)"""
        return self._thunder
    @property
    def cloudiness(self) -> int:
        """Cloudiness (Percent)"""
        return self._cloudiness
    @property
    def symbol(self) -> int:
        """Symbol (Percent)
            1	Clear sky
            2	Nearly clear sky
            3	Variable cloudiness
            4	Halfclear sky
            5	Cloudy sky
            6	Overcast
            7	Fog
            8	Light rain showers
            9	Moderate rain showers
            10	Heavy rain showers
            11	Thunderstorm
            12	Light sleet showers
            13	Moderate sleet showers
            14	Heavy sleet showers
            15	Light snow showers
            16	Moderate snow showers
            17	Heavy snow showers
            18	Light rain
            19	Moderate rain
            20	Heavy rain
            21	Thunder
            22	Light sleet
            23	Moderate sleet
            24	Heavy sleet
            25	Light snowfall
            26	Moderate snowfall
            27	Heavy snowfall"""
        return self._symbol

# pylint: disable=R0903
class SmhiAPIBase():
    """
    Baseclass to use as dependecy incjection pattern for easier automatic testing
    """
    @abc.abstractmethod
    def get_forecast_api(self, longitude: str, latitude: str) -> {}:
        """Override this"""
        raise NotImplementedError('users must define get_forecast to use this base class')

    @abc.abstractmethod
    async def async_get_forecast_api(self, longitude: str, latitude: str,
                                     session: aiohttp.ClientSession) -> {}:
        """Override this"""
        raise NotImplementedError('users must define get_forecast to use this base class')

# pylint: disable=R0903
class ShmiAPI(SmhiAPIBase):
    """Default implementation for SMHI api"""

    def __init__(self):
        self.url_template = "https://opendata-download-metfcst.smhi.se/api/category"\
                            "/pmp3g/version/2/geotype/point/lon/{}/lat/{}/data.json"

    def get_forecast_api(self, longitude: str, latitude: str) -> {}:
        """gets data from API"""
        api_url = self.url_template.format(longitude, latitude)

        response = urlopen(api_url)
        data = response.read().decode('utf-8')
        json_data = json.loads(data)

        return json_data

    async def async_get_forecast_api(self, longitude: str, latitude: str,
                                     session: aiohttp.ClientSession = None) -> {}:
        """gets data from API asyncronious"""
        api_url = self.url_template.format(longitude, latitude)

        if session is None:
            session = aiohttp.ClientSession()

        async with session.get(api_url) as response:
            assert response.status == 200
            data = await response.text()
            return json.loads(data)

class Smhi():
    """
    Class that use the Swedish Weather Institute (SMHI) weather forecast
    open API to return the current forecast data
    """
    def __init__(self, longitude: str, latitude: str, api: SmhiAPIBase = ShmiAPI()) -> None:
        self._longitude: str = longitude
        self._latitude: str = latitude
        self._api: SmhiAPIBase = api

    def get_forecast(self) -> List[SmhiForecast]:
        """Returns a list of forecasts. The first in list are the current one"""
        json_data = self._api.get_forecast_api(self._longitude, self._latitude)
        return _get_forecast(json_data)

    async def async_get_forecast(self, session: aiohttp.ClientSession = None) -> List[SmhiForecast]:
        """Returns a list of forecasts. The first in list are the current one"""
        json_data = await self._api.async_get_forecast_api(self._longitude, self._latitude, session)
        return _get_forecast(json_data)


def _get_forecast(api_result: dict) -> List[SmhiForecast]:
    """Converts results fråm API to SmhiForeCast list"""
    forecasts: List[SmhiForecast] = []

    # Get the parameters
    for forecast in api_result['timeSeries']:
        temperature = 0
        pressure = 0
        humidity = 0
        thunder = 0
        symbol = 0
        cloudiness = 0

        for param in forecast['parameters']:
            if param['name'] == 't':
                temperature = int(param['values'][0]) #Celcisus
            elif param['name'] == 'r':
                humidity = int(param['values'][0]) #Percent
            elif param['name'] == 'msl':
                pressure = int(param['values'][0])  #hPa
            elif param['name'] == 'tstm':
                thunder = int(param['values'][0])   #Percent
            elif param['name'] == 'tcc_mean':
                octa = int(param['values'][0])       #Cloudiness in octas
                if 0 <= octa <= 8: # Between 0 -> 8
                    cloudiness = round(100*octa/8) # Convert octas to percent
                else:
                    cloudiness = 100 #If not determined use 100%
            elif param['name'] == 'Wsymb2':
                symbol = int(param['values'][0]) #category
        forecasts.append(
            SmhiForecast(temperature, humidity, pressure, thunder, cloudiness, symbol))
    return forecasts
