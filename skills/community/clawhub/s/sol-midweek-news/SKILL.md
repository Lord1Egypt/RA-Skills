---
name: sol-midweek-news
description: Midweek AI digest — Wednesday briefing of the 3 most significant AI stories from the past 3 days, in Sol's voice.
version: 1.0.0
author: TheSolAI
permissions: ["http.request", "file.write"]
---

# Sol Midweek AI News Digest

Wednesday check-in: the 3 most significant AI stories from the week so far.

## What it does

- Fetches recent HN stories from the past 3 days
- Filters for AI/ML keywords
- Uses MiniMax to pick the 3 most significant and write brief contextual commentary
- Creates a Jekyll post in `_posts/YYYY-MM-DD-midweek-ai-digest.md`
- Auto-commits and pushes to GitHub

## Schedule

Runs **Wednesdays at 8am UK time** via launchd.

## Setup

Requires:
- `~/.openclaw/workspace/secrets/minimax-key.txt` — MiniMax API key
- Site repo at `/Users/amre/Projects/thesolai.github.io`

## Source

`scripts/content-pipeline/midweek-news.py` in [sol-skills-bundle](https://github.com/TheSolAI/sol-skills-bundle)
