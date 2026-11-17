---
name: scraping-tweets-from-account
description: >
  Scrapes all tweets, replies, and media from any Twitter/X account using apidojo's
  Tweet scraper on Apify. Triggers when the user asks to: get all tweets from a Twitter
  account, export a user's tweet history, scrape a specific Twitter profile's posts,
  fetch the latest tweets from an account, download tweet data from a user timeline,
  or collect all posts from a Twitter username. Returns tweet text, likes, retweets,
  replies, media URLs, and timestamp per tweet.
  Ideal for journalists, researchers, competitive analysts, and data engineers.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/tweet-scraper
---

# Scraping Tweets from an Account

Exports the full tweet history of any public Twitter/X account. Returns the raw timeline dataset including replies and media.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `searchTerms` | array | ✅ | `[]` | Twitter advanced search queries (e.g. `["#AI lang:en", "from:NASA"]`) |
| `sort` | string | Optional | `Top` | Sort order: `Latest`, `Top`, or `Latest+Top` |
| `tweetLanguage` | string | Optional | — | ISO 639-1 language code (e.g. `en`) |
| `maxItems` | number | Optional | Unlimited | Maximum tweets to return |
| `onlyVerifiedUsers` | boolean | Optional | `false` | Only tweets from verified users |
| `onlyTwitterBlue` | boolean | Optional | `false` | Only Twitter Blue subscribers |
| `onlyImage` | boolean | Optional | `false` | Only tweets with images |
| `onlyVideo` | boolean | Optional | `false` | Only tweets with videos |
| `onlyQuote` | boolean | Optional | `false` | Only quote tweets |
| `author` | string | Optional | — | Filter to a specific author handle |
| `inReplyTo` | string | Optional | — | Tweets replying to a specific handle |
| `mentioning` | string | Optional | — | Tweets mentioning a specific handle |
| `geotaggedNear` | string | Optional | — | Tweets near a location |
| `withinRadius` | string | Optional | — | Radius around geotaggedNear |
| `geocode` | string | Optional | — | Lat/lng + radius string |
| `placeObjectId` | string | Optional | — | Tweets tagged with a place |
| `minimumRetweets` | number | Optional | — | Minimum retweet count |
| `minimumFavorites` | number | Optional | — | Minimum like count |
| `minimumReplies` | number | Optional | — | Minimum reply count |
| `start` | string | Optional | — | Tweets after this date (YYYY-MM-DD) |
| `end` | string | Optional | — | Tweets before this date (YYYY-MM-DD) |
| `includeSearchTerms` | boolean | Optional | `false` | Add the matched search term to each tweet |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## Workflow

```
Progress:
- [ ] Step 1: Confirm account is public
- [ ] Step 2: Run tweet-scraper
- [ ] Step 3: Poll for SUCCEEDED
- [ ] Step 4: Fetch and deliver dataset
```

### Step 1: Validate Input

Strip `@` from username if present. Do not attempt to scrape private accounts — the actor will return 0 results.

### Step 2: Run the Actor


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~tweet-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~tweet-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~tweet-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~tweet-scraper"
Input:
{
  "twitterHandles": ["<handle>"],
  "maxItems": 200,
  "sort": "Latest"
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"twitterHandles": ["<handle>"], "maxItems": 200, "sort": "Latest"}'
```

Save `id` as `RUN_ID`. Poll until `status = SUCCEEDED`:
```bash
curl "https://api.apify.com/v2/actor-runs/$RUN_ID?token=$APIFY_TOKEN" | grep '"status"'
```

Fetch results:
```bash
curl "https://api.apify.com/v2/actor-runs/$RUN_ID/dataset/items?token=$APIFY_TOKEN&format=json"
```

### Step 3: Handle Edge Cases

- **0 results**: Account may be private, suspended, or handle misspelled. Report to user.
- **Fewer results than expected**: Account may have fewer public tweets than requested. Return what is available.
- **Protected account**: Actor returns empty — inform user the account is private.

## Output Format

```
# Tweet Timeline: @<username>
Tweets collected: N | Includes replies: YES/NO | Includes retweets: YES/NO

| Tweet ID | Text (truncated) | Likes | Retweets | Replies | Media | Timestamp |
|----------|-----------------|-------|----------|---------|-------|-----------|
| ...      | ...             | ...   | ...      | ...     | ...   | ...       |

Full dataset: N rows × 12 fields
Available fields: id, text, likeCount, retweetCount, replyCount, quoteCount,
isReply, isRetweet, media, tweetUrl, lang, createdAt
```

## Troubleshooting

**0 results for a known public account:** Try again — Twitter may rate-limit intermittently.
**Missing older tweets:** Twitter API limits historical access; very old tweets may not be available.
**Timeout:** Reduce `maxItems` to 500 max per run.