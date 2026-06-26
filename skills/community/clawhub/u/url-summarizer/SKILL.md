---
name: url-summarizer
description: Summarize any web page by URL into a concise structured brief. Use when the user asks to summarize, digest, or extract key points from a URL or web page. Also use for batch URL summarization and comparison tasks.
---

# URL Summarizer

Summarize web pages into structured briefs using a deterministic extraction + summarization pipeline.

## Quick Start

```bash
python3 scripts/summarize_url.py <url>
```

## Workflow

1. Receive URL(s) from user
2. Run `scripts/summarize_url.py <url>` to extract and format content
3. Return the structured summary

## Output Format

Each summary includes:
- **Title**: Page title
- **Source**: Original URL
- **Key Points**: 3-5 bullet points
- **Summary**: 2-3 sentence overview

## Batch Usage

For multiple URLs, run the script once per URL and aggregate results into a comparison table when requested.