---
name: harvard-art-museums-data-pipeline
description: Build ETL pipelines and analytics dashboards using the Harvard Art Museums API with Python, SQL, and Streamlit
triggers:
  - build a data pipeline for museum artifacts
  - create ETL workflow with Harvard Art Museums API
  - visualize art museum data with Streamlit
  - analyze artifact metadata with SQL queries
  - set up museum data engineering project
  - extract and transform Harvard Art Museums data
  - build analytics dashboard for cultural artifacts
  - query museum artifact collections programmatically
---

# Harvard Art Museums Data Pipeline

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This skill enables building end-to-end data engineering pipelines using the Harvard Art Museums API. The project demonstrates ETL workflows, SQL database design, analytical querying, and interactive visualization with Streamlit.

## What It Does

The Harvard-Artifacts-Collection-Data-Engineering-Analytics-App provides:

- **API Integration**: Fetches artifact data from Harvard Art Museums API with pagination and rate limiting
- **ETL Pipeline**: Extracts nested JSON, transforms to relational format, loads into SQL databases
- **Database Schema**: Normalizes data into `artifactmetadata`, `artifactmedia`, and `artifactcolors` tables
- **Analytics Engine**: Executes 20+ predefined SQL queries for insights
- **Visualization Dashboard**: Interactive Streamlit interface with Plotly charts

## Installation

### Prerequisites

```bash
# Python 3.8+
python --version

# MySQL or TiDB Cloud account
```

### Setup

```bash
# Clone repository
git clone https://github.com/Manali0711/Harvard-Artifacts-Collection-Data-Engineering-Analytics-App.git
cd Harvard-Artifacts-Collection-Data-Engineering-Analytics-App

# Install dependencies
pip install -r requirements.txt

# Create .env file for configuration
cat > .env << EOF
HARVARD_API_KEY=your_api_key_here
DB_HOST=your_database_host
DB_PORT=3306
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=harvard_artifacts
EOF
```

### Required Dependencies

```txt
streamlit>=1.25.0
pandas>=2.0.0
requests>=2.31.0
mysql-connector-python>=8.0.33
plotly>=5.14.0
python-dotenv>=1.0.0
```

## Configuration

### API Key Setup

Get your Harvard Art Museums API key from: https://harvardartmuseums.org/collections/api

```python
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('HARVARD_API_KEY')
BASE_URL = "https://api.harvardartmuseums.org/object"
```

### Database Connection

```python
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_connection():
    """Establish MySQL database connection"""
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
```

## Key Components

### 1. Extract Data from API

```python
import requests
import pandas as pd

def extract_artifacts(api_key, num_pages=5, page_size=100):
    """
    Extract artifact data from Harvard Art Museums API
    
    Args:
        api_key: Harvard API key
        num_pages: Number of pages to fetch
        page_size: Records per page (max 100)
    
    Returns:
        List of artifact dictionaries
    """
    artifacts = []
    base_url = "https://api.harvardartmuseums.org/object"
    
    for page in range(1, num_pages + 1):
        params = {
            'apikey': api_key,
            'size': page_size,
            'page': page,
            'hasimage': 1  # Only artifacts with images
        }
        
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            artifacts.extend(data.get('records', []))
            print(f"Fetched page {page}: {len(data.get('records', []))} records")
        else:
            print(f"Error on page {page}: {response.status_code}")
            break
    
    return artifacts
```

### 2. Transform to Relational Schema

```python
def transform_artifacts(raw_artifacts):
    """
    Transform nested JSON to normalized dataframes
    
    Returns:
        tuple: (metadata_df, media_df, colors_df)
    """
    metadata_list = []
    media_list = []
    colors_list = []
    
    for artifact in raw_artifacts:
        artifact_id = artifact.get('id')
        
        # Metadata table
        metadata_list.append({
            'artifact_id': artifact_id,
            'title': artifact.get('title'),
            'culture': artifact.get('culture'),
            'century': artifact.get('century'),
            'dated': artifact.get('dated'),
            'department': artifact.get('department'),
            'classification': artifact.get('classification'),
            'medium': artifact.get('medium'),
            'dimensions': artifact.get('dimensions'),
            'creditline': artifact.get('creditline'),
            'accession_number': artifact.get('accessionyear')
        })
        
        # Media table
        if artifact.get('primaryimageurl'):
            media_list.append({
                'artifact_id': artifact_id,
                'media_type': 'image',
                'media_url': artifact.get('primaryimageurl'),
                'is_primary': True
            })
        
        # Colors table
        for color in artifact.get('colors', []):
            colors_list.append({
                'artifact_id': artifact_id,
                'color_hex': color.get('hex'),
                'color_name': color.get('color'),
                'percentage': color.get('percent')
            })
    
    return (
        pd.DataFrame(metadata_list),
        pd.DataFrame(media_list),
        pd.DataFrame(colors_list)
    )
```

