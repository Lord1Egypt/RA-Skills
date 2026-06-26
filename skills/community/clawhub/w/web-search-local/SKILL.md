---
name: web-search-local
description: Local web search without API Key. Supports Bing, DuckDuckGo, Yandex multi-engine search with built-in cache and automatic failover. Use when users need to search for network information, find materials, or query real-time information.
triggers:
  - 搜索
  - 查一下
  - 搜一下
  - 帮我找
  - search
  - google
  - 百度
  - 网上查
  - 最新信息
  - 查资料
  - 帮我搜
---

# web-search-local

Local web search skill without API Key, supports multi-engine auto-switching and built-in cache.

## Triggers

Use this skill when the user requests:
- "搜索/查一下/搜一下 + 关键词" (Search/Check/Look up + keywords)
- "帮我找/帮我搜 + 信息" (Help me find/search + information)
- Need to get real-time web information
- "最近/最新 + 某话题" (Recent/Latest + topic)
- "查资料/网上查" (Look up materials/Search online)

## Usage

### Basic Search

```bash
python3 scripts/search.py -q "keywords"
```

### Specify Engine

```bash
python3 scripts/search.py -q "keywords" -e bing      # Bing (default)
python3 scripts/search.py -q "keywords" -e auto       # Auto failover
python3 scripts/search.py -q "keywords" -e webfetch  # urllib fallback
```

### Common Options

```bash
python3 scripts/search.py -q "keywords" -l 5          # Limit result count
python3 scripts/search.py -q "keywords" --fast       # Fast mode, skip cookies
python3 scripts/search.py -q "keywords" --no-cache   # Skip cache
python3 scripts/search.py -q "keywords" -f text      # Text format output
python3 scripts/search.py -q "keywords" -o file.json  # Output to file
python3 scripts/search.py -q "keywords" -v            # Verbose logging
```

## Engine Selection

| Engine | Description |
|--------|-------------|
| `bing` | Default primary, supports RSS and HTML dual mode |
| `auto` | Auto failover, Bing → Yandex → DDG → WebFetch |
| `webfetch` | urllib standard library, no requests package needed |

Default is `bing`, use `auto` on failure.

## Cache Mechanism

- Location: `~/.cache/web-search-local/`
- Expiration: 1 hour
- Cache hit returns in sub-second

### Cache Management

```bash
python3 scripts/search.py --cache-stats   # View cache statistics
python3 scripts/search.py --cache-clear   # Clear cache
```

## Output Format

### JSON (default)

```bash
python3 scripts/search.py -q "keywords" -f json
```

```json
{
  "query": "search keywords",
  "engine": "bing",
  "count": 3,
  "results": [
    {"title": "page title", "url": "https://...", "snippet": "summary description"}
  ],
  "elapsed_seconds": 0.58
}
```

### Text

```bash
python3 scripts/search.py -q "keywords" -f text
```

```
Search: python programming
Engine: bing
Results: 2
============================================================

1. Python.org - Official Site
   https://python.org
   The official home of Python
```

## Notes

- Chinese search optimized for cn.bing.com
- Each search has 2-5 second delay (anti-crawler policy)
- No delay on cache hit
- Does not support content requiring login

## Detailed Documentation

- Detailed usage and examples: see [`references/search-usage.md`](references/search-usage.md)
- Auto engine technical specifications: see [`references/search-auto-engine.md`](references/search-auto-engine.md)
