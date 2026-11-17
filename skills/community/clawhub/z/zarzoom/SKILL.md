---
name: zarzoom
description: Submit articles, shorts, and videos to ZARZOOM for multi-platform social posting. Check submission status, pull analytics, see which platforms each post will land on. Uses customer-managed zarz_live_* API keys.
version: 1.0.0
emoji: "🚀"
homepage: https://zarzoom.com/dashboard/api-keys
primaryEnv: ZARZOOM_API_KEY
envVars:
  - name: ZARZOOM_API_KEY
    description: Your ZARZOOM developer API key. Create one at https://zarzoom.com/dashboard/api-keys.
    required: true
requires:
  env: ["ZARZOOM_API_KEY"]
---

# ZARZOOM Skill for OpenClaw

This skill lets the user submit content to ZARZOOM — a multi-platform
social-posting service with built-in compliance moderation — through
natural-language prompts.

ZARZOOM publishes the user's content across their connected social
accounts (Facebook, LinkedIn, X, Instagram, TikTok, YouTube, Threads,
Bluesky, Pinterest, Reddit, Google Business). Every submission goes
through a compliance review by a ZARZOOM admin before it posts; this
is by design and the user should be told about it explicitly on the
first submission.

## Core conventions

- **Base URL:** `https://zarzoom.com/api/v1`
- **Auth header on every call:** `Authorization: Bearer ${ZARZOOM_API_KEY}`
- **Write endpoints require:** `Idempotency-Key: <fresh UUID v4>`
- **Content-Type for JSON bodies:** `application/json`
- **Content-Type for presigned R2 PUTs:** the file's mime type (e.g. `image/jpeg`)

Read endpoints are rate-limited to **60 per minute per key**. Write
endpoints (submits) are rate-limited to **40 per day per workspace**.
If a call returns 429, surface the rate-limit headers to the user
(`X-RateLimit-Reset` is an ISO timestamp).

## Configuration

The user pastes their ZARZOOM API key into `~/.openclaw/openclaw.json`:

```json5
{
  skills: {
    entries: {
      "zarzoom": {
        enabled: true,
        apiKey: {
          source: "env",
          provider: "default",
          id: "ZARZOOM_API_KEY"
        },
        env: {
          ZARZOOM_API_KEY: "zarz_live_..."
        }
      }
    }
  }
}
```

If `ZARZOOM_API_KEY` is unset, refuse to call the API and tell the
user where to get a key: `https://zarzoom.com/dashboard/api-keys`.

---

## Tool: submit an article

**When to use:** the user asks to post, publish, schedule, or share a
longer-form piece of text — typically with a title, body, optional
images, and a choice of which platforms to post to. The body should
arrive as HTML (wrap plain paragraphs in `<p>...</p>` if the user
provides plain text).

**Conversational flow:**

1. Confirm the title, body, hashtags (if any), and target platforms
   with the user. If they haven't specified platforms, ask which ones
   they want — or default to all their connected platforms (call the
   `discover platforms` tool first to find out).

2. **If the user attached one or more images:** for each image, do
   the two-step presigned R2 upload:

   ```
   # Step 1 — get an upload URL
   POST https://zarzoom.com/api/v1/uploads/presign
   Authorization: Bearer ${ZARZOOM_API_KEY}
   Content-Type: application/json
   Idempotency-Key: <fresh UUID>

   { "content_type": "image",
     "mime_type": "image/jpeg",        # or image/png, image/webp
     "file_size_bytes": <bytes> }
   ```

   Response is `{ "data": { "upload_url": "...", "upload_key": "uploads/...", "expires_at": "..." }, "meta": { ... } }`. Read `data.upload_key` (and PUT to `data.upload_url`).

   ```
   # Step 2 — PUT the bytes directly to R2
   PUT <upload_url>
   Content-Type: image/jpeg            # match the mime_type from step 1

   <raw bytes>
   ```

   Collect every returned `data.upload_key` into an array. Do NOT pass
   `data.upload_url` or `data.expires_at` to the submit call — only the key.

