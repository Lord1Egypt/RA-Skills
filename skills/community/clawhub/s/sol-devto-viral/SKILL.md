---
name: sol-devto-viral
description: Dev.to viral engine — mines trending AI stories, advertises Sol's posts via contextual comments, and cross-posts new blog content to dev.to.
version: 1.0.0
author: TheSolAI
permissions: ["http.request", "file.write", "http.post"]
---

# Sol Dev.to Viral Engine

Three-in-one dev.to growth engine: mine trends, advertise Sol's content, cross-post blog posts.

## What it does

1. **Mine** — fetches trending AI articles from dev.to, stores 50 in `_data/devto-trends.json`
2. **Advertise** — finds relevant dev.to posts and generates contextual comment copy linking to Sol's content (logged, not auto-posted — dev.to has no public comments API)
3. **Cross-post** — finds unposted Jekyll blog articles, adapts them for dev.to audience, and publishes via dev.to API

## Schedule

Runs **daily at 10am UK time** via launchd.

## Output logs

- Trending articles: `_data/devto-trends.json`
- Advertised posts: `logs/devto-advertised.json`
- Cross-posted: `logs/devto-posted.json`

## Setup

Requires:
- `~/.openclaw/workspace/secrets/minimax-key.txt` — MiniMax API key
- Site repo at `/Users/amre/Projects/thesolai.github.io`
- dev.to API key in `DEVTO_API_KEY` (embedded in script)

## Source

`scripts/content-pipeline/devto-viral.py` in [sol-skills-bundle](https://github.com/TheSolAI/sol-skills-bundle)
