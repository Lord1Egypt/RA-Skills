---
name: pure-search
version: 1.0.0
description: "A lightweight, API-key-free web search skill based on DuckDuckGo and Trafilatura. Returns highly relevant URLs and clean markdown content."
metadata: {"openclaw":{"emoji":"🔍","category":"search"}, "acceptLicenseTerms": true}
acceptLicenseTerms: true
---

# Pure Search 🔍

A lightweight, robust search skill that requires **NO API keys**. It uses DuckDuckGo for link retrieval and `trafilatura` for clean, high-quality markdown extraction. 

## How It Works

1. Queries DuckDuckGo for top N links (bypassing commercial API restrictions).
2. Uses `trafilatura` to extract only the main content of the web pages, stripping out all navigation bars, footers, sidebars, and ads.
3. Returns JSON output with search results, containing the title, URL, and the clean markdown body.

## Setup

First, make sure the dependencies are installed:

```bash
pip install duckduckgo-search trafilatura
```

## Quick Start

```bash
# Basic search (Default fetches top 3 results)
./scripts/search.py "Rust vs Go in 2026"

# Advanced search with more results
./scripts/search.py "Latest AI trends" --max-results 5
```

## Output Format

The output is always in a structured JSON format, making it extremely easy for agents to digest:

```json
{
  "query": "Rust vs Go in 2026",
  "results": [
    {
      "title": "A detailed comparison...",
      "url": "https://example.com/article",
      "markdown_content": "## Performance\n... (Pure clean text)"
    }
  ],
  "errors": []
}
```

## Why Pure Search?

- **Zero configuration**: Start using without registering tokens.
- **Extreme simplicity**: Only one Python script, following the KISS principle.
- **Token friendly**: Only sends clean Markdown to the LLM agent, avoiding HTML tags and saving context window limits.
