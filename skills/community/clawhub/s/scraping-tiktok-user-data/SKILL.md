---
name: scraping-tiktok-user-data
description: >
  Scrapes detailed TikTok user data and recent video history using apidojo's TikTok User
  scraper on Apify. Triggers when the user asks to: get all videos from a TikTok account,
  fetch a TikTok creator's recent posts and stats, export a TikTok user's video history,
  scrape all TikTok content from a specific creator, get TikTok post data by username,
  or collect video-level metrics from a TikTok profile. Returns per-video view count,
  likes, comments, shares, captions, and timestamps for a given account.
  Ideal for creator analysis, content auditing, and competitive benchmarking.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/tiktok-user-scraper
---

# Scraping TikTok User Data

Exports a creator's full video history with per-video engagement metrics. Complements `scraping-tiktok-profile-data` (account-level) with video-level detail.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | ✅ | `[]` | TikTok profile URLs or video URLs (extracts author from videos) |
| `getFollowers` | boolean | Optional | `false` | Also extract complete follower lists |
| `getFollowing` | boolean | Optional | `false` | Also extract complete following lists |
| `maxItems` | number | Optional | Unlimited | Maximum users to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## Workflow

```
Progress:
- [ ] Step 1: Run tiktok-user-scraper
- [ ] Step 2: Poll for SUCCEEDED
- [ ] Step 3: Deliver video dataset
```

### Step 1: Run the Actor


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~tiktok-user-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~tiktok-user-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~tiktok-user-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~tiktok-user-scraper"
Input:
{
  "username": "<handle>",
  "maxVideos": 50
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~tiktok-user-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username": "<handle>", "maxVideos": 50}'
```

Save `id` as `RUN_ID`. Poll until `status = SUCCEEDED`:
```bash
curl "https://api.apify.com/v2/actor-runs/$RUN_ID?token=$APIFY_TOKEN" | grep '"status"'
```

Fetch results:
```bash
curl "https://api.apify.com/v2/actor-runs/$RUN_ID/dataset/items?token=$APIFY_TOKEN&format=json"
```

### Step 2: Handle Edge Cases

- **Private account**: Returns 0 videos. Inform user.
- **Account with < requested videos**: Return all available; note count in output.
- **Deleted videos in feed**: Skip entries with missing `playCount` fields.

## Output Format

```
# TikTok Video History: @<username>
Videos collected: N

| Video ID | Caption (truncated) | Views | Likes | Comments | Shares | Duration | Posted |
|----------|---------------------|-------|-------|----------|--------|----------|--------|
| ...      | ...                 | ...   | ...   | ...      | ...    | ...      | ...    |

Available fields: videoId, desc, playCount, diggCount, commentCount, shareCount,
duration, createTime, videoUrl, musicTitle, hashtags
```

## Troubleshooting

**0 videos returned:** Account is private or username incorrect.
**Pay-per-result billing:** This actor uses pay-per-result pricing — set `maxVideos` to control cost.