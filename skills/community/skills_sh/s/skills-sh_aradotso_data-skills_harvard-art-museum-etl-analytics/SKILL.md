---
name: harvard-art-museum-etl-analytics
description: Build end-to-end ETL pipelines and analytics dashboards using the Harvard Art Museums API with Python, SQL, and Streamlit
triggers:
  - build an ETL pipeline for museum data
  - create analytics dashboard for Harvard Art Museums
  - extract and transform artifact data from API
  - set up Streamlit app for art collection analytics
  - query and visualize museum artifact metadata
  - integrate Harvard Art Museums API with SQL database
  - analyze art collection data with Python and SQL
  - build data engineering pipeline for museum artifacts
---

# Harvard Art Museum ETL Analytics Skill

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This skill enables AI agents to build end-to-end data engineering and analytics applications using the Harvard Art Museums API. The project demonstrates real-world ETL pipelines, SQL database design, analytical queries, and interactive Streamlit dashboards for artifact collection data.

## What This Project Does

The Harvard Artifacts Collection Data Engineering Analytics App provides:

- **API Integration**: Fetch artifact data from Harvard Art Museums API with pagination and rate limiting
- **ETL Pipeline**: Extract, transform, and load artifact metadata, media, and color data into relational SQL tables
- **SQL Analytics**: Pre-built analytical queries for insights on artifacts, cultures, centuries, and media
- **Interactive Dashboards**: Streamlit-based UI with Plotly visualizations
- **Database Design**: Normalized schema with `artifactmetadata`, `artifactmedia`, and `artifactcolors` tables

## Installation

```bash
# Clone the repository
git clone https://github.com/Manali0711/Harvard-Artifacts-Collection-Data-Engineering-Analytics-App.git
cd Harvard-Artifacts-Collection-Data-Engineering-Analytics-App

# Install dependencies
pip install -r requirements.txt
```

**Required dependencies:**
```
streamlit
pandas
requests
mysql-connector-python
plotly
python-dotenv
```

## Configuration

### Environment Variables

Create a `.env` file or use Streamlit secrets:

```bash
# .env file
HARVARD_API_KEY=your_api_key_here
DB_HOST=your_database_host
DB_PORT=4000
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_database_name
```

### Streamlit Secrets

Alternatively, configure in `.streamlit/secrets.toml`:

```toml
HARVARD_API_KEY = "your_api_key_here"
DB_HOST = "your_database_host"
DB_PORT = 4000
DB_USER = "your_db_user"
DB_PASSWORD = "your_db_password"
DB_NAME = "your_database_name"
```

### Get Harvard Art Museums API Key

Register at: https://docs.harvardartmuseums.org/

## Running the Application

```bash
# Start the Streamlit app
streamlit run app.py

# The app will be available at http://localhost:8501
```

## Core Components

### 1. API Data Extraction

```python
import requests
import os

def fetch_artifacts(api_key, num_artifacts=100):
    """Fetch artifacts from Harvard Art Museums API with pagination"""
    base_url = "https://api.harvardartmuseums.org/object"
    artifacts = []
    page = 1
    size = 100  # Max items per page
    
    while len(artifacts) < num_artifacts:
        params = {
            'apikey': api_key,
            'size': min(size, num_artifacts - len(artifacts)),
            'page': page
        }
        
        response = requests.get(base_url, params=params)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break
            
        data = response.json()
        records = data.get('records', [])
        
        if not records:
            break
            
        artifacts.extend(records)
        page += 1
        
    return artifacts[:num_artifacts]
```

### 2. ETL Pipeline - Transform

```python
import pandas as pd

def transform_artifacts(artifacts):
    """Transform raw API data into normalized dataframes"""
    
    # Metadata table
    metadata_records = []
    media_records = []
    color_records = []
    
    for artifact in artifacts:
        artifact_id = artifact.get('id')
        
        # Extract metadata
        metadata_records.append({
            'id': artifact_id,
            'title': artifact.get('title'),
            'culture': artifact.get('culture'),
            'period': artifact.get('period'),
            'century': artifact.get('century'),
            'dated': artifact.get('dated'),
            'classification': artifact.get('classification'),
            'medium': artifact.get('medium'),
            'dimensions': artifact.get('dimensions'),
            'department': artifact.get('department'),
            'division': artifact.get('division'),
            'creditline': artifact.get('creditline')
        })
        
        # Extract media
        images = artifact.get('images', [])
        for image in images:
            media_records.append({
                'artifact_id': artifact_id,
                'image_url': image.get('baseimageurl'),
                'alt_text': image.get('alttext'),
                'height': image.get('height'),
                'width': image.get('width')
            })
        
        # Extract colors
        colors = artifact.get('colors', [])
        for color in colors:
            color_records.append({
                'artifact_id': artifact_id,
                'color_name': color.get('color'),
                'hex_value': color.get('hex'),
                'percentage': color.get('percent')
            })
    
    return (
        pd.DataFrame(metadata_records),
        pd.DataFrame(media_records),
        pd.DataFrame(color_records)
    )
```

