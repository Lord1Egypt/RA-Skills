---
name: publora
description: >
  Publora API — schedule and publish social media posts across 10 platforms
  (X/Twitter, LinkedIn, Instagram, Threads, TikTok, YouTube, Facebook, Bluesky,
  Mastodon, Telegram). Use this skill when the user wants to post,
  schedule, draft, bulk-schedule, manage workspace users, configure webhooks,
  or retrieve LinkedIn analytics via Publora.
---

# Publora API — Core Skill

Publora is an affordable REST API for scheduling and publishing social media posts
across 10 platforms (Pinterest is listed internally but not yet supported). Base URL: `https://api.publora.com/api/v1`

## Plans & API Access

| Plan | Price | Posts/Month | Platforms |
|------|-------|-------------|-----------|
| Starter | Free | 15 | LinkedIn & Bluesky |
| Pro | $2.99/account | 100/account | All |
| Premium | $5.99/account | 500/account | All |

> ℹ️ Starter gives API access for LinkedIn and Bluesky. Twitter/X requires Pro or Premium (explicitly excluded from Starter). See [publora.com/pricing](https://publora.com/pricing).

## Authentication

All requests require the `x-publora-key` header. Keys start with `sk_` (format: `sk_xxxxxxx.xxxxxx...`).

```bash
curl https://api.publora.com/api/v1/platform-connections \
  -H "x-publora-key: sk_YOUR_KEY"
```

Get your key: [publora.com](https://publora.com) → Settings → API Keys → Generate API Key.
⚠️ Copy immediately — shown only once.

## Step 0: Get Platform IDs

**Always call this first** to get valid platform IDs before posting.

```javascript
const res = await fetch('https://api.publora.com/api/v1/platform-connections', {
  headers: { 'x-publora-key': 'sk_YOUR_KEY' }
});
const { connections } = await res.json();
// connections[i].platformId → e.g. "linkedin-ABC123", "twitter-456"
// Also returns: tokenStatus, tokenExpiresIn, lastSuccessfulPost, lastError
```

Platform IDs look like: `twitter-123`, `linkedin-ABC`, `instagram-456`, `threads-789`, etc.

## Post Immediately

Omit `scheduledTime` to publish right away:

```javascript
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Your post content here',
    platforms: ['twitter-123', 'linkedin-ABC']
  })
});
```

## Schedule a Post

Include `scheduledTime` in ISO 8601 UTC — must be in the future:

```javascript
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Scheduled post content',
    platforms: ['twitter-123', 'linkedin-ABC'],
    scheduledTime: '2026-03-16T10:00:00.000Z'
  })
});
// Response: { postGroupId: "pg_abc123", scheduledTime: "..." }
```

## Save as Draft

Omit `scheduledTime` — post is created as draft. Schedule it later:

```javascript
// Create draft
const { postGroupId } = await createPost({ content, platforms });

// Schedule later
await fetch(`https://api.publora.com/api/v1/update-post/${postGroupId}`, {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({ status: 'scheduled', scheduledTime: '2026-03-16T10:00:00.000Z' })
});
```

## List Posts

Filter, paginate and sort your scheduled/published posts:

```javascript
// GET /api/v1/list-posts
// Query params: status, platform, fromDate, toDate, page, limit, sortBy, sortOrder
const res = await fetch(
  'https://api.publora.com/api/v1/list-posts?status=scheduled&platform=twitter&page=1&limit=20',
  { headers: { 'x-publora-key': 'sk_YOUR_KEY' } }
);
const { posts, pagination } = await res.json();
// pagination: { page, limit, totalItems, totalPages, hasNextPage, hasPrevPage }
```

Valid statuses: `draft`, `scheduled`, `published`, `failed`, `partially_published`

## Get / Delete a Post

```bash
# Get post details
GET /api/v1/get-post/:postGroupId

# Delete post (also removes media from storage)
DELETE /api/v1/delete-post/:postGroupId
```

## Get Post Logs

Debug failed or partially published posts:

```javascript
const res = await fetch(
  `https://api.publora.com/api/v1/post-logs/${postGroupId}`,
  { headers: { 'x-publora-key': 'sk_YOUR_KEY' } }
);
const { logs } = await res.json();
```

## Test a Connection

Verify a platform connection is healthy before posting:

```javascript
const res = await fetch(
  'https://api.publora.com/api/v1/test-connection/linkedin-ABC123',
  { method: 'POST', headers: { 'x-publora-key': 'sk_YOUR_KEY' } }
);
// Returns: { status: "ok"|"error", message, permissions, tokenExpiresIn }
```

## Bulk Schedule (a Week of Content)

```python
from datetime import datetime, timedelta, timezone
import requests

