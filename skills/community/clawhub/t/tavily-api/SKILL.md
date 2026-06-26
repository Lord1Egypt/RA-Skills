---
name: tavily
description: |
  Tavily API integration with managed API key authentication. Perform AI-powered web search, extract content from URLs, crawl websites, map site structure, and run research tasks.
  Use this skill when users want to search the web, extract page content, crawl websites, discover URLs, or conduct in-depth research with citations.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---

# Tavily

Access the Tavily API with managed API key authentication. Perform AI-powered web searches, extract content from URLs, crawl websites, map site structure, and run in-depth research tasks.

## Quick Start

```bash
# Search the web
python <<'EOF'
import urllib.request, os, json
data = json.dumps({"query": "latest AI news", "max_results": 5}).encode()
req = urllib.request.Request('https://gateway.maton.ai/tavily/search', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://gateway.maton.ai/tavily/{endpoint}
```

Replace `{endpoint}` with the Tavily API endpoint (`search`, `extract`, `crawl`, `map`, `research`). The gateway proxies requests to `api.tavily.com` and automatically injects your API key.

## Authentication

All requests require the Maton API key in the Authorization header:

```
Authorization: Bearer $MATON_API_KEY
```

**Environment Variable:** Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### Getting Your API Key

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key

## Connection Management

Manage your Tavily API key connections at `https://ctrl.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=tavily&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'tavily', 'method': 'API_KEY'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

Open the returned `url` in a browser to enter your Tavily API key.

### Get Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Delete Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Specifying Connection

If you have multiple Tavily connections, specify which one to use with the `Maton-Connection` header:

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({"query": "AI news"}).encode()
req = urllib.request.Request('https://gateway.maton.ai/tavily/search', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If omitted, the gateway uses the default (oldest) active connection.

## API Reference

### Search

Perform AI-powered web search with optional answer generation.

```bash
POST /tavily/search
Content-Type: application/json

{
  "query": "What is artificial intelligence?",
  "max_results": 5
}
```

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | string | Yes | Search query string |
| max_results | integer | No | Number of results (0-20, default 5) |
| search_depth | string | No | `basic`, `advanced`, `fast`, `ultra-fast` (default: basic) |
| topic | string | No | `general` or `news` (default: general) |
| include_answer | boolean/string | No | `true`, `false`, `basic`, `advanced` |
| include_raw_content | boolean/string | No | `true`, `false`, `markdown`, `text` |
| include_images | boolean | No | Include image results |
| include_domains | array | No | Only search these domains (max 300) |
| exclude_domains | array | No | Exclude these domains (max 150) |
| time_range | string | No | `day`, `week`, `month`, `year` |
| start_date | string | No | Filter by date (YYYY-MM-DD) |
| end_date | string | No | Filter by date (YYYY-MM-DD) |

**Response:**

```json
{
  "query": "What is artificial intelligence?",
  "answer": "Artificial intelligence (AI) is...",
  "results": [
    {
      "title": "What is AI?",
      "url": "https://example.com/ai",
      "content": "AI is a branch of computer science...",
      "score": 0.95
    }
  ],
  "response_time": 0.55
}
```

### Extract

Extract content from one or more URLs.

```bash
POST /tavily/extract
Content-Type: application/json

{
  "urls": ["https://example.com/article"],
  "format": "markdown"
}
```

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| urls | string/array | Yes | URL or array of URLs to extract |
| query | string | No | User intent for reranking content |
| chunks_per_source | integer | No | Max chunks per source (1-5, default 3) |
| extract_depth | string | No | `basic` or `advanced` (default: basic) |
| format | string | No | `markdown` or `text` (default: markdown) |
| include_images | boolean | No | Include extracted images |
| timeout | float | No | Max wait time in seconds (1-60) |

**Response:**

```json
{
  "results": [
    {
      "url": "https://example.com/article",
      "raw_content": "# Article Title\n\nContent in markdown...",
      "images": [],
      "favicon": "https://example.com/favicon.ico"
    }
  ],
  "failed_results": [],
  "response_time": 0.01
}
```

### Map

Discover URLs from a website without extracting content.

```bash
POST /tavily/map
Content-Type: application/json

{
  "url": "https://example.com",
  "limit": 20
}
```

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| url | string | Yes | Root URL to begin mapping |
| instructions | string | No | Natural language guidance for crawler |
| max_depth | integer | No | Exploration depth (1-5, default 1) |
| max_breadth | integer | No | Links per page level (1-500, default 20) |
| limit | integer | No | Total links to process (default 50) |
| select_paths | array | No | Regex patterns for URL inclusion |
| exclude_paths | array | No | Regex patterns for URL exclusion |
| allow_external | boolean | No | Include external links (default true) |
| timeout | float | No | Max wait time (10-150 seconds) |

**Response:**

```json
{
  "base_url": "https://example.com",
  "results": [
    "https://example.com/about",
    "https://example.com/products",
    "https://example.com/contact"
  ],
  "response_time": 0.1
}
```

### Crawl

Crawl a website and extract content from discovered pages.

```bash
POST /tavily/crawl
Content-Type: application/json

