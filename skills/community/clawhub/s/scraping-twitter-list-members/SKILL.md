---
name: scraping-twitter-list-members
description: >
  Scrapes all members and their profile data from any public Twitter/X list using
  apidojo's Twitter List scraper on Apify. Triggers when the user asks to: get all
  members of a Twitter list, export accounts in a Twitter list, scrape profiles from
  a curated Twitter list, fetch the usernames in a public Twitter list, download data
  from a Twitter list URL, or collect profile stats for everyone on a list.
  Returns username, bio, follower count, and profile metadata for each list member.
  Ideal for competitive intelligence teams, curators, and list-based outreach pipelines.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/twitter-list-scraper
---

# Scraping Twitter List Members

Exports all member profiles from any public Twitter/X list. Useful for curated industry lists, competitor watchlists, or pre-built audiences.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | Optional | `[]` | Twitter list URLs (e.g. `https://x.com/i/lists/12345`) |
| `listIds` | array | Optional | `[]` | Twitter list IDs |
| `maxItems` | number | Optional | Unlimited | Maximum tweets to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## Workflow

```
Progress:
- [ ] Step 1: Validate list URL
- [ ] Step 2: Run twitter-list-scraper
- [ ] Step 3: Poll for SUCCEEDED
- [ ] Step 4: Deliver member dataset
```

### Step 2: Run the Actor


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~twitter-list-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~twitter-list-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~twitter-list-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~twitter-list-scraper"
Input:
{
  "listUrl": "https://twitter.com/i/lists/<LIST_ID>",
  "maxItems": 500
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~twitter-list-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"listUrl": "https://twitter.com/i/lists/<LIST_ID>"}'
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

- **Private list**: Actor returns 0 results — inform user the list is not publicly accessible.
- **List deleted or moved**: Validate URL returns 200 before running actor.
- **Very large lists (> 5000 members)**: May timeout — use `maxItems: 2000` and paginate.

## Output Format

```
# Twitter List Members: <list name>
List URL: <url> | Members collected: N

| Username | Display Name | Followers | Bio (truncated) | Location | Verified |
|----------|-------------|-----------|-----------------|----------|----------|
| ...      | ...         | ...       | ...             | ...      | ...      |
```

## Troubleshooting

**0 results:** List is private or URL is malformed. Verify the list is public.
**Partial results:** Large lists may be rate-limited — retry with smaller `maxItems`.