---
name: search
description: "Search the web using Tavily's Search API. Returns relevant, accurate results with content snippets, scores, and metadata. Use when the user asks to search the web, look up sources, find links, or research a topic."
homepage: https://docs.tavily.com/documentation
metadata: {"openclaw": {"homepage": "https://docs.tavily.com/documentation", "primaryEnv": "TAVILY_API_KEY", "requires": {"bins": ["curl"], "env": ["TAVILY_API_KEY"]}}}
---

# Search Skill

Search the web and get relevant results optimized for LLM consumption.

## Requirements

Set your API key as an environment variable:

```bash
export TAVILY_API_KEY=tvly-...
```

Get an API key at [tavily.com](https://tavily.com).

## Quick Start

The script accepts a single `--json` argument — the raw Tavily API request body. The JSON maps 1:1 to the [Tavily Search API](https://docs.tavily.com/documentation/api-reference/endpoint/search).

```bash
./scripts/search.sh --json '{"query": "python async patterns"}'
```

**Examples:**

```bash
# Quick lookup
./scripts/search.sh --json '{"query": "OpenAI latest funding round"}'

# More results
./scripts/search.sh --json '{"query": "Stripe documentation", "max_results": 10}'

# Recent news only
./scripts/search.sh --json '{"query": "Landscape of electric vehicles 2026", "time_range": "week", "max_results": 10}'

# Scoped to specific sources
./scripts/search.sh --json '{"query": "NVIDIA stock analysis", "search_depth": "advanced"}'
```

### Equivalent curl

The script is a thin wrapper around this call:

```bash
curl --request POST \
  --url https://api.tavily.com/search \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "query": "latest developments in quantum computing",
    "max_results": 5
  }'
```

## API Reference

### Endpoint

```
POST https://api.tavily.com/search
```

### Headers

| Header | Value |
|--------|-------|
| `Authorization` | `Bearer <TAVILY_API_KEY>` |
| `Content-Type` | `application/json` |

### Request Body

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `query` | string | Required | Search query (keep under 400 chars) |
| `max_results` | integer | 10 | Maximum results (0-20) |
| `search_depth` | string | `"basic"` | `basic`, `advanced` |
| `time_range` | string | null | `day`, `week`, `month`, `year` |
| `start_date` | string | null | Return results after this date (`YYYY-MM-DD`) |
| `end_date` | string | null | Return results before this date (`YYYY-MM-DD`) |
| `include_domains` | array | [] | Domains to include |
| `exclude_domains` | array | [] | Domains to exclude |
| `country` | string | null | Boost results from a specific country (general topic only) |
| `include_raw_content` | boolean | false | Include full page content |
| `include_images` | boolean | false | Include image results |
| `include_image_descriptions` | boolean | false | Include descriptions for images |
| `include_favicon` | boolean | false | Include favicon URL for each result |

### Response Format

```json
{
  "query": "latest developments in quantum computing",
  "results": [
    {
      "title": "Page Title",
      "url": "https://example.com/page",
      "content": "Extracted text snippet...",
      "score": 0.85
    }
  ],
  "response_time": 1.2
}
```

## Search Depth

| Depth | Latency | Relevance | Content Type |
|-------|---------|-----------|--------------|
| `basic` | Medium | High | NLP summary |
| `advanced` | Higher | Highest | Chunks |

**When to use each:**
- `basic`: General-purpose, balanced
- `advanced`: Precision matters (default recommendation)

## Data Handling
**Never include in the JSON body:**
- Secrets, API keys, or credentials
- Personal or sensitive user data


## Tips

- **Keep queries under 400 characters** - Think search query, not prompt
- **Break complex queries into sub-queries** - Better results than one massive query
- **Use `include_domains`** to focus on trusted sources
- **Use `time_range`** for recent information
