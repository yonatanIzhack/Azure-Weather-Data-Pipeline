import requests
import time
import os
from datetime import datetime
from azure.storage.blob import BlobServiceClient

# --- הגדרות ---
# וודא שהרצת ב-CMD: setx AZURE_STORAGE_CONNECTION_STRING "your_connection_string"
CONNECTION_STRING = os.environ.get("AZURE_WEATHER_CONNECTION_STRING")
CONTAINER_NAME = "weather" 
BLOB_NAME = "tel_aviv_weather.csv"

def get_weather():
    """משיכת נתוני מזג אוויר נוכחיים לתל אביב"""
    url = "https://api.open-meteo.com/v1/forecast?latitude=32.0853&longitude=34.7818&current=temperature_2m,relative_humidity_2m,apparent_temperature&timezone=auto"
    try:
        response = requests.get(url)
        response.raise_for_status()
        res = response.json()['current']
        
        # יצירת שורת הנתונים
        return {
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Temp": res["temperature_2m"],
            "FeelsLike": res["apparent_temperature"],
            "Humidity": res["relative_humidity_2m"]
        }
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def main():
    if not CONNECTION_STRING:
        print("Error: Connection String not found in environment variables!")
        return

    # התחברות ל-Azure
    service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    
    # --- חדש! בדיקה ויצירה של הקונטיינר ---
    container_client = service_client.get_container_client(CONTAINER_NAME)
    try:
        if not container_client.exists():
            print(f"Container '{CONTAINER_NAME}' not found. Creating it...")
            container_client.create_container()
    except Exception as e:
        print(f"Could not verify/create container: {e}")
        return
    # --------------------------------------

    blob_client = service_client.get_blob_client(container=CONTAINER_NAME, blob=BLOB_NAME)

    # יצירת הקובץ עם כותרות אם הוא לא קיים
    if not blob_client.exists():
        headers = "Time,Temp,FeelsLike,Humidity\n"
        blob_client.create_append_blob()
        blob_client.append_block(headers)
        print(f"Created new CSV blob: {BLOB_NAME}")

    print(f"Streaming started to {BLOB_NAME}. Press Ctrl+C to stop...")
    
    try:
        while True:
            data = get_weather()
            if data:
                csv_line = f"{data['Time']},{data['Temp']},{data['FeelsLike']},{data['Humidity']}\n"
                blob_client.append_block(csv_line)
                print(f"[{data['Time']}] Appended data successfully.")
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    main()
