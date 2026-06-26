---
name: harvard-artifacts-etl-streamlit-analytics
description: Build ETL pipelines and analytics dashboards for Harvard Art Museums API data using Python, SQL, and Streamlit
triggers:
  - build a data pipeline for museum artifacts
  - create ETL workflow for Harvard Art Museums API
  - set up artifact analytics dashboard with Streamlit
  - process Harvard museum collection data
  - build SQL analytics for art collection data
  - create museum artifact visualization pipeline
  - integrate Harvard Art Museums API with database
  - develop end-to-end museum data engineering app
---

# Harvard Artifacts ETL & Analytics Skill

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This skill enables AI agents to help developers build end-to-end data engineering pipelines using the Harvard Art Museums API. The project demonstrates ETL workflows, SQL database design, analytical queries, and interactive Streamlit dashboards for artifact collection data.

## What This Project Does

The Harvard Artifacts Collection Data Engineering Analytics App provides:

- **API Integration**: Fetch artifact data from Harvard Art Museums API with pagination and rate limiting
- **ETL Pipeline**: Extract, transform, and load nested JSON data into relational SQL tables
- **Database Design**: Store artifacts across normalized tables (metadata, media, colors)
- **SQL Analytics**: Execute 20+ predefined analytical queries
- **Visualization**: Interactive Plotly charts and Streamlit dashboards

## Installation

```bash
# Clone the repository
git clone https://github.com/Manali0711/Harvard-Artifacts-Collection-Data-Engineering-Analytics-App.git
cd Harvard-Artifacts-Collection-Data-Engineering-Analytics-App

# Install dependencies
pip install -r requirements.txt

# Required packages
pip install streamlit pandas requests mysql-connector-python plotly sqlalchemy
```

## Configuration

### Environment Variables

Store sensitive credentials in environment variables or Streamlit secrets:

```python
# .streamlit/secrets.toml
[database]
host = "your-database-host"
port = 4000
user = "your-db-user"
password = "your-db-password"
database = "harvard_artifacts"

[api]
key = "your-harvard-api-key"
```

### Database Setup

Create the database schema for storing artifact data:

```sql
-- Create database
CREATE DATABASE IF NOT EXISTS harvard_artifacts;
USE harvard_artifacts;

-- Artifact metadata table
CREATE TABLE artifactmetadata (
    id INT PRIMARY KEY,
    title VARCHAR(500),
    culture VARCHAR(255),
    century VARCHAR(100),
    classification VARCHAR(255),
    department VARCHAR(255),
    division VARCHAR(255),
    dated VARCHAR(255),
    period VARCHAR(255),
    technique VARCHAR(500),
    medium VARCHAR(500),
    dimensions VARCHAR(500),
    url VARCHAR(500),
    accession_number VARCHAR(100),
    INDEX idx_culture (culture),
    INDEX idx_century (century),
    INDEX idx_department (department)
);

-- Artifact media table
CREATE TABLE artifactmedia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    image_url VARCHAR(1000),
    description TEXT,
    caption TEXT,
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id),
    INDEX idx_artifact_id (artifact_id)
);

-- Artifact colors table
CREATE TABLE artifactcolors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    color VARCHAR(50),
    percentage FLOAT,
    hue VARCHAR(50),
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id),
    INDEX idx_artifact_id (artifact_id)
);
```

## Core Components

### 1. API Data Collection

Fetch artifacts from Harvard Art Museums API with pagination:

```python
import requests
import os

def fetch_artifacts(api_key, num_pages=5, page_size=100):
    """
    Fetch artifacts from Harvard Art Museums API
    
    Args:
        api_key: Harvard API key
        num_pages: Number of pages to fetch
        page_size: Records per page (max 100)
    
    Returns:
        List of artifact records
    """
    base_url = "https://api.harvardartmuseums.org/object"
    all_artifacts = []
    
    for page in range(1, num_pages + 1):
        params = {
            'apikey': api_key,
            'size': page_size,
            'page': page,
            'fields': 'id,title,culture,century,classification,department,division,dated,period,technique,medium,dimensions,url,accessionNumber,images,colors'
        }
        
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            all_artifacts.extend(data.get('records', []))
        else:
            print(f"Error fetching page {page}: {response.status_code}")
            
    return all_artifacts

# Usage
api_key = os.getenv('HARVARD_API_KEY')
artifacts = fetch_artifacts(api_key, num_pages=10)
print(f"Fetched {len(artifacts)} artifacts")
```

### 2. ETL Pipeline

Transform nested JSON into relational format:

