---
name: harvard-artifacts-collection-data-engineering-analytics
description: Build end-to-end data pipelines with Harvard Art Museums API using ETL, SQL analytics, and Streamlit visualization
triggers:
  - build a data engineering pipeline for museum artifacts
  - create an ETL pipeline with Harvard Art Museums API
  - set up analytics dashboard for art collection data
  - extract and analyze museum artifact data
  - build Streamlit app for art museum analytics
  - create SQL database for Harvard artifacts collection
  - implement data pipeline with API integration and visualization
  - analyze art museum data with ETL and SQL
---

# Harvard Artifacts Collection Data Engineering & Analytics

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This project provides a complete data engineering pipeline that extracts artifact data from the Harvard Art Museums API, transforms it into relational structures, loads it into SQL databases, and visualizes analytics through an interactive Streamlit dashboard.

## What It Does

- **API Integration**: Connects to Harvard Art Museums API with pagination and rate limiting
- **ETL Pipeline**: Transforms nested JSON artifact data into normalized relational tables
- **SQL Storage**: Stores artifacts in MySQL/TiDB Cloud with proper schema design
- **Analytics Queries**: Executes 20+ predefined analytical SQL queries
- **Visualization**: Interactive dashboards using Streamlit and Plotly

## Installation

```bash
# Clone the repository
git clone https://github.com/Manali0711/Harvard-Artifacts-Collection-Data-Engineering-Analytics-App.git
cd Harvard-Artifacts-Collection-Data-Engineering-Analytics-App

# Install dependencies
pip install -r requirements.txt
```

### Required Dependencies

```txt
streamlit
pandas
requests
mysql-connector-python
plotly
python-dotenv
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
HARVARD_API_KEY=your_api_key_here
DB_HOST=your_database_host
DB_PORT=3306
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=harvard_artifacts
```

### API Key Setup

