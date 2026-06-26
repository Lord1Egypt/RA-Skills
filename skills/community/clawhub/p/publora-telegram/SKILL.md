---
name: publora-telegram
description: >
  Post or schedule content to Telegram channels and groups using the Publora API.
  Use this skill when the user wants to publish or schedule Telegram messages via
  Publora.
---

# Publora — Telegram

Telegram platform skill for the Publora API. For auth, core scheduling, media upload, and workspace/webhook docs, see the `publora` core skill.

**Base URL:** `https://api.publora.com/api/v1`  
**Header:** `x-publora-key: sk_YOUR_KEY`  
**Platform ID format:** `telegram-{chatId}`

## Requirements

1. Create a bot via [@BotFather](https://t.me/BotFather) on Telegram
2. Copy the bot token
3. Add the bot as an **administrator** of your target channel or group
4. Connect via Publora dashboard using the bot token + channel name

## Platform Limits (API — Bot API)

> ⚠️ Telegram Bot API has a strict 50 MB file limit (not the 4 GB that user clients allow).

| Property | Bot API Limit | User Client |
|----------|--------------|-------------|
| Text (message) | **4,096 characters** | Same |
| Media caption | **1,024 characters** ⚠️ | 4,096 (Premium) |
| Images | Up to 10 × 10 MB | JPEG, PNG, GIF, WebP, BMP |
| Video | **50 MB** ⚠️ | 4 GB |
| Video formats | MP4, MOV, AVI, MKV, WebM | — |
| Text only | ✅ Yes | — |
| Rate limit | 30 messages/sec | 20 messages/min per group |

**Common errors:**
- `MEDIA_CAPTION_TOO_LONG` — caption exceeds 1,024 chars → reduce or move text to message body
- `Bad Request: file is too big` — file exceeds 50 MB → compress or use a smaller file

## Post a Text Message

```javascript
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: '📢 **Announcement**: Our new feature is live! Check it out at publora.com\n\n#update #publora',
    platforms: ['telegram--1001234567890']  // note: group chat IDs are negative
  })
});
```

Markdown formatting is supported in Telegram messages.

## Schedule a Message

```javascript
body: JSON.stringify({
  content: 'Your Telegram channel message here',
  platforms: ['telegram--1001234567890'],
  scheduledTime: '2026-03-20T09:00:00.000Z'
})
```

## Send an Image

```python
import requests

HEADERS = { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' }

# Step 1: Create post (content = caption, max 1,024 chars for media)
post = requests.post('https://api.publora.com/api/v1/create-post', headers=HEADERS, json={
    'content': 'Check out our latest update! 🚀',   # keep under 1,024 chars when attaching media
    'platforms': ['telegram--1001234567890']
}).json()

# Step 2: Get upload URL (max 10 MB per image)
upload = requests.post('https://api.publora.com/api/v1/get-upload-url', headers=HEADERS, json={
    'postGroupId': post['postGroupId'],
    'fileName': 'image.jpg',
    'contentType': 'image/jpeg',
    'type': 'image'
}).json()

# Step 3: Upload
with open('image.jpg', 'rb') as f:
    requests.put(upload['uploadUrl'], headers={'Content-Type': 'image/jpeg'}, data=f)
```

## Send a Video (max 50 MB)

Same flow as image but use `contentType: 'video/mp4'` and `type: 'video'`. Keep the file under 50 MB.

## Platform Quirks

- **Bot API file limit is 50 MB** — not 4 GB like Telegram user clients. For larger files, you'd need a Local Bot API Server (not supported by Publora)
- **Caption vs message body**: When attaching media, `content` becomes the caption (max 1,024 chars). For text-only posts, content can be up to 4,096 chars.
- **Markdown supported**: Use `**bold**`, `_italic_`, `` `code` ``, `[link](url)` in message content
- **Group chat IDs are negative**: e.g. `telegram--1001234567890`
- **Bot must be admin**: The bot needs admin permissions to post in channels; in groups, it needs at least "Send messages" permission
- **Rate limit**: 30 messages/second globally; 20 messages/minute per group — Publora handles queuing automatically
