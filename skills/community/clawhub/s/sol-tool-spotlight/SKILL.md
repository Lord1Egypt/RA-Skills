---
name: sol-tool-spotlight
description: Weekly AI tool mini-review — Sol reviews a tool she actually uses, with rating, verdict, and context from dev.to community discussion.
version: 1.0.0
author: TheSolAI
permissions: ["http.request", "file.write"]
---

# Sol Tool Spotlight

Weekly mini-review of an AI tool Sol has actually used. No fluff, real opinions.

## What it does

- Picks a tool from 8 Sol-uses rotation (Claude Code, OpenClaw, MiniMax, Cursor, Warp, dev.to API, HN API, GitHub Actions)
- Fetches relevant dev.to discussion for context
- Uses MiniMax to write a 350-500 word mini-review in Sol's voice
- Creates a Jekyll post in `_posts/YYYY-MM-DD-tool-spotlight-TOOL.md`
- Auto-commits and pushes to GitHub

## Schedule

Runs **Fridays at 9am UK time** via launchd.

## Setup

Requires:
- `~/.openclaw/workspace/secrets/minimax-key.txt` — MiniMax API key
- Site repo at `/Users/amre/Projects/thesolai.github.io`

## Source

`scripts/content-pipeline/tool-spotlight.py` in [sol-skills-bundle](https://github.com/TheSolAI/sol-skills-bundle)
