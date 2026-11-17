---
name: scraping-instagram-location-posts
description: >
  Scrapes Instagram posts tagged at a specific location or place using apidojo's Instagram
  Location scraper on Apify. Triggers when the user asks to: get Instagram posts from a
  location, scrape photos tagged at a restaurant or hotel, fetch Instagram content from
  an event or venue, collect posts from a geographic area on Instagram, export location-
  tagged Instagram media, or find what people post from a specific place on Instagram.
  Returns post URL, author handle, caption, likes, comments, and timestamp per post.
  Ideal for hospitality brands, event teams, and UGC content collectors.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/instagram-location-scraper
---

# Scraping Instagram Location Posts

Exports Instagram posts tagged at any physical location. Uses Instagram's location ID or place name to collect geo-tagged content.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | Optional | `[]` | Instagram location page URLs |
| `locationIds` | array | Optional | `[]` | Instagram location IDs |
| `maxItems` | number | Optional | Unlimited | Maximum posts to return |
| `until` | string | Optional | — | Date filter (YYYY-MM-DD) |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## Workflow

```
Progress:
- [ ] Step 1: Resolve location ID
- [ ] Step 2: Run instagram-location-scraper
- [ ] Step 3: Poll for SUCCEEDED
- [ ] Step 4: Deliver post dataset
```

### Step 2: Run the Actor


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~instagram-location-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~instagram-location-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~instagram-location-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~instagram-location-scraper"
Input:
{
  "locationIds": ["<LOCATION_ID>"],
  "maxItems": 100
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~instagram-location-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"locationIds": ["<LOCATION_ID>"], "maxItems": 100}'
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

- **Location ID not found**: Invalid ID or location removed from Instagram — report to user.
- **Low post volume**: Niche locations may have < 20 posts — return all available.
- **Private account posts in feed**: Metadata visible but media may be restricted.

## Output Format

```
# Instagram Location Posts: <location name>
Location ID: <id> | Posts collected: N

| Post ID | Author | Caption (truncated) | Likes | Comments | Type | Timestamp |
|---------|--------|---------------------|-------|----------|------|-----------|
| ...     | ...    | ...                 | ...   | ...      | ...  | ...       |
```

## Troubleshooting

**Don't have the Location ID:** Visit `https://www.instagram.com/explore/locations/` and search — the ID is in the URL.
**0 results:** Location may have been renamed or merged — search for new ID.