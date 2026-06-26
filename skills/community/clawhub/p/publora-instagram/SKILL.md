---
name: publora-instagram
description: >
  Post or schedule content to Instagram using the Publora API. Use this skill
  when the user wants to publish images, reels, stories, or carousels to
  Instagram via Publora.
---

# Publora — Instagram

Instagram platform skill for the Publora API. For auth, core scheduling, media upload, and workspace/webhook docs, see the `publora` core skill.

**Base URL:** `https://api.publora.com/api/v1`  
**Header:** `x-publora-key: sk_YOUR_KEY`  
**Platform ID format:** `instagram-{accountId}`

## Requirements

- **Instagram Business account recommended** — personal accounts are not supported; Creator accounts may also work (`instagram_business_*` scopes), but Business is the officially tested and recommended type
- Connected directly via Instagram OAuth through the Publora dashboard (no Facebook Page required)

## Platform Limits (API)

> ⚠️ Instagram API is significantly more restrictive than the native app.

| Property | API Limit | Native App |
|----------|-----------|-----------|
| Caption | **2,200 characters** | 2,200 |
| Images | **10 × 8 MB** | 20 images |
| Image format | **JPEG recommended** via API (PNG may work in practice; GIF not supported) | PNG, GIF also work |
| Mixed carousel | ❌ No images + videos | ✅ |
| Reels duration | **3 min (180s)** via API ⚠️ | 20 minutes |
| Reels size | 300 MB | — |
| Stories duration | **60s** / 100 MB | — |
| Carousel video | 60s per clip / 300 MB | — |
| Text only | ❌ Media required | — |
| Rate limit | 50 posts/24hr | — |

First 125 characters visible before "more".

**Common errors:**
- `(#10) The user is not an Instagram Business` — Creator accounts not supported, switch to Business
- `Error 2207010` — caption exceeds 2,200 chars
- `Error 2207004` — image exceeds 8 MB
- `Error 9, Subcode 2207042` — rate limit reached

## Post an Image

```javascript
// Step 1: Create the post
const post = await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Your caption here ✨ #hashtag',
    platforms: ['instagram-17841412345678'],
    scheduledTime: '2026-03-20T12:00:00.000Z'
  })
}).then(r => r.json());

// Step 2: Get upload URL
const upload = await fetch('https://api.publora.com/api/v1/get-upload-url', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    postGroupId: post.postGroupId,
    fileName: 'photo.jpg',
    contentType: 'image/jpeg',   // ⚠️ JPEG only for Instagram
    type: 'image'
  })
}).then(r => r.json());

// Step 3: Upload to S3
await fetch(upload.uploadUrl, {
  method: 'PUT',
  headers: { 'Content-Type': 'image/jpeg' },
  body: imageFileBytes
});
```

## Post a Carousel (up to 10 images)

Call `get-upload-url` N times with the **same `postGroupId`**:

```python
import requests

HEADERS = { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' }

# Create post
post = requests.post('https://api.publora.com/api/v1/create-post', headers=HEADERS, json={
    'content': 'Swipe through our product highlights! 👆',
    'platforms': ['instagram-17841412345678'],
    'scheduledTime': '2026-03-20T12:00:00.000Z'
}).json()

# Upload each image (max 10)
images = ['slide1.jpg', 'slide2.jpg', 'slide3.jpg']
for img_path in images:
    upload = requests.post('https://api.publora.com/api/v1/get-upload-url', headers=HEADERS, json={
        'postGroupId': post['postGroupId'],
        'fileName': img_path,
        'contentType': 'image/jpeg',
        'type': 'image'
    }).json()
    with open(img_path, 'rb') as f:
        requests.put(upload['uploadUrl'], headers={'Content-Type': 'image/jpeg'}, data=f)
```

## Post a Reel (video, up to 3 min via API)

```javascript
// Create post, then upload video via get-upload-url with type: 'video'
const post = await createPost({
  content: 'Check out our latest Reel! 🎬',
  platforms: ['instagram-17841412345678'],
  platformSettings: { instagram: { videoType: 'REELS' } }
});

const upload = await getUploadUrl({
  postGroupId: post.postGroupId,
  fileName: 'reel.mp4',
  contentType: 'video/mp4',
  type: 'video'
});
// Then PUT the video file to upload.uploadUrl
```

> ⚠️ Reels via API accept up to **3 minutes (180s)** / 300 MB. Native app allows 20 min — API is significantly stricter. Only videos **5–90 seconds** appear in the Reels feed tab; longer clips post but show as regular video posts.

## Platform Quirks

- **JPEG recommended**: The Instagram Graph API works best with JPEG. PNG may work in practice but is not guaranteed. Always use JPEG to be safe — Publora does NOT auto-convert for Instagram.
- **Business account recommended**: Personal accounts are not supported. Creator accounts may work via `instagram_business_*` scopes but are not fully tested — Business is safest.
- **Reels via API**: The `platform-limits` doc (March 2026) states 3 min (180s) max; the platform-specific doc states 15 min. Use 3 min as the safe design limit. Only videos **5–90s** appear in the Reels tab regardless.
- **Stories vs Reels**: Use `platformSettings: { instagram: { videoType: "STORIES" } }` to post as Story (disappears after 24h). Default is `"REELS"`.
- **No shopping tags, branded content, filters, or music** via API
- **Carousels**: 2–10 items (native allows 20); cannot mix images and videos in same carousel
- **WebP**: Must be converted to JPEG manually before upload
- **Aspect ratios**: Instagram supports 4:5 (portrait) to 1.91:1 (landscape); images outside range will be cropped
- **Hashtags**: Max 30 per post; included in caption text (no separate field)
