---
name: harvard-artifacts-data-pipeline
description: Build ETL pipelines and analytics dashboards for Harvard Art Museums API using Python, SQL, and Streamlit
triggers:
  - build a data pipeline for museum artifacts
  - fetch and analyze Harvard Art Museums data
  - create an ETL pipeline with Streamlit
  - query and visualize museum collection data
  - set up Harvard API data engineering workflow
  - analyze art museum artifacts with SQL
  - build museum collection analytics dashboard
  - extract museum data into SQL database
---

# Harvard Artifacts Data Pipeline Skill

> Skill by [ara.so](https://ara.so) — Data Skills collection.

## Overview

The Harvard Artifacts Collection Data Engineering & Analytics App is an end-to-end data pipeline that extracts artifact data from the Harvard Art Museums API, transforms it into relational tables, loads it into SQL databases, and provides interactive analytics through a Streamlit dashboard.

**Architecture Flow**: API → ETL → SQL → Analytics → Visualization

## Installation

```bash
# Clone the repository
git clone https://github.com/Manali0711/Harvard-Artifacts-Collection-Data-Engineering-Analytics-App.git
cd Harvard-Artifacts-Collection-Data-Engineering-Analytics-App

# Install dependencies
pip install -r requirements.txt
```

**Required packages**:
```txt
streamlit
pandas
requests
mysql-connector-python
plotly
python-dotenv
```

## Configuration

### 1. Harvard Art Museums API Key

Get your free API key from: https://docs.harvardartmuseums.org/

Store it in environment variables or `.env` file:

```bash
# .env
HARVARD_API_KEY=your_api_key_here
```

### 2. Database Configuration

Set up MySQL or TiDB Cloud connection:

```python
# Database connection config
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME', 'harvard_artifacts'),
    'port': int(os.getenv('DB_PORT', 3306))
}
```

## Database Schema

The pipeline creates three main tables:

```sql
-- Artifact Metadata
CREATE TABLE artifactmetadata (
    id INT PRIMARY KEY,
    title VARCHAR(500),
    culture VARCHAR(200),
    century VARCHAR(100),
    classification VARCHAR(200),
    department VARCHAR(200),
    dated VARCHAR(200),
    description TEXT,
    technique VARCHAR(500),
    medium VARCHAR(500),
    dimensions VARCHAR(500),
    creditline TEXT,
    provenance TEXT,
    division VARCHAR(200),
    totalpageviews INT,
    totaluniquepageviews INT
);

-- Artifact Media
CREATE TABLE artifactmedia (
    media_id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    baseimageurl VARCHAR(500),
    format VARCHAR(50),
    description TEXT,
    technique VARCHAR(200),
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
);

-- Artifact Colors
CREATE TABLE artifactcolors (
    color_id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    color VARCHAR(50),
    spectrum VARCHAR(50),
    hue VARCHAR(50),
    percent DECIMAL(5,2),
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
);
```

## ETL Pipeline Components

### 1. Extract Data from API

```python
import requests
import os

def fetch_artifacts(api_key, num_records=100):
    """
    Fetch artifact data from Harvard Art Museums API with pagination
    """
    base_url = "https://api.harvardartmuseums.org/object"
    all_artifacts = []
    page = 1
    size = 100  # Max per page
    
    while len(all_artifacts) < num_records:
        params = {
            'apikey': api_key,
            'size': min(size, num_records - len(all_artifacts)),
            'page': page
        }
        
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            records = data.get('records', [])
            
            if not records:
                break
                
            all_artifacts.extend(records)
            page += 1
        else:
            print(f"Error: {response.status_code}")
            break
    
    return all_artifacts[:num_records]
```

### 2. Transform Data

```python
import pandas as pd

def transform_artifacts(artifacts):
    """
    Transform nested JSON into relational dataframes
    """
    metadata_list = []
    media_list = []
    colors_list = []
    
    for artifact in artifacts:
        # Extract metadata
        metadata = {
            'id': artifact.get('id'),
            'title': artifact.get('title'),
            'culture': artifact.get('culture'),
            'century': artifact.get('century'),
            'classification': artifact.get('classification'),
            'department': artifact.get('department'),
            'dated': artifact.get('dated'),
            'description': artifact.get('description'),
            'technique': artifact.get('technique'),
            'medium': artifact.get('medium'),
            'dimensions': artifact.get('dimensions'),
            'creditline': artifact.get('creditline'),
            'provenance': artifact.get('provenance'),
            'division': artifact.get('division'),
            'totalpageviews': artifact.get('totalpageviews', 0),
            'totaluniquepageviews': artifact.get('totaluniquepageviews', 0)
        }
        metadata_list.append(metadata)
        
        # Extract media
        for media in artifact.get('images', []):
            media_list.append({
                'artifact_id': artifact.get('id'),
                'baseimageurl': media.get('baseimageurl'),
                'format': media.get('format'),
                'description': media.get('description'),
                'technique': media.get('technique')
            })
        
        # Extract colors
        for color in artifact.get('colors', []):
            colors_list.append({
                'artifact_id': artifact.get('id'),
                'color': color.get('color'),
                'spectrum': color.get('spectrum'),
                'hue': color.get('hue'),
                'percent': color.get('percent')
            })
    
    return (
        pd.DataFrame(metadata_list),
        pd.DataFrame(media_list),
        pd.DataFrame(colors_list)
    )
```

### 3. Load Data into SQL

```python
import mysql.connector
from mysql.connector import Error

def load_to_database(metadata_df, media_df, colors_df, db_config):
    """
    Load transformed data into MySQL database
    """
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        # Load metadata (batch insert)
        metadata_query = """
            INSERT INTO artifactmetadata 
            (id, title, culture, century, classification, department, dated, 
             description, technique, medium, dimensions, creditline, provenance, 
             division, totalpageviews, totaluniquepageviews)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE title=VALUES(title)
        """
        cursor.executemany(metadata_query, metadata_df.values.tolist())
        
        # Load media
        media_query = """
            INSERT INTO artifactmedia 
            (artifact_id, baseimageurl, format, description, technique)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.executemany(media_query, media_df.values.tolist())
        
        # Load colors
        colors_query = """
            INSERT INTO artifactcolors 
            (artifact_id, color, spectrum, hue, percent)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.executemany(colors_query, colors_df.values.tolist())
        
        connection.commit()
        print(f"Successfully loaded {len(metadata_df)} artifacts")
        
    except Error as e:
        print(f"Database error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
```

## Analytical SQL Queries

### Example Analytics Queries

```python
# Common analytical queries for the dashboard

ANALYTICAL_QUERIES = {
    "artifacts_by_culture": """
        SELECT culture, COUNT(*) as count
        FROM artifactmetadata
        WHERE culture IS NOT NULL
        GROUP BY culture
        ORDER BY count DESC
        LIMIT 10
    """,
    
    "artifacts_by_century": """
        SELECT century, COUNT(*) as count
        FROM artifactmetadata
        WHERE century IS NOT NULL
        GROUP BY century
        ORDER BY count DESC
    """,
    
    "media_availability": """
        SELECT 
            CASE WHEN EXISTS (
                SELECT 1 FROM artifactmedia WHERE artifact_id = am.id
            ) THEN 'With Media' ELSE 'Without Media' END as media_status,
            COUNT(*) as count
        FROM artifactmetadata am
        GROUP BY media_status
    """,
    
    "top_colors": """
        SELECT color, COUNT(*) as frequency, AVG(percent) as avg_percent
        FROM artifactcolors
        WHERE color IS NOT NULL
        GROUP BY color
        ORDER BY frequency DESC
        LIMIT 10
    """,
    
    "department_distribution": """
        SELECT department, COUNT(*) as count
        FROM artifactmetadata
        WHERE department IS NOT NULL
        GROUP BY department
        ORDER BY count DESC
    """,
    
    "most_viewed_artifacts": """
        SELECT title, culture, totalpageviews
        FROM artifactmetadata
        WHERE totalpageviews > 0
        ORDER BY totalpageviews DESC
        LIMIT 20
    """
}
```

## Streamlit Dashboard

### Main Application Structure

```python
import streamlit as st
import plotly.express as px
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def main():
    st.set_page_config(
        page_title="Harvard Artifacts Analytics",
        page_icon="🏛️",
        layout="wide"
    )
    
    st.title("🏛️ Harvard Art Museums Analytics Dashboard")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("Harvard API Key", type="password", 
                                value=os.getenv('HARVARD_API_KEY', ''))
        
        num_records = st.number_input("Records to Fetch", 
                                      min_value=10, max_value=1000, 
                                      value=100, step=10)
        
        if st.button("🔄 Run ETL Pipeline"):
            run_etl_pipeline(api_key, num_records)
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["📊 Analytics", "🗄️ Data Explorer", "📈 Visualizations"])
    
    with tab1:
        display_analytics()
    
    with tab2:
        display_data_explorer()
    
    with tab3:
        display_visualizations()

def run_etl_pipeline(api_key, num_records):
    """Execute full ETL pipeline"""
    with st.spinner("Fetching data from API..."):
        artifacts = fetch_artifacts(api_key, num_records)
        st.success(f"Fetched {len(artifacts)} artifacts")
    
    with st.spinner("Transforming data..."):
        metadata_df, media_df, colors_df = transform_artifacts(artifacts)
        st.success("Data transformed successfully")
    
    with st.spinner("Loading to database..."):
        load_to_database(metadata_df, media_df, colors_df, DB_CONFIG)
        st.success("Data loaded to database")

def display_analytics():
    """Display analytical queries and results"""
    st.header("SQL Analytics")
    
    query_name = st.selectbox("Select Analysis", list(ANALYTICAL_QUERIES.keys()))
    
    if st.button("Run Query"):
        query = ANALYTICAL_QUERIES[query_name]
        results_df = execute_query(query)
        
        st.code(query, language='sql')
        st.dataframe(results_df)
        
        # Auto-generate visualization
        if len(results_df.columns) >= 2:
            fig = px.bar(results_df, 
                        x=results_df.columns[0], 
                        y=results_df.columns[1],
                        title=query_name.replace('_', ' ').title())
            st.plotly_chart(fig, use_container_width=True)

def execute_query(query):
    """Execute SQL query and return results as DataFrame"""
    connection = mysql.connector.connect(**DB_CONFIG)
    df = pd.read_sql(query, connection)
    connection.close()
    return df

if __name__ == "__main__":
    main()
```

## Running the Application

```bash
# Set environment variables
export HARVARD_API_KEY=your_api_key
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=your_password
export DB_NAME=harvard_artifacts

# Run Streamlit app
streamlit run app.py
```

## Common Patterns

### Pattern 1: Incremental Data Loading

```python
def incremental_load(api_key, last_id=0):
    """Load only new artifacts since last run"""
    query = f"SELECT MAX(id) as max_id FROM artifactmetadata"
    result = execute_query(query)
    last_id = result['max_id'].iloc[0] or 0
    
    # Fetch only newer records
    artifacts = fetch_artifacts_after_id(api_key, last_id)
    return artifacts
```

### Pattern 2: Error Handling in ETL

```python
def safe_etl_pipeline(api_key, num_records):
    """ETL with comprehensive error handling"""
    try:
        artifacts = fetch_artifacts(api_key, num_records)
        if not artifacts:
            raise ValueError("No artifacts fetched")
        
        metadata_df, media_df, colors_df = transform_artifacts(artifacts)
        
        # Validate data
        assert not metadata_df.empty, "Metadata is empty"
        
        load_to_database(metadata_df, media_df, colors_df, DB_CONFIG)
        return True
        
    except requests.RequestException as e:
        st.error(f"API Error: {e}")
        return False
    except Error as e:
        st.error(f"Database Error: {e}")
        return False
    except Exception as e:
        st.error(f"Unexpected Error: {e}")
        return False
```

## Troubleshooting

### API Rate Limiting

```python
import time

def fetch_with_rate_limit(api_key, num_records, delay=1):
    """Fetch data with rate limiting"""
    artifacts = []
    for page in range(1, (num_records // 100) + 2):
        response = requests.get(base_url, params={'apikey': api_key, 'page': page})
        artifacts.extend(response.json().get('records', []))
        time.sleep(delay)  # Respect rate limits
    return artifacts
```

### Database Connection Issues

```python
def test_db_connection(db_config):
    """Test database connectivity"""
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Database connection successful")
            return True
    except Error as e:
        print(f"Connection failed: {e}")
        return False
```

### Missing Data Handling

```python
def safe_get(dictionary, key, default=''):
    """Safely extract values from nested JSON"""
    return dictionary.get(key, default) if dictionary else default
```

## Performance Optimization

```python
# Use batch inserts for better performance
def batch_insert(cursor, query, data, batch_size=1000):
    """Insert data in batches"""
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        cursor.executemany(query, batch)
        connection.commit()
```
