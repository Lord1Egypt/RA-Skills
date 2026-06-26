---
name: socialcannon
description: >
  Publish, schedule, and manage social media posts across Twitter/X, Facebook,
  Instagram, LinkedIn, TikTok, and YouTube. Content calendar with gap analysis,
  A/B testing, engagement inbox, AI content repurposing, optimal timing
  suggestions, auto-scheduling, and UTM tracking.
version: 1.8.0
metadata:
  openclaw:
    requires:
      env:
        - SOCIALCANNON_CLIENT_ID
        - SOCIALCANNON_CLIENT_SECRET
      bins:
        - curl
    primaryEnv: SOCIALCANNON_CLIENT_ID
    emoji: "\U0001F4E3"
    homepage: https://socialcannon.app
---

# SocialCannon

Social media publishing API. Publish to Twitter/X, Facebook, Instagram, LinkedIn, TikTok, and YouTube from one API with scheduling, analytics, A/B testing, and AI-powered features.

**Base URL:** `https://socialcannon.app`

> **Closed beta — invite only.** SocialCannon is currently in closed beta. Public signup is not yet open. To request access, email **support@socialcannon.app** with a short note about how you plan to use the API.

## Getting Started

Before making API calls, you need credentials and at least one connected social account.

### 1. Get your API credentials

SocialCannon is in **closed beta** — accounts are issued by request, not self-serve. Email **support@socialcannon.app** to request beta access. Once approved, you'll be sent an invite link to sign in at [socialcannon.app](https://socialcannon.app). Your **Client ID** and **Client Secret** are then available on the dashboard Settings page — these are the values for `SOCIALCANNON_CLIENT_ID` and `SOCIALCANNON_CLIENT_SECRET`.

### 2. Connect social accounts

Social accounts are connected via OAuth in the browser. Open the connect URL for each platform you want to use — you'll authorize SocialCannon and get redirected back:

| Platform | Connect URL |
|----------|-------------|
| Twitter/X | `https://socialcannon.app/api/connect/twitter?client_id=YOUR_CLIENT_ID` |
| Facebook | `https://socialcannon.app/api/connect/facebook?client_id=YOUR_CLIENT_ID` |
| Instagram | `https://socialcannon.app/api/connect/instagram?client_id=YOUR_CLIENT_ID` |
| LinkedIn | `https://socialcannon.app/api/connect/linkedin?client_id=YOUR_CLIENT_ID` |
| TikTok | `https://socialcannon.app/api/connect/tiktok?client_id=YOUR_CLIENT_ID` |
| YouTube | `https://socialcannon.app/api/connect/youtube?client_id=YOUR_CLIENT_ID` |

You can also connect accounts from the dashboard at **Settings → Accounts**. Instagram uses Facebook's OAuth flow — make sure you select the Facebook Page linked to your Instagram Business account.

### 3. Get an API token and start posting

Once you have credentials and at least one connected account, authenticate and create your first post:

```bash
# Get a token
TOKEN=$(curl -s -X POST https://socialcannon.app/api/v1/auth/token \
  -H "Content-Type: application/json" \
  -d "{\"grant_type\": \"client_credentials\", \"client_id\": \"$SOCIALCANNON_CLIENT_ID\", \"client_secret\": \"$SOCIALCANNON_CLIENT_SECRET\"}" \
  | jq -r '.data.access_token')

# List your connected accounts
curl -s https://socialcannon.app/api/v1/accounts \
  -H "Authorization: Bearer $TOKEN" | jq '.data'

# Publish a post (replace <account_id> with an ID from the list above)
curl -X POST https://socialcannon.app/api/v1/posts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"accountId": "<account_id>", "content": "Hello from SocialCannon!"}'
```

## Use via MCP (Hermes, Claude Desktop, OpenClaw)

Instead of raw HTTP, you can expose SocialCannon's 23 tools to any MCP-compatible agent with the [`@socialcannon/mcp`](https://www.npmjs.com/package/@socialcannon/mcp) package. Use the same `SOCIALCANNON_CLIENT_ID` / `SOCIALCANNON_CLIENT_SECRET` from your dashboard.

