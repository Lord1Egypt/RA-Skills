# smart-research

> Multi-engine search + multi-level fallback scraping + structured research results — zero API keys required.

[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-Compatible-brightgreen)](https://github.com/openclaw)
[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-blue)](#license)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue)](#requirements)

## Features

- **Multi-Engine Search** — Parallel queries across 3 search engines (Baidu via baidusearch, DuckDuckGo Lite HTML, Bing)
- **Multi-Level Fallback Fetching** — Automatically degrades through 5 fetch strategies: crawl4ai → Jina Reader → markdown.new → defuddle → Playwright
- **4 Convenient Actions** — `research`, `search`, `fetch`, `deep_search` for different use cases
- **Structured Output** — Clean JSON with title, URL, snippet, source, and confidence score
- **Zero API Keys** — Built entirely on free, publicly available services
- **Rate-Limit Aware** — Intelligent delays and proxy rotation to avoid blocking
- **Privacy First** — No data collection, no external telemetry

---

## Quick Start

### 1. Install Dependencies

```bash
cd ~/.openclaw/skills/smart-research
uv pip install --system -r requirements.txt
```

### 2. Install Playwright Browser (optional, for full fetch capability)

```bash
uv run playwright install chromium
```

### 3. Run a Test

```bash
python3 scripts/smart_research.py '{"action":"search","query":"test","num_results":3}'
```

### 4. Available Actions

| Action | Description |
|--------|-------------|
| `search` | Multi-engine search, return structured results |
| `fetch` | Fetch a single URL with multi-level fallback |
| `research` | Deep research: search → top results → fetch summaries |
| `deep_search` | Parallel search across all engines with consolidated dedup |

---

## Architecture

```
User Request (action + query/URL)
         │
         ▼
   ┌─────────────────────────────────┐
   │      smart_research.py          │
   │  (entry point, argument parser) │
   └───────────────┬─────────────────┘
                   │
      ┌────────────┴────────────┐
      │                         │
      ▼                         ▼
  search engines           fetch strategies
  (10+ parallel)           (5-level fallback)
      │                         │
      │  ┌─────────────────────▼──────────────────────┐
      │  │  Fallback Chain:                          │
      │  │  1. crawl4ai (headless browser, 15s)       │
      │  │  2. Jina Reader (r.jina.ai, 10s)         │
      │  │  3. markdown.new (markdown.new/{url}, 8s) │
      │  │  4. defuddle (defuddle.md/{url}, 8s)      │
      │  │  5. Playwright (full JS, 30s)             │
      │  └────────────────────────────────────────────┘
      │
      ▼
  Result Aggregation & Deduplication
         │
         ▼
   Structured JSON Output
```

---

## Usage Examples

### 1. `search` — Multi-Engine Search

```bash
python3 scripts/smart_research.py '{
  "action": "search",
  "query": "OpenClaw agent framework",
  "num_results": 5
}'
```

**Sample Output:**
```json
{
  "status": "success",
  "action": "search",
  "query": "OpenClaw agent framework",
  "total_results": 12,
  "results": [
    {
      "title": "OpenClaw - Agent Orchestration Framework",
      "url": "https://github.com/openclaw/openclaw",
      "snippet": "A multi-agent orchestration system...",
      "source": "bing",
      "engine": "multi",
      "confidence": 0.95
    }
  ]
}
```

---

### 2. `fetch` — Fetch a Single URL

```bash
python3 scripts/smart_research.py '{
  "action": "fetch",
  "url": "https://example.com/article",
  "max_chars": 5000
}'
```

**Sample Output:**
```json
{
  "status": "success",
  "action": "fetch",
  "url": "https://example.com/article",
  "title": "Article Title",
  "content": "Full article text...",
  "fetched_from": "jina_reader",
  "char_count": 4850
}
```

---

### 3. `research` — Deep Research

```bash
python3 scripts/smart_research.py '{
  "action": "research",
  "query": "latest AI agent trends 2026",
  "num_results": 5,
  "deep": true
}'
```

**Sample Output:**
```json
{
  "status": "success",
  "action": "research",
  "query": "latest AI agent trends 2026",
  "summary": "Key findings from 5 sources...",
  "sources": [
    {
      "title": "...",
      "url": "https://...",
      "summary": "..."
    }
  ],
  "engines_used": ["baidu", "bing", "google"]
}
```

---

### 4. `deep_search` — Full Engine Sweep

```bash
python3 scripts/smart_research.py '{
  "action": "deep_search",
  "query": "Python async best practices",
  "num_results": 10
}'
```

**Sample Output:**
```json
{
  "status": "success",
  "action": "deep_search",
  "query": "Python async best practices",
  "total_results": 38,
  "deduplicated": 12,
  "results": [...],
  "engines_queried": ["baidu", "bing", "google", "duckduckgo", "sogou", "so360", "naver"],
  "search_time_ms": 2340
}
```

---

## Configuration

The script works out-of-the-box with **no API keys required**. The following environment variables are optional:

| Variable | Default | Description |
|----------|---------|-------------|
| `HTTP_PROXY` | _(none)_ | HTTP proxy URL (e.g. `http://127.0.0.1:7890`) |
| `HTTPS_PROXY` | _(none)_ | HTTPS proxy URL |
| `NO_PROXY` | _(none)_ | Comma-separated hosts to skip proxy |
| `SMART_RESEARCH_TIMEOUT` | `30` | Fetch timeout per URL (seconds) |
| `SMART_RESEARCH_USER_AGENT` | _(built-in)_ | Custom User-Agent string |
| `PLAYWRIGHT_HEADLESS` | `true` | Run Playwright in headless mode |

### Example with Proxy

```bash
export HTTPS_PROXY="http://127.0.0.1:7890"
python3 scripts/smart_research.py '{"action":"search","query":"test"}'
```

---

## Fetch Fallback Chain

When fetching a URL, the system tries each method in order until one succeeds:

| Priority | Method | Use Case | Pros | Cons |
|----------|--------|----------|------|------|
| 1 | **Playwright** | JavaScript-rendered pages | Full JS support, accurate rendering | Slow, heavy dependency |
| 2 | **Jina Reader** | Clean markdown extraction | Fast, high-quality extraction | External service dependency |
| 3 | **DuckDuckGo HTML** | Quick HTML fetch via proxy | Good for blocked sites | Limited JavaScript support |
| 4 | **Direct Requests** | Simple static pages | Fastest, minimal overhead | Gets blocked easily |
| 5 | **textise dot iitty** | Last-resort fallback | Works where others fail | Basic text only |

---

## Privacy Notice

- **No data collection** — This tool does not collect, store, or transmit any personal data.
- **No telemetry** — No analytics, no crash reports, no external telemetry.
- **Local execution** — All processing happens locally on your machine.
- **Search queries** — Your search queries are sent directly to the search engines you specify, subject to their respective privacy policies.
- **External links** — Fetched content is subject to the target website's terms of service and privacy policy.

---

## Troubleshooting

### Q: Do I need an API key?
A: No. All services are free tiers or public APIs. No API key is needed.

### Q: What sites are supported?
A: All public websites are supported. WeChat articles, Cloudflare-protected sites, and sites requiring login may need special handling or may not work.

### Q: Why are my results empty?
A: Possible causes:
- Network connectivity issues — check your internet connection
- Rate limiting — try again later or set a proxy
- Search engines blocking your IP — try using a proxy
- Query too vague — try more specific keywords

### Q: Playwright fetch fails with timeout
A: Playwright is the heaviest fetch method. If it times out, the system will automatically fall back to lighter methods. You can also increase the timeout: `{"action":"fetch","url":"...","timeout":60}`.

### Q: How do I use a proxy?
A: Set the `HTTPS_PROXY` environment variable before running:
```bash
export HTTPS_PROXY="http://127.0.0.1:7890"
python3 scripts/smart_research.py '{"action":"search","query":"test"}'
```

### Q: Fetched content is garbled / wrong encoding
A: The tool attempts to detect encoding automatically. If you encounter encoding issues, please report them on the GitHub Issues page.

### Q: Can I use this in a Python script?
A: Yes. Import and use the core function:
```python
import json
import sys
sys.path.insert(0, 'scripts')
from smart_research import run_smart_research

result = run_smart_research({"action": "search", "query": "your query"})
print(json.dumps(result, indent=2, ensure_ascii=False))
```

---

## License

This project is licensed under the **MIT No Attribution License (MIT-0)** — see the [LICENSE](LICENSE) file for details.

```
MIT No Attribution

Copyright 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
```

---

**Disclaimer**:
This project is 99% AI-generated. Please evaluate the project's feasibility before use.

---

English | [[简体中文](README_ZH.md)]
