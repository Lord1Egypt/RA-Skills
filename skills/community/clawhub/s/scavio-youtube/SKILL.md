---
name: scavio-youtube
description: Search YouTube and retrieve video metadata. Use for finding videos, checking view counts, channel info, or AI training suitability.
version: 2.1.3
tags: youtube, video-search, metadata, agents, langchain, crewai, autogen, structured-data, json, ai-agents, content-research
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 90
    throttle: 1
    emoji: "\u25B6"
    homepage: https://scavio.dev/docs
---

# YouTube Search and Metadata via Scavio

Search YouTube and retrieve video metadata. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find YouTube videos on a topic
- Check view counts, upload date, or video metadata
- Verify if a video is suitable for AI training or has captions available

## Setup

Get a free API key at https://scavio.dev (250 free credits/month, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

## Workflow

1. **Finding a video:** call `/search` with the topic. Use `sort_by: view_count` for the most-watched result.
2. **Checking metadata:** call `/metadata` for view counts, likes, tags, or channel info.
3. **Trainability:** call `/trainability` to check license and caption availability before ingesting.

## Endpoints

| Endpoint | Description |
|---|---|
| `POST https://api.scavio.dev/api/v1/youtube/search` | Search YouTube videos |
| `POST https://api.scavio.dev/api/v1/youtube/metadata` | Get structured video metadata |
| `POST https://api.scavio.dev/api/v1/youtube/trainability` | Check AI training suitability |

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Search Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `search` | string | required | Search query — note: this field is `search`, not `query` |
| `upload_date` | string | -- | `last_hour`, `today`, `this_week`, `this_month`, `this_year` |
| `type` | string | -- | `video`, `channel`, or `playlist` |
| `duration` | string | -- | `short` (< 4 min), `medium` (4-20 min), `long` (> 20 min) |
| `sort_by` | string | `relevance` | `relevance`, `date`, `view_count`, `rating` |
| `subtitles` | boolean | `false` | Videos with captions only |
| `creative_commons` | boolean | `false` | Creative Commons videos only |

## Examples

```python
import os, requests

BASE = "https://api.scavio.dev"
HEADERS = {"Authorization": f"Bearer {os.environ['SCAVIO_API_KEY']}"}

# Search — use "search" field, not "query"
results = requests.post(f"{BASE}/api/v1/youtube/search", headers=HEADERS,
    json={"search": "langchain tutorial", "type": "video", "sort_by": "view_count"}).json()

video_id = results["data"][0]["videoId"]

# Metadata
metadata = requests.post(f"{BASE}/api/v1/youtube/metadata", headers=HEADERS,
    json={"video_id": video_id}).json()
```

## Search Response

```json
{
  "data": [
    {
      "videoId": "sVcwVQRHIc8",
      "title": "Learn RAG From Scratch - Python AI Tutorial",
      "channel": "freeCodeCamp.org",
      "publishedAt": "2024-04-17",
      "duration": "2:33:11",
      "viewCount": 1258310,
      "thumbnail": "https://i.ytimg.com/vi/sVcwVQRHIc8/hq720.jpg"
    }
  ],
  "credits_used": 1
}
```

Metadata response: `title`, `view_count`, `like_count`, `comment_count`, `categories`, `tags`, `channel_id`, `upload_date`, `thumbnails`.

Trainability response: `has_transcript`, `transcript_languages`, `license`, `is_trainable`.

## Guardrails

- The search parameter is `search`, not `query` — this is different from other Scavio endpoints.
- Never fabricate video IDs, view counts, or metadata.

## Failure handling

- If search returns no results, suggest different keywords or relaxing filters.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## LangChain

```bash
pip install langchain-scavio
```

```python
from langchain_scavio import ScavioSearchTool
tool = ScavioSearchTool(engine="youtube")
```
