# API Documentation Reference

## Apify API

### Facebook Posts Scraper (Primary)
- Actor ID: `apify~facebook-posts-scraper`
- Run URL: `POST https://api.apify.com/v2/acts/apify~facebook-posts-scraper/runs`

Request body:
```json
{
  "token": "<APIFY_TOKEN>",
  "startUrls": [{"url": "<FB_URL>"}],
  "maxPosts": 1,
  "waitForFinish": 60
}
```

Response fields:
- `text` — Post content
- `images` — Array of image URLs
- `videoUrl` — Video URL if present
- `likesCount`, `commentsCount`, `sharesCount` — Engagement
- `pageName` — Source page name
- `timestamp` — Post timestamp

### Alternative: Facebook Scraper
- Actor ID: `apify~facebook-scraper`
- Same API pattern

---

## Gemini API

### Imagen 3.0 (Preferred)
```
POST https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key=<KEY>

{
  "instances": [{"prompt": "<PROMPT>"}],
  "parameters": {
    "sampleCount": 1,
    "aspectRatio": "16:9"
  }
}
```

### Gemini Flash (Fallback)
```
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent?key=<KEY>

{
  "contents": [{"parts": [{"text": "Generate an image: <PROMPT>"}]}],
  "generationConfig": {"responseModalities": ["Text", "Image"]}
}
```

---

## Facebook Graph API

### Upload Photo (Unpublished)
```
POST https://graph.facebook.com/v19.0/{PAGE_ID}/photos

Form data:
- source: <binary image data>
- published: false
- access_token: {PAGE_TOKEN}

Response: {"id": "<photo_id>", "post_id": "<post_id>"}
```

### Post to Feed
```
POST https://graph.facebook.com/v19.0/{PAGE_ID}/feed

Body:
{
  "message": "<TEXT>",
  "attached_media": [{"media_fbid": "<photo_id>"}],
  "access_token": "<PAGE_TOKEN>"
}

Response: {"id": "<page_id_post_id>"}
```

### Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Permission/access error | Refresh token |
| 368 | Content policy violation | Rewrite content |
| 4 | API rate limit | Wait and retry |
| 190 | Invalid/expired token | Get new token |

---

## Getting Credentials

### Apify Token
1. Go to https://console.apify.com/account/integrations
2. Copy Personal API Token

### Gemini API Key
1. Go to https://aistudio.google.com/app/apikey
2. Create new API key

### Facebook Page Token
1. Go to Facebook Developer Console
2. Create app with "Pages" product
3. Get User Access Token with `pages_manage_posts` permission
4. Exchange for Page Access Token:
   ```
   GET https://graph.facebook.com/{USER_ID}/accounts?access_token={USER_TOKEN}
   ```
5. Find token for your page in response
