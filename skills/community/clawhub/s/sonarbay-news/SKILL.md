---
name: sonarbay-news
description: Search and analyze global news using SonarBay News Intelligence. Provides real-time access to 7 days of worldwide news coverage via CLI or REST API. Use when the user needs news search, trending entities, mention counts over time, or any news-related data analysis.
metadata:
  author: sonarbay
  version: "1.0"
---

# SonarBay News Intelligence

Real-time access to 7 days of global news, updated every 15 minutes. ~100K+ articles from thousands of sources worldwide.

## CLI

The primary way to access SonarBay.

### Install

```bash
# Mac/Linux
curl -fsSL https://sonarbay.com/install.sh | sh

# Windows (PowerShell)
irm https://sonarbay.com/install.ps1 | iex
```

### Search News

```bash
sonarbay search "AI regulation"
sonarbay search "climate change" -n 20 -s newest
sonarbay search "Tesla" --country US --source reuters.com
```

| Flag | Description |
|------|-------------|
| `-n <num>` | Results per page (default: 10) |
| `-p <num>` | Page number (default: 1) |
| `-s <sort>` | `relevance` (default), `newest`, `oldest` |
| `--country <code>` | Filter by country code (e.g. `US`, `IN`, `DE`) |
| `--source <domain>` | Filter by source domain |
| `--json` | Raw JSON output for piping |

### Trending Entities

```bash
sonarbay trending
sonarbay trending -t organizations -w 48h -n 10
```

| Flag | Description |
|------|-------------|
| `-t <type>` | `persons` (default), `organizations`, `countries`, `source` |
| `-w <window>` | Time window: `1h`, `6h`, `12h`, `24h` (default), `48h`, `7d` |
| `-n <num>` | Number of results (default: 20) |

### Time-Series Counts

```bash
sonarbay counts "bitcoin" -i 1h -w 72
```

| Flag | Description |
|------|-------------|
| `-i <interval>` | Bucket size: `15m`, `1h` (default), `6h`, `1d` |
| `-w <hours>` | Lookback window in hours (default: 24) |

### Other Commands

```bash
sonarbay status          # Health check
sonarbay update          # Self-update to latest version
sonarbay --version       # Show version
```

### Pipe-Friendly

Every command supports `--json` for scripting and piping:

```bash
sonarbay search "OpenAI" --json | jq '.results[].title'
sonarbay trending --json | jq '.trending[:5]'
sonarbay counts "inflation" --json | jq '.buckets[] | select(.count > 100)'
```

## Common Patterns

### Monitor a topic over time
1. Run `sonarbay counts "topic" -w 72` to see the trend
2. Identify spikes in the histogram
3. Run `sonarbay search "topic" -s newest` to find what triggered a spike

### Find who's making news
1. Run `sonarbay trending -t persons` or `-t organizations`
2. Search for a specific entity to get articles

### Compare coverage across sources
1. Search the same topic with different `--source` filters
2. Compare result counts and article titles

## REST API (Fallback)

If the CLI is not available, use the REST API directly.

Base URL: `https://sonarbay.com`

| Endpoint | Description |
|----------|-------------|
| `GET /v1/search?q=<query>&per_page=10&sort=relevance` | Search articles |
| `GET /v1/trending?type=persons&hours=24&limit=20` | Trending entities |
| `GET /v1/counts?q=<query>&interval=1h&hours=24` | Time-series counts |
| `GET /v1/article/<id>` | Single article by ID |
| `GET /v1/status` | Health check |

All endpoints return JSON. No authentication required.

## Data Details

- **Coverage**: 7-day rolling window, ~100K+ articles
- **Update frequency**: Every 15 minutes
- **Sources**: Thousands of global news outlets
- **Languages**: Primarily English, with multilingual coverage
- **Fields per article**: title, source, url, date (ISO), countries, location names
- **Country codes**: ISO 2-letter (US, UK, IN, DE, etc.)
