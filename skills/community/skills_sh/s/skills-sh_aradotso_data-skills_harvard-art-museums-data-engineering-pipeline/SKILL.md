---
name: harvard-art-museums-data-engineering-pipeline
description: Build end-to-end ETL pipelines and analytics dashboards with Harvard Art Museums API using Python, SQL, and Streamlit
triggers:
  - how do I build a data pipeline with Harvard Art Museums API
  - set up ETL for Harvard artifacts collection
  - create analytics dashboard for museum data
  - integrate Harvard Art Museums API with SQL database
  - build Streamlit app for art collection analytics
  - extract and transform Harvard museum artifact data
  - query Harvard art collection data with SQL
  - visualize museum artifact data with Plotly
---

# Harvard Art Museums Data Engineering Pipeline

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This project demonstrates a complete data engineering workflow: extracting artifact data from the Harvard Art Museums API, transforming it into relational structures, loading into SQL databases, running analytical queries, and visualizing results through an interactive Streamlit dashboard.

## What It Does

- **API Integration**: Fetches artifact data from Harvard Art Museums with pagination and rate limiting
- **ETL Pipeline**: Transforms nested JSON into normalized relational tables
- **SQL Analytics**: Stores data in MySQL/TiDB with proper schema design
- **Interactive Dashboard**: Streamlit-based UI for querying and visualization
- **Data Visualization**: Plotly charts for analytical insights

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

### API Key Setup

