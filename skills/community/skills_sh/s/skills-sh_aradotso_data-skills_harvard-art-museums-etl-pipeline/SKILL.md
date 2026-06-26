---
name: harvard-art-museums-etl-pipeline
description: Build ETL pipelines and analytics dashboards using the Harvard Art Museums API with Python, SQL, and Streamlit
triggers:
  - how do I build an ETL pipeline for Harvard Art Museums data
  - set up Harvard artifacts collection analytics app
  - create a data engineering pipeline with Harvard API
  - build Streamlit dashboard for museum artifact data
  - extract and analyze Harvard Art Museums collection
  - implement SQL analytics for art museum artifacts
  - how to use the Harvard artifacts ETL application
  - build end-to-end data pipeline for museum collections
---

# Harvard Art Museums ETL Pipeline

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This skill enables AI agents to help developers build end-to-end data engineering and analytics applications using the Harvard Art Museums API. The project demonstrates real-world ETL pipelines, SQL database design, analytical queries, and interactive Streamlit dashboards for artifact collection data.

## What This Project Does

The Harvard Artifacts Collection Data Engineering & Analytics App provides:

- **API Integration**: Fetches artifact data from Harvard Art Museums API with pagination and rate limiting
- **ETL Pipeline**: Extracts, transforms, and loads artifact metadata, media, and color data into relational SQL tables
- **SQL Analytics**: Pre-built analytical queries for insights on artifacts by culture, century, department, and media
- **Interactive Dashboards**: Streamlit-based visualization using Plotly for real-time analytics
- **Database Design**: Normalized schema with proper foreign key relationships across artifact metadata, media, and color tables

## Installation

### Prerequisites

