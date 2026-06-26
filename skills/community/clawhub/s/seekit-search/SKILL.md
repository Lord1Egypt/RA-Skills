---
name: seekit-search
description: Use this skill when an agent needs fresh web results. No API key required. Supports multiple platforms (web, video, social). It explains how to choose a provider, call `seekit` for live network fetches, and consume the json data from search engines.
---

# Seekit Live Search

Use this skill for live web search through `seekit`.

## Install

```bash
pip install seekit
```

## Workflow

Prefer the command line over the Python API — it is simpler and produces structured output directly.

### CLI (preferred)

```bash
seekit <query> --engine <provider> --format json --limit 10
```

Examples:

```bash
seekit "latest OpenAI reasoning model" --engine bing --format json
seekit "python asyncio tutorial" --engine google --format markdown
seekit "cat videos" --engine youtube --format json --limit 5
```

### Python API

```python
import seekit
results = seekit.search(query, provider="bing")
```

Each result is a `SerpItem` with fields: `provider`, `title`, `excerpt`, `url`, optional `author`, optional `cover_url`.

## JSON output example

```json
[
  {
    "provider": "bing",
    "title": "OpenAI announces new reasoning model",
    "excerpt": "OpenAI has released its latest reasoning model...",
    "url": "https://example.com/article",
    "author": "John Doe",
    "cover_url": null,
    "time": "2026-03-15"
  }
]
```

## Choosing a provider

- `bing`, `brave`, `duckduckgo`, `so`, `sogou`, `toutiao` for web
- `youtube`, `bilibili` for video
- `reddit`, `threads`, `weibo` for social

If one provider looks thin or noisy, retry with a second provider instead of overfitting the parser output.

