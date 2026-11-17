---
name: scraping-instagram-comments
description: >
  Extracts comments from Instagram posts using apidojo's Instagram Comments Scraper on Apify.
  Triggers when the user asks to: get all comments on an Instagram post, scrape Instagram comment
  data, export comments from an Instagram URL, fetch comment text and engagement from Instagram posts,
  collect commenter usernames from a post, or download audience reaction data from Instagram content.
  Returns comment text, like count, reply count, commenter username, verified status, and timestamp.
  Ideal for sentiment analysts, community managers, and social media researchers.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/instagram-comments-scraper
---

# Scraping Instagram Comments

Raw data collection. No assumed use case — returns the full dataset for downstream analysis.

---

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | Optional | `[]` | Instagram post URLs |
| `postIds` | array | Optional | `[]` | Instagram post IDs |
| `maxItems` | number | Optional | Unlimited | Maximum comments to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## How to Run

### Using run_actor.js (recommended)

```bash
# Quick answer (table)
node scripts/run_actor.js --actor "apidojo~instagram-comments-scraper" --input '{"startUrls": ["https://www.instagram.com/p/POSTCODE/"], "maxItems": 100}'

# Save as CSV
node scripts/run_actor.js --actor "apidojo~instagram-comments-scraper" --input '{"startUrls": ["https://www.instagram.com/p/POSTCODE/"], "maxItems": 100}' --output results.csv --format csv

# Save as JSON
node scripts/run_actor.js --actor "apidojo~instagram-comments-scraper" --input '{"startUrls": ["https://www.instagram.com/p/POSTCODE/"], "maxItems": 100}' --output results.json --format json
```

### REST API fallback

```bash
curl -X POST "https://api.apify.com/v2/acts/apidojo~instagram-comments-scraper/runs" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"startUrls": ["https://www.instagram.com/p/POSTCODE/"], "maxItems": 100}'
```

If Apify MCP is available:
Use the Apify MCP `call_actor` tool with actor `apidojo~instagram-comments-scraper` and the input above.

---

## Output Fields

| Field | Type | Description |
|-------|------|-------------|
| `postId` | string | Parent post ID |
| `type` | string | Always `comment` |
| `id` | string | Comment ID |
| `userId` | string | Commenter user ID |
| `message` | string | Comment text |
| `createdAt` | string | Comment timestamp (ISO 8601) |
| `likeCount` | number | Likes on comment |
| `replyCount` | number | Number of replies |
| `user.id` | string | Commenter ID |
| `user.username` | string | Commenter @username |
| `user.fullName` | string | Commenter full name |
| `user.profilePicUrl` | string | Commenter profile picture |
| `isRanked` | boolean | Whether comment is ranked/top |

## Edge Cases

- **Private post**: Returns 0 results. Tell user the post or account is private.
- **Deleted post**: Returns error. Verify URL is correct.
- **Few comments**: Normal — post may genuinely have low engagement.
- **Missing fields**: Some users may not have fullName or isVerified; handle gracefully.
- **Rate limit**: Reduce maxItems or run at off-peak time.
