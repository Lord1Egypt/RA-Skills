---
name: harvard-art-museums-etl-analytics
description: Build end-to-end ETL pipelines and analytics dashboards using the Harvard Art Museums API with Python, SQL, and Streamlit
triggers:
  - how do I fetch data from the Harvard Art Museums API
  - build an ETL pipeline for museum artifacts
  - create a Streamlit dashboard for art collection analytics
  - set up SQL database for Harvard Art Museums data
  - extract and transform Harvard Art Museums API data
  - visualize museum artifact data with Plotly
  - implement pagination for Harvard Art API
  - design relational schema for artifact metadata
---

# Harvard Art Museums ETL Analytics Skill

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This skill enables you to build production-ready ETL pipelines that extract artifact data from the Harvard Art Museums API, transform it into relational structures, load it into SQL databases, and create interactive analytics dashboards using Streamlit.

## What This Project Does

The Harvard-Artifacts-Collection-Data-Engineering-Analytics-App demonstrates a complete data engineering workflow:

1. **Extract**: Fetch artifact data from Harvard Art Museums API with pagination and rate limiting
2. **Transform**: Convert nested JSON responses into normalized relational tables
3. **Load**: Batch insert data into MySQL/TiDB databases with proper relationships
4. **Analyze**: Execute SQL queries for insights on culture, century, media, and colors
5. **Visualize**: Display results in interactive Streamlit dashboards with Plotly charts

## Installation

```bash
# Clone the repository
git clone https://github.com/Manali0711/Harvard-Artifacts-Collection-Data-Engineering-Analytics-App.git
cd Harvard-Artifacts-Collection-Data-Engineering-Analytics-App

# Install dependencies
pip install -r requirements.txt

# Required packages (if no requirements.txt)
pip install streamlit pandas requests mysql-connector-python plotly python-dotenv
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
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=harvard_artifacts
```

Get your Harvard Art Museums API key from: https://docs.google.com/forms/d/e/1FAIpQLSfkmEBqH76HLMMiCC-GPPnhcvHC9aJS86E32dOd0Z6MHEc1Cw/viewform

### Database Setup

```python
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

# Create database connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

# Create tables schema
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Artifact Metadata Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifactmetadata (
            id INT PRIMARY KEY,
            title VARCHAR(500),
            culture VARCHAR(200),
            century VARCHAR(100),
            classification VARCHAR(200),
            department VARCHAR(200),
            technique VARCHAR(300),
            medium VARCHAR(300),
            dated VARCHAR(100),
            period VARCHAR(200)
        )
    """)
    
    # Artifact Media Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifactmedia (
            media_id INT AUTO_INCREMENT PRIMARY KEY,
            artifact_id INT,
            baseimageurl VARCHAR(500),
            iiifbaseuri VARCHAR(500),
            primaryimageurl VARCHAR(500),
            imagepermissionlevel INT,
            FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
        )
    """)
    
    # Artifact Colors Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifactcolors (
            color_id INT AUTO_INCREMENT PRIMARY KEY,
            artifact_id INT,
            color VARCHAR(50),
            spectrum VARCHAR(50),
            hue VARCHAR(50),
            percent DECIMAL(5,2),
            FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

create_tables()
```

## API Integration

### Fetching Data with Pagination

```python
import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()

def fetch_artifacts(num_records=100, page_size=100):
    """
    Fetch artifacts from Harvard Art Museums API with pagination
    """
    api_key = os.getenv('HARVARD_API_KEY')
    base_url = "https://api.harvardartmuseums.org/object"
    
    all_artifacts = []
    page = 1
    
    while len(all_artifacts) < num_records:
        params = {
            'apikey': api_key,
            'size': page_size,
            'page': page,
            'hasimage': 1  # Only artifacts with images
        }
        
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            records = data.get('records', [])
            
            if not records:
                break
            
            all_artifacts.extend(records)
            print(f"Fetched page {page}: {len(records)} records")
            page += 1
            
            # Rate limiting
            time.sleep(0.5)
        else:
            print(f"Error: {response.status_code}")
            break
    
    return all_artifacts[:num_records]

# Usage
artifacts = fetch_artifacts(num_records=500, page_size=100)
print(f"Total artifacts fetched: {len(artifacts)}")
```

## ETL Pipeline Implementation

### Extract, Transform, Load

