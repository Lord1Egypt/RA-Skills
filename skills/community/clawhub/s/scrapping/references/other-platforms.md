# Other Platform Endpoints

## Pinterest

Base path: `/v1/pinterest`

### Search
```
GET /v1/pinterest/search?query={keyword}&cursor={cursor}
```

### User Boards
```
GET /v1/pinterest/user/boards?handle={username}
```

### Board Details
```
GET /v1/pinterest/board?board_id={id}
```

## Threads

Base path: `/v1/threads`

### Search by Keyword
```
GET /v1/threads/search?query={keyword}&cursor={cursor}
```
Search Threads posts by keyword.

## Bluesky

Base path: `/v1/bluesky`

All public Bluesky endpoints are available. Check docs for specific endpoints:
https://docs.scrapecreators.com

## Snapchat

Base path: `/v1/snapchat`

Check docs for available Snapchat endpoints:
https://docs.scrapecreators.com

## Twitch

Base path: `/v1/twitch`

Check docs for available Twitch endpoints:
https://docs.scrapecreators.com

## Kick

Base path: `/v1/kick`

### Clip
```
GET /v1/kick/clip?clip_id={id}
```
Get details for a Kick clip.

## Truth Social

Base path: `/v1/truthsocial`

### User Posts
```
GET /v1/truthsocial/user/posts?handle={username}
```
Get a user's Truth Social posts. Pass `user_id` instead of `handle` for faster responses.

## Google

Base path: `/v1/google`

### Google Ad Library — Company Ads
```
GET /v1/google/company/ads?query={company_name}&region={region}
```
Search Google Ad Library for a company's ads. Supports `region` parameter (e.g., `region=US`, `region=UK`).

### Google Search
Scrape Google search results with region filtering. Supports `region` parameter.

## Link-in-Bio Platforms

### Linktree
```
GET /v1/linktree/profile?handle={username}
```

### Komi
```
GET /v1/komi/profile?handle={username}
```

### Pillar
```
GET /v1/pillar/profile?handle={username}
```

### Linkbio
```
GET /v1/linkbio/profile?handle={username}
```

### Linkme
```
GET /v1/linkme/profile?handle={username}
```

## Amazon Shop

### Creator Amazon Shop
```
GET /v1/amazon/shop?handle={username}
```
Scrape a creator's Amazon storefront/shop.

## Notes

- These platforms have fewer endpoints than TikTok/Instagram/YouTube
- For the latest endpoints, always check https://docs.scrapecreators.com
- All endpoints follow the same auth pattern: `x-api-key` header
- Use `trim=true` where supported to reduce response size