1. Register at [Harvard Art Museums API](https://www.harvardartmuseums.org/collections/api)
2. Obtain your API key
3. Add to `.env` file or configure in Streamlit app

### Database Schema

The application creates three main tables:

```sql
CREATE TABLE artifactmetadata (
    objectid INT PRIMARY KEY,
    title VARCHAR(500),
    culture VARCHAR(200),
    century VARCHAR(100),
    dated VARCHAR(200),
    classification VARCHAR(200),
    department VARCHAR(200),
    division VARCHAR(200),
    accessionyear INT,
    technique VARCHAR(500),
    medium VARCHAR(500),
    dimensions VARCHAR(500),
    url VARCHAR(500)
);

CREATE TABLE artifactmedia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    objectid INT,
    imageid INT,
    baseimageurl VARCHAR(500),
    iiifbaseuri VARCHAR(500),
    FOREIGN KEY (objectid) REFERENCES artifactmetadata(objectid)
);

CREATE TABLE artifactcolors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    objectid INT,
    color VARCHAR(50),
    spectrum VARCHAR(50),
    percent FLOAT,
    FOREIGN KEY (objectid) REFERENCES artifactmetadata(objectid)
);
```

## Running the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Key Components and Usage

### 1. API Data Extraction

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_artifacts(api_key, num_records=100, page_size=100):
    """
    Fetch artifacts from Harvard Art Museums API with pagination
    """
    base_url = "https://api.harvardartmuseums.org/object"
    all_records = []
    page = 1
    
    while len(all_records) < num_records:
        params = {
            'apikey': api_key,
            'size': min(page_size, num_records - len(all_records)),
            'page': page
        }
        
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            records = data.get('records', [])
            
            if not records:
                break
                
            all_records.extend(records)
            page += 1
        else:
            print(f"Error: {response.status_code}")
            break
    
    return all_records[:num_records]
```

### 2. ETL Transformation

```python
import pandas as pd

def transform_artifacts(raw_data):
    """
    Transform nested JSON into relational DataFrames
    """
    metadata_records = []
    media_records = []
    color_records = []
    
    for artifact in raw_data:
        # Extract metadata
        metadata = {
            'objectid': artifact.get('objectid'),
            'title': artifact.get('title'),
            'culture': artifact.get('culture'),
            'century': artifact.get('century'),
            'dated': artifact.get('dated'),
            'classification': artifact.get('classification'),
            'department': artifact.get('department'),
            'division': artifact.get('division'),
            'accessionyear': artifact.get('accessionyear'),
            'technique': artifact.get('technique'),
            'medium': artifact.get('medium'),
            'dimensions': artifact.get('dimensions'),
            'url': artifact.get('url')
        }
        metadata_records.append(metadata)
        
        # Extract media
        images = artifact.get('images', [])
        for image in images:
            media = {
                'objectid': artifact.get('objectid'),
                'imageid': image.get('imageid'),
                'baseimageurl': image.get('baseimageurl'),
                'iiifbaseuri': image.get('iiifbaseuri')
            }
            media_records.append(media)
        
        # Extract colors
        colors = artifact.get('colors', [])
        for color in colors:
            color_record = {
                'objectid': artifact.get('objectid'),
                'color': color.get('color'),
                'spectrum': color.get('spectrum'),
                'percent': color.get('percent')
            }
            color_records.append(color_record)
    
    return (
        pd.DataFrame(metadata_records),
        pd.DataFrame(media_records),
        pd.DataFrame(color_records)
    )
```

### 3. Database Loading

```python
import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """
    Create database connection using environment variables
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def batch_insert_dataframe(df, table_name, connection):
    """
    Efficiently insert DataFrame into SQL table
    """
    cursor = connection.cursor()
    
    # Prepare INSERT statement
    columns = ', '.join(df.columns)
    placeholders = ', '.join(['%s'] * len(df.columns))
    query = f"INSERT IGNORE INTO {table_name} ({columns}) VALUES ({placeholders})"
    
    # Convert DataFrame to list of tuples
    data = [tuple(row) for row in df.values]
    
    try:
        cursor.executemany(query, data)
        connection.commit()
        print(f"Inserted {cursor.rowcount} rows into {table_name}")
    except Error as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
    finally:
        cursor.close()
```

### 4. SQL Analytics Queries

```python
def execute_analytics_query(connection, query_name):
    """
    Execute predefined analytics queries
    """
    queries = {
        'artifacts_by_culture': """
            SELECT culture, COUNT(*) as count
            FROM artifactmetadata
            WHERE culture IS NOT NULL
            GROUP BY culture
            ORDER BY count DESC
            LIMIT 10
        """,
        
        'artifacts_by_century': """
            SELECT century, COUNT(*) as count
            FROM artifactmetadata
            WHERE century IS NOT NULL
            GROUP BY century
            ORDER BY count DESC
        """,
        
        'top_colors': """
            SELECT color, COUNT(*) as frequency, AVG(percent) as avg_percent
            FROM artifactcolors
            GROUP BY color
            ORDER BY frequency DESC
            LIMIT 10
        """,
        
        'media_coverage': """
            SELECT 
                COUNT(DISTINCT m.objectid) as artifacts_with_media,
                COUNT(DISTINCT a.objectid) as total_artifacts,
                ROUND(COUNT(DISTINCT m.objectid) * 100.0 / COUNT(DISTINCT a.objectid), 2) as coverage_percent
            FROM artifactmetadata a
            LEFT JOIN artifactmedia m ON a.objectid = m.objectid
        """,
        
        'department_distribution': """
            SELECT department, COUNT(*) as count
            FROM artifactmetadata
            WHERE department IS NOT NULL
            GROUP BY department
            ORDER BY count DESC
        """
    }
    
    cursor = connection.cursor(dictionary=True)
    cursor.execute(queries[query_name])
    results = cursor.fetchall()
    cursor.close()
    
    return pd.DataFrame(results)
```

### 5. Streamlit Dashboard

```python
import streamlit as st
import plotly.express as px

def main():
    st.set_page_config(page_title="Harvard Artifacts Analytics", layout="wide")
    st.title("🏛️ Harvard Art Museums - Data Analytics Dashboard")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("API Key", type="password", value=os.getenv('HARVARD_API_KEY', ''))
        num_records = st.number_input("Number of Records", min_value=10, max_value=1000, value=100)
        
        if st.button("Fetch & Load Data"):
            with st.spinner("Fetching artifacts..."):
                artifacts = fetch_artifacts(api_key, num_records)
                metadata_df, media_df, colors_df = transform_artifacts(artifacts)
                
                conn = get_db_connection()
                if conn:
                    batch_insert_dataframe(metadata_df, 'artifactmetadata', conn)
                    batch_insert_dataframe(media_df, 'artifactmedia', conn)
                    batch_insert_dataframe(colors_df, 'artifactcolors', conn)
                    conn.close()
                    st.success("Data loaded successfully!")
    
    # Analytics section
    st.header("📊 Analytics")
    
    query_options = {
        "Artifacts by Culture": "artifacts_by_culture",
        "Artifacts by Century": "artifacts_by_century",
        "Top Colors": "top_colors",
        "Media Coverage": "media_coverage",
        "Department Distribution": "department_distribution"
    }
    
    selected_query = st.selectbox("Select Analysis", list(query_options.keys()))
    
    if st.button("Run Analysis"):
        conn = get_db_connection()
        if conn:
            results = execute_analytics_query(conn, query_options[selected_query])
            conn.close()
            
            st.dataframe(results)
            
            # Visualization
            if len(results) > 0 and len(results.columns) >= 2:
                fig = px.bar(results, x=results.columns[0], y=results.columns[1],
                           title=selected_query)
                st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
```

## Common Patterns

### Complete ETL Workflow

```python
from dotenv import load_dotenv
import os

# Load environment
load_dotenv()

# 1. Extract
api_key = os.getenv('HARVARD_API_KEY')
raw_data = fetch_artifacts(api_key, num_records=500)

# 2. Transform
metadata_df, media_df, colors_df = transform_artifacts(raw_data)

# 3. Load
connection = get_db_connection()
batch_insert_dataframe(metadata_df, 'artifactmetadata', connection)
batch_insert_dataframe(media_df, 'artifactmedia', connection)
batch_insert_dataframe(colors_df, 'artifactcolors', connection)
connection.close()
```

### Custom Analytics Query

```python
def run_custom_query(sql_query):
    """
    Execute custom SQL query and return results
    """
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        df = pd.read_sql(sql_query, conn)
        return df
    except Error as e:
        print(f"Query error: {e}")
        return None
    finally:
        conn.close()

# Example usage
query = """
    SELECT a.century, COUNT(DISTINCT c.color) as unique_colors
    FROM artifactmetadata a
    JOIN artifactcolors c ON a.objectid = c.objectid
    WHERE a.century IS NOT NULL
    GROUP BY a.century
    ORDER BY unique_colors DESC
"""
results = run_custom_query(query)
```

## Troubleshooting

### API Rate Limiting
```python
import time

def fetch_with_retry(url, params, max_retries=3):
    for attempt in range(max_retries):
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response
        elif response.status_code == 429:
            wait_time = 2 ** attempt
            time.sleep(wait_time)
        else:
            break
    return None
```

### Database Connection Issues
- Verify `.env` file contains correct credentials
- Check database server is running and accessible
- Ensure database exists before running ETL
- Check firewall rules for remote databases (TiDB Cloud)

### Missing Data in Queries
- Some artifacts may not have all fields populated
- Use `IS NOT NULL` filters in SQL queries
- Handle null values in DataFrames: `df.fillna('')`

### Memory Issues with Large Datasets
```python
# Process in chunks
chunk_size = 100
for i in range(0, len(raw_data), chunk_size):
    chunk = raw_data[i:i+chunk_size]
    metadata_df, media_df, colors_df = transform_artifacts(chunk)
    # Load to database
```

## Advanced Usage

### Incremental Data Loading

```python
def get_max_objectid(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT MAX(objectid) FROM artifactmetadata")
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result[0] else 0

def fetch_new_artifacts(api_key, last_objectid):
    # Fetch only new artifacts not in database
    params = {
        'apikey': api_key,
        'size': 100,
        'sort': 'objectid',
        'sortorder': 'asc',
        'q': f'objectid:>{last_objectid}'
    }
    response = requests.get("https://api.harvardartmuseums.org/object", params=params)
    return response.json().get('records', [])
```

This skill enables AI agents to help developers build complete data engineering pipelines with the Harvard Art Museums API, including ETL processes, SQL analytics, and interactive visualizations.
