# Weather-Airflow-ETL-Hypothesis-Testing

### Overview

This project is a work in progress. The main goals are to learn and explore **Apache Airflow** in the context of data pipelines and **ETL (Extract, Transform, Load)** processes, as well as perform further **Analysis** such as **Hypothesis Testing**.

### Current Focus

Currently, the project revolves around extracting weather data from the **IPMA API** (https://api.ipma.pt/), processing it with basic transformations, and storing it in a **SQL database**.
At the moment, I am primarily working with the `more_features_data` table. In the future, I plan to enrich the ETL pipeline by incorporating more complex processes and more advanced data analysis techniques.

### Workflow Details

- **Data Extraction**:
  - Data is fetched from the IPMA API, which provides weather-related information such as temperature, wind direction, pressure, and more.
  
- **Data Transformation**:
  - Simple transformations are applied to the data:
    - Handling `Date` related columns.
    - Creating a `Time of Day` column.
    - Renaming Headers appropriately.
  
- **Data Loading**:
  - The transformed data is then loaded into a SQLite database for further analysis.

### Current Analysis

On the analysis side, I am using the **weather_analysis** workbook to perform hypothesis testing using **T-Tests** and **P-Values**. Specifically, I am analyzing the relationship between **Wind Direction** and **Atmospheric Pressure** to determine if there’s a statistically significant correlation between these variables. The current conclusions are extremely unsatisfying as the database has very few entries. This process is helping me both:

- **Work on my skills** by experimenting with different approaches and tools.
- **Refresh my statistical knowledge**, which has become a bit rusty since my college days!

### Future Goals

- **Gather more data** to make conclusions more robust.
- **Enhance the ETL pipeline** with more complex data processing steps, such as additional transformations, feature engineering, and better handling of edge cases.
- **Integrate machine learning models** to predict weather-related variables using the historical data collected.
- **Expand the analysis** to include more advanced statistical methods and explore relationships between additional variables.
- **Create Visualizations** to present insights in a visually appealing manner.


### DAG Visualization
<img src="airflow dag screenshot.png" width="600" />
