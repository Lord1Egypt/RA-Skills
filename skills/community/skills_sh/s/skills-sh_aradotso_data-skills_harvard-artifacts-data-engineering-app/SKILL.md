---
name: harvard-artifacts-data-engineering-app
description: Build ETL pipelines and analytics dashboards using Harvard Art Museums API with MySQL and Streamlit
triggers:
  - how do I fetch data from Harvard Art Museums API
  - build an ETL pipeline for museum artifacts
  - create analytics dashboard with Streamlit and museum data
  - query Harvard artifacts collection database
  - set up MySQL database for museum artifact data
  - visualize Harvard Art Museums data with Plotly
  - implement pagination for Harvard API requests
  - transform nested JSON artifacts into relational tables
---

# Harvard Artifacts Collection Data Engineering Analytics App

> Skill by [ara.so](https://ara.so) — Data Skills collection.

An end-to-end data engineering and analytics application that demonstrates real-world ETL pipelines using the Harvard Art Museums API. This project extracts artifact data, transforms it into relational structures, loads it into MySQL/TiDB, and provides interactive SQL-based analytics dashboards through Streamlit.

## What This Project Does

- **API Integration**: Fetches artifact data from Harvard Art Museums API with pagination and rate limiting
- **ETL Pipeline**: Transforms nested JSON into normalized relational tables (metadata, media, colors)
- **Database Management**: Stores structured data in MySQL with proper foreign key relationships
- **SQL Analytics**: Provides 20+ predefined analytical queries for insights
- **Visualization**: Interactive Plotly charts rendered in Streamlit dashboards

## Installation

```bash
# Clone the repository
git clone https://github.com/Manali0711/Harvard-Artifacts-Collection-Data-Engineering-Analytics-App.git
cd Harvard-Artifacts-Collection-Data-Engineering-Analytics-App

# Install dependencies
pip install -r requirements.txt
```

**Required packages:**
```
streamlit
pandas
requests
mysql-connector-python
plotly
python-dotenv
```

## Configuration

### 1. Harvard Art Museums API Key

Get your API key from [Harvard Art Museums API](https://www.harvardartmuseums.org/collections/api).

Create a `.env` file:
```bash
HARVARD_API_KEY=your_api_key_here
```

### 2. MySQL/TiDB Database Setup

Configure database connection in your application or `.env`:
```
DB_HOST=your_database_host
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=harvard_artifacts
```

### 3. Database Schema

Create the required tables:

```sql
CREATE TABLE artifactmetadata (
    id INT PRIMARY KEY,
    title VARCHAR(500),
    culture VARCHAR(200),
    century VARCHAR(100),
    classification VARCHAR(200),
    department VARCHAR(200),
    division VARCHAR(200),
    dated VARCHAR(200),
    accession_year INT,
    technique VARCHAR(500)
);

CREATE TABLE artifactmedia (
    media_id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    image_url VARCHAR(1000),
    media_type VARCHAR(100),
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
);

CREATE TABLE artifactcolors (
    color_id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    color_hex VARCHAR(10),
    color_percent DECIMAL(5,2),
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
);
```

## Core API Usage Patterns

### Fetching Artifacts with Pagination

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('HARVARD_API_KEY')
BASE_URL = 'https://api.harvardartmuseums.org/object'

def fetch_artifacts(page=1, size=100):
    """
    Fetch artifacts from Harvard API with pagination
    """
    params = {
        'apikey': API_KEY,
        'page': page,
        'size': size,
        'hasimage': 1  # Only artifacts with images
    }
    
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return {
            'records': data.get('records', []),
            'total_pages': data.get('info', {}).get('pages', 0),
            'total_records': data.get('info', {}).get('totalrecords', 0)
        }
    else:
        raise Exception(f"API Error: {response.status_code}")

# Fetch first 100 artifacts
result = fetch_artifacts(page=1, size=100)
print(f"Total artifacts: {result['total_records']}")
print(f"Fetched: {len(result['records'])} records")
```

### Batch Collection with Rate Limiting

```python
import time

def collect_artifacts_batch(max_pages=10, delay=1):
    """
    Collect multiple pages with rate limiting
    """
    all_artifacts = []
    
    for page in range(1, max_pages + 1):
        print(f"Fetching page {page}...")
        result = fetch_artifacts(page=page, size=100)
        all_artifacts.extend(result['records'])
        
        # Rate limiting
        if page < max_pages:
            time.sleep(delay)
    
    return all_artifacts

# Collect 1000 artifacts (10 pages)
artifacts = collect_artifacts_batch(max_pages=10, delay=1)
```

## ETL Pipeline Implementation

### Extract and Transform

```python
import pandas as pd

def transform_artifacts(artifacts):
    """
    Transform raw API data into relational structures
    """
    metadata_records = []
    media_records = []
    color_records = []
    
    for artifact in artifacts:
        # Extract metadata
        metadata = {
            'id': artifact.get('id'),
            'title': artifact.get('title', '')[:500],
            'culture': artifact.get('culture', '')[:200],
            'century': artifact.get('century', '')[:100],
            'classification': artifact.get('classification', '')[:200],
            'department': artifact.get('department', '')[:200],
            'division': artifact.get('division', '')[:200],
            'dated': artifact.get('dated', '')[:200],
            'accession_year': artifact.get('accessionyear'),
            'technique': artifact.get('technique', '')[:500]
        }
        metadata_records.append(metadata)
        
        # Extract media
        for image in artifact.get('images', []):
            media = {
                'artifact_id': artifact.get('id'),
                'image_url': image.get('baseimageurl'),
                'media_type': 'image'
            }
            media_records.append(media)
        
        # Extract colors
        for color in artifact.get('colors', []):
            color_record = {
                'artifact_id': artifact.get('id'),
                'color_hex': color.get('hex'),
                'color_percent': color.get('percent')
            }
            color_records.append(color_record)
    
    return {
        'metadata': pd.DataFrame(metadata_records),
        'media': pd.DataFrame(media_records),
        'colors': pd.DataFrame(color_records)
    }

# Transform collected artifacts
transformed = transform_artifacts(artifacts)
print(f"Metadata rows: {len(transformed['metadata'])}")
print(f"Media rows: {len(transformed['media'])}")
print(f"Colors rows: {len(transformed['colors'])}")
```

### Load to Database

```python
import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """Create database connection"""
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT', 3306),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME', 'harvard_artifacts')
    )