Get your API key from [Harvard Art Museums API](https://www.harvardartmuseums.org/collections/api).

```python
# Store in .env file
HARVARD_API_KEY=your_api_key_here
```

### Database Configuration

```python
# Database connection settings (store in .env)
DB_HOST=your_database_host
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=harvard_artifacts
```

## Core Architecture

### ETL Pipeline Structure

```python
import requests
import pandas as pd
import mysql.connector
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

class HarvardArtETL:
    def __init__(self):
        self.api_key = os.getenv('HARVARD_API_KEY')
        self.base_url = "https://api.harvardartmuseums.org/object"
        self.db_config = {
            'host': os.getenv('DB_HOST'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_NAME')
        }
    
    def extract_artifacts(self, page: int = 1, size: int = 100) -> Dict:
        """Extract artifacts from Harvard API with pagination"""
        params = {
            'apikey': self.api_key,
            'page': page,
            'size': size
        }
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json()
    
    def transform_metadata(self, records: List[Dict]) -> pd.DataFrame:
        """Transform artifact records into metadata DataFrame"""
        metadata = []
        for record in records:
            metadata.append({
                'artifact_id': record.get('id'),
                'title': record.get('title'),
                'culture': record.get('culture'),
                'period': record.get('period'),
                'century': record.get('century'),
                'classification': record.get('classification'),
                'medium': record.get('medium'),
                'dimensions': record.get('dimensions'),
                'department': record.get('department'),
                'division': record.get('division'),
                'dated': record.get('dated'),
                'accessionyear': record.get('accessionyear')
            })
        return pd.DataFrame(metadata)
    
    def transform_media(self, records: List[Dict]) -> pd.DataFrame:
        """Transform media information into separate DataFrame"""
        media = []
        for record in records:
            artifact_id = record.get('id')
            if record.get('primaryimageurl'):
                media.append({
                    'artifact_id': artifact_id,
                    'media_type': 'image',
                    'media_url': record.get('primaryimageurl'),
                    'is_primary': True
                })
            for img in record.get('images', []):
                media.append({
                    'artifact_id': artifact_id,
                    'media_type': 'image',
                    'media_url': img.get('baseimageurl'),
                    'is_primary': False
                })
        return pd.DataFrame(media)
    
    def transform_colors(self, records: List[Dict]) -> pd.DataFrame:
        """Transform color data into separate DataFrame"""
        colors = []
        for record in records:
            artifact_id = record.get('id')
            for color in record.get('colors', []):
                colors.append({
                    'artifact_id': artifact_id,
                    'color_name': color.get('color'),
                    'color_hex': color.get('hex'),
                    'color_percentage': color.get('percent')
                })
        return pd.DataFrame(colors)
    
    def load_to_db(self, df: pd.DataFrame, table_name: str):
        """Load DataFrame to MySQL database"""
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()
        
        # Create insert query
        cols = ','.join(df.columns)
        placeholders = ','.join(['%s'] * len(df.columns))
        insert_query = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"
        
        # Batch insert
        for _, row in df.iterrows():
            cursor.execute(insert_query, tuple(row))
        
        conn.commit()
        cursor.close()
        conn.close()
```

## Database Schema

```sql
-- Artifact Metadata Table
CREATE TABLE artifactmetadata (
    artifact_id INT PRIMARY KEY,
    title VARCHAR(500),
    culture VARCHAR(255),
    period VARCHAR(255),
    century VARCHAR(100),
    classification VARCHAR(255),
    medium TEXT,
    dimensions VARCHAR(500),
    department VARCHAR(255),
    division VARCHAR(255),
    dated VARCHAR(255),
    accessionyear INT
);

-- Artifact Media Table
CREATE TABLE artifactmedia (
    media_id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    media_type VARCHAR(50),
    media_url TEXT,
    is_primary BOOLEAN,
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(artifact_id)
);

-- Artifact Colors Table
CREATE TABLE artifactcolors (
    color_id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    color_name VARCHAR(100),
    color_hex VARCHAR(10),
    color_percentage FLOAT,
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(artifact_id)
);
```

## Streamlit Application

```python
import streamlit as st
import pandas as pd
import plotly.express as px
from harvard_etl import HarvardArtETL

st.set_page_config(page_title="Harvard Art Analytics", layout="wide")

# Initialize ETL
etl = HarvardArtETL()

# Sidebar
st.sidebar.title("Harvard Art Museums Analytics")
page = st.sidebar.radio("Navigation", ["Data Collection", "Analytics", "Visualizations"])

if page == "Data Collection":
    st.title("📥 Data Collection Pipeline")
    
    num_pages = st.number_input("Number of pages to collect", min_value=1, max_value=100, value=5)
    page_size = st.selectbox("Records per page", [10, 25, 50, 100])
    
    if st.button("Start ETL Process"):
        with st.spinner("Extracting data from API..."):
            all_records = []
            for page_num in range(1, num_pages + 1):
                data = etl.extract_artifacts(page=page_num, size=page_size)
                all_records.extend(data.get('records', []))
                st.progress(page_num / num_pages)
            
            st.success(f"Extracted {len(all_records)} records")
        
        with st.spinner("Transforming data..."):
            df_metadata = etl.transform_metadata(all_records)
            df_media = etl.transform_media(all_records)
            df_colors = etl.transform_colors(all_records)
            st.success("Data transformed successfully")
        
        with st.spinner("Loading to database..."):
            etl.load_to_db(df_metadata, 'artifactmetadata')
            etl.load_to_db(df_media, 'artifactmedia')
            etl.load_to_db(df_colors, 'artifactcolors')
            st.success("Data loaded to SQL database")

elif page == "Analytics":
    st.title("📊 SQL Analytics Dashboard")
    
    queries = {
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
        "Artifacts with Images": """
            SELECT 
                COUNT(DISTINCT m.artifact_id) as with_images,
                COUNT(DISTINCT a.artifact_id) - COUNT(DISTINCT m.artifact_id) as without_images
            FROM artifactmetadata a
            LEFT JOIN artifactmedia m ON a.artifact_id = m.artifact_id
        """,
        "Top Colors in Collection": """
            SELECT color_name, COUNT(*) as usage_count, AVG(color_percentage) as avg_percentage
            FROM artifactcolors
            GROUP BY color_name
            ORDER BY usage_count DESC
            LIMIT 10
        """,
        "Artifacts by Department": """
            SELECT department, COUNT(*) as count
            FROM artifactmetadata
            WHERE department IS NOT NULL
            GROUP BY department
            ORDER BY count DESC
        """
    }
    
    selected_query = st.selectbox("Select Query", list(queries.keys()))
    
    if st.button("Execute Query"):
        conn = mysql.connector.connect(**etl.db_config)
        df_result = pd.read_sql(queries[selected_query], conn)
        conn.close()
        
        st.dataframe(df_result)
        
        # Auto-generate visualization
        if len(df_result.columns) == 2:
            fig = px.bar(df_result, x=df_result.columns[0], y=df_result.columns[1])
            st.plotly_chart(fig, use_container_width=True)

elif page == "Visualizations":
    st.title("📈 Data Visualizations")
    
    viz_type = st.selectbox("Visualization Type", [
        "Culture Distribution",
        "Century Timeline",
        "Color Analysis",
        "Media Availability"
    ])
    
    conn = mysql.connector.connect(**etl.db_config)
    
    if viz_type == "Culture Distribution":
        query = "SELECT culture, COUNT(*) as count FROM artifactmetadata WHERE culture IS NOT NULL GROUP BY culture ORDER BY count DESC LIMIT 15"
        df = pd.read_sql(query, conn)
        fig = px.bar(df, x='culture', y='count', title='Artifacts by Culture')
        st.plotly_chart(fig, use_container_width=True)
    
    elif viz_type == "Color Analysis":
        query = "SELECT color_name, AVG(color_percentage) as avg_pct FROM artifactcolors GROUP BY color_name ORDER BY avg_pct DESC LIMIT 10"
        df = pd.read_sql(query, conn)
        fig = px.pie(df, values='avg_pct', names='color_name', title='Color Distribution')
        st.plotly_chart(fig, use_container_width=True)
    
    conn.close()
```

## Running the Application

```bash
# Run Streamlit app
streamlit run app.py

# Access at http://localhost:8501
```

## Common Patterns

### Batch Processing with Rate Limiting

```python
import time

def collect_all_artifacts(max_pages: int = 50):
    """Collect artifacts with rate limiting"""
    etl = HarvardArtETL()
    all_records = []
    
    for page in range(1, max_pages + 1):
        try:
            data = etl.extract_artifacts(page=page, size=100)
            all_records.extend(data.get('records', []))
            time.sleep(0.5)  # Rate limiting
        except Exception as e:
            print(f"Error on page {page}: {e}")
            continue
    
    return all_records
```

### Incremental Loading

```python
def incremental_load():
    """Load only new artifacts"""
    conn = mysql.connector.connect(**etl.db_config)
    cursor = conn.cursor()
    
    # Get max artifact_id
    cursor.execute("SELECT MAX(artifact_id) FROM artifactmetadata")
    max_id = cursor.fetchone()[0] or 0
    
    # Fetch only newer artifacts
    # Implementation depends on API capabilities
    
    conn.close()
```

## Troubleshooting

**API Rate Limiting**: Add `time.sleep()` between requests or implement exponential backoff.

**Database Connection Errors**: Verify credentials in `.env` and ensure database is accessible.

**Missing Data**: Handle NULL values in transformations with `.get()` and default values.

**Memory Issues**: Process data in smaller batches rather than loading all at once.

**Duplicate Keys**: Use `INSERT IGNORE` or `ON DUPLICATE KEY UPDATE` for upsert behavior.
