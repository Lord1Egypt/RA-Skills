---
name: scraping-tweets-by-keyword
description: >
  Scrapes tweets matching any keyword, hashtag, phrase, or boolean query using apidojo's
  Twitter Search scraper on Apify. Triggers when the user asks to: scrape tweets about
  a topic, fetch tweets containing a keyword or hashtag, export Twitter search results to
  a dataset, get all tweets mentioning a phrase, pull recent tweets for a search term,
  or collect tweet data for analysis or research. Returns tweet text, author, likes,
  retweets, replies, timestamp, and tweet URL per result.
  Ideal for researchers, data analysts, journalists, and social listening teams.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/tweet-scraper
---

# Scraping Tweets by Keyword

Raw tweet collection for any keyword, hashtag, or boolean search query. No assumed use case — returns the full tweet dataset for downstream analysis.

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
- [ ] Step 1: Build search query string
- [ ] Step 2: Run tweet-scraper
- [ ] Step 3: Poll for SUCCEEDED
- [ ] Step 4: Fetch and deliver dataset
```

### Step 1: Build Search Query

- Hashtag search → `#keyword`
- Exact phrase → `"exact phrase"`
- Boolean → `word1 AND word2 -exclude`
- From account → `from:username`
- Mention → `@username`

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
  "searchTerms": ["<query>"],
  "maxItems": 200,
  "since": "<YYYY-MM-DD>",
  "lang": "<lang_code>"
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"searchTerms": ["<query>"], "maxItems": 200}'
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

- **0 results**: Query may be too narrow, misspelled, or language-filtered. Broaden term, remove language filter, extend date range.
- **< 20 results**: Try removing `since`/`until` constraints. Some low-volume terms have sparse data.
- **Duplicate tweet IDs**: Deduplicate by `id` field before delivering.
- **Suspended/deleted accounts**: Tweets from suspended accounts return with empty author fields — flag these rows.

## Output Format

```
# Tweet Dataset: "<query>"
Total collected: N | Date range: SINCE – UNTIL | Language: LANG

| Tweet ID | Author | Text (truncated) | Likes | Retweets | Replies | Timestamp |
|----------|--------|-----------------|-------|----------|---------|-----------|
| ...      | ...    | ...             | ...   | ...      | ...     | ...       |

Full dataset: N rows × 15 fields
Available fields: id, text, author_id, author_username, likeCount, retweetCount,
replyCount, quoteCount, lang, createdAt, tweetUrl, media, isRetweet, isQuote, source
```

## Troubleshooting

**Empty results for a valid hashtag:** Twitter API indexing lag — try again after 15 minutes.
**Rate limit error:** Reduce `maxItems` to 100 and retry.
**Timeout on large requests:** Set `maxItems: 500` max per run; chain multiple runs with date ranges for larger datasets.

