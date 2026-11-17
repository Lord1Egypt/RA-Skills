---
name: x-apify
version: 1.1.0
description: Fetch X/Twitter data via Apify actors. Search tweets, get user profiles, retrieve specific tweets with replies. Features local caching to save API costs. Works from any IP via Apify's proxy infrastructure.
tags: [twitter, x, apify, tweets, social-media, search, scraping, caching]
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      env: ["APIFY_API_TOKEN"]
    primaryEnv: APIFY_API_TOKEN
    envVars:
      - name: APIFY_API_TOKEN
        required: true
        description: "Apify API token from https://console.apify.com/account/integrations"
      - name: APIFY_ACTOR_ID
        required: false
        description: "Apify actor to use. Defaults to apidojo~tweet-scraper."
      - name: X_APIFY_CACHE_DIR
        required: false
        description: "Cache directory. Defaults to .cache/ in the skill directory."
---

# x-apify

Fetch X/Twitter data via Apify API (search tweets, user profiles, specific tweets).

## Default actor

This skill documents `apidojo~tweet-scraper` (Tweet Scraper V2). Store sheet: https://apify.com/apidojo/tweet-scraper

Checked against the Apify API on 2026-08-31:

- Public, not deprecated (`isDeprecated: false`, `notice: NONE`)
- Last code change: 2026-08-31
- 30-day public runs: 4,501,223 succeeded, 0 failed, 19,055 timed out, 245,137 aborted (4,765,415 total). Succeeded share: 94.5%. Failed share: 0%.
- 76,051 total users, 7,247 in the last 30 days

The old default `quacker~twitter-scraper` is deprecated (`isDeprecated: true`, `notice: UNDER_MAINTENANCE`). Last code change: 2026-03-16. 30-day public runs: 24,276 succeeded, 6,746 failed (about 22% failed). https://apify.com/quacker/twitter-scraper is a generic landing page, not an actor sheet.

`scripts/config.py` defaults to this actor. Override it only if you need a different one:

```bash
export APIFY_ACTOR_ID="apidojo~tweet-scraper"
```

### Cost

Pay per event: $0.0004 per tweet ($0.40 per 1,000 tweets) on every Apify plan tier, including Free. The actor page states platform compute is included in that event price. Track spend at https://console.apify.com/billing

