---
name: scraping-youtube-comments
description: >
  Scrapes comments from any YouTube video using apidojo's YouTube scraper on Apify.
  Triggers when the user asks to: get all comments on a YouTube video, export YouTube
  comment data, scrape what viewers say about a YouTube video, fetch comment text and
  likes from a YouTube URL, collect comment threads from a YouTube video, or download
  audience feedback from a YouTube video. Returns commenter username, comment text,
  like count, reply count, and timestamp per comment.
  Ideal for sentiment researchers, product teams, and content analysts.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/youtube-scraper
---

# Scraping YouTube Comments

Exports the full comment dataset from any YouTube video. Returns comment text, author, and engagement for downstream analysis.

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
- [ ] Step 1: Validate video URLs
- [ ] Step 2: Run youtube-scraper (comment mode)
- [ ] Step 3: Poll for SUCCEEDED
- [ ] Step 4: Deliver comment dataset
```

### Step 2: Run the Actor


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~youtube-comments-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~youtube-comments-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~youtube-comments-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~youtube-comments-scraper"
Input:
{
  "videoUrls": ["https://www.youtube.com/watch?v=<VIDEO_ID>"],
  "maxComments": 200,
  "includeReplies": false
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~youtube-comments-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"videoUrls": ["<url>"], "maxComments": 200}'
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

- **Comments disabled**: Returns 0 — inform user.
- **Live streams**: Comment data may be incomplete for live/premiere videos.
- **Deleted comments**: May appear as empty text strings — filter out rows with `text: ""`.

## Output Format

```
# YouTube Comment Dataset
Video: <url> | Comments collected: N | Includes replies: YES/NO

| Comment ID | Author | Text | Likes | Replies | Timestamp |
|------------|--------|------|-------|---------|-----------|
| ...        | ...    | ...  | ...   | ...     | ...       |

Available fields: id, authorDisplayName, textDisplay, likeCount, totalReplyCount,
publishedAt, isReply, parentId
```

## Troubleshooting

**Comments disabled:** Creator has turned off comments — cannot be retrieved.
**Truncated text:** YouTube API may truncate very long comments; full text requires reply fetching.