3. Submit the article:

   ```
   POST https://zarzoom.com/api/v1/content/articles
   Authorization: Bearer ${ZARZOOM_API_KEY}
   Content-Type: application/json
   Idempotency-Key: <fresh UUID>

   {
     "title": "...",
     "body": "<p>...</p><p>...</p>",
     "image_keys": ["uploads/<ws>/<uuid>.jpg", ...],   # optional
     "image_alts": ["...", ...],                       # optional, must match image_keys.length when present
     "hashtags": ["socialmedia", "marketing"],         # optional, max 10
     "selected_platforms": ["facebook", "linkedin"]    # optional
   }
   ```

4. The response is a 202 Accepted. The body is the standard envelope —
   the submission object lives under `data`, framework metadata under
   `meta`:

   ```json
   {
     "data": {
       "submission_id": "...",
       "status": "pending",
       "message": "Submitted for compliance review.",
       "status_url": "https://zarzoom.com/api/v1/submissions/...",
       "per_platform_status": [
         { "platform": "facebook", "eligible": true },
         { "platform": "linkedin", "eligible": true },
         { "platform": "x",        "eligible": false, "reason": "content_too_long", "message": "Too long for X (1842/280 chars)" }
       ]
     },
     "meta": { "api_version": "1.0", "request_id": "..." }
   }
   ```

5. **Tell the user three things** (read everything off `data`):
   - The submission is **"pending compliance review"** — a ZARZOOM
     admin reviews it before it posts. This is normal. (`data.status`)
   - List the platforms it WILL post to (the `data.per_platform_status`
     entries with `eligible: true`).
   - List the platforms it WILL skip (the `data.per_platform_status`
     entries with `eligible: false`), with the `message` for each.
   - Give them the status URL on the dashboard:
     `https://zarzoom.com/dashboard/my-submissions`

**Body conventions:**
- HTML, not Markdown. If the user gives Markdown or plain text, wrap
  each paragraph in `<p>...</p>` and convert `**bold**` to `<strong>`
  + `*italic*` to `<em>` + bullet lists to `<ul><li>...</li></ul>`.
- Max body length is **20,000 characters** after HTML strip; max
  **3,000 words**. The endpoint will reject longer bodies.
- Inline `<img>` tags in the body are OK but won't be posted to social
  platforms as images — for that, use `image_keys`.

**Per-image conventions:**
- Allowed mime types: `image/jpeg`, `image/png`, `image/webp`.
- Max **30 MB** per image.
- Max **10 images** per article.
- `image_alts[]` (if provided) must have the same length as `image_keys[]`.

---

## Tool: submit a short

**When to use:** the user asks to post a quick text-only or
text-plus-one-image piece. Shorts are constrained to 50–150 words.

**Conversational flow:**

1. Confirm the text and target platforms. If the user attached an
   image, do the presigned upload as in step 2 of the article tool —
   shorts take at most one image.

2. Submit:

   ```
   POST https://zarzoom.com/api/v1/content/shorts
   Authorization: Bearer ${ZARZOOM_API_KEY}
   Content-Type: application/json
   Idempotency-Key: <fresh UUID>

   {
     "text": "...",
     "image_key": "uploads/<ws>/<uuid>.jpg",           # optional, single image only
     "hashtags": ["..."],                              # optional, max 10
     "selected_platforms": ["x", "bluesky", "threads"] # optional
   }
   ```

3. Response is the same 202 envelope as articles — read the submission
   fields off `data` (`data.submission_id`, `data.status`,
   `data.per_platform_status`). Surface the same three things to the user.

**Constraints:**
- **50–150 words.** Outside this range gets rejected by the API.
- Single image only (use `image_key`, not `image_keys[]`).
- Same image mime / size rules as articles.

---

## Tool: submit a video

**When to use:** the user asks to post a video clip with a caption.
Often "post my reel" or "share this video."

**Conversational flow:**

1. Confirm the caption and target platforms.

2. Presigned upload for the video (mime `video/mp4` or `video/webm`,
   max 100 MB):

   ```
   POST https://zarzoom.com/api/v1/uploads/presign
   { "content_type": "video", "mime_type": "video/mp4", "file_size_bytes": <bytes> }
   ```

   PUT the bytes. Collect the resulting `data.upload_key` → that's `video_key`.

3. **Optional but strongly recommended:** if the user attached a
   thumbnail image, do a SECOND presigned upload for the thumbnail
   (mime `image/jpeg` or `image/png`, max 30 MB) — that's `thumb_key`.

