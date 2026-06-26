---
name: rss-aggregator
description: Parse, aggregate and process RSS/Atom feeds. Use when user wants to track multiple RSS feeds, create personalized news digest, monitor blog updates, or build newsletter content from various sources.
---

# RSS Aggregator

Parse, aggregate and process RSS/Atom feeds for content aggregation and monitoring.

## Quick Start

```bash
python scripts/aggregator.py --feeds feeds.txt --output items.json
```

## Core Features

- **Multi-feed Aggregation**: Combine multiple RSS/Atom sources
- **Content Parsing**: Extract title, link, description, pubDate
- **Filtering**: Filter by keyword, date, category
- **Output Formats**: JSON, HTML, Markdown
- **Scheduling**: Integrate with cron for periodic updates

## Usage

```bash
python scripts/aggregator.py [OPTIONS]

Options:
  --feeds FILE       File with feed URLs (one per line)
  --url URL          Single feed URL (can repeat)
  --output FILE      Output file (JSON)
  --format FORMAT   Output format: json, html, markdown
  --limit N          Maximum items to return
  --keyword TEXT     Filter by keyword in title/description
  --since DATE       Only items after this date (ISO format)
```

## Examples

```bash
# Aggregate multiple feeds
python scripts/aggregator.py --feeds my-feeds.txt --output news.json

# Single feed with keyword filter
python scripts/aggregator.py --url "https://example.com/feed.xml" --keyword "AI" --limit 10

# Generate HTML newsletter
python scripts/aggregator.py --feeds feeds.txt --format html --output newsletter.html

# Filter recent items
python scripts/aggregator.py --feeds feeds.txt --since "2026-01-01" --output recent.json
```

## Feed File Format

```
# Lines starting with # are comments
# Blank lines are ignored

# Tech news
https://news.ycombinator.com/rss
https://www.reddit.com/r/programming/.rss

# Blogs
https://example.com/blog/feed.xml
```

## Integration

### Telegram Notification
```bash
python scripts/aggregator.py --feeds feeds.txt --output /tmp/items.json
telegram-send "Found $(jq '. | length' /tmp/items.json) new items"
```

### Daily Newsletter
```bash
# Run daily at 8 AM
0 8 * * * python /path/to/aggregator.py --feeds feeds.txt --format markdown --output /tmp/digest.md && telegram-send --file /tmp/digest.md
```

## Use Cases

- Personal news aggregator
- Competitive intelligence monitoring
- Content curation for newsletters
- Industry trend tracking
- Blog update notifications
