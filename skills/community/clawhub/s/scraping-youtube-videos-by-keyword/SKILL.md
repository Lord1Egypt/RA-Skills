---
name: scraping-youtube-videos-by-keyword
description: >
  Scrapes YouTube videos matching any keyword or search query using apidojo's YouTube
  scraper on Apify. Triggers when the user asks to: get YouTube videos for a keyword,
  scrape YouTube search results for a topic, export YouTube video data for a query,
  fetch video metadata for a YouTube search term, collect YouTube videos about a subject,
  or download YouTube video stats by keyword. Returns video title, channel name, view
  count, like count, comment count, duration, and publish date per video.
  Ideal for content researchers, SEO analysts, and market intelligence teams.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/youtube-scraper
---

# Scraping YouTube Videos by Keyword

Raw YouTube video dataset for any search query. Returns video-level metadata including engagement metrics and channel info.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | Optional | `[]` | YouTube URLs — channels, playlists, Shorts, search results |
| `youtubeHandles` | array | Optional | `[]` | YouTube channel handles (e.g. `@kurzgesagt`) |
| `getTrending` | boolean | Optional | `false` | Retrieve trending videos |
| `keywords` | array | Optional | `[]` | Search keywords |
| `gl` | string | Optional | `us` | Country code for results (e.g. `US`, `GB`) |
| `hl` | string | Optional | `en` | Language code (e.g. `en`, `de`) |
| `uploadDate` | string | Optional | `all` | Upload date filter: `any`, `hour`, `today`, `week`, `month`, `year` |
| `duration` | string | Optional | `all` | Duration filter: `any`, `short`, `long` |
| `features` | string | Optional | `all` | Feature filter: `4k`, `hd`, `live`, `cc`, `3d`, `hdr`, etc. |
| `sort` | string | Optional | `r` | Sort order for search results |
| `maxItems` | number | Optional | Unlimited | Maximum videos to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## Workflow

```
Progress:
- [ ] Step 1: Build search query
- [ ] Step 2: Run youtube-scraper
- [ ] Step 3: Poll for SUCCEEDED
- [ ] Step 4: Deliver video dataset
```

### Step 2: Run the Actor


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~youtube-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~youtube-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~youtube-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~youtube-scraper"
Input:
{
  "searchKeywords": "<query>",
  "maxResults": 50,
  "sortBy": "relevance"
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~youtube-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"searchKeywords": "<query>", "maxResults": 50}'
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

- **< 20 results**: Query may be too narrow; broaden search term.
- **Age-restricted content in results**: These may have limited metadata — flag rows with missing `viewCount`.
- **Duplicate video IDs**: Deduplicate by `videoId`.

## Output Format

```
# YouTube Video Dataset: "<query>"
Videos collected: N | Sort: <sortBy>

| Video ID | Title | Channel | Views | Likes | Comments | Duration | Published |
|----------|-------|---------|-------|-------|----------|----------|-----------|
| ...      | ...   | ...     | ...   | ...   | ...      | ...      | ...       |

Available fields: videoId, title, channelName, channelId, viewCount, likeCount,
commentCount, duration, publishedAt, videoUrl, thumbnailUrl, description
```

## Troubleshooting

**Fewer results than requested:** YouTube search may have limited results for niche queries.
**Missing like counts:** YouTube hides dislikes but likes are still available; some videos hide all counts.