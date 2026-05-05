import pyodbc
import requests
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
conn=pyodbc.connect("DRIVER={SQL Server};""SERVER=DESKTOP-6VLO5VS\\SQLEXPRESS;""DATABASE=DW;""Trusted_Connection=yes;")


cities = ["Cairo", "London", "Dubai", "Paris", "New York"]
for city_name in cities:
    url = f"http://api.weatherapi.com/v1/forecast.json?key=686093052f1545dc820154953260305&q={city_name}&days=1"
    response = requests.get(url)
    data = response.json()

    # print((data))
    cursor=conn.cursor()
    # cursor.execute()
    hours = data['forecast']['forecastday'][0]['hour']
    # print(data['location'])
    city=data['location']['name']
    country=data['location']['country']
    lat=data['location']['lat']
    lon=data['location']['lon']
    cursor.execute("""
    SELECT city_key FROM DimCity 
    WHERE city_name = ? AND country = ?
    """, (city, country))
    row = cursor.fetchone()
    if row:
        city_key = row[0]
    else:
        cursor.execute("""
            INSERT INTO DimCity (city_name, country, latitude, longitude)
            OUTPUT INSERTED.city_key
            VALUES (?, ?, ?, ?)
        """, (city, country, lat, lon))

        city_key = cursor.fetchone()[0]
    # print(city_key)


    # print(city_key)
    # print(city)
    for h in hours:
        temp = h['temp_c']
        humidity = h['humidity']
        time = h['time']
        condition = h['condition']['text']
        cond_text = h['condition']['text']
        cond_code = h['condition']['code']
        dt = datetime.strptime(h['time'], "%Y-%m-%d %H:%M")
        date = dt.date()
        hour = dt.hour
        minute = dt.minute
        date_str = date.strftime("%Y-%m-%d")
        cursor.execute("SELECT date_key FROM DimDate WHERE full_date = ?", date_str)
        row = cursor.fetchone()

        if row:
            date_key = row[0]
        else:
            cursor.execute("""
                INSERT INTO DimDate (full_date, day, month, year, weekday, is_weekend)
                OUTPUT INSERTED.date_key
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                date_str,
                dt.day,
                dt.month,
                dt.year,
                dt.strftime("%A"),
                1 if dt.weekday() >= 5 else 0
            ))

            date_key = cursor.fetchone()[0]

        # print(date_key)



        cursor.execute("""
        SELECT condition_key FROM DimWeatherCondition
        WHERE main_condition = ? AND condition_code = ?
        """, (cond_text, cond_code))

        row = cursor.fetchone()

        if row:
            condition_key = row[0]
        else:
            cursor.execute("""
                INSERT INTO DimWeatherCondition (main_condition, description, condition_code)
                OUTPUT INSERTED.condition_key
                VALUES (?, ?, ?)
            """, (cond_text, cond_text, cond_code))

            condition_key = cursor.fetchone()[0]
        cursor.execute("""
        SELECT time_key FROM DimTime 
        WHERE hour = ? AND minute = ?
        """, (hour, minute))

        row = cursor.fetchone()

        if row:
            time_key = row[0]
        else:
            cursor.execute("""
                INSERT INTO DimTime (hour, minute)
                OUTPUT INSERTED.time_key
                VALUES (?, ?)
            """, (hour, minute))

            time_key = cursor.fetchone()[0]
        cursor.execute("""
        SELECT 1 FROM FactWeatherForecast
        WHERE city_key = ? AND date_key = ? AND time_key = ?
        """, (city_key, date_key, time_key))

        exists = cursor.fetchone()
        if not exists:
            cursor.execute("""
            INSERT INTO FactWeatherForecast (
                temperature, humidity, pressure, wind_speed,
                city_key, date_key, time_key, condition_key
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                temp,
                humidity,
                h['pressure_mb'],
                h['wind_kph'],
                city_key,
                date_key,
                time_key,
                condition_key
            ))

query=""" select c.city_name,
    d.full_date,
    t.hour,
    f.temperature,
    f.humidity
FROM FactWeatherForecast f
JOIN DimCity c ON f.city_key = c.city_key
JOIN DimDate d ON f.date_key = d.date_key
JOIN DimTime t ON f.time_key = t.time_key    """
conn.commit()
df = pd.read_sql(query, conn)

