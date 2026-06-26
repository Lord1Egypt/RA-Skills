---
name: publora-youtube
description: >
  Upload and publish video content to YouTube using the Publora API. Use this
  skill when the user wants to upload or schedule YouTube videos via Publora.
---

# Publora — YouTube

YouTube platform skill for the Publora API. For auth, core scheduling, media upload, and workspace/webhook docs, see the `publora` core skill.

**Base URL:** `https://api.publora.com/api/v1`  
**Header:** `x-publora-key: sk_YOUR_KEY`  
**Platform ID format:** `youtube-{channelId}`

## Platform Limits (API)

| Property | Limit | Notes |
|----------|-------|-------|
| Title | **100 characters** | — |
| Description | **5,000 characters** | First 150 chars visible |
| Video duration | **12 hours** | — |
| Video size | 256 GB | — |
| Video formats | MP4, MOV, AVI, WebM | — |
| Images | ❌ Video only | — |
| Text only | ❌ Video required | — |
| Privacy | public / unlisted / private | Default: public |

## Upload a YouTube Video

YouTube requires video and supports privacy settings and metadata:

```javascript
// Step 1: Create post with YouTube-specific platform settings
const post = await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Your video description here. Full details about what this video covers.',
    platforms: ['youtube-UC_CHANNEL_ID'],
    scheduledTime: '2026-03-20T15:00:00.000Z'
  })
}).then(r => r.json());

// Step 2: Get upload URL
const upload = await fetch('https://api.publora.com/api/v1/get-upload-url', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    postGroupId: post.postGroupId,
    fileName: 'video.mp4',
    contentType: 'video/mp4',
    type: 'video'
  })
}).then(r => r.json());

// Step 3: Upload video to S3
await fetch(upload.uploadUrl, {
  method: 'PUT',
  headers: { 'Content-Type': 'video/mp4' },
  body: videoFileBytes
});
```

## Python Example

```python
import requests

HEADERS = { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' }

# Step 1: Create post (content = video description)
post = requests.post('https://api.publora.com/api/v1/create-post', headers=HEADERS, json={
    'content': 'Complete guide to building REST APIs in 2026. We cover authentication, rate limiting, and best practices.',
    'platforms': ['youtube-UC_CHANNEL_ID'],
    'scheduledTime': '2026-03-20T15:00:00.000Z'
}).json()

# Step 2: Get upload URL
upload = requests.post('https://api.publora.com/api/v1/get-upload-url', headers=HEADERS, json={
    'postGroupId': post['postGroupId'],
    'fileName': 'tutorial.mp4',
    'contentType': 'video/mp4',
    'type': 'video'
}).json()

# Step 3: Upload
with open('tutorial.mp4', 'rb') as f:
    requests.put(upload['uploadUrl'], headers={'Content-Type': 'video/mp4'}, data=f)

print(f"Scheduled: {post['postGroupId']}")
```

## Platform Quirks

- **Video only** — YouTube does not support images or text-only posts
- **content field = description** — the `content` field maps to the YouTube video description
- **Title**: Set via platform settings (defaults to first line of description if not set)
- **Privacy**: Defaults to `public`. Can be set to `unlisted` or `private` via platform settings
- **YouTube Shorts**: Videos under 60 seconds in portrait orientation (9:16) are automatically treated as Shorts
- **Large files**: 256 GB max — YouTube is the most generous platform for file size
- **Processing time**: YouTube processes uploaded videos before they go live; scheduling accounts for this
