---
name: twitter-intel
description: Twitter keyword search, monitoring, and trend analysis via GraphQL
homepage: https://canlah.ai
metadata: {"openclaw": {"emoji": "🔍", "os": ["darwin", "linux"], "requires": {"bins": ["python3"], "env": ["TWITTER_COOKIES_PATH"]}}}
---

# Twitter Intel — Keyword Search & Trend Monitor

Search Twitter by keyword, collect high-engagement tweets, analyze trends over time, and generate structured reports. Powered by `rnet_twitter.py` GraphQL search (no browser automation needed).

---

## Architecture

```
Phase 1: On-demand Search (user-triggered)
  User says "search OpenAI on twitter" -> search -> filter -> report

Phase 2: Keyword Monitoring (cron-driven)
  Config defines keywords -> scheduled search -> diff with last run -> alert on new high-engagement tweets

Phase 3: Trend Analysis (on-demand or weekly)
  Aggregate saved searches -> group by week -> detect topic shifts -> generate narrative
```

---

## Prerequisites

```bash
# Install rnet (Rust HTTP client with TLS fingerprint emulation)
pip install "rnet>=3.0.0rc20" --pre

# Required files:
# 1. rnet_twitter.py — lightweight async Twitter GraphQL client
#    Get it: https://github.com/PHY041/rnet-twitter-client
# 2. twitter_cookies.json — your auth cookies
#    Format: [{"name": "auth_token", "value": "..."}, {"name": "ct0", "value": "..."}]
#    Get cookies: Chrome DevTools → Application → Cookies → x.com
#    Cookies expire ~2 weeks. Refresh when you get 403 errors.
```

Set `TWITTER_COOKIES_PATH` env var to your cookies file location.

---

## Phase 1: On-demand Search

When user says "search [keyword] on twitter", "twitter intel [topic]", "find tweets about [X]":

### Step 1 — Run Search

```python
import asyncio, os
from rnet_twitter import RnetTwitterClient

async def search(query, count=200):
    client = RnetTwitterClient()
    cookies_path = os.environ.get("TWITTER_COOKIES_PATH", "twitter_cookies.json")
    client.load_cookies(cookies_path)
    tweets = await client.search_tweets(query, count=count, product="Top")
    return tweets
```

**Search modes:**

| Mode | `product=` | Use case |
|------|-----------|----------|
| High-engagement | `"Top"` | Find influential tweets, content analysis |
| Real-time | `"Latest"` | Monitor breaking discussions, live tracking |

**Useful Twitter search operators:**

| Operator | Example | Effect |
|----------|---------|--------|
| `lang:en` | `OpenAI lang:en` | English only |
| `since:` / `until:` | `since:2026-01-24 until:2026-02-24` | Date range |
| `-filter:replies` | `OpenAI -filter:replies` | Original tweets only |
| `min_faves:N` | `min_faves:50` | Minimum likes (only works with Latest) |
| `from:` | `from:karpathy` | Specific author |
| `"exact"` | `"AI agent"` | Exact phrase |

### Step 2 — Filter & Enrich

After raw search, filter for quality:

```python
filtered = [
    t for t in tweets
    if keyword.lower() in t["text"].lower()
    and (t["favorite_count"] >= 10 or t["retweet_count"] >= 5)
    and not t["is_reply"]
]
```

### Step 3 — Report

Output a structured summary:

```
## Twitter Intel: [keyword]
**Period:** [date range] | **Tweets found:** N | **After filter:** N

### Top Tweets (by engagement)
1. @author (X likes, Y RTs, Z views) — date
   "tweet text..."
   [link]

### Key Themes
- Theme 1: [description] (N tweets)
- Theme 2: [description] (N tweets)

### Notable Authors
| Author | Followers | Tweets in set | Total engagement |
```

---

## Phase 2: Keyword Monitoring (Cron)

### Config File

```json
{
  "monitors": [
    {
      "id": "my-product-en",
      "query": "MyProduct lang:en -filter:replies",
      "product": "Top",
      "count": 100,
      "min_likes": 10,
      "alert_threshold": 100,
      "enabled": true
    }
  ]
}
```

### State File

```json
{
  "my-product-en": {
    "last_run": "2026-02-24T12:00:00Z",
    "last_tweet_ids": ["id1", "id2"],
    "total_collected": 450
  }
}
```

### Cron Workflow

1. Read config -> iterate enabled monitors
2. For each monitor:
   - Run `search_tweets(query, count, product)`
   - Filter by `min_likes`
   - Diff against `last_tweet_ids` -> find NEW tweets only
   - If any new tweet has `favorite_count >= alert_threshold` -> immediate alert
   - Save all new tweets to daily file `{monitor_id}/YYYY-MM-DD.json`
   - Update state file
3. Send summary notification (if there are new notable tweets)

---

## Phase 3: Trend Analysis

When user says "analyze twitter trend for [keyword]", "twitter trend report":

1. Load all saved daily files from `{monitor_id}/`
2. Group tweets by week
3. For each week, extract:
   - Total tweet count + total engagement
   - Top 5 tweets by likes
   - Dominant themes (use LLM to categorize)
   - New authors that appeared
   - Sentiment shift
4. Generate a week-by-week narrative

---

## Commands

| User Says | Agent Does |
|-----------|-----------|
| `/twitter-intel [keyword]` | Search + filter + report (Top, 200 tweets) |
| `/twitter-intel "[phrase]" --latest` | Search Latest mode |
| `monitor "[keyword]" on twitter` | Add to monitoring config |
| `twitter intel status` | Show all active monitors + last run |
| `twitter trend report [keyword]` | Analyze saved data, generate trend narrative |
| `refresh twitter cookies` | Guide user through cookie refresh |

---

## Technical Notes

- **SearchTimeline requires POST** (GET returns 404) — handled by `rnet_twitter.py`
- **GraphQL query IDs rotate** — if search returns 404, re-extract from `https://abs.twimg.com/responsive-web/client-web/main.*.js`
- **Rate limits**: ~300 requests/15min window. With 20 tweets per page, 200 tweets = 10 requests. Safe for cron every 4 hours.
- **Cookie lifetime**: `auth_token` expires after ~2 weeks. Monitor for 403 errors.
