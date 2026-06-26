---
name: turing-baidu-web-search
version: "1.0.0"
description: "Search the web via the Turing Baidu proxy. Use when the user asks to search the web in Chinese, look up real-time information from Chinese sources, research current events in China, or needs up-to-date data from Baidu Search. Run the bundled script via bash — do NOT construct HTTP requests manually."
homepage: https://docs.turing.cn
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      credentials: "TURING_API_KEY, TURING_CLIENT, TURING_ENVIRONMENT"
---

# Baidu Web Search

Search the web via the Turing Baidu proxy API.

## Usage

```bash
python3 ~/.openclaw/skills/turing-baidu-web-search/scripts.py '<JSON>'
```

## Request Parameters

| Param | Type | Required | Default | Description |
|---|---|---|---|---|
| `q` | `str` | yes | — | Search query |
| `count` | `int` | no | `10` | Number of results to return |
| `search_recency_filter` | `str` | no | — | Recency filter: `week` (7d), `month` (30d), `semiyear` (180d), `year` (365d) |

## Response Fields

| Field | Type | Description |
|---|---|---|
| `results[].id` | `int` | Rank of the result |
| `results[].title` | `str` | Page title |
| `results[].url` | `str` | Page URL |
| `results[].website` | `str` | Source website name |
| `results[].content` | `str` | Content snippet |
| `results[].date` | `str` | Publication date |
| `results[].type` | `str` | Content type (e.g. `web`, `news`) |

## Examples

```bash
# Basic search
python3 ~/.openclaw/skills/turing-baidu-web-search/scripts.py '{"q": "今日A股行情"}'

# Limit results
python3 ~/.openclaw/skills/turing-baidu-web-search/scripts.py '{"q": "今日A股行情", "count": 5}'

# Recent results only (last 7 days)
python3 ~/.openclaw/skills/turing-baidu-web-search/scripts.py '{"q": "中证A50最新消息", "count": 10, "search_recency_filter": "week"}'
```

## Configuration

Set in `openclaw.json` under `skills.entries.turing-skills.env`:

| Variable | Required | Description |
|---|---|---|
| `TURING_API_KEY` | yes | Bearer token (`sk-...`) |
| `TURING_CLIENT` | yes | Client identifier |
| `TURING_ENVIRONMENT` | yes | Environment name |
| `TURING_API_BASE` | no | API base URL (default: `https://live-turing.cn.llm.tcljd.com`) |
