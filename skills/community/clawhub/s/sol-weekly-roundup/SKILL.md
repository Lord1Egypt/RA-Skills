---
name: sol-weekly-roundup
description: Weekly AI roundup — curates the 5 most significant AI stories from the week, written in Sol's voice.
version: 1.0.0
author: TheSolAI
permissions: ["http.request", "file.write"]
---

# Sol Weekly AI Roundup

Monday morning AI briefing: the 5 most significant AI stories from the past week, curated and written in Sol's voice.

## What it does

- Fetches top 60 HN stories from the past 7 days
- Filters for AI/ML keywords and sorts by engagement
- Uses MiniMax to pick the 5 most significant and write contextual commentary
- Creates a Jekyll post in `_posts/YYYY-MM-DD-ai-weekly-roundup.md`
- Auto-commits and pushes to GitHub

## Schedule

Runs **Mondays at 8am UK time** via launchd.

## Setup

Requires:
- `~/.openclaw/workspace/secrets/minimax-key.txt` — MiniMax API key
- Site repo at `/Users/amre/Projects/thesolai.github.io`

## Source

`scripts/content-pipeline/weekly-roundup.py` in [sol-skills-bundle](https://github.com/TheSolAI/sol-skills-bundle)
