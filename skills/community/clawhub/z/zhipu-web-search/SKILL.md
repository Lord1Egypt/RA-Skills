---
name: zhipu-web-search
description: |
  Zhipu AI Web Search Tool - Provides flexible search engine capabilities directly via cURL.
  
  Use when:
  - Need to search web information for the latest data
  - Need specific search engines (defaults to Quark, supports Sogou, Zhipu Search)
  - Need to filter search results by time range or domain
  - Need to control result count and detail level
  
  Supported search engines: search_std (basic), search_pro (advanced), search_pro_sogou (Sogou), search_pro_quark (Quark - default)
metadata:
  {
    "openclaw":
      {
        "requires": { "env": ["ZHIPU_API_KEY"], "bins": ["curl"] },
      },
  }
---

# Zhipu Web Search

Web search via Zhipu AI's dedicated API (`/paas/v4/web_search`), refactored to use lightweight `cURL` instead of Python or `jq`. It defaults to using the `search_pro_quark` engine with 20 results.

## Quick Start

### Basic cURL Usage

```bash
curl --request POST \
  --url https://open.bigmodel.cn/api/paas/v4/web_search \
  --header "Authorization: Bearer $ZHIPU_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "search_query": "OpenClaw framework",
    "search_engine": "search_pro_quark",
    "search_intent": false,
    "count": 20
  }'
```

### Script Usage

A wrapper shell script is provided for convenience.

```bash
# Basic Search (defaults to search_pro_quark and 20 results)
bash scripts/zhipu_search.sh --query "AI development trends"

# Advanced Search
bash scripts/zhipu_search.sh \
  --query "latest open source LLMs" \
  --engine "search_pro_sogou" \
  --count 50 \
  --intent \
  --recency "oneWeek"
```

## API Parameter Reference

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `search_query` | string | ✅ | - | Search content, recommended ≤70 chars |
| `search_engine` | enum | ✅ | `search_pro_quark` | `search_std` / `search_pro` / `search_pro_sogou` / `search_pro_quark` |
| `search_intent` | boolean | - | `false` | Enable search intent recognition |
| `count` | integer | - | `20` | Result count, range 1-50 |
| `search_domain_filter` | string | - | - | Whitelist domain filter |
| `search_recency_filter` | enum | - | `noLimit` | `oneDay` / `oneWeek` / `oneMonth` / `oneYear` / `noLimit` |
| `content_size` | enum | - | `medium` | `medium` (summary) / `high` (detailed) |

## Search Engine Selection Guide

| Engine | Use Case |
|--------|----------|
| `search_pro_quark` | Quark search, tailored for specific advanced scenarios (**Default**) |
| `search_std` | Basic search, regular Q&A |
| `search_pro` | Advanced search, need more accurate results |
| `search_pro_sogou` | Sogou search, China domestic content |

## Response Structure

The API returns JSON directly.

```json
{
  "id": "task-id",
  "created": 1704067200,
  "request_id": "request-id",
  "search_intent": [
    {
      "query": "original query",
      "intent": "SEARCH_ALL",
      "keywords": "rewritten keywords"
    }
  ],
  "search_result": [
    {
      "title": "title",
      "content": "content summary",
      "link": "result link",
      "media": "site name",
      "icon": "site icon",
      "refer": "reference number",
      "publish_date": "publish date"
    }
  ]
}
```

## Environment Requirements

- Environment variable `ZHIPU_API_KEY` must be configured.
- `curl` command must be available in your system path.