{
  "url": "https://example.com",
  "limit": 10,
  "max_depth": 2
}
```

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| url | string | Yes | Root URL to begin crawl |
| instructions | string | No | Natural language guidance (2x cost) |
| chunks_per_source | integer | No | Max snippets per source (1-5, default 3) |
| max_depth | integer | No | Exploration depth (1-5, default 1) |
| max_breadth | integer | No | Links per page level (1-500, default 20) |
| limit | integer | No | Total links to process (default 50) |
| select_paths | array | No | Regex patterns for URL inclusion |
| exclude_paths | array | No | Regex patterns for URL exclusion |
| allow_external | boolean | No | Include external links (default true) |
| extract_depth | string | No | `basic` or `advanced` (default: basic) |
| format | string | No | `markdown` or `text` (default: markdown) |
| timeout | float | No | Max wait time (10-150 seconds) |

**Response:**

```json
{
  "base_url": "https://example.com",
  "results": [
    {
      "url": "https://example.com/about",
      "raw_content": "# About Us\n\nContent...",
      "favicon": "https://example.com/favicon.ico"
    }
  ],
  "response_time": 0.09
}
```

### Research Tasks

Run async research tasks that gather sources and synthesize findings.

#### Create Research Task

```bash
POST /tavily/research
Content-Type: application/json

{
  "input": "What are the latest developments in AI safety?",
  "model": "mini"
}
```

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| input | string | Yes | Research task or question |
| model | string | No | `mini`, `pro`, or `auto` (default: auto) |
| stream | boolean | No | Stream results via SSE (default: false) |
| output_schema | object | No | JSON Schema for structured output |
| citation_format | string | No | `numbered`, `mla`, `apa`, `chicago` |

**Response:**

```json
{
  "request_id": "582a6eec-9a10-43ba-830f-d9a1aeb19f07",
  "status": "pending",
  "input": "What are the latest developments in AI safety?",
  "model": "mini",
  "created_at": "2026-03-08T11:36:12.674507+00:00",
  "response_time": 0.05
}
```

#### Get Research Task

```bash
GET /tavily/research/{request_id}
```

**Response (completed):**

```json
{
  "request_id": "582a6eec-9a10-43ba-830f-d9a1aeb19f07",
  "status": "completed",
  "content": "## AI Safety Developments\n\nResearch findings...",
  "sources": [
    {
      "title": "Source Title",
      "url": "https://example.com/source",
      "favicon": "https://example.com/favicon.ico"
    }
  ],
  "created_at": "2026-03-08T11:36:12.674507+00:00",
  "response_time": 45
}
```

**Status values:** `pending`, `in_progress`, `completed`, `failed`

## Code Examples

### JavaScript

```javascript
// Search with answer
const response = await fetch('https://gateway.maton.ai/tavily/search', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    query: 'latest AI news',
    max_results: 5,
    include_answer: true
  })
});
const data = await response.json();
```

### Python

```python
import os
import requests

# Search with answer
response = requests.post(
    'https://gateway.maton.ai/tavily/search',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    json={
        'query': 'latest AI news',
        'max_results': 5,
        'include_answer': True
    }
)
data = response.json()
```

## Notes

- Search endpoints return AI-generated answers when `include_answer` is enabled
- Map returns URLs only; Crawl returns URLs with extracted content
- Using `instructions` parameter in crawl/map doubles the credit cost
- Research tasks are async - poll with GET to check status
- Research models: `mini` (fast/efficient), `pro` (comprehensive)
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Tavily connection or invalid request |
| 401 | Invalid or missing Maton API key |
| 429 | Rate limit exceeded |
| 432 | Plan limit exceeded |
| 433 | Pay-as-you-go limit exceeded |
| 4xx/5xx | Passthrough error from Tavily API |

## Resources

- [Tavily API Documentation](https://docs.tavily.com)
- [Search API Reference](https://docs.tavily.com/documentation/api-reference/endpoint/search)
- [Extract API Reference](https://docs.tavily.com/documentation/api-reference/endpoint/extract)
- [Crawl API Reference](https://docs.tavily.com/documentation/api-reference/endpoint/crawl)
- [Research API Reference](https://docs.tavily.com/documentation/api-reference/endpoint/research)
- [Tavily Dashboard](https://app.tavily.com)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
