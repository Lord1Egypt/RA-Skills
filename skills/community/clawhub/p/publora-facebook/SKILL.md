---
name: publora-facebook
description: >
  Post or schedule content to Facebook Pages using the Publora API. Use this
  skill when the user wants to publish or schedule Facebook posts via Publora.
---

# Publora — Facebook

Facebook platform skill for the Publora API. For auth, core scheduling, media upload, and workspace/webhook docs, see the `publora` core skill.

**Base URL:** `https://api.publora.com/api/v1`  
**Header:** `x-publora-key: sk_YOUR_KEY`  
**Platform ID format:** `facebook-{pageId}`

If you manage multiple Pages, each Page gets its own platform ID.

## Requirements

- A **Facebook Page** (not a personal profile) connected via OAuth
- Page admin permissions granted during OAuth

## Platform Limits (API)

> ⚠️ API video limits are significantly stricter than native.

| Property | API Limit | Notes |
|----------|-----------|-------|
| Text (API) | Up to **63,206 characters** | Publora frontend editor caps at 2,200; API itself has no lower limit |
| Images | Up to 10 × 10 MB | JPEG, PNG, GIF, BMP, TIFF; WebP auto-converted to JPEG |
| Video | **45 min** / **512 MB** (Publora server limit) | FB natively allows 2 GB — Publora caps at 512 MB |
| Reels duration | **3–90 seconds** | Pages only; 30/day |
| Reels rate limit | 30 Reels/day/Page | — |
| Reels posting | Pages only (not profiles) | — |
| Text only | ✅ Yes | — |

**Token management:** Facebook page tokens expire after **59 days**. Publora auto-refreshes, but if refresh fails silently (permission changes), posts will fail without a clear token error — reconnect the page in dashboard.

**Common errors:**
- `Error 1363026` — video over 45 min → trim
- `Error 1363023` — file over 2 GB (Publora's 512 MB limit kicks in first)
- `Error 1363128` — Reels duration outside 3–90s range

> Posts under 80 characters get 66% more engagement on Facebook.

## Post a Text Update

```javascript
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Exciting news from our team! We just launched a new feature. Check it out at publora.com 🎉',
    platforms: ['facebook-123456789']
  })
});
```

## Schedule a Post

```javascript
body: JSON.stringify({
  content: 'Your Facebook Page update',
  platforms: ['facebook-123456789'],
  scheduledTime: '2026-03-20T13:00:00.000Z'
})
```

## Post with Image

```javascript
// Step 1: Create post
const post = await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Check out our latest product photo!',
    platforms: ['facebook-123456789']
  })
}).then(r => r.json());

// Step 2: Get upload URL
const upload = await fetch('https://api.publora.com/api/v1/get-upload-url', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    postGroupId: post.postGroupId,
    fileName: 'photo.jpg',
    contentType: 'image/jpeg',
    type: 'image'
  })
}).then(r => r.json());

// Step 3: Upload
await fetch(upload.uploadUrl, {
  method: 'PUT',
  headers: { 'Content-Type': 'image/jpeg' },
  body: imageBytes
});
```

## Post a Reel (3–90 seconds)

Use the same flow but upload a short video file. Reels are posted to Pages only.

## Platform Quirks

- **Pages only** — personal profiles are not supported via the Facebook Graph API
- **Multiple pages** — each Page has a separate platform ID; include multiple `facebook-{pageId}` in `platforms` array to post to several at once
- **Video limit**: 45 min / **512 MB** (Publora server cap — FB natively allows 2 GB; Publora's limit kicks in first)
- **Reels**: Must be 3–90 seconds; Pages only; 30/day per Page
- **Images only in multi-media**: Multiple videos in one post are not supported — they'll go through the photo path incorrectly. Use one video per post.
- **No mixed media**: Images + video in same post will fail at Facebook API level (Publora doesn't pre-validate this for Facebook)
- **WebP auto-converted** to JPEG — no action needed
- **59-day token**: Publora auto-refreshes page tokens; reconnect dashboard if you see unexplained posting failures
- **Link previews**: Including a URL in text triggers Facebook's auto link preview — not controllable via API
- **Rate limit formula**: 200 × users/hour
