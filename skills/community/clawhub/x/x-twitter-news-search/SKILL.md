---
name: x-twitter-news-search
description: >
  Use this skill to search Twitter/X for recent tweets matching keywords and engagement
  filters. Returns raw tweet data (text, author, likes, retweets, views, URL). Trigger
  when the user asks to "search twitter", "find tweets about", "check twitter for",
  "scan X for", "get tweets about", "what's on twitter about", or any request to fetch
  tweet data from Twitter/X. Also trigger when a cron job or another agent needs tweet
  data. This skill only fetches and filters — it does NOT score, summarize, rank, or
  format results. The calling agent decides what to do with the data.
metadata:
  openclaw:
    requires:
      env:
        - TWITTER_BEARER_TOKEN
      bins:
        - curl
        - jq
    primaryEnv: TWITTER_BEARER_TOKEN
required_environment_variables:
  - name: TWITTER_BEARER_TOKEN
    prompt: "Twitter/X API bearer token (pay-per-use)"
    help: "https://developer.x.com — create a Project, attach an App, copy the Bearer Token"
    required_for: "Searching tweets via Twitter API v2"
---

# X/Twitter News Search

Search Twitter/X for recent tweets matching keywords and engagement thresholds. Returns raw tweet data as JSON — the calling agent handles scoring, formatting, and delivery.

## Quick reference

```bash
curl -s -G "https://api.x.com/2/tweets/search/recent" \
  --data-urlencode 'query=("AI agent" OR "agentic AI") (lang:en) -is:reply -is:retweet' \
  --data-urlencode "max_results=30" \
  --data-urlencode "start_time=$(date -u -v-24H +%Y-%m-%dT%H:%M:%SZ)" \
  --data-urlencode "tweet.fields=created_at,public_metrics,author_id" \
  --data-urlencode "user.fields=username,name" \
  --data-urlencode "expansions=author_id" \
  --data-urlencode "sort_order=relevancy" \
  -H "Authorization: Bearer $TWITTER_BEARER_TOKEN" | jq .
```

## Parameters

The caller provides these. Use defaults when not specified.

| Parameter | Default | Description |
|-----------|---------|-------------|
| keywords | *(required)* | Search terms, combined with OR |
| languages | `["en"]` | Language codes for `lang:` filter |
| min_likes | `0` | Minimum like count (filtered after fetch) |
| min_retweets | `0` | Minimum retweet count (filtered after fetch) |
| lookback_hours | `24` | Time window |
| max_results | `30` | Tweets to return (after filtering) |
| exclude_replies | `true` | Add `-is:reply` to query |
| exclude_retweets | `true` | Add `-is:retweet` to query |

## Procedure

### 1. Check API key

Verify `$TWITTER_BEARER_TOKEN` is set:

```bash
test -n "$TWITTER_BEARER_TOKEN" && echo "OK" || echo "MISSING"
```

If missing, tell the user:
1. Go to https://developer.x.com
2. Create a **Project** and attach an **App**
3. Copy the **Bearer Token**
4. Save it: `hermes config set TWITTER_BEARER_TOKEN <token>`

### 2. Build the query

Combine keywords with OR. Wrap multi-word phrases in quotes:

```
("keyword one" OR "keyword two" OR single) -is:reply -is:retweet
```

Add language filter: `(lang:en OR lang:fr)`

**Available on pay-per-use:** `lang:`, `-is:reply`, `-is:retweet`, `from:`, `has:links`, `has:media`

**NOT available on pay-per-use:** `min_faves`, `min_retweets`, `since`, `until`, `-filter:replies` — use API params and post-fetch filtering instead.

### 3. Call the API

Use `start_time` as an API parameter for the time window:

```bash
curl -s -G "https://api.x.com/2/tweets/search/recent" \
  --data-urlencode "query=QUERY_HERE" \
  --data-urlencode "max_results=50" \
  --data-urlencode "start_time=ISO_TIMESTAMP" \
  --data-urlencode "tweet.fields=created_at,public_metrics,author_id" \
  --data-urlencode "user.fields=username,name" \
  --data-urlencode "expansions=author_id" \
  --data-urlencode "sort_order=relevancy" \
  -H "Authorization: Bearer $TWITTER_BEARER_TOKEN"
```

Generate `start_time`:
- Linux: `date -u -d "$N hours ago" +%Y-%m-%dT%H:%M:%SZ`
- macOS: `date -u -v-${N}H +%Y-%m-%dT%H:%M:%SZ`

Fetch 3x `max_results` to have enough after engagement filtering.

### 4. Extract and filter

Parse with jq — see `references/twitter-api.md` for full response schema.

```bash
... | jq '[
  .data[] as $t |
  (.includes.users[] | select(.id == $t.author_id)) as $u |
  {
    id: $t.id,
    text: $t.text,
    author: $u.username,
    author_name: $u.name,
    likes: $t.public_metrics.like_count,
    retweets: $t.public_metrics.retweet_count,
    replies: $t.public_metrics.reply_count,
    views: $t.public_metrics.impression_count,
    created_at: $t.created_at,
    url: ("https://x.com/" + $u.username + "/status/" + $t.id)
  }
] | sort_by(-.likes)'
```

Filter by engagement:

```bash
... | jq --argjson ml 50 --argjson mr 5 '[.[] | select(.likes >= $ml and .retweets >= $mr)]'
```

Trim to max_results: `| .[:30]`

### 5. Return the data

Return the filtered array as JSON. Do not score, summarize, or format — just the raw tweet objects.

## Pitfalls

- **Empty results:** Return empty array `[]`, not an error. Some queries have no matches.
- **start_time format:** Must be ISO 8601 with Z: `2026-04-28T00:00:00Z`
- **API cost:** $0.005 per tweet read. A 50-tweet fetch = $0.25.
- **Rate cap:** 2M reads/month on pay-per-use. Budget accordingly.
- **Engagement filtering:** Always fetch more tweets than needed since `min_faves`/`min_retweets` operators are not available on pay-per-use.

## Verification

After fetching, confirm:
1. Returned tweets meet the engagement thresholds
2. No replies or retweets unless caller requested them
3. Tweets are within the lookback window
4. Author usernames and URLs are resolved correctly
