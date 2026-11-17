---
name: scraping-youtube-channel-data
description: >
  Scrapes YouTube channel statistics and video catalog for any list of channels using
  apidojo's YouTube scraper on Apify. Triggers when the user asks to: get YouTube channel
  stats, fetch subscriber count and video count for YouTube channels, scrape channel
  metadata in bulk, export YouTube channel information by URL or handle, get all videos
  from a YouTube channel, or check channel growth data for a list of creators.
  Returns channel name, subscriber count, total views, video count, and recent video data.
  Ideal for competitor analysis, creator research, and audience benchmarking.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/youtube-scraper
---

# Scraping YouTube Channel Data

Exports channel-level statistics and optional video catalog for any YouTube channel URL or handle.

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
- [ ] Step 1: Normalize channel URLs
- [ ] Step 2: Run youtube-scraper
- [ ] Step 3: Poll for SUCCEEDED
- [ ] Step 4: Deliver channel dataset
```

### Step 2: Run the Actor


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~youtube-channel-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~youtube-channel-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~youtube-channel-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~youtube-channel-scraper"
Input:
{
  "channelUrls": ["https://www.youtube.com/@channelhandle"],
  "maxVideos": 30
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~youtube-channel-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channelUrls": ["https://www.youtube.com/@channelhandle"], "maxVideos": 30}'
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

- **Channel URL not found**: Handle may have changed — verify on YouTube.
- **Hidden subscriber count**: Some channels hide subscriber counts; field returns null — flag these.
- **Age-restricted channel**: May return limited metadata.

## Output Format

```
# YouTube Channel Dataset
Channels requested: N | Returned: N

| Channel | Subscribers | Total Views | Videos | Joined | Country | Recent Avg Views |
|---------|-------------|-------------|--------|--------|---------|-----------------|
| ...     | ...         | ...         | ...    | ...    | ...     | ...             |

Available fields: channelName, channelId, subscriberCount, viewCount, videoCount,
country, joinedDate, description, channelUrl, recentVideos[]
```

## Troubleshooting

**Hidden subscriber count:** YouTube allows channels to hide this — return `null` and note in output.
**Large video catalogs:** Set `maxVideos: 100` max per run to avoid timeouts.