```python
import pandas as pd

def transform_artifacts(artifacts):
    """
    Transform raw API data into normalized dataframes
    
    Returns:
        Tuple of (metadata_df, media_df, colors_df)
    """
    metadata_records = []
    media_records = []
    color_records = []
    
    for artifact in artifacts:
        # Extract metadata
        metadata_records.append({
            'id': artifact.get('id'),
            'title': artifact.get('title', ''),
            'culture': artifact.get('culture', ''),
            'century': artifact.get('century', ''),
            'classification': artifact.get('classification', ''),
            'department': artifact.get('department', ''),
            'division': artifact.get('division', ''),
            'dated': artifact.get('dated', ''),
            'period': artifact.get('period', ''),
            'technique': artifact.get('technique', ''),
            'medium': artifact.get('medium', ''),
            'dimensions': artifact.get('dimensions', ''),
            'url': artifact.get('url', ''),
            'accession_number': artifact.get('accessionNumber', '')
        })
        
        # Extract media/images
        images = artifact.get('images', [])
        for img in images:
            media_records.append({
                'artifact_id': artifact.get('id'),
                'image_url': img.get('baseimageurl', ''),
                'description': img.get('description', ''),
                'caption': img.get('caption', '')
            })
        
        # Extract colors
        colors = artifact.get('colors', [])
        for color in colors:
            color_records.append({
                'artifact_id': artifact.get('id'),
                'color': color.get('color', ''),
                'percentage': color.get('percent', 0.0),
                'hue': color.get('hue', '')
            })
    
    return (
        pd.DataFrame(metadata_records),
        pd.DataFrame(media_records),
        pd.DataFrame(color_records)
    )
```

### 3. Database Loading

Batch insert data into SQL database:

```python
import mysql.connector
from mysql.connector import Error

def load_to_database(metadata_df, media_df, colors_df, db_config):
    """
    Load transformed data into MySQL database
    
    Args:
        metadata_df: Artifact metadata DataFrame
        media_df: Media/images DataFrame
        colors_df: Colors DataFrame
        db_config: Database connection config dict
    """
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Insert metadata (batch)
        metadata_sql = """
            INSERT INTO artifactmetadata 
            (id, title, culture, century, classification, department, division, 
             dated, period, technique, medium, dimensions, url, accession_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE title=VALUES(title)
        """
        metadata_values = metadata_df.values.tolist()
        cursor.executemany(metadata_sql, metadata_values)
        
        # Insert media
        media_sql = """
            INSERT INTO artifactmedia (artifact_id, image_url, description, caption)
            VALUES (%s, %s, %s, %s)
        """
        media_values = media_df.values.tolist()
        cursor.executemany(media_sql, media_values)
        
        # Insert colors
        colors_sql = """
            INSERT INTO artifactcolors (artifact_id, color, percentage, hue)
            VALUES (%s, %s, %s, %s)
        """
        colors_values = colors_df.values.tolist()
        cursor.executemany(colors_sql, colors_values)
        
        conn.commit()
        print(f"Loaded {len(metadata_df)} artifacts successfully")
        
    except Error as e:
        print(f"Database error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
```

### 4. Streamlit Dashboard

Create interactive analytics dashboard:

```python
import streamlit as st
import plotly.express as px

def run_analytics_dashboard():
    """
    Main Streamlit dashboard for artifact analytics
    """
    st.set_page_config(page_title="Harvard Artifacts Analytics", layout="wide")
    
    st.title("🏛️ Harvard Art Museums Analytics Dashboard")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("Configuration")
        db_host = st.text_input("Database Host", value=st.secrets.database.host)
        db_user = st.text_input("Database User", value=st.secrets.database.user)
        db_password = st.text_input("Database Password", type="password", 
                                     value=st.secrets.database.password)
        db_name = st.text_input("Database Name", value=st.secrets.database.database)
    
    db_config = {
        'host': db_host,
        'user': db_user,
        'password': db_password,
        'database': db_name
    }
    
    # Analytics queries
    queries = {
        "Artifacts by Culture": """
            SELECT culture, COUNT(*) as count 
            FROM artifactmetadata 
            WHERE culture != '' 
            GROUP BY culture 
            ORDER BY count DESC 
            LIMIT 15
        """,
        "Artifacts by Century": """
            SELECT century, COUNT(*) as count 
            FROM artifactmetadata 
            WHERE century != '' 
            GROUP BY century 
            ORDER BY count DESC
        """,
        "Top Colors Used": """
            SELECT color, SUM(percentage) as total_percentage 
            FROM artifactcolors 
            GROUP BY color 
            ORDER BY total_percentage DESC 
            LIMIT 10
        """,
        "Artifacts with Images": """
            SELECT 
                CASE WHEN media_count > 0 THEN 'With Images' ELSE 'No Images' END as has_images,
                COUNT(*) as artifact_count
            FROM (
                SELECT m.id, COUNT(am.id) as media_count
                FROM artifactmetadata m
                LEFT JOIN artifactmedia am ON m.id = am.artifact_id
                GROUP BY m.id
            ) as subquery
            GROUP BY has_images
        """
    }
    
    st.header("📊 SQL Analytics")
    query_name = st.selectbox("Select Analysis", list(queries.keys()))
    
    if st.button("Run Query"):
        df = execute_query(queries[query_name], db_config)
        
        if not df.empty:
            st.subheader("Query Results")
            st.dataframe(df)
            
            # Auto-generate visualization
            if len(df.columns) == 2:
                fig = px.bar(df, x=df.columns[0], y=df.columns[1],
                            title=query_name)
                st.plotly_chart(fig, use_container_width=True)

def execute_query(sql, db_config):
    """Execute SQL query and return DataFrame"""
    try:
        conn = mysql.connector.connect(**db_config)
        df = pd.read_sql(sql, conn)
        conn.close()
        return df
    except Error as e:
        st.error(f"Query error: {e}")
        return pd.DataFrame()

# Run the app
if __name__ == "__main__":
    run_analytics_dashboard()
```

