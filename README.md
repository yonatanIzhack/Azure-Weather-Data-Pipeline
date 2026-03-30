# 🌦️ Azure Real-Time Weather Data Pipeline

A cloud-native ETL pipeline that streams live weather data from Tel Aviv (Open-Meteo API) into Azure Cloud and visualizes it in real-time using Power BI.

## 🚀 Architecture
1. **Data Source:** Open-Meteo API (REST).
2. **Ingestion:** Python script running locally (simulating an edge device/sensor).
3. **Cloud Storage:** Azure Blob Storage (Append Blobs) for continuous data streams.
4. **Visualization:** Power BI Desktop connected to Azure via Account Key.

## 🛠️ Tech Stack
* **Python** (Requests, Azure SDK)
* **Microsoft Azure** (Blob Storage)
* **Power BI** (Data Modeling & Visualization)

## 📊 Dashboard Preview
![Dashboard Preview](dashboard_sample.png)
*(Replace this with your actual screenshot)*

## ⚙️ Setup
1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Set your environment variable: 
   `setx AZURE_WEATHER_CONNECTION_STRING "your_connection_string"`
4. Run the script: `python openWeatherStreaming.py`.

## 📜 Key Features
* **Error Handling:** Handles API timeouts and connection issues.
* **Scalability:** Uses Azure Append Blobs for efficient data growth.
* **Real-Time:** Data is pushed every 10 seconds.
