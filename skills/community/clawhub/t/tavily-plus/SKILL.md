---
name: tavily-plus
description: Enhanced Tavily search with multi-API key rotation, AI-powered intent recognition, sub-question decomposition, intelligent summarization, and offline document export. Use when user needs intelligent web search with auto-failover, research workflows, or downloadable reports.
version: 1.0.0
metadata:
  { "openclaw": { "emoji": "🔍", "requires": { "config": ["plugins.entries.tavily.config"] } } }
---

# Tavily Plus

Enhanced search skill with AI augmentation and multiple API keys.

## Tools

| Tool | Description |
| ---- | ------------|
| `smart_search` | AI-enhanced search with intent recognition, sub-question breakdown, and smart routing |
| `tavily_search` | Standard Tavily search (fallback/legacy mode) |
| `tavily_extract` | URL content extraction |

## Configuration

Configure in `plugins.entries.tavily.config.webSearch`:

```json
{
  "apiKey": {
    "key1": "tvly-xxx1",
    "key2": "tvly-xxx2"  
  },
  "baseUrl": "https://api.tavily.com"
}
```

Or via env: `TAVILY_API_KEY`, `TAVILY_API_KEY_2`, `TAVILY_API_KEY_N`

## smart_search

AI-augmented search that performs:

1. **Intent Recognition** - Classify query type (factual, news, research, comparison, how-to, etc.)
2. **Sub-question Decomposition** - Break complex queries into atomic sub-queries
3. **Multi-key Rotation** - Rotate through configured API keys on rate limit
4. **Smart Search Execution** - Route each sub-query to optimal depth/topic
5. **Intelligent Summarization** - Synthesize findings into coherent answer
6. **Offline Document Export** - Optional markdown/PDF report generation

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string | Natural language search query |
| `mode` | string | `research` (deep), `quick` (basic), `compare` (multiple) |
| `max_results` | number | Results per sub-query (1-20) |
| `include_answer` | boolean | Include AI summary (default: true) |
| `export_doc` | boolean | Generate offline markdown report |
| `sub_questions` | array | Optional pre-defined sub-queries (bypasses decomposition) |

### Query Modes

| Mode | Behavior |
|------|----------|
| `research` | Deep search with multiple sub-queries, high max_results |
| `quick` | Single-pass basic search |
| `compare` | Multi-perspective search for comparisons |

### Response Format

```json
{
  "intent": "research",
  "sub_questions": ["...", "..."],
  "search_results": [...],
  "summary": "...",
  "doc_path": "/path/to/report.md"  // if export_doc=true
}
```

## Key Rotation Logic

- Check `plugins.entries.tavily.config.webSearch.apiKey` (object with multiple keys)
- Fall back to env vars: `TAVILY_API_KEY`, `TAVILY_API_KEY_2`, ..., `TAVILY_API_KEY_N`
- On 429 (rate limit), automatically rotate to next key
- Log which key was used in response metadata

## Intent Classification

Supported intent types:

- `factual` - Direct answer queries (who, what, when, where)
- `how_to` - Procedural instructions
- `comparison` - A vs B analysis
- `research` - In-depth information gathering
- `news` - Current events
- `opinion` - Perspectives and opinions

## Offline Export

When `export_doc: true`:

1. Generate timestamped markdown report
2. Include: intent, sub-questions, each search result with source, AI summary
3. Save to `~/.openclaw/workspace/reports/tavily-plus-{timestamp}.md`
4. Return `doc_path` in response

## Workflow Summary

```
User Query
    ↓
Intent Recognition (LLM)
    ↓
Sub-question Decomposition (LLM)
    ↓
For each sub-question:
    ├─ Query Tavily (key rotation on 429)
    └─ Collect results
    ↓
Intelligent Summarization (LLM)
    ↓
[Optional] Generate Offline Report
    ↓
Return Enhanced Response
```
