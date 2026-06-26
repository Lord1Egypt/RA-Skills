---
name: x-prospecting
description: Find and engage potential leads on X (Twitter) by searching for keywords and buying-intent posts via Brave Search.
version: 1.0.0
author: ModelFitAI <skills@modelfitai.com>
license: MIT
keywords: [openclaw, skill, twitter, x, lead-gen, prospecting, brave-search]
requires:
  env: [BRAVE_API_KEY]
---

# X (Twitter) Prospecting Skill

Find potential leads on X by searching for keyword mentions and buying-intent posts. Uses the Brave Search API to query `site:x.com` — no X API credentials required.

## Available Tools

Run with Node.js: `node {baseDir}/x-prospecting.js <command> [args]`

- **search** - Search X posts by keyword via Brave
- **score** - Score a prospect based on their tweet and bio signals
- **thread** - Generate a lead-magnet thread outline
- **dm-sequence** - Generate a DM outreach sequence for a prospect

## Usage

```bash
node {baseDir}/x-prospecting.js search "looking for AI tools"
node {baseDir}/x-prospecting.js score --handle "@username" --bio "founder at SaaS" --tweet "frustrated with my current tool"
node {baseDir}/x-prospecting.js dm-sequence --handle "@username" --name "Jane"
```

## How Brave Search Works for X

```bash
curl -s -H "Accept: application/json" \
     -H "X-Subscription-Token: $BRAVE_API_KEY" \
     "https://api.search.brave.com/res/v1/web/search?q=site:x.com+%22looking+for+AI+tools%22&count=10"
```

Substitute the query with your target keywords. Parse results to extract handles and tweet text, then run through lead scoring.

## Environment Variables

- `BRAVE_API_KEY` - Brave Search API key (free tier: 2,000 queries/month)
