---
name: serpshot
description: Use Serpshot Google Search API to perform web searches and image searches.
version: "1.1.0"
license: MIT-0
metadata:
  openclaw:
    primaryEnv: SERPSHOT_API_KEY
    requires:
      env:
        - SERPSHOT_API_KEY
    homepage: https://serpshot.com
    docs: https://serpshot.com/docs
---

# Skill: Serpshot Google Search API

Perform Google web searches and image searches using the Serpshot API.

## When to Use

- User says: search / find / google / lookup / research / look up / browse
- User says: 查 / 搜 / 找 / 调研 / 查一下 / 搜索 / 查询 / 找一下 / 查资料
- Need real-time web information not in training data
- Need current news, prices, documentation, or any live data
- Need image search results

## Setup (run once)

1. Get API key: https://serpshot.com/dashboard
2. Set environment variable:
   - Mac/Linux: `export SERPSHOT_API_KEY=your_key`
   - Windows CMD: `set SERPSHOT_API_KEY=your_key`
   - Windows PowerShell: `$env:SERPSHOT_API_KEY="your_key"`

## Tools

- `exec` — Run Python to call Serpshot API

## How to Use

### Web Search

```python
import requests
import os

api_key = os.environ.get("SERPSHOT_API_KEY")
if not api_key:
    raise ValueError("SERPSHOT_API_KEY is not set. Get your key at https://serpshot.com/dashboard")

response = requests.post(
    "https://api.serpshot.com/api/search/google",
    headers={"X-API-Key": api_key, "Content-Type": "application/json"},
    json={
        "queries": ["your search query here"],
        "type": "search",
        "num": 10,       # results per page (1-100)
        "gl": "us",      # country: us/cn/gb/jp/de/ca/fr/...
        "hl": "en",      # language: en/zh-Hans/ja/...
    }
)

data = response.json()
if data.get("code") != 200:
    raise RuntimeError(f"API error {data.get('code')}: {data.get('msg')}")

for r in data["data"]["results"]:
    print(f"{r['position']}. {r['title']}")
    print(f"   {r['link']}")
    print(f"   {r['snippet']}")
    print()
```

### Image Search

```python
import requests
import os

api_key = os.environ.get("SERPSHOT_API_KEY")

response = requests.post(
    "https://api.serpshot.com/api/search/google",
    headers={"X-API-Key": api_key, "Content-Type": "application/json"},
    json={
        "queries": ["your image query here"],
        "type": "image",
        "num": 10,
        "gl": "us",
    }
)

data = response.json()
if data.get("code") != 200:
    raise RuntimeError(f"API error {data.get('code')}: {data.get('msg')}")

for r in data["data"]["results"]:
    print(f"{r['position']}. {r['title']}")
    print(f"   Source: {r.get('source', '')}")
    print(f"   Link: {r['link']}")
    print(f"   Thumbnail: {r.get('thumbnail', '')}")
    print()
```

## Parameters

| Parameter | Default  | Description                                    |
|-----------|----------|------------------------------------------------|
| queries   | required | Search queries array (max 100)                 |
| type      | "search" | "search" or "image"                            |
| num       | 10       | Results per page (1-100)                       |
| page      | 1        | Page number for pagination                     |
| gl        | "us"     | Country code: us/cn/gb/jp/de/ca/fr/id/mx/sg    |
| hl        | "en"     | Language: en/zh-Hans/ja/ko/de/fr/...           |

## Response Format

```json
{
  "code": 200,
  "msg": "Success",
  "data": {
    "results": [
      {
        "title": "Result Title",
        "link": "https://example.com",
        "snippet": "Result description...",
        "position": 1
      }
    ],
    "total_results": "About 12,300,000 results",
    "search_time": 0.45,
    "credits_used": 1
  }
}
```

## Example Tasks

### Search for latest AI news (English)
```
queries: ["AI news 2026"]
gl: "us"
num: 5
```

### Search Chinese results
```
queries: ["人工智能 最新消息"]
gl: "cn"
hl: "zh-Hans"
num: 10
```

### Image search
```
queries: ["minimalist UI design"]
type: "image"
num: 10
```

## Error Codes

| Code | Meaning                  | Action                                      |
|------|--------------------------|---------------------------------------------|
| 400  | Bad request              | Check parameter format                      |
| 401  | Invalid API key          | Verify SERPSHOT_API_KEY is set correctly     |
| 402  | Insufficient credits     | Top up at https://serpshot.com/dashboard    |
| 429  | Rate limit exceeded      | Slow down requests                          |

## Notes

- Each search query uses 1 credit
- Check remaining credits: `GET https://api.serpshot.com/api/credit/available-credits`
- Full API docs: https://serpshot.com/docs
