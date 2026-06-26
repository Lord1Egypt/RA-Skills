# Twitter API v2 — Reference

## Endpoint

```
GET https://api.x.com/2/tweets/search/recent
```

Searches tweets from the last 7 days.

## Authentication

```
Authorization: Bearer $TWITTER_BEARER_TOKEN
```

## Query parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `query` | Yes | Search query (max 512 chars) |
| `max_results` | No | 10-100 (default 10) |
| `start_time` | No | ISO 8601 timestamp, oldest tweets |
| `end_time` | No | ISO 8601 timestamp, newest tweets |
| `sort_order` | No | `recency` or `relevancy` |
| `tweet.fields` | No | Comma-separated: `created_at,public_metrics,author_id` |
| `user.fields` | No | Comma-separated: `username,name,verified` |
| `expansions` | No | `author_id` to include user objects |
| `next_token` | No | Pagination cursor from previous response |

## Query operators (pay-per-use tier)

| Operator | Example | Description |
|----------|---------|-------------|
| keyword | `AI agent` | Matches word in tweet text |
| "exact phrase" | `"agentic AI"` | Exact phrase match |
| OR | `cat OR dog` | Either term |
| -negation | `-crypto` | Exclude term |
| lang: | `lang:en` | Tweet language |
| -is:reply | `-is:reply` | Exclude replies |
| -is:retweet | `-is:retweet` | Exclude retweets |
| from: | `from:elonmusk` | Tweets by user |
| to: | `to:openai` | Replies to user |
| has:links | `has:links` | Only tweets with URLs |
| has:media | `has:media` | Only tweets with media |
| has:images | `has:images` | Only tweets with images |
| url: | `url:github.com` | Tweets linking to domain |

### NOT available on pay-per-use

These require Pro ($5K/mo) or Enterprise:
- `min_faves:N`, `min_retweets:N`
- `since:`, `until:` (use `start_time`/`end_time` params instead)
- `-filter:replies` (use `-is:reply` instead)
- `place:`, `bounding_box:`
- Streaming endpoints

## Response format

```json
{
  "data": [
    {
      "id": "1234567890",
      "text": "Full tweet text here...",
      "author_id": "9876543210",
      "created_at": "2026-04-28T10:30:00.000Z",
      "public_metrics": {
        "retweet_count": 42,
        "reply_count": 7,
        "like_count": 256,
        "quote_count": 3,
        "impression_count": 15000
      }
    }
  ],
  "includes": {
    "users": [
      {
        "id": "9876543210",
        "username": "airesearcher",
        "name": "AI Researcher"
      }
    ]
  },
  "meta": {
    "newest_id": "1234567890",
    "oldest_id": "1234567880",
    "result_count": 10,
    "next_token": "abc123_pagination_token"
  }
}
```

## Pagination

If `meta.next_token` exists, there are more results. Pass it as `next_token` parameter:

```bash
curl -s -G "https://api.x.com/2/tweets/search/recent" \
  --data-urlencode "query=QUERY" \
  --data-urlencode "next_token=abc123_pagination_token" \
  ...
```

## Error responses

| Status | Meaning | Common cause |
|--------|---------|--------------|
| 400 | Invalid request | Bad query syntax or unsupported operator |
| 401 | Unauthorized | Invalid or expired bearer token |
| 403 | Forbidden | App not attached to a Project |
| 429 | Rate limited | Too many requests |

## Pricing (pay-per-use)

- $0.005 per tweet read
- 24h dedup: same tweet read twice in a UTC day = 1 charge
- Monthly cap: 2M reads
- No streaming endpoints on this tier

## jq recipes

### Extract flat tweet objects with author

```bash
jq '[
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

### Filter by engagement

```bash
jq --argjson ml 50 --argjson mr 5 '[.[] | select(.likes >= $ml and .retweets >= $mr)]'
```

### Count results

```bash
jq '.meta.result_count'
```

### Get just URLs

```bash
jq -r '[.data[] as $t | (.includes.users[] | select(.id == $t.author_id)) as $u | "https://x.com/\($u.username)/status/\($t.id)"] | .[]'
```
