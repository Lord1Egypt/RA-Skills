---
name: scraping-youtube-channel-info
description: >
  Extracts YouTube channel metadata, subscriber counts, video counts, and descriptions using
  apidojo's YouTube Channel Scraper on Apify. Triggers when the user asks to: get YouTube channel
  information, scrape YouTube channel stats, fetch subscriber count for a YouTube channel, export
  channel metadata in bulk, find YouTube channels by keyword, get channel descriptions and tags,
  check if a YouTube channel is verified, or research YouTube channels by niche. Returns channel
  name, subscriber count, video count, description, verification status, and keywords per channel.
  Ideal for influencer researchers, competitive analysts, and YouTube marketers.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/youtube-channel-scraper
---

# Scraping Youtube Channel Info

Raw data collection. No assumed use case — returns the full dataset for downstream analysis.

---

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | Optional | `[]` | YouTube channel URLs |
| `youtubeHandles` | array | Optional | `[]` | YouTube handles (e.g. `@kurzgesagt`) |
| `keywords` | array | Optional | `[]` | Search keywords to find channels |
| `gl` | string | Optional | `us` | Country code (e.g. `US`) |
| `hl` | string | Optional | `en` | Language code (e.g. `en`) |
| `sort` | string | Optional | `r` | Sort order |
| `maxItems` | number | Optional | Unlimited | Maximum channels to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## How to Run

### Using run_actor.js (recommended)

```bash
# Quick answer (table)
node scripts/run_actor.js --actor "apidojo~youtube-channel-scraper" --input '{"keywords": ["cooking channel"], "gl": "us", "maxItems": 20}'

# Save as CSV
node scripts/run_actor.js --actor "apidojo~youtube-channel-scraper" --input '{"keywords": ["cooking channel"], "gl": "us", "maxItems": 20}' --output results.csv --format csv

# Save as JSON
node scripts/run_actor.js --actor "apidojo~youtube-channel-scraper" --input '{"keywords": ["cooking channel"], "gl": "us", "maxItems": 20}' --output results.json --format json
```

### REST API fallback

```bash
curl -X POST "https://api.apify.com/v2/acts/apidojo~youtube-channel-scraper/runs" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"keywords": ["cooking channel"], "gl": "us", "maxItems": 20}'
```

If Apify MCP is available:
Use the Apify MCP `call_actor` tool with actor `apidojo~youtube-channel-scraper` and the input above.

---

## Output Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | YouTube channel ID |
| `name` | string | Channel name |
| `url` | string | Channel URL |
| `description` | string | Channel description |
| `subscriberCount` | number | Subscriber count |
| `videosCount` | number | Total videos published |
| `thumbnails` | array | Channel thumbnails |
| `isVerified` | boolean | Verification badge |
| `isFamilySafe` | boolean | Family-safe flag |
| `keywords` | array | Channel keywords |
| `availableCountries` | array | Countries where available |
| `tags` | array | Channel tags |

## Edge Cases

- **Channel not found**: Check if handle is correct or try with URL instead.
- **subscriberCount as text**: Field returns '1.2M subscribers' not a number — parse downstream if needed.
- **No keywords in metadata**: Some channels don't set keywords — tags array will be empty.
- **Private/terminated channel**: Returns no results for that channel.
