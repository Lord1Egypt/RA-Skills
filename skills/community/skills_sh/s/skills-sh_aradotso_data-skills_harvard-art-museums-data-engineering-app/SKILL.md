---
name: harvard-art-museums-data-engineering-app
description: ETL pipeline and analytics app for Harvard Art Museums API with SQL database, Streamlit UI, and Plotly visualizations
triggers:
  - build an ETL pipeline for Harvard Art Museums data
  - create analytics dashboard for museum artifacts
  - extract and transform Harvard Art Museums API data
  - set up data engineering pipeline with Streamlit
  - query Harvard Art Museums collection database
  - visualize museum artifact data with Plotly
  - implement museum data warehouse with SQL
  - analyze Harvard Art Museums collection patterns
---

# Harvard Art Museums Data Engineering App

> Skill by [ara.so](https://ara.so) — Data Skills collection.

## Overview

This project is an end-to-end data engineering and analytics application that demonstrates real-world ETL pipelines using the Harvard Art Museums API. It extracts artifact data, transforms it into relational database tables, stores it in MySQL/TiDB Cloud, and provides interactive analytics through a Streamlit dashboard with Plotly visualizations.

**Architecture Flow:** API → ETL → SQL → Analytics → Visualization

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

```bash
# Harvard Art Museums API
HARVARD_API_KEY=your_api_key_here

# Database Configuration
DB_HOST=your_database_host
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=harvard_artifacts
```

### Database Schema

The application uses three main tables with foreign key relationships:

```sql
-- Artifact Metadata Table
CREATE TABLE artifactmetadata (
    id INT PRIMARY KEY,
    title VARCHAR(500),
    culture VARCHAR(200),
    period VARCHAR(200),
    century VARCHAR(100),
    classification VARCHAR(200),
    department VARCHAR(200),
    dated VARCHAR(200),
    technique VARCHAR(500),
    medium VARCHAR(500),
    dimensions VARCHAR(500),
    credit_line TEXT,
    accession_number VARCHAR(100),
    verificationlevel INT,
    totalpageviews INT,
    totaluniquepageviews INT
);

-- Artifact Media Table
CREATE TABLE artifactmedia (
    media_id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    image_url TEXT,
    base_image_url TEXT,
    width INT,
    height INT,
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
);

-- Artifact Colors Table
CREATE TABLE artifactcolors (
    color_id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    color VARCHAR(50),
    spectrum VARCHAR(50),
    hue VARCHAR(50),
    percent FLOAT,
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
);
```

## Running the Application

```bash
# Start the Streamlit app
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Core Components

### 1. API Integration

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_artifacts(page=1, size=100):
    """Fetch artifacts from Harvard Art Museums API"""
    api_key = os.getenv('HARVARD_API_KEY')
    url = f"https://api.harvardartmuseums.org/object"
    
    params = {
        'apikey': api_key,
        'page': page,
        'size': size,
        'hasimage': 1  # Only artifacts with images
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data['records'], data['info']
    else:
        raise Exception(f"API Error: {response.status_code}")

# Fetch multiple pages with rate limiting
import time

def fetch_all_artifacts(max_pages=10):
    """Fetch artifacts with pagination"""
    all_artifacts = []
    
    for page in range(1, max_pages + 1):
        artifacts, info = fetch_artifacts(page=page)
        all_artifacts.extend(artifacts)
        print(f"Fetched page {page}/{max_pages}")
        time.sleep(1)  # Rate limiting
    
    return all_artifacts
```

### 2. ETL Pipeline

```python
import pandas as pd
import mysql.connector
from mysql.connector import Error

def transform_artifacts(raw_data):
    """Transform nested JSON to relational format"""
    metadata_list = []
    media_list = []
    colors_list = []
    
    for artifact in raw_data:
        # Extract metadata
        metadata = {
            'id': artifact.get('id'),
            'title': artifact.get('title'),
            'culture': artifact.get('culture'),
            'period': artifact.get('period'),
            'century': artifact.get('century'),
            'classification': artifact.get('classification'),
            'department': artifact.get('department'),
            'dated': artifact.get('dated'),
            'technique': artifact.get('technique'),
            'medium': artifact.get('medium'),
            'dimensions': artifact.get('dimensions'),
            'credit_line': artifact.get('creditline'),
            'accession_number': artifact.get('accessionyear'),
            'verificationlevel': artifact.get('verificationlevel'),
            'totalpageviews': artifact.get('totalpageviews', 0),
            'totaluniquepageviews': artifact.get('totaluniquepageviews', 0)
        }
        metadata_list.append(metadata)
        
        # Extract media
        if artifact.get('images'):
            for image in artifact['images']:
                media = {
                    'artifact_id': artifact.get('id'),
                    'image_url': image.get('imageurl'),
                    'base_image_url': image.get('baseimageurl'),
                    'width': image.get('width'),
                    'height': image.get('height')
                }
                media_list.append(media)
        
        # Extract colors
        if artifact.get('colors'):
            for color in artifact['colors']:
                color_data = {
                    'artifact_id': artifact.get('id'),
                    'color': color.get('color'),
                    'spectrum': color.get('spectrum'),
                    'hue': color.get('hue'),
                    'percent': color.get('percent')
                }
                colors_list.append(color_data)
    
    return (
        pd.DataFrame(metadata_list),
        pd.DataFrame(media_list),
        pd.DataFrame(colors_list)
    )

def load_to_database(metadata_df, media_df, colors_df):
    """Load transformed data into MySQL"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        
        cursor = connection.cursor()
        
        # Insert metadata (batch insert)
        metadata_insert = """
            INSERT IGNORE INTO artifactmetadata 
            (id, title, culture, period, century, classification, department, 
             dated, technique, medium, dimensions, credit_line, accession_number, 
             verificationlevel, totalpageviews, totaluniquepageviews)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(metadata_insert, metadata_df.values.tolist())
        
        # Insert media
        if not media_df.empty:
            media_insert = """
                INSERT INTO artifactmedia 
                (artifact_id, image_url, base_image_url, width, height)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.executemany(media_insert, media_df.values.tolist())
        
        # Insert colors
        if not colors_df.empty:
            colors_insert = """
                INSERT INTO artifactcolors 
                (artifact_id, color, spectrum, hue, percent)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.executemany(colors_insert, colors_df.values.tolist())
        
        connection.commit()
        print(f"Loaded {len(metadata_df)} artifacts successfully")
        
    except Error as e:
        print(f"Database Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
```

### 3. Analytics Queries

```python
def execute_query(query):
    """Execute SQL query and return results as DataFrame"""
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    
    df = pd.read_sql(query, connection)
    connection.close()
    return df

# Sample analytical queries
ANALYTICS_QUERIES = {
    "Artifacts by Culture": """
        SELECT culture, COUNT(*) as artifact_count
        FROM artifactmetadata
        WHERE culture IS NOT NULL
        GROUP BY culture
        ORDER BY artifact_count DESC
        LIMIT 20
    """,
    
    "Artifacts by Century": """
        SELECT century, COUNT(*) as count
        FROM artifactmetadata
        WHERE century IS NOT NULL
        GROUP BY century
        ORDER BY count DESC
    """,
    
    "Top Departments": """
        SELECT department, COUNT(*) as artifact_count
        FROM artifactmetadata
        WHERE department IS NOT NULL
        GROUP BY department
        ORDER BY artifact_count DESC
    """,
    
    "Color Distribution": """
        SELECT color, COUNT(*) as usage_count, AVG(percent) as avg_percentage
        FROM artifactcolors
        GROUP BY color
        ORDER BY usage_count DESC
        LIMIT 15
    """,
    
    "Most Viewed Artifacts": """
        SELECT title, culture, totalpageviews
        FROM artifactmetadata
        WHERE totalpageviews > 0
        ORDER BY totalpageviews DESC
        LIMIT 20
    """,
    
    "Artifacts with Media": """
        SELECT 
            COUNT(DISTINCT am.id) as total_artifacts,
            COUNT(DISTINCT media.artifact_id) as artifacts_with_media,
            ROUND(COUNT(DISTINCT media.artifact_id) * 100.0 / COUNT(DISTINCT am.id), 2) as percentage
        FROM artifactmetadata am
        LEFT JOIN artifactmedia media ON am.id = media.artifact_id
    """,
    
    "Classification Distribution": """
        SELECT classification, COUNT(*) as count
        FROM artifactmetadata
        WHERE classification IS NOT NULL
        GROUP BY classification
        ORDER BY count DESC
        LIMIT 15
    """
}
```

### 4. Streamlit Dashboard

```python
import streamlit as st
import plotly.express as px

def main():
    st.set_page_config(
        page_title="Harvard Art Museums Analytics",
        page_icon="🎨",
        layout="wide"
    )
    
    st.title("🎨 Harvard Art Museums Data Analytics")
    st.markdown("---")
    
    # Sidebar
    st.sidebar.header("🔧 Configuration")
    
    # ETL Section
    st.sidebar.subheader("ETL Pipeline")
    if st.sidebar.button("Run ETL Pipeline"):
        with st.spinner("Fetching data from API..."):
            artifacts = fetch_all_artifacts(max_pages=5)
            metadata_df, media_df, colors_df = transform_artifacts(artifacts)
            load_to_database(metadata_df, media_df, colors_df)
            st.success(f"✅ Loaded {len(metadata_df)} artifacts")
    
    # Analytics Section
    st.header("📊 Analytics Dashboard")
    
    query_name = st.selectbox(
        "Select Analysis",
        list(ANALYTICS_QUERIES.keys())
    )
    
    if st.button("Run Query"):
        query = ANALYTICS_QUERIES[query_name]
        
        with st.spinner("Executing query..."):
            df = execute_query(query)
        
        # Display results
        st.subheader("Query Results")
        st.dataframe(df, use_container_width=True)
        
        # Visualization
        if len(df.columns) >= 2 and len(df) > 0:
            st.subheader("Visualization")
            
            fig = px.bar(
                df,
                x=df.columns[0],
                y=df.columns[1],
                title=query_name,
                labels={df.columns[0]: df.columns[0], df.columns[1]: df.columns[1]}
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
```

## Common Patterns

### Full ETL Pipeline Execution

```python
def run_full_etl_pipeline(max_pages=10):
    """Complete ETL workflow"""
    print("Starting ETL Pipeline...")
    
    # Extract
    print("1. Extracting data from API...")
    raw_artifacts = fetch_all_artifacts(max_pages=max_pages)
    
    # Transform
    print("2. Transforming data...")
    metadata_df, media_df, colors_df = transform_artifacts(raw_artifacts)
    
    # Load
    print("3. Loading to database...")
    load_to_database(metadata_df, media_df, colors_df)
    
    print("ETL Pipeline completed successfully!")
    return metadata_df, media_df, colors_df
```

### Custom Query Execution

```python
def custom_analytics():
    """Run custom SQL queries"""
    custom_query = """
        SELECT 
            am.culture,
            am.century,
            COUNT(DISTINCT am.id) as artifact_count,
            COUNT(DISTINCT media.media_id) as image_count,
            AVG(am.totalpageviews) as avg_views
        FROM artifactmetadata am
        LEFT JOIN artifactmedia media ON am.id = media.artifact_id
        WHERE am.culture IS NOT NULL
        GROUP BY am.culture, am.century
        HAVING artifact_count > 5
        ORDER BY artifact_count DESC
    """
    
    return execute_query(custom_query)
```

## Troubleshooting

### API Rate Limiting
```python
# Add retry logic with exponential backoff
from time import sleep
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def get_session_with_retries():
    session = requests.Session()
    retry = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    return session
```

### Database Connection Issues
```python
# Test database connection
def test_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        if connection.is_connected():
            print("✅ Database connection successful")
            connection.close()
            return True
    except Error as e:
        print(f"❌ Database connection failed: {e}")
        return False
```

### Handling Missing Data
```python
def safe_transform(artifact, key, default=None):
    """Safely extract nested values"""
    return artifact.get(key, default)

# Use in transformation
metadata = {
    'id': safe_transform(artifact, 'id'),
    'title': safe_transform(artifact, 'title', 'Unknown'),
    'culture': safe_transform(artifact, 'culture', 'Unspecified')
}
```

### Memory Management for Large Datasets
```python
def batch_etl(batch_size=100, total_pages=100):
    """Process data in batches to manage memory"""
    for batch_start in range(1, total_pages, batch_size // 10):
        batch_end = min(batch_start + batch_size // 10, total_pages)
        artifacts = fetch_all_artifacts_range(batch_start, batch_end)
        metadata_df, media_df, colors_df = transform_artifacts(artifacts)
        load_to_database(metadata_df, media_df, colors_df)
        print(f"Processed pages {batch_start}-{batch_end}")
```
