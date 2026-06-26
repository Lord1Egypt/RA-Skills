---
name: web2md
description: Convert any URL to clean, readable Markdown. Use when the user wants to save a web article as Markdown, extract clean content from a webpage, batch-convert URLs to Markdown files, or add AI summaries to web articles. Triggers on requests like "convert this to markdown", "save this article", "extract content from URL", "web to md", or when processing web reading lists.
---

# Web to Markdown

Extract clean article content from any URL and convert it to readable Markdown.

## Quick Start

```bash
web2md https://example.com/article
web2md https://example.com/article -o article.md
web2md https://example.com/article --summary
```

## Installation

```bash
pip install web2md
```

## Common Patterns

### Save an article the user shared

```bash
web2md <url> -o ~/Documents/reading/<slug>.md
```

### Extract with AI summary (needs Ollama running)

```bash
web2md <url> --summary --ai -o article.md
```

### Batch convert a reading list

```bash
web2md urls.txt --batch -d output/
```

## How It Works

web2md uses `readability-lxml` to extract the main article content (stripping ads, nav, sidebars) and `markdownify` to convert the HTML to clean Markdown. It preserves headings, links, lists, and text formatting while removing clutter.

## What It's Good For

- Saving articles for offline reading
- Extracting content for LLM context
- Archiving blog posts and news articles
- Building a personal knowledge base from web content
- Research: batch-convert sources to Markdown

## Limits (Free Tier)

- Single URL at a time
- No image download
- No AI summarization (heuristic fallback only)

For batch mode, image download, and AI features: <https://web2md.dev> (paid CLI, $19)
