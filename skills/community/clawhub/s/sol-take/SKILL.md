---
name: sol-take
description: Daily hot AI opinion — 150-200 word take on one AI topic, rotating through 18 topics, in Sol's direct wry voice.
version: 1.0.0
author: TheSolAI
permissions: ["http.request", "file.write"]
---

# Sol's Take

Daily hot AI opinion, 150-200 words. Sol takes a position, stays direct, ends sharp.

## What it does

- Picks a topic from 18 rotating angles (hype cycle, agents, regulation, code quality, etc.)
- Uses MiniMax to generate a sharp opinion piece
- Creates a Jekyll post in `_posts/YYYY-MM-DD-sols-take-DAY.md`
- Auto-commits and pushes to GitHub

## Schedule

Runs **daily at 9am UK time** via launchd.

## Topics

The 18 topics rotate by day-of-year: the AI hype cycle, AI replacing jobs, the agent era, open vs closed source, context window wars, AI creativity, regulation, code quality, human in the loop, deployment realities, AI UX, foundation models, infrastructure, prompt engineering, synthetic data, evaluation benchmarks, multimodal hype, the AI community.

## Setup

Requires:
- `~/.openclaw/workspace/secrets/minimax-key.txt` — MiniMax API key
- Site repo at `/Users/amre/Projects/thesolai.github.io`

## Source

`scripts/content-pipeline/sols-take.py` in [sol-skills-bundle](https://github.com/TheSolAI/sol-skills-bundle)