HEADERS = { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' }
base_date = datetime(2026, 3, 16, 10, 0, 0, tzinfo=timezone.utc)

posts = ['Monday post', 'Tuesday post', 'Wednesday post', 'Thursday post', 'Friday post']

for i, content in enumerate(posts):
    scheduled_time = base_date + timedelta(days=i)
    requests.post('https://api.publora.com/api/v1/create-post', headers=HEADERS, json={
        'content': content,
        'platforms': ['twitter-123', 'linkedin-ABC'],
        'scheduledTime': scheduled_time.isoformat()
    })
```

## Media Uploads

All media (images and videos) use a 3-step pre-signed upload workflow:

**Step 1:** `POST /api/v1/create-post` → get `postGroupId`  
**Step 2:** `POST /api/v1/get-upload-url` → get `uploadUrl`  
**Step 3:** `PUT {uploadUrl}` with file bytes (no auth needed for S3)

```python
import requests

HEADERS = { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' }

# Step 1: Create post
post = requests.post('https://api.publora.com/api/v1/create-post', headers=HEADERS, json={
    'content': 'Check this out!',
    'platforms': ['instagram-456'],
    'scheduledTime': '2026-03-15T14:30:00.000Z'
}).json()
post_group_id = post['postGroupId']

# Step 2: Get pre-signed upload URL
upload = requests.post('https://api.publora.com/api/v1/get-upload-url', headers=HEADERS, json={
    'fileName': 'photo.jpg',
    'contentType': 'image/jpeg',
    'type': 'image',  # or 'video'
    'postGroupId': post_group_id
}).json()

# Step 3: Upload directly to S3 (no auth header needed)
with open('./photo.jpg', 'rb') as f:
    requests.put(upload['uploadUrl'], headers={'Content-Type': 'image/jpeg'}, data=f)
```

For carousels: call `get-upload-url` N times with the **same `postGroupId`**.

## Cross-Platform Threading

X/Twitter and Threads support threading. Three methods:

- **Auto-split**: Content over the char limit is split automatically at paragraph/sentence/word breaks. Publora adds `(1/N)` markers (e.g. `(1/3)`).
- **Manual `---`**: Use `---` on its own line to define exact split points.
- **Explicit `[n/m]`**: Use `[1/3]`, `[2/3]` markers — Publora preserves them as-is.

```javascript
// Manual split example
body: JSON.stringify({
  content: 'First tweet.\n\n---\n\nSecond tweet.\n\n---\n\nThird tweet.',
  platforms: ['twitter-123']
})
```

> ⚠️ **Threads Restriction:** Multi-threaded nested posts are **temporarily unavailable on Threads** (connected replies). Single posts, images, and carousels work normally. Contact support@publora.com for updates.

## LinkedIn Analytics

```javascript
// Post statistics — queryTypes is an ARRAY (not a string; 'ALL' is invalid here)
// Use queryType (singular string) for one metric, queryTypes (array) for multiple
await fetch('https://api.publora.com/api/v1/linkedin-post-statistics', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    postedId: 'urn:li:share:7123456789',
    platformId: 'linkedin-ABC123',
    queryTypes: ['IMPRESSION', 'MEMBERS_REACHED', 'RESHARE', 'REACTION', 'COMMENT']
    // OR: queryType: 'IMPRESSION'  ← singular, returns { count: 123 }
    // Multi-metric response: { metrics: { IMPRESSION: 4521, MEMBERS_REACHED: 3200, ... } }
  })
});

// Profile summary (followers + aggregated stats)
await fetch('https://api.publora.com/api/v1/linkedin-profile-summary', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({ platformId: 'linkedin-ABC123' })
});
```

Available analytics endpoints:

| Endpoint | Description |
|----------|-------------|
| `POST /linkedin-post-statistics` | Impressions, reactions, reshares for a post |
| `POST /linkedin-account-statistics` | Aggregated account metrics |
| `POST /linkedin-followers` | Follower count and growth |
| `POST /linkedin-profile-summary` | Combined profile overview |
| `POST /linkedin-create-reaction` | React to a post |
| `DELETE /linkedin-delete-reaction` | Remove a reaction |

## Webhooks

Get real-time notifications when posts are published, fail, or tokens are expiring.

```javascript
// Create a webhook
await fetch('https://api.publora.com/api/v1/webhooks', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    name: 'My webhook',
    url: 'https://myapp.com/webhooks/publora',
    events: ['post.published', 'post.failed', 'token.expiring']
  })
});
// Returns: { webhook: { _id, name, url, events, secret, isActive } }
// Save the `secret` — it's only shown once. Use it to verify webhook signatures.
```

Valid events: `post.scheduled`, `post.published`, `post.failed`, `token.expiring`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/webhooks` | GET | List all webhooks |
| `/webhooks` | POST | Create webhook |
| `/webhooks/:id` | PATCH | Update webhook |
| `/webhooks/:id` | DELETE | Delete webhook |
| `/webhooks/:id/regenerate-secret` | POST | Rotate webhook secret |

