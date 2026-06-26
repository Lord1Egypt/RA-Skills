---
name: tweet-pipeline
version: 1.0.0
description: Notion-to-Twitter automation — pull approved tweets from a Notion database, schedule one-shot crons for exact post times, and post via X/Twitter OAuth2 API. Use when managing a content calendar in Notion and want automated, precisely-timed tweet posting.
metadata:
  {"openclaw": {"emoji": "🐦", "requires": {"bins": ["python3"], "env": ["NOTION_API_KEY"]}, "primaryEnv": "NOTION_API_KEY", "network": {"outbound": true, "reason": "Reads from Notion API (api.notion.com) for tweet queue. Posts to X/Twitter API (api.x.com) via OAuth2."}}}
---

# Tweet Pipeline

Automate tweet posting from a Notion content calendar. Draft tweets in Notion, set status to "Approved" with a scheduled time, and this pipeline handles the rest.

## Workflow

```
Notion DB (Tweet Pipeline)
  ├── Status: Pending → Agent drafts tweet
  ├── Status: Approved → Heartbeat picks up
  │     ├── Future time → Schedules one-shot cron
  │     └── Past due → Posts immediately
  └── Status: Posted → Done (updated by poster)
```

## Notion DB Schema

| Property | Type | Values |
|---|---|---|
| Title | title | Tweet text |
| Status | select | Pending, Approved, Posted, Failed |
| Scheduled | date | ISO datetime with timezone |
| Platform | select | Twitter, LinkedIn |
| Posted At | date | Filled after posting |

## Usage

```bash
python3 scripts/tweet_poster.py             # Check and schedule
python3 scripts/tweet_poster.py --dry-run   # Preview without scheduling
```

## Key Lessons

- **One-shot crons for exact times** — don't batch-post from heartbeat, schedule each tweet individually
- **X Free tier:** 1,500 tweets/month, 280 char limit, no media upload via API
- **Track scheduled tweets** in a state file to avoid duplicate scheduling

## Files

- `scripts/tweet_poster.py` — Scheduler (reads Notion, creates crons)
- `scripts/tweet_post_one.py` — Poster (called by each cron job)
