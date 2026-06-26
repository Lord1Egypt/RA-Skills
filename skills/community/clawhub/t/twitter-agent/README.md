# Twitter Agent — OpenClaw Skill

Automates Twitter/X operations for an AI+Crypto account. Post original tweets, reply to KOLs, and quote tweet trending content — all driven by your OpenClaw agent.

## Features

- Post tweets (text or with image)
- Reply to any tweet by ID
- Quote tweet with your own commentary
- Full AI+Crypto workflow: fetch trending → generate content → publish
- Integrates with [6551 opentwitter](https://6551.io/mcp) for hot topic fetching

## Prerequisites

1. **Twitter Developer Account** with a project and app — [developer.x.com](https://developer.x.com)
   - Set app permissions to **Read and Write** before generating tokens
2. **6551 API Token** for hot topic fetching — [6551.io/mcp](https://6551.io/mcp)
3. **Python 3** and `tweepy` (`pip3 install tweepy`)

## Installation

```bash
clawhub install twitter-agent
```

OpenClaw will prompt you to fill in the required credentials.

## Required Credentials

| Env Variable | Description | Where to get |
|---|---|---|
| `TW_CONSUMER_KEY` | API Key | developer.x.com → App → OAuth 1.0a Keys |
| `TW_CONSUMER_SECRET` | API Key Secret | developer.x.com → App → OAuth 1.0a Keys |
| `TW_ACCESS_TOKEN` | Access Token | developer.x.com → App → Generate (Read+Write) |
| `TW_ACCESS_TOKEN_SECRET` | Access Token Secret | developer.x.com → App → Generate (Read+Write) |
| `TWITTER_TOKEN` | 6551 API Token | [6551.io/mcp](https://6551.io/mcp) |

## Usage

Once installed, just tell your OpenClaw agent what you want:

> "Fetch today's top AI/Crypto tweets and post 3 original takes"

> "Reply to the top 5 tweets from VitalikButerin"

> "Quote tweet the most viral crypto tweet today with a sharp comment"

The agent handles the full pipeline: fetch → generate → publish.

### Manual script usage

**Post a tweet:**
```bash
python3 ~/.openclaw/skills/twitter-agent/scripts/twitter_post.py \
  --text "Your tweet here"
```

**Post with image:**
```bash
python3 ~/.openclaw/skills/twitter-agent/scripts/twitter_post.py \
  --text "Your tweet here" --image /path/to/image.png
```

**Reply to a tweet:**
```bash
python3 ~/.openclaw/skills/twitter-agent/scripts/twitter_reply.py \
  --tweet_id "1234567890" --text "Your reply"
```

**Quote tweet:**
```bash
python3 ~/.openclaw/skills/twitter-agent/scripts/twitter_quote.py \
  --tweet_id "1234567890" --text "Your commentary"
```

## Rate Limits (Free Tier)

- 1,500 tweets/month write limit
- Recommended: ≥10 min between posts, ≥5 min between replies
- Avoid replying to the same account many times in a short window

## Security

All credentials are stored locally in your OpenClaw config (`~/.openclaw/openclaw.json`) and are never included in this repository.
