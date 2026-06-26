---
name: publora-threads
description: >
  Post or schedule content to Threads using the Publora API. Use this skill
  when the user wants to publish or schedule a Threads post via Publora.
---

# Publora — Threads

Threads platform skill for the Publora API. For auth, core scheduling, media upload, and workspace/webhook docs, see the `publora` core skill.

**Base URL:** `https://api.publora.com/api/v1`  
**Header:** `x-publora-key: sk_YOUR_KEY`  
**Platform ID format:** `threads-{accountId}`

## ⚠️ Temporary Restriction — Thread Nesting Unavailable

**Multi-threaded nested posts are temporarily unavailable** on Threads due to Threads app reconnection status.

This means: content over 500 characters that would normally auto-split into connected reply chains does **not** work right now.

**What still works normally:**
- Single posts (text, images, videos, carousels)
- Standalone posts under 500 characters

Contact support@publora.com for updates on when thread nesting will be restored.

## Platform Limits (API)

| Property | API Limit | Notes |
|----------|-----------|-------|
| Text | **500 characters** | 10,000 via text attachment |
| Images | Up to 10 × 8 MB | JPEG, PNG; WebP auto-converted |
| Video | **5 min** / 500 MB | MP4, MOV; 1 per post |
| Max links | 5 per post | — |
| **Hashtags** | **Max 1 per post** | More than 1 may be ignored or rejected |
| Text only | ✅ Yes | — |
| Threading (nested) | ⚠️ Temporarily unavailable | See above |
| Rate limit | 250 posts/24hr | 1,000 replies/24hr |

## Post a Single Thread

```javascript
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Building in public is the best marketing strategy. Here\'s why 👇',
    platforms: ['threads-17841412345678']
  })
});
```

## Schedule a Post

```javascript
body: JSON.stringify({
  content: 'Your Threads post here',
  platforms: ['threads-17841412345678'],
  scheduledTime: '2026-03-20T10:00:00.000Z'
})
```

## Post with Image

```javascript
// Step 1: Create post
const post = await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Caption for your image post',
    platforms: ['threads-17841412345678']
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

// Step 3: Upload to S3
await fetch(upload.uploadUrl, {
  method: 'PUT',
  headers: { 'Content-Type': 'image/jpeg' },
  body: imageBytes
});
```

## Thread Nesting (temporarily unavailable)

When restored, long content auto-splits into connected posts. Three methods:

**Auto-split** (content > 500 chars): Publora splits at paragraphs/sentences/words, adds `(1/N)` markers.

**Manual `---` separator:**
```javascript
body: JSON.stringify({
  content: 'First post.\n\n---\n\nSecond post.\n\n---\n\nThird post.',
  platforms: ['threads-17841412345678']
})
```

**Explicit `[n/m]` markers:** Publora detects `[1/3]`, `[2/3]` format and splits at those points exactly.

> ⚠️ Currently **all nested threading is disabled**. Single posts, images, carousels work normally.

**Media in threads:** Images/video attach to the **first post only**. Subsequent posts are text-only.

## Reply Control (platformSettings)

Control who can reply to posts:

```javascript
body: JSON.stringify({
  content: 'Your post here',
  platforms: ['threads-17841412345678'],
  platformSettings: {
    threads: {
      replyControl: 'mentioned_only'  // or: 'accounts_you_follow', 'everyone', '' (default)
    }
  }
})
```

| Value | Who can reply |
|-------|---------------|
| `""` (default) | Platform default (anyone) |
| `"everyone"` | Anyone |
| `"accounts_you_follow"` | Only accounts you follow |
| `"mentioned_only"` | Only mentioned accounts |

## Platform Quirks

- **Connected via Meta OAuth** — same account as Instagram
- **Max 1 hashtag per post** — more than 1 may be ignored or rejected by Threads
- **5 links per post max** — enforced at the API level
- **PNG supported** — unlike Instagram, Threads accepts PNG images; WebP auto-converted
- **Video carousels limited** — video support in carousels is limited; use images for carousels
- **Nested threading disabled** — see the notice at the top of this skill
