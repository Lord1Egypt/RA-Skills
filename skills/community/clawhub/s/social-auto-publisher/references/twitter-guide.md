# Twitter (X) Operations Guide

## Platform Characteristics

| Attribute | Description |
|-----------|-------------|
| User Profile | Global users, leaning toward tech/business/media audiences |
| Content Format | 280-character text + images/videos/polls |
| Distribution Mechanism | Algorithmic recommendation + following timeline |
| Best Publishing Time | Adjust based on target time zone |

## Integration Method

### Twitter API v2 (Required)

```bash
# Environment variable configuration
export TWITTER_API_KEY="your_api_key"
export TWITTER_API_SECRET="your_api_secret"
export TWITTER_ACCESS_TOKEN="your_access_token"
export TWITTER_ACCESS_SECRET="your_access_secret"
```

API Endpoints:
- Post Tweet: `POST /2/tweets`
- Reply: `POST /2/tweets` (with `in_reply_to_tweet_id`)
- User Info: `GET /2/users/me`
- Mentions: `GET /2/users/:id/mentions`

### Rate Limits

| Endpoint | Limit |
|----------|-------|
| POST /2/tweets | 200 per 15 min (app) / 50 per 24h (user) |
| GET mentions | 180 per 15 min |
| GET user info | 900 per 15 min |

## Content Creation Essentials

### Threads
- Split into a thread when the body exceeds 280 characters
- The first tweet is the hook
- The last tweet is the CTA
- Number the middle tweets in sequence (1/5, 2/5...)

### Hashtag Strategy
- 1-3 precise tags
- Use PascalCase: `#AIDevelopment`
- Avoid tag stuffing

### Visual Content
- Image aspect ratio: 16:9 or 1:1
- GIFs autoplay
- Video max 140 seconds

## Compliance Red Lines

❌ Spam / Mass duplicate content
❌ Platform manipulation (fake engagement)
❌ Impersonation
❌ Publishing private information
❌ Hate speech and violent content

## Successful Tweet Formula

```
Hook (Grab attention)
  ↓
Context (Provide background)
  ↓
Insight (Core viewpoint)
  ↓
CTA (Call to action / Lead discussion)
```