---
name: scraping-twitter-profiles
description: >
  Scrapes Twitter/X profile data for any list of usernames using apidojo's Twitter User
  scraper on Apify. Triggers when the user asks to: get profile data for Twitter accounts,
  fetch follower counts for a list of usernames, scrape Twitter bio and stats for multiple
  users, export Twitter profile metadata, check account details for a set of handles,
  or bulk-fetch Twitter user information. Returns username, display name, bio, follower
  count, following count, tweet count, verified status, and profile URL.
  Ideal for data analysts, list enrichment pipelines, and market researchers.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/twitter-user-scraper
---

# Scraping Twitter Profiles

Bulk profile data export for any set of Twitter/X usernames. Returns account-level metadata: follower counts, bios, join dates, verification status.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | Optional | `[]` | Twitter profile or tweet URLs |
| `twitterHandles` | array | Optional | `[]` | Twitter usernames (without @) |
| `twitterUserIds` | array | Optional | `[]` | Twitter user IDs |
| `getFollowers` | boolean | Optional | `false` | Extract follower lists |
| `getFollowing` | boolean | Optional | `false` | Extract following lists |
| `getRetweeters` | boolean | Optional | `false` | Extract retweeters of a tweet URL |
| `includeUnavailableUsers` | boolean | Optional | `false` | Include unavailable/suspended users |
| `maxItems` | number | Optional | Unlimited | Maximum users to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## Workflow

```
Progress:
- [ ] Step 1: Normalize username list
- [ ] Step 2: Run twitter-user-scraper
- [ ] Step 3: Poll for SUCCEEDED
- [ ] Step 4: Deliver profile dataset
```

### Step 1: Normalize

Remove `@` symbols, deduplicate, validate no empty strings.

### Step 2: Run the Actor


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~twitter-user-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~twitter-user-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~twitter-user-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~twitter-user-scraper"
Input:
{
  "usernames": ["handle1", "handle2", "handle3"]
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~twitter-user-scraper/runs?token=$APIFY_TOKEN" \
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

- **Missing accounts in results**: Account suspended, deleted, or handle changed. Note missing handles in output.
- **Private accounts**: Returns profile metadata but no tweet content — flag `isPrivate: true` rows.
- **Deactivated accounts**: Returns null or empty object — exclude from final dataset.

## Output Format

```
# Twitter Profile Dataset
Accounts requested: N | Accounts returned: N | Missing: N

| Username | Display Name | Followers | Following | Tweets | Verified | Bio (truncated) | Joined |
|----------|-------------|-----------|-----------|--------|----------|-----------------|--------|
| ...      | ...         | ...       | ...       | ...    | ...      | ...             | ...    |

Available fields: username, displayName, followersCount, followingCount, tweetCount,
isVerified, isBlueVerified, description, location, url, profileImageUrl, createdAt, isPrivate
```

## Troubleshooting

**Some handles missing from results:** Accounts may be suspended or renamed — cross-reference manually.
**Large lists (> 1000):** Break into batches of 500 and run sequentially.