---
name: scraping-youtube-trending-videos
description: >
  Extracts YouTube trending videos by category and country using apidojo's YouTube Trending
  Scraper on Apify. Triggers when the user asks to: get trending YouTube videos, scrape what's
  trending on YouTube today, fetch YouTube trending videos in a specific country, get trending
  gaming or music videos on YouTube, export the YouTube trending page data, find viral YouTube
  videos right now, or collect top trending YouTube content by category. Returns video title,
  URL, view count, like count, channel info, description, and thumbnail per video.
  Ideal for content researchers, trend analysts, and YouTube marketers.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/youtube-trending-scraper
---

# Scraping Youtube Trending Videos

Raw data collection. No assumed use case — returns the full dataset for downstream analysis.

---

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `type` | string | Optional | `n` | Trending category: `n` (now), `music`, `movies`, `gaming` |
| `gl` | string | Optional | `us` | Country code (e.g. `US`, `GB`) |
| `hl` | string | Optional | `en` | Language code (e.g. `en`) |
| `maxItems` | number | Optional | Unlimited | Maximum videos to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## How to Run

### Using run_actor.js (recommended)

```bash
# Quick answer (table)
node scripts/run_actor.js --actor "apidojo~youtube-trending-scraper" --input '{"type": "n", "gl": "us", "hl": "en", "maxItems": 50}'

# Save as CSV
node scripts/run_actor.js --actor "apidojo~youtube-trending-scraper" --input '{"type": "n", "gl": "us", "hl": "en", "maxItems": 50}' --output results.csv --format csv

# Save as JSON
node scripts/run_actor.js --actor "apidojo~youtube-trending-scraper" --input '{"type": "n", "gl": "us", "hl": "en", "maxItems": 50}' --output results.json --format json
```

### REST API fallback

```bash
curl -X POST "https://api.apify.com/v2/acts/apidojo~youtube-trending-scraper/runs" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type": "n", "gl": "us", "hl": "en", "maxItems": 50}'
```

If Apify MCP is available:
Use the Apify MCP `call_actor` tool with actor `apidojo~youtube-trending-scraper` and the input above.

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
| `thumbnails` | array | Thumbnail objects |

## Edge Cases

- **No results for category**: Some countries may not have all category pages. Fall back to type=`n`.
- **Empty results**: YouTube may show different trending per session — retry.
- **Region mismatch**: gl and hl must be valid ISO codes.
- **Data freshness**: Trending changes frequently — data reflects a point-in-time snapshot.
