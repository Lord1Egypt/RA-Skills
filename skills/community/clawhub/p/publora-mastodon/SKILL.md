---
name: publora-mastodon
description: >
  Post or schedule content to Mastodon using the Publora API. Use this skill
  when the user wants to publish or schedule Mastodon posts via Publora.
---

# Publora — Mastodon

Mastodon / Fediverse platform skill for the Publora API. For auth, core scheduling, media upload, and workspace/webhook docs, see the `publora` core skill.

**Base URL:** `https://api.publora.com/api/v1`  
**Header:** `x-publora-key: sk_YOUR_KEY`  
**Platform ID format:** `mastodon-{accountId}`

> **Note:** Publora currently posts to the **mastodon.social** instance. Other instances are not supported at this time.

## Platform Limits (API)

| Property | Limit | Notes |
|----------|-------|-------|
| Text (toot) | **500 characters** | Instance-configurable; some allow 5,000+ |
| Images | Up to **4** × **16 MB** | JPEG, PNG, GIF, WebP |
| Video | ~**99 MB** | MP4, MOV, WebM; no duration limit, capped by size |
| Text only | ✅ Yes | — |
| Rate limit | 30 media uploads/30 min | 300 requests/5 min per account |

## Post a Toot (text)

```javascript
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Hello Fediverse! Building open, decentralized tools for everyone. #fediverse #opensource',
    platforms: ['mastodon-123456789']
  })
});
```

## Schedule a Toot

```javascript
body: JSON.stringify({
  content: 'Your Mastodon post here',
  platforms: ['mastodon-123456789'],
  scheduledTime: '2026-03-20T10:00:00.000Z'
})
```

## Post with Image

```python
import requests

HEADERS = { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' }

# Step 1: Create post
post = requests.post('https://api.publora.com/api/v1/create-post', headers=HEADERS, json={
    'content': 'Here is a photo from our event 📷 #community',
    'platforms': ['mastodon-123456789']
}).json()

# Step 2: Get upload URL (up to 16 MB, JPEG/PNG/GIF/WebP)
upload = requests.post('https://api.publora.com/api/v1/get-upload-url', headers=HEADERS, json={
    'postGroupId': post['postGroupId'],
    'fileName': 'photo.jpg',
    'contentType': 'image/jpeg',
    'type': 'image'
}).json()

# Step 3: Upload
with open('photo.jpg', 'rb') as f:
    requests.put(upload['uploadUrl'], headers={'Content-Type': 'image/jpeg'}, data=f)
```

## Platform Quirks

- **mastodon.social only** — Publora currently supports this instance
- **Generous image limit**: 16 MB per image, much more than most platforms
- **Video capped by size** (~99 MB default) — no explicit duration limit
- **WebP supported** — unlike Instagram, Mastodon accepts WebP natively
- **Federation**: Posts federate automatically to the broader Fediverse
- **Hashtags**: Important for discoverability on Mastodon — use them in posts
- **Content warnings**: Not directly supported via Publora API yet; use text conventions if needed