def load_metadata(df):
    """Batch insert metadata"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    insert_query = """
    INSERT INTO artifactmetadata 
    (id, title, culture, century, classification, department, 
     division, dated, accession_year, technique)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    title=VALUES(title), culture=VALUES(culture)
    """
    
    data = [tuple(row) for row in df.values]
    cursor.executemany(insert_query, data)
    conn.commit()
    
    cursor.close()
    conn.close()
    print(f"Inserted {cursor.rowcount} metadata records")

def load_media(df):
    """Batch insert media"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    insert_query = """
    INSERT INTO artifactmedia (artifact_id, image_url, media_type)
    VALUES (%s, %s, %s)
    """
    
    data = [tuple(row) for row in df.values]
    cursor.executemany(insert_query, data)
    conn.commit()
    
    cursor.close()
    conn.close()

def load_colors(df):
    """Batch insert colors"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    insert_query = """
    INSERT INTO artifactcolors (artifact_id, color_hex, color_percent)
    VALUES (%s, %s, %s)
    """
    
    data = [tuple(row) for row in df.values]
    cursor.executemany(insert_query, data)
    conn.commit()
    
    cursor.close()
    conn.close()

# Load transformed data
load_metadata(transformed['metadata'])
load_media(transformed['media'])
load_colors(transformed['colors'])
```

## Streamlit Dashboard Implementation

### Basic App Structure

```python
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Harvard Artifacts Analytics", layout="wide")

st.title("🏛️ Harvard Art Museums Analytics Dashboard")

# Sidebar navigation
page = st.sidebar.selectbox(
    "Select Page",
    ["Data Collection", "SQL Analytics", "Visualizations"]
)

if page == "Data Collection":
    st.header("📥 Data Collection from API")
    
    num_pages = st.number_input("Number of pages to fetch", 1, 50, 5)
    
    if st.button("Fetch Data"):
        with st.spinner("Collecting artifacts..."):
            artifacts = collect_artifacts_batch(max_pages=num_pages)
            transformed = transform_artifacts(artifacts)
            
            load_metadata(transformed['metadata'])
            load_media(transformed['media'])
            load_colors(transformed['colors'])
            
            st.success(f"✅ Loaded {len(transformed['metadata'])} artifacts")
            st.dataframe(transformed['metadata'].head())

elif page == "SQL Analytics":
    st.header("📊 SQL Analytics")
    
    # Predefined queries
    queries = {
        "Top 10 Cultures": """
            SELECT culture, COUNT(*) as count
            FROM artifactmetadata
            WHERE culture IS NOT NULL AND culture != ''
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
            SELECT department, COUNT(*) as count
            FROM artifactmetadata
            GROUP BY department
            ORDER BY count DESC
        """,
        "Media Availability": """
            SELECT 
                CASE WHEN media_id IS NULL THEN 'No Media' ELSE 'Has Media' END as media_status,
                COUNT(*) as count
            FROM artifactmetadata m
            LEFT JOIN artifactmedia am ON m.id = am.artifact_id
            GROUP BY media_status
        """
    }
    
    selected_query = st.selectbox("Select Analysis", list(queries.keys()))
    
    if st.button("Run Query"):
        conn = get_db_connection()
        df = pd.read_sql(queries[selected_query], conn)
        conn.close()
        
        st.dataframe(df)
        
        # Auto-generate chart
        if len(df.columns) == 2:
            fig = px.bar(df, x=df.columns[0], y=df.columns[1], 
                        title=selected_query)
            st.plotly_chart(fig, use_container_width=True)
```

### Advanced Analytics Query

```python
def run_color_analysis():
    """Analyze most common colors across artifacts"""
    query = """
    SELECT 
        c.color_hex,
        COUNT(DISTINCT c.artifact_id) as artifact_count,
        AVG(c.color_percent) as avg_percent
    FROM artifactcolors c
    GROUP BY c.color_hex
    HAVING artifact_count > 10
    ORDER BY artifact_count DESC
    LIMIT 20
    """
    
    conn = get_db_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    
    # Create color visualization
    fig = px.bar(df, x='color_hex', y='artifact_count',
                 color='color_hex',
                 title='Top 20 Colors in Harvard Collection')
    
    # Apply actual hex colors to bars
    fig.update_traces(marker_color=['#' + hex for hex in df['color_hex']])
    
    return fig

# In Streamlit
st.plotly_chart(run_color_analysis(), use_container_width=True)
```

## Common Patterns

### Error Handling for API Requests

```python
def safe_api_fetch(page, max_retries=3):
    """Fetch with retry logic"""
    for attempt in range(max_retries):
        try:
            result = fetch_artifacts(page=page)
            return result
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                st.error(f"Failed after {max_retries} attempts: {e}")
                return None
            time.sleep(2 ** attempt)  # Exponential backoff
```

### Data Validation

```python
def validate_artifact_data(df):
    """Validate data before loading"""
    # Remove duplicates
    df = df.drop_duplicates(subset=['id'])
    
    # Handle null IDs
    df = df[df['id'].notna()]
    
    # Truncate long strings
    for col in df.select_dtypes(include=['object']):
        max_len = 500 if col == 'title' else 200
        df[col] = df[col].astype(str).str[:max_len]
    
    return df
```

## Troubleshooting

**API Rate Limiting**: Add delays between requests (1-2 seconds recommended)
```python
time.sleep(1)  # Between API calls
```

**Database Connection Errors**: Verify credentials and firewall rules
```python
try:
    conn = get_db_connection()
    conn.ping(reconnect=True)
except Error as e:
    print(f"Database error: {e}")
```

**Memory Issues with Large Datasets**: Process in batches
```python
BATCH_SIZE = 100
for i in range(0, len(df), BATCH_SIZE):
    batch = df.iloc[i:i+BATCH_SIZE]
    load_metadata(batch)
```

**Streamlit Caching**: Use caching for expensive operations
```python
@st.cache_data(ttl=3600)
def load_analytics_data(query):
    conn = get_db_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df
```