### 3. Load into SQL Database

```python
def create_tables(connection):
    """Create database schema"""
    cursor = connection.cursor()
    
    # Metadata table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifactmetadata (
            artifact_id INT PRIMARY KEY,
            title VARCHAR(500),
            culture VARCHAR(255),
            century VARCHAR(100),
            dated VARCHAR(255),
            department VARCHAR(255),
            classification VARCHAR(255),
            medium TEXT,
            dimensions TEXT,
            creditline TEXT,
            accession_number VARCHAR(50)
        )
    """)
    
    # Media table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifactmedia (
            id INT AUTO_INCREMENT PRIMARY KEY,
            artifact_id INT,
            media_type VARCHAR(50),
            media_url TEXT,
            is_primary BOOLEAN,
            FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(artifact_id)
        )
    """)
    
    # Colors table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifactcolors (
            id INT AUTO_INCREMENT PRIMARY KEY,
            artifact_id INT,
            color_hex VARCHAR(7),
            color_name VARCHAR(100),
            percentage DECIMAL(5,2),
            FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(artifact_id)
        )
    """)
    
    connection.commit()
    cursor.close()


def load_data(connection, metadata_df, media_df, colors_df):
    """Batch insert data into SQL tables"""
    cursor = connection.cursor()
    
    # Insert metadata
    for _, row in metadata_df.iterrows():
        cursor.execute("""
            INSERT INTO artifactmetadata 
            (artifact_id, title, culture, century, dated, department, 
             classification, medium, dimensions, creditline, accession_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE title=VALUES(title)
        """, tuple(row))
    
    # Insert media
    for _, row in media_df.iterrows():
        cursor.execute("""
            INSERT INTO artifactmedia 
            (artifact_id, media_type, media_url, is_primary)
            VALUES (%s, %s, %s, %s)
        """, tuple(row))
    
    # Insert colors
    for _, row in colors_df.iterrows():
        cursor.execute("""
            INSERT INTO artifactcolors 
            (artifact_id, color_hex, color_name, percentage)
            VALUES (%s, %s, %s, %s)
        """, tuple(row))
    
    connection.commit()
    cursor.close()
```

### 4. Analytics Queries

```python
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
    
    "Top Departments": """
        SELECT department, COUNT(*) as artifact_count
        FROM artifactmetadata
        WHERE department IS NOT NULL
        GROUP BY department
        ORDER BY artifact_count DESC
    """,
    
    "Color Distribution": """
        SELECT color_name, COUNT(*) as usage_count,
               AVG(percentage) as avg_percentage
        FROM artifactcolors
        WHERE color_name IS NOT NULL
        GROUP BY color_name
        ORDER BY usage_count DESC
        LIMIT 15
    """,
    
    "Artifacts with Media": """
        SELECT 
            COUNT(DISTINCT m.artifact_id) as total_with_media,
            COUNT(DISTINCT a.artifact_id) as total_artifacts,
            ROUND(COUNT(DISTINCT m.artifact_id) * 100.0 / COUNT(DISTINCT a.artifact_id), 2) as percentage
        FROM artifactmetadata a
        LEFT JOIN artifactmedia m ON a.artifact_id = m.artifact_id
    """
}

def execute_query(connection, query_name):
    """Execute analytical query and return DataFrame"""
    cursor = connection.cursor(dictionary=True)
    cursor.execute(ANALYTICS_QUERIES[query_name])
    results = cursor.fetchall()
    cursor.close()
    return pd.DataFrame(results)
```

### 5. Streamlit Dashboard

```python
import streamlit as st
import plotly.express as px

def main():
    st.title("🎨 Harvard Art Museums Analytics Dashboard")
    
    # Sidebar for query selection
    st.sidebar.header("Analytics Queries")
    query_name = st.sidebar.selectbox(
        "Select Analysis",
        list(ANALYTICS_QUERIES.keys())
    )
    
    # Execute query
    if st.sidebar.button("Run Query"):
        with st.spinner("Executing query..."):
            conn = get_db_connection()
            df = execute_query(conn, query_name)
            conn.close()
            
            # Display results
            st.subheader(f"Results: {query_name}")
            st.dataframe(df)
            
            # Visualization
            if len(df.columns) >= 2:
                fig = px.bar(
                    df, 
                    x=df.columns[0], 
                    y=df.columns[1],
                    title=query_name
                )
                st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
```

## Running the Application

### ETL Pipeline Execution

