---
name: track-upvotes
description: Track Product Hunt launch upvotes, comments, and daily ranking in real-time — get Telegram alerts when you move up the leaderboard.
version: 1.0.0
author: ModelFitAI <skills@modelfitai.com>
license: MIT
keywords: [openclaw, skill, product-hunt, launch, tracking, upvotes, growth]
requires: {}
---

# Product Hunt Launch Tracker

Monitor your Product Hunt launch in real-time — upvotes, rank, comments, and hourly trends. No API key needed.

## Commands

Run with Node.js: `node {baseDir}/track-upvotes.js <command> [args]`

- **check `<url>`** — Get current upvotes, rank, and comments
- **trend `<url>`** — Get current stats + trend vs last check

## Usage

```bash
node {baseDir}/track-upvotes.js check https://www.producthunt.com/posts/your-product
node {baseDir}/track-upvotes.js trend https://www.producthunt.com/posts/your-product
```

## No API Key Required

Reads the public Product Hunt page directly. Nothing to configure — just pass your product URL.