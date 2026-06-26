---
name: scrapebadger
description: Web scraping platform — Twitter/X data, Vinted marketplace, and general web scraping API
version: 1.0.0
requires:
  env:
    - SCRAPEBADGER_API_KEY
tags:
  - twitter
  - vinted
  - web-scraping
  - scraping
  - social-media
  - marketplace
  - api
  - data
---

# ScrapeBadger — Web Scraping Platform

ScrapeBadger provides REST APIs for three products. Use the `web_fetch` tool to call these endpoints.

## Authentication

Every request needs the `SCRAPEBADGER_API_KEY` environment variable.
Include it as an HTTP header: `X-API-Key: $SCRAPEBADGER_API_KEY`

## Base URL

```
https://scrapebadger.com
```

---

## Twitter/X API

### Users

**Get user profile by username:**
```
GET /v1/twitter/users/{username}/by_username
```

**Get user profile by numeric ID:**
```
GET /v1/twitter/users/{user_id}/by_id
```

**Batch get users by usernames (comma-separated):**
```
GET /v1/twitter/users/batch_by_usernames?usernames=elonmusk,OpenAI
```

**Batch get users by IDs (comma-separated):**
```
GET /v1/twitter/users/batch_by_ids?user_ids=44196397,1230113324
```

**Search users:**
```
GET /v1/twitter/users/search_users?query=AI+agents
```

**Get followers:**
```
GET /v1/twitter/users/{username}/followers
```

**Get following:**
```
GET /v1/twitter/users/{username}/followings
```

**Get mentions:**
```
GET /v1/twitter/users/{username}/mentions
```

**Get subscriptions:**
```
GET /v1/twitter/users/{user_id}/subscriptions
```

**Get user articles:**
```
GET /v1/twitter/users/{user_id}/articles
```

### Tweets

**Get tweet by ID:**
```
GET /v1/twitter/tweets/tweet/{tweet_id}
```

**Get multiple tweets by IDs:**
```
GET /v1/twitter/tweets/?tweets=123,456,789
```

**Advanced search:**
```
GET /v1/twitter/tweets/advanced_search?query=web+scraping&query_type=Latest&count=20
```

**Get replies:**
```
GET /v1/twitter/tweets/tweet/{tweet_id}/replies
```

**Get quotes:**
```
GET /v1/twitter/tweets/tweet/{tweet_id}/quotes
```

**Get retweeters:**
```
GET /v1/twitter/tweets/tweet/{tweet_id}/retweeters
```

**Get favoriters (likes):**
```
GET /v1/twitter/tweets/tweet/{tweet_id}/favoriters
```

**Get similar tweets:**
```
GET /v1/twitter/tweets/tweet/{tweet_id}/similar
```

**Get edit history:**
```
GET /v1/twitter/tweets/tweet/{tweet_id}/edit_history
```

**Get community notes:**
```
GET /v1/twitter/tweets/tweet/{tweet_id}/community_notes
```

**Get article:**
```
GET /v1/twitter/tweets/article/{article_id}
```

### Communities

**Get community:**
```
GET /v1/twitter/communities/{community_id}
```

**Get community tweets:**
```
GET /v1/twitter/communities/{community_id}/tweets
```

**Search communities:**
```
GET /v1/twitter/communities/search?query=AI
```

### Lists

**Get list details:**
```
GET /v1/twitter/lists/{list_id}/detail
```

**Get list tweets:**
```
GET /v1/twitter/lists/{list_id}/tweets
```

**Search tweets in list:**
```
GET /v1/twitter/lists/{list_id}/search_tweets?query=keyword
```

### Trends

**Get trending topics:**
```
GET /v1/twitter/trends/
```

**Get trends by location (WOEID):**
```
GET /v1/twitter/trends/place/{woeid}
```

### Geo

**Search places:**
```
GET /v1/twitter/geo/search?query=New+York
```

**Get place details:**
```
GET /v1/twitter/geo/places/{place_id}
```

### Spaces

**Get Space details:**
```
GET /v1/twitter/spaces/{space_id}
```

**Get broadcast details:**
```
GET /v1/twitter/spaces/broadcast/{broadcast_id}
```

---

## Vinted Marketplace API

**Search items:**
```
GET /v1/vinted/search?query=nike+shoes&market=fr&page=1&per_page=20
```
Optional params: `price_from`, `price_to`, `brand_ids`, `order`

**Get item details:**
```
GET /v1/vinted/items/{item_id}?market=fr
```

**Get user profile:**
```
GET /v1/vinted/users/{user_id}?market=fr
```

**Get user's items:**
```
GET /v1/vinted/users/{user_id}/items?market=fr
```

**Search brands:**
```
GET /v1/vinted/brands?keyword=nike&market=fr
```

**List colors:**
```
GET /v1/vinted/colors?market=fr
```

**List statuses:**
```
GET /v1/vinted/statuses?market=fr
```

**List markets:**
```
GET /v1/vinted/markets
```

Supported markets: fr, de, uk, us, es, it, nl, be, at, pl, pt, cz, lt, and more.

---

## Web Scraping API

**Scrape a URL:**
```
POST /v1/web/scrape
Content-Type: application/json

{"url": "https://example.com", "render_js": false, "return_format": "markdown"}
```
Optional fields: `render_js` (boolean), `wait_for` (CSS selector), `timeout_ms`, `proxy_country`, `return_format` (html/markdown/text)

**Detect anti-bot protection (1 credit):**
```
POST /v1/web/detect
Content-Type: application/json

{"url": "https://example.com"}
```

**Take screenshot:**
```
POST /v1/web/screenshot
Content-Type: application/json

{"url": "https://example.com", "full_page": true}
```

**Extract structured data:**
```
POST /v1/web/extract
Content-Type: application/json

{"url": "https://example.com", "ai_query": "What is the main product price?"}
```
Optional fields: `extract_rules` (CSS/XPath), `ai_extract_rules`, `ai_query`

**Submit batch job:**
```
POST /v1/web/batch
Content-Type: application/json

{"urls": ["https://example.com", "https://example.org"]}
```

**Check batch status:**
```
GET /v1/web/batch/{job_id}
```

---

## Pagination

Most list endpoints support cursor-based pagination. Pass the `cursor` query parameter from the previous response to get the next page.

## Credits

Each API call costs credits. Check your balance:
- Twitter endpoints: 1 credit per call
- Web scraping: 1-10 credits depending on complexity
- Vinted: 1 credit per call

## Rate Limits

Rate limits are per API key. Check the `X-RateLimit-*` response headers for current limits.

## More Information

- Documentation: https://docs.scrapebadger.com
- Dashboard: https://scrapebadger.com/dashboard
- MCP Server: https://mcp.scrapebadger.com/mcp
