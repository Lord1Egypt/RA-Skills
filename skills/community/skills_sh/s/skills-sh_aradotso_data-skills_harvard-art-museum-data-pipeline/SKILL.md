---
name: harvard-art-museum-data-pipeline
description: Build ETL pipelines and analytics dashboards using Harvard Art Museums API with Python, SQL, and Streamlit
triggers:
  - how do I build a data pipeline with the Harvard Art Museums API
  - show me how to extract and transform Harvard museum data
  - help me create an ETL pipeline for art museum data
  - how to set up analytics dashboards for Harvard Art Museums
  - build a Streamlit app for museum artifact data
  - create SQL queries for Harvard Art Museums collection
  - implement ETL workflow for art museum API data
  - analyze Harvard museum artifacts with Python and SQL
---

# Harvard Art Museum Data Pipeline

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This skill enables you to build end-to-end data engineering and analytics applications using the Harvard Art Museums API. The project demonstrates ETL pipeline construction, SQL database design, analytical queries, and interactive Streamlit dashboards for museum artifact data.

## What This Project Does

The Harvard-Artifacts-Collection-Data-Engineering-Analytics-App provides:
- **API Integration**: Fetch artifact data from Harvard Art Museums API with pagination and rate limiting
- **ETL Pipeline**: Extract, transform, and load nested JSON into relational database tables
- **SQL Storage**: Structure data across `artifactmetadata`, `artifactmedia`, and `artifactcolors` tables
- **Analytics**: Execute predefined SQL queries for insights on artifacts, cultures, media, and colors
- **Visualization**: Interactive Plotly charts and Streamlit dashboards

## Installation

```bash
# Clone the repository
git clone https://github.com/Manali0711/Harvard-Artifacts-Collection-Data-Engineering-Analytics-App.git
cd Harvard-Artifacts-Collection-Data-Engineering-Analytics-App

# Install dependencies
pip install -r requirements.txt

# Required packages
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
DB_USER=your_db_username
DB_PASSWORD=your_db_password
DB_NAME=harvard_artifacts
```

### Obtaining API Key

