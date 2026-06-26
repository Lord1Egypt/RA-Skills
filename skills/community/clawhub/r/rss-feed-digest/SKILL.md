---
name: rss-digest
description: Fetch, filter, and summarize RSS/Atom feeds into a clean daily or weekly digest. Supports multiple feeds, keyword filtering, deduplication, and outputs Markdown or plain text summaries.
author: zacjiang
version: 1.0.0
tags: rss, atom, feed, news, digest, summary, newsletter, monitoring, automation
---

# RSS Feed Digest

Aggregate multiple RSS/Atom feeds into a clean, summarized digest. Perfect for automated newsletters, news monitoring, or daily briefings.

## Usage

### Fetch and display recent items
```bash
python3 {baseDir}/scripts/rss_digest.py fetch \
  --feeds "https://hnrss.org/frontpage" "https://feeds.arstechnica.com/arstechnica/technology-lab" \
  --hours 24 \
  --limit 20
```

### Filter by keywords
```bash
python3 {baseDir}/scripts/rss_digest.py fetch \
  --feeds "https://hnrss.org/frontpage" \
  --keywords "AI,LLM,agent,OpenClaw" \
  --hours 48
```

### Output as Markdown file
```bash
python3 {baseDir}/scripts/rss_digest.py fetch \
  --feeds "https://hnrss.org/frontpage" \
  --output digest.md \
  --format markdown
```

### Use a feed list file
```bash
# Create feeds.txt with one URL per line
python3 {baseDir}/scripts/rss_digest.py fetch \
  --feed-file feeds.txt \
  --hours 24
```

## Features

- 📰 Supports RSS 2.0 and Atom feeds
- 🔍 Keyword filtering (include/exclude)
- 🔄 Deduplication across multiple feeds
- 📅 Time-based filtering (last N hours)
- 📝 Markdown or plain text output
- 📋 Feed list file support for managing many sources

## Dependencies

```bash
pip3 install feedparser
```

## Example: Daily AI News Digest

```bash
# feeds.txt
https://hnrss.org/frontpage
https://feeds.arstechnica.com/arstechnica/technology-lab
https://www.artificialintelligence-news.com/feed/
https://openai.com/blog/rss.xml

# Run daily via cron
python3 rss_digest.py fetch --feed-file feeds.txt --keywords "AI,LLM,GPT,Claude,agent" --hours 24 --output /tmp/daily-ai-digest.md
```

## Use Cases

- **Daily briefings**: Summarize industry news for your team
- **Newsletter automation**: Generate content for Beehiiv/Substack newsletters
- **Competitive monitoring**: Track mentions of competitors or keywords
- **Research**: Aggregate academic/industry feeds on a topic
- **Heartbeat integration**: Run during OpenClaw heartbeat to check for relevant news
