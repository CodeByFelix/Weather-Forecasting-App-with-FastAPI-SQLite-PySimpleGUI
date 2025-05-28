import PySimpleGUI as sg
import requests
import time
from datetime import datetime
import pandas as pd


def getMyLocation () -> str:
    response = requests.get (GEOLOCATE_URL)
    return response.json()['city']

def updateDropDown ():
    response = requests.get ("http://127.0.0.1:8000/weather/data")
    if response.status_code == 200:
        newData = []
        data = response.json ()

        for d in data['data']:
            newData.append (d['timestamp'])
        window['_list_'].update(values=newData)

GEOLOCATE_URL = "http://ip-api.com/json/"
url = 'http://127.0.0.2:8000'

#R1 = [sg.Text ("City:")]
#R2 = [sg.Input ('City', key='_city_'), sg.Button ("Get Weather", '_get_weather_')]
dropDown = []
CC = [
    [sg.Text ("City:")],
    [sg.Input (key='_city_'), sg.Button ("Get Weather", key='_get_weather_')]
]

CC1 = [
    [sg.Text ("Select Timestamp:")],
    [sg.Combo(dropDown, size=(30, 10), key='_list_', enable_events=True), sg.Button ("Select", key='_select_timestamp_')]
]

layout = [
    [sg.Push(), sg.Column (CC1, element_justification='left'), sg.Push(), sg.Column(CC, element_justification='left'), sg.Push()],
    [sg.Text (key='_text_', font=('Any', 12, 'bold'))],
    [sg.Canvas (key='_canvas_')],
    [sg.VPush()],
    [sg.Push(), sg.Button ("Delete Record", key='_delete_'), sg.Push(), sg.Button ("Use My Location", key='_my_location_'), sg.Push(), sg.Button ("Download Weather Data", key='_download_'), sg.Push()]
]

window = sg.Window ("Weather App", layout, resizable=True, size=(1280, 960))

event, values = window.read ()
response = requests.get ("http://127.0.0.1:8000/weather/data")
updateDropDown ()
# if response.status_code == 200:
#     newData = []
#     data = response.json ()

#     for d in data['data']:
#         newData.append (d['timestamp'])
#     window['_list_'].update(values=newData)

# elif response.status_code == 404:
#     sg.Popup ("No weather record found")


while True:
    event, values = window.read ()

    if event == sg.WIN_CLOSED:
        break

    if event == '_my_location_':
        location = getMyLocation()
        #print (location)
        url = f"http://127.0.0.1:8000/weather/city/{location}"
        response = requests.get (url)
        if response.status_code == 200:
            data = response.json()
            textData = f"""
                    Weather Description of {data['city']} at {datetime.utcfromtimestamp(int(data['timestamp']))}.
                    Country: {data['country']}
                    City: {data['city']}
                    Weather Description: {data['description']}
                    Temperature: {data['temp']}°C
                    Humidity: {data['humidity']}%
                    Preasure: {data['pressure']}hPa
                    Wind Speed: {data['wind']}m/s
                    Coordinate: Lon: {data['long']}   Lat: {data['lat']}
                    
                    """
            window ['_text_'].update(value=textData)
            dd = data['timestamp']
            updateDropDown ()
            #window['_list_'].update(values=dd)
        
        else:
            sg.Popup(f"HTTP request error {response.status_code}")

    if event == '_get_weather_':
        location = values['_city_']
        url = f"http://127.0.0.1:8000/weather/city/{location}"
        response = requests.get (url)
        if response.status_code == 200:
            data = response.json()
            textData = f"""
                    Weather Description of {data['city']} at {datetime.utcfromtimestamp(int(data['timestamp']))}.
                    Country: {data['country']}
                    City: {data['city']}
                    Weather Description: {data['description']}
                    Temperature: {data['temp']}°C
                    Humidity: {data['humidity']}%
                    Preasure: {data['pressure']}hPa
                    Wind Speed: {data['wind']}m/s
                    Coordinate: Lon: {data['long']}   Lat: {data['lat']}
                    
                    """
            window ['_text_'].update(value=textData)
            dd = data['timestamp']
            updateDropDown ()
            #window['_list_'].update(values=dd)
        
        else:
            sg.Popup(f"HTTP request error {response.status_code}")

    if event == '_select_timestamp_':
        timestamp = values['_list_']
        url = f"http://127.0.0.1:8000/weather/timestamp/{timestamp}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            textData = f"""
                    Weather Description of {data['city']} at {datetime.utcfromtimestamp(int(data['timestamp']))}.
                    Country: {data['country']}
                    City: {data['city']}
                    Weather Description: {data['description']}
                    Temperature: {data['temp']}°C
                    Humidity: {data['humidity']}%
                    Preasure: {data['pressure']}hPa
                    Wind Speed: {data['wind']}m/s
                    Coordinate: Lon: {data['long']}   Lat: {data['lat']}
                    
                    """
            window ['_text_'].update(value=textData)
        else:
            sg.Popup(f"HTTP request error {response.status_code}")


    if event =='_delete_':
        timestamp = values['_list_']
        url = f"http://127.0.0.1:8000/weather/delete/{timestamp}"
        response = requests.delete(url)
        if response.status_code == 200:
            data = response.json()
            sg.popup(data['message'])
            updateDropDown ()
            window ['_text_'].update(value="")

    if event == '_download_':
        response = requests.get ("http://127.0.0.1:8000/weather/data")
        if response.status_code == 200:
            data = response.json ()['data']
            df = pd.DataFrame (data)
            dd = datetime.now().strftime("%Y%m%d%H%M%S")
            fileName = f"Weather Data {dd}.csv"
            df.to_csv(fileName, index=False)
            sg.Popup (f"Weather Data saved as {fileName}")