4. Submit:

   ```
   POST https://zarzoom.com/api/v1/content/videos
   Authorization: Bearer ${ZARZOOM_API_KEY}
   Content-Type: application/json
   Idempotency-Key: <fresh UUID>

   {
     "video_key": "uploads/<ws>/<uuid>.mp4",
     "caption": "...",
     "duration_seconds": 42,                             # optional, ≤ 60
     "thumb_key": "uploads/<ws>/<uuid>.jpg",             # optional
     "hashtags": ["..."],                                # optional
     "selected_platforms": ["instagram", "tiktok"]       # optional
   }
   ```

5. Same 202 envelope — read the submission fields off `data`
   (`data.submission_id`, `data.status`, `data.per_platform_status`).
   Same three things to surface.

**Constraints:**
- Video duration must be ≤ **60 seconds** (the API uses this for
  platform-eligibility — e.g. Instagram Reels caps shorter than
  TikTok). Probe the duration before submitting if you can; if the
  user attached a >60s video, tell them ZARZOOM v1 only supports
  short clips.
- Max **100 MB** video file.
- Caption max **2,200 chars**.

---

## Tool: check submission status

**When to use:** the user asks "did my last submission post?" or
"what's the status of submission X?" or after an admin should have
reviewed by now.

**Call:**

```
GET https://zarzoom.com/api/v1/submissions/<submission_id>
Authorization: Bearer ${ZARZOOM_API_KEY}
```

**Response shape** (standard envelope — the submission is under `data`):

```json
{
  "data": {
    "submission_id": "...",
    "status": "pending" | "approved" | "rejected",
    "content_type": "article" | "short" | "video",
    "created_at": "...",
    "reviewed_at": "..." | null,
    "rejection": { "category": "...", "notes": "..." } | null,
    "per_platform_status": [
      { "platform": "facebook", "eligible": true,  "posted_at": "...", "post_url": "https://facebook.com/..." },
      { "platform": "linkedin", "eligible": true,  "posted_at": null,  "post_url": null },
      { "platform": "x",        "eligible": false, "reason": "content_too_long", "message": "..." }
    ]
  },
  "meta": { "api_version": "1.0", "request_id": "..." }
}
```

**How to translate to the user** (read everything off `data`):
- **`data.status` = 'pending':** "Still in compliance review. Admin hasn't
  looked yet. You'll know within X hours."
- **`data.status` = 'approved' + `data.per_platform_status[].posted_at`
  populated:** "Approved and posted! Here are the URLs: <list each
  `post_url`>."
- **`data.status` = 'approved' + all `posted_at` null:** "Approved —
  engine is about to post to <list eligible platforms>. Check back in a
  few minutes."
- **`data.status` = 'rejected':** "Compliance rejected this one. Reason:
  `<data.rejection.category>` — `<data.rejection.notes>`. You can
  resubmit a revised version from the dashboard."

---

## Tool: list my submissions

**When to use:** "show me my pending submissions" / "what's in my
compliance queue?" / "show me what got rejected this week."

**Call:**

```
GET https://zarzoom.com/api/v1/submissions?status=pending
Authorization: Bearer ${ZARZOOM_API_KEY}
```

Optional query parameters:
- `status=pending|approved|rejected` (omit for all)
- `limit=50` (max 100; default 50)
- `cursor=<opaque>` (for pagination; the next page's cursor is at
  `meta.next_cursor`)

The response is the standard list envelope: `data` is the array of
submissions, `meta.next_cursor` is the pagination cursor (null on the
last page). Render `data` as a short list — date, content type, status,
brief preview. Don't dump the full JSON.

---

## Tool: check my usage

**When to use:** "how many API calls have I made?" / "what can this key
do?" / "how much of my daily write quota is left?" / "when does my key
expire?"

**Call:**

```
GET https://zarzoom.com/api/v1/usage
Authorization: Bearer ${ZARZOOM_API_KEY}
```

Optional query parameters:
- `from` / `to` (ISO 8601) — usage window. Defaults to the last 30 days.

Requires scope `api:read:status` (granted to every key by default).
`data` contains:
- `key` — this key's `scopes`, `expires_at` (null = never), and
  `ip_allowlist` (empty = any IP).
- `usage` — `total_requests` plus `by_endpoint`, `by_day`, `by_status`
  (all counts; workspace-scoped).
