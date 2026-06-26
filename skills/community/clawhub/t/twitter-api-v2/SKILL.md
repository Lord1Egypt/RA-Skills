---
name: x
version: 1.0.0
description: "Access X (Twitter) via API v2: user profiles, timelines, threads, search, bookmarks, likes, and posting. Use when asked to: (1) get user info or profile, (2) fetch someone's tweets/timeline, (3) extract conversation threads, (4) search for tweets about a topic, (5) retrieve bookmarks, (6) get liked tweets, (7) post tweets, or (8) lookup tweets by ID or URL."
summary: "X (Twitter) API v2 client — profiles, timelines, search, bookmarks, posting."
metadata:
  openclaw:
    emoji: "🐦"
    requires:
      bins: ["python3"]
---

# X (Twitter) API

Interact with X via API v2. Pure Python stdlib — no dependencies.

## Features

**Public data (bearer token):**
- User profiles (bio, followers, tweets count)
- User timelines (with filters: exclude retweets/replies)
- Conversation threads (self-threads by same author)
- Search recent tweets (last 7 days)
- Single/batch tweet lookup
- Tweet metrics (likes, retweets, replies)

**User context (OAuth 2.0):**
- Bookmarks
- Liked tweets
- Post tweets

## Setup

See [SETUP.md](SETUP.md) for credentials setup (bearer token + optional OAuth 2.0).

## Usage

### User Info

```bash
# Get user profile (bio, followers, verification status)
python3 {baseDir}/scripts/x.py user steipete
python3 {baseDir}/scripts/x.py user elonmusk
```

### Timeline

```bash
# Get user's recent tweets
python3 {baseDir}/scripts/x.py timeline steipete --max 50

# Exclude retweets
python3 {baseDir}/scripts/x.py timeline steipete --max 100 --exclude retweets

# Exclude both retweets and replies
python3 {baseDir}/scripts/x.py timeline steipete --max 100 --exclude retweets,replies
```

### Threads

```bash
# Get conversation thread (self-thread by same author)
python3 {baseDir}/scripts/x.py thread https://x.com/steipete/status/123456
python3 {baseDir}/scripts/x.py thread 123456789

# Note: Only searches last 7 days (recent search). For older threads, need full-archive search.
```

### Search

```bash
# Search recent tweets (last 7 days)
python3 {baseDir}/scripts/x.py search "OpenClaw" --max 20
python3 {baseDir}/scripts/x.py search "from:steipete OpenAI" --max 50

# Advanced search operators work (from:, to:, -filter:retweets, etc.)
```

### Tweet Lookup

```bash
# Single tweet
python3 {baseDir}/scripts/x.py tweet 2025504475100614695
python3 {baseDir}/scripts/x.py tweet https://x.com/steipete/status/2025504475100614695

# Multiple tweets (batch)
python3 {baseDir}/scripts/x.py tweets 123456 789012 345678
```

### Bookmarks (OAuth Required)

```bash
# One-time auth setup
python3 {baseDir}/scripts/x.py auth

# Get your bookmarks
python3 {baseDir}/scripts/x.py bookmarks --max 100
```

### Likes (OAuth Required)

```bash
# Get user's liked tweets (requires OAuth)
python3 {baseDir}/scripts/x.py likes steipete --max 50
```

### Posting (OAuth Required)

```bash
# Post a tweet
python3 {baseDir}/scripts/x.py post "Hello from OpenClaw! 🦞"

# Note: 280 character limit enforced by API
```

## Output Format

All commands output clean, readable text:

```
👤 Peter Steinberger 🦞 (@steipete)
   ID: 25401953
   Bio: Polyagentmorous ClawFather...
   👥 382,854 followers · 2,241 following · 135,096 tweets
   https://x.com/steipete

🐦 @VictorKnox99 I think my stance on using AI here is pretty clear.
   📅 2026-02-22 09:34:33
   ❤️  5  🔁 0  💬 0
   https://x.com/steipete/status/2025504475100614695
```

## Common Use Cases

**Research user activity:**
```bash
# Get someone's recent thoughts on a topic
python3 {baseDir}/scripts/x.py timeline steipete --max 100 --exclude retweets | grep -i openai
```

