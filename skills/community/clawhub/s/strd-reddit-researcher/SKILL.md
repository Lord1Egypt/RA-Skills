---
name: reddit-researcher
description: Scan Reddit for posts matching keywords and summarize findings. Uses Bing primary + Reddit JSON API fallback — robust against DuckDuckGo bot blocking. Use when researching Reddit communities, finding pain points, or gathering user feedback on a topic.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["curl"] },
        "install": [],
      },
  }
---

# Reddit Researcher

Search Reddit for posts and comments matching your keywords, extract insights and pain points.

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `REDDIT_SUBREDDITS` | No | `all` | Comma-separated list of subreddits (e.g., `technology,programming`) |
| `REDDIT_KEYWORDS` | Yes | — | Comma-separated keywords to search for |
| `REDDIT_SEARCH_ENGINE` | No | `bing` | Search engine: `bing`, `google`, or `reddit` (direct JSON API) |

## Scripts

### scan.sh — Search Reddit

Searches Reddit for posts matching keywords using DuckDuckGo.

```bash
./scripts/scan.sh <keywords>
```

**Output:** List of Reddit post titles with URLs.

### summarize.sh — Extract Pain Points

Fetches Reddit posts and extracts common themes, complaints, and requests.

```bash
./scripts/summarize.sh <post_urls_file>
```

**Output:** Markdown summary with pain points, desires, and patterns.

### export.sh — Export Findings

Exports all research findings to a markdown file with timestamp.

```bash
./scripts/export.sh <summary_file>
```

**Output:** `reddit-research-YYYY-MM-DD.md` in the output directory.

## Usage Example

```bash
export REDDIT_KEYWORDS="AI coding,ChatGPT,developer tools"
export REDDIT_SUBREDDITS="programming,technology,artificial"

# Search for posts
./scripts/scan.sh "$REDDIT_KEYWORDS" > posts.txt

# Summarize findings
./scripts/summarize.sh posts.txt

# Export results
./scripts/export.sh summary.md
```

## Notes

- Uses Bing as primary search engine, with Reddit JSON API and Google as fallbacks — designed to work even when DuckDuckGo blocks automated queries
- Set `REDDIT_SEARCH_ENGINE=reddit` for direct Reddit API access (no search engine needed)
- Respects rate limits; adds delays between requests
- Results cached in `~/.openclaw/workspace/skills/reddit-researcher/cache/`
- Output format is Reddit markdown with proper link formatting
