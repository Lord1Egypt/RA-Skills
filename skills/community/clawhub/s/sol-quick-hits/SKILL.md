---
name: sol-quick-hits
description: Weekday AI briefing — fetches top AI stories from Hacker News and dev.to, generates a 3-item curated briefing post in Sol's voice.
version: 1.0.0
author: TheSolAI
permissions: ["http.request", "file.write"]
---

# Sol Quick Hits

Daily weekday AI briefing: 3 curated stories from Hacker News and dev.to, written in Sol's voice.

## What it does

- Fetches top 30 HN stories, filters for AI keywords
- Fetches top 10 AI-tagged dev.to articles
- Uses MiniMax to pick the 3 most interesting and write a punchy briefing
- Creates a Jekyll post in `_posts/YYYY-MM-DD-quick-hits-DAY.md`
- Auto-commits and pushes to GitHub

## Schedule

Runs **weekdays at 8am UK time** via launchd.

## Setup

Requires:
- `~/.openclaw/workspace/secrets/minimax-key.txt` — MiniMax API key
- Site repo at `/Users/amre/Projects/thesolai.github.io`
- Pipeline at `/Users/amre/Projects/sol-skills-bundle/scripts/content-pipeline/`

## Source

`scripts/content-pipeline/quick-hits.py` in [sol-skills-bundle](https://github.com/TheSolAI/sol-skills-bundle)
