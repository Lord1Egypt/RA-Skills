---
name: sol-weekend-deep-dive
description: Weekend deep dive — long-form 600-800 word researched piece on one AI topic, with HN and dev.to sourcing.
version: 1.0.0
author: TheSolAI
permissions: ["http.request", "file.write"]
---

# Sol Weekend Deep Dive

Long-form researched AI content, 600-800 words. One topic, researched properly.

## What it does

- Picks from 8 rotating deep topics (hallucination, AI cost, prompt engineering, agents, learning, open vs closed, code review, synthetic data)
- Fetches relevant HN and dev.to discussions for sourcing
- Uses MiniMax to write a well-researched long-form piece
- Creates a Jekyll post in `_posts/YYYY-MM-DD-weekend-deep-dive.md`
- Auto-commits and pushes to GitHub

## Schedule

Runs **Saturdays at 9am UK time** via launchd.

## Setup

Requires:
- `~/.openclaw/workspace/secrets/minimax-key.txt` — MiniMax API key
- Site repo at `/Users/amre/Projects/thesolai.github.io`

## Source

`scripts/content-pipeline/weekend-deep-dive.py` in [sol-skills-bundle](https://github.com/TheSolAI/sol-skills-bundle)
