---
name: smart-research
description: 多引擎搜索 + 多级降级抓取 + 结构化研究结果。零API Key，一键完成搜索+抓取+融合。
homepage: https://github.com/xx235300/smart-research
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins: ["python3", "uv"]
      env: []
---

## smart-research

Universal research skill — multi-engine search + multi-layer fallback fetching + structured results.

## Features

- 🔍 **Multi-Engine Search**: Baidu, DuckDuckGo, Bing with automatic fallback
- 🔄 **Multi-Layer Fallback Fetching**: crawl4ai → Jina → markdown.new → defuddle → Playwright
- 📊 **Structured Output**: title / body / href / source_type / fetch_method / fetched_at
- 🚀 **Zero API Key**: All services are free
- 📦 **One-Click Research**: Single `research()` action for search + fetch + fusion

## Architecture

```
┌─────────────────────────────────────────────┐
│           smart-research 统一入口            │
└─────────────────────────────────────────────┘
                     │
   ┌─────────────────┼─────────────────┐
   ▼                 ▼                 ▼
┌────────┐      ┌────────┐       ┌────────┐
│ Search │      │ Fetch  │       │ Fusion │
│ Layer  │      │ Layer  │       │ Layer  │
└────────┘      └────────┘       └────────┘
```

## Usage

### Python API

```python
result = main({
    "action": "research",
    "query": "Python tutorial",
    "num_results": 5,
    "crawl_depth": 3
})
```

### Search Only

```python
result = main({
    "action": "search",
    "query": "machine learning latest research",
    "num_results": 5
})
```

### Fetch Only

```python
result = main({
    "action": "fetch",
    "url": "https://example.com/article"
})
```

### Deep Search

```python
result = main({
    "action": "deep_search",
    "query": "AI agent trends 2024",
    "num_results": 5
})
```

## Input Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `action` | string | Yes | - | Operation type: `research`, `search`, `fetch`, `deep_search` |
| `query` | string | Conditional | - | Search query (required for `research`/`search`/`deep_search`) |
| `url` | string | Conditional | - | Target URL (required for `fetch`) |
| `num_results` | int | No | 5 | Number of search results (1-20) |
| `crawl_depth` | int | No | 3 | Number of top results to fetch details (1-10) |

## Output Format

### Research Result

```json
{
  "success": true,
  "query": "Python tutorial",
  "search_results": [
    {
      "title": "Result title",
      "href": "https://example.com",
      "body": "Snippet content",
      "score": 85.5,
      "source_type": "baidu",
      "fetch_method": "crawl4ai",
      "fetched_at": "2024-01-01T12:00:00Z"
    }
  ],
  "message": "Research completed"
}
```

### Fetch Result

```json
{
  "success": true,
  "url": "https://example.com",
  "content": "# Article Title\n\nClean markdown content...",
  "source": "jina",
  "fetched_at": "2024-01-01T12:00:00Z"
}
```

## Execution

```yaml
type: script
script_path: scripts/smart_research.py
entry_point: main
dependencies:
  - uv>=0.1.0
  - requests>=2.28.0
  - baidusearch>=1.0.3
  - crawl4ai>=0.8.0
  - playwright>=1.40.0
```

## Fetch Fallback Chain

Each URL automatically tries:

| Priority | Service | Timeout | Description |
|----------|---------|---------|-------------|
| 1 | crawl4ai | 15s | AI-powered, local |
| 2 | Jina Reader | 10s | Free, no key needed |
| 3 | markdown.new | 8s | Simple pages |
| 4 | defuddle | 8s | Better noise reduction |
| 5 | Playwright | 30s | Dynamic rendering |

## Privacy Notice

- Public web pages: Fully supported
- Private/internal URLs: Not supported by default
- Sensitive content: Requires user consent

## Error Handling

- Returns `{"success": false, "message": "..."}` on errors
- Automatically falls back to next service
- Partial results returned if some fetches fail
