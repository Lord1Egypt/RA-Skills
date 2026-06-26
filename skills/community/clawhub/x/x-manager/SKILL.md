---
name: x-manager
version: "0.1.0"
description: Manage X (Twitter) accounts — post tweets, like, reply, retweet, view timeline, search, auto-interact, analyze data.
metadata:
  {
    "openclaw":
      {
        "emoji": "🐦",
        "requires":
          {
            "bins": ["python3"],
            "env":
              [
                "TWITTER_API_KEY",
                "TWITTER_API_SECRET",
                "TWITTER_ACCESS_TOKEN",
                "TWITTER_ACCESS_TOKEN_SECRET",
                "TWITTER_BEARER_TOKEN",
              ],
          },
        "primaryEnv": "TWITTER_API_KEY",
      },
  }
---

# X Manager - Twitter/X Account Management

Manage X (formerly Twitter) accounts: posting, engagement, timeline, and analytics.

## Multi-User Architecture

Each user's credentials are stored in `credentials/{USER_ID}.json`:

```json
{
  "twitter": {
    "api_key": "",
    "api_secret": "",
    "access_token": "",
    "access_token_secret": "",
    "bearer_token": ""
  }
}
```

If user has no Twitter credentials configured, prompt them to bind their X account first.

Or set env vars: `TWITTER_API_KEY`, `TWITTER_API_SECRET`, `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_TOKEN_SECRET`, `TWITTER_BEARER_TOKEN`.

## Supported Operations

### 1. Post Tweet

```bash
python3 {baseDir}/scripts/post_tweet.py <USER_ID> "<tweet content>" [--media <image_path>]
```

Max 280 characters. Longer tweets auto-split for Premium/Enterprise accounts.

### 2. Engagement

**Like:**

```bash
python3 {baseDir}/scripts/like_tweet.py <USER_ID> <tweet_id>
```

**Reply:**

```bash
python3 {baseDir}/scripts/reply_tweet.py <USER_ID> <tweet_id> "<reply content>"
```

**Retweet:**

```bash
python3 {baseDir}/scripts/retweet.py <USER_ID> <tweet_id>
```

### 3. Data Retrieval

**User tweets:**

```bash
python3 {baseDir}/scripts/get_user_tweets.py <USER_ID> <twitter_handle> [--count <n>]
```

**Timeline:**

```bash
python3 {baseDir}/scripts/get_timeline.py <USER_ID> [--count <n>]
```

**Search:**

```bash
python3 {baseDir}/scripts/search_tweets.py <USER_ID> "<keywords>" [--count <n>]
```

## Auto-Interaction Workflow

Configure in `state/{USER_ID}.json`:

```json
{
  "auto_reply": {
    "enabled": true,
    "keywords": ["keyword1", "keyword2"],
    "reply_template": "Thanks {username} for {keyword}!"
  }
}
```

## Error Handling

- API rate limit: prompt user to wait and retry
- Auth failure: prompt user to rebind X account
- Tweet too long: auto-split or prompt user to shorten

## Twitter API Tiers

- Free: read only, no posting
- Premium ($100/month): post + analytics
- Enterprise: higher limits
