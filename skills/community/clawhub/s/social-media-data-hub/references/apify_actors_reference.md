# Apify Actor Quick Reference

## Actor Mapping

| Platform | Actor ID | BRONZE Pricing |
|------|----------|---------------|
| TikTok | `clockworks/tiktok-scraper` | $0.003 per item, $0.50 minimum per run |
| Instagram | `apify/instagram-scraper` | $0.0023 per item |
| X/Twitter bulk | `apidojo/tweet-scraper` | $0.0004 per item for batches of 50+ |
| X/Twitter precise | `apidojo/twitter-scraper-lite` | $0.016 per query + $0.0004 per item |
| YouTube | `streamers/youtube-scraper` | $0.003 per item |

## API Call Pattern

```text
POST https://api.apify.com/v2/acts/{actorId}/runs?token={APIFY_TOKEN}
Content-Type: application/json
Body: {input parameters}

# Fetch dataset items
GET https://api.apify.com/v2/datasets/{datasetId}/items?format=json&token={APIFY_TOKEN}
```

## TikTok Key Inputs

| Mode | Parameters | Example |
|------|------|------|
| User videos | `profiles` + `resultsPerPage` | `{"profiles": ["username"], "resultsPerPage": 20}` |
| Video URL | `postURLs` | `{"postURLs": ["https://..."]}` |
| Search | `searchQueries` | `{"searchQueries": ["keyword"]}` |
| Comments | `commentsPerPost` (additional) | `{"postURLs": [...], "commentsPerPost": 50}` |

Sorting: `profileSorting`: `latest` / `popular` / `oldest`

## Instagram Key Inputs

| Mode | Parameters | Example |
|------|------|------|
| Posts | `directUrls` + `resultsType:"posts"` | `{"directUrls": ["https://instagram.com/user/"], "resultsType": "posts"}` |
| Profile details | `resultsType:"details"` | `{"directUrls": [...], "resultsType": "details"}` |
| Comments | `resultsType:"comments"` | `{"directUrls": ["https://instagram.com/p/xxx/"], "resultsType": "comments"}` |
| Reels | `resultsType:"reels"` | `{"directUrls": [...], "resultsType": "reels"}` |

Limits: comments are capped at 50 per post, search up to 250 items

## X/Twitter Key Inputs

**V2 bulk actor (50+ items):**

| Mode | Parameters | Example |
|------|------|------|
| User tweets | `twitterHandles` | `{"twitterHandles": ["username"], "maxItems": 100}` |
| Search | `searchTerms` | `{"searchTerms": ["from:user since:2024-01-01"]}` |

**Unlimited actor (precise, any quantity):**

| Mode | Parameters | Example |
|------|------|------|
| Single tweet | `startUrls` | `{"startUrls": [{"url": "https://x.com/.../status/xxx"}]}` |
| Conversation replies | `searchTerms` | `{"searchTerms": ["conversation_id:xxx"]}` |
| Small batch | `twitterHandles` | `{"twitterHandles": ["user"], "maxItems": 10}` |

Selection rule: use V2 for 50 or more items ($0.40 per 1K), and Unlimited for single-item or sub-50 retrievals ($0.05 per query)

## YouTube Key Inputs

| Mode | Parameters | Example |
|------|------|------|
| Channel videos | `startUrls` + `maxResults` | `{"startUrls": [{"url": "https://youtube.com/@channel"}], "maxResults": 50}` |
| Search | `searchQueries` | `{"searchQueries": ["keyword"], "maxResults": 20}` |
| Single video | `startUrls` | `{"startUrls": [{"url": "https://youtube.com/watch?v=xxx"}]}` |

Sorting: `sortVideosBy`: `NEWEST` / `POPULAR` / `OLDEST`

## Unified Field Mapping

| Unified Field | TikTok | Instagram | X/Twitter | YouTube |
|---------|--------|-----------|---------|---------|
| `likes` | `diggCount` | `likesCount` | `likeCount` | `likes` |
| `comments` | `commentCount` | `commentsCount` | `replyCount` | `commentsCount` |
| `shares` | `shareCount` | `null` | `retweetCount` | `null` |
| `views` | `playCount` | `null` | `null` | `viewCount` |
| `saves` | `collectCount` | `null` | `bookmarkCount` | `null` |
| `author` | `authorMeta.name` | `ownerUsername` | `author.userName` | `channelName` |
| `date` | `createTimeISO` | `timestamp` | `createdAt` | `date` |

## Cost Snapshot (BRONZE, 10 accounts x 100 items per account)

| Platform | Monthly Cost |
|------|--------|
| TikTok | ~$3.00 |
| Instagram | ~$2.30 |
| X/Twitter (V2) | ~$0.40 |
| YouTube | ~$3.00 |
| **Total** | **~$8.70** |