1. Register at [Harvard Art Museums API](https://www.harvardartmuseums.org/collections/api)
2. Request an API key (free for non-commercial use)
3. Add to `.env` file

### Database Setup

```sql
-- Create database
CREATE DATABASE harvard_artifacts;
USE harvard_artifacts;

-- Artifact metadata table
CREATE TABLE artifactmetadata (
    id INT PRIMARY KEY,
    title VARCHAR(500),
    culture VARCHAR(255),
    classification VARCHAR(255),
    period VARCHAR(255),
    century VARCHAR(255),
    dated VARCHAR(255),
    department VARCHAR(255),
    division VARCHAR(255),
    technique VARCHAR(500),
    medium VARCHAR(500),
    dimensions VARCHAR(500),
    credit_line TEXT,
    accession_year INT,
    url TEXT,
    last_updated DATETIME
);

-- Artifact media table
CREATE TABLE artifactmedia (
    media_id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    base_image_url VARCHAR(500),
    primary_image_url TEXT,
    image_count INT,
    has_image BOOLEAN,
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
);

-- Artifact colors table
CREATE TABLE artifactcolors (
    color_id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    color_hex VARCHAR(10),
    color_percent FLOAT,
    color_spectrum VARCHAR(50),
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
);
```

## Core Functionality

### ETL Pipeline Implementation

```python
import requests
import pandas as pd
import mysql.connector
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

class HarvardETL:
    """ETL pipeline for Harvard Art Museums API"""
    
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
    
    def extract_artifacts(self, num_pages: int = 5, per_page: int = 100) -> List[Dict]:
        """Extract artifact data from API with pagination"""
        artifacts = []
        
        for page in range(1, num_pages + 1):
            params = {
                'apikey': self.api_key,
                'page': page,
                'size': per_page,
                'hasimage': 1  # Only artifacts with images
            }
            
            response = requests.get(self.base_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                artifacts.extend(data.get('records', []))
                print(f"Extracted page {page}: {len(data.get('records', []))} artifacts")
            else:
                print(f"Error on page {page}: {response.status_code}")
                break
        
        return artifacts
    
    def transform_metadata(self, artifacts: List[Dict]) -> pd.DataFrame:
        """Transform artifact data into metadata dataframe"""
        metadata = []
        
        for artifact in artifacts:
            metadata.append({
                'id': artifact.get('id'),
                'title': artifact.get('title'),
                'culture': artifact.get('culture'),
                'classification': artifact.get('classification'),
                'period': artifact.get('period'),
                'century': artifact.get('century'),
                'dated': artifact.get('dated'),
                'department': artifact.get('department'),
                'division': artifact.get('division'),
                'technique': artifact.get('technique'),
                'medium': artifact.get('medium'),
                'dimensions': artifact.get('dimensions'),
                'credit_line': artifact.get('creditline'),
                'accession_year': artifact.get('accessionyear'),
                'url': artifact.get('url'),
                'last_updated': pd.Timestamp.now()
            })
        
        return pd.DataFrame(metadata)
    
    def transform_media(self, artifacts: List[Dict]) -> pd.DataFrame:
        """Transform media data into dataframe"""
        media = []
        
        for artifact in artifacts:
            media.append({
                'artifact_id': artifact.get('id'),
                'base_image_url': artifact.get('baseimageurl'),
                'primary_image_url': artifact.get('primaryimageurl'),
                'image_count': len(artifact.get('images', [])),
                'has_image': 1 if artifact.get('primaryimageurl') else 0
            })
        
        return pd.DataFrame(media)
    
    def transform_colors(self, artifacts: List[Dict]) -> pd.DataFrame:
        """Transform color data into dataframe"""
        colors = []
        
        for artifact in artifacts:
            artifact_id = artifact.get('id')
            color_data = artifact.get('colors', [])
            
            for color in color_data:
                colors.append({
                    'artifact_id': artifact_id,
                    'color_hex': color.get('hex'),
                    'color_percent': color.get('percent'),
                    'color_spectrum': color.get('spectrum')
                })
        
        return pd.DataFrame(colors)
    
    def load_to_db(self, df: pd.DataFrame, table_name: str, if_exists: str = 'append'):
        """Load dataframe to MySQL database"""
        connection = mysql.connector.connect(**self.db_config)
        cursor = connection.cursor()
        
        try:
            # Convert DataFrame to list of tuples
            records = df.to_records(index=False).tolist()
            
            if table_name == 'artifactmetadata':
                sql = """INSERT INTO artifactmetadata 
                         (id, title, culture, classification, period, century, dated, 
                          department, division, technique, medium, dimensions, 
                          credit_line, accession_year, url, last_updated)
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                         ON DUPLICATE KEY UPDATE last_updated=VALUES(last_updated)"""
            
            elif table_name == 'artifactmedia':
                sql = """INSERT INTO artifactmedia 
                         (artifact_id, base_image_url, primary_image_url, image_count, has_image)
                         VALUES (%s, %s, %s, %s, %s)"""
            
            elif table_name == 'artifactcolors':
                sql = """INSERT INTO artifactcolors 
                         (artifact_id, color_hex, color_percent, color_spectrum)
                         VALUES (%s, %s, %s, %s)"""
            
            cursor.executemany(sql, records)
            connection.commit()
            print(f"Loaded {cursor.rowcount} records to {table_name}")
            
        except Exception as e:
            print(f"Error loading to {table_name}: {e}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
    
    def run_pipeline(self, num_pages: int = 5):
        """Execute complete ETL pipeline"""
        print("Starting ETL pipeline...")
        
        # Extract
        artifacts = self.extract_artifacts(num_pages=num_pages)
        print(f"Total artifacts extracted: {len(artifacts)}")
        
        # Transform
        metadata_df = self.transform_metadata(artifacts)
        media_df = self.transform_media(artifacts)
        colors_df = self.transform_colors(artifacts)
        
        # Load
        self.load_to_db(metadata_df, 'artifactmetadata')
        self.load_to_db(media_df, 'artifactmedia')
        self.load_to_db(colors_df, 'artifactcolors')
        
        print("ETL pipeline completed successfully!")

# Usage
if __name__ == "__main__":
    etl = HarvardETL()
    etl.run_pipeline(num_pages=10)
```

### SQL Analytics Queries

```python
class HarvardAnalytics:
    """Analytics queries for Harvard Art Museums data"""
    
    def __init__(self, db_config: dict):
        self.db_config = db_config
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """Execute SQL query and return results as DataFrame"""
        connection = mysql.connector.connect(**self.db_config)
        df = pd.read_sql(query, connection)
        connection.close()
        return df
    
    def artifacts_by_culture(self) -> pd.DataFrame:
        """Top 15 cultures by artifact count"""
        query = """
        SELECT culture, COUNT(*) as artifact_count
        FROM artifactmetadata
        WHERE culture IS NOT NULL
        GROUP BY culture
        ORDER BY artifact_count DESC
        LIMIT 15
        """
        return self.execute_query(query)
    
    def artifacts_by_century(self) -> pd.DataFrame:
        """Artifact distribution by century"""
        query = """
        SELECT century, COUNT(*) as artifact_count
        FROM artifactmetadata
        WHERE century IS NOT NULL
        GROUP BY century
        ORDER BY artifact_count DESC
        """
        return self.execute_query(query)
    
    def media_availability(self) -> pd.DataFrame:
        """Artifacts with and without images"""
        query = """
        SELECT 
            CASE WHEN has_image = 1 THEN 'With Image' ELSE 'No Image' END as media_status,
            COUNT(*) as count
        FROM artifactmedia
        GROUP BY has_image
        """
        return self.execute_query(query)
    
    def top_color_usage(self) -> pd.DataFrame:
        """Most common color spectrums"""
        query = """
        SELECT color_spectrum, COUNT(*) as usage_count,
               AVG(color_percent) as avg_percent
        FROM artifactcolors
        WHERE color_spectrum IS NOT NULL
        GROUP BY color_spectrum
        ORDER BY usage_count DESC
        LIMIT 10
        """
        return self.execute_query(query)
    
    def artifacts_by_department(self) -> pd.DataFrame:
        """Department-wise artifact distribution"""
        query = """
        SELECT department, COUNT(*) as artifact_count
        FROM artifactmetadata
        WHERE department IS NOT NULL
        GROUP BY department
        ORDER BY artifact_count DESC
        """
        return self.execute_query(query)
    
    def artifacts_by_accession_year(self) -> pd.DataFrame:
        """Artifacts acquired by year"""
        query = """
        SELECT accession_year, COUNT(*) as artifact_count
        FROM artifactmetadata
        WHERE accession_year IS NOT NULL
        GROUP BY accession_year
        ORDER BY accession_year DESC
        LIMIT 20
        """
        return self.execute_query(query)
```

### Streamlit Dashboard

```python
import streamlit as st
import plotly.express as px
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Harvard Art Museums Analytics",
    page_icon="🎨",
    layout="wide"
)

# Database configuration
db_config = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

analytics = HarvardAnalytics(db_config)

# Title
st.title("🎨 Harvard Art Museums Analytics Dashboard")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Navigation")
    analysis_type = st.selectbox(
        "Select Analysis",
        [
            "Artifacts by Culture",
            "Artifacts by Century",
            "Media Availability",
            "Color Usage",
            "Department Distribution",
            "Accession Timeline"
        ]
    )

# Main content
if analysis_type == "Artifacts by Culture":
    st.subheader("Top 15 Cultures by Artifact Count")
    df = analytics.artifacts_by_culture()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = px.bar(df, x='culture', y='artifact_count',
                     title='Artifact Distribution by Culture',
                     labels={'culture': 'Culture', 'artifact_count': 'Number of Artifacts'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.dataframe(df, use_container_width=True)

elif analysis_type == "Artifacts by Century":
    st.subheader("Artifact Distribution by Century")
    df = analytics.artifacts_by_century()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = px.bar(df, x='century', y='artifact_count',
                     title='Artifacts per Century',
                     labels={'century': 'Century', 'artifact_count': 'Count'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.dataframe(df, use_container_width=True)

elif analysis_type == "Media Availability":
    st.subheader("Image Availability Analysis")
    df = analytics.media_availability()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = px.pie(df, values='count', names='media_status',
                     title='Artifacts with/without Images')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.dataframe(df, use_container_width=True)

elif analysis_type == "Color Usage":
    st.subheader("Top Color Spectrum Usage")
    df = analytics.top_color_usage()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = px.bar(df, x='color_spectrum', y='usage_count',
                     title='Most Common Color Spectrums',
                     labels={'color_spectrum': 'Color Spectrum', 'usage_count': 'Usage Count'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.dataframe(df, use_container_width=True)

# Run ETL section
st.markdown("---")
st.subheader("Run ETL Pipeline")

col1, col2 = st.columns(2)

with col1:
    num_pages = st.number_input("Number of pages to fetch", min_value=1, max_value=50, value=5)

with col2:
    if st.button("Run ETL Pipeline"):
        with st.spinner("Running ETL pipeline..."):
            etl = HarvardETL()
            etl.run_pipeline(num_pages=num_pages)
            st.success("ETL pipeline completed successfully!")
```

## Common Patterns

### Incremental Data Loading

```python
def load_incremental(self, since_date: str):
    """Load only artifacts updated since specific date"""
    params = {
        'apikey': self.api_key,
        'updatedate': f'>{since_date}',
        'size': 100
    }
    
    response = requests.get(self.base_url, params=params)
    artifacts = response.json().get('records', [])
    
    # Process and load
    metadata_df = self.transform_metadata(artifacts)
    self.load_to_db(metadata_df, 'artifactmetadata', if_exists='replace')
```

### Custom Query Execution

```python
def run_custom_query(query: str) -> pd.DataFrame:
    """Execute user-provided SQL query"""
    analytics = HarvardAnalytics(db_config)
    return analytics.execute_query(query)

# Usage in Streamlit
custom_sql = st.text_area("Enter SQL Query")
if st.button("Execute"):
    result = run_custom_query(custom_sql)
    st.dataframe(result)
```

### Data Export

```python
def export_to_csv(df: pd.DataFrame, filename: str):
    """Export query results to CSV"""
    df.to_csv(filename, index=False)
    print(f"Data exported to {filename}")

# In Streamlit
if st.button("Export to CSV"):
    df = analytics.artifacts_by_culture()
    csv = df.to_csv(index=False)
    st.download_button("Download CSV", csv, "artifacts.csv", "text/csv")
```

## Troubleshooting

### API Rate Limiting

```python
import time

def extract_with_rate_limit(self, delay: float = 0.5):
    """Add delay between API requests"""
    for page in range(1, num_pages + 1):
        response = requests.get(self.base_url, params=params)
        # Process response
        time.sleep(delay)  # Prevent rate limiting
```

### Database Connection Issues

```python
def test_db_connection(db_config: dict) -> bool:
    """Test database connectivity"""
    try:
        connection = mysql.connector.connect(**db_config)
        connection.close()
        print("Database connection successful")
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False
```

### Handling Missing Data

```python
def safe_get(data: dict, key: str, default=None):
    """Safely extract values from nested JSON"""
    return data.get(key, default) if data else default

# Usage
culture = safe_get(artifact, 'culture', 'Unknown')
```

### Large Dataset Processing

```python
def batch_insert(self, df: pd.DataFrame, table_name: str, batch_size: int = 1000):
    """Insert data in batches for performance"""
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]
        self.load_to_db(batch, table_name)
        print(f"Inserted batch {i//batch_size + 1}")
```

## Running the Application

```bash
# Start Streamlit dashboard
streamlit run app.py

# Run ETL pipeline standalone
python etl_pipeline.py

# Execute analytics queries
python analytics.py
```

This skill provides complete coverage of the Harvard Art Museums data pipeline, from API extraction through SQL analytics to interactive visualization.
