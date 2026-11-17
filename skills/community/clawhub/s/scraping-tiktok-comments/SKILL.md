---
name: scraping-tiktok-comments
description: >
  Scrapes comments from any TikTok video using apidojo's TikTok Comments scraper on Apify.
  Triggers when the user asks to: get all comments on a TikTok video, export TikTok comment
  data, scrape what viewers are saying on a TikTok post, fetch comment text and likes from
  a TikTok URL, collect TikTok comment threads for analysis, or download comments from a
  viral TikTok video. Returns commenter username, comment text, like count, reply count,
  and timestamp per comment.
  Ideal for sentiment analysts, brand monitors, and content researchers.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/tiktok-comments-scraper
---

# Scraping TikTok Comments

Exports all comments from any TikTok video URL. Returns the raw comment dataset for sentiment analysis, community research, or product feedback extraction.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | ✅ | `[]` | TikTok video URLs to scrape comments from |
| `includeReplies` | boolean | Optional | `false` | Include reply comments (nested) |
| `maxItems` | number | Optional | Unlimited | Maximum comments to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## Workflow

```
Progress:
- [ ] Step 1: Validate video URLs
- [ ] Step 2: Run tiktok-comments-scraper
- [ ] Step 3: Poll for SUCCEEDED
- [ ] Step 4: Deliver comment dataset
```

### Step 2: Run the Actor


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~tiktok-comments-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~tiktok-comments-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~tiktok-comments-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~tiktok-comments-scraper"
Input:
{
  "videoUrls": ["https://www.tiktok.com/@user/video/123456"],
  "maxItems": 200,
  "includeReplies": false
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~tiktok-comments-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"videoUrls": ["<url>"], "maxItems": 200}'
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

- **0 comments**: Video may have comments disabled or be private. Report to user.
- **Video deleted or unavailable**: Actor returns error — remove URL from batch and notify.
- **Comment count less than expected**: TikTok filters spam comments server-side; this is expected.

## Output Format

```
# TikTok Comment Dataset
Video: <url> | Comments collected: N | Includes replies: YES/NO

| Comment ID | Author | Text | Likes | Replies | Timestamp |
|------------|--------|------|-------|---------|-----------|
| ...        | ...    | ...  | ...   | ...     | ...       |

Available fields: id, text, authorUsername, diggCount, replyCount, createTime,
isReply, parentCommentId
```

## Troubleshooting

**Comments disabled:** Creator has disabled comments — no workaround.
**Truncated comments:** Some comments may be cut off by TikTok's API; full text available via video page.