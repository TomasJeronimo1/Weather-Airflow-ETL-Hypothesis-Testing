from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import requests
import sqlite3

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 23),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'weather_etl_dag',
    default_args=default_args,
    schedule_interval='0 10,16,22 * * *',
    catchup=False
) as dag:
    
    def extract_data():
        url = "https://api.ipma.pt/open-data/observation/meteorology/stations/obs-surface.geojson"
        response = requests.get(url)
        data = response.json()

        features = data["features"]
        filtered_data = [
            feature["properties"]
            for feature in features
            if feature["properties"]["localEstacao"] == "Oeiras / Vila Fria"
        ]
        df = pd.DataFrame(filtered_data)
        df.to_csv('/tmp/extracted_weather_data.csv', index=False)

    def transform_data():
        df = pd.read_csv('/tmp/extracted_weather_data.csv')

        # Convert time column
        df["time"] = pd.to_datetime(df["time"])
        df["hour"] = df["time"].dt.hour
        df["Date"] = df["time"].dt.date
        df["Unique Time Key"] = df["time"]
        df["time"] = df["time"].dt.strftime("%H:%M:%S")

        # Categorize time of day
        def categorize_time(hour):
            if 6 <= hour < 12:
                return "Morning"
            elif 12 <= hour < 18:
                return "Afternoon"
            else:
                return "Night"
        
        df["Time of Day"] = df["hour"].apply(categorize_time)

        # Rename columns
        df = df.rename(columns={
            "intensidadeVentoKM": "Wind Intensity",
            "pressao": "Pressure",
            "localEstacao": "Weather Station",
            "precAcumulada": "Accumulated Precipitation",
            "radiacao": "Radiation",
            "time": "Time",
            "descDirVento": "Wind Direction"
        })

        # Select and reorder columns
        df = df[["Date", "Time of Day", "Time", "Wind Intensity", "Pressure", "Weather Station", "Accumulated Precipitation", "Radiation", "Wind Direction", "Unique Time Key"]]

        df.to_csv('/tmp/transformed_weather_data.csv', index=False)

    def load_data():
        con = sqlite3.connect('/mnt/c/Users/diogo/Desktop/work/ETL/weather.db')
        df = pd.read_csv('/tmp/transformed_weather_data.csv')

        existing_data_query = 'SELECT "Unique Time Key" FROM more_features_data'
        existing_data_df = pd.read_sql(existing_data_query, con)

        new_data_cleaned = df[~df["Unique Time Key"].isin(existing_data_df["Unique Time Key"])]
        new_data_cleaned.to_sql('more_features_data', con, if_exists='append', index=False)
        print(f"Appended {len(new_data_cleaned)} new rows.")
        con.close()

    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data
    )

    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data
    )

    load_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data
    )

    extract_task >> transform_task >> load_task