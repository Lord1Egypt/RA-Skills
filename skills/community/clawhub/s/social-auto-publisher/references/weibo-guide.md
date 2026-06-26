# Weibo Operations Guide

## Platform Characteristics

| Attribute | Description |
|-----------|-------------|
| User Profile | All age groups, skewing younger, high sensitivity to trending topics |
| Content Format | 140-character short text + images/videos |
| Distribution Mechanism | Follower timeline + trending hashtags + recommendation feed |
| Best Publishing Time | 08:00-10:00, 12:00-14:00, 20:00-23:00 |

## Integration Method

### Method 1: Weibo Open Platform API (Recommended)

```bash
# Environment variable configuration
export WEIBO_APP_KEY="your_app_key"
export WEIBO_APP_SECRET="your_app_secret"
export WEIBO_ACCESS_TOKEN="your_access_token"
```

API Endpoints:
- Post Weibo: `POST /2/statuses/update.json`
- Post Weibo with Image: `POST /2/statuses/upload.json`
- Comment List: `GET /2/comments/show.json`
- Reply to Comment: `POST /2/comments/reply.json`
- @ Mentions: `GET /2/statuses/mentions.json`

### Method 2: Cookie Emulation

If API access is unavailable, use browser automation:

```bash
browser navigate https://weibo.com
browser act ref=<post-weibo-input> kind=click
browser act ref=<weibo-content-input-area> kind=type text="Content"
browser act ref=<publish-button> kind=click
```

## Content Creation Essentials

### Text Format
- 140 characters maximum
- Hashtags use double hash signs: `#TopicName#`
- @ users: `@Username`
- Links can be included (short links)

### Image Strategy
- Maximum of 9 images
- The first image determines the click-through rate
- Suitable for infographics, posters, and chat screenshots

### Topic Operations
- Ride trending hashtags to increase exposure
- Create your own topics to cultivate UGC
- Keep topic names to 6-12 characters

## Compliance Red Lines

❌ Sensitive political topics
❌ Non-compliant external links
❌ Malicious marketing / artificial engagement
❌ Infringement of others' rights
❌ Unlabeled marketing content

## Data Metrics

- **Views**: Content reach
- **Engagement**: Total retweets, comments, and likes
- **Follower Growth**: New follows
- **Video Plays**: For video content