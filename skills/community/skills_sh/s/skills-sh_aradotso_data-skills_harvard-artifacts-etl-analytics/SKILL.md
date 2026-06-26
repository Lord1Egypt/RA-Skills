---
name: harvard-artifacts-etl-analytics
description: End-to-end ETL pipeline and analytics for Harvard Art Museums API with Streamlit dashboards
triggers:
  - build an ETL pipeline for Harvard Art Museums data
  - create a data engineering pipeline with Harvard artifacts
  - query and visualize Harvard museum collections
  - set up Harvard Art Museums API integration
  - build analytics dashboard for art museum data
  - implement SQL analytics for Harvard artifacts
  - create Streamlit app for museum data visualization
  - process Harvard Art Museums API with Python
---

# Harvard Artifacts Collection Data Engineering & Analytics

> Skill by [ara.so](https://ara.so) — Data Skills collection.

## Overview

This project provides a complete data engineering solution for the Harvard Art Museums API, featuring:
- ETL pipeline to extract, transform, and load artifact data
- SQL database schema for relational storage (MySQL/TiDB Cloud)
- 20+ predefined analytical SQL queries
- Interactive Streamlit dashboard with Plotly visualizations
- Rate-limited API pagination handling
- Batch processing for performance optimization

## Installation

```bash
# Clone the repository
git clone https://github.com/Manali0711/Harvard-Artifacts-Collection-Data-Engineering-Analytics-App.git
cd Harvard-Artifacts-Collection-Data-Engineering-Analytics-App

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export HARVARD_API_KEY="your_api_key_here"
export DB_HOST="your_database_host"
export DB_USER="your_database_user"
export DB_PASSWORD="your_database_password"
export DB_NAME="harvard_artifacts"
```

### Required Dependencies

```python
# requirements.txt typical contents
streamlit
pandas
requests
mysql-connector-python
plotly
python-dotenv
```

## Architecture

**Data Flow:** API → Extract → Transform → Load → SQL → Analytics → Visualization

### Database Schema

The project uses three main tables:

1. **artifactmetadata** - Core artifact information
2. **artifactmedia** - Media files and images
3. **artifactcolors** - Color composition data

## Configuration

### API Setup

```python
import os
import requests

# Load API key from environment
API_KEY = os.getenv('HARVARD_API_KEY')
BASE_URL = "https://api.harvardartmuseums.org/object"

# Basic API request structure
def fetch_artifacts(page=1, size=100):
    params = {
        'apikey': API_KEY,
        'page': page,
        'size': size
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()
```

### Database Connection

```python
import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """Create database connection"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None
```

## ETL Pipeline Implementation

### Extract Phase

```python
import time
import requests

def extract_artifacts(num_pages=10, page_size=100):
    """Extract artifacts with pagination and rate limiting"""
    all_artifacts = []
    
    for page in range(1, num_pages + 1):
        params = {
            'apikey': os.getenv('HARVARD_API_KEY'),
            'page': page,
            'size': page_size
        }
        
        response = requests.get(BASE_URL, params=params)
        
        if response.status_code == 200:
            data = response.json()
            artifacts = data.get('records', [])
            all_artifacts.extend(artifacts)
            print(f"Extracted page {page}: {len(artifacts)} artifacts")
        else:
            print(f"Error on page {page}: {response.status_code}")
            
        # Rate limiting
        time.sleep(0.5)
    
    return all_artifacts
```

### Transform Phase

```python
import pandas as pd

def transform_artifact_metadata(artifacts):
    """Transform raw JSON to structured metadata"""
    metadata_records = []
    
    for artifact in artifacts:
        record = {
            'artifact_id': artifact.get('id'),
            'title': artifact.get('title'),
            'culture': artifact.get('culture'),
            'century': artifact.get('century'),
            'classification': artifact.get('classification'),
            'medium': artifact.get('medium'),
            'department': artifact.get('department'),
            'division': artifact.get('division'),
            'dated': artifact.get('dated'),
            'accession_year': artifact.get('accessionyear'),
            'object_number': artifact.get('objectnumber')
        }
        metadata_records.append(record)
    
    return pd.DataFrame(metadata_records)

def transform_artifact_media(artifacts):
    """Extract media/image information"""
    media_records = []
    
    for artifact in artifacts:
        artifact_id = artifact.get('id')
        images = artifact.get('images', [])
        
        for img in images:
            media_record = {
                'artifact_id': artifact_id,
                'media_id': img.get('iiifbaseuri'),
                'image_url': img.get('baseimageurl'),
                'format': img.get('format'),
                'width': img.get('width'),
                'height': img.get('height')
            }
            media_records.append(media_record)
    
    return pd.DataFrame(media_records)

def transform_artifact_colors(artifacts):
    """Extract color composition data"""
    color_records = []
    
    for artifact in artifacts:
        artifact_id = artifact.get('id')
        colors = artifact.get('colors', [])
        
        for color in colors:
            color_record = {
                'artifact_id': artifact_id,
                'color': color.get('color'),
                'spectrum': color.get('spectrum'),
                'percent': color.get('percent'),
                'css3': color.get('css3')
            }
            color_records.append(color_record)
    
    return pd.DataFrame(color_records)
```

### Load Phase

```python
def load_to_database(df, table_name, connection):
    """Batch insert DataFrame into SQL table"""
    cursor = connection.cursor()
    
    # Create table if not exists
    if table_name == 'artifactmetadata':
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS artifactmetadata (
            artifact_id INT PRIMARY KEY,
            title TEXT,
            culture VARCHAR(255),
            century VARCHAR(100),
            classification VARCHAR(255),
            medium TEXT,
            department VARCHAR(255),
            division VARCHAR(255),
            dated VARCHAR(255),
            accession_year INT,
            object_number VARCHAR(255)
        )
        """
        cursor.execute(create_table_sql)
    
    # Batch insert
    cols = ','.join(df.columns)
    placeholders = ','.join(['%s'] * len(df.columns))
    insert_sql = f"INSERT IGNORE INTO {table_name} ({cols}) VALUES ({placeholders})"
    
    data_tuples = [tuple(row) for row in df.values]
    cursor.executemany(insert_sql, data_tuples)
    
    connection.commit()
    print(f"Loaded {cursor.rowcount} rows into {table_name}")
    cursor.close()
```

## Analytics SQL Queries

### Example Analytical Queries

```python
# Sample queries for the analytics dashboard
ANALYTICS_QUERIES = {
    "Artifacts by Culture": """
        SELECT culture, COUNT(*) as count
        FROM artifactmetadata
        WHERE culture IS NOT NULL
        GROUP BY culture
        ORDER BY count DESC
        LIMIT 10
    """,
    
    "Artifacts by Century": """
        SELECT century, COUNT(*) as count
        FROM artifactmetadata
        WHERE century IS NOT NULL
        GROUP BY century
        ORDER BY count DESC
    """,
    
    "Department Distribution": """
        SELECT department, COUNT(*) as artifact_count
        FROM artifactmetadata
        GROUP BY department
        ORDER BY artifact_count DESC
    """,
    
    "Media Availability": """
        SELECT 
            CASE WHEN m.artifact_id IS NOT NULL THEN 'Has Media' ELSE 'No Media' END as media_status,
            COUNT(*) as count
        FROM artifactmetadata a
        LEFT JOIN artifactmedia m ON a.artifact_id = m.artifact_id
        GROUP BY media_status
    """,
    
    "Top Colors Used": """
        SELECT color, COUNT(*) as frequency, AVG(percent) as avg_percent
        FROM artifactcolors
        WHERE color IS NOT NULL
        GROUP BY color
        ORDER BY frequency DESC
        LIMIT 15
    """,
    
    "Artifacts by Classification": """
        SELECT classification, COUNT(*) as count
        FROM artifactmetadata
        WHERE classification IS NOT NULL
        GROUP BY classification
        ORDER BY count DESC
        LIMIT 10
    """
}

def execute_analytics_query(query_name, connection):
    """Execute analytical query and return results"""
    cursor = connection.cursor(dictionary=True)
    query = ANALYTICS_QUERIES[query_name]
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return pd.DataFrame(results)
```

## Streamlit Dashboard

### Main Application Structure

```python
import streamlit as st
import plotly.express as px

def main():
    st.set_page_config(page_title="Harvard Artifacts Analytics", layout="wide")
    st.title("🏛️ Harvard Art Museums - Data Analytics Dashboard")
    
    # Sidebar configuration
    st.sidebar.header("Configuration")
    
    # ETL Section
    if st.sidebar.button("Run ETL Pipeline"):
        with st.spinner("Running ETL..."):
            run_etl_pipeline()
            st.success("ETL completed successfully!")
    
    # Analytics Section
    st.header("📊 Analytics Queries")
    
    query_options = list(ANALYTICS_QUERIES.keys())
    selected_query = st.selectbox("Select Analysis", query_options)
    
    if st.button("Run Query"):
        connection = get_db_connection()
        if connection:
            df_results = execute_analytics_query(selected_query, connection)
            
            # Display results
            st.subheader("Query Results")
            st.dataframe(df_results)
            
            # Visualize
            if len(df_results.columns) >= 2:
                fig = px.bar(
                    df_results,
                    x=df_results.columns[0],
                    y=df_results.columns[1],
                    title=selected_query
                )
                st.plotly_chart(fig, use_container_width=True)
            
            connection.close()

def run_etl_pipeline():
    """Complete ETL pipeline execution"""
    # Extract
    artifacts = extract_artifacts(num_pages=5)
    
    # Transform
    df_metadata = transform_artifact_metadata(artifacts)
    df_media = transform_artifact_media(artifacts)
    df_colors = transform_artifact_colors(artifacts)
    
    # Load
    connection = get_db_connection()
    if connection:
        load_to_database(df_metadata, 'artifactmetadata', connection)
        load_to_database(df_media, 'artifactmedia', connection)
        load_to_database(df_colors, 'artifactcolors', connection)
        connection.close()

if __name__ == "__main__":
    main()
```

### Running the Dashboard

```bash
# Start the Streamlit application
streamlit run app.py

# Access at http://localhost:8501
```

## Common Patterns

### Error Handling in ETL

```python
def safe_extract(num_pages=10):
    """Extract with error handling"""
    artifacts = []
    failed_pages = []
    
    for page in range(1, num_pages + 1):
        try:
            response = requests.get(
                BASE_URL,
                params={'apikey': os.getenv('HARVARD_API_KEY'), 'page': page},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            artifacts.extend(data.get('records', []))
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch page {page}: {e}")
            failed_pages.append(page)
        except Exception as e:
            print(f"Unexpected error on page {page}: {e}")
            failed_pages.append(page)
        
        time.sleep(0.5)
    
    return artifacts, failed_pages
```

### Data Quality Checks

```python
def validate_data(df, table_name):
    """Validate transformed data before loading"""
    issues = []
    
    # Check for nulls in primary key
    if table_name == 'artifactmetadata':
        null_ids = df['artifact_id'].isnull().sum()
        if null_ids > 0:
            issues.append(f"{null_ids} null artifact_ids found")
    
    # Check for duplicates
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        issues.append(f"{duplicates} duplicate rows found")
    
    # Data type validation
    if 'accession_year' in df.columns:
        invalid_years = df[~df['accession_year'].between(1800, 2030, na=True)]
        if len(invalid_years) > 0:
            issues.append(f"{len(invalid_years)} invalid accession years")
    
    return issues
```

## Troubleshooting

### API Rate Limiting

```python
# If hitting rate limits, increase sleep time
import time

def extract_with_backoff(page, max_retries=3):
    """Extract with exponential backoff"""
    for attempt in range(max_retries):
        try:
            response = requests.get(BASE_URL, params={'apikey': os.getenv('HARVARD_API_KEY'), 'page': page})
            if response.status_code == 429:  # Too Many Requests
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(wait_time)
                continue
            return response.json()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
```

### Database Connection Issues

```python
# Test database connectivity
def test_connection():
    """Test database connection"""
    try:
        conn = get_db_connection()
        if conn and conn.is_connected():
            print("✓ Database connection successful")
            cursor = conn.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"MySQL Version: {version[0]}")
            cursor.close()
            conn.close()
            return True
    except Error as e:
        print(f"✗ Connection failed: {e}")
        return False
```

### Memory Management for Large Datasets

```python
def load_in_chunks(df, table_name, connection, chunk_size=1000):
    """Load large DataFrames in chunks"""
    total_rows = len(df)
    
    for start_idx in range(0, total_rows, chunk_size):
        end_idx = min(start_idx + chunk_size, total_rows)
        chunk = df.iloc[start_idx:end_idx]
        load_to_database(chunk, table_name, connection)
        print(f"Loaded chunk {start_idx}-{end_idx} of {total_rows}")
```

## Best Practices

1. **Always use environment variables** for sensitive credentials
2. **Implement rate limiting** when calling the Harvard API
3. **Validate data** before loading to database
4. **Use batch inserts** for better performance
5. **Handle missing values** appropriately in transformations
6. **Log ETL operations** for debugging and monitoring
7. **Create database indexes** on frequently queried columns
