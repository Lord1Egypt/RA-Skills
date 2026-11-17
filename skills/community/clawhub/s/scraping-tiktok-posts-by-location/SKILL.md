---
name: scraping-tiktok-posts-by-location
description: >
  Extracts TikTok posts tagged at a specific location using apidojo's TikTok Location Scraper
  on Apify. Triggers when the user asks to: get TikTok videos from a specific location, scrape
  TikTok posts tagged at a place, find TikTok content from a city or venue, collect TikTok videos
  geotagged at a location URL, export TikTok location-tagged content, or pull TikTok posts from
  a place page. Returns video title, views, likes, comments, shares, channel info, hashtags,
  and timestamp per post. Ideal for local marketing teams, event researchers, and geo-targeting analysts.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/tiktok-location-scraper
---

# Scraping Tiktok Posts By Location

Raw data collection. No assumed use case — returns the full dataset for downstream analysis.

---

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | ✅ | `[]` | TikTok location/place URLs (e.g. `https://www.tiktok.com/tag/newyork?location=true`) |
| `maxItems` | number | Optional | Unlimited | Maximum posts to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## How to Run

### Using run_actor.js (recommended)

```bash
# Quick answer (table)
node scripts/run_actor.js --actor "apidojo~tiktok-location-scraper" --input '{"startUrls": ["https://www.tiktok.com/place/New-York-City-123456"], "maxItems": 100}'

# Save as CSV
node scripts/run_actor.js --actor "apidojo~tiktok-location-scraper" --input '{"startUrls": ["https://www.tiktok.com/place/New-York-City-123456"], "maxItems": 100}' --output results.csv --format csv

# Save as JSON
node scripts/run_actor.js --actor "apidojo~tiktok-location-scraper" --input '{"startUrls": ["https://www.tiktok.com/place/New-York-City-123456"], "maxItems": 100}' --output results.json --format json
```

### REST API fallback

```bash
curl -X POST "https://api.apify.com/v2/acts/apidojo~tiktok-location-scraper/runs" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"startUrls": ["https://www.tiktok.com/place/New-York-City-123456"], "maxItems": 100}'
```

If Apify MCP is available:
Use the Apify MCP `call_actor` tool with actor `apidojo~tiktok-location-scraper` and the input above.

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
| `bookmarks` | number | Bookmark/save count |
| `hashtags` | array | Hashtags used in post |
| `channel.name` | string | Creator display name |
| `channel.username` | string | Creator @username |
| `channel.verified` | boolean | Verification status |
| `uploadedAt` | number | Upload timestamp (Unix) |
| `uploadedAtFormatted` | string | Upload timestamp (ISO 8601) |
| `video.url` | string | Video file URL |
| `video.duration` | number | Duration in seconds |
| `song.title` | string | Audio track title |
| `postPage` | string | Full post URL |

## Edge Cases

- **No location URL**: This actor requires a TikTok location page URL, not a city name. Ask user to navigate to TikTok > search the location > copy the URL.
- **Low results**: Some locations have few tagged posts — return what's available.
- **Private videos**: Excluded automatically.
- **Deleted location**: Returns empty. URL may be stale.
