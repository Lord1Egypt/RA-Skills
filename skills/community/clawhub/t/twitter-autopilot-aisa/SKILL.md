---
name: twitter-autopilot
description: "Search X Twitter data, monitor accounts, track trends, and publish posts through the AISA relay. Use when: the user needs Twitter search, social listening, influencer monitoring, posting, reply, like, or follow workflows."
author: aisa
version: "1.0.0"
license: Apache-2.0
user-invocable: true
primaryEnv: AISA_API_KEY
requires:
  env:
    - AISA_API_KEY
  bins:
    - python3
metadata:
  openclaw:
    primaryEnv: AISA_API_KEY
    requires:
      env:
        - AISA_API_KEY
      bins:
        - python3
---
# Twitter Autopilot

## When to Use

- Search X Twitter data, monitor accounts, track trends, and publish posts through the AISA relay. Use when: the user needs Twitter search, social listening, influencer monitoring, posting, reply, like, or follow workflows.

## When NOT to Use

- Do not use this skill for browser-cookie extraction, passwords, Keychain access, or other local sensitive credential access.
- Prefer a different skill when the user request is outside this skill's domain.

## Capabilities

- Read Twitter X profiles, timelines, mentions, followers, trends, and search results via AISA APIs.
- Support posting, replying, quoting, liking, unliking, following, and unfollowing through the shipped OAuth relay clients.
- Keep auth API-key based for read paths and OAuth based for write paths without asking for passwords or browser cookies.

## Quick Start

```bash
export AISA_API_KEY="your-key"
```

## Primary Runtime

Use the bundled Python client as the canonical ClawHub runtime path:

```bash
python3 scripts/twitter_client.py
```

## Example Queries

- Research "@OpenAI" and summarize the last 20 tweets about GPT releases.
- Find trending AI topics on X Twitter and group them by sentiment.
- Post this product launch thread to X Twitter after authorization is ready.

## Notes

- Write actions use the bundled `twitter_oauth_client.py` and `twitter_engagement_client.py` helpers.
- If posting or engagement requires authorization, start the OAuth flow first and then retry the action.
