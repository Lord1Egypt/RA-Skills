---
name: scraping-instagram-users-by-keyword
description: >
  Extracts Instagram user profiles, followers, and following lists using apidojo's Instagram
  User Scraper on Apify. Triggers when the user asks to: find Instagram users by keyword or name,
  get follower lists for Instagram accounts, get following lists for Instagram accounts, export
  Instagram profile data in bulk, fetch public email addresses from Instagram business profiles,
  search for Instagram users by username or handle, or build a dataset of Instagram account metadata.
  Returns username, follower count, bio, post count, verification status, public email, and more.
  Ideal for influencer researchers, outreach teams, and competitive intelligence analysts.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/instagram-user-scraper
---

# Scraping Instagram Users By Keyword

Raw data collection. No assumed use case — returns the full dataset for downstream analysis.

---

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `keywords` | array | Optional | `[]` | Keywords to search for users |
| `handles` | array | Optional | `[]` | Instagram usernames (without @) |
| `startUrls` | array | Optional | `[]` | Instagram profile URLs |
| `userIds` | array | Optional | `[]` | Instagram user IDs |
| `getFollowers` | boolean | Optional | `false` | Extract follower lists for each profile |
| `getFollowings` | boolean | Optional | `false` | Extract following lists for each profile |
| `maxItems` | number | Optional | Unlimited | Maximum users to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## How to Run

### Using run_actor.js (recommended)

```bash
# Quick answer (table)
node scripts/run_actor.js --actor "apidojo~instagram-user-scraper" --input '{"handles": ["natgeo"], "getFollowers": false, "maxItems": 50}'

# Save as CSV
node scripts/run_actor.js --actor "apidojo~instagram-user-scraper" --input '{"handles": ["natgeo"], "getFollowers": false, "maxItems": 50}' --output results.csv --format csv

# Save as JSON
node scripts/run_actor.js --actor "apidojo~instagram-user-scraper" --input '{"handles": ["natgeo"], "getFollowers": false, "maxItems": 50}' --output results.json --format json
```

### REST API fallback

```bash
curl -X POST "https://api.apify.com/v2/acts/apidojo~instagram-user-scraper/runs" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"handles": ["natgeo"], "getFollowers": false, "maxItems": 50}'
```

If Apify MCP is available:
Use the Apify MCP `call_actor` tool with actor `apidojo~instagram-user-scraper` and the input above.

---

## Output Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Instagram user ID |
| `username` | string | @username |
| `fullName` | string | Display name |
| `biography` | string | Profile bio text |
| `externalUrl` | string | Link in bio (website) |
| `followerCount` | number | Follower count |
| `followingCount` | number | Following count |
| `postCount` | number | Total posts |
| `isVerified` | boolean | Verification status |
| `isBusinessAccount` | boolean | Business account flag |
| `businessCategoryName` | string | Business category |
| `profilePicUrl` | string | Profile picture URL |
| `profilePicUrlHd` | string | High-resolution profile picture URL |
| `isPrivate` | boolean | Private account flag |
| `publicEmail` | string | Public email (if available) |
| `publicPhoneNumber` | string | Public phone (if available) |
| `contactPhoneNumber` | string | Contact phone (if available) |

## Edge Cases

- **Private account**: Returns profile metadata but no followers/following.
- **No public email**: publicEmail field absent — normal for personal accounts.
- **Large follower list**: Set maxItems limit to avoid excessive cost.
- **Account not found**: Returns empty result. Check handle spelling.
- **Keyword returns many**: Use maxItems to cap results.