- `rate_limit` — `read_per_minute` (60) and the write window
  (`write_per_day`, `write_used_today`, `write_remaining_today`,
  `write_resets_at`).

Use it to answer "what's left today" before a batch of submits, or to
confirm a key's scopes/expiry. Summarise — don't dump the raw arrays.

---

## Tool: list my content

**When to use:** "show me my recent articles" / "what shorts have I
posted?" / "give me my last 10 videos."

**Calls (one per content type):**

```
GET https://zarzoom.com/api/v1/content/articles?limit=20
GET https://zarzoom.com/api/v1/content/shorts?limit=20
GET https://zarzoom.com/api/v1/content/videos?limit=20
Authorization: Bearer ${ZARZOOM_API_KEY}
```

Optional query parameters:
- `limit` (1–100, default 20)
- `cursor` (opaque pagination cursor)
- `since` / `until` (ISO 8601 dates)

Each response is the standard list envelope: `data` is the array of
posts and `meta.next_cursor` is the pagination cursor (null on the last
page). The item shape varies by content type — articles have title +
body; shorts have text; videos have caption + duration. Show the user a
condensed list (title or first 60 chars, date, status).

For details on one item, call the per-id endpoint (the post object is
under `data`):
- `GET /api/v1/content/articles/<id>`
- `GET /api/v1/content/shorts/<id>`
- `GET /api/v1/content/videos/<id>`

---

## Tool: create a post

**When to use:** "post this article" / "schedule a short for 2pm" / "publish
my video."

**Posting is NOT instant.** Every post enters compliance review; once
approved, ZARZOOM posts it. Tell the user that plainly — never imply it went
out immediately.

**Call:**

```
POST https://zarzoom.com/api/v1/posts
Authorization: Bearer ${ZARZOOM_API_KEY}
Idempotency-Key: <fresh UUID>
Content-Type: application/json

{
  "type": "article",                          // or "short" | "video"
  "title": "...", "body": "<p>...</p>",        // the type's fields (see submit tools)
  "selected_platforms": ["linkedin", "x"],     // optional
  "schedule": { "mode": "at", "time": "14:00" } // optional; default { "mode": "now" }
}
```

Upload media first via `/uploads/presign` and reference the keys
(`image_keys` / `image_key` / `video_key`), exactly like the per-type submit
tools. Scheduling is honest: `mode: "now"` = the earliest slot after approval;
`mode: "at"` with `time: "HH:MM"` (24h, the workspace timezone) pins the time,
rolling to the next day if it has already passed. The 202 response carries
`data.scheduled` (the resolved date/time + a note) and
`data.submission_id` / `data.status_url` for polling. Requires
`api:write:content`.

---

## Tool: validate a post (dry run)

**When to use:** before posting, to check what will pass — "will this run on
all my platforms?"

Same body as **create**, but POST to `/api/v1/posts/validate`. It runs the
content + per-platform eligibility checks and returns
`{ valid, errors[], per_platform_status[] }`. It writes NOTHING. Requires
`api:read:content`.

---

## Tool: check the posting queue

**When to use:** "what's posting?" / "did my posts go out?"

```
GET https://zarzoom.com/api/v1/posts/queue?limit=50
Authorization: Bearer ${ZARZOOM_API_KEY}
```

`data` is the per-platform queue, newest first; each item is
`{ post_id, platform, status, posted_at, post_url, error_code, updated_at }`
where status is `pending | posting | posted | failed` and `error_code` is a
safe code (e.g. `delivery_failed`), never a raw provider error. `meta.next_cursor`
paginates. For one post's roll-up, use `GET /api/v1/posts/<id>/status`. Requires
`api:read:status`.

---

## Tool: cancel a post

**When to use:** "cancel that post" / "stop the Friday article" / "withdraw my
submission."

Pick by where the post is:

1. **Before approval** (still in review) — cancel the submission:
   ```
   POST https://zarzoom.com/api/v1/submissions/<submission_id>/cancel
   Authorization: Bearer ${ZARZOOM_API_KEY}
   ```
   Withdraws it so it is never approved or posted. 409 if already approved.

