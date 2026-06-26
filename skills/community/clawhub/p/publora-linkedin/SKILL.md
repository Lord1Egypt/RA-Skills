---
name: publora-linkedin
description: >
  Post or schedule content to LinkedIn using the Publora API. Use this skill
  when the user wants to publish or schedule LinkedIn posts, retrieve analytics
  (impressions, reactions, followers), manage reactions, post comments, or
  @mention people/organizations via Publora.
---

# Publora — LinkedIn

LinkedIn platform skill for the Publora API. For auth, core scheduling, media upload, and workspace/webhook docs, see the `publora` core skill.

**Base URL:** `https://api.publora.com/api/v1`  
**Header:** `x-publora-key: sk_YOUR_KEY`  
**Platform ID format:** `linkedin-{profileId}`

## Platform Limits (API)

> ⚠️ API limits differ from native app. Design against these.

| Property | API Limit | Native App |
|----------|-----------|-----------|
| Text | **3,000 characters** | 3,000 |
| Images | Up to 10 × 5 MB, JPEG/PNG/GIF, WebP | Same |
| Video | 30 min / **500 MB** | 15 min / 5 GB |
| Video format | MP4 only | MP4, MOV |
| Organic carousels | ❌ Not via API | ✅ |
| Mixed media | ❌ No | ✅ |
| Rate limit | ~200 calls/hr | — |

First 210 characters visible before "see more".

**Common errors:**
- `MEDIA_ASSET_PROCESSING_FAILED` — file too large or unsupported format
- `Error 429` — rate limit exceeded

## Post a Text Update

```javascript
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Excited to announce our latest product update! #buildinpublic',
    platforms: ['linkedin-ABC123']
  })
});
```

## @Mentioning People and Organizations

Use the following syntax inside `content`:

```
@{urn:li:person:MEMBER_ID|Display Name}       # person
@{urn:li:organization:ORG_ID|Company Name}    # company
```

The display name must **exactly match** the LinkedIn profile name (case-sensitive).

```javascript
body: JSON.stringify({
  content: 'Great collaboration with @{urn:li:organization:107107343|Creative Content Crafts Inc}!',
  platforms: ['linkedin-ABC123']
})
```

## Schedule a Post

```javascript
body: JSON.stringify({
  content: 'Your LinkedIn update here',
  platforms: ['linkedin-ABC123'],
  scheduledTime: '2026-03-20T09:00:00.000Z'
})
```

## Analytics

### Post Statistics

> ⚠️ `queryTypes` is an **array** — `'ALL'` is invalid. Use `queryType` (singular string) for one metric, or `queryTypes` (array) for multiple. At least one is required.

**Multiple metrics** — returns `{ metrics: { IMPRESSION: 4521, ... }, cached: bool }`:
```javascript
const res = await fetch('https://api.publora.com/api/v1/linkedin-post-statistics', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    postedId: 'urn:li:share:7123456789',   // or urn:li:ugcPost:xxx
    platformId: 'linkedin-ABC123',
    queryTypes: ['IMPRESSION', 'MEMBERS_REACHED', 'RESHARE', 'REACTION', 'COMMENT']
  })
});
```

**Single metric** — returns `{ count: 4521, cached: bool }`:
```javascript
body: JSON.stringify({
  postedId: 'urn:li:share:7123456789',
  platformId: 'linkedin-ABC123',
  queryType: 'IMPRESSION'   // singular; valid: IMPRESSION | MEMBERS_REACHED | RESHARE | REACTION | COMMENT
})
```
```

### Account Statistics

```javascript
await fetch('https://api.publora.com/api/v1/linkedin-account-statistics', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({ platformId: 'linkedin-ABC123' })
});
```

### Follower Count & Growth

```javascript
await fetch('https://api.publora.com/api/v1/linkedin-followers', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({ platformId: 'linkedin-ABC123' })
});
```

### Profile Summary (combined overview)

```javascript
await fetch('https://api.publora.com/api/v1/linkedin-profile-summary', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({ platformId: 'linkedin-ABC123' })
});
```

> Analytics may take up to 24h to fully populate after posting.

## Reactions

Supported types: `LIKE`, `PRAISE`, `EMPATHY`, `INTEREST`, `APPRECIATION`, `ENTERTAINMENT`

### Create Reaction

> Returns **HTTP 201** (not 200). Response may include `urnTranslated: { from, to }` when URN translation was needed.

```javascript
await fetch('https://api.publora.com/api/v1/linkedin-reactions', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    postedId: 'urn:li:ugcPost:7429953213384187904',
    reactionType: 'INTEREST',
    platformId: 'linkedin-ABC123'
  })
});
// Response: { success: true, reaction: { id: "urn:li:reaction:...", reactionType: "INTEREST" } }
```

### Delete Reaction

> Response: `{ success: true, reaction: null }` — `reaction` is always `null` on delete (not the deleted type).

```javascript
await fetch('https://api.publora.com/api/v1/linkedin-reactions', {
  method: 'DELETE',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    postedId: 'urn:li:ugcPost:7429953213384187904',
    platformId: 'linkedin-ABC123'
  })
});
```

## Comments

### Create Comment

> Returns **HTTP 201** (not 200). Response: `{ success: true, comment: { id, commentUrn, message, ... } }`

```javascript
await fetch('https://api.publora.com/api/v1/linkedin-comments', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    postedId: 'urn:li:share:7434685316856377344',
    message: 'Great post! Thanks for sharing.',  // max 1,250 characters
    platformId: 'linkedin-ABC123',
    // parentComment: 'urn:li:comment:(...)' ← for nested replies
  })
});
```

### Delete Comment

> `commentId` accepts both full URN (`urn:li:comment:(...)`) and plain numeric ID (`7434695495614312448`).

```javascript
await fetch('https://api.publora.com/api/v1/linkedin-comments', {
  method: 'DELETE',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    postedId: 'urn:li:share:7434685316856377344',
    commentId: 'urn:li:comment:(urn:li:activity:xxx,7434695495614312448)',  // or plain: '7434695495614312448'
    platformId: 'linkedin-ABC123'
  })
});
```

## Platform Quirks

- **No bold/italic via API** — LinkedIn API does not support rich text formatting
- **URN format**: Posts created via Publora → use `postedId` from `/get-post`. External posts: find `urn:li:share:xxx` or `urn:li:ugcPost:xxx`
- **WebP images** auto-converted to JPEG
- **Hashtags** work as plain text but become clickable
- **No organic carousels** via API — only multi-image grid layout