### 3. Database Schema Setup

```python
import mysql.connector

def create_database_schema(connection):
    """Create normalized database tables"""
    cursor = connection.cursor()
    
    # Artifact Metadata Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifactmetadata (
            id INT PRIMARY KEY,
            title VARCHAR(500),
            culture VARCHAR(255),
            period VARCHAR(255),
            century VARCHAR(255),
            dated VARCHAR(255),
            classification VARCHAR(255),
            medium TEXT,
            dimensions VARCHAR(500),
            department VARCHAR(255),
            division VARCHAR(255),
            creditline TEXT
        )
    """)
    
    # Artifact Media Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifactmedia (
            id INT AUTO_INCREMENT PRIMARY KEY,
            artifact_id INT,
            image_url VARCHAR(1000),
            alt_text TEXT,
            height INT,
            width INT,
            FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
        )
    """)
    
    # Artifact Colors Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifactcolors (
            id INT AUTO_INCREMENT PRIMARY KEY,
            artifact_id INT,
            color_name VARCHAR(100),
            hex_value VARCHAR(10),
            percentage FLOAT,
            FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
        )
    """)
    
    connection.commit()
    cursor.close()
```

### 4. Load Data to SQL

```python
def load_to_database(metadata_df, media_df, colors_df, connection):
    """Batch insert dataframes into SQL database"""
    cursor = connection.cursor()
    
    # Insert metadata
    metadata_sql = """
        INSERT INTO artifactmetadata 
        (id, title, culture, period, century, dated, classification, 
         medium, dimensions, department, division, creditline)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE title=VALUES(title)
    """
    cursor.executemany(metadata_sql, metadata_df.values.tolist())
    
    # Insert media
    if not media_df.empty:
        media_sql = """
            INSERT INTO artifactmedia 
            (artifact_id, image_url, alt_text, height, width)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.executemany(media_sql, media_df.values.tolist())
    
    # Insert colors
    if not colors_df.empty:
        colors_sql = """
            INSERT INTO artifactcolors 
            (artifact_id, color_name, hex_value, percentage)
            VALUES (%s, %s, %s, %s)
        """
        cursor.executemany(colors_sql, colors_df.values.tolist())
    
    connection.commit()
    cursor.close()
```

### 5. Analytical SQL Queries

```python
# Sample analytical queries for insights

ANALYTICS_QUERIES = {
    "Artifacts by Culture": """
        SELECT culture, COUNT(*) as artifact_count
        FROM artifactmetadata
        WHERE culture IS NOT NULL
        GROUP BY culture
        ORDER BY artifact_count DESC
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
        SELECT department, COUNT(*) as total_artifacts
        FROM artifactmetadata
        GROUP BY department
        ORDER BY total_artifacts DESC
    """,
    
    "Media Availability": """
        SELECT 
            CASE WHEN EXISTS (
                SELECT 1 FROM artifactmedia m 
                WHERE m.artifact_id = a.id
            ) THEN 'Has Media' ELSE 'No Media' END as media_status,
            COUNT(*) as count
        FROM artifactmetadata a
        GROUP BY media_status
    """,
    
    "Top Colors Used": """
        SELECT color_name, COUNT(*) as usage_count, AVG(percentage) as avg_percentage
        FROM artifactcolors
        GROUP BY color_name
        ORDER BY usage_count DESC
        LIMIT 10
    """
}

def execute_analytics_query(query, connection):
    """Execute analytical query and return DataFrame"""
    return pd.read_sql(query, connection)
```

### 6. Streamlit Dashboard Integration

