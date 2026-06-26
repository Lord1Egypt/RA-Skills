---
name: harvard-artifacts-data-engineering-pipeline
description: Build ETL pipelines and analytics dashboards using Harvard Art Museums API with SQL and Streamlit
triggers:
  - how do I build a data pipeline with Harvard Art Museums API
  - set up ETL for Harvard artifacts collection
  - create analytics dashboard for museum artifacts data
  - extract and transform Harvard museum data to SQL
  - build Streamlit app for art museum analytics
  - query Harvard Art Museums API and visualize results
  - implement data engineering pipeline for museum artifacts
  - analyze Harvard art collection with SQL queries
---

# Harvard Artifacts Data Engineering Pipeline

> Skill by [ara.so](https://ara.so) — Data Skills collection.

## Overview

This project provides an end-to-end data engineering solution for analyzing Harvard Art Museums collections. It demonstrates:

- **API Integration**: Fetching paginated data from Harvard Art Museums API
- **ETL Pipeline**: Extracting, transforming, and loading artifact metadata into SQL
- **Relational Database**: Structured storage with proper foreign key relationships
- **SQL Analytics**: 20+ predefined analytical queries for insights
- **Interactive Visualization**: Streamlit dashboard with Plotly charts

Architecture: `API → ETL → SQL → Analytics → Visualization`

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

### Dependencies

```txt
streamlit
pandas
requests
mysql-connector-python
plotly
python-dotenv
```

## Getting Harvard API Key

1. Visit [Harvard Art Museums API](https://www.harvardartmuseums.org/collections/api)
2. Register for a free API key
3. Store in environment variable: `HARVARD_API_KEY`

## Database Setup

Create three main tables for the ETL pipeline:

```sql
CREATE TABLE artifactmetadata (
    id INT PRIMARY KEY,
    title VARCHAR(500),
    culture VARCHAR(200),
    period VARCHAR(200),
    century VARCHAR(100),
    classification VARCHAR(200),
    department VARCHAR(200),
    division VARCHAR(200),
    dated VARCHAR(200),
    accession_number VARCHAR(100),
    total_page_views INT,
    total_unique_pageviews INT,
    url TEXT
);

CREATE TABLE artifactmedia (
    media_id INT PRIMARY KEY AUTO_INCREMENT,
    artifact_id INT,
    image_url TEXT,
    height INT,
    width INT,
    format VARCHAR(50),
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
);

CREATE TABLE artifactcolors (
    color_id INT PRIMARY KEY AUTO_INCREMENT,
    artifact_id INT,
    color_hex VARCHAR(10),
    color_percent FLOAT,
    color_spectrum VARCHAR(50),
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
);
```

## Core Components

### 1. API Data Collection

```python
import requests
import os

def fetch_artifacts(api_key, page=1, size=100):
    """Fetch artifacts from Harvard Art Museums API with pagination"""
    base_url = "https://api.harvardartmuseums.org/object"
    
    params = {
        "apikey": api_key,
        "page": page,
        "size": size
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    
    data = response.json()
    return data["records"], data["info"]

# Usage
api_key = os.getenv("HARVARD_API_KEY")
artifacts, info = fetch_artifacts(api_key, page=1, size=50)

print(f"Total artifacts available: {info['totalrecords']}")
print(f"Fetched: {len(artifacts)} artifacts")
```

### 2. ETL Pipeline

```python
import pandas as pd
import mysql.connector
from typing import List, Dict

class HarvardETL:
    def __init__(self, db_config):
        self.db_config = db_config
        self.conn = None
    
    def connect_db(self):
        """Establish database connection"""
        self.conn = mysql.connector.connect(
            host=self.db_config['host'],
            user=self.db_config['user'],
            password=self.db_config['password'],
            database=self.db_config['database']
        )
        return self.conn.cursor()
    
    def extract_metadata(self, artifacts: List[Dict]) -> pd.DataFrame:
        """Extract artifact metadata into DataFrame"""
        metadata = []
        
        for artifact in artifacts:
            metadata.append({
                'id': artifact.get('id'),
                'title': artifact.get('title'),
                'culture': artifact.get('culture'),
                'period': artifact.get('period'),
                'century': artifact.get('century'),
                'classification': artifact.get('classification'),
                'department': artifact.get('department'),
                'division': artifact.get('division'),
                'dated': artifact.get('dated'),
                'accession_number': artifact.get('accessionnumber'),
                'total_page_views': artifact.get('totalpageviews', 0),
                'total_unique_pageviews': artifact.get('totaluniquepageviews', 0),
                'url': artifact.get('url')
            })
        
        return pd.DataFrame(metadata)
    
    def extract_media(self, artifacts: List[Dict]) -> pd.DataFrame:
        """Extract media/image data from artifacts"""
        media_data = []
        
        for artifact in artifacts:
            artifact_id = artifact.get('id')
            images = artifact.get('images', [])
            
            for image in images:
                media_data.append({
                    'artifact_id': artifact_id,
                    'image_url': image.get('baseimageurl'),
                    'height': image.get('height'),
                    'width': image.get('width'),
                    'format': image.get('format')
                })
        
        return pd.DataFrame(media_data)
    
    def extract_colors(self, artifacts: List[Dict]) -> pd.DataFrame:
        """Extract color data from artifacts"""
        color_data = []
        
        for artifact in artifacts:
            artifact_id = artifact.get('id')
            colors = artifact.get('colors', [])
            
            for color in colors:
                color_data.append({
                    'artifact_id': artifact_id,
                    'color_hex': color.get('hex'),
                    'color_percent': color.get('percent'),
                    'color_spectrum': color.get('spectrum')
                })
        
        return pd.DataFrame(color_data)
    
    def load_metadata(self, df: pd.DataFrame):
        """Load metadata into SQL database"""
        cursor = self.connect_db()
        
        insert_query = """
        INSERT INTO artifactmetadata 
        (id, title, culture, period, century, classification, department, 
         division, dated, accession_number, total_page_views, 
         total_unique_pageviews, url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        title=VALUES(title), culture=VALUES(culture)
        """
        
        data = [tuple(row) for row in df.values]
        cursor.executemany(insert_query, data)
        self.conn.commit()
        cursor.close()
    
    def load_media(self, df: pd.DataFrame):
        """Load media data into SQL database"""
        cursor = self.connect_db()
        
        insert_query = """
        INSERT INTO artifactmedia (artifact_id, image_url, height, width, format)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        data = [tuple(row) for row in df.values]
        cursor.executemany(insert_query, data)
        self.conn.commit()
        cursor.close()
    
    def load_colors(self, df: pd.DataFrame):
        """Load color data into SQL database"""
        cursor = self.connect_db()
        
        insert_query = """
        INSERT INTO artifactcolors 
        (artifact_id, color_hex, color_percent, color_spectrum)
        VALUES (%s, %s, %s, %s)
        """
        
        data = [tuple(row) for row in df.values]
        cursor.executemany(insert_query, data)
        self.conn.commit()
        cursor.close()

# Usage
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

etl = HarvardETL(db_config)

# Extract
metadata_df = etl.extract_metadata(artifacts)
media_df = etl.extract_media(artifacts)
colors_df = etl.extract_colors(artifacts)

# Load
etl.load_metadata(metadata_df)
etl.load_media(media_df)
etl.load_colors(colors_df)
```

### 3. SQL Analytics Queries

```python
ANALYTICAL_QUERIES = {
    "artifacts_by_culture": """
        SELECT culture, COUNT(*) as count
        FROM artifactmetadata
        WHERE culture IS NOT NULL
        GROUP BY culture
        ORDER BY count DESC
        LIMIT 15
    """,
    
    "artifacts_by_century": """
        SELECT century, COUNT(*) as count
        FROM artifactmetadata
        WHERE century IS NOT NULL
        GROUP BY century
        ORDER BY count DESC
    """,
    
    "most_viewed_artifacts": """
        SELECT title, culture, century, total_page_views
        FROM artifactmetadata
        WHERE total_page_views > 0
        ORDER BY total_page_views DESC
        LIMIT 20
    """,
    
    "artifacts_with_images": """
        SELECT 
            CASE WHEN COUNT(am.media_id) > 0 THEN 'With Images' ELSE 'Without Images' END as has_images,
            COUNT(DISTINCT a.id) as artifact_count
        FROM artifactmetadata a
        LEFT JOIN artifactmedia am ON a.id = am.artifact_id
        GROUP BY has_images
    """,
    
    "color_distribution": """
        SELECT color_spectrum, COUNT(*) as count, AVG(color_percent) as avg_percent
        FROM artifactcolors
        WHERE color_spectrum IS NOT NULL
        GROUP BY color_spectrum
        ORDER BY count DESC
    """,
    
    "artifacts_by_department": """
        SELECT department, COUNT(*) as count
        FROM artifactmetadata
        WHERE department IS NOT NULL
        GROUP BY department
        ORDER BY count DESC
    """,
    
    "classification_breakdown": """
        SELECT classification, COUNT(*) as count
        FROM artifactmetadata
        WHERE classification IS NOT NULL
        GROUP BY classification
        ORDER BY count DESC
        LIMIT 10
    """
}

def execute_query(query_name: str, db_config: dict) -> pd.DataFrame:
    """Execute analytical query and return results as DataFrame"""
    conn = mysql.connector.connect(**db_config)
    
    query = ANALYTICAL_QUERIES[query_name]
    df = pd.read_sql(query, conn)
    
    conn.close()
    return df

# Usage
result = execute_query("artifacts_by_culture", db_config)
print(result)
```

### 4. Streamlit Dashboard

```python
import streamlit as st
import plotly.express as px

def main():
    st.set_page_config(page_title="Harvard Artifacts Analytics", layout="wide")
    
    st.title("🏛️ Harvard Art Museums Analytics Dashboard")
    
    # Sidebar for query selection
    st.sidebar.header("Select Analysis")
    query_options = list(ANALYTICAL_QUERIES.keys())
    selected_query = st.sidebar.selectbox("Choose a query:", query_options)
    
    # Database configuration from environment
    db_config = {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME')
    }
    
    if st.sidebar.button("Run Query"):
        with st.spinner("Executing query..."):
            try:
                result_df = execute_query(selected_query, db_config)
                
                st.subheader(f"Results: {selected_query.replace('_', ' ').title()}")
                st.dataframe(result_df, use_container_width=True)
                
                # Auto-generate visualization
                if len(result_df.columns) >= 2:
                    fig = px.bar(
                        result_df,
                        x=result_df.columns[0],
                        y=result_df.columns[1],
                        title=f"{selected_query.replace('_', ' ').title()}"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error executing query: {str(e)}")
    
    # ETL Section
    st.sidebar.header("Data Collection")
    num_pages = st.sidebar.number_input("Pages to fetch:", min_value=1, max_value=10, value=1)
    
    if st.sidebar.button("Fetch New Data"):
        api_key = os.getenv("HARVARD_API_KEY")
        etl = HarvardETL(db_config)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for page in range(1, num_pages + 1):
            status_text.text(f"Fetching page {page}/{num_pages}...")
            artifacts, info = fetch_artifacts(api_key, page=page, size=100)
            
            # ETL process
            metadata_df = etl.extract_metadata(artifacts)
            media_df = etl.extract_media(artifacts)
            colors_df = etl.extract_colors(artifacts)
            
            etl.load_metadata(metadata_df)
            etl.load_media(media_df)
            etl.load_colors(colors_df)
            
            progress_bar.progress(page / num_pages)
        
        status_text.text(f"✅ Successfully loaded {num_pages * 100} artifacts!")

if __name__ == "__main__":
    main()
```

## Running the Application

```bash
# Start Streamlit dashboard
streamlit run app.py

# The app will be available at http://localhost:8501
```

## Common Patterns

### Batch Processing with Rate Limiting

```python
import time

def batch_collect_artifacts(api_key, total_pages=10, delay=1):
    """Collect artifacts in batches with rate limiting"""
    all_artifacts = []
    
    for page in range(1, total_pages + 1):
        try:
            artifacts, info = fetch_artifacts(api_key, page=page)
            all_artifacts.extend(artifacts)
            
            print(f"Collected page {page}/{total_pages}")
            time.sleep(delay)  # Rate limiting
            
        except Exception as e:
            print(f"Error on page {page}: {str(e)}")
            continue
    
    return all_artifacts
```

### Data Quality Checks

```python
def validate_artifacts(df: pd.DataFrame) -> dict:
    """Perform data quality checks"""
    return {
        'total_records': len(df),
        'null_titles': df['title'].isna().sum(),
        'null_cultures': df['culture'].isna().sum(),
        'duplicate_ids': df['id'].duplicated().sum(),
        'valid_records': len(df[df['id'].notna() & df['title'].notna()])
    }

# Usage
quality_report = validate_artifacts(metadata_df)
print(quality_report)
```

## Troubleshooting

### API Rate Limiting
**Issue**: 429 Too Many Requests error

**Solution**: Add delays between requests
```python
import time
time.sleep(1)  # 1 second delay between API calls
```

### Database Connection Errors
**Issue**: Cannot connect to MySQL/TiDB

**Solution**: Verify environment variables and connection string
```python
# Test connection
try:
    conn = mysql.connector.connect(**db_config)
    print("✅ Database connected successfully")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {str(e)}")
```

### Missing Data in Results
**Issue**: Queries return empty or incomplete data

**Solution**: Check for NULL values and use COALESCE
```sql
SELECT 
    COALESCE(culture, 'Unknown') as culture,
    COUNT(*) as count
FROM artifactmetadata
GROUP BY culture
```

### Memory Issues with Large Datasets
**Issue**: Out of memory when processing many artifacts

**Solution**: Use chunked processing
```python
def process_in_chunks(artifacts, chunk_size=100):
    for i in range(0, len(artifacts), chunk_size):
        chunk = artifacts[i:i + chunk_size]
        etl.load_metadata(etl.extract_metadata(chunk))
```

## Advanced Usage

### Custom Query Builder

```python
def build_custom_query(filters: dict) -> str:
    """Build custom SQL query based on filters"""
    base_query = "SELECT * FROM artifactmetadata WHERE 1=1"
    
    if filters.get('culture'):
        base_query += f" AND culture = '{filters['culture']}'"
    
    if filters.get('century'):
        base_query += f" AND century = '{filters['century']}'"
    
    if filters.get('min_views'):
        base_query += f" AND total_page_views >= {filters['min_views']}"
    
    return base_query

# Usage in Streamlit
culture_filter = st.selectbox("Filter by culture:", ['All', 'American', 'Chinese', 'Greek'])
custom_query = build_custom_query({'culture': culture_filter if culture_filter != 'All' else None})
```

### Export Results

```python
def export_to_csv(df: pd.DataFrame, filename: str):
    """Export query results to CSV"""
    df.to_csv(filename, index=False)
    st.download_button(
        label="Download CSV",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name=filename,
        mime='text/csv'
    )
```
