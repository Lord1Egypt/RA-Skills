---
name: scraping-tiktok-videos-by-hashtag
description: >
  Scrapes TikTok videos for any hashtag or keyword using apidojo's TikTok scraper on Apify.
  Triggers when the user asks to: get all TikTok videos for a hashtag, scrape TikTok content
  by topic or tag, export TikTok video data for a keyword, fetch TikTok posts under a
  challenge or trend, collect TikTok video metrics for a hashtag, or download TikTok
  video metadata by tag. Returns video URL, view count, like count, comment count, share
  count, author handle, caption, and timestamp per video.
  Ideal for trend researchers, data analysts, and social media teams.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/tiktok-scraper
---

# Scraping TikTok Videos by Hashtag

Raw video dataset for any TikTok hashtag or keyword. Returns full video metadata including engagement metrics and author info.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | Optional | `[]` | TikTok URLs — user profiles, hashtags, music pages, search, locations |
| `keywords` | array | Optional | `[]` | Search keywords/terms to find posts |
| `sortType` | string | Optional | `RELEVANCE` | Sort order for keyword results: `RELEVANCE`, `MOST_LIKED`, `DATE_POSTED` |
| `location` | string | Optional | — | ISO 3166-1 alpha-2 country code for regional filtering (e.g. `US`, `GB`) |
| `maxItems` | number | Optional | Unlimited | Maximum posts to return across the run |
| `includeSearchKeywords` | boolean | Optional | `false` | Add the matched search keyword field to each post |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## Workflow

```
Progress:
- [ ] Step 1: Normalize hashtag list
- [ ] Step 2: Run tiktok-scraper
- [ ] Step 3: Poll for SUCCEEDED
- [ ] Step 4: Deliver video dataset
```

### Step 2: Run the Actor


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~tiktok-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~tiktok-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~tiktok-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~tiktok-scraper"
Input:
{
  "keywords": ["tag1", "tag2"],
  "maxItems": 100
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~tiktok-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"keywords": ["tag1", "tag2"], "maxItems": 100}'
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

- **0 results for hashtag**: Hashtag may be banned on TikTok or spelled incorrectly. Try alternate spelling.
- **< 20 results**: Hashtag may be very niche — inform user, return what is available.
- **Duplicate video IDs across hashtags**: Deduplicate by `videoId` field.

## Output Format

```
# TikTok Video Dataset: #<hashtag>
Videos collected: N | Hashtags queried: N

| Video ID | Author | Caption (truncated) | Views | Likes | Comments | Shares | Posted |
|----------|--------|---------------------|-------|-------|----------|--------|--------|
| ...      | ...    | ...                 | ...   | ...   | ...      | ...    | ...    |

Available fields: videoId, authorUsername, desc, playCount, diggCount, commentCount,
shareCount, createTime, videoUrl, musicTitle, hashtags, isAd
```

## Troubleshooting

**Banned hashtag returns 0:** Some hashtags are restricted by TikTok — try parent category tag.
**Slow run:** TikTok rate-limits heavily; `maxItems: 200` is a safe cap per run.