---
name: scraping-tiktok-profile-data
description: >
  Scrapes TikTok profile statistics and metadata for any list of accounts using apidojo's
  TikTok Profile scraper on Apify. Triggers when the user asks to: get TikTok profile stats
  for an account, fetch follower count and engagement data for TikTok users, scrape TikTok
  account metadata in bulk, export TikTok profile information for a list of creators, check
  TikTok stats for multiple usernames, or get bio and follower data from TikTok profiles.
  Returns username, follower count, following count, total likes, video count, and bio.
  Ideal for influencer vetting, data enrichment, and audience analysis.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/tiktok-profile-scraper
---

# Scraping TikTok Profile Data

Bulk account-level statistics for any set of TikTok usernames. Returns follower counts, engagement totals, bio, and video count.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | Optional | `[]` | TikTok profile URLs |
| `usernames` | array | Optional | `[]` | TikTok usernames (without @) |
| `since` | string | Optional | — | Return posts after this date (YYYY-MM-DD) |
| `until` | string | Optional | — | Return posts before this date (YYYY-MM-DD) |
| `maxItems` | number | Optional | Unlimited | Maximum posts to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## Workflow

```
Progress:
- [ ] Step 1: Normalize username list
- [ ] Step 2: Run tiktok-profile-scraper
- [ ] Step 3: Poll for SUCCEEDED
- [ ] Step 4: Deliver profile dataset
```

### Step 2: Run the Actor


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~tiktok-profile-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~tiktok-profile-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~tiktok-profile-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~tiktok-profile-scraper"
Input:
{
  "usernames": ["creator1", "creator2"]
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~tiktok-profile-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"usernames": ["creator1", "creator2"]}'
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

- **Account not found**: Username banned, deleted, or changed. Flag in output.
- **Private account**: Returns 0 video count with profile metadata — mark `isPrivate: true`.
- **Batch > 500**: Split into smaller batches for reliability.

## Output Format

```
# TikTok Profile Dataset
Accounts requested: N | Returned: N | Not found: N

| Username | Followers | Following | Total Likes | Videos | Bio (truncated) | Verified |
|----------|-----------|-----------|-------------|--------|-----------------|----------|
| ...      | ...       | ...       | ...         | ...    | ...             | ...      |

Available fields: username, nickname, followerCount, followingCount, heartCount,
videoCount, signature, verified, bioLink, avatarUrl
```

## Troubleshooting

**Missing accounts:** Username may have changed — verify on TikTok directly.
**Stale follower counts:** TikTok data may lag 24–48 hours; re-run for fresh data.