---
name: tavily-search
description: "Web search and data retrieval via Tavily API. Use when you need to search the web, get news, find answers, or look up sources. Supports 5 modes: search (general), news (fresh headlines), qna (Q&A), images, and context. Returns structured results with title, URL, snippet, and optional AI answer summary."
---

# Tavily Search — Enhanced Edition

Tavily is a search API optimized for AI applications — returns structured results with relevance scores and optional AI-generated summaries.

## Quick Start

```bash
# Standard search (default, 5 results, ~brave format)
python3 {baseDir}/scripts/tavily_search.py --query "..." --format md

# Include AI short answer
python3 {baseDir}/scripts/tavily_search.py --query "..." --include-answer

# Advanced search (higher quality, slower)
python3 {baseDir}/scripts/tavily_search.py --query "..." --search-depth advanced
```

## Output Formats

| Format | Description | Best For |
|--------|-------------|----------|
| `--format md` | Human-readable Markdown | Direct user display |
| `--format brave` | title/url/snippet JSON | Structured processing (default) |
| `--format raw` | Full JSON with all fields | Debugging / advanced use |

## Modes

### `--mode search` (default)
General web search. Good for research, finding links, fact-checking.
```
python3 {baseDir}/scripts/tavily_search.py --query "OpenAI GPT-5 release" --mode search
```

### `--mode news`
Fresh news headlines (past N days). Good for current events, breaking news.
```
python3 {baseDir}/scripts/tavily_search.py --query "US Iran war" --mode news --days 7
```

### `--mode qna`
Direct Q&A — asks Tavily to answer a specific question from web sources.
```
python3 {baseDir}/scripts/tavily_search.py --query "What happened at Nvidia GTC 2026?" --mode qna
```

### `--mode images`
Image search results.
```
python3 {baseDir}/scripts/tavily_search.py --query "Tesla Cybertruck" --mode images
```

### `--mode context`
Research-oriented — includes related topics, better for deep dives.
```
python3 {baseDir}/scripts/tavily_search.py --query "Claude AI agent architecture" --mode context
```

## Common Options

| Flag | Default | Description |
|------|---------|-------------|
| `--max-results N` | 5 | Number of results (max 10) |
| `--include-answer` | off | Add AI-generated short answer |
| `--search-depth` | basic | `basic` (fast) or `advanced` (better quality) |
| `--days N` | 3 | Freshness for news mode (1-7) |
| `--domains` | none | Restrict to domain(s), e.g. `--domains reuters.com bbc.com` |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `TAVILY_API_KEY` | API key (from tavily.io) |
| `TAVILY_SEARCH_DEPTH` | Default: `basic` or `advanced` |

## Examples

```
# Quick fact-check
python3 {baseDir}/scripts/tavily_search.py --query "Charlie Kirk death September 2025" --include-answer

# Latest news on a topic
python3 {baseDir}/scripts/tavily_search.py --query "AI agents March 2026" --mode news --days 7 --format md

# Deep research with related topics
python3 {baseDir}/scripts/tavily_search.py --query "Claude Opus 4.6 capabilities" --mode context --search-depth advanced

# Domain-restricted search
python3 {baseDir}/scripts/tavily_search.py --query "China EV market 2026" --domains reuters.com bloomberg.com
```

## Notes

- Keep `--max-results` small (3–5) by default to reduce token/reading load
- Prefer `--format md` when displaying results directly to users
- Use `--include-answer` for quick summaries without reading all results
- Dev plan: 1000 searches/month. Pro plan: unlimited.
