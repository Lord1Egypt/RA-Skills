# ZARZOOM API endpoint reference

Quick lookup of every endpoint this Skill calls. For the canonical
spec see `https://zarzoom.com/api/v1/openapi.json`.

All endpoints require:
- `Authorization: Bearer ${ZARZOOM_API_KEY}`
- HTTPS to `https://zarzoom.com/api/v1`

Write endpoints additionally require:
- `Idempotency-Key: <UUID v4>` (a fresh one per logical request)
- `Content-Type: application/json` (unless noted otherwise)

## Uploads

### POST /uploads/presign

Mint a presigned R2 PUT URL for an image or video upload.

| Body field | Type | Required | Notes |
|---|---|---|---|
| content_type | `"image" \| "video"` | yes | |
| mime_type | string | yes | image/jpeg, image/png, image/webp, video/mp4, video/webm |
| file_size_bytes | integer | yes | Used for content-length enforcement on the PUT |

Response 200 (standard envelope — fields under `data`):
```json
{
  "data": {
    "upload_url": "https://<r2-presigned-url>",
    "upload_key": "uploads/<workspace_id>/<uuid>.<ext>",
    "expires_at": "2026-05-25T11:30:00Z"
  },
  "meta": { "api_version": "1.0", "request_id": "..." }
}
```

The presigned URL is valid for **15 minutes**. PUT bytes directly to
`data.upload_url` with the matching `Content-Type` header; ZARZOOM
HEAD-checks the key when the parent submission is created.

## Submissions (writes)

### POST /content/articles

| Body field | Type | Required | Notes |
|---|---|---|---|
| title | string | yes | ≤ 200 chars |
| body | string | yes | HTML; ≤ 20,000 chars after strip, ≤ 3,000 words |
| image_keys | string[] | no | R2 keys from /uploads/presign; ≤ 10 |
| image_alts | string[] | no | Length must match image_keys |
| hero_image_key | string | no | Often image_keys[0] |
| hashtags | string[] | no | ≤ 10; each ≤ 64 chars |
| selected_platforms | string[] | no | Platform keys; omit for all eligible |

Response 202 (standard envelope — submission under `data`):
```json
{
  "data": {
    "submission_id": "uuid",
    "status": "pending",
    "message": "Submitted for compliance review.",
    "status_url": "https://zarzoom.com/api/v1/submissions/<id>",
    "per_platform_status": [
      { "platform": "facebook", "eligible": true },
      { "platform": "x", "eligible": false, "reason": "content_too_long", "message": "..." }
    ]
  },
  "meta": { "api_version": "1.0", "request_id": "..." }
}
```

### POST /content/shorts

| Body field | Type | Required | Notes |
|---|---|---|---|
| text | string | yes | 50–150 words after trim |
| image_key | string | no | Single R2 key |
| hashtags | string[] | no | |
| selected_platforms | string[] | no | |

### POST /content/videos

| Body field | Type | Required | Notes |
|---|---|---|---|
| video_key | string | yes | R2 key from /uploads/presign (content_type: video) |
| caption | string | yes | ≤ 2,200 chars |
| duration_seconds | number | no | ≤ 60 |
| thumb_key | string | no | R2 key for the poster image |
| hashtags | string[] | no | |
| selected_platforms | string[] | no | |

## Status reads

### GET /submissions

Query params: `status`, `limit` (≤ 100, default 50), `cursor`.

Standard list envelope: `data` is the array, `meta.next_cursor` is the
pagination cursor (null on the last page). Each `data[]` item includes
`submission_id`, `content_type`, `status`, `created_at`, `preview`,
`per_platform_status`.

### GET /submissions/{id}

Returns the full submission row under `data`, with
`data.per_platform_status` populated after the engine has posted. See
SKILL.md "Tool: check submission status" for the full shape.

### GET /posts/{post_id}/status

Per-platform success/failure for an approved post after engine fan-out.
The roll-up `status` + `platforms[]` array are under `data`.

## Content reads

### GET /content/articles | /content/shorts | /content/videos

Query params: `limit` (default 20), `cursor`, `since`, `until`.

Standard list envelope: `data` is the array of posts,
`meta.next_cursor` is the pagination cursor (null on the last page).

### GET /content/articles/{id} | /content/shorts/{id} | /content/videos/{id}

Per-item detail — the post object is under `data`.

## Posts (unified)

### POST /posts

Unified create over the typed compliance chain. Scope: `api:write:content`.
Requires `Idempotency-Key`. Posting is async (compliance review → approval →
engine posts).