Max 10 webhooks per account.

## Workspace / B2B API

Manage multiple users under your workspace account. Contact serge@publora.com to enable Workspace API access.

```javascript
// Create a managed user (returns HTTP 201)
const { user } = await fetch('https://api.publora.com/api/v1/workspace/users', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_CORP_KEY' },
  body: JSON.stringify({ username: 'client@example.com', displayName: 'Acme Corp' })
}).then(r => r.json());
// user._id is the MongoDB ObjectId (24-char hex), e.g. "6626a1f5e4b0c91a2d3f4567"

// Generate connection URL for user to connect their social accounts
const { connectionUrl } = await fetch(
  `https://api.publora.com/api/v1/workspace/users/${user._id}/connection-url`,
  { method: 'POST', headers: { 'x-publora-key': 'sk_CORP_KEY' } }
).then(r => r.json());

// Post on behalf of managed user
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'x-publora-key': 'sk_CORP_KEY',
    'x-publora-user-id': user._id  // ← key header for acting on behalf of a user
  },
  body: JSON.stringify({ content: 'Post for Acme Corp!', platforms: ['linkedin-XYZ'] })
});
```

Workspace endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/workspace/users` | GET | List managed users |
| `/workspace/users` | POST | Create managed user |
| `/workspace/users/:userId` | DELETE | Detach managed user (preserves user record, removes workspace association) |
| `/workspace/users/:userId/api-key` | POST | Generate per-user API key |
| `/workspace/users/:userId/connection-url` | POST | Generate OAuth connection link |

Each managed user has a `dailyPostsLeft` field (default: 100) — note this is informational only and **not enforced as an actual posting limit**. Real limits are workspace-level: `monthlyPosts`, `scheduledPosts`, `scheduleHorizonDays` — enforced at scheduling time. Never expose your workspace key client-side — use per-user API keys for client-facing scenarios.

## Platform Limits Quick Reference (API)

> ⚠️ API limits are often stricter than native app limits. Always design against these.

| Platform | Char Limit | Max Images | Video Max | Text Only? |
|----------|-----------|-----------|-----------|------------|
| Twitter/X | 280 (25K Premium) | 4 × 5MB | 2 min / 512MB | ✅ |
| LinkedIn | 3,000 | 10 × 5MB | 30 min / 500MB | ✅ |
| Instagram | 2,200 | **10 × 8MB (JPEG only)** | **3 min (180s)** Reels / 60s Stories / 300MB | ❌ |
| Threads | 500 | 20 × 8MB | 5 min / 500MB | ✅ |
| TikTok | 2,200 | Video only | 10 min / 4GB | ❌ |
| YouTube | 5,000 desc | Video only | 12h / 256GB | ❌ |
| Facebook | 63,206 | 10 × 10MB | 45 min / 2GB | ✅ |
| Bluesky | 300 | 4 × 1MB | 3 min / 100MB | ✅ |
| Mastodon | 500 | 4 × 16MB | ~99MB | ✅ |
| Telegram | 4,096 (1,024 captions) | 10 × 10MB | 50MB (Bot API) | ✅ |

For full limits detail, see the `docs/guides/platform-limits.md` in the [Publora API Docs](https://github.com/publora/publora-api-docs).

## Platform-Specific Skills

For platform-specific settings, limits, and examples:

- `publora-linkedin` — LinkedIn posts + analytics + reactions
- `publora-twitter` — X/Twitter posts & threads
- `publora-instagram` — Instagram images/reels/carousels
- `publora-threads` — Threads posts
- `publora-tiktok` — TikTok videos
- `publora-youtube` — YouTube videos
- `publora-facebook` — Facebook page posts
- `publora-bluesky` — Bluesky posts
- `publora-mastodon` — Mastodon posts
- `publora-telegram` — Telegram channels

## Post Statuses

- `draft` — Not scheduled yet
- `scheduled` — Waiting to publish
- `published` — Successfully posted
- `failed` — Publishing failed (check `/post-logs`)
- `partially_published` — Some platforms failed

## Errors

| Code | Meaning |
|------|---------|
| 400 | Invalid request (check `scheduledTime` format, required fields) |
| 401 | Invalid or missing API key |
| 403 | Plan limit reached or Workspace API not enabled |
| 404 | Post/resource not found |
| 429 | Platform rate limit exceeded |