```bash
# Run complete ETL pipeline
python etl_pipeline.py
```

```python
# etl_pipeline.py
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    # Extract
    print("Extracting data from API...")
    api_key = os.getenv('HARVARD_API_KEY')
    artifacts = extract_artifacts(api_key, num_pages=10)
    
    # Transform
    print("Transforming data...")
    metadata_df, media_df, colors_df = transform_artifacts(artifacts)
    
    # Load
    print("Loading into database...")
    conn = get_db_connection()
    create_tables(conn)
    load_data(conn, metadata_df, media_df, colors_df)
    conn.close()
    
    print(f"ETL Complete: {len(artifacts)} artifacts processed")

if __name__ == "__main__":
    main()
```

### Launch Dashboard

```bash
streamlit run app.py
```

## Common Patterns

### Incremental Data Loading

```python
def get_latest_artifact_id(connection):
    """Get the most recent artifact ID in database"""
    cursor = connection.cursor()
    cursor.execute("SELECT MAX(artifact_id) FROM artifactmetadata")
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result[0] else 0

def incremental_extract(api_key, last_id):
    """Only fetch artifacts newer than last_id"""
    params = {
        'apikey': api_key,
        'size': 100,
        'sort': 'id',
        'sortorder': 'asc',
        'q': f'id:>{last_id}'
    }
    response = requests.get(BASE_URL, params=params)
    return response.json().get('records', [])
```

### Error Handling and Retry Logic

```python
import time
from requests.exceptions import RequestException

def fetch_with_retry(url, params, max_retries=3):
    """Fetch data with exponential backoff"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            wait_time = 2 ** attempt
            print(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...")
            time.sleep(wait_time)
    raise Exception(f"Failed after {max_retries} retries")
```

## Troubleshooting

### API Rate Limiting

```python
import time

def rate_limited_fetch(api_key, num_pages, delay=0.5):
    """Add delay between requests to avoid rate limits"""
    artifacts = []
    for page in range(1, num_pages + 1):
        params = {'apikey': api_key, 'size': 100, 'page': page}
        response = requests.get(BASE_URL, params=params)
        
        if response.status_code == 429:  # Too Many Requests
            print("Rate limit hit. Waiting 60 seconds...")
            time.sleep(60)
            response = requests.get(BASE_URL, params=params)
        
        artifacts.extend(response.json().get('records', []))
        time.sleep(delay)  # Polite delay
    
    return artifacts
```

### Database Connection Issues

```python
def get_db_connection_with_retry():
    """Retry database connection"""
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            return mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                port=int(os.getenv('DB_PORT', 3306)),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME'),
                connect_timeout=10
            )
        except mysql.connector.Error as e:
            print(f"Connection attempt {attempt + 1} failed: {e}")
            if attempt < max_attempts - 1:
                time.sleep(5)
    raise Exception("Could not connect to database")
```

### Handling Missing Data

```python
def safe_transform(artifact):
    """Handle missing fields gracefully"""
    return {
        'artifact_id': artifact.get('id'),
        'title': artifact.get('title', 'Untitled'),
        'culture': artifact.get('culture') or 'Unknown',
        'century': artifact.get('century') or 'Unknown',
        'department': artifact.get('department', 'Not Specified'),
        'medium': artifact.get('medium') or None
    }
```

### Query Performance Optimization

```sql
-- Add indexes for common queries
CREATE INDEX idx_culture ON artifactmetadata(culture);
CREATE INDEX idx_century ON artifactmetadata(century);
CREATE INDEX idx_department ON artifactmetadata(department);
CREATE INDEX idx_artifact_colors ON artifactcolors(artifact_id);
CREATE INDEX idx_color_name ON artifactcolors(color_name);
```

## Advanced Usage

### Custom Query Builder

```python
def build_custom_query(filters):
    """Build dynamic SQL query from user filters"""
    base_query = "SELECT * FROM artifactmetadata WHERE 1=1"
    
    if filters.get('culture'):
        base_query += f" AND culture = '{filters['culture']}'"
    if filters.get('century'):
        base_query += f" AND century = '{filters['century']}'"
    if filters.get('department'):
        base_query += f" AND department = '{filters['department']}'"
    
    return base_query
```

### Export Results

```python
def export_to_csv(df, filename):
    """Export query results to CSV"""
    df.to_csv(filename, index=False)
    print(f"Exported to {filename}")

def export_to_json(df, filename):
    """Export query results to JSON"""
    df.to_json(filename, orient='records', indent=2)
    print(f"Exported to {filename}")
```

This skill provides complete patterns for building production-ready data pipelines with the Harvard Art Museums API, from extraction through visualization.
