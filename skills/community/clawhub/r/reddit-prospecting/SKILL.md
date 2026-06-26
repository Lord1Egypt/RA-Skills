---
name: reddit-prospecting
description: Find buying-intent leads on Reddit via Brave Search — no Reddit account or OAuth needed. Score posts and generate value-first comments.
version: 1.0.0
author: ModelFitAI <skills@modelfitai.com>
license: MIT
keywords: [openclaw, skill, reddit, lead-gen, prospecting, brave-search, sales]
requires:
  env: [BRAVE_API_KEY]
---

# Reddit Lead Prospecting Skill

Find high-intent leads on Reddit using **Brave Search** (`site:reddit.com`) — no Reddit account, no OAuth, no credentials except a free Brave API key.

## How It Works

Instead of Reddit's OAuth API (which requires app registration and credentials), this skill queries `site:reddit.com` via the Brave Search API. You get real Reddit posts and comments with buying intent — without touching Reddit's API at all.

## Commands

Run with Node.js: `node {baseDir}/reddit-prospecting.js <command> [args]`

- **search `<keyword>`** — Find high-intent Reddit posts via Brave Search
- **score** — Score a Reddit prospect for lead quality
- **comment** — Generate a value-first comment structure for a post

## Usage

```bash
node {baseDir}/reddit-prospecting.js search "looking for AI agent tool"
node {baseDir}/reddit-prospecting.js search "alternative to Zapier" --subreddit startups
node {baseDir}/reddit-prospecting.js score --username u/founder123 --post "frustrated with my current tool"
node {baseDir}/reddit-prospecting.js comment --title "Best AI tools for lead gen?" --subreddit AIMarketing
```

## Environment Variables

- `BRAVE_API_KEY` — Brave Search API key. Free tier: 2,000 queries/month. Sign up at [api.search.brave.com](https://api.search.brave.com)

## What It Does NOT Use

- No Reddit client ID or secret
- No Reddit username or password
- No Reddit OAuth flow
- No direct calls to reddit.com API endpoints