| Body field | Type | Notes |
|---|---|---|
| type | `"article" \| "short" \| "video"` | required; selects the content fields |
| ...content | — | the type's fields (see Submissions above) |
| selected_platforms | string[] | optional |
| schedule | object | optional; `{ mode: "now" \| "at", time?: "HH:MM" }` (default `now`) |

202 `data`: `{ submission_id, status, message, status_url,
per_platform_status[], scheduled: { mode, planned_date, planned_time, note } }`.
`scheduled` states when posting will begin. Inactive subscription → 402; reused
key + different body → 422.

### POST /posts/validate

READ-ONLY. Same body as create; runs content + eligibility checks and returns
`{ valid, errors[], per_platform_status[] }`. Inserts nothing. Scope:
`api:read:content`.

### GET /posts/queue

READ-ONLY poster queue (allowlist projection — no engine internals, no raw
media keys). Scope: `api:read:status`. Query: `limit` (1..100, default 50),
`cursor`. Each item: `{ post_id, platform, status, posted_at, post_url,
error_code, updated_at }`, status ∈ `pending | posting | posted | failed`.
`error_code` is sanitised (e.g. `delivery_failed`) — never a raw provider error.

### POST /posts/queue/{id}/cancel

Cancel the still-queued platform rows of a post (`id` = the queue's `post_id`).
Scope: `api:write:content`. Race-free (cancels only rows not yet claimed by the
poster). PARTIAL: returns `{ post_id, cancelled_count, platforms: [{ platform,
outcome }] }` where outcome ∈ `cancelled | already_posting | already_posted |
failed`. Never implies a whole-post cancel. 404 if the post has no queue.

### POST /submissions/{id}/cancel

Withdraw a still-pending submission before approval (CAS on status='pending').
Scope: `api:write:content`. Returns `{ submission_id, cancelled, status,
message }`. 409 if already approved/processed; 404 if not found.

## Calendar (read + override)

`PUT /calendar/{id}` is a naturally-idempotent update — it does NOT
require an `Idempotency-Key` (unlike the create-style writes above).

### GET /calendar

List the workspace content calendar (tightened external projection).
Scope: `api:read:content`.

| Query | Type | Default | Notes |
|---|---|---|---|
| from | date (YYYY-MM-DD) | today | inclusive lower bound on planned_date |
| to | date (YYYY-MM-DD) | today + 14d | inclusive upper bound |
| limit | integer | 50 | 1..100 |
| cursor | string | — | opaque; `meta.next_cursor` is null on the last page |

`data` is the array of calendar items; each EXCLUDES every internal field
(tenant id, costs, pipeline columns, director notes) and surfaces video as
a 15-minute presigned `video_url` — never the raw R2 key.

### PUT /calendar/{id}

Override one calendar entry. Scope: `api:write:content`.

| Body field | Type | Notes |
|---|---|---|
| worker_instructions | object | only headline (≤200) / hook (≤300) / angle (≤1000) / cta (≤200) / tone (≤100) / hashtags (≤30×≤100) / key_points (≤20×≤500) |
| user_notes | string \| null | ≤ 2000 |
| platforms_override | object \| null | `{ enabled?: string[], disabled?: string[] }` |
| override_reason | string \| null | ≤ 500 |

Unknown keys (including `status`) → 400. `status` is route-derived, never
agent-set. Posted / posting rows → 403. Every edit forces
`is_user_edited = true`. Response `data` is the updated item.

## Analytics

All three analytics responses use the standard envelope — the stats
object is under `data`.

### GET /me/stats/overview

Query: `days=7|14|30|60|90` (default 30).

`data` holds workspace-wide totals (posts published, engagements,
reach, followers) over the window.

### GET /me/stats/top

Query: `days`, `limit` (≤ 50).

`data` holds the top N posts ranked by engagement.

### GET /me/stats/by-platform

Query: `days`.

`data` holds the per-platform breakdown (engagements, reach, followers,
follower delta) for each connected platform.

## Discovery

### GET /capabilities/platforms

No query params. Standard envelope — `data` holds the discovery object,
whose `data.platforms` is an array of all 11 supported platforms, each
with:

- `id`, `name`, `display_name`
- `connected: boolean` (for THIS workspace)
- `supports: { article: bool, short: bool, video: bool }`
- `limits: { max_text_chars, max_video_seconds, max_image_size_mb, max_video_size_mb, images_per_post }`
- `requires_image: boolean` (Pinterest needs an image; others don't)
- `structural_notes: string[]` (free-text guidance)

## Reference

- OpenAPI 3.1 spec: `https://zarzoom.com/api/v1/openapi.json`
- Customer dashboard: `https://zarzoom.com/dashboard/api-keys`
- Docs page: `https://zarzoom.com/dashboard/api-keys/docs`
