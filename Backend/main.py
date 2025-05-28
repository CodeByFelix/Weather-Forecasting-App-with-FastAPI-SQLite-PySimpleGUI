from pydantic import BaseModel
from typing import List
from fastapi import FastAPI
from fastapi import HTTPException
import database
import requests

app = FastAPI()

API_KEY = "9bd69bb316dbb0f7d7f9191a596f933e"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"


class weatherData (BaseModel):
    timestamp: str
    city: str
    country: str
    description: str
    temp: float
    humidity: int
    pressure: int
    wind: float
    long: float
    lat: float

class allWeatherData (BaseModel):
    data: List[weatherData]

class querryCity (BaseModel):
    city: str

class querryTime (BaseModel):
    timestamp: str


def getWeather (location: str) -> dict:
    params = {'q': location, 'appid': API_KEY, 'units': 'metric'}
    try:
        #print (params)
        response = requests.get (BASE_URL, params=params)
    except:
        raise Exception ("Couldnt Complet Request")
    else:
        data = response.json()
        if data['cod'] != 200:
            raise Exception ("Incomplete Response")
        else:
            return {
                'timestamp': str(data['dt']),
                'country': data['sys']['country'],
                'city': data['name'],
                'description': data['weather'][0]['description'],
                'temp': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'pressure': data ['main']['pressure'],
                'wind': data['wind']['speed'],
                'long': data['coord']['lon'],
                'lat': data['coord']['lat']
            }

@app.on_event('startup')
async def app_startup ():
    app.state.db = database.init_db ()


@app.get("/weather/city/{city}", response_model=weatherData)
async def get_weather_city (city: str):
    weather = getWeather (city)
    database.insert_weather_data (app.state.db, weather)
    return weather

@app.get("/weather/timestamp/{timestamp}", response_model=weatherData)
async def get_weather_timestamp (timestamp:str):
    row = database.get_weather_data (app.state.db, timestamp)
    if row:
        return {
            "timestamp": row[0]["timestamp"],
            "city": row[0]["city"],
            "country": row[0]["country"],
            "description": row[0]["description"],
            "temp": row[0]["temp"],
            "humidity": row[0]["humidity"],
            "pressure": row[0]["pressure"],
            "wind": row[0]["wind"],
            "long": row[0]["long"],
            "lat": row[0]["lat"]
        }
    else:
        raise HTTPException(status_code=404, detail="Weather data not found")

@app.get("/weather/data", response_model=allWeatherData)
async def get_all_weather_data ():
    data = database.get_all_weather_data (app.state.db)
    if data:
        dd = [
            {
            "timestamp": row["timestamp"],
            "city": row["city"],
            "country": row["country"],
            "description": row["description"],
            "temp": row["temp"],
            "humidity": row["humidity"],
            "pressure": row["pressure"],
            "wind": row["wind"],
            "long": row["long"],
            "lat": row["lat"]
            } for row in data
        ]
        return {'data': dd}
    else:
        raise HTTPException(status_code=404, detail="Weather data not found")
    
@app.delete ("/weather/delete/{timestamp}")
async def delete_weather_data (timestamp:str):
    success = database.delete_weather_data(app.state.db, timestamp)
    if success:
        return {'message': f"Record at timestamp {timestamp} deleted sucessfully"}
    else:
        raise HTTPException (status_code=404, detail="Weather record not found")