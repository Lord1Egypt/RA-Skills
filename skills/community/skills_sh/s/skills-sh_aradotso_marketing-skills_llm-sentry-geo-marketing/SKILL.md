---
name: llm-sentry-geo-marketing
description: GEO (Generative Engine Optimization) monitoring platform for tracking brand mentions in AI search engines like DeepSeek and Doubao
triggers:
  - monitor my brand in AI search results
  - track GEO performance across AI engines
  - analyze citations in generative search
  - set up AI search monitoring with LLM Sentry
  - measure brand share of voice in AI responses
  - automate GEO tracking and analysis
  - extract reference links from AI answers
  - compare brand visibility in DeepSeek and Doubao
---

# LLM Sentry GEO Marketing Skill

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

## What This Project Does

LLM Sentry is an automated monitoring and analysis platform for **GEO (Generative Engine Optimization)**. It tracks how AI search engines (DeepSeek, Doubao, Bocha) mention brands and analyze citation sources in their responses. The platform uses browser automation (Playwright) to simulate real user queries, extract AI responses, parse reference links, and calculate Share of Voice (SoV) metrics.

**Core capabilities:**
- Real-time brand exposure monitoring in AI search results
- Citation source extraction and domain analysis
- Multi-round query execution for stability testing
- Desktop client (Wails + Go + React) with local SQLite storage
- RESTful API for task automation
- PostgreSQL-based data persistence

## Project Structure

This is a monorepo with three main components:

```
GEO/
├── geo_db/                  # PostgreSQL database service
├── llm_sentry_monitor/      # Python monitoring service (Playwright-based)
└── geo_client2/             # Desktop client (Wails + Go + React)
```

## Installation

### Prerequisites

- Python 3.11+ with `uv` package manager
- Docker and Docker Compose
- PostgreSQL 15+ (via Docker)
- For desktop client: Go 1.21+, Node.js 18+, Wails v2

### Quick Setup with Makefile

```bash
# Clone the repository
git clone https://github.com/daijinma/geo_marketing.git
cd geo_marketing

# Initialize environment and install dependencies
make setup

# Start PostgreSQL database
make db

# Run monitoring service
make run
```

### Manual Setup

```bash
# Create virtual environment with uv
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Python dependencies
cd llm_sentry_monitor
uv pip install -e ".[dev]"

# Install Playwright browsers
playwright install chromium

# Start database
cd ../geo_db
docker-compose up -d
```

### Desktop Client Setup

```bash
cd geo_client2

# Install frontend dependencies
cd frontend
pnpm install

# Install Go dependencies
cd ..
go mod tidy

# Run in development mode
wails dev

# Build for production
wails build
```

## Database Schema

The system uses two main tables:

**Records table** (monitoring results):
```sql
CREATE TABLE records (
    id SERIAL PRIMARY KEY,
    query VARCHAR(500) NOT NULL,
    provider VARCHAR(50) NOT NULL,
    response_text TEXT,
    raw_citations JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Citations table** (extracted references):
```sql
CREATE TABLE citations (
    id SERIAL PRIMARY KEY,
    record_id INTEGER REFERENCES records(id),
    url TEXT NOT NULL,
    domain VARCHAR(255),
    title VARCHAR(500),
    sequence INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## API Usage

### Start API Server

```python
# llm_sentry_monitor/main.py
from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="LLM Sentry API")
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Start server:
```bash
cd llm_sentry_monitor
python main.py
```

### Create Monitoring Task

**POST** `/mock`

```bash
curl -X POST http://localhost:8000/mock \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": ["AI search engines", "generative search optimization"],
    "platforms": ["deepseek", "doubao"],
    "query_count": 3,
    "settings": {
      "headless": false,
      "timeout": 60000,
      "delay_between_tasks": 5
    }
  }'
```

Python example:

```python
import requests

payload = {
    "keywords": ["AI搜索引擎对比", "DeepSeek vs ChatGPT"],
    "platforms": ["deepseek", "doubao"],
    "query_count": 2,
    "settings": {
        "headless": True,
        "timeout": 60000,
        "delay_between_tasks": 3
    }
}

response = requests.post("http://localhost:8000/mock", json=payload)
results = response.json()

for result in results:
    print(f"Query: {result['query']}")
    print(f"Platform: {result['provider']}")
    print(f"Citations: {len(result['citations'])}")
```

## Provider Implementation Pattern

Each AI platform has a dedicated provider class:

```python
# llm_sentry_monitor/providers/base.py
from abc import ABC, abstractmethod
from playwright.async_api import Page

class BaseProvider(ABC):
    def __init__(self, page: Page):
        self.page = page
    
    @abstractmethod
    async def search(self, query: str) -> dict:
        """Execute search and return response + citations"""
        pass
    
    @abstractmethod
    async def login(self) -> bool:
        """Handle authentication if needed"""
        pass
```

Example DeepSeek provider:

```python
# llm_sentry_monitor/providers/deepseek.py
from .base import BaseProvider
import asyncio

class DeepSeekProvider(BaseProvider):
    BASE_URL = "https://chat.deepseek.com"
    
    async def search(self, query: str) -> dict:
        await self.page.goto(self.BASE_URL)
        
        # Enable search mode
        search_toggle = await self.page.wait_for_selector('[data-testid="search-toggle"]')
        await search_toggle.click()
        
        # Enter query
        input_box = await self.page.wait_for_selector('textarea[placeholder*="Ask"]')
        await input_box.fill(query)
        await input_box.press("Enter")
        
        # Wait for response
        await asyncio.sleep(5)
        response_text = await self.page.text_content('.response-content')
        
        # Extract citations
        citations = await self.page.locator('.citation-link').all()
        citation_data = []
        for idx, citation in enumerate(citations, 1):
            url = await citation.get_attribute('href')
            title = await citation.text_content()
            citation_data.append({
                "sequence": idx,
                "url": url,
                "title": title
            })
        
        return {
            "query": query,
            "provider": "deepseek",
            "response_text": response_text,
            "citations": citation_data
        }
```

## Core Domain Extraction Logic

```python
# llm_sentry_monitor/core/parser.py
import tldextract
from urllib.parse import urlparse

def extract_domain(url: str) -> str:
    """Extract clean domain from URL"""
    parsed = tldextract.extract(url)
    domain = f"{parsed.domain}.{parsed.suffix}"
    return domain

def calculate_sov(citations: list[dict]) -> dict:
    """Calculate Share of Voice by domain"""
    domain_counts = {}
    total = len(citations)
    
    for citation in citations:
        domain = extract_domain(citation['url'])
        domain_counts[domain] = domain_counts.get(domain, 0) + 1
    
    sov = {
        domain: {
            "count": count,
            "percentage": round(count / total * 100, 2)
        }
        for domain, count in domain_counts.items()
    }
    
    return sov
```

## Database Operations

```python
# llm_sentry_monitor/core/database.py
import psycopg2
import os
import json

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            user=os.getenv("DB_USER", "geo_user"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME", "geo_db")
        )
    
    def save_record(self, query: str, provider: str, response_text: str, citations: list) -> int:
        """Save monitoring record and return record_id"""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO records (query, provider, response_text, raw_citations)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (query, provider, response_text, json.dumps(citations))
            )
            record_id = cur.fetchone()[0]
            self.conn.commit()
            return record_id
    
    def save_citations(self, record_id: int, citations: list):
        """Save individual citations linked to record"""
        with self.conn.cursor() as cur:
            for citation in citations:
                domain = extract_domain(citation['url'])
                cur.execute(
                    """
                    INSERT INTO citations (record_id, url, domain, title, sequence)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (record_id, citation['url'], domain, citation.get('title'), citation['sequence'])
                )
            self.conn.commit()
```

## Running Monitoring Tasks

### Single Query Example

```python
from playwright.async_api import async_playwright
from providers.deepseek import DeepSeekProvider
from core.database import Database

async def run_monitoring():
    db = Database()
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        provider = DeepSeekProvider(page)
        
        result = await provider.search("最好的AI搜索引擎推荐")
        
        # Save to database
        record_id = db.save_record(
            query=result['query'],
            provider=result['provider'],
            response_text=result['response_text'],
            citations=result['citations']
        )
        db.save_citations(record_id, result['citations'])
        
        await browser.close()
        print(f"Saved record #{record_id} with {len(result['citations'])} citations")

# Run
import asyncio
asyncio.run(run_monitoring())
```

### Multi-Round Query Example

```python
async def run_multi_round_monitoring(keywords: list, platforms: list, rounds: int):
    db = Database()
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        for keyword in keywords:
            for platform in platforms:
                page = await browser.new_page()
                
                # Get provider class
                if platform == "deepseek":
                    provider = DeepSeekProvider(page)
                elif platform == "doubao":
                    provider = DoubaoProvider(page)
                
                for round_num in range(1, rounds + 1):
                    print(f"Round {round_num}/{rounds}: {keyword} on {platform}")
                    
                    result = await provider.search(keyword)
                    record_id = db.save_record(
                        query=result['query'],
                        provider=result['provider'],
                        response_text=result['response_text'],
                        citations=result['citations']
                    )
                    db.save_citations(record_id, result['citations'])
                    
                    # Delay between rounds
                    await asyncio.sleep(5)
                
                await page.close()
        
        await browser.close()
```

## Desktop Client (Wails) Backend

```go
// geo_client2/backend/app.go
package backend

import (
    "context"
    "database/sql"
    _ "github.com/mattn/go-sqlite3"
)

type App struct {
    ctx context.Context
    db  *sql.DB
}

func NewApp() *App {
    return &App{}
}

func (a *App) startup(ctx context.Context) {
    a.ctx = ctx
    
    // Initialize SQLite
    db, err := sql.Open("sqlite3", "./geo_sentry.db")
    if err != nil {
        panic(err)
    }
    a.db = db
    
    // Create tables
    a.initDatabase()
}

func (a *App) CreateTask(keywords []string, platforms []string, queryCount int) (string, error) {
    // Insert task into database
    tx, _ := a.db.Begin()
    result, err := tx.Exec(`
        INSERT INTO tasks (keywords, platforms, query_count, status)
        VALUES (?, ?, ?, 'pending')
    `, strings.Join(keywords, ","), strings.Join(platforms, ","), queryCount)
    
    if err != nil {
        tx.Rollback()
        return "", err
    }
    
    tx.Commit()
    taskID, _ := result.LastInsertId()
    
    // Start monitoring in background
    go a.executeTask(taskID)
    
    return fmt.Sprintf("Task %d created", taskID), nil
}
```

## Configuration

### Environment Variables

Create `.env` file in `llm_sentry_monitor/`:

```bash
# Database
DB_HOST=localhost
DB_PORT=5432
DB_USER=geo_user
DB_PASSWORD=your_secure_password
DB_NAME=geo_db

# Playwright
HEADLESS_MODE=false
BROWSER_TIMEOUT=60000

# API
API_PORT=8000
DELAY_BETWEEN_TASKS=5
```

### Settings File

```python
# llm_sentry_monitor/config/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "geo_user"
    db_password: str
    db_name: str = "geo_db"
    
    headless_mode: bool = False
    browser_timeout: int = 60000
    delay_between_tasks: int = 5
    
    class Config:
        env_file = ".env"

settings = Settings()
```

## Common Patterns

### Pattern 1: Batch Keyword Monitoring

```python
async def monitor_keyword_matrix(brands: list, question_templates: list):
    """Monitor multiple brands across question patterns"""
    keywords = []
    
    for brand in brands:
        for template in question_templates:
            keywords.append(template.format(brand=brand))
    
    await run_multi_round_monitoring(
        keywords=keywords,
        platforms=["deepseek", "doubao"],
        rounds=3
    )
```

### Pattern 2: Citation Analysis Pipeline

```python
def analyze_citations_by_brand(brand: str, days: int = 7):
    """Analyze citation sources for a brand over time"""
    db = Database()
    
    with db.conn.cursor() as cur:
        cur.execute("""
            SELECT c.domain, COUNT(*) as mentions
            FROM citations c
            JOIN records r ON c.record_id = r.id
            WHERE r.query LIKE %s
            AND r.created_at >= NOW() - INTERVAL '%s days'
            GROUP BY c.domain
            ORDER BY mentions DESC
        """, (f"%{brand}%", days))
        
        results = cur.fetchall()
        
    return [{"domain": row[0], "mentions": row[1]} for row in results]
```

### Pattern 3: Share of Voice Calculation

```python
def calculate_brand_sov(brands: list[str], query: str):
    """Calculate Share of Voice for multiple brands"""
    db = Database()
    
    with db.conn.cursor() as cur:
        cur.execute("""
            SELECT r.response_text
            FROM records r
            WHERE r.query = %s
            ORDER BY r.created_at DESC
            LIMIT 1
        """, (query,))
        
        response = cur.fetchone()[0]
    
    sov = {}
    for brand in brands:
        mentions = response.lower().count(brand.lower())
        sov[brand] = mentions
    
    total = sum(sov.values())
    return {
        brand: {
            "mentions": count,
            "percentage": round(count / total * 100, 2) if total > 0 else 0
        }
        for brand, count in sov.items()
    }
```

## Troubleshooting

### Issue: Playwright Browser Not Found

```bash
# Install browsers explicitly
playwright install chromium

# Or install all browsers
playwright install
```

### Issue: Database Connection Failed

```bash
# Check database is running
docker ps | grep postgres

# Restart database
cd geo_db
docker-compose restart

# Check connection
psql -h localhost -U geo_user -d geo_db
```

### Issue: Login Required During Headless Mode

First run in non-headless mode to complete login:

```python
# In settings or API call
"settings": {
    "headless": false
}
```

After successful login, browser will save cookies. Then enable headless mode.

### Issue: Citations Not Extracted

Check selector patterns in provider code:

```python
# Debug citation extraction
citations = await page.locator('.citation-link').all()
print(f"Found {len(citations)} citations")

# Try alternative selectors
citations = await page.locator('a[data-citation]').all()
```

### Issue: Rate Limiting or Blocking

Add delays between requests:

```python
# In settings
"settings": {
    "delay_between_tasks": 10  # Increase to 10 seconds
}

# Or add random delays
import random
await asyncio.sleep(random.uniform(5, 15))
```

## Makefile Commands

```bash
make setup    # Initialize environment with uv
make db       # Start PostgreSQL database
make run      # Run monitoring service
make test     # Run tests
make clean    # Stop database and clean cache
make help     # Show all available commands
```

## Key Metrics to Track

1. **Brand Mention Rate**: Percentage of queries where brand appears
2. **Citation Count**: Number of reference links per query
3. **Domain Distribution**: Top domains cited by AI
4. **Position Analysis**: Average position of brand mentions
5. **Share of Voice**: Brand percentage vs. competitors
6. **Stability Score**: Consistency across multi-round queries