## Sample Analytical Queries

```sql
-- Top 10 cultures by artifact count
SELECT culture, COUNT(*) as artifact_count
FROM artifactmetadata
WHERE culture IS NOT NULL AND culture != ''
GROUP BY culture
ORDER BY artifact_count DESC
LIMIT 10;

-- Artifacts by department and classification
SELECT department, classification, COUNT(*) as count
FROM artifactmetadata
GROUP BY department, classification
ORDER BY count DESC;

-- Color distribution across artifacts
SELECT color, COUNT(DISTINCT artifact_id) as artifact_count, 
       AVG(percentage) as avg_percentage
FROM artifactcolors
GROUP BY color
ORDER BY artifact_count DESC;

-- Artifacts with complete data (images and colors)
SELECT m.title, m.culture, m.century,
       COUNT(DISTINCT am.id) as image_count,
       COUNT(DISTINCT ac.id) as color_count
FROM artifactmetadata m
LEFT JOIN artifactmedia am ON m.id = am.artifact_id
LEFT JOIN artifactcolors ac ON m.id = ac.artifact_id
GROUP BY m.id, m.title, m.culture, m.century
HAVING image_count > 0 AND color_count > 0
LIMIT 20;
```

## Common Patterns

### Full ETL Workflow

```python
def run_etl_pipeline(api_key, db_config, num_pages=10):
    """
    Complete ETL pipeline execution
    """
    # Extract
    print("Extracting data from API...")
    artifacts = fetch_artifacts(api_key, num_pages)
    
    # Transform
    print("Transforming data...")
    metadata_df, media_df, colors_df = transform_artifacts(artifacts)
    
    # Load
    print("Loading to database...")
    load_to_database(metadata_df, media_df, colors_df, db_config)
    
    print("ETL pipeline completed successfully!")
    return len(artifacts)

# Execute
total_artifacts = run_etl_pipeline(
    api_key=os.getenv('HARVARD_API_KEY'),
    db_config={
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': 'harvard_artifacts'
    }
)
```

## Troubleshooting

### API Rate Limiting

```python
import time

def fetch_with_retry(url, params, max_retries=3):
    """Fetch with exponential backoff"""
    for attempt in range(max_retries):
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            wait_time = 2 ** attempt
            print(f"Rate limited. Waiting {wait_time}s...")
            time.sleep(wait_time)
        else:
            break
    return None
```

### Database Connection Issues

```python
def test_db_connection(db_config):
    """Test database connectivity"""
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print("✅ Database connection successful")
            conn.close()
            return True
    except Error as e:
        print(f"❌ Connection failed: {e}")
        return False
```

### Handling Missing Data

```python
def safe_get(dictionary, key, default=''):
    """Safely extract values from nested dictionaries"""
    value = dictionary.get(key, default)
    return value if value is not None else default
```

## Running the Application

```bash
# Start Streamlit dashboard
streamlit run app.py

# Run ETL pipeline only
python etl_pipeline.py

# Run with custom configuration
streamlit run app.py --server.port 8501
```

This skill enables you to build production-ready data engineering pipelines for cultural heritage data, demonstrating ETL best practices, SQL analytics, and modern visualization techniques.
