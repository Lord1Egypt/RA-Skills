---
name: social-media-publisher
description: Daily social media posting with NewsAPI for PayLessTax & LevelUpLove
version: 2.7.0
author: Migration from Agent Zero
---

# Social Media Publisher Skill

## Overview
Automated daily social media posting system that generates content using NewsAPI and UploadPost API with Templated.io image rendering.

## Purpose
- Fetch industry news via NewsAPI
- Generate branded image posts using Templated.io
- Publish to social platforms via UploadPost API
- Schedule daily posts for LevelUpLove and PayLessTax

## Input Variables
| Variable | Description | Example |
|----------|-------------|---------|
| NEWS_API_KEY | NewsAPI.org key | 92a8bbc150d... |
| UPLOADPOST_API_KEY | UploadPost API key | from uploadpost.json |
| TEMPLATED_IO_KEY | Templated.io API key | from templated_io.json |
| BRAND | Which brand to post | "paylesstax" or "leveluplove" |
| CONTENT_TYPE | Post type | "news" or "onerliner" |
| PLATFORM | Where to post | "instagram", "facebook", "twitter" |

## Content Types

### News-Based Posts
1. Scrape latest news via NewsAPI (tax for PayLessTax, relationship for LevelUpLove)
2. Summarize headline
3. Generate image via Templated.io
4. Post via UploadPost API
5. Schedule next post

### One-Liner Pool Posts
- Rotate through hand-written one-liners from JSON pool
- Quick generation, no external news fetch
- Fast turnaround for high-frequency posting

## One-Liner Pools

### PayLessTax Topics:
- Tax deadline reminders
- VAT compliance tips
- Penalty warnings
- Professional services CTA

### LevelUpLove Topics:
- Dating advice
- Relationship tips
- Gaming/streaming culture
- Engagement questions

## Triggers
Scheduled through OpenClaw:
- PayLessTax: Every 2 hours during business hours (06:00-18:00)
- LevelUpLove: Every 3 hours (09:00, 12:00, 15:00, 18:00, 21:00)

## APIs & Dependencies
- NewsAPI.org: Fresh content headlines
- Templated.io: Image generation via templates
- UploadPost API: Social media publishing
- requests: HTTP client
- Pillow: Image manipulation (fallback)

## Image Rendering Flow
1. Select template from config (paylesstax_ig_post, leveluplove_ig_post)
2. Replace text layer with news headline or one-liner
3. Render to PNG via Templated.io
4. Download and confirm
5. Upload via UploadPost

## Config Files Required

### paylesstax_oneliners.json
```json
[
  "Miss the 2026 deadline? Penalties apply automatically.",
  "VAT compliance made simple: We're the shortcut you need."
]
```

### uploadpost.json
```json
{
  "api_key": "...",
  "endpoint": "https://api.upload-post.com/api/upload_photos"
}
```

### templated_io.json
```json
{
  "api_key": "...",
  "templates": {
    "paylesstax": {"template_id": "tpl_xxx"},
    "leveluplove": {"template_id": "tpl_yyy"}
  }
}
```

## Output
```json
{
  "brand": "paylesstax",
  "content_type": "news",
  "headline": "SARS Extends Tax Deadline",
  "image_url": "https://...",
  "post_id": 12345,
  "status": "published",
  "scheduled_next": "2026-03-04T08:00:00"
}
```

## Files
- index.py - Main posting logic
- onliners/paylesstax.json - One-liner pool
- onliners/leveluplove.json - One-liner pool
- config/uploadpost.example.json - Template config
- config/templated_io.example.json - Template config
