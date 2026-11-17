---
name: scraping-youtube-playlist
description: >
  Extracts all videos from a YouTube playlist using apidojo's YouTube Playlist Scraper on
  Apify. Triggers when the user asks to: get all videos from a YouTube playlist, scrape a YouTube
  playlist for video data, export playlist video metadata, fetch video stats from a YouTube playlist
  URL, collect all videos in a YouTube channel playlist, download YouTube playlist contents, or
  analyze a curated list of YouTube videos. Returns video title, URL, view count, like count,
  duration, channel info, and description per video. Ideal for content curators, educators, and
  YouTube channel analysts.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/youtube-playlist-scraper
---

# Scraping Youtube Playlist

Raw data collection. No assumed use case — returns the full dataset for downstream analysis.

---

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | Optional | `[]` | YouTube playlist URLs |
| `keywords` | array | Optional | `[]` | Search keywords to find playlists |
| `gl` | string | Optional | `us` | Country code (e.g. `US`) |
| `hl` | string | Optional | `en` | Language code (e.g. `en`) |
| `sort` | string | Optional | `r` | Sort order |
| `maxItems` | number | Optional | Unlimited | Maximum videos to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## How to Run

### Using run_actor.js (recommended)

```bash
# Quick answer (table)
node scripts/run_actor.js --actor "apidojo~youtube-playlist-scraper" --input '{"startUrls": ["https://www.youtube.com/playlist?list=PLABCDE12345"], "maxItems": 50}'

# Save as CSV
node scripts/run_actor.js --actor "apidojo~youtube-playlist-scraper" --input '{"startUrls": ["https://www.youtube.com/playlist?list=PLABCDE12345"], "maxItems": 50}' --output results.csv --format csv

# Save as JSON
node scripts/run_actor.js --actor "apidojo~youtube-playlist-scraper" --input '{"startUrls": ["https://www.youtube.com/playlist?list=PLABCDE12345"], "maxItems": 50}' --output results.json --format json
```

### REST API fallback

```bash
curl -X POST "https://api.apify.com/v2/acts/apidojo~youtube-playlist-scraper/runs" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"startUrls": ["https://www.youtube.com/playlist?list=PLABCDE12345"], "maxItems": 50}'
```

If Apify MCP is available:
Use the Apify MCP `call_actor` tool with actor `apidojo~youtube-playlist-scraper` and the input above.

---

## Output Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Always `video` |
| `id` | string | Video ID |
| `title` | string | Video title |
| `url` | string | Video URL |
| `description` | string | Video description |
| `duration` | number | Duration in seconds |
| `views` | number | View count |
| `likes` | number | Like count |
| `status` | string | Availability status |
| `channel.id` | string | Channel ID |
| `channel.name` | string | Channel name |
| `channel.url` | string | Channel URL |
| `keywords` | array | Video tags/keywords |
| `isLive` | boolean | Live stream flag |
| `isPrivate` | boolean | Private flag |
| `thumbnails` | array | Thumbnail objects |

## Edge Cases

- **Private playlist**: Returns 0 results. Tell user the playlist is private.
- **Deleted playlist**: Returns error or empty. Check URL.
- **Very large playlist**: Use maxItems to cap results and avoid long run times.
- **Mix playlist (YouTube auto-generated)**: May behave differently than user-created playlists.
