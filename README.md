# 🌦️ Weather Forecast Application

A complete **Weather Forecasting Application** built using **FastAPI (Backend)**, **SQLite3 (Database)**, and **PySimpleGUI (Frontend)**. It fetches real-time weather data from the OpenWeatherMap API and stores it locally for query, analysis, and visualization.

---

## 📦 Features

- 🌍 Fetch live weather data by city or current location (IP-based)
- 🧠 Store and manage weather data locally in a SQLite3 database
- 📈 Display temperature, humidity, pressure, wind speed, and coordinates
- 📅 Query past weather records by timestamp
- 🗑️ Delete weather records by timestamp
- 🧾 Download weather data for external use
- 🧩 Simple and interactive GUI using PySimpleGUI

---

## 🗂️ Project Structure

Root/
├── Backend/
│ ├── main.py # FastAPI backend with endpoints
│ └── database.py # SQLite3 database logic
│
├── Frontend/
│ └── UI.py # PySimpleGUI user interface
│
├── weather.db # SQLite database file (auto-created)
├── README.md # Project description
└── requirements.txt # Python dependencies

yaml
Copy
Edit

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/weather-forecast-app.git
cd weather-forecast-app
2. Create a virtual environment (optional but recommended)
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Start the backend server
bash
Copy
Edit
cd Backend
uvicorn main:app --reload
Make sure main.py is in the same directory where you run the command.

5. Launch the frontend
bash
Copy
Edit
cd ../Frontend
python UI.py
🔑 Configuration
This project uses the OpenWeatherMap API. Replace the API_KEY in main.py with your own key from:

🔗 https://openweathermap.org/api

python
Copy
Edit
API_KEY = "your_api_key_here"
📥 Sample API Endpoints (FastAPI)
GET /weather/city/{city} → Get live weather and store in DB

GET /weather/timestamp/{timestamp} → Fetch weather by timestamp

GET /weather/data → Get all stored records

DELETE /weather/delete/{timestamp} → Delete a record

🛠️ Built With
FastAPI

SQLite3

PySimpleGUI

Requests

OpenWeatherMap API