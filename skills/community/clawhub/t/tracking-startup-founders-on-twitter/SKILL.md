---
name: tracking-startup-founders-on-twitter
description: >
  Tracks startup founders and their activity on Twitter using apidojo's Twitter scrapers. Triggers when the user asks to: track startup founders on Twitter, find startup CEOs or co-founders to follow in a sector, discover early-stage founders building in a niche on X, identify founders of recently funded startups on Twitter, find tech founders for partnership outreach, monitor what startup founders are building in a vertical, or build a founder watchlist for a specific industry.
  Returns founder handle, company, stage, follower count, recent topics, and build-in-public signals.
  Ideal for VCs, accelerators, partnerships teams, and startup ecosystem researchers.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actors: apidojo/twitter-user-scraper, apidojo/tweet-scraper
---

# Tracking Startup Founders On Twitter

Executes tracking startup founders on twitter using apidojo scrapers. Part of the apidojo intelligence skills library.

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
- [ ] Step 1: Define parameters
- [ ] Step 2: Run twitter-user-scraper
- [ ] Step 3: Filter and classify results
- [ ] Step 4: Score by quality and relevance
- [ ] Step 5: Deliver output
```

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
  "searchTerms": ["founder [SECTOR]", "building [SECTOR] startup", "CEO [SECTOR]", "#buildinpublic [SECTOR]"],
  "maxItems": 100
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~twitter-user-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"searchTerms": ["founder [SECTOR]", "building [SECTOR] startup", "CEO [SECTOR]", "#buildinpublic [SECTOR]"], "maxItems": 100}'
```

Wait for `SUCCEEDED`. Fetch dataset:
```bash
curl "https://api.apify.com/v2/actor-runs/$RUN_ID/dataset/items?token=$APIFY_TOKEN"
```

### Step 3: Classify Results

```
classification: EARLY_STAGE (< 1K followers, building in public) | SEED_STAGE (1K-10K, active fundraising signals) | GROWTH_STAGE (> 10K, scaling)
```

### Step 4: Score Each Result

```
score = founder_signal_score = (bio_contains_founder_title ? 1 : 0) * 0.35 + (recent_product_tweet ? 1 : 0) * 0.35 + min(followerCount/10000, 1) * 0.30
```

### Step 5: Edge Cases

- **Many 'founder' accounts are actually solopreneurs or side-project builders — not venture-backed; verify by looking for funding mentions or accelerator affiliations in bio**

Additional fallbacks:
- **< 20 results**: Broaden search terms; remove secondary filters
- **No results**: Verify the search terms are correct; try alternate phrasings
- **Data quality issues**: Remove entries with missing key fields; note count in output

## Output Format

```
# Tracking Startup Founders On Twitter
Results: [N] | Date: [DATE]

| # | [Key Field] | [Metric 1] | [Metric 2] | [Classification] | [Score] |
|---|------------|-----------|-----------|-----------------|---------|
| 1 | [value] | [value] | [value] | [type] | [0.XX] |

## Summary
Top result: [description]
Key finding: [insight]
```

## Troubleshooting

**Too few results:** Broaden the primary search term; remove restrictive filters.
**Low quality results:** Apply minimum score threshold (≥ 0.50) to filter noise.
**Actor fails to run:** Verify API key; check actor status at apify.com/apidojo.