**Hermes Agent** — add to `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  socialcannon:
    command: "npx"
    args: ["-y", "@socialcannon/mcp"]
    env:
      SOCIALCANNON_CLIENT_ID: "your-client-id"
      SOCIALCANNON_CLIENT_SECRET: "your-client-secret"
```

**Claude Desktop** — add an entry under `mcpServers` in `claude_desktop_config.json` with the same `command`/`args`/`env`.

The REST API documented below remains fully available; MCP is an optional convenience layer over the same endpoints.

## Authentication

All requests require a JWT Bearer token. Get one by exchanging your client credentials:

```bash
curl -X POST https://socialcannon.app/api/v1/auth/token \
  -H "Content-Type: application/json" \
  -d "{
    \"grant_type\": \"client_credentials\",
    \"client_id\": \"$SOCIALCANNON_CLIENT_ID\",
    \"client_secret\": \"$SOCIALCANNON_CLIENT_SECRET\"
  }"
```

Response:
```json
{
  "success": true,
  "data": {
    "access_token": "eyJ...",
    "token_type": "Bearer",
    "expires_in": 3600,
    "scope": "posts:read posts:write ..."
  }
}
```

Use `response.data.access_token` as a Bearer token in all subsequent requests. Tokens expire after 1 hour — request a new one when you get a 401.

**All requests below require this header:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

## Response Format

**IMPORTANT: ALL responses are wrapped in a standard envelope.** This includes the token endpoint.

- Success: `{ "success": true, "data": { ... } }`
- Error: `{ "success": false, "error": "message", "code": "ERROR_CODE" }`

When extracting data from any response, always read from `response.data`, not from the response root. For example, to get the access token: `response.data.access_token`, not `response.access_token`.

## Accounts

Accounts represent social media profiles connected via OAuth (see Getting Started above). You need at least one connected account before you can create posts.

### List connected accounts

```bash
curl https://socialcannon.app/api/v1/accounts \
  -H "Authorization: Bearer $TOKEN"
```

Returns all connected social accounts with their platform, username, and status. Use the account `id` field when creating posts. Filter by platform with `?platform=twitter`.

### Get a single account

```bash
curl https://socialcannon.app/api/v1/accounts/<account_id> \
  -H "Authorization: Bearer $TOKEN"
```

### Disconnect an account

```bash
curl -X DELETE https://socialcannon.app/api/v1/accounts/<account_id> \
  -H "Authorization: Bearer $TOKEN"
```

## Posts

### Create a post

Publish immediately (omit `scheduledAt`) or schedule for later:

```bash
curl -X POST https://socialcannon.app/api/v1/posts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "accountId": "<account_id>",
    "content": "Your post text here",
    "mediaUrls": ["https://example.com/image.jpg"],
    "scheduledAt": "2026-04-15T10:00:00Z",
    "platformOptions": {
      "autoUtm": true
    }
  }'
```

Fields:
- `accountId` (required) — ID from the accounts list
- `content` (required) — post text
- `mediaUrls` (optional) — array of public image/video URLs
- `scheduledAt` (optional) — ISO 8601 datetime, `"optimal"` (auto-pick best time based on engagement data, Pro), or omit for immediate publish
- `platformOptions.autoUtm` (optional) — auto-tag URLs with UTM parameters
- `platformOptions.mediaType` (optional) — controls content type:
  - `"reel"` — Facebook/Instagram Reel (vertical 9:16 video)
  - `"story"` — Facebook/Instagram/TikTok Story (24h ephemeral)
  - `"short"` — YouTube Short (vertical video ≤60s)
  - `"community"` — YouTube Community post (text/image)
