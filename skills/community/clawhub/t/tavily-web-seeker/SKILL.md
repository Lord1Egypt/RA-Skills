---
name: tavily-web-seeker
description: Enhanced Tavily search with intelligent intent recognition, source preferences, critical source validation, and offline report generation.
version: 1.1.0
metadata:
  { "openclaw": { "emoji": "🎯", "requires": { "config": ["plugins.entries.tavily.config"] } } }
---

# tavily-web-seeker

Enhanced web search skill built on Tavily API with intelligent search strategies, user source preferences, and critical source handling.

## Features

1. **Intent Recognition** - Auto-classify queries (factual, news, research, comparison, how-to, academic)
2. **Source Preferences** - Topic-based domain routing (tech→GitHub, news→Reuters, finance→WSJ)
3. **Search Operators** - Support OR, site:, -, exact phrase, time filters
4. **Critical Source Check** - Validate results against preferred sources, return not-found conclusions
5. **Multi-API Key Rotation** - Auto-failover on rate limits (429)
6. **Offline Report** - Markdown export with source coverage analysis

## Tools

| Tool | Description |
|------|-------------|
| `tavily_search` | Standard Tavily search |
| `web_seeker` | Enhanced search with all features |

## Configuration

### API Keys

```json
{
  "apiKey": { "key1": "tvly-xxx1", "key2": "tvly-xxx2" }
}
```

Or env: `TAVILY_API_KEY`, `TAVILY_API_KEY_2`

### Source Preferences

```javascript
// User preferences
const PREFERENCES = {
  default_sites: ["wikipedia.org", "github.com"],
  preferred_topics: {
    tech: ["wikipedia.org", "github.com", "stackoverflow.com"],
    news: ["reuters.com", "apnews.com", "bbc.com"],
    finance: ["wsj.com", "bloomberg.com", "ft.com"],
    academic: ["scholar.google.com", "arxiv.org"]
  },
  critical_sources: {
    "官方": ["gov.cn", "moe.gov.cn"],
    "财经": ["wsj.com", "bloomberg.com"],
    "技术": ["github.com", "stackoverflow.com"]
  }
};
```

## web_seeker Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | string | - | Search query |
| `mode` | string | "quick" | quick/research/compare |
| `max_results` | number | 5 | Results 1-20 |
| `domains` | array | auto | Preferred domains |
| `time_range` | string | auto | day/week/month/year |
| `operators` | string | - | Raw operators |
| `strict_mode` | boolean | false | Require preferred sources only |
| `export_doc` | boolean | false | Generate report |

## Response Format

```json
{
  "original_query": "Iran oil news",
  "intent": "news",
  "domains_used": ["reuters.com", "bbc.com"],
  "search_operator_applied": "site:reuters.com OR site:bbc.com",
  "results_found": true,
  "source_coverage": { "preferred": 3, "total": 10 },
  "results": [...],
  "summary": "..."
}
```

### Not Found Response

```json
{
  "results_found": false,
  "not_found_conclusion": "在指定的核心信源中未搜索到...",
  "suggestions": ["扩展搜索词", "放宽信源限制", "手动访问目标网站"]
}
```

## Usage

```bash
# Basic search
node seeker.js "AI news"

# Research mode with report
node seeker.js "machine learning" --mode research --export

# Strict mode (require preferred sources)
node seeker.js "python tutorial" --strict
```