```python
import pandas as pd
from typing import List, Dict

def transform_artifacts(artifacts: List[Dict]) -> tuple:
    """
    Transform raw API data into normalized DataFrames
    """
    metadata_records = []
    media_records = []
    color_records = []
    
    for artifact in artifacts:
        # Extract metadata
        metadata_records.append({
            'id': artifact.get('id'),
            'title': artifact.get('title', '')[:500],
            'culture': artifact.get('culture', '')[:200],
            'century': artifact.get('century', '')[:100],
            'classification': artifact.get('classification', '')[:200],
            'department': artifact.get('department', '')[:200],
            'technique': artifact.get('technique', '')[:300],
            'medium': artifact.get('medium', '')[:300],
            'dated': artifact.get('dated', '')[:100],
            'period': artifact.get('period', '')[:200]
        })
        
        # Extract media information
        if artifact.get('primaryimageurl'):
            media_records.append({
                'artifact_id': artifact.get('id'),
                'baseimageurl': artifact.get('baseimageurl', '')[:500],
                'iiifbaseuri': artifact.get('iiifbaseuri', '')[:500],
                'primaryimageurl': artifact.get('primaryimageurl', '')[:500],
                'imagepermissionlevel': artifact.get('imagepermissionlevel', 0)
            })
        
        # Extract color information
        colors = artifact.get('colors', [])
        for color in colors:
            color_records.append({
                'artifact_id': artifact.get('id'),
                'color': color.get('color', '')[:50],
                'spectrum': color.get('spectrum', '')[:50],
                'hue': color.get('hue', '')[:50],
                'percent': color.get('percent', 0.0)
            })
    
    df_metadata = pd.DataFrame(metadata_records)
    df_media = pd.DataFrame(media_records)
    df_colors = pd.DataFrame(color_records)
    
    return df_metadata, df_media, df_colors

def load_to_database(df_metadata, df_media, df_colors):
    """
    Load DataFrames into SQL database using batch inserts
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Insert metadata
    metadata_tuples = list(df_metadata.itertuples(index=False, name=None))
    cursor.executemany("""
        INSERT INTO artifactmetadata 
        (id, title, culture, century, classification, department, technique, medium, dated, period)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        title=VALUES(title), culture=VALUES(culture)
    """, metadata_tuples)
    
    # Insert media
    if not df_media.empty:
        media_tuples = list(df_media.itertuples(index=False, name=None))
        cursor.executemany("""
            INSERT INTO artifactmedia 
            (artifact_id, baseimageurl, iiifbaseuri, primaryimageurl, imagepermissionlevel)
            VALUES (%s, %s, %s, %s, %s)
        """, media_tuples)
    
    # Insert colors
    if not df_colors.empty:
        color_tuples = list(df_colors.itertuples(index=False, name=None))
        cursor.executemany("""
            INSERT INTO artifactcolors 
            (artifact_id, color, spectrum, hue, percent)
            VALUES (%s, %s, %s, %s, %s)
        """, color_tuples)
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"Loaded {len(df_metadata)} metadata, {len(df_media)} media, {len(df_colors)} color records")

# Execute ETL Pipeline
artifacts = fetch_artifacts(num_records=500)
df_metadata, df_media, df_colors = transform_artifacts(artifacts)
load_to_database(df_metadata, df_media, df_colors)
```

## Analytics Queries

### Common SQL Patterns

```python
def execute_query(query: str) -> pd.DataFrame:
    """Execute SQL query and return DataFrame"""
    conn = get_db_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Top 10 cultures by artifact count
query_cultures = """
    SELECT culture, COUNT(*) as artifact_count
    FROM artifactmetadata
    WHERE culture IS NOT NULL AND culture != ''
    GROUP BY culture
    ORDER BY artifact_count DESC
    LIMIT 10
"""

# Artifacts by century
query_century = """
    SELECT century, COUNT(*) as count
    FROM artifactmetadata
    WHERE century IS NOT NULL
    GROUP BY century
    ORDER BY count DESC
"""

# Most common colors
query_colors = """
    SELECT color, COUNT(*) as frequency, AVG(percent) as avg_percent
    FROM artifactcolors
    WHERE color IS NOT NULL
    GROUP BY color
    ORDER BY frequency DESC
    LIMIT 15
"""

# Department distribution
query_departments = """
    SELECT department, COUNT(*) as total_artifacts
    FROM artifactmetadata
    WHERE department IS NOT NULL
    GROUP BY department
    ORDER BY total_artifacts DESC
"""

# Media availability
query_media = """
    SELECT 
        CASE WHEN am.artifact_id IS NOT NULL THEN 'Has Media' ELSE 'No Media' END as media_status,
        COUNT(*) as count
    FROM artifactmetadata a
    LEFT JOIN artifactmedia am ON a.id = am.artifact_id
    GROUP BY media_status
"""

# Execute examples
df_cultures = execute_query(query_cultures)
df_colors = execute_query(query_colors)
```

