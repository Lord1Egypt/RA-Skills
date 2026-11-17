# ZARZOOM API error codes

Every ZARZOOM API error response uses this envelope:

```json
{
  "error": {
    "code": "<machine-readable>",
    "message": "<human-readable>",
    "details": { /* structured extras */ },
    "request_id": "<uuid>"
  }
}
```

The `request_id` is what ZARZOOM support needs to trace an error.

## Per-code recovery

### 400 / `validation_failed`

The request body failed schema validation. `details.issues` is an
array of Zod-style issues — each has `path`, `code`, `message`.

**Recovery:** read the issues, summarise in plain English for the
user, ask them to revise. Common cases:
- Title or body too long → ask the user to shorten.
- Image alt-text length mismatch with image_keys → either supply alts
  for every image or drop the alts array entirely.
- Hashtag > 64 chars → trim it.
- `image_keys` exceeds 10 entries → split into multiple submissions.

### 401 / `unauthorized`

The API key is missing, malformed, revoked, or rejected. This usually
means `ZARZOOM_API_KEY` is unset or stale.

**Recovery:** tell the user verbatim:

> "Your ZARZOOM API key isn't working. Create a new one at
> https://zarzoom.com/dashboard/api-keys and paste it into your
> `~/.openclaw/openclaw.json` under
> `skills.entries.zarzoom.env.ZARZOOM_API_KEY`."

### 403 / `forbidden`

The key is valid but lacks the required scope, or the workspace
exceeded a plan-level limit (e.g. the 10-posts-per-24h cap).

**Recovery:** `details.reason` (if present) explains. Common cases:
- Missing scope → tell the user to create a new key with the right
  scope at /dashboard/api-keys.
- Daily-post limit → wait until tomorrow OR upgrade plan.

### 422 / `upload_not_found`

The `image_keys[]` or `video_key` references an R2 key that has no
bytes (the PUT to the presigned URL never landed, or the key was
never minted).

**Recovery:** retry the presign + PUT for the affected key, then
resubmit with the new key.

### 422 / `upload_not_in_workspace`

The upload key belongs to a different workspace's prefix
(`uploads/<other-ws-id>/...`).

**Recovery:** mint a fresh presign on this workspace. Don't try to
reuse keys across workspaces.

### 422 / `idempotency_key_conflict`

The same `Idempotency-Key` was used for a different request body
within the last 24 hours. ZARZOOM detects body drift via SHA-256.

**Recovery:** generate a fresh UUID v4 and retry.

### 429 / `rate_limit_exceeded`

Either the per-key read rate limit (60/min) or the workspace-wide
write cap (40/day) was hit. The response includes:
- `X-RateLimit-Limit`
- `X-RateLimit-Remaining`
- `X-RateLimit-Reset` (ISO 8601)
- `Retry-After` (seconds)

**Recovery:** tell the user when they can retry (translate
`X-RateLimit-Reset` to a relative time). Don't auto-retry blindly —
ask before the next attempt.

### 5xx / `internal_error` / `service_unavailable`

ZARZOOM had a transient problem. Retry once after 5–10 seconds. If it
fails again, surface the `request_id` to the user so they can quote
it to support.

## Always surface

When telling the user about ANY error:

- The friendly **what** ("your key isn't working", "image upload
  didn't land").
- The friendly **what to do next** (concrete URL or action).
- If the error is unrecoverable, share the `request_id` so ZARZOOM
  support can trace it.

Never dump raw JSON to the user. Translate.
