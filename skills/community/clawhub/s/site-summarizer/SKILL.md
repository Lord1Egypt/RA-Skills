---
name: site-summarizer
description: URL fetcher with summarization. Fetches URLs, extracts content, generates summaries. Optional caching with configurable directory and TTL. Use for web content extraction.
---

# Site Summarizer v4.1.0

## Features

- Content extraction from HTML pages
- Automatic summarization  
- Keyword extraction and language detection
- Optional caching with env vars

## Output

```json
{
  "success": true,
  "content": "...",
  "summary": "...",
  "metadata": {"title": "...", "description": "...", "author": "..."},
  "analysis": {"language": "en", "keywords": [...], "word_count": N, "read_time_min": N},
  "status": 200,
  "from_cache": false
}
```

## Environment Variables

- `SITE_SUMMARIZER_CACHE_DIR` - Cache directory (default: ~/.cache/site-summarizer)
- `SITE_SUMMARIZER_CACHE_TTL` - Cache TTL in seconds (default: 3600)
- `SITE_SUMMARIZER_HIDE_IP` - Set to "true" to hide resolved IP in output

## Usage

```bash
python fetch_and_summarize.py <url>
```

## v4.1.0 Fixes

- Fixed redirect header parsing
- Fixed regex patterns for redaction
- Added optional IP hiding via env var
- Code cleanup and bug fixes