## Streamlit Dashboard

### Basic App Structure

```python
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Harvard Art Analytics", layout="wide")

st.title("🎨 Harvard Art Museums Analytics Dashboard")

# Sidebar for query selection
st.sidebar.header("Analytics Queries")

query_options = {
    "Top Cultures": query_cultures,
    "Century Distribution": query_century,
    "Color Analysis": query_colors,
    "Department Overview": query_departments,
    "Media Availability": query_media
}

selected_query = st.sidebar.selectbox("Select Analysis", list(query_options.keys()))

# Execute selected query
if st.button("Run Analysis"):
    with st.spinner("Executing query..."):
        df_result = execute_query(query_options[selected_query])
        
        # Display results
        st.subheader(f"Results: {selected_query}")
        st.dataframe(df_result)
        
        # Auto-generate visualization
        if len(df_result.columns) >= 2:
            fig = px.bar(
                df_result,
                x=df_result.columns[0],
                y=df_result.columns[1],
                title=selected_query
            )
            st.plotly_chart(fig, use_container_width=True)

# Data collection interface
st.sidebar.header("Data Collection")
num_records = st.sidebar.number_input("Number of records to fetch", 100, 1000, 500)

if st.sidebar.button("Fetch & Load Data"):
    with st.spinner(f"Fetching {num_records} artifacts..."):
        artifacts = fetch_artifacts(num_records=num_records)
        df_metadata, df_media, df_colors = transform_artifacts(artifacts)
        load_to_database(df_metadata, df_media, df_colors)
        st.success(f"Successfully loaded {len(df_metadata)} artifacts!")
```

### Advanced Visualization

```python
def create_color_spectrum_chart(df_colors):
    """Create interactive color spectrum visualization"""
    fig = go.Figure()
    
    for spectrum in df_colors['spectrum'].unique():
        spectrum_data = df_colors[df_colors['spectrum'] == spectrum]
        fig.add_trace(go.Bar(
            name=spectrum,
            x=spectrum_data['color'],
            y=spectrum_data['frequency']
        ))
    
    fig.update_layout(
        title="Color Distribution by Spectrum",
        barmode='stack',
        xaxis_title="Color",
        yaxis_title="Frequency"
    )
    
    return fig

# Usage in Streamlit
df_colors = execute_query(query_colors)
fig = create_color_spectrum_chart(df_colors)
st.plotly_chart(fig, use_container_width=True)
```

## Common Patterns

### Incremental Data Loading

```python
def get_max_artifact_id():
    """Get the highest artifact ID already in database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM artifactmetadata")
    max_id = cursor.fetchone()[0] or 0
    cursor.close()
    conn.close()
    return max_id

def fetch_new_artifacts():
    """Fetch only artifacts newer than what's in database"""
    max_id = get_max_artifact_id()
    
    params = {
        'apikey': os.getenv('HARVARD_API_KEY'),
        'size': 100,
        'sort': 'id',
        'sortorder': 'asc',
        'q': f'id:>{max_id}'
    }
    
    response = requests.get("https://api.harvardartmuseums.org/object", params=params)
    return response.json().get('records', [])
```

### Error Handling and Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_etl_pipeline(num_records):
    """ETL pipeline with error handling"""
    try:
        logger.info(f"Starting ETL for {num_records} records")
        artifacts = fetch_artifacts(num_records)
        
        if not artifacts:
            logger.warning("No artifacts fetched")
            return
        
        df_metadata, df_media, df_colors = transform_artifacts(artifacts)
        load_to_database(df_metadata, df_media, df_colors)
        
        logger.info("ETL pipeline completed successfully")
        
    except requests.RequestException as e:
        logger.error(f"API request failed: {e}")
    except Exception as e:
        logger.error(f"ETL pipeline error: {e}")
        raise
```

## Troubleshooting

### API Rate Limiting

If you encounter rate limit errors:

```python
from time import sleep
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def create_session_with_retries():
    session = requests.Session()
    retry = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

# Use in fetch function
session = create_session_with_retries()
response = session.get(base_url, params=params)
```

### Database Connection Issues

```python
def test_db_connection():
    """Test database connectivity"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
```

### Missing API Key

```python
def validate_config():
    """Validate required environment variables"""
    required_vars = ['HARVARD_API_KEY', 'DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
    
    print("✅ Configuration validated")

# Run at startup
validate_config()
```

## Running the Application

```bash
# Start the Streamlit dashboard
streamlit run app.py

# Run ETL pipeline standalone
python etl_pipeline.py

# Run with custom parameters
python etl_pipeline.py --records 1000 --batch-size 100
```