```python
import streamlit as st
import plotly.express as px

def create_dashboard():
    """Build interactive Streamlit dashboard"""
    st.set_page_config(page_title="Harvard Art Analytics", layout="wide")
    
    st.title("🎨 Harvard Art Museums Analytics Dashboard")
    
    # Sidebar for query selection
    query_name = st.sidebar.selectbox(
        "Select Analytics Query",
        list(ANALYTICS_QUERIES.keys())
    )
    
    # Execute query
    if st.sidebar.button("Run Query"):
        connection = get_database_connection()
        
        try:
            df = execute_analytics_query(ANALYTICS_QUERIES[query_name], connection)
            
            # Display results
            st.subheader(f"📊 {query_name}")
            st.dataframe(df, use_container_width=True)
            
            # Auto-generate visualization
            if len(df.columns) >= 2:
                fig = px.bar(
                    df, 
                    x=df.columns[0], 
                    y=df.columns[1],
                    title=f"{query_name} Visualization"
                )
                st.plotly_chart(fig, use_container_width=True)
                
        except Exception as e:
            st.error(f"Error executing query: {e}")
        finally:
            connection.close()

def get_database_connection():
    """Create database connection from environment variables"""
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
```

## Common Patterns

### Full ETL Workflow

```python
import os
from dotenv import load_dotenv

def run_full_etl_pipeline(num_artifacts=500):
    """Execute complete ETL pipeline"""
    load_dotenv()
    
    # Extract
    print("Extracting data from API...")
    api_key = os.getenv('HARVARD_API_KEY')
    artifacts = fetch_artifacts(api_key, num_artifacts)
    
    # Transform
    print("Transforming data...")
    metadata_df, media_df, colors_df = transform_artifacts(artifacts)
    
    # Load
    print("Loading to database...")
    connection = get_database_connection()
    create_database_schema(connection)
    load_to_database(metadata_df, media_df, colors_df, connection)
    connection.close()
    
    print(f"✅ ETL Complete: {len(metadata_df)} artifacts loaded")

if __name__ == "__main__":
    run_full_etl_pipeline(num_artifacts=1000)
```

### Incremental Data Updates

```python
def incremental_update(last_update_date):
    """Fetch only new artifacts since last update"""
    base_url = "https://api.harvardartmuseums.org/object"
    params = {
        'apikey': os.getenv('HARVARD_API_KEY'),
        'after': last_update_date,  # ISO format date
        'size': 100
    }
    
    response = requests.get(base_url, params=params)
    new_artifacts = response.json().get('records', [])
    
    # Process only new records
    if new_artifacts:
        metadata_df, media_df, colors_df = transform_artifacts(new_artifacts)
        connection = get_database_connection()
        load_to_database(metadata_df, media_df, colors_df, connection)
        connection.close()
```

## Troubleshooting

### API Rate Limiting

```python
import time

def fetch_with_rate_limit(api_key, num_artifacts, delay=0.5):
    """Add delay between requests to avoid rate limiting"""
    artifacts = []
    page = 1
    
    while len(artifacts) < num_artifacts:
        # Fetch page
        response = requests.get(base_url, params={'apikey': api_key, 'page': page})
        artifacts.extend(response.json().get('records', []))
        page += 1
        
        # Rate limit delay
        time.sleep(delay)
    
    return artifacts
```

### Database Connection Issues

```python
def get_database_connection_with_retry(max_retries=3):
    """Retry database connection on failure"""
    for attempt in range(max_retries):
        try:
            return mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                port=int(os.getenv('DB_PORT', 3306)),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME'),
                connect_timeout=10
            )
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
```

### Missing API Key

```python
def validate_configuration():
    """Validate all required environment variables"""
    required_vars = ['HARVARD_API_KEY', 'DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        raise ValueError(f"Missing environment variables: {', '.join(missing)}")
```

### Handling NULL Values

```python
def clean_dataframe(df):
    """Clean dataframe before database insert"""
    # Replace None with empty string for VARCHAR columns
    string_columns = df.select_dtypes(include=['object']).columns
    df[string_columns] = df[string_columns].fillna('')
    
    # Replace None with 0 for numeric columns
    numeric_columns = df.select_dtypes(include=['number']).columns
    df[numeric_columns] = df[numeric_columns].fillna(0)
    
    return df
```

## Key Commands Reference

```bash
# Run the Streamlit app
streamlit run app.py

# Run ETL pipeline programmatically
python etl_pipeline.py

# Install dependencies
pip install -r requirements.txt

# Run with custom port
streamlit run app.py --server.port 8080
```

This skill provides comprehensive guidance for building production-ready ETL pipelines and analytics dashboards using museum API data, SQL databases, and modern Python visualization tools.
