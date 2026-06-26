---
name: x-api
description: Post tweets, threads, replies, and quote-tweets to X (Twitter) via API v2 with OAuth 1.0a.
version: 1.0.0
author: ModelFitAI <skills@modelfitai.com>
license: MIT
keywords: [openclaw, skill, twitter, x, social-media, posting, oauth]
requires:
  env: [X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET]
---

# X (Twitter) API Skill

## CRITICAL: Read This First

You control the X (Twitter) account **using the script at `/root/.openclaw/skills/x-api/x-api.js`**.

There is NO `twitter` command, NO Python, NO pip in this container. Do NOT search for other tools. Do NOT try to use curl with OAuth headers. Do NOT try to install anything.

**The ONLY way to post tweets is:**

```bash
node /root/.openclaw/skills/x-api/x-api.js post "Your tweet text here"
```

This script handles ALL OAuth 1.0a signing automatically using your configured API keys. Just run it.

## Commands

**Post a tweet:**
```bash
node /root/.openclaw/skills/x-api/x-api.js post "Hello world! This is my first tweet."
```

**Post a thread (multiple connected tweets):**
```bash
node /root/.openclaw/skills/x-api/x-api.js thread "First tweet of thread" "Second tweet continues..." "Third tweet wraps up"
```

**Reply to a tweet:**
```bash
node /root/.openclaw/skills/x-api/x-api.js reply 1234567890 "This is my reply"
```

**Quote-tweet:**
```bash
node /root/.openclaw/skills/x-api/x-api.js quote 1234567890 "Interesting take!"
```

**Like a tweet:**
```bash
node /root/.openclaw/skills/x-api/x-api.js like 1234567890
```

**Delete a tweet:**
```bash
node /root/.openclaw/skills/x-api/x-api.js delete 1234567890
```

**Check your recent tweets:**
```bash
node /root/.openclaw/skills/x-api/x-api.js timeline 10
```

**Schedule a tweet for later (saved to queue, posted by cron):**
```bash
node /root/.openclaw/skills/x-api/x-api.js schedule "Good morning!" "2026-02-22T09:00:00Z"
```

**Schedule a thread for later:**
```bash
node /root/.openclaw/skills/x-api/x-api.js schedule-thread "Tweet 1" "Tweet 2" "2026-02-22T09:00:00Z"
```

## How It Works

- The script uses Node.js built-in `crypto` module — zero dependencies
- OAuth 1.0a HMAC-SHA1 signing is done automatically
- API credentials are read from environment variables
- Output is JSON with `{ success: true/false, data: {...}, summary: "..." }`

## Important Rules

1. Always use `node /root/.openclaw/skills/x-api/x-api.js` — this is your Twitter tool
2. Never try `pip install`, `python`, `curl` with OAuth, or any other method
3. Tweet text max 280 characters
4. Thread max 25 tweets
5. The script returns JSON — check the `success` field to confirm it worked

## Environment Variables

- `X_API_KEY` — X API key (OAuth 1.0a consumer key)
- `X_API_SECRET` — X API secret
- `X_ACCESS_TOKEN` — Access token
- `X_ACCESS_SECRET` — Access token secret
