---
name: scavio-reddit
description: Search Reddit posts or fetch a full post with threaded comments by URL. Use for discussion research, brand monitoring, sentiment analysis, or RAG pipelines needing community context.
version: 1.0.3
tags: reddit, social, forum, discussion, community, sentiment, brand-monitoring, agents, langchain, crewai, autogen, structured-data, json, ai-agents, rag, research
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 90
    throttle: 1
    emoji: "\U0001F4AC"
    homepage: https://scavio.dev/docs/reddit-api
---

# Reddit Search and Post Retrieval via Scavio

Search Reddit posts or retrieve a full post with its threaded comment tree. Returns structured JSON with subreddit, author, score, flair, awards, and media fields.

## When to trigger

Use this skill when the user asks to:
- Search Reddit for opinions, discussions, or community sentiment on a topic
- Fetch the full text and comments of a Reddit post by URL
- Research how developers or communities talk about a product, library, or issue
- Build RAG pipelines that need community-sourced context
- Monitor brand or competitor mentions across Reddit

Note: Reddit requests take 5-15 seconds. Set a client timeout of at least 30 seconds.

## Setup

Get a free API key at https://scavio.dev (250 free credits/month, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

## Workflow

1. **Finding discussions:** call `/reddit/search` with a keyword query. Use `sort: top` for the most upvoted posts or `sort: new` for freshest results.
2. **Reading a post:** if the user provides a Reddit URL, call `/reddit/post` to get the full body and comment tree.
3. **Pagination:** pass `nextCursor` from the search response back as `cursor` to get the next page. Stop when `nextCursor` is `null`.
4. **Comment tree:** comments are returned flat in traversal order. Use `depth` for indentation or `parentId` to reconstruct the tree. Top-level replies have `parentId` equal to the post id (`t3_…`); nested replies have `parentId` equal to a comment id (`t1_…`).

## Endpoints

| Endpoint | Credits | Description |
|---|---|---|
| `POST https://api.scavio.dev/api/v1/reddit/search` | 2 | Search Reddit posts by query, sort, and cursor |
| `POST https://api.scavio.dev/api/v1/reddit/post` | 2 | Get a full post with threaded comments by URL |

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Search Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search query (1-500 chars) |
| `sort` | string | `relevance` | `relevance`, `hot`, `top`, `new`, `comments` |
| `cursor` | string | -- | Pagination token from previous response's `nextCursor` |

## Post Detail Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string | required | Full Reddit post URL |

## Examples

```python
import os, requests

BASE = "https://api.scavio.dev"
HEADERS = {"Authorization": f"Bearer {os.environ['SCAVIO_API_KEY']}"}

# Search Reddit
results = requests.post(f"{BASE}/api/v1/reddit/search", headers=HEADERS,
    json={"query": "FastAPI vs Django 2026", "sort": "top"}).json()

posts = results["data"]["posts"]
next_cursor = results["data"]["nextCursor"]  # pass as "cursor" for next page

# Fetch full post and comments
post_data = requests.post(f"{BASE}/api/v1/reddit/post", headers=HEADERS,
    json={"url": "https://www.reddit.com/r/Python/comments/1smb9du/fastapi_vs_django/"}).json()

post = post_data["data"]["post"]
comments = post_data["data"]["comments"]  # flat list, use depth/parentId for tree
```

## Search Response

```json
{
  "data": {
    "searchQuery": "FastAPI vs Django 2026",
    "totalResults": 14,
    "nextCursor": "eyJjYW5kaWRhdGVzX3JldH...",
    "posts": [
      {
        "position": 0,
        "id": "t3_1smb9du",
        "title": "FastAPI vs Django in 2026 -- what the teams are actually using",
        "url": "https://www.reddit.com/r/Python/comments/1smb9du/fastapi_vs_django/",
        "subreddit": "Python",
        "author": "python_dev",
        "timestamp": "2026-04-15T16:34:40.389000+0000",
        "nsfw": false
      }
    ]
  },
  "credits_used": 2,
  "credits_remaining": 498
}
```

## Post Detail Response

```json
{
  "data": {
    "post": {
      "id": "t3_1smb9du",
      "title": "FastAPI vs Django in 2026 -- what the teams are actually using",
      "body": "After a year of running both in production...",
      "url": "https://www.reddit.com/r/Python/comments/1smb9du/fastapi_vs_django/",
      "contentUrl": "https://www.reddit.com/r/Python/comments/1smb9du/fastapi_vs_django/",
      "subreddit": "Python",
      "author": "python_dev",
      "score": 842,
      "upvoteRatio": 0.97,
      "numComments": 214,
      "timestamp": "2026-04-15T16:34:40.389000+0000",
      "flair": "Discussion",
      "nsfw": false,
      "awards": []
    },
    "comments": [
      {
        "id": "t1_lxs9a0k",
        "author": "senior_py",
        "body": "We moved to FastAPI for the API surface and kept Django for admin...",
        "score": 312,
        "depth": 0,
        "timestamp": "2026-04-15T17:02:11.000000+0000",
        "parentId": "t3_1smb9du"
      }
    ]
  },
  "credits_used": 2,
  "credits_remaining": 496
}
```

`url` is the canonical Reddit permalink. `contentUrl` is the rendered URL — for link posts it will be the external article; for text/self posts it is the same as `url`; for image/video posts it is the media URL.

## Guardrails

- Each Reddit call costs 2 credits (not 1). Inform the user if they are paginating many results.
- Never fabricate post titles, authors, scores, or comment content. Only return API data.
- Requests take 5-15 seconds. If the user's UX is time-sensitive, recommend async or streaming patterns.
- Do not filter out NSFW posts silently — surface the `nsfw` flag so the user can decide.
- When summarizing comment threads, preserve the author attribution.

## Failure handling

- `504` means Reddit timed out. Retry once with the same request.
- `502` / `503` mean upstream is temporarily unavailable. Wait a few seconds before retrying.
- If search returns no results, suggest different keywords or a different `sort` value.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## LangChain

```bash
pip install langchain-scavio
```

```python
from langchain_scavio import ScavioSearchTool
tool = ScavioSearchTool(engine="reddit")
```
