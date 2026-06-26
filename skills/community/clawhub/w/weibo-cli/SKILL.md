---
name: weibo-cli
description: |
  Query Weibo (微博) public data via CLI. Use when user asks about:
  - Weibo hot searches / trending topics (微博热搜)
  - Searching Weibo posts, users, or topics
  - Getting user profiles, feeds, followers
  - Reading post details or comments
  No authentication required - uses public mobile web API.
  Chinese social media platform.
---

# Weibo CLI

Query Weibo public data via `weibo` command. No login or API key required.

## Installation

```bash
# Global install
npm install -g @marvae24/weibo-cli

# Or local install (safer)
npm install @marvae24/weibo-cli
npx @marvae24/weibo-cli hot
```

## Authentication

**No authentication required.** The CLI uses Weibo's public mobile web API with auto-generated visitor cookies. All data accessed is publicly available on weibo.com.

Optional: Set `WEIBO_COOKIE` environment variable for higher rate limits (your own login cookie).

## Commands

### Hot Searches

```bash
# Top 50 trending
weibo hot --json

# Limit results
weibo hot --limit 10 --json

# Topic detail (read count, discussion count)
weibo hot "AI" --json
```

### Search

```bash
# Search posts (default)
weibo search "咖啡" --json

# Search users
weibo search "咖啡" --type user --json

# Search topics with stats
weibo search "旅行" --type topic --stats --json

# Types: content, user, topic, realtime, hot, video, image, article
weibo search "猫" --type video --limit 5 --json
```

### User

```bash
# Profile (need UID)
weibo user 123456789 --json

# User feeds
weibo user 123456789 --feeds --json

# Hot feeds (sorted by engagement)
weibo user 123456789 --feeds --hot --json

# Following/followers
weibo user 123456789 --following --json
weibo user 123456789 --followers --json

# Pagination
weibo user 123456789 --feeds --limit 20 --page 2 --json
```

### Post

```bash
# Post detail
weibo post 5000000000000000 --json

# Comments
weibo post 5000000000000000 --comments --json
```

## Output

Always use `--json` for structured output. Parse with jq:

```bash
weibo hot --limit 10 --json | jq '.[] | {keyword: .description, heat: .trending}'
weibo user 123456789 --json | jq '{name: .screen_name, followers: .followers_count}'
weibo search "coffee" --json | jq '.[0] | {text: .text, reposts: .reposts_count}'
```

## Rate Limiting

If you see rate limit errors, wait 1-2 minutes. The CLI auto-retries with exponential backoff.
