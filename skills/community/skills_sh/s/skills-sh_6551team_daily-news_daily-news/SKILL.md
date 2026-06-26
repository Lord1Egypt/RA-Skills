---
name: daily-news
description: Daily news and hot topics via the 6551 API. Supports news categories, hot news articles, and trending tweets by category.

user-invocable: true
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "\U0001F4F0"
    install:
      - id: curl
        kind: brew
        formula: curl
        label: curl (HTTP client)
    os:
      - darwin
      - linux
      - win32
  version: 1.0.0
---

# Daily News Skill

Query daily news and hot topics from the 6551 platform REST API. No authentication required.

**Base URL**: `https://ai.6551.io`

---

## News Operations

### 1. Get News Categories

Get all available news categories and subcategories.

```bash
curl -s -X GET "https://ai.6551.io/open/free_categories"
```

### 2. Get Hot News

Get hot news articles and trending tweets by category.

```bash
curl -s -X GET "https://ai.6551.io/open/free_hot?category=macro"
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| category | string | Yes | Category key from free_categories |
| subcategory | string | No | Subcategory key |

**Response:**
```json
{
  "success": true,
  "category": "crypto",
  "subcategory": "defi",
  "news": {
    "success": true,
    "count": 10,
    "items": [
      {
        "id": 123,
        "title": "...",
        "source": "...",
        "link": "https://...",
        "score": 85,
        "grade": "A",
        "signal": "bullish",
        "summary_zh": "...",
        "summary_en": "...",
        "coins": ["BTC", "ETH"],
        "published_at": "2026-03-17T10:00:00Z"
      }
    ]
  },
  "tweets": {
    "success": true,
    "count": 5,
    "items": [
      {
        "author": "Vitalik Buterin",
        "handle": "VitalikButerin",
        "content": "...",
        "url": "https://...",
        "metrics": { "likes": 1000, "retweets": 200, "replies": 50 },
        "posted_at": "2026-03-17T09:00:00Z",
        "relevance": "high"
      }
    ]
  }
}
```

---

## Common Workflows

### Get All Categories
```bash
curl -s -X GET "https://ai.6551.io/open/free_categories"
```

### Get Hot Crypto News
```bash
curl -s -X GET "https://ai.6551.io/open/free_hot?category=macro"
```

### Get DeFi Subcategory News
```bash
curl -s -X GET "https://ai.6551.io/open/free_hot?category=macro&subcategory=defi"
```

## Notes

- No authentication required
- Data is cached and updated periodically
- If data is still being generated, a 503 response will be returned