- `platformOptions` **TikTok fields** — TikTok posts require `privacyLevel` and support `disableComment` / `disableDuet` / `disableStitch`, `commercialContent`, `brandOrganic`, `brandedContent`. See the [TikTok](#tiktok) section under Platform-Specific Notes.

### List posts

```bash
curl "https://socialcannon.app/api/v1/posts?status=published&platform=twitter&limit=20" \
  -H "Authorization: Bearer $TOKEN"
```

Query params: `status` (draft/scheduled/published/failed), `platform`, `accountId`, `limit`, `cursor`

### Get a single post

```bash
curl https://socialcannon.app/api/v1/posts/<post_id> \
  -H "Authorization: Bearer $TOKEN"
```

### Update a draft or scheduled post

```bash
curl -X PATCH https://socialcannon.app/api/v1/posts/<post_id> \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Updated text",
    "scheduledAt": "2026-04-16T14:00:00Z",
    "platformOptions": { "autoUtm": true }
  }'
```

Fields: `content`, `scheduledAt`, `platformOptions` — all optional.

### Delete a post

```bash
curl -X DELETE https://socialcannon.app/api/v1/posts/<post_id> \
  -H "Authorization: Bearer $TOKEN"
```

If the post is published, this also attempts to delete it from the social platform.

### Retry a failed post

```bash
curl -X POST https://socialcannon.app/api/v1/posts/<post_id>/retry \
  -H "Authorization: Bearer $TOKEN"
```

Resets the failed post and attempts to publish immediately. No body needed. If it fails again, the post returns to `failed` status with the new error.

## Threads & Carousels

Create multi-part threads (Twitter reply chains or Instagram carousels):

```bash
curl -X POST https://socialcannon.app/api/v1/posts/thread \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "accountId": "<account_id>",
    "items": [
      { "content": "Thread part 1 — the hook" },
      { "content": "Thread part 2 — the detail" },
      { "content": "Thread part 3 — the CTA", "mediaUrls": ["https://..."] }
    ],
    "scheduledAt": "2026-04-15T10:00:00Z",
    "platformOptions": { "autoUtm": true }
  }'
```

Fields: `accountId` (required), `items` (required, min 2, max 25), `scheduledAt` (optional), `platformOptions` (optional). Instagram requires media on each item.

## Media Upload

Upload images/videos before creating posts. **Three-step direct-to-GCS flow** — bytes go straight to Google Cloud Storage via a signed URL, never through SocialCannon's server. This supports files up to **4GB**.

Accepted types: `image/jpeg`, `image/png`, `image/gif`, `image/webp`, `video/mp4`, `video/quicktime`, `video/webm`.

### Step 1 — Initialize upload

```bash
curl -X POST https://socialcannon.app/api/v1/media/upload-init \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "photo.jpg",
    "contentType": "image/jpeg",
    "size": 1048576
  }'
```

Response:
```json
{
  "success": true,
  "data": {
    "uploadUrl": "https://storage.googleapis.com/...?X-Goog-Signature=...",
    "publicUrl": "https://storage.googleapis.com/<bucket>/media/<clientId>/<uuid>.jpg",
    "requiredHeaders": {
      "Content-Type": "image/jpeg",
      "x-goog-acl": "public-read"
    }
  }
}
```

`uploadUrl` is a V4 signed PUT URL valid for **15 minutes**. `size` must be the exact byte size of the file you're about to upload.

### Step 2 — PUT the file to the signed URL

```bash
curl -X PUT "$UPLOAD_URL" \
  -H "Content-Type: image/jpeg" \
  -H "x-goog-acl: public-read" \
  --data-binary @photo.jpg
```

You **must** send the exact headers returned in `requiredHeaders`. Do **not** send the `Authorization` header — the signed URL carries its own auth. A successful PUT returns HTTP 200 with an empty body.

### Step 3 — Finalize

```bash
curl -X POST https://socialcannon.app/api/v1/media/upload-complete \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{ "publicUrl": "https://storage.googleapis.com/<bucket>/media/<clientId>/<uuid>.jpg" }'
```

Pass the `publicUrl` you got from step 1 verbatim. The server verifies the object exists, stamps `customTime` (starting the 30-day retention window), and increments your upload quota.

Response: `{ "success": true, "data": { "url": "https://...", "filename": "media/<clientId>/<uuid>.jpg", "contentType": "image/jpeg", "size": 1048576 } }`

Use the returned `url` in the `mediaUrls` field when creating posts. Bytes are stored as-is — there is no server-side optimization, so upload the format/quality you want published.

### Quota & errors

- `403` on step 1 with `code` set → your tier has hit its upload quota. Inspect `limit` in the response body.
- `404` on step 3 → the PUT didn't actually land. Retry from step 2.
- `403` on step 3 → `publicUrl` doesn't belong to your client. Use the exact URL returned by step 1, do not construct it yourself.

## Content Calendar

### Get calendar view

See posts grouped by date with gap analysis:

```bash
curl "https://socialcannon.app/api/v1/calendar?startDate=2026-04-01&endDate=2026-04-30" \
  -H "Authorization: Bearer $TOKEN"
```

Returns `posts`, `summary` (totals by status/platform/day), and `gaps` (dates with no posts).

Query params: `startDate` (required), `endDate` (required), `accountId`, `platform`

### Find available slots

```bash
curl "https://socialcannon.app/api/v1/calendar/slots?startDate=2026-04-01&endDate=2026-04-07&slotDurationMinutes=60" \
  -H "Authorization: Bearer $TOKEN"
```

Query params: `startDate` (required), `endDate` (required, max 14-day range), `slotDurationMinutes` (optional, 30-1440, default 60).

Returns `{ slots[], totalSlots, availableSlots, occupiedSlots }`.

## Analytics

### Per-post analytics

Fetch live engagement metrics from the platform:

```bash
curl https://socialcannon.app/api/v1/posts/<post_id>/analytics \
  -H "Authorization: Bearer $TOKEN"
```

Returns: likes, comments, shares, impressions, reach, clicks, engagementRate, plus historical snapshots.

### Aggregate analytics

```bash
curl "https://socialcannon.app/api/v1/analytics/summary?startDate=2026-04-01&endDate=2026-04-30" \
  -H "Authorization: Bearer $TOKEN"
```

Returns totals across all posts for the date range.

### Bulk refresh analytics

```bash
curl -X POST https://socialcannon.app/api/v1/analytics/refresh \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{ "platform": "twitter", "limit": 20 }'
```

Fields: `postIds` (optional, array of up to 50 post IDs to refresh), `platform` (optional, filter), `limit` (optional, default 20, max 50). If `postIds` is provided, those specific posts are refreshed; otherwise recent published posts are refreshed.

## Engagements (Comment Inbox)

### List engagements

```bash
curl "https://socialcannon.app/api/v1/engagements?isRead=false&limit=20" \
  -H "Authorization: Bearer $TOKEN"
```

Query params: `postId`, `isRead` (true/false), `limit`, `cursor`

### Fetch engagements for a post

```bash
curl "https://socialcannon.app/api/v1/posts/<post_id>/engagements?cursor=<next_cursor>" \
  -H "Authorization: Bearer $TOKEN"
```

Fetches fresh comments from the platform and stores them. Supports `cursor` for pagination.

### Mark as read

```bash
curl -X PATCH https://socialcannon.app/api/v1/engagements/<engagement_id> \
  -H "Authorization: Bearer $TOKEN"
```

Marks the engagement as read. No request body needed — the endpoint auto-marks on PATCH.

### Reply to an engagement

```bash
curl -X POST https://socialcannon.app/api/v1/engagements/<engagement_id>/reply \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{ "content": "Thanks for the feedback!" }'
```

Posts the reply directly on the social platform.

## AI Content Repurposing

Adapt content for multiple platforms using AI. Two modes available:

### Preview mode (default) — adapt and return variants for review:

```bash
curl -X POST https://socialcannon.app/api/v1/posts/repurpose \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "sourceContent": "Your long-form content here...",
    "targetPlatforms": ["twitter", "facebook", "tiktok"],
    "mode": "preview",
    "tone": "professional"
  }'
```

Returns `{ "variants": [{ "platform", "content", "validation", "characterCount" }], "allValid" }`.

### Post mode — adapt and publish in one call:

```bash
curl -X POST https://socialcannon.app/api/v1/posts/repurpose \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "sourceContent": "Your content here...",
    "targetPlatforms": ["twitter", "facebook"],
    "mode": "post",
    "accountIds": { "twitter": "acc_123", "facebook": "acc_456" },
    "mediaUrls": { "twitter": ["https://example.com/video.mp4"] },
    "appendContent": { "twitter": "Links or extra text for Twitter only" },
    "appendToAll": "Text appended to all platforms"
  }'
```

Returns `{ "results": [{ "platform", "success", "postUrl?", "error?" }] }`.

All content is humanized automatically to remove AI writing patterns. Trusted clients bypass tier limits.

## A/B Testing (Pro)

> **Not available for TikTok.** A/B-test variants carry only content + media, so they can't set the per-post privacy level TikTok requires. A TikTok account is rejected with `400` and `code: "PLATFORM_UNSUPPORTED"` — publish individual posts to TikTok instead.

### Create a test

```bash
curl -X POST https://socialcannon.app/api/v1/ab-tests \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "accountId": "<account_id>",
    "name": "CTA test",
    "variants": [
      { "content": "Check out our new feature!", "mediaUrls": ["https://..."] },
      { "content": "You won'\''t believe this new feature..." }
    ],
    "metric": "engagementRate",
    "minDurationHours": 24,
    "scheduledAt": "2026-04-20T10:00:00Z"
  }'
```

**Publish behavior matches `POST /api/v1/posts`:**
- **Omit `scheduledAt`** → all variants publish **immediately** to the platform via the social adapter
- **Provide `scheduledAt`** → all variants are **scheduled** for that time (must be within 30 days; cron publishes them hourly)

Each variant is a separate post record. Auto-completes after `minDurationHours` and the winner is determined by the chosen metric. Per-variant `mediaUrls` is optional.

**Partial failure semantics:** if ANY variant fails to publish during immediate mode, the endpoint returns **HTTP 502** and the failed variants are marked with `status: 'failed'`. The A/B test record is still created, but the winner comparison at completion only considers successfully published variants. Inspect each variant's post status before relying on test results.

### Get test results

```bash
curl https://socialcannon.app/api/v1/ab-tests/<test_id> \
  -H "Authorization: Bearer $TOKEN"
```

Returns per-variant metrics, current winner, and confidence score.

### List tests

```bash
curl "https://socialcannon.app/api/v1/ab-tests?status=active" \
  -H "Authorization: Bearer $TOKEN"
```

### Force-complete a test

```bash
curl -X POST https://socialcannon.app/api/v1/ab-tests/<test_id>/complete \
  -H "Authorization: Bearer $TOKEN"
```

## Timing Suggestions (Pro)

### Get recommended posting times

```bash
curl "https://socialcannon.app/api/v1/accounts/<account_id>/timing?timezone=UTC-5" \
  -H "Authorization: Bearer $TOKEN"
```

Returns top 5 time slots ranked by average engagement rate with confidence scores.

### Find the single best available slot

Combines engagement data with calendar availability:

```bash
curl "https://socialcannon.app/api/v1/timing/optimal-slot?accountId=<account_id>&timezone=UTC-5" \
  -H "Authorization: Bearer $TOKEN"
```

Returns the next open slot ranked by historical performance.

### Auto-schedule multiple posts

Distribute posts across optimal time slots for the next 7 days:

```bash
curl -X POST https://socialcannon.app/api/v1/posts/auto-schedule \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "accountId": "<account_id>",
    "posts": [
      { "content": "Post 1 text" },
      { "content": "Post 2 text", "mediaUrls": ["https://..."] },
      { "content": "Post 3 text" }
    ],
    "timezone": "UTC-5"
  }'
```

Max 20 posts per request. Each post gets a unique slot. Returns `{ scheduled: [...], unscheduled: [...], summary: {...} }`.

## UTM Link Tracking

Generate UTM-tagged URLs:

```bash
curl -X POST https://socialcannon.app/api/v1/links/generate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/product",
    "platform": "twitter",
    "campaign": "spring-launch",
    "content": "hero-cta",
    "postId": "<post_id>",
    "save": true
  }'
```

Fields: `url` (required), `platform` (optional — sets `utm_source`), `campaign` (optional — `utm_campaign`), `content` (optional — `utm_content`), `term` (optional — `utm_term`), `postId` (optional — link to a post), `save` (optional, default true — persist to tracked_links).

### List tracked links

```bash
curl "https://socialcannon.app/api/v1/links?postId=<post_id>&platform=twitter&limit=20&cursor=<cursor>" \
  -H "Authorization: Bearer $TOKEN"
```

Query params: `postId`, `platform`, `limit`, `cursor` — all optional.

## Platforms

List supported platforms and their capabilities (public, no auth required):

```bash
curl https://socialcannon.app/api/v1/platforms
```

## Platform-Specific Notes

### Twitter/X
- 280 char limit. Up to 4 images. Threads via reply chains.

### Facebook
- 63,206 char limit. Supports native scheduling. Page-level tokens.
- **Reels**: Set `platformOptions.mediaType` to `"reel"`. Video must be MP4/MOV, vertical (9:16). Without this, videos post as regular video posts.
- **Stories**: Set `platformOptions.mediaType` to `"story"`. Supports one image or video. Ephemeral (24h).

```bash
curl -X POST https://socialcannon.app/api/v1/posts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "accountId": "<account_id>",
    "content": "Check out this tutorial!",
    "mediaUrls": ["https://example.com/video.mp4"],
    "platformOptions": {
      "mediaType": "reel"
    }
  }'
```

### Instagram
- Requires media (no text-only). Max 10 carousel items. No API deletion.
- **Stories**: Set `platformOptions.mediaType` to `"story"`. One image or video.
- **Reels**: Set `platformOptions.mediaType` to `"reel"`. Vertical 9:16 video.

### TikTok
- Requires media — no text-only posts. Supports video, photo carousel (up to 35 images), and Stories.
- **`platformOptions.privacyLevel` is REQUIRED** on every TikTok post — there is no default. Omitting it returns `400` with code `TIKTOK_PRIVACY_REQUIRED`. Use a value from the creator-info endpoint's `privacyLevelOptions` (e.g. `PUBLIC_TO_EVERYONE`, `MUTUAL_FOLLOW_FRIENDS`, `FOLLOWER_OF_CREATOR`, `SELF_ONLY`).
- **Interaction toggles** (optional, default = allowed): `disableComment`, `disableDuet`, `disableStitch` (booleans). Duet/Stitch apply to video only. If the creator-info endpoint reports an interaction is disabled account-side (`commentDisabled` / `duetDisabled` / `stitchDisabled`), set the matching `disable*` to `true` (the server force-disables it regardless).
- **Commercial content disclosure** (optional): set `commercialContent: true` if the post promotes a brand, product, or service, then set `brandOrganic: true` (your own brand) and/or `brandedContent: true` (paid/third-party partnership). If `brandedContent` is true, `privacyLevel` cannot be `SELF_ONLY`.
- **Stories**: Set `platformOptions.mediaType` to `"story"`. One video. Ephemeral (24h).
- Video publish uses an async poll model. No API deletion support.

**Get a TikTok account's posting capabilities** — call this before composing a TikTok post; it returns the allowed privacy levels and which interactions are disabled:

```bash
curl https://socialcannon.app/api/v1/accounts/<account_id>/tiktok/creator-info \
  -H "Authorization: Bearer $TOKEN"
```

Returns `{ creatorNickname, creatorUsername, creatorAvatarUrl, privacyLevelOptions, commentDisabled, duetDisabled, stitchDisabled, maxVideoPostDurationSec }`. Choose `privacyLevel` from `privacyLevelOptions` and respect the `*Disabled` flags.

**Example — publish a public TikTok video with comments on:**
```bash
curl -X POST https://socialcannon.app/api/v1/posts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "accountId": "<account_id>",
    "content": "New track out now!",
    "mediaUrls": ["https://example.com/clip.mp4"],
    "platformOptions": {
      "privacyLevel": "PUBLIC_TO_EVERYONE",
      "disableComment": false,
      "disableDuet": false,
      "disableStitch": false
    }
  }'
```

### YouTube
- Supports regular videos, Shorts, and Community posts. Native scheduling support.
- **Shorts**: Set `platformOptions.mediaType` to `"short"`. Vertical video ≤60s.
- **Community posts**: Set `platformOptions.mediaType` to `"community"`. Text/image post to channel's Community tab.
- Scheduled videos are uploaded as private with a `publishAt` timestamp.

### LinkedIn
- 3,000 char limit. Supports text-only and images (single or multi-image). Threads combine all items into one post.
- Scheduling works via SocialCannon (LinkedIn has no native scheduling).
- **No analytics, engagement inbox, or replies** for LinkedIn.

## Rate Limits

- Free tier: 30 requests/minute
- Pro tier: 300 requests/minute
- Agency tier: 600 requests/minute
- Enterprise tier: 1200 requests/minute (default; negotiable)
- Returns `429` with `Retry-After` header when exceeded

## Subscription Tiers

Four tiers. Twitter/X is the only platform with a per-post API cost passed through, so every tier carries an X-write quota.

### Free — $0
- 2 connected accounts
- 10 posts per billing period
- **3 Twitter/X posts per billing period** (thread items count individually)
- 2 scheduled posts at a time
- 3 media uploads per billing period
- 2-item threads, 5 tracked links
- Twitter/X, Facebook only — Instagram, LinkedIn, TikTok, YouTube are Pro+
- No analytics, no engagement replies, no A/B testing, no timing suggestions
- 30 API requests/minute

### Pro — $15/month
- Unlimited accounts, posts, scheduling on free platforms
- **50 Twitter/X posts per billing period**
- All 6 platforms: Twitter/X, Facebook, Instagram, LinkedIn, TikTok, YouTube
- Analytics with history, 90-day calendar
- 25-item threads, unlimited tracked links
- A/B testing (5 concurrent, 4 variants)
- Engagement replies, timing suggestions
- 300 API requests/minute

### Agency — $49/month
- Everything in Pro
- **250 Twitter/X posts per billing period**
- A/B testing (20 concurrent, 6 variants)
- 365-day calendar range
- Priority support
- 600 API requests/minute

### Enterprise — custom contract
- Custom Twitter/X quota, custom rate limits, SLA, dedicated support
- Contact `sales@socialcannon.app`

### Hitting a cap

Any tier exceeding its `maxTwitterPostsPerPeriod` cap returns:
```json
{
  "success": false,
  "error": "Twitter/X post limit reached (50/50). Upgrade to Pro for unlimited Twitter publishing.",
  "code": "LIMIT_EXCEEDED",
  "limit": { "type": "twitter_posts_per_period", "current": 50, "max": 50, "tier": "pro" }
}
```
HTTP `403`. Resets at the start of the next billing period.

## Support

If you run into issues with the API, account connections, or integration setup, contact **support@socialcannon.app**.

## Tips for Agents

1. Always list accounts first to get valid `accountId` values before creating posts.
2. Use the calendar endpoint to check for gaps before suggesting new posts.
3. For Instagram and TikTok, always include at least one media URL — text-only posts will fail.
4. Use `autoUtm: true` in `platformOptions` to automatically tag URLs in posts.
5. Check analytics after 24+ hours for meaningful engagement data.
6. When repurposing content, review the returned `validation` field — if `valid` is false, adjust the content before publishing.
7. Use `scheduledAt: "optimal"` to let SocialCannon pick the best posting time automatically (Pro).
8. For batch scheduling, use the auto-schedule endpoint instead of creating posts one by one.
9. For YouTube, set `mediaType` to `"short"` for Shorts or `"community"` for Community tab posts.
10. For TikTok, call `GET /api/v1/accounts/{id}/tiktok/creator-info` first — it returns the allowed `privacyLevelOptions` (pass one as `platformOptions.privacyLevel`; it is required) and which of Comment/Duet/Stitch are disabled (never enable a disabled one).
