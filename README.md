# 🌍 Weather Data Engineering Pipeline

## 📌 Project Overview

This project demonstrates an end-to-end data engineering pipeline that collects weather data from an external API, processes it, stores it in a data warehouse, and visualizes it through an interactive dashboard.

---

## 🚀 Key Features

* Extract real-time weather data from API
* Transform and clean raw data
* Load data into SQL Server Data Warehouse
* Designed using Star Schema
* Prevent duplicate records (data deduplication)
* Interactive dashboard using Streamlit
* Multi-city support

---

## 🏗️ Architecture

API → Python (ETL) → SQL Server (Data Warehouse) → Streamlit Dashboard

---

## 🧠 Data Model

### ⭐ Fact Table:

* `FactWeatherForecast`

  * temperature
  * humidity
  * pressure
  * wind_speed

### 📊 Dimension Tables:

* `DimCity` → city info
* `DimDate` → date details
* `DimTime` → hour & minute
* `DimWeatherCondition` → weather status

---

## ⚙️ Tech Stack

* Python
* Pandas
* SQL Server
* PyODBC
* Streamlit
* Matplotlib
* REST API

---

## 🔄 ETL Process

1. **Extract**
   Fetch weather data from Weather API

2. **Transform**

   * Convert timestamps to date & hour
   * Clean and structure data
   * Handle duplicates

3. **Load**

   * Insert into dimension tables
   * Insert into fact table

---

## 📊 Dashboard Features

* Select one or multiple cities
* Temperature visualization over time
* Key metrics:

  * Average temperature
  * Maximum temperature
  * Minimum temperature
* Data table view

---

## ▶️ How to Run

### 1. Run ETL script

```bash
python main.py
```

### 2. Run dashboard

```bash
streamlit run dashboard.py
```


## 📈 Future Improvements

* Automate ETL (scheduled jobs)
* Use cloud database (Azure / PostgreSQL)
* Deploy dashboard online
* Add real-time updates
* Improve UI/UX

---

## 👨‍💻 Author

Mohamed Magdy

---

## 💬 Summary

This project reflects a complete data engineering workflow, from data ingestion to visualization, simulating real-world data pipeline design.
