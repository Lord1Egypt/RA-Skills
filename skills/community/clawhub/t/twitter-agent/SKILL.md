---
name: twitter-agent
description: AI+Crypto Twitter automation agent. Post tweets, reply to KOLs, and quote tweet trending content. Integrates with opentwitter/opennews (6551) for hot topic fetching and Claude for content generation.

user-invocable: true
metadata:
  openclaw:
    requires:
      env:
        - TW_CONSUMER_KEY
        - TW_CONSUMER_SECRET
        - TW_ACCESS_TOKEN
        - TW_ACCESS_TOKEN_SECRET
        - TWITTER_TOKEN
      bins:
        - python3
        - pip3
    primaryEnv: TW_CONSUMER_KEY
    emoji: "🐦"
    install:
      - id: tweepy
        kind: pip
        package: tweepy
        label: tweepy (Twitter API client)
    os:
      - darwin
      - linux
  version: 1.0.0
---

# Twitter Agent Skill

**IMPORTANT: Use the exec tool to run all commands below. Do NOT just display them.**

Automates Twitter/X operations for an AI+Crypto account: post original tweets, reply to KOLs, and quote tweet trending content.

## Prerequisites

You need:
1. **Twitter Developer Account** — get API keys at https://developer.x.com
2. **6551 API Token** (`TWITTER_TOKEN`) — get at https://6551.io/mcp (for hot topic fetching)

When installing, OpenClaw will prompt you to fill in each env variable.

### Required env vars

| Variable | Where to get |
|---|---|
| `TW_CONSUMER_KEY` | developer.x.com → Your App → OAuth 1.0a Keys |
| `TW_CONSUMER_SECRET` | developer.x.com → Your App → OAuth 1.0a Keys |
| `TW_ACCESS_TOKEN` | developer.x.com → Your App → Generate (Read+Write) |
| `TW_ACCESS_TOKEN_SECRET` | developer.x.com → Your App → Generate (Read+Write) |
| `TWITTER_TOKEN` | https://6551.io/mcp |

> **Important**: Set your Twitter App permissions to **Read and Write** before generating the Access Token.

---

## Operations

### 1. Post a tweet

```bash
python3 $SKILL_DIR/scripts/twitter_post.py --text "Your tweet text (max 280 chars)"
```

With image:
```bash
python3 $SKILL_DIR/scripts/twitter_post.py --text "Tweet text" --image /path/to/image.png
```

### 2. Reply to a tweet

```bash
python3 $SKILL_DIR/scripts/twitter_reply.py --tweet_id "TWEET_ID" --text "Your reply"
```

### 3. Quote tweet

```bash
python3 $SKILL_DIR/scripts/twitter_quote.py --tweet_id "TWEET_ID" --text "Your comment"
```

---

## Full AI+Crypto workflow

### Step 1 — Fetch trending tweets (via 6551 opentwitter)

```bash
curl -s -X POST "https://ai.6551.io/open/twitter_search" \
  -H "Authorization: Bearer $TWITTER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"keywords": "AI crypto", "minLikes": 500, "product": "Top", "maxResults": 10}'
```

Fetch KOL tweets:
```bash
curl -s -X POST "https://ai.6551.io/open/twitter_user_tweets" \
  -H "Authorization: Bearer $TWITTER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username": "VitalikButerin", "maxResults": 5}'
```

### Step 2 — Generate content (Agent handles this)

Based on trending tweets, generate one of:
- **Original tweet**: Insightful AI/Crypto take, ≤280 chars
- **Reply**: Unique perspective, not robotic, ≤120 chars
- **Quote**: One punchy line that adds value

Guidelines:
- Write in English (target: English-speaking Crypto/AI community)
- Have a real opinion, avoid generic takes
- Max 1–2 emojis

### Step 3 — Publish

Call the appropriate script from Step 1 above.

---

## Output format

All scripts return JSON:
```json
{
  "success": true,
  "tweet_id": "1234567890",
  "url": "https://x.com/username/status/1234567890",
  "text": "Published content"
}
```

---

## Rate limit notes

- Free tier: 1,500 tweets/month write limit
- Recommended intervals: ≥10 min between posts, ≥5 min between replies
- Avoid replying to the same account many times in a short window
