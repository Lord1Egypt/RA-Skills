---
name: web-reader-pro
description: "Advanced web content extraction skill for OpenClaw using multi-tier fallback strategy (Jina → Scrapling → WebFetch) with intelligent routing, caching, quality scoring, and domain learning. Use when: reading article content, extracting web page text, scraping dynamic JS-heavy pages, or fetching WeChat official account articles."
metadata:
  author: 0xcjl
  version: "1.0.0"
---

# Web Reader Pro - OpenClaw Skill

## Overview

Web Reader Pro is an advanced web content extraction skill for OpenClaw that uses a multi-tier fallback strategy with intelligent routing, caching, and quality assessment.

## Features

### 1. Three-Tier Fallback Strategy
- **Tier 1: Jina Reader API** - Fast, reliable, best for most websites
- **Tier 2: Scrapling + Playwright** - Dynamic content rendering for JS-heavy sites
- **Tier 3: WebFetch Fallback** - Basic extraction for simple pages

### 2. Jina Quota Monitoring
- Tracks API call count with persistent counter
- Warning alerts when approaching quota limits
- Automatic fallback to lower-tier methods when quota exhausted

### 3. Smart Cache Layer
- Short-term caching (configurable TTL, default 1 hour)
- Cache key based on URL hash
- Reduces redundant API calls

### 4. Extraction Quality Scoring
- Scores based on: word count, title detection, content density
- Minimum quality threshold (default: 200 words + valid title)
- Auto-escalation to next tier if quality below threshold

### 5. Domain-Level Routing Learning
- Learns optimal extraction tier per domain
- Persists learned routes in local JSON database
- Adapts based on historical success rates

### 6. Retry with Exponential Backoff
- Configurable max retries per tier (default: 3)
- Exponential backoff: 1s, 2s, 4s, 8s...
- Respects rate limits and transient failures

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install Scrapling (requires Node.js)
./scripts/install_scrapling.sh

# Or install Scrapling manually
npm install -g @scrapinghub/scrapling
```

## Usage

### Basic Usage

```python
from scripts.web_reader_pro import WebReaderPro

reader = WebReaderPro()
result = reader.fetch("https://example.com")
print(result['title'])
print(result['content'])
```

### Advanced Configuration

```python
reader = WebReaderPro(
    jina_api_key="your-jina-key",      # Optional: set via env JINA_API_KEY
    cache_ttl=3600,                      # Cache TTL in seconds (default: 3600)
    quality_threshold=200,               # Min word count for quality (default: 200)
    max_retries=3,                       # Max retries per tier (default: 3)
    enable_learning=True,                # Enable domain learning (default: True)
    scrapling_path="/usr/local/bin/scrapling"  # Path to scrapling binary
)
```

## Result Format

```python
{
    "title": "Page Title",
    "content": "Extracted content in markdown...",
    "url": "https://example.com",
    "tier_used": "jina|scrapling|webfetch",
    "quality_score": 85,
    "cached": False,
    "domain_learned_tier": "jina",
    "extracted_at": "2024-01-01T00:00:00Z"
}
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `JINA_API_KEY` | Jina Reader API key | Required for Tier 1 |
| `WEB_READER_CACHE_DIR` | Cache directory path | `~/.openclaw/cache/web-reader-pro/` |
| `WEB_READER_LEARNING_DB` | Learning database path | `~/.openclaw/data/web-reader-pro/routes.json` |
| `WEB_READER_JINA_QUOTA` | Jina quota limit | `100000` |

## API Reference

### WebReaderPro.fetch(url, force_refresh=False)

Fetch and extract content from a URL.

**Parameters:**
- `url` (str): Target URL
- `force_refresh` (bool): Bypass cache if True

**Returns:** Dict with title, content, metadata

### WebReaderPro.fetch_with_tier(url, preferred_tier)

Fetch using a specific tier (bypassing automatic selection).

**Parameters:**
- `url` (str): Target URL
- `preferred_tier` (str): "jina", "scrapling", or "webfetch"

### WebReaderPro.get_jina_status()

Get current Jina API quota usage.

**Returns:** Dict with count, limit, percentage, warnings

### WebReaderPro.clear_cache(url=None)

Clear cache for specific URL or all URLs.

**Parameters:**
- `url` (str, optional): Specific URL to clear, or None for all

### WebReaderPro.get_domain_routes()

Get learned domain-to-tier mappings.

**Returns:** Dict of domain -> preferred tier

## Tier Comparison

| Tier | Speed | JS Rendering | Best For | Cost |
|------|-------|--------------|----------|------|
| Jina | Fast | No | Static pages, articles | API calls |
| Scrapling | Medium | Yes | SPAs, dynamic content | CPU |
| WebFetch | Fastest | No | Simple pages, fallbacks | Free |

## License

MIT
