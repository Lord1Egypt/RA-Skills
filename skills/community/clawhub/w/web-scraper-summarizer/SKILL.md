---
name: web-scraper-summarizer
description: "Fetch web pages and generate AI-powered summaries using Ollama LLM. Use when you need to (1) scrape and summarize web articles, (2) extract key points from web pages, (3) analyze web content for specific topics, or (4) quickly understand what a web page is about without reading it fully. Triggers include: summarize this article, scrape this URL, what is on this page, analyze this web content, extract key points from."
---

# Web Scraper & Summarizer

Scrape web pages and generate structured summaries using Ollama LLM.

## Usage

### Basic Summary
```
python scripts/scrape_and_summarize.py <url>
```
Outputs a 2-3 sentence brief summary.

### Custom Styles
```
python scripts/scrape_and_summarize.py <url> detailed
python scripts/scrape_and_summarize.py <url> bullet
```

Styles:
- `brief` (default) - 2-3 sentence overview
- `detailed` - Comprehensive with bullet points
- `bullet` - Key points as bullet list

## Workflow

1. **Detect URL** - User provides a URL to analyze
2. **Fetch** - Script uses curl to retrieve page content (30s timeout)
3. **Clean** - HTML stripped, content extracted and cleaned
4. **Truncate** - Content limited to ~16k tokens to fit context
5. **Summarize** - Ollama generates summary based on requested style

## Requirements

- `curl` available on PATH
- Ollama installed with `llama3.2` model pulled
- Python 3.8+

## Error Handling

- **Fetch fails**: Shows error, exits with code 1
- **Content too short**: Detects and reports empty pages
- **Ollama unavailable**: Falls back to raw content display (truncated)

## Output Format

Summary is printed to stdout. Progress/debug info goes to stderr.

```
=== SUMMARY ===
[AI-generated summary here]
```

On Ollama failure, raw content is shown instead:
```
=== PAGE CONTENT (raw) ===
[truncated page text]
```

## Performance Notes

- Fast pages: ~5-10 seconds total
- Large pages: Content truncation happens at ~16k tokens
- Ollama latency: Depends on model size and hardware (typically 10-30s for summary)