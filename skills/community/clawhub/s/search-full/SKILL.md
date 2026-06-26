---
name: search-full
description: "Search the web with SearXNG, then fetch the full page with Crawl4AI and answer from the page正文."
---

# Search full-page workflow

Use this skill when a search result summary is not enough and you need the actual page contents.

## Workflow

1. Search with SearXNG.
2. Open the best result with Crawl4AI.
3. Read the Markdown正文, not just the snippet.
4. If the page cannot be opened, report the failure clearly and do not invent content.

## Local command

Use the fixed command:

```bash
ocsearch "your query"
```

## What it already does

- Uses `SEARXNG_URL`, defaulting to `http://localhost:8080`
- Searches the web
- Crawls the top result with Crawl4AI
- Prints extracted Markdown正文

## Best for

- Official docs
- Pricing pages
- API references
- Version notes
- Pages where snippets are too short