**Monitor discussions:**
```bash
# Search for OpenClaw mentions
python3 {baseDir}/scripts/x.py search "OpenClaw" --max 100
```

**Extract threads:**
```bash
# Get full thread for analysis
python3 {baseDir}/scripts/x.py thread <tweet_url> > thread.txt
```

**Archive bookmarks:**
```bash
# Export bookmarks to file
python3 {baseDir}/scripts/x.py bookmarks --max 100 > bookmarks.txt
```

## Rate Limits

X API enforces rate limits per 15-minute window:

| Endpoint | App-Only (Bearer) | User Context (OAuth) |
|----------|-------------------|----------------------|
| User lookup | 900 | 900 |
| User timeline | ~1,500 | ~900 |
| Search | 450 | 300 |
| Tweet lookup | 900 | 900 |
| Bookmarks | N/A | ~180 |
| Likes | N/A | ~75 |

**Headers in responses:**
- `x-rate-limit-limit` — max requests allowed
- `x-rate-limit-remaining` — requests left in window
- `x-rate-limit-reset` — Unix timestamp when limit resets

**Design tips:**
- Cache results locally (deduplication helps but isn't guaranteed)
- Add delays between requests (avoid hitting limits)
- Use batch endpoints when possible (`tweets` for multiple IDs)

## Billing & Costs

**Pay-per-usage model:**
- Buy credits in Developer Console
- Charged per unique tweet/user returned
- **24-hour deduplication** — same tweet fetched twice in a UTC day = charged once
- Set spending limits to control costs
- Monitor usage: `/2/usage/tweets` endpoint or console

**What's billable:**
- Tweet lookups
- Search results
- Timeline requests
- Bookmarks retrieval

**What's NOT billable:**
- Failed requests (4xx/5xx errors)
- Re-fetching same tweet within 24h UTC window (deduplicated)

See [references/pricing.md](references/pricing.md) for detailed pricing info.

## Search Operators

X API search supports advanced operators:

| Operator | Example | Description |
|----------|---------|-------------|
| `from:` | `from:steipete` | Tweets from user |
| `to:` | `to:steipete` | Replies to user |
| `-` | `-from:steipete` | Exclude user |
| `-filter:` | `-filter:retweets` | Exclude retweets |
| `filter:` | `filter:verified` | Only verified users |
| `lang:` | `lang:en` | Language filter |
| `since:` | `since:2026-02-01` | After date |
| `until:` | `until:2026-02-20` | Before date |

**Example:**
```bash
# OpenClaw tweets from verified users, excluding retweets
python3 {baseDir}/scripts/x.py search "OpenClaw filter:verified -filter:retweets" --max 50
```

## Limitations

**Recent search only:**
- `search` and `thread` commands only cover **last 7 days**
- Full-archive search requires Pro tier ($5,000/mo) or pay-per-usage

**Bookmarks/likes require OAuth:**
- Bearer token alone can't access private user data
- Need OAuth 2.0 user context (one-time setup)

**No Watch Later equivalent:**
- X API doesn't expose "Watch Later" or similar lists
- Use bookmarks as alternative

**Rate limits still apply:**
- Pay-per-usage removes monthly caps but rate limits per 15-min window remain
- Design for retries with exponential backoff

## Troubleshooting

**403 Forbidden:**
- Check credentials file exists and has valid bearer_token
- Ensure endpoint doesn't require OAuth (bookmarks, likes, posting need OAuth)

**429 Too Many Requests:**
- Hit rate limit — wait until `x-rate-limit-reset` time
- Reduce `--max` values
- Add delays between requests

**No results found:**
- Recent search only covers 7 days — thread/search may miss older content
- User may have no tweets or privacy settings blocking access

**Authentication errors (OAuth):**
- Ensure `oauth2.json` has correct client_id/client_secret
- Re-run `x.py auth` to refresh tokens
- Check scopes in Developer Portal match required scopes

## Notes

- **Pure stdlib** — no pip dependencies, uses urllib + json
- **Works offline** — caches nothing, always fetches fresh data
- **Thread-safe** — stateless CLI, safe for parallel invocations
- **Deduplication** — X API deduplicates within 24h UTC day (soft guarantee)
- **Output encoding** — UTF-8, handles emoji and international characters
