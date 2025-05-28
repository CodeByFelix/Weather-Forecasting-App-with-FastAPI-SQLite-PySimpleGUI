import sqlite3
import time
from typing import List

dbPath = "weather.db"

def get_connection ():
    return sqlite3.connect (dbPath, check_same_thread=False)

def init_db () -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    conn = get_connection ()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor ()

    cursor.execute ("""
            CREATE TABLE IF NOT EXISTS weather(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    city TEXT,
                    country TEXT,
                    description TEXT,
                    temp REAL,
                    humidity INTEGER,
                    pressure INTEGER,
                    wind REAL,
                    long REAL,
                    lat REAL
                    )
                    """)
    
    conn.commit ()

    return conn, cursor

def insert_weather_data (conn_cursor: tuple[sqlite3.Connection, sqlite3.Cursor], data:dict) -> bool:
    conn, cursor = conn_cursor

    cursor.execute ("""
                INSERT INTO weather (timestamp, city, country, description, temp, humidity, pressure, wind, long, lat)
                    VALUES (?,?,?,?,?,?,?,?,?,?)""",
                    (
                        data['timestamp'],
                        data['city'],
                        data['country'],
                        data['description'],
                        data['temp'],
                        data['humidity'],
                        data['pressure'],
                        data['wind'],
                        data['long'],
                        data['lat']
                    ))
    conn.commit()
    return cursor.rowcount > 0

def get_weather_data (conn_cursor: tuple[sqlite3.Connection, sqlite3.Cursor], timestamp: str) -> sqlite3.Row:
    conn, cursor = conn_cursor
    cursor.execute ("""SELECT * from weather WHERE timestamp = ?""",
                    (timestamp,))
    rows = cursor.fetchall()
    return rows

def get_all_weather_data (conn_cursor: tuple[sqlite3.Connection, sqlite3.Cursor]) -> List[sqlite3.Row]:
    conn, cursor = conn_cursor
    cursor.execute("""SELECT * FROM weather""")
    rows = cursor.fetchall ()
    return rows

def delete_weather_data (conn_cursor: tuple[sqlite3.Connection, sqlite3.Cursor], timestamp:str) -> bool:
    conn, cursor = conn_cursor
    cursor.execute ("DELETE FROM weather WHERE timestamp = ?", (timestamp,))
    conn.commit ()
    return cursor.rowcount > 0