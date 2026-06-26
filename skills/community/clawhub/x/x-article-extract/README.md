# x-article-extract

> OpenClaw Skill: Extract full content from X/Twitter — tweets, X Articles, and external links shared via t.co.

## Problem

When someone shares an X Article (long-form content on X), the tweet text is just a `t.co` short link with zero content. Standard tools like `xreach tweet` only return that bare URL, making the material useless for downstream processing.

## Solution

This skill handles three extraction scenarios with automatic fallback:

| Scenario | Method | Output |
|----------|--------|--------|
| Regular tweet | `xreach tweet` | Tweet text + media + engagement |
| X Article | **Playwright + xreach auth cookie** | Full article body (up to 8000 chars) |
| External link via t.co | **Firecrawl API** | Page markdown content |

All scenarios include engagement metrics (views, likes, retweets, bookmarks, replies).

## Install

```bash
# Via ClawhHub
npx clawhub install x-article-extract

# Or manually
git clone https://github.com/yuxiaoyang2007-prog/x-article-extract.git \
  ~/.openclaw/workspace/skills/x-article-extract
```

## Prerequisites

```bash
# Required
npm install -g xreach-cli    # X/Twitter CLI
xreach auth extract --cookie-source chrome  # Authenticate with your X account

# Required for X Article extraction
pip install playwright
python3 -m playwright install chromium

# Optional (for external page extraction)
export FIRECRAWL_API_KEY=fc-xxxxx

# If behind a firewall (e.g., China)
export HTTPS_PROXY=http://your-proxy:port
```

## Usage

### CLI

```bash
# Extract a single tweet or X Article
python3 scripts/extract.py --url "https://x.com/user/status/123"

# Extract and ingest into content factory
python3 scripts/extract.py --url "https://x.com/user/status/123" --ingest

# Batch extract
python3 scripts/extract.py \
  --url "https://x.com/a/status/111" \
  --url "https://x.com/b/status/222"

# Just resolve a t.co short link
python3 scripts/extract.py --resolve "https://t.co/abc123"

# JSON output
python3 scripts/extract.py --url "https://x.com/user/status/123" --json
```

### As OpenClaw Skill

Once installed, your agent can use it naturally:

> "Extract this X article: https://x.com/user/status/123"

The agent will find and invoke the skill automatically via `knowledge_search`.

## Output Format

```json
{
  "url": "https://x.com/user/status/123",
  "title": "@user: Article title here",
  "author": "Display Name",
  "screen_name": "user",
  "description": "Full article content...",
  "content_type": "x_article",
  "article_url": "https://x.com/i/article/456",
  "engagement": {
    "views": 1298474,
    "likes": 3942,
    "retweets": 366,
    "bookmarks": 13042,
    "replies": 67,
    "quotes": 45
  },
  "word_count": 8130,
  "language": "en",
  "publish_date": "2026-03-17"
}
```

## How It Works

```
Input: x.com/user/status/123
  │
  ├─ xreach tweet → get tweet text
  │
  ├─ Tweet has real content (>30 chars after removing t.co)?
  │   └─ YES → return as regular tweet
  │   └─ NO → detect "thin content", resolve t.co links
  │
  ├─ t.co → x.com/i/article/xxx ?
  │   └─ YES → Playwright + xreach cookie → scrape full article
  │   │         (fallback: xreach thread for discussion context)
  │   └─ NO → external URL → Firecrawl API → page markdown
  │
  └─ Attach engagement metrics (views/likes/bookmarks/etc)
```

## License

MIT
