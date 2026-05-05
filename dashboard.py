import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import pyodbc

conn = pyodbc.connect(
    "DRIVER={SQL Server};SERVER=DESKTOP-6VLO5VS\\SQLEXPRESS;DATABASE=DW;Trusted_Connection=yes;"
)

query = """
SELECT 
    c.city_name,
    d.full_date,
    t.hour,
    f.temperature
FROM FactWeatherForecast f
JOIN DimCity c ON f.city_key = c.city_key
JOIN DimDate d ON f.date_key = d.date_key
JOIN DimTime t ON f.time_key = t.time_key
"""

df = pd.read_sql(query, conn)

st.title("🌍 Weather Dashboard")


selected_cities = st.multiselect(
    "Choose Cities",
    df['city_name'].unique(),
    default=df['city_name'].unique()
)

filtered = df[df['city_name'].isin(selected_cities)]


col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Avg Temp", round(filtered['temperature'].mean(), 1))

with col2:
    st.metric("Max Temp", filtered['temperature'].max())

with col3:
    st.metric("Min Temp", filtered['temperature'].min())


fig, ax = plt.subplots()

for city in selected_cities:
    city_data = filtered[filtered['city_name'] == city]
    city_data = city_data.sort_values(by='hour')

    ax.plot(city_data['hour'], city_data['temperature'], label=city)

ax.set_title("Temperature Comparison")
ax.set_xlabel("Hour")
ax.set_ylabel("Temperature")
ax.legend()

st.pyplot(fig)


st.dataframe(filtered)