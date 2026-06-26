---
name: web-search-by-searxng
description: Search using a custom SearXNG instance via HTTP API. Enables privacy-friendly web search by aggregating results from multiple search engines. Supports query, format (json/csv/rss), language, time range, categories, engines, pagination, and safe search filtering. Requires a user-provided or configured SearXNG instance URL.
---

# SearXNG Search

This skill enables web search using a custom SearXNG instance via its HTTP API.

## Overview

SearXNG is a privacy-respecting metasearch engine that aggregates results from multiple search engines. This skill allows you to search using a custom SearXNG instance URL.

## API Endpoints

- `GET /` or `GET /search` - Query parameters in URL
- `POST /` or `POST /search` - Form data

## Required Configuration

You need a SearXNG instance URL. The user can provide:
1. A public instance URL (e.g., `https://searx.be`)
2. A self-hosted instance URL
3. An environment variable `SEARXNG_URL` containing the instance URL

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `q` | Yes | Search query string |
| `format` | No | Output format: `json`, `csv`, `rss` (default: HTML) |
| `language` | No | Language code (e.g., `en`, `zh`, `de`) |
| `pageno` | No | Page number (default: 1) |
| `time_range` | No | Time filter: `day`, `month`, `year` |
| `categories` | No | Comma-separated category list |
| `engines` | No | Comma-separated engine list |
| `safesearch` | No | Safe search level: `0`, `1`, `2` |

## Categories and Engines

SearXNG organizes search into categories (tabs) with multiple engines per category.

**Available Categories:**
- `general` - General web search
- `images` - Image search
- `videos` - Video search
- `news` - News articles
- `map` - Maps and locations
- `music` - Music and audio
- `it` - IT/Technology resources
- `science` - Scientific publications
- `files` - Files and torrents
- `social_media` - Social media content

**Common Engines:**
- Web: `google`, `duckduckgo`, `bing`, `brave`, `startpage`, `wikipedia`
- Images: `google images`, `bing images`, `unsplash`, `flickr`
- Videos: `youtube`, `google videos`, `vimeo`, `dailymotion`
- News: `google news`, `bing news`, `reuters`
- IT: `github`, `stackoverflow`, `arch linux wiki`, `pypi`
- Science: `google scholar`, `arxiv`, `pubmed`

**Bang Syntax:** Use `!` prefix in queries to target specific engines:
- `!go python` - Search Google
- `!wp artificial intelligence` - Search Wikipedia
- `!github machine learning` - Search GitHub

For detailed engine lists and features, see [references/engines_and_categories.md](references/engines_and_categories.md).

## Usage

### Using the Python Script

```python
# Basic search
python scripts/searxng_search.py -u https://searx.example.org -q "python tutorial"

# JSON output
python scripts/searxng_search.py -u https://searx.example.org -q "python tutorial" --format json

# With language and time range
python scripts/searxng_search.py -u https://searx.example.org -q "news" --lang en --time-range day

# Use environment variable for URL
export SEARXNG_URL=https://searx.example.org
python scripts/searxng_search.py -q "search query"

# Search specific category
python scripts/searxng_search.py -u https://searx.example.org -q "AI" --categories news

# Search specific engines
python scripts/searxng_search.py -u https://searx.example.org -q "python" --engines google,stackoverflow
```

### Using HTTP Requests Directly

```python
import requests

url = "https://searx.example.org/search"
params = {
    "q": "python tutorial",
    "format": "json",
    "language": "en",
    "categories": "general,it",  # Multiple categories
    "engines": "google,duckduckgo"  # Specific engines
}

response = requests.get(url, params=params, timeout=30)
results = response.json()
```

### Bang Syntax in Query

```python
# Use bang syntax to target specific engines
params = {
    "q": "!github machine learning framework",  # Only search GitHub
    "format": "json"
}
```

## JSON Response Format

```json
{
  "query": "search query",
  "number_of_results": 1000000,
  "results": [
    {
      "title": "Result Title",
      "url": "https://example.com",
      "content": "Snippet text...",
      "engine": "google",
      "score": 1.0
    }
  ],
  "answers": [],
  "suggestions": [],
  "unresponsive_engines": []
}
```

## Important Notes

1. **Format Availability**: JSON/CSV/RSS formats must be enabled in the instance's `settings.yml`. Many public instances disable these formats.
2. **Rate Limiting**: Be respectful of the instance's resources. Add delays between requests.
3. **Self-Hosting**: For reliable API access, consider self-hosting a SearXNG instance.
4. **Time Range**: Not all engines support time range filtering. Check instance preferences.
5. **Engine Availability**: Not all engines are enabled on all instances. Check the instance's preferences page.

## Example Workflows

### Basic Web Search
1. Ask user for SearXNG instance URL or use configured URL
2. Construct search query
3. Call API with `format=json`
4. Parse and present results

### Category-Specific Search
1. Choose category based on query type (news, images, science, etc.)
2. Use `categories` parameter or bang syntax
3. Filter results as needed

### Multi-Page Search
1. Perform initial search
2. If more results needed, increment `pageno` parameter
3. Combine results from multiple pages

### Filtered Search
1. Use `time_range=day` for recent results
2. Use `safesearch=2` for strict filtering
3. Use `language` parameter for locale-specific results
4. Use `categories` or `engines` to narrow search scope

## References

- [engines_and_categories.md](references/engines_and_categories.md) - Complete list of engines and categories
