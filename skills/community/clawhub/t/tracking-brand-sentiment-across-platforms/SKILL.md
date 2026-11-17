---
name: tracking-brand-sentiment-across-platforms
description: >
  Tracks brand sentiment across Twitter Reddit and TikTok simultaneously using apidojo's scrapers
  on Apify. Triggers when the user asks to: monitor brand reputation across social platforms,
  track how people talk about a brand on multiple channels, compare brand sentiment on Twitter
  vs Reddit vs TikTok, get a cross-platform brand health score, monitor a product launch reaction
  across social media, measure overall public sentiment for a brand, or build a multi-platform
  social listening dashboard for a brand.
  Returns per-platform sentiment distribution, cross-platform score, top positive/negative posts, and theme analysis.
  Ideal for brand managers, CMOs, PR teams, and reputation management agencies.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actors: apidojo/tweet-scraper, apidojo/tweet-scraper, apidojo/tiktok-scraper
---

# Tracking Brand Sentiment Across Platforms

Monitors brand sentiment on Twitter, Reddit, and TikTok in parallel, then produces a unified brand health score. Each platform serves a different role: Twitter = real-time news/opinion, Reddit = deep community discussion, TikTok = Gen Z product culture.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `searchTerms` | array | ✅ | `[]` | Twitter advanced search queries (e.g. `["#AI lang:en", "from:NASA"]`) |
| `sort` | string | Optional | `Top` | Sort order: `Latest`, `Top`, or `Latest+Top` |
| `tweetLanguage` | string | Optional | — | ISO 639-1 language code (e.g. `en`) |
| `maxItems` | number | Optional | Unlimited | Maximum tweets to return |
| `onlyVerifiedUsers` | boolean | Optional | `false` | Only tweets from verified users |
| `onlyTwitterBlue` | boolean | Optional | `false` | Only Twitter Blue subscribers |
| `onlyImage` | boolean | Optional | `false` | Only tweets with images |
| `onlyVideo` | boolean | Optional | `false` | Only tweets with videos |
| `onlyQuote` | boolean | Optional | `false` | Only quote tweets |
| `author` | string | Optional | — | Filter to a specific author handle |
| `inReplyTo` | string | Optional | — | Tweets replying to a specific handle |
| `mentioning` | string | Optional | — | Tweets mentioning a specific handle |
| `geotaggedNear` | string | Optional | — | Tweets near a location |
| `withinRadius` | string | Optional | — | Radius around geotaggedNear |
| `geocode` | string | Optional | — | Lat/lng + radius string |
| `placeObjectId` | string | Optional | — | Tweets tagged with a place |
| `minimumRetweets` | number | Optional | — | Minimum retweet count |
| `minimumFavorites` | number | Optional | — | Minimum like count |
| `minimumReplies` | number | Optional | — | Minimum reply count |
| `start` | string | Optional | — | Tweets after this date (YYYY-MM-DD) |
| `end` | string | Optional | — | Tweets before this date (YYYY-MM-DD) |
| `includeSearchTerms` | boolean | Optional | `false` | Add the matched search term to each tweet |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## Workflow

```
Progress:
- [ ] Step 1: Run scrapers for all three platforms in parallel
- [ ] Step 2: Classify sentiment per platform
- [ ] Step 3: Calculate cross-platform brand health score
- [ ] Step 4: Identify top themes and alerts
- [ ] Step 5: Deliver unified report
```

### Step 1: Run Three Scrapers

**Twitter (If Apify MCP is available):**
```
Tool: apify:run-actor
Actor: "apidojo~tweet-scraper"
Input: {"searchTerms": ["[BRAND_NAME]"], "maxItems": 300, "tweetLanguage": "en"}
```

**Reddit:**
```
Tool: apify:run-actor
Actor: "apidojo~tweet-scraper"
Input: {"searches": ["[BRAND_NAME]"], "maxItems": 200, "sort": "new", "time": "month"}
```

**TikTok:**
```
Tool: apify:run-actor
Actor: "apidojo~tiktok-scraper"
Input: {"keywords": ["#[brandname]", "#[brandname]review"], "maxItems": 200}
```

**REST API fallback — run each sequentially:**
```bash
# Twitter
curl -X POST "https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs?token=$APIFY_TOKEN"   -H "Content-Type: application/json"   -d '{"searchTerms": ["[BRAND_NAME]"], "maxItems": 300}'

# Reddit
curl -X POST "https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs?token=$APIFY_TOKEN"   -H "Content-Type: application/json"   -d '{"searches": ["[BRAND_NAME]"], "maxItems": 200, "sort": "new", "time": "month"}'
```

### Step 2: Sentiment Classification

Use the same lexical model for all platforms (positive/negative/neutral indicators from `analyzing-twitter-sentiment-for-topic` skill). Weight by platform-specific engagement:
- Twitter: `likeCount + replyCount * 3`
- Reddit: `upvotes + commentCount * 2`
- TikTok: `playCount / 1000 + diggCount`

### Step 3: Brand Health Score

```
platform_sentiment[p] = (positive_count[p] - negative_count[p]) / total_count[p]  # range: -1 to +1

platform_weight = {twitter: 0.35, reddit: 0.40, tiktok: 0.25}  # Reddit = most considered opinion

brand_health_score = sum(platform_sentiment[p] * platform_weight[p] for p in platforms)
brand_health_score = (brand_health_score + 1) / 2 * 100  # normalize to 0-100
```

**Score interpretation:** 0–40 = Crisis, 40–55 = Concerning, 55–70 = Neutral, 70–85 = Positive, 85–100 = Strong.

### Step 4: Edge Cases

- **Brand name is a common word** (e.g. "Apple"): Add qualifier ("Apple iPhone", "Apple Inc") to search to reduce noise; report disambiguation rate
- **One platform dominates volume** (e.g. TikTok has 10× Twitter posts): Weight by volume in the composite score
- **Rapid sentiment shift** (score changes > 20 points): Flag as `ALERT` — may indicate PR crisis or viral positive moment
- **Reddit returns no results**: Brand may not be discussed there; set `reddit_weight = 0` and redistribute to other platforms

## Output Format

```
# Cross-Platform Brand Sentiment: [BRAND_NAME]
Period: [DATE_RANGE] | Total posts: [N] | Date: [DATE]

## Brand Health Score: [X]/100 — [INTERPRETATION]

## Per-Platform Breakdown
| Platform | Posts | Positive | Negative | Neutral | Score |
|----------|-------|----------|----------|---------|-------|
| Twitter | [N] | [X%] | [X%] | [X%] | [+/-X] |
| Reddit | [N] | [X%] | [X%] | [X%] | [+/-X] |
| TikTok | [N] | [X%] | [X%] | [X%] | [+/-X] |

## Top Negative Themes (Cross-Platform)
1. [Theme] — [N] posts across [platforms]
2. [Theme]

## Top Positive Themes
1. [Theme] — [N] posts
2. [Theme]

## Most Impactful Posts
🔴 Top negative: [platform] | [handle] | [N engagement] | "[excerpt]"
🟢 Top positive: [platform] | [handle] | [N engagement] | "[excerpt]"
```

## Troubleshooting

**Brand health score conflicts between platforms**: This is meaningful signal — discuss in output why platforms diverge (e.g. "Reddit community discusses product quality issues while TikTok shows positive unboxing content").
**Sample too small for reliable sentiment** (< 50 posts per platform): Widen date range or note low confidence in that platform's score.
**Brand name not found on a platform**: Some brands have no organic TikTok presence — note as gap in output.



**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~tweet-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~tweet-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~tweet-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