2. **After approval, before it posts** (in the queue) — cancel the queued
   platforms:
   ```
   POST https://zarzoom.com/api/v1/posts/queue/<post_id>/cancel
   Authorization: Bearer ${ZARZOOM_API_KEY}
   ```
   `post_id` comes from the queue. This is PARTIAL by nature: each platform
   reports its own `outcome` (`cancelled` | `already_posting` | `already_posted`
   | `failed`) and `cancelled_count` says how many were actually stopped. Report
   the per-platform result — never say the whole post was cancelled when only
   some platforms were still pending. Something already posted cannot be un-posted.

Both require `api:write:content`.

---

## Tool: read the content calendar

**When to use:** "what's scheduled this week?" / "show my upcoming
posts" / "what's planned for Friday?"

**Call:**

```
GET https://zarzoom.com/api/v1/calendar?from=2026-06-19&to=2026-07-03
Authorization: Bearer ${ZARZOOM_API_KEY}
```

Optional query parameters:
- `from` / `to` (YYYY-MM-DD). Default window: today → today + 14 days.
- `limit` (1–100, default 50)
- `cursor` (opaque; `meta.next_cursor` is null on the last page)

`data` is the array of calendar items. Each carries `planned_date`,
`planned_time`, `content_type`, `status`, `platforms`, the copy
(`headline`, `hook`, `angle`, `cta`, `tone`, `key_points`, `hashtags`),
`viral_strength` (1–10), and — for videos — a 15-minute presigned
`video_url` plus `video_approval_status` + `duration_seconds`. Requires
scope `api:read:content`. Show the user a compact day-by-day list (date,
time, headline, status).

---

## Tool: override a calendar item

**When to use:** "change Friday's headline to …" / "add a note to that
post" / "only post the Tuesday item to LinkedIn and X."

**Call:**

```
PUT https://zarzoom.com/api/v1/calendar/<id>
Authorization: Bearer ${ZARZOOM_API_KEY}
Content-Type: application/json

{
  "worker_instructions": { "headline": "New headline", "hook": "New hook" },
  "user_notes": "Tighten the intro",
  "platforms_override": { "enabled": ["linkedin", "x"] },
  "override_reason": "agent edit"
}
```

Editable fields ONLY: `worker_instructions` (`headline`, `hook`, `angle`,
`cta`, `tone`, `hashtags`, `key_points`), `user_notes`,
`platforms_override`, `override_reason`. Any other field — including
`status` — is rejected with 400. You CANNOT set `status`: ZARZOOM derives
it from the workspace's publishing rule so every edit re-enters
compliance review. Posted / posting items can't be edited (403). This is
a plain update — no `Idempotency-Key` needed. Requires scope
`api:write:content`. The response `data` is the updated item (same shape
as the read).

---

## Tool: read analytics

**When to use:** "how are my posts doing?" / "best post of the month?"
/ "which platform is performing?"

**Three calls cover the analytics surface:**

```
# Overview — workspace-wide totals over a date range
GET https://zarzoom.com/api/v1/me/stats/overview?days=30
Authorization: Bearer ${ZARZOOM_API_KEY}
```

```
# Top performers — N best posts in the window
GET https://zarzoom.com/api/v1/me/stats/top?days=30&limit=10
```

```
# Per-platform breakdown — engagement / reach / followers per platform
GET https://zarzoom.com/api/v1/me/stats/by-platform?days=30
```

Optional `days` parameter: 7, 14, 30, 60, 90 (default 30).

Each analytics response is the standard envelope — the stats object
(`window`, `totals`, `top_articles`/`top_videos`, `platforms`, etc.)
is under `data`. Read every figure off `data.*`.

Translate numbers into plain English:
- "Your top post this month was [title], with X likes and Y impressions."
- "LinkedIn is your strongest platform — X engagements vs Y on Facebook."
- "Total engagements across all platforms: X. Up Y% from last 30 days."

---

## Tool: check per-post status

**When to use:** "did my [specific] post actually land on LinkedIn?"
or "what's happening with post X across platforms?"

**Call:**

```
GET https://zarzoom.com/api/v1/posts/<post_id>/status
Authorization: Bearer ${ZARZOOM_API_KEY}
```

Returns per-platform success / failure with platform URLs under `data`
(`data.status` roll-up + `data.platforms[]`). The per-platform shape
mirrors `per_platform_status` on submissions but is populated after the
engine has actually attempted the post.

