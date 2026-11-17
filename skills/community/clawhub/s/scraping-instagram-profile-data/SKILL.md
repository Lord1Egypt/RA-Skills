---
name: scraping-instagram-profile-data
description: >
  Scrapes Instagram profile statistics and recent posts for any list of accounts using
  apidojo's Instagram scraper on Apify. Triggers when the user asks to: get Instagram
  profile data for an account, fetch follower count and post count for Instagram users,
  scrape Instagram bio and stats in bulk, export Instagram account metadata, check
  profile information for a list of Instagram handles, or get engagement data from
  Instagram profiles. Returns username, follower count, following count, post count,
  bio, and recent post metrics.
  Ideal for influencer vetting, brand research, and list enrichment.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/instagram-scraper
---

# Scraping Instagram Profile Data

Bulk profile export for any set of Instagram usernames. Returns account-level stats and optional recent post data.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | ✅ | `[]` | Instagram URLs — profiles, hashtags, locations, audio pages, reels |
| `until` | string | Optional | — | Scrape posts until this date (YYYY-MM-DD) |
| `maxItems` | number | Optional | Unlimited | Maximum posts to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## Workflow

```
Progress:
- [ ] Step 1: Normalize username list
- [ ] Step 2: Run instagram-scraper
- [ ] Step 3: Poll for SUCCEEDED
- [ ] Step 4: Deliver profile dataset
```

### Step 2: Run the Actor


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~instagram-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~instagram-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~instagram-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~instagram-scraper"
Input:
{
  "usernames": ["handle1", "handle2"],
  "includeRecentPosts": false
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~instagram-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"usernames": ["handle1", "handle2"]}'
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

- **Private accounts**: Returns profile stats but no posts — flag `isPrivate: true`.
- **Account not found**: Handle may be renamed or deactivated — note in output.
- **Business vs personal accounts**: Business accounts expose contact info; personal accounts do not.

## Output Format

```
# Instagram Profile Dataset
Accounts requested: N | Returned: N | Private: N | Not found: N

| Username | Followers | Following | Posts | Bio (truncated) | Business | Verified |
|----------|-----------|-----------|-------|-----------------|----------|----------|
| ...      | ...       | ...       | ...   | ...             | ...      | ...      |

Available fields: username, fullName, followersCount, followingCount, postsCount,
biography, isVerified, isBusinessAccount, businessCategory, externalUrl, profilePicUrl
```

## Troubleshooting

**Missing accounts:** Username changed or account deactivated since list was compiled.
**No engagement data:** Engagement is per-post; use `includeRecentPosts: true` for post-level data.