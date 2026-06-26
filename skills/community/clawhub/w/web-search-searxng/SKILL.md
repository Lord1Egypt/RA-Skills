---
name: searxng
description: Search the web using SearXNG meta-search engine. Use when the user wants to search the web, find current information, look up facts, news, or any query that requires web search capabilities. Integrates with SearXNG instances to provide search results across multiple engines. Use for queries like "search for X", "look up Y", "find information about Z", or when real-time web data is needed.
---

# SearXNG Search

Web search integration using SearXNG meta-search engine. SearXNG aggregates results from multiple search engines (Google, Bing, DuckDuckGo, etc.) without tracking or ads.

## Quick Start

```bash
# Search
python scripts/search.py "quantum computing latest research"

# With specific engine
python scripts/search.py "weather in Tokyo" --engines duckduckgo

# News search
python scripts/search.py "AI breakthroughs 2024" --category news
```

## How It Works

```
User Query
    ↓
Format Search Parameters
    ↓
Call SearXNG API
    ↓
Aggregate Results
    ↓
Return Formatted Results
```

## Configuration

Edit `config/searxng.yaml`:

```yaml
# SearXNG instance URL
# Use public instance or your own
base_url: "https://searx.be"  # or your local instance

# Default search settings
defaults:
  language: "en-US"
  safesearch: 0  # 0 = off, 1 = moderate, 2 = strict
  time_range: ""  # day, week, month, year
  results_per_page: 10

# Preferred engines (optional)
engines:
  - google
  - duckduckgo
  - bing
  - brave
  - wikipedia

# Categories
categories:
  general: "general"
  news: "news"
  images: "images"
  videos: "videos"
  files: "files"
```

## File Structure

```
searxng/
├── SKILL.md                          # This file
├── requirements.txt                    # Dependencies
│
├── config/
│   └── searxng.yaml                  # Configuration
│
└── scripts/
    └── search.py                     # Search functionality
```

## Usage

### CLI

```bash
# Basic search
python scripts/search.py "python async tutorial"

# Limit results
python scripts/search.py "machine learning" --limit 5

# Specific category
python scripts/search.py "breaking news" --category news

# Time range
python scripts/search.py "tech announcements" --time week

# Specific engines
python scripts/search.py "wikipedia python" --engines wikipedia

# JSON output
python scripts/search.py "docker tutorial" --json
```

### Python API

```python
from searxng import SearXNGClient

# Initialize
client = SearXNGClient()

# Search
results = client.search("quantum computing")

# Access results
for result in results["results"]:
    print(f"{result['title']}: {result['url']}")

# Search with options
results = client.search(
    query="AI safety",
    category="news",
    time_range="month",
    limit=5
)
```

## Search Categories

| Category | Use For |
|----------|---------|
| general | Standard web search |
| news | News articles |
| images | Image search |
| videos | Video search |
| files | File search (PDFs, etc.) |
| science | Scientific papers |
| social media | Social platforms |

## Features

### Multiple Engine Aggregation

Results from 70+ search engines including:
- Google, Bing, DuckDuckGo
- Wikipedia, Wikidata
- GitHub, Stack Overflow
- News sources (BBC, Reuters, etc.)
- Academic (arXiv, PubMed)

### Privacy

- No tracking
- No ads
- Self-hostable
- Open source

### Rate Limiting

Built-in rate limiting to respect SearXNG instances:
```python
# Automatic delay between requests
client = SearXNGClient(rate_limit=1.0)  # 1 second between calls
```

## Response Format

```json
{
  "query": "quantum computing",
  "number_of_results": 10,
  "results": [
    {
      "title": "Quantum Computing - Wikipedia",
      "url": "https://en.wikipedia.org/wiki/Quantum_computing",
      "content": "Quantum computing is a type of computation...",
      "engine": "wikipedia",
      "score": 1.0
    }
  ],
  "suggestions": ["quantum computing explained", "quantum computing applications"],
  "infobox": {}  // Knowledge panel if available
}
```

## Testing

```bash
# Run search tests
python tests/test_search.py
```

## Troubleshooting

### "Connection refused"
```bash
# Check if SearXNG instance is reachable
curl https://your-searx-instance/healthz
```

### "No results"
- Try different engines: `--engines google,duckduckgo`
- Check category: `--category general`
- Verify instance isn't rate-limiting you

### "Rate limited"
- Add delay between requests
- Use different SearXNG instance
- Self-host your own instance

## Self-Hosting

Deploy your own SearXNG:

```bash
# Docker
docker run -d --name searxng -p 8080:8080 \
  -v searxng-config:/etc/searxng \
  searxng/searxng:latest

# Then update config/searxng.yaml
base_url: "http://localhost:8080"
```

## Public Instances

Popular public SearXNG instances:
- https://searx.be
- https://search.sapti.me
- https://searx.tiekoetter.com
- https://search.bus-hit.me

> Note: Public instances may have rate limits. For heavy use, self-host.

## Requirements

- Python 3.8+
- requests library
- SearXNG instance (public or self-hosted)