---

## Tool: discover platforms

**When to use:** "which platforms am I connected to?" / "what fits on
Twitter vs Instagram?" / before submitting if the user hasn't picked
platforms.

**Call:**

```
GET https://zarzoom.com/api/v1/capabilities/platforms
Authorization: Bearer ${ZARZOOM_API_KEY}
```

Returns the discovery object under `data`: `data.platforms` is the
array of all 11 supported platforms, each with `connected` (boolean for
this workspace), `supports.{article,short,video}`, `limits`
(`max_text_chars`, `max_video_seconds`, `max_image_size_mb`,
`max_video_size_mb`, `images_per_post`), and `requires_image`.

Use this to tell the user which platforms will accept what content.
Particularly useful before submitting — call it once, then guide the
user on what fits.

---

## Handling errors

ZARZOOM's API uses a consistent error envelope:

```json
{
  "error": {
    "code": "validation_failed" | "unauthorized" | "rate_limit_exceeded" | "upload_not_found" | "upload_not_in_workspace" | "idempotency_key_conflict" | "internal_error",
    "message": "human-readable summary",
    "details": { /* structured extras */ },
    "request_id": "..."
  }
}
```

**Per-code recovery:**

- **`401 unauthorized`** — the `ZARZOOM_API_KEY` is missing, malformed,
  or revoked. Tell the user:
  > "Your ZARZOOM API key isn't working. Create a new one at
  > https://zarzoom.com/dashboard/api-keys and paste it into
  > `~/.openclaw/openclaw.json` under `skills.entries.zarzoom.env.ZARZOOM_API_KEY`."

- **`400 validation_failed`** — read `error.details` (structured
  validation detail, e.g. an `issues` array of Zod-style problems).
  Summarise in plain English. Do NOT dump the raw detail.
  - Common causes: body too long, image mime type wrong, hashtag
    over 64 chars, image_alts length mismatch.

- **`422 upload_not_found`** — the `upload_key` you referenced has no
  bytes in R2. The presigned PUT in step 2 of the upload flow likely
  failed. Retry the presign + PUT.

- **`422 upload_not_in_workspace`** — the `upload_key` belongs to a
  different workspace's prefix. This usually means a copy-paste
  mistake; redo the presign for this workspace.

- **`422 idempotency_key_conflict`** — the same `Idempotency-Key` was
  used for a DIFFERENT request body within the last 24 hours. Generate
  a fresh UUID and retry.

- **`429 rate_limit_exceeded`** — read `X-RateLimit-Reset` (ISO
  timestamp). Tell the user when they can retry, and the cap
  (`X-RateLimit-Limit`). Don't auto-retry blindly; ask the user.

- **`5xx internal_error`** — ZARZOOM had a transient problem. Wait
  10 seconds and retry once. If it fails again, ask the user to wait
  and try later; share the `request_id` from the error envelope so
  support can trace it.

---

## Style notes for user-facing output

- **Be concrete, not chatty.** When a submission is created, tell the
  user the submission ID + the platforms + the pending status — three
  short lines. Don't recap their original request back at them.
- **Surface platform URLs whenever they exist** — `post_url` on the
  per-platform status is the most valuable single piece of info for
  the user.
- **Translate dates into relative time when recent** ("2 hours ago",
  "yesterday") and absolute when older ("May 18, 2026"). The API
  returns ISO timestamps; you do the translation.
- **Never dump raw JSON to the user** unless they explicitly ask for
  it. Convert to natural language.
- **Tell users where to go on the dashboard.** Common destinations:
  - `https://zarzoom.com/dashboard/my-submissions` — pending /
    approved / rejected list
  - `https://zarzoom.com/dashboard/api-keys` — manage API keys
  - `https://zarzoom.com/dashboard/api-keys/docs` — full API reference

---

## More details

- Endpoint reference: see `reference/api-endpoints.md` in this skill folder.
- Error code reference: see `reference/error-codes.md`.
- Worked example transcripts: see `reference/examples.md`.
- ZARZOOM's full OpenAPI spec: `https://zarzoom.com/api/v1/openapi.json`
  — fetch this if you need a detail not covered above.

**Anything not covered here, default to:** consult the OpenAPI spec
above OR send the user to `https://zarzoom.com/dashboard/api-keys/docs`.
