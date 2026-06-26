---
name: turing-tavily-web-search
version: "1.0.0"
description: "Search the web via the Turing Tavily proxy. Use when the user asks to search the web, look up real-time information, research current events, or needs up-to-date data not in training data. Run the bundled script via bash — do NOT construct HTTP requests manually."
homepage: https://docs.turing.cn
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      credentials: "TURING_API_KEY, TURING_CLIENT, TURING_ENVIRONMENT"
---

# Tavily Web Search

Search the web via the Turing Tavily proxy API.

## Usage

```bash
python3 ~/.openclaw/skills/turing-tavily-web-search/scripts.py '<JSON>'
```

## Request Parameters

| Param | Type | Required | Default | Description |
|---|---|---|---|---|
| `query` | `str` or `list[str]` | yes | — | Search query, or list of queries for batch search |
| `max_results` | `int` | no | `10` | Max results per query (1–20) |
| `max_tokens_per_page` | `int` | no | `1024` | Max tokens extracted per result page |
| `search_domain_filter` | `list[str]` | no | — | Restrict results to specific domains (max 20) |

## Response Fields

| Field | Type | Description |
|---|---|---|
| `answer` | `str` | AI-generated summary (if available) |
| `results[].title` | `str` | Page title |
| `results[].url` | `str` | Page URL |
| `results[].content` | `str` | Content snippet |
| `results[].publishedDate` | `str` | Publication date (if available) |

## Examples

```bash
# Basic search
python3 ~/.openclaw/skills/turing-tavily-web-search/scripts.py '{"query": "latest AI news"}'

# Limit results
python3 ~/.openclaw/skills/turing-tavily-web-search/scripts.py '{"query": "latest AI news", "max_results": 5}'

# Domain filter
python3 ~/.openclaw/skills/turing-tavily-web-search/scripts.py '{"query": "transformer architecture", "search_domain_filter": ["arxiv.org", "github.com"]}'
```

## Configuration

Set in `openclaw.json` under `skills.entries.turing-skills.env`:

| Variable | Required | Description |
|---|---|---|
| `TURING_API_KEY` | yes | Bearer token (`sk-...`) |
| `TURING_CLIENT` | yes | Client identifier |
| `TURING_ENVIRONMENT` | yes | Environment name |
| `TURING_API_BASE` | no | API base URL (default: `https://live-turing.cn.llm.tcljd.com`) |
