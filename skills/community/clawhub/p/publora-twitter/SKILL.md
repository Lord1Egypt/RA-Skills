---
name: publora-twitter
description: >
  Post or schedule content to X (Twitter) using the Publora API. Use this skill
  when the user wants to tweet, schedule a tweet, or post a thread to X/Twitter
  via Publora.
---

# Publora — X / Twitter

X/Twitter platform skill for the Publora API. For auth, core scheduling, media upload, and workspace/webhook docs, see the `publora` core skill.

**Base URL:** `https://api.publora.com/api/v1`  
**Header:** `x-publora-key: sk_YOUR_KEY`  
**Platform ID format:** `twitter-{userId}`

> ⚠️ **Twitter/X requires Pro or Premium plan** — excluded from the Starter plan.

## Platform Limits (API)

> ⚠️ API limits differ from native app. Design against these.

| Property | API Limit | Notes |
|----------|-----------|-------|
| Text | **280 characters** | 25,000 with Premium account |
| Images | Up to **4** × 5 MB | All formats auto-converted to PNG (max 1000px width) |
| Video | **2 min (120s)** / 512 MB | ⚠️ Native allows 2:20 — API is stricter |
| Video format | MP4, MOV | — |
| Threading | ✅ Auto-split with `(1/N)` or manual `---` | See Threading section |
| Text only | ✅ Yes | — |

**Common errors:**
- `This user is not allowed to post a video longer than 2 minutes` — trim video to under 120s

## Character Counting

X has specific rules Publora handles automatically:
- **Standard characters** count as 1
- **Emojis** count as **2 characters**
- **URLs** are counted by their **literal length** — Publora does NOT apply Twitter's 23-character URL shortening rule

## Post a Tweet

```javascript
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Just shipped a new feature! 🚀 #buildinpublic',
    platforms: ['twitter-123456789']
  })
});
```

## Threading

### Auto-split (content > 280 chars)
Publora automatically splits at paragraph/sentence/word breaks and adds `(1/N)` markers (e.g., `(1/3)`, `(2/3)`). 10 characters reserved per tweet for the marker.

### Manual split with `---`
Use `---` on its own line to define exact split points:

```javascript
body: JSON.stringify({
  content: '1/ Everything I learned building in public this year.\n\n---\n\n2/ First lesson: ship early. Don\'t wait for perfect.\n\n---\n\n3/ Second lesson: your audience is your best product team.',
  platforms: ['twitter-123456789']
})
```

### Explicit markers `[n/m]`
Use `[1/3]`, `[2/3]` etc. — Publora detects these and splits at those points exactly (preserves as written).

### Media in threads
- Up to 4 images or 1 video attached to the **first tweet only**
- Subsequent tweets in thread are text-only
- Images and video cannot be mixed in the same tweet

## Schedule a Tweet

```javascript
body: JSON.stringify({
  content: 'Scheduled announcement: our product launches tomorrow! 🎉',
  platforms: ['twitter-123456789'],
  scheduledTime: '2026-03-20T14:00:00.000Z'
})
```

## Platform Quirks

- **Pro/Premium required** — Twitter/X is excluded from the Starter plan
- **All images → PNG**: Publora auto-converts all image formats (JPEG, WebP, GIF, etc.) to PNG and resizes to max 1000px width before uploading
- **API video limit is 2 min** — not 2:20 like native app; videos over 120s will fail
- **Emojis count as 2 chars** — factor this into character counting
- **URLs use literal length** — Publora does NOT apply Twitter's 23-char shortening; a 40-char URL counts as 40
- **Premium accounts** get 25,000 character limit — Publora uses extended limit automatically
- **GIF posts** count as a video, not an image — different size/count rules apply
- **Media only on first tweet** when threading
