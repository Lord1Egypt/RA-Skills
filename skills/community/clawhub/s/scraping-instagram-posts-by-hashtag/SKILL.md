---
name: scraping-instagram-posts-by-hashtag
description: >
  Scrapes Instagram posts for any hashtag using apidojo's Instagram scraper on Apify.
  Triggers when the user asks to: get Instagram posts for a hashtag, scrape Instagram
  content by tag, export Instagram post data for a keyword or topic, fetch posts under
  an Instagram challenge or trend, collect Instagram media for a specific tag, or
  download Instagram post metadata by hashtag. Returns post URL, caption, like count,
  comment count, author handle, and timestamp per post.
  Ideal for trend analysts, UGC collectors, and social media researchers.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/instagram-hashtag-scraper
---

# Scraping Instagram Posts by Hashtag

Raw Instagram post dataset for any hashtag. Returns post-level metadata including engagement and author info.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | Optional | `[]` | Instagram hashtag search URLs |
| `keyword` | string | Optional | — | Hashtag keyword to search (e.g. `fitness`) |
| `getReels` | boolean | Optional | `false` | Include Reels in results |
| `getPosts` | boolean | Optional | `true` | Include regular posts in results |
| `until` | string | Optional | — | Date filter (YYYY-MM-DD) |
| `maxItems` | number | Optional | Unlimited | Maximum posts to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## Workflow

```
Progress:
- [ ] Step 1: Normalize hashtag input
- [ ] Step 2: Run instagram-scraper
- [ ] Step 3: Poll for SUCCEEDED
- [ ] Step 4: Deliver post dataset
```

### Step 2: Run the Actor


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~instagram-hashtag-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~instagram-hashtag-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~instagram-hashtag-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~instagram-hashtag-scraper"
Input:
{
  "keywords": ["tag1", "tag2"],
  "maxItems": 100,
  "mediaType": "all"
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~instagram-hashtag-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"keywords": ["tag1"], "maxItems": 100}'
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

- **Banned hashtag**: Instagram hides some hashtags — returns 0. Try parent category.
- **Only top posts returned**: Instagram limits hashtag feeds; very popular tags may return only top posts.
- **Private account posts**: Post metadata visible but media URL may be restricted.

## Output Format

```
# Instagram Post Dataset: #<hashtag>
Posts collected: N | Media type: all/image/video

| Post ID | Author | Caption (truncated) | Likes | Comments | Type | Timestamp |
|---------|--------|---------------------|-------|----------|------|-----------|
| ...     | ...    | ...                 | ...   | ...      | ...  | ...       |

Available fields: id, ownerUsername, caption, likesCount, commentsCount, type,
timestamp, url, mediaUrl, hashtags, mentions
```

## Troubleshooting

**0 results:** Hashtag may be banned or restricted by Instagram.
**Rate limiting:** Keep `maxItems` ≤ 200 per run; space runs 5 minutes apart.