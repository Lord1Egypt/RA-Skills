---
name: verosight-monitor
description: "Integrate Verosight API for social media intelligence and cyber monitoring. Sentiment analysis, trend detection, influencer identification, and bot detection across X (Twitter), Instagram, TikTok, YouTube, Threads, and news portals. Use when: user asks for sentiment analysis, social media monitoring, trend analysis, influencer tracking, bot detection, or mentions 'Verosight', 'social listening', 'cyber monitoring', 'digital reputation'. Covers auth setup, querying posts, analytics (sentiment/trending/volume), profile search, and report generation."
---

# Verosight Monitor — Social Media Intelligence Skill

Integrate Verosight API for real-time social media monitoring and digital reputation management across major platforms.

## Quick Setup

### 1. Get API Key
Sign up at [verosight.com](https://verosight.com) and generate an API key from the [API Keys dashboard](https://verosight.com/dashboard/keys). Keys start with `vlt_live_` (production) or `vlt_test_` (test).

### 2. Authenticate
Exchange your API key for a JWT token (valid 24 hours):

```bash
JWT=$(curl -s -X POST "https://api.verosight.com/v1/auth/token" \
  -H "X-API-Key: vlt_live_YOUR_KEY" | jq -r '.token')
```

Or use the bundled auth script:
```bash
./scripts/verosight-auth.sh vlt_live_YOUR_KEY
```

### 3. Query Data
```bash
# Sentiment analysis
curl -s "https://api.verosight.com/v1/analytics/sentiment?query=KEYWORD&sources=x,instagram&days=7" \
  -H "Authorization: Bearer $JWT"

# Search posts
curl -s "https://api.verosight.com/v1/posts?query=KEYWORD&sources=x,instagram&limit=10" \
  -H "Authorization: Bearer $JWT"
```

## API Endpoints

### Posts
```
GET /v1/posts
```
Search posts across platforms with filters.

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string | Search keyword |
| `sources` | string | Comma-separated: `x,instagram,tiktok,youtube,threads,news_portal` |
| `limit` | int | Results per page (default: 10, max: 50) |
| `days` | int | Lookback period (1-90) |
| `sentiment` | string | Filter: `positive`, `negative`, `neutral` |

```
GET /v1/posts/:id
```
Get a single post by ID.

```
GET /v1/posts/:id/comments
```
Get comments for a post.

### Analytics
```
GET /v1/analytics/sentiment
```
Sentiment analysis for a keyword. Returns positive/negative/neutral breakdown, weighted percentages, and sample posts.

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string | Search keyword |
| `sources` | string | Comma-separated platforms |
| `days` | int | Lookback period |
| `limit` | int | Number of sample posts to return |

```
GET /v1/analytics/volume
```
Post/comment volume over time (daily breakdown).

```
GET /v1/analytics/trending
```
Trending posts and profiles for a keyword.

### Profiles
```
GET /v1/profiles?query=ACCOUNT&source=instagram
```
Search for social media profiles.

```
GET /v1/profiles/:source/:account
```
Get profile details (auto-crawls if missing).

```
GET /v1/profiles/:source/:account/stats
```
Engagement stats for a profile.

### Search
```
POST /v1/search
```
Semantic search across all content.

Body:
```json
{
  "query": "keyword",
  "sources": ["x", "instagram"],
  "days": 7
}
```

### Account
```
GET /v1/account/balance
```
Check credit balance (0 cost).

```
GET /v1/account/usage
```
Usage history and statistics (0 cost).

## Response Format

All responses follow a standard envelope:

```json
{
  "data": { ... },
  "meta": {
    "request_id": "uuid",
    "credits_used": 2,
    "credits_remaining": 998
  },
  "pagination": {
    "next_cursor": "base64...",
    "has_more": true,
    "total": 38113
  }
}
```

## Workflows

### Sentiment Analysis Report

1. Authenticate → get JWT
2. Query `/v1/analytics/sentiment` → get positive/negative/neutral breakdown
3. Query `/v1/posts` with `sentiment=negative` → identify vocal accounts
4. Query `/v1/analytics/volume` → trend over time
5. Compile report: overview → trend → narratives → insights → recommendations

For detailed workflow, see [references/sentiment-workflow.md](references/sentiment-workflow.md).

### Influencer Identification

1. Query posts about target topic with high engagement
2. Sort by likes, shares, views
3. Cross-reference with sentiment (positive vs negative influencers)
4. Profile top accounts for follower count and verification status

### Bot Detection

1. Query posts about target topic across platforms
2. Look for patterns:
   - Multiple posts from same account in short timeframe
   - Identical or near-identical content across accounts
   - Coordinated posting timing
   - New accounts with abnormally high activity
3. Flag suspicious accounts for manual review

### PDF Report Generation

Generate professional reports with tables, charts, and formatted layouts using pdfkit (Node.js).

See [references/pdf-template.md](references/pdf-template.md) for complete guide.

## Supported Platforms

| Platform | Coverage |
|----------|----------|
| X (Twitter) | Posts, replies, engagement metrics |
| Instagram | Posts, captions, engagement |
| TikTok | Videos, descriptions |
| YouTube | Videos, comments |
| Threads | Posts, replies |
| Facebook | Posts, pages |
| LinkedIn | Posts, articles |
| News Portals | Articles from Indonesian media |

## Credit System

Each successful API call (2xx response) costs credits. Failed calls (4xx/5xx) do not deduct credits.

| Tier | Rate Limit | Starting Credits |
|------|-----------|-----------------|
| Standard | 60 req/min | 1,000 |
| Pro | 300 req/min | 10,000 |
| Enterprise | Custom | Custom |

Check balance:
```bash
curl -s "https://api.verosight.com/v1/account/balance" \
  -H "Authorization: Bearer $JWT"
```

## Known Limitations

- News portal results dominate volume (~70%); social platforms contribute less
- Semantic search returns broadly relevant results; source/date filters are limited
- Instagram direct scraping often blocked; use Verosight API for Instagram data
- Profile metadata (followers, account age) may not be available for all accounts

## Bundled Resources

| File | Purpose |
|------|---------|
| `references/sentiment-workflow.md` | Step-by-step sentiment analysis workflow with report template |
| `references/pdf-template.md` | PDF generation guide with pdfkit (tables, charts, layout) |
| `scripts/verosight-auth.sh` | Auth helper — exchange API key for JWT |
| `scripts/quick-sentiment.sh` | Quick sentiment check from command line |

## Links

- [Verosight API](https://verosight.com)
- [API Dashboard](https://verosight.com/dashboard)
- [Documentation](https://verosight.com/docs)
- [ClawHub](https://clawhub.com/skills/verosight-monitor)
- [GitHub](https://github.com/jrrqd/verosight-monitor)