Apify Free plan (https://apify.com/pricing, 2026-08-31): $5 prepaid usage per month, no credit card. Unused credits do not roll over. At $0.40 per 1,000 tweets, $5 covers 12,500 tweets, subject to the actor's own Free-plan limits below.

### Actor limits

From the actor README on 2026-08-31:

- Each query must return at least 50 tweets.
- Single-tweet fetch and conversation/reply scraping are not allowed on this actor.
- Free-plan users: at most 5 runs per month, 10 items per run. The actor README states Free-plan users cannot call this actor via the API.

This skill's `--url` mode (one tweet plus replies) does not match this actor. For that, set `APIFY_ACTOR_ID=apidojo~twitter-scraper-lite`. The script default `--max-results` is 50, the actor's minimum.

### Input

JSON. Fields this skill's search/user/url modes map onto:

| Field | Type | Role |
| --- | --- | --- |
| `searchTerms` | string[] | Keyword or [advanced-search](https://github.com/igorbrigadir/twitter-advanced-search) queries |
| `startUrls` | string[] | Profile, search, list, or tweet URLs |
| `twitterHandles` | string[] | Handles without a full URL |
| `maxItems` | integer | Cap on returned tweets |
| `sort` | `"Top"` / `"Latest"` / `"Latest + Top"` | Search sort |
| `tweetLanguage` | ISO 639-1 code | Optional language filter |

Search:

```json
{
  "searchTerms": ["artificial intelligence"],
  "maxItems": 50,
  "sort": "Latest"
}
```

User timeline:

```json
{
  "startUrls": ["https://x.com/OpenAI"],
  "maxItems": 50
}
```

The OpenAPI schema types `startUrls` items as strings. The script currently sends `[{"url": "..."}]` Request-list objects.

### Output

Each dataset item is one tweet. Field names differ from `quacker~twitter-scraper`. If you consume raw actor output (not this skill's normalized JSON), remap:

| Meaning | quacker (old) | apidojo (current) |
| --- | --- | --- |
| Tweet id | `id_str` | `id` |
| Text | `text` | `text` |
| Handle | `user.screen_name` | `author.userName` |
| Display name | `user.name` | `author.name` |
| Created | `created_at` | `createdAt` |
| Likes | `favorite_count` | `likeCount` |
| Retweets | (not provided) | `retweetCount` |
| Replies | `conversation_count` | `replyCount` |
| URL | often missing; built from handle + id | `url` / `twitterUrl` |

The skill script already maps both shapes into `{id, text, author, author_name, created_at, likes, retweets, replies, url}`.

`kaitoeasyapi` uses a different **input** schema (`from`, `tweetIDs`, `twitterContent`; no `startUrls`). Its **output** tweet object uses the same `author.userName` / `likeCount` / `createdAt` names as apidojo.

## Links

- [Apify Pricing](https://apify.com/pricing)
- [Get API token](https://console.apify.com/account/integrations)
- [Tweet Scraper V2 actor](https://apify.com/apidojo/tweet-scraper)

## Setup

1. Create a free Apify account: https://apify.com/
2. Get your API token: https://console.apify.com/account/integrations
3. Set environment variables:

```bash
# Add to ~/.bashrc or ~/.zshrc
export APIFY_API_TOKEN="apify_api_YOUR_TOKEN_HERE"
export APIFY_ACTOR_ID="apidojo~tweet-scraper"

# Or use .env file (never commit this!)
echo 'APIFY_API_TOKEN=apify_api_YOUR_TOKEN_HERE' >> .env
```

Install the Python dependency once:

```bash
python3 -m pip install requests
```

## Usage

### Search Tweets

```bash
# Search for tweets containing keywords
python3 scripts/fetch_tweets.py --search "artificial intelligence"

# Search with hashtags
python3 scripts/fetch_tweets.py --search "#AI #MachineLearning"

# Limit results (use 50+ with the default actor)
python3 scripts/fetch_tweets.py --search "OpenAI" --max-results 50
```

### User Profiles

```bash
# Get tweets from a specific user
python3 scripts/fetch_tweets.py --user "elonmusk"

# Multiple users (comma-separated)
python3 scripts/fetch_tweets.py --user "OpenAI,AnthropicAI"
```

### Specific Tweet

`--url` asks the actor for one tweet URL and up to 50 items (intended to include replies). `apidojo~tweet-scraper` does not allow single-tweet fetch or conversation scraping. Set `APIFY_ACTOR_ID=apidojo~twitter-scraper-lite` for this mode, or expect empty/rejected runs on the default actor.

```bash
python3 scripts/fetch_tweets.py --url "https://x.com/user/status/123456789"

# Also works with twitter.com URLs
python3 scripts/fetch_tweets.py --url "https://twitter.com/user/status/123456789"
```

### Output Formats

```bash
# JSON output (default)
python3 scripts/fetch_tweets.py --search "query" --format json --max-results 50

# Summary format (human-readable)
python3 scripts/fetch_tweets.py --search "query" --format summary --max-results 50

# Save to file
python3 scripts/fetch_tweets.py --search "query" --output results.json --max-results 50
```

### Caching

Tweets are cached locally by default so repeat requests do not start a new actor run.

```bash
# First request: fetches from Apify (costs credits)
python3 scripts/fetch_tweets.py --search "query" --max-results 50

# Second request: uses cache
python3 scripts/fetch_tweets.py --search "query" --max-results 50
# Output: [cached] Results for: query

# Bypass cache (force fresh fetch)
python3 scripts/fetch_tweets.py --search "query" --no-cache --max-results 50

# View cache stats
python3 scripts/fetch_tweets.py --cache-stats

# Clear all cached results
python3 scripts/fetch_tweets.py --clear-cache
```

Cache TTL:

- Search results: 1 hour
- User profiles: 24 hours
- Specific tweets: 24 hours

Cache location: `.cache/` in skill directory (override with `X_APIFY_CACHE_DIR` env var)

## Output Examples

Normalized skill JSON (after `format_results`, not raw actor items):

### JSON Format

```json
{
  "query": "OpenAI",
  "mode": "search",
  "fetched_at": "2026-02-11T10:30:00Z",
  "count": 20,
  "tweets": [
    {
      "id": "1234567890",
      "text": "OpenAI just announced...",
      "author": "techreporter",
      "author_name": "Tech Reporter",
      "created_at": "2026-02-11T09:00:00Z",
      "likes": 1500,
      "retweets": 300,
      "replies": 50,
      "url": "https://x.com/techreporter/status/1234567890"
    }
  ]
}
```

### Summary Format

```
=== X/Twitter Search Results ===
Query: OpenAI
Fetched: 2026-02-11 10:30:00 UTC
Results: 20 tweets

---
@techreporter (Tech Reporter)
2026-02-11 09:00
OpenAI just announced...
[Likes: 1500 | RTs: 300 | Replies: 50]
https://x.com/techreporter/status/1234567890

---
...
```

## Error Handling

The script handles common errors:

- Invalid search query
- User not found
- Tweet not found
- API quota exceeded
- Network errors

## Metadata

```yaml
metadata:
  openclaw:
    emoji: "X"
    requires:
      env:
        APIFY_API_TOKEN: required
        APIFY_ACTOR_ID: optional
        X_APIFY_CACHE_DIR: optional
      bins:
        - python3
```
