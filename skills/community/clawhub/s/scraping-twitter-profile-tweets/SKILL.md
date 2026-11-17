---
name: scraping-twitter-profile-tweets
description: >
  Extracts tweets, reply threads, and engagement metrics from a specific Twitter/X profile
  using apidojo's Twitter Profile Scraper on Apify. Triggers when the user asks to: get all tweets
  from a Twitter account, scrape tweets from a specific user's profile, export tweet history from
  a Twitter handle, get recent tweets from a Twitter account with engagement stats, fetch tweet
  timeline for a specific user, or collect posts from a Twitter profile by username. Returns tweet
  text, likes, retweets, replies, views, bookmarks, and author info per tweet.
  Ideal for social media monitors, journalists, and competitive intelligence teams.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/twitter-profile-scraper
---

# Scraping Twitter Profile Tweets

Raw data collection. No assumed use case — returns the full dataset for downstream analysis.

---

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | Optional | `[]` | Twitter profile URLs (x.com or twitter.com formats) |
| `twitterHandles` | array | Optional | `[]` | Twitter usernames (without @) |
| `start` | string | Optional | — | Tweets after this date (YYYY-MM-DD or YYYY-MM-DD_HH:MM:SS_UTC) |
| `end` | string | Optional | — | Tweets before this date (YYYY-MM-DD or YYYY-MM-DD_HH:MM:SS_UTC) |
| `includeNativeRetweets` | boolean | Optional | `false` | Include native retweets in results |
| `onlyImages` | boolean | Optional | `false` | Only tweets containing images |
| `getReplies` | boolean | Optional | `false` | Include tweet replies |
| `minReplyCount` | number | Optional | — | Minimum reply count threshold |
| `getAboutData` | boolean | Optional | `false` | Fetch full profile about data |
| `maxItems` | number | Optional | Unlimited | Maximum tweets to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## How to Run

### Using run_actor.js (recommended)

```bash
# Quick answer (table)
node scripts/run_actor.js --actor "apidojo~twitter-profile-scraper" --input '{"twitterHandles": ["elonmusk"], "maxItems": 100}'

# Save as CSV
node scripts/run_actor.js --actor "apidojo~twitter-profile-scraper" --input '{"twitterHandles": ["elonmusk"], "maxItems": 100}' --output results.csv --format csv

# Save as JSON
node scripts/run_actor.js --actor "apidojo~twitter-profile-scraper" --input '{"twitterHandles": ["elonmusk"], "maxItems": 100}' --output results.json --format json
```

### REST API fallback

```bash
curl -X POST "https://api.apify.com/v2/acts/apidojo~twitter-profile-scraper/runs" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"twitterHandles": ["elonmusk"], "maxItems": 100}'
```

If Apify MCP is available:
Use the Apify MCP `call_actor` tool with actor `apidojo~twitter-profile-scraper` and the input above.

---

## Output Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Always `tweet` |
| `id` | string | Tweet ID |
| `url` | string | Tweet URL (x.com) |
| `twitterUrl` | string | Tweet URL (twitter.com) |
| `text` | string | Tweet text content |
| `retweetCount` | number | Retweet count |
| `replyCount` | number | Reply count |
| `likeCount` | number | Like count |
| `quoteCount` | number | Quote tweet count |
| `bookmarkCount` | number | Bookmark count |
| `createdAt` | string | Creation timestamp |
| `lang` | string | Detected language |
| `isReply` | boolean | Whether this is a reply |
| `isRetweet` | boolean | Whether this is a retweet |
| `isQuote` | boolean | Whether this is a quote tweet |
| `source` | string | Twitter client used |
| `author.userName` | string | Author @username |
| `author.name` | string | Author display name |
| `author.isVerified` | boolean | Legacy verification |
| `author.isBlueVerified` | boolean | Twitter Blue verification |
| `author.profilePicture` | string | Author profile picture URL |
| `author.followers` | number | Author follower count |

## Edge Cases

- **Private account**: Returns 0 tweets. Tell user the account is private.
- **Account suspended**: Returns error. Handle may be banned.
- **Very active account**: Use maxItems to cap and control cost ($0.0004 per extra tweet).
- **Date range**: Minimum 50 results needed for the query to run. If few tweets in range, widen date range.
- **Retweets in results**: Actor returns all public tweets including retweets.
