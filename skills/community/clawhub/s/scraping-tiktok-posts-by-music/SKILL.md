---
name: scraping-tiktok-posts-by-music
description: >
  Extracts TikTok posts using a specific audio track or sound using apidojo's TikTok Music
  Scraper on Apify. Triggers when the user asks to: get all TikTok videos using a specific sound,
  find TikTok posts using an audio clip, scrape TikTok videos using a trending music track, export
  TikTok posts made with a song, find creators using a specific sound, or collect TikTok content
  associated with a music URL. Returns video caption, views, likes, comments, channel info, song
  metadata, and hashtags per post. Ideal for music marketers, trend analysts, and viral sound trackers.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/tiktok-music-scraper
---

# Scraping Tiktok Posts By Music

Raw data collection. No assumed use case — returns the full dataset for downstream analysis.

---

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | ✅ | `[]` | TikTok music/sound page URLs |
| `maxItems` | number | Optional | Unlimited | Maximum posts to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## How to Run

### Using run_actor.js (recommended)

```bash
# Quick answer (table)
node scripts/run_actor.js --actor "apidojo~tiktok-music-scraper" --input '{"startUrls": ["https://www.tiktok.com/music/Song-Title-123456"], "maxItems": 100}'

# Save as CSV
node scripts/run_actor.js --actor "apidojo~tiktok-music-scraper" --input '{"startUrls": ["https://www.tiktok.com/music/Song-Title-123456"], "maxItems": 100}' --output results.csv --format csv

# Save as JSON
node scripts/run_actor.js --actor "apidojo~tiktok-music-scraper" --input '{"startUrls": ["https://www.tiktok.com/music/Song-Title-123456"], "maxItems": 100}' --output results.json --format json
```

### REST API fallback

```bash
curl -X POST "https://api.apify.com/v2/acts/apidojo~tiktok-music-scraper/runs" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"startUrls": ["https://www.tiktok.com/music/Song-Title-123456"], "maxItems": 100}'
```

If Apify MCP is available:
Use the Apify MCP `call_actor` tool with actor `apidojo~tiktok-music-scraper` and the input above.

---

## Output Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | TikTok post ID |
| `title` | string | Post caption/text |
| `views` | number | View count |
| `likes` | number | Like count |
| `comments` | number | Comment count |
| `shares` | number | Share count |
| `hashtags` | array | Hashtags used in post |
| `channel.name` | string | Creator display name |
| `channel.username` | string | Creator @username |
| `channel.verified` | boolean | Verification status |
| `uploadedAt` | number | Upload timestamp (Unix) |
| `video.url` | string | Video file URL |
| `video.duration` | number | Duration in seconds |
| `song.id` | string | Sound/music ID |
| `song.title` | string | Sound title |
| `song.artist` | string | Sound artist |
| `song.duration` | number | Sound duration |

## Edge Cases

- **No music URL**: Requires TikTok sound page URL. Tell user to find the sound on TikTok and copy the URL.
- **Copyrighted sound**: May have fewer results in some regions.
- **Trending sound**: May return thousands of posts — use maxItems to cap.
- **Sound removed**: Returns empty dataset.
