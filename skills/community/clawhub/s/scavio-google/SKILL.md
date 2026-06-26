---
name: scavio-google
description: Search Google and get structured JSON results (web, news, images, maps). Use for any query requiring current web information or recent news.
version: 2.0.3
tags: google, web-search, search, news-search, image-search, agents, langchain, crewai, autogen, structured-data, json, ai-agents, research, serp
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 90
    throttle: 1
    emoji: "\U0001F50D"
    homepage: https://scavio.dev/docs
---

# Google Search via Scavio

Search Google and return structured JSON — no HTML parsing required. Covers web, news, images, maps, and lens search types.

## When to trigger

Use this skill when the user asks to:
- Look something up on the web or check a current fact
- Find recent news or events
- Search for images, maps, or documentation
- Answer any question that requires real-time or up-to-date information

Do not answer from memory when current information is needed. Search first.

## Setup

Get a free API key at https://scavio.dev (250 free credits/month, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

## Workflow

1. Identify the user's intent and pick the right `search_type` (`classic`, `news`, `images`, `maps`, `lens`).
2. Choose `light_request: false` only if you need knowledge graph, people also ask, or related searches (costs 2 credits vs 1).
3. Call the endpoint with the query and any filters.
4. Return results in a clear, structured response. Cite URLs.

## Endpoint

```
POST https://api.scavio.dev/api/v1/google
Authorization: Bearer $SCAVIO_API_KEY
```

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search query (1-500 chars) |
| `search_type` | string | `classic` | `classic`, `news`, `maps`, `images`, `lens` |
| `country_code` | string | -- | ISO 3166-1 alpha-2 (e.g. `us`, `gb`, `de`) |
| `language` | string | -- | ISO 639-1 code (e.g. `en`, `fr`, `es`) |
| `page` | number | `1` | Result page number |
| `device` | string | `desktop` | `desktop` or `mobile` |
| `nfpr` | boolean | `false` | Set `true` to disable autocorrection |
| `light_request` | boolean | omitted | Omit for 1 credit. Set `false` for full results (2 credits) |

## Example

```python
import os, requests

response = requests.post(
    "https://api.scavio.dev/api/v1/google",
    headers={"Authorization": f"Bearer {os.environ['SCAVIO_API_KEY']}"},
    json={"query": "langchain agents tutorial", "country_code": "us", "language": "en"},
)
data = response.json()
# results in data["results"]
```

## Response

```json
{
  "results": [
    {
      "title": "Result title",
      "url": "https://example.com",
      "description": "Snippet...",
      "position": 1
    }
  ],
  "query": "langchain agents tutorial",
  "credits_used": 1,
  "credits_remaining": 999
}
```

Full mode (`"light_request": false`) also returns: `knowledge_graph`, `questions` (people also ask), `related_searches`, `news_results`, `top_stories`.

## Guardrails

- Never fabricate search results or URLs. Only return what the API gives you.
- If the query is time-sensitive, always call the API — do not answer from training data.
- `search_type: news` only supports `device: desktop`.
- Cite sources when summarizing results.

## Failure handling

- If the API returns an error, report the status code and stop.
- If no results are returned, tell the user and suggest rephrasing.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## LangChain

```bash
pip install langchain-scavio
```

```python
from langchain_scavio import ScavioSearchTool
tool = ScavioSearchTool(engine="google")
```
