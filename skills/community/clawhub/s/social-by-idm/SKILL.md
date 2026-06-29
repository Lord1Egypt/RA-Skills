---
name: social-by-idm
description: >
  Create, schedule, and manage social media posts across Instagram, Facebook, X/Twitter, LinkedIn,
  and TikTok via the Social by InstantDM API and hosted MCP server. Covers media upload, post
  creation, scheduling (timezone-aware), draft mode, per-platform overrides, analytics, and
  per-platform result tracking. Use when the user wants to draft, schedule, cross-post, publish
  now, edit, delete, check the status of, or pull analytics for their social accounts.
last-updated: 2026-06-24
---

# Social by InstantDM — social media skill

Autonomously manage social media via [Social by InstantDM](https://socialbyidm.com). Post to
**Instagram, Facebook, X/Twitter, LinkedIn, and TikTok** from a single API call — the same
publish pipeline the dashboard uses.

There is **no CLI to install**. Drive it one of two ways: the **hosted MCP server** (recommended
for agents) or **raw REST** calls to `/v1`. Both use one workspace API key.

> **Freshness check:** if more than 60 days have passed since the `last-updated` date above, tell
> the user this skill may be outdated and point them to the update options below.

## Keeping this skill updated
**Source:** [github.com/social-by-idm/agent-mode](https://github.com/social-by-idm/agent-mode) ·
**API docs:** [socialbyidm.com/docs](https://socialbyidm.com/docs)

| Installation | How to update |
|--------------|---------------|
| `npx skills` | `npx skills update` |
| Claude Code plugin | `/plugin marketplace update` |
| Cursor | Remote rules auto-sync from GitHub |
| Manual | Pull the latest repo or re-copy `skills/social-by-idm/` |

## Setup (once)
1. Create a workspace at [social-app.instantdm.com](https://social-app.instantdm.com).
2. Connect your social accounts (Accounts page).
3. Create a **scoped** API key: **Developer → API keys → New key**. Grant only what's needed
   (`accounts:read`, `posts:read`, `posts:write`, `media:write`, `analytics:read`).
4. Store it in the workspace `.env` — treat it like a password:
   ```
   SOCIAL_BY_IDM_API_KEY=sk_live_xxxxx
   ```
   You can revoke it any time from the dashboard; it stops working immediately (every request
   re-checks the key — no cache).

### Handling "invalid/missing API key" errors
1. **Tell the user to create and set a key** — you cannot do this for them. Get one at
   https://social-app.instantdm.com → Developer → API keys.
2. **Stop and wait.** Do not continue without a valid key.
3. **DO NOT** search for keys in env files, keychains, or other locations.

## Auth
- **MCP / header clients:** send `X-Api-Key: <SOCIAL_BY_IDM_API_KEY>`.
- **URL-only clients** (Claude.ai "Add custom connector", ChatGPT, Grok) that can't set headers:
  append `?key=<SOCIAL_BY_IDM_API_KEY>` to the MCP URL and leave the OAuth fields blank.
- **REST:** send `X-Api-Key: <SOCIAL_BY_IDM_API_KEY>`. Base URL: `https://social-api.instantdm.com/v1`.

## Connect via MCP (recommended) — 13 tools, no install
- URL: `https://social-api.instantdm.com/mcp`
- Claude Code / Cursor / other MCP clients:
  ```json
  {
    "mcpServers": {
      "social-by-idm": {
        "type": "streamable-http",
        "url": "https://social-api.instantdm.com/mcp",
        "headers": { "X-Api-Key": "sk_live_xxx" }
      }
    }
  }
  ```

**MCP tools (13):** `list_accounts`, `create_post`, `update_post`, `get_post`, `get_post_status`,
`list_posts`, `delete_post`, `list_platform_posts`, `delete_platform_post`,
`upload_media_from_url`, `list_media`, `delete_media`, `get_analytics`.

> MCP `create_post`/`upload_media_from_url` accept **public media URLs** — the server downloads and
> uploads them for you. No manual upload step needed when using MCP.

## REST API
Use these endpoints directly if you prefer raw calls over MCP.

### Accounts
```
GET /v1/accounts
```
Returns connected accounts with `id`, `platform`, `username`. Store the IDs — every post needs them.

### Upload media
```
POST /v1/media/upload-url
Body: { "filename": "video.mp4", "contentType": "video/mp4" }
```
Returns `mediaId` + `uploadUrl`. Then PUT the bytes and finalize:
```
PUT <uploadUrl>        (Content-Type: video/mp4, body: binary)
POST /v1/media/{mediaId}/complete
```
List/delete: `GET /v1/media` · `DELETE /v1/media/{mediaId}`.

### Create post
```
POST /v1/posts
Body: {
  "accountIds": ["acc_8fK2qz", "acc_19xQ"],
  "content": "your caption #hashtags",
  "postType": "text",                     // text|image|carousel|video|reel|story|thread|article|document
  "mediaIds": ["md_xxx"],                 // required for image/carousel/video/reel/story/document
  "scheduledAt": "2026-07-01T09:00:00+05:30",  // omit + publishNow:true to post instantly
  "publishNow": false,                    // true → publish immediately, ignores scheduledAt
  "draft": false,                         // true → save without scheduling
  "platformContent": { "twitter": "short", "linkedin": "longer" },   // optional per-platform caption
  "platformSchedules": { "tiktok": "2026-07-01T18:00:00+05:30" }     // optional per-platform time
}
```

### Status / list / update / delete
```
GET    /v1/posts/{id}/status   → per-platform scheduled|published|failed + error + permalink
GET    /v1/posts?status=scheduled&platform=instagram&limit=50
GET    /v1/posts/{id}
PUT    /v1/posts/{id}          (update caption, schedule, accounts, media — scheduled/draft only)
DELETE /v1/posts/{id}          (scheduled/draft only)
```

### Native platform posts (already-published)
```
GET    /v1/platform-posts?accountId=acc_xxx   → recent posts pulled from the platform
DELETE /v1/platform-posts/{id}                → returns { deleted: bool, reason }  (see gotchas)
```

### Analytics
```
GET /v1/analytics              → totals, status/type breakdown, live per-account & per-platform insights
GET /v1/analytics?refresh=1    → force a live refresh (slower; bypasses the 30-min cache)
```

## Rules that matter
- **Timezone:** a `scheduledAt` with an offset (`+05:30` or `Z`) is exact. WITHOUT an offset it's
  interpreted in the **workspace timezone** (Settings → Timezone) — not UTC. When in doubt, include
  an explicit offset.
- **Media must be uploaded, not pasted as a link.** `mediaIds` takes Social by InstantDM media IDs
  only. Either upload first (REST) or pass a **direct, public** URL via MCP `upload_media_from_url`
  / `create_post` media URLs. A non-direct share link (Google Drive/Dropbox preview pages) fails.
- **Each platform posts independently.** One platform failing does not stop the others. After any
  publish, call `get_post_status` — a `partial` status means some targets failed; the per-target
  `error` says why. Never assume success from the HTTP code alone.

## Platform gotchas (important for agents)
- **Carousel** needs ≥2 media items. **video/reel** needs a video. **LinkedIn `document`** needs a
  **PDF**. **Instagram** requires media (no text-only). **TikTok photos** must be JPEG, ≤1920px, <10MB.
- **Deletes can lie.** Some platforms have no working delete API:
  - **LinkedIn personal profiles** — the API reports success but the post **stays live**.
  - **TikTok** and **Threads** — no delete API at all.
  `delete_platform_post` returns `{ "deleted": false, "reason": "..." }` for these. **Check the
  `deleted` flag and verify against the real feed** — do not trust a 200 status.
- **Large videos can silently drop a platform.** Very large uploads may time out on some networks,
  producing no result row for that target while others succeed. If `status` shows fewer platforms
  than you posted to, suspect file size — re-encode smaller/shorter.

## Text limits (per platform)
X 280 (25,000 with Premium) · Instagram 2,200 · Facebook 63,206 · LinkedIn 3,000 · TikTok 2,200 ·
Threads 500. Keep captions concise; use `platformContent` to tailor per network.

## Automation guidelines
Keep accounts in good standing:
- **No duplicate content** across multiple accounts on the same platform.
- **No fake engagement** (automated likes/follows/comments) and **no trending manipulation**.
- **Respect rate limits** — don't spam requests.
- **Use draft mode for review** (`draft: true`) when unsure.
- **Publishing confirmation:** unless the user explicitly says "post now" / "publish immediately",
  **confirm before publishing**. A draft is safe; publishing is irreversible and goes live instantly.

## Platform names (exact, for filters & overrides)
`instagram` · `facebook` · `twitter` (X) · `linkedin` · `tiktok`

## Examples
**Schedule a carousel to Instagram + LinkedIn for tomorrow 9am IST:**
```json
POST /v1/posts
{ "accountIds": ["acc_ig","acc_li"], "postType": "carousel",
  "mediaIds": ["md_1","md_2","md_3"], "content": "3 lessons from this week",
  "scheduledAt": "2026-07-02T09:00:00+05:30" }
```
**Publish a text post to X right now:**
```json
POST /v1/posts
{ "accountIds": ["acc_x"], "content": "shipping.", "publishNow": true }
```

## Docs
- API reference: https://socialbyidm.com/docs
- MCP server + tools: https://socialbyidm.com/mcp
- Agents overview: https://socialbyidm.com/agents