- Python 3.8+
- MySQL or TiDB Cloud database instance
- Harvard Art Museums API key (get from https://www.harvardartmuseums.org/collections/api)

### Setup

```bash
# Clone the repository
git clone https://github.com/Manali0711/Harvard-Artifacts-Collection-Data-Engineering-Analytics-App.git
cd Harvard-Artifacts-Collection-Data-Engineering-Analytics-App

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export HARVARD_API_KEY="your_api_key_here"
export DB_HOST="your_database_host"
export DB_USER="your_db_username"
export DB_PASSWORD="your_db_password"
export DB_NAME="harvard_artifacts"
```

### Database Setup

Create the database and tables:

```sql
CREATE DATABASE harvard_artifacts;
USE harvard_artifacts;

CREATE TABLE artifactmetadata (
    id INT PRIMARY KEY,
    title VARCHAR(500),
    culture VARCHAR(255),
    century VARCHAR(100),
    classification VARCHAR(255),
    department VARCHAR(255),
    dated VARCHAR(255),
    medium VARCHAR(500),
    technique VARCHAR(500),
    period VARCHAR(255),
    url TEXT,
    copyright TEXT
);

CREATE TABLE artifactmedia (
    media_id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    iiifbaseuri TEXT,
    baseimageurl TEXT,
    primaryimageurl TEXT,
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
);

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

## Key Components

### API Data Collection

```python
import requests
import os

class HarvardAPIClient:
    def __init__(self):
        self.api_key = os.getenv('HARVARD_API_KEY')
        self.base_url = "https://api.harvardartmuseums.org/object"
    
    def fetch_artifacts(self, page=1, size=100):
        """Fetch artifacts from Harvard Art Museums API"""
        params = {
            'apikey': self.api_key,
            'page': page,
            'size': size,
            'hasimage': 1  # Only artifacts with images
        }
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json()
    
    def collect_paginated_data(self, max_pages=10):
        """Collect data across multiple pages"""
        all_artifacts = []
        for page in range(1, max_pages + 1):
            data = self.fetch_artifacts(page=page)
            all_artifacts.extend(data.get('records', []))
            if page >= data.get('info', {}).get('pages', 0):
                break
        return all_artifacts
```

### ETL Pipeline

```python
import pandas as pd
import mysql.connector
from typing import List, Dict

class ArtifactETL:
    def __init__(self, db_config):
        self.db_config = db_config
        self.connection = None
    
    def connect_db(self):
        """Establish database connection"""
        self.connection = mysql.connector.connect(
            host=self.db_config['host'],
            user=self.db_config['user'],
            password=self.db_config['password'],
            database=self.db_config['database']
        )
        return self.connection.cursor()
    
    def extract_metadata(self, artifacts: List[Dict]) -> pd.DataFrame:
        """Extract artifact metadata"""
        metadata = []
        for artifact in artifacts:
            metadata.append({
                'id': artifact.get('id'),
                'title': artifact.get('title'),
                'culture': artifact.get('culture'),
                'century': artifact.get('century'),
                'classification': artifact.get('classification'),
                'department': artifact.get('department'),
                'dated': artifact.get('dated'),
                'medium': artifact.get('medium'),
                'technique': artifact.get('technique'),
                'period': artifact.get('period'),
                'url': artifact.get('url'),
                'copyright': artifact.get('copyright')
            })
        return pd.DataFrame(metadata)
    
    def extract_media(self, artifacts: List[Dict]) -> pd.DataFrame:
        """Extract artifact media information"""
        media_data = []
        for artifact in artifacts:
            artifact_id = artifact.get('id')
            media_data.append({
                'artifact_id': artifact_id,
                'iiifbaseuri': artifact.get('images', [{}])[0].get('iiifbaseuri') if artifact.get('images') else None,
                'baseimageurl': artifact.get('images', [{}])[0].get('baseimageurl') if artifact.get('images') else None,
                'primaryimageurl': artifact.get('primaryimageurl')
            })
        return pd.DataFrame(media_data)
    
    def extract_colors(self, artifacts: List[Dict]) -> pd.DataFrame:
        """Extract color information"""
        color_data = []
        for artifact in artifacts:
            artifact_id = artifact.get('id')
            colors = artifact.get('colors', [])
            for color in colors:
                color_data.append({
                    'artifact_id': artifact_id,
                    'color': color.get('color'),
                    'spectrum': color.get('spectrum'),
                    'hue': color.get('hue'),
                    'percent': color.get('percent')
                })
        return pd.DataFrame(color_data)
    
    def load_data(self, df: pd.DataFrame, table_name: str):
        """Load dataframe into SQL table"""
        cursor = self.connect_db()
        
        # Prepare batch insert
        cols = ','.join(df.columns)
        placeholders = ','.join(['%s'] * len(df.columns))
        sql = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"
        
        # Convert dataframe to list of tuples
        values = [tuple(row) for row in df.values]
        
        cursor.executemany(sql, values)
        self.connection.commit()
        cursor.close()
        
        return len(values)
```

### Complete ETL Workflow

```python
# Initialize components
api_client = HarvardAPIClient()
etl = ArtifactETL({
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
})

# Extract from API
print("Extracting artifacts from API...")
artifacts = api_client.collect_paginated_data(max_pages=5)

# Transform
print("Transforming data...")
metadata_df = etl.extract_metadata(artifacts)
media_df = etl.extract_media(artifacts)
colors_df = etl.extract_colors(artifacts)

# Load
print("Loading data to database...")
etl.load_data(metadata_df, 'artifactmetadata')
etl.load_data(media_df, 'artifactmedia')
etl.load_data(colors_df, 'artifactcolors')

print("ETL pipeline completed successfully!")
```

## SQL Analytics Queries

### Top Cultures by Artifact Count

```sql
SELECT culture, COUNT(*) as artifact_count
FROM artifactmetadata
WHERE culture IS NOT NULL
GROUP BY culture
ORDER BY artifact_count DESC
LIMIT 10;
```

### Artifacts by Century

```sql
SELECT century, COUNT(*) as count
FROM artifactmetadata
WHERE century IS NOT NULL
GROUP BY century
ORDER BY count DESC;
```

### Department Distribution

```sql
SELECT department, COUNT(*) as total_artifacts
FROM artifactmetadata
WHERE department IS NOT NULL
GROUP BY department
ORDER BY total_artifacts DESC;
```

### Color Analysis

```sql
SELECT 
    c.color,
    c.spectrum,
    COUNT(*) as usage_count,
    AVG(c.percent) as avg_percentage
FROM artifactcolors c
GROUP BY c.color, c.spectrum
ORDER BY usage_count DESC
LIMIT 15;
```

### Media Availability

```sql
SELECT 
    COUNT(*) as total_artifacts,
    SUM(CASE WHEN primaryimageurl IS NOT NULL THEN 1 ELSE 0 END) as with_images,
    ROUND(SUM(CASE WHEN primaryimageurl IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as image_percentage
FROM artifactmedia;
```

## Streamlit Dashboard

### Basic Dashboard Structure

```python
import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector

st.set_page_config(page_title="Harvard Artifacts Analytics", layout="wide")

# Database connection
@st.cache_resource
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

# Query execution
def run_query(query: str) -> pd.DataFrame:
    conn = get_db_connection()
    df = pd.read_sql(query, conn)
    return df

# Sidebar navigation
st.sidebar.title("Harvard Artifacts Analytics")
analysis_type = st.sidebar.selectbox(
    "Select Analysis",
    ["Culture Distribution", "Century Analysis", "Department Stats", "Color Insights", "Media Availability"]
)

# Main content
st.title("🏛️ Harvard Art Museums Analytics Dashboard")

if analysis_type == "Culture Distribution":
    st.header("Artifact Distribution by Culture")
    
    query = """
    SELECT culture, COUNT(*) as artifact_count
    FROM artifactmetadata
    WHERE culture IS NOT NULL
    GROUP BY culture
    ORDER BY artifact_count DESC
    LIMIT 15
    """
    
    df = run_query(query)
    
    # Display table
    st.dataframe(df, use_container_width=True)
    
    # Visualization
    fig = px.bar(df, x='culture', y='artifact_count', 
                 title='Top 15 Cultures by Artifact Count',
                 labels={'culture': 'Culture', 'artifact_count': 'Number of Artifacts'})
    st.plotly_chart(fig, use_container_width=True)

elif analysis_type == "Color Insights":
    st.header("Color Usage Patterns")
    
    query = """
    SELECT 
        color,
        spectrum,
        COUNT(*) as usage_count,
        ROUND(AVG(percent), 2) as avg_percentage
    FROM artifactcolors
    GROUP BY color, spectrum
    ORDER BY usage_count DESC
    LIMIT 20
    """
    
    df = run_query(query)
    
    st.dataframe(df, use_container_width=True)
    
    fig = px.scatter(df, x='avg_percentage', y='usage_count', 
                     color='spectrum', size='usage_count',
                     hover_data=['color'],
                     title='Color Usage Analysis')
    st.plotly_chart(fig, use_container_width=True)
```

### Custom Query Interface

```python
st.header("Custom SQL Query")

query_templates = {
    "Artifacts by Medium": """
        SELECT medium, COUNT(*) as count
        FROM artifactmetadata
        WHERE medium IS NOT NULL
        GROUP BY medium
        ORDER BY count DESC
        LIMIT 10
    """,
    "Artifacts by Period": """
        SELECT period, COUNT(*) as total
        FROM artifactmetadata
        WHERE period IS NOT NULL
        GROUP BY period
        ORDER BY total DESC
    """
}

selected_template = st.selectbox("Choose Query Template", list(query_templates.keys()))
custom_query = st.text_area("SQL Query", value=query_templates[selected_template], height=150)

if st.button("Execute Query"):
    try:
        result_df = run_query(custom_query)
        st.success(f"Query returned {len(result_df)} rows")
        st.dataframe(result_df, use_container_width=True)
        
        # Auto-generate chart if applicable
        if len(result_df.columns) == 2:
            col1, col2 = result_df.columns
            fig = px.bar(result_df, x=col1, y=col2, title=f"{col2} by {col1}")
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Query error: {str(e)}")
```

## Running the Application

```bash
# Run the Streamlit dashboard
streamlit run app.py

# The app will be available at http://localhost:8501
```

## Common Patterns

### Incremental Data Loading

```python
def get_last_artifact_id():
    """Get the last loaded artifact ID"""
    cursor = etl.connect_db()
    cursor.execute("SELECT MAX(id) FROM artifactmetadata")
    result = cursor.fetchone()
    return result[0] if result[0] else 0

def incremental_load():
    """Load only new artifacts"""
    last_id = get_last_artifact_id()
    
    # Fetch artifacts after last_id
    params = {
        'apikey': os.getenv('HARVARD_API_KEY'),
        'after': last_id,
        'size': 100
    }
    
    response = requests.get(api_client.base_url, params=params)
    new_artifacts = response.json().get('records', [])
    
    # Process and load
    if new_artifacts:
        metadata_df = etl.extract_metadata(new_artifacts)
        etl.load_data(metadata_df, 'artifactmetadata')
        print(f"Loaded {len(new_artifacts)} new artifacts")
```

### Error Handling in ETL

```python
def safe_etl_run(artifacts):
    """ETL with comprehensive error handling"""
    try:
        # Metadata
        try:
            metadata_df = etl.extract_metadata(artifacts)
            loaded = etl.load_data(metadata_df, 'artifactmetadata')
            print(f"Loaded {loaded} metadata records")
        except Exception as e:
            print(f"Metadata error: {e}")
        
        # Media
        try:
            media_df = etl.extract_media(artifacts)
            loaded = etl.load_data(media_df, 'artifactmedia')
            print(f"Loaded {loaded} media records")
        except Exception as e:
            print(f"Media error: {e}")
        
        # Colors
        try:
            colors_df = etl.extract_colors(artifacts)
            if not colors_df.empty:
                loaded = etl.load_data(colors_df, 'artifactcolors')
                print(f"Loaded {loaded} color records")
        except Exception as e:
            print(f"Colors error: {e}")
            
    except Exception as e:
        print(f"Critical ETL error: {e}")
        raise
```

## Troubleshooting

### API Rate Limiting

```python
import time

def fetch_with_retry(page, max_retries=3):
    """Fetch with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return api_client.fetch_artifacts(page=page)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:  # Too many requests
                wait_time = 2 ** attempt
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
    raise Exception("Max retries exceeded")
```

### Database Connection Issues

```python
def test_database_connection():
    """Verify database connectivity"""
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print("✓ Database connection successful")
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False
```

### Missing Environment Variables

```python
def validate_env_vars():
    """Ensure all required environment variables are set"""
    required_vars = ['HARVARD_API_KEY', 'DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")
    
    print("✓ All environment variables configured")
```

### Data Quality Checks

```python
def validate_artifact_data(df: pd.DataFrame):
    """Validate artifact metadata before loading"""
    issues = []
    
    # Check for duplicate IDs
    if df['id'].duplicated().any():
        issues.append("Duplicate artifact IDs found")
    
    # Check for null IDs
    if df['id'].isnull().any():
        issues.append("Null artifact IDs found")
    
    # Check data types
    if not pd.api.types.is_integer_dtype(df['id']):
        issues.append("Invalid ID data type")
    
    if issues:
        raise ValueError(f"Data validation failed: {'; '.join(issues)}")
    
    print(f"✓ Data validation passed for {len(df)} records")
```

This skill provides comprehensive guidance for building ETL pipelines and analytics dashboards with the Harvard Art Museums API, including database design, data transformation, visualization, and production-ready error handling patterns.
