---
name: xfyun-search
description: Search the web using iFlytek ONE SEARCH API (万搜/聚合搜索). Returns titles, summaries, URLs, and full text from web pages. Good for Chinese-language web search.
---

# xfyun-search

Search the web using iFlytek ONE SEARCH API (万搜/聚合搜索). Returns titles, summaries, URLs, and full text content from web pages.

## When to Use

- User asks to search the Chinese web or needs Chinese-language search results
- Need an alternative to Brave Search (especially for Chinese content)
- User explicitly requests iFlytek / 讯飞 / 万搜 search

## Prerequisites

- **Python 3** (standard library only, no pip install needed)
- **Environment variable**: `XFYUN_API_PASSWORD` — API password from [讯飞控制台](https://console.xfyun.cn/services/cbm)

## Usage

The script is at `scripts/search.py` relative to this skill directory.

### Basic Search

```bash
python3 scripts/search.py "搜索关键词"
```

### Options

| Flag | Description |
|------|-------------|
| `--limit N` | Max results, 1–20 (default 10) |
| `--no-rerank` | Disable result reranking |
| `--no-fulltext` | Disable full text retrieval |
| `--raw` | Output raw JSON instead of formatted text |

### Examples

```bash
# Simple search
python3 scripts/search.py "美国现任总统是谁"

# Limit to 5 results
python3 scripts/search.py "Python asyncio 教程" --limit 5

# Raw JSON output for programmatic use
python3 scripts/search.py "量子计算最新进展" --raw

# Minimal mode — no rerank, no full text
python3 scripts/search.py "天气预报" --no-rerank --no-fulltext
```

### Output Format (default)

```
Query: 美国现任总统是谁

## 1. Page Title
URL: https://example.com/page
Summary: Brief description of the page content

## 2. Another Result
URL: https://example.com/other
Summary: Another brief description
```

### Output Format (--raw)

Returns the full API JSON response including `data.search_results.documents[].content` (full page text).

## API Details

- **Endpoint**: `POST https://search-api-open.cn-huabei-1.xf-yun.com/v2/search`
- **Auth**: `Authorization: Bearer <XFYUN_API_PASSWORD>`
- **Rate limits**: Per-app daily and per-second limits apply (see error codes below)

### Error Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 11200 | Authorization error or quota exceeded |
| 11201 | Daily rate limit exceeded |
| 11202 | Per-second rate limit exceeded |
| 11203 | Concurrent connection limit exceeded |
| 21001 | Missing parameters |
| 21009 | Unauthorized appId |

## Tips

- Use complete questions (e.g. "美国现任总统是谁？") rather than keywords for better time-sensitive results
- Query length should be ≤512 characters
