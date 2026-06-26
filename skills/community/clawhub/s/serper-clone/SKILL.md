---
name: serper-clone
version: 1.0.0
description: "Web search via a self-hosted Serper-compatible API (powered by SearXNG). Free, no rate limits, runs on your own infrastructure. Use for: web searches, news, images, videos, shopping, scholar, patents. Drop-in replacement for the Serper API."
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "files": ["~/.openclaw/workspace/.serper-clone-api-key"] },
      },
  }
---

# Serper Clone Skill

Web search using a self-hosted [Serper-compatible API](https://github.com/paulscode/serper-startos). Uses SearXNG as the search backend with a lightweight bridge that exposes the familiar Serper API format.

## Why Self-Hosted Search?

- **Free & unlimited** — no API quotas, no per-query costs
- **Private** — queries never leave your infrastructure
- **No rate limits** — search as much as you need
- **Drop-in compatible** — same API format as serper.dev

## Setup

### 1. Deploy a Serper Clone Instance

You need a running instance of the Serper Clone API. Options:

- **StartOS (recommended for home servers):** Install from [serper-startos](https://github.com/paulscode/serper-startos)
- **Docker:** See the [serper-startos](https://github.com/paulscode/serper-startos) README for Docker deployment
- **Any SearXNG + bridge setup** that exposes a Serper-compatible API

After deployment, note your:
- **Base URL** (e.g., `https://search.example.com` or `http://192.168.1.50:8080`)
- **API key** (configured during setup)

### 2. Configure the Skill

Create the API key file:

```bash
echo "API_KEY=your-api-key-here" > ~/.openclaw/workspace/.serper-clone-api-key
echo "BASE_URL=https://your-serper-clone-host" >> ~/.openclaw/workspace/.serper-clone-api-key
chmod 600 ~/.openclaw/workspace/.serper-clone-api-key
```

The skill will not activate until this file exists.

## Endpoints

All endpoints accept POST requests with a JSON body.

| Endpoint | Description |
|----------|-------------|
| `/search` | General web search |
| `/news` | News articles |
| `/images` | Image search |
| `/videos` | Video search |
| `/places` | Local places/businesses |
| `/maps` | Maps/location search |
| `/shopping` | Shopping results |
| `/scholar` | Academic papers |
| `/patents` | Patent search |
| `/autocomplete` | Query autocomplete suggestions |

## Usage

### Reading Configuration

```bash
API_KEY=$(grep '^API_KEY=' ~/.openclaw/workspace/.serper-clone-api-key | cut -d'=' -f2)
BASE_URL=$(grep '^BASE_URL=' ~/.openclaw/workspace/.serper-clone-api-key | cut -d'=' -f2)
```

### Web Search

```bash
curl -s -X POST "$BASE_URL/search" \
  -H "X-API-KEY: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "search query", "num": 10}' | jq .
```

### Search Parameters

```json
{
  "q": "search query",          // Required: search terms
  "gl": "us",                   // Country code
  "hl": "en",                   // Language code
  "num": 10,                    // Number of results (1-100)
  "page": 1,                    // Result page number
  "autocorrect": true,          // Enable/disable spell correction
  "location": "Austin, Texas"   // Location hint
}
```

### Response Format

```json
{
  "searchParameters": { "q": "...", "gl": "us", "hl": "en", "num": 10 },
  "organic": [
    {
      "title": "Result Title",
      "link": "https://example.com",
      "snippet": "Description of the result...",
      "position": 1,
      "date": "2026-02-16T00:00:00"
    }
  ],
  "answerBox": { "answer": "...", "snippet": "..." },
  "relatedSearches": [ { "query": "related search" } ],
  "credits": 0
}
```

### News Search

```bash
curl -s -X POST "$BASE_URL/news" \
  -H "X-API-KEY: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "latest AI news", "num": 5}'
```

### Image Search

```bash
curl -s -X POST "$BASE_URL/images" \
  -H "X-API-KEY: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "neural network architecture diagram"}'
```

### Scholarly Articles

```bash
curl -s -X POST "$BASE_URL/scholar" \
  -H "X-API-KEY: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "mixture of experts transformer", "num": 10}'
```

## Helper Function

For convenience in shell scripts:

```bash
serper_search() {
  local endpoint="${1:-search}"
  local query="$2"
  local num="${3:-10}"
  local api_key=$(grep '^API_KEY=' ~/.openclaw/workspace/.serper-clone-api-key | cut -d'=' -f2)
  local base_url=$(grep '^BASE_URL=' ~/.openclaw/workspace/.serper-clone-api-key | cut -d'=' -f2)

  curl -s -X POST "$base_url/$endpoint" \
    -H "X-API-KEY: $api_key" \
    -H "Content-Type: application/json" \
    -d "{\"q\": \"$query\", \"num\": $num}"
}

# Examples:
# serper_search search "OpenClaw agent framework" 10
# serper_search news "AI releases 2026" 5
# serper_search scholar "large language models" 10
```

## Security Notes

- The API key file should be `chmod 600` (owner-read only)
- All requests stay between your OpenClaw instance and your Serper Clone instance
- No data is sent to any third-party service
- The skill only activates when the API key file exists

## Related

- **Serper Clone server:** [github.com/paulscode/serper-startos](https://github.com/paulscode/serper-startos)
- **SearXNG:** [github.com/searxng/searxng](https://github.com/searxng/searxng) — the search backend
