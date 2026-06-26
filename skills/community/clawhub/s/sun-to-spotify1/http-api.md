# Sun Public HTTP API

Direct HTTP reference for environments where the `sun` CLI isn't available. Same operations as the CLI; identical wire formats. The API generates audio experiences — podcasts, audiobooks, or audio courses — from a prompt.

All paths under `/v1/public/`. JSON in, JSON out, UTF-8. Set `BASE` to the deployment URL (production, staging, or `http://127.0.0.1:8000` for local dev).

```bash
BASE="https://<your-sun-api-host>"
```

## Auth flows

| Endpoint family | Auth header | Token type |
| --- | --- | --- |
| `/v1/public/tokens*` | `Authorization: Bearer <jwt>` | Supabase JWT |
| `/v1/public/courses*`, `/v1/public/whoami` | `Authorization: Bearer sk_live_...` | Personal API token |

Token-management endpoints reject API-token auth. A leaked API token cannot mint replacements.

## Bootstrap from email + password

The public `auth-config` endpoint exposes the Supabase URL + anon key (both are public — same values every browser client embeds). Discover them dynamically rather than hard-coding:

```bash
CFG=$(curl -s "$BASE/v1/public/auth-config")
SUPABASE_URL=$(echo "$CFG" | jq -r .supabase_url)
SUPABASE_ANON_KEY=$(echo "$CFG" | jq -r .supabase_anon_key)
```

Exchange email + password for a JWT via Supabase's password grant:

```bash
JWT=$(curl -sX POST "$SUPABASE_URL/auth/v1/token?grant_type=password" \
  -H "apikey: $SUPABASE_ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"..."}' \
  | jq -r .access_token)
```

A valid JWT is what `/v1/public/tokens` calls require. Anonymous Supabase users get `403 forbidden` on token mint by design.

## Mint a personal API token

```bash
curl -sX POST "$BASE/v1/public/tokens" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{"name":"laptop"}'
```

Response — `201 Created`:

```json
{
  "id": "...",
  "name": "laptop",
  "prefix": "sk_live_aaaaaaaaaaaaaaaaaaaaaa",
  "token": "sk_live_aaaaaaaaaaaaaaaaaaaaaa_bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
  "created_at": "..."
}
```

The `token` field is the **full secret**, returned exactly once. Store it somewhere safe (env var, secret manager) — there's no way to recover it after this response.

`name` must match `^[a-z0-9-]+$`, 1-64 chars, unique per user. Duplicate name → `409 conflict`. Malformed name → `422 validation_error`.

### List tokens

```bash
curl -s "$BASE/v1/public/tokens" -H "Authorization: Bearer $JWT"
```

Response — `200 OK`:

```json
{
  "tokens": [
    {
      "id": "...",
      "name": "laptop",
      "prefix": "sk_live_aaaaaaaaaaaaaaaaaaaaaa",
      "created_at": "...",
      "last_used_at": "...",
      "revoked_at": null
    }
  ]
}
```

No secrets are ever returned by the list endpoint.

### Revoke a token (idempotent)

```bash
curl -X DELETE "$BASE/v1/public/tokens/<id>" -H "Authorization: Bearer $JWT"
# 204 No Content
```

Second call still returns `204`. `404` if the id is unknown or owned by another user. Soft-revoked tokens remain visible in `list` for audit; they can no longer authenticate.

## Verify a token

```bash
TOKEN="sk_live_..._..."
curl -s "$BASE/v1/public/whoami" -H "Authorization: Bearer $TOKEN"
# 200 → { "user_id": "...", "token_id": "..." }
```

Use this to confirm a token works before kicking off a generation.

## Generate audio (podcast / audiobook / audio course)

> The HTTP path is still `/v1/public/courses/*`, the `course_id` response field, and the `lectures[]` array name are stable API identifiers — they predate the broadened framing and won't be renamed. The CLI subcommand was renamed to `sun audio`; the wire format is unchanged. The user-facing concept (podcast / audiobook / audio course) is independent of these wire identifiers.

```bash
curl -sX POST "$BASE/v1/public/courses" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
        "prompt": "A 30-minute course on the French Revolution",
        "duration_minutes": 30
      }'
```

Response — `202 Accepted`:

```json
{
  "job_id": "ce7a...uuid",
  "course_id": "f0a1...uuid",
  "status": "PENDING",
  "status_url": "/v1/public/courses/ce7a.../status",
  "result_url": "/v1/public/courses/ce7a...",
  "rate_limit": { "limit": 3, "remaining": 2, "reset_at": null }
}
```

### Request body

| Field | Required | Type | Constraints |
| --- | --- | --- | --- |
| `prompt` | yes | string | 1-4000 chars. Topic for the audio (podcast, audiobook, or audio course). |
| `duration_minutes` | no | int | 5-120, default 30 |
| `voice_id` | no | uuid string | optional voice override |
| `callback_url` | no | https URL | The server POSTs `{event, job_id, episode_id, episode_number, title, audio_url}` to this URL every time an episode finishes generating. Fire-and-forget (5s timeout, failures logged + swallowed). Treat as a hint; re-fetch the manifest for truth. |

Unknown fields → `422 validation_error` (every model enforces `extra='forbid'`).

### Episode-ready webhook payload

If `callback_url` was set on create, the server POSTs this body to it as each episode finishes:

```json
{
  "event": "episode_ready",
  "job_id": "ce7a...uuid",
  "episode_id": "...",
  "episode_number": 1,
  "title": "Causes",
  "audio_url": "https://...l1.mp3"
}
```

The receiver should respond `2xx`. Non-2xx, timeouts, and network errors are logged server-side but do not retry — the manifest endpoint (`GET /v1/public/courses/{job_id}?include_partial=true`) remains the reliable source of truth for clients that miss a webhook.

## Poll status

```bash
curl -s "$BASE/v1/public/courses/$JOB_ID/status" \
  -H "Authorization: Bearer $TOKEN"
```

Response — always `200`, even on `ERROR`:

```json
{
  "job_id": "ce7a...",
  "course_id": "f0a1...",
  "status": "PENDING",
  "created_at": "2026-05-08T10:00:00Z",
  "updated_at": "2026-05-08T10:00:01Z",
  "error": null,
  "progress": null
}
```

When `status == "ERROR"`:

```json
{
  "status": "ERROR",
  "error": { "message": "...", "retryable": true },
  "...": "..."
}
```

`progress` is `0-100` when populated; `null` until the worker reports it.

Recommended cadence: first poll at **5s**, then exponential back-off capped at 30s. Total client-side timeout 30 min. Typical 30-min course completes in 60-300s.

```bash
while true; do
  S=$(curl -s "$BASE/v1/public/courses/$JOB_ID/status" \
        -H "Authorization: Bearer $TOKEN" | jq -r .status)
  echo "status: $S"
  case "$S" in SUCCESS|ERROR) break ;; esac
  sleep 10
done
```

## Fetch the result

```bash
curl -s "$BASE/v1/public/courses/$JOB_ID" \
  -H "Authorization: Bearer $TOKEN"
# Add ?include_partial=true to fetch whatever's ready while the job is still
# PENDING/PROCESSING. Without it, the server returns 409 not_ready until SUCCESS.
curl -s "$BASE/v1/public/courses/$JOB_ID?include_partial=true" \
  -H "Authorization: Bearer $TOKEN"
```

Response — `200 OK`:

```json
{
  "job_id": "ce7a...",
  "course_id": "f0a1...",
  "name": "A 30-minute course on the French Revolution",
  "description": "...",
  "duration_ms": 1800123,
  "image_url": "https://...",
  "audio_format": "mp3",
  "lectures": [
    {
      "number": 1,
      "title": "Causes",
      "duration_ms": 360000,
      "image_url": "https://...",
      "audio_url": "https://...signed.../l1.mp3?token=..."
    }
  ],
  "generation": {
    "cost_usd": 0.42,
    "completed_at": "2026-05-08T10:08:33Z"
  }
}
```

`409 not_ready` while the job is in `PENDING` or `PROCESSING` (without `?include_partial=true`):

```json
{
  "error": {
    "code": "not_ready",
    "message": "Job not ready. Poll the status_url until status='SUCCESS'.",
    "status": "PROCESSING",
    "status_url": "/v1/public/courses/ce7a.../status"
  }
}
```

With `?include_partial=true`, the same endpoint returns `200` even mid-generation. Episodes still in progress appear in `lectures[]` with `audio_url: null`; course-level fields (e.g. `image_url`, `description`) may also be null until the worker fills them in. `ERROR` jobs still return `409 not_ready` even with the flag — read `/status` for error details.

Signed `audio_url` values are valid for 7 days, but the result endpoint **re-signs them on every read**. Don't cache them long-term — re-fetch the result if you need fresh URLs.

## Download per-lecture audio

```bash
curl -s "$BASE/v1/public/courses/$JOB_ID" \
  -H "Authorization: Bearer $TOKEN" \
  | jq -r '.lectures[] | "\(.number)\t\(.audio_url)"' \
  | while IFS=$'\t' read -r n url; do
      [ -n "$url" ] && [ "$url" != "null" ] || continue
      curl -sL "$url" -o "lecture-$(printf %03d "$n").mp3"
    done
```

Lectures with `audio_url == null` (storage propagation lag) are skipped — re-fetch the result endpoint a few seconds later to retry.

## End-to-end (Python `httpx`)

```python
import httpx, time

TOKEN = "sk_live_..._..."
BASE = "https://<your-sun-api-host>"
H = {"Authorization": f"Bearer {TOKEN}"}

with httpx.Client(base_url=BASE, headers=H, timeout=30) as c:
    r = c.post("/v1/public/courses", json={
        "prompt": "A 30-minute course on the French Revolution",
        "duration_minutes": 30,
    })
    r.raise_for_status()
    job = r.json()["job_id"]

    delay = 5
    while True:
        s = c.get(f"/v1/public/courses/{job}/status").json()["status"]
        if s in ("SUCCESS", "ERROR"):
            break
        time.sleep(delay)
        delay = min(30, delay * 2)

    if s != "SUCCESS":
        raise SystemExit(f"job {job} ended in ERROR")

    result = c.get(f"/v1/public/courses/{job}").json()
    for lec in result["lectures"]:
        if not lec["audio_url"]:
            continue
        with c.stream("GET", lec["audio_url"]) as resp:
            with open(f"l{lec['number']:03d}.mp3", "wb") as f:
                for chunk in resp.iter_bytes():
                    f.write(chunk)
```

## Rate-limit headers

Set on every public-API response:

```
X-RateLimit-Limit:     3
X-RateLimit-Remaining: 2          # or "unlimited"
X-RateLimit-Reset:     1714074000 # epoch seconds; only when the limit applies
Retry-After:           12345      # seconds; only on 429
```

`429 rate_limit_exceeded` body:

```json
{
  "error": {
    "code": "rate_limit_exceeded",
    "message": "You have used 3 of your 3 daily generations. Try again later.",
    "limit": 3,
    "used": 3,
    "reset_at": "2026-05-09T01:00:00Z"
  }
}
```

What counts toward quota: rows in `PENDING`, `PROCESSING`, or `SUCCESS` created via the public API. `ERROR` rows release their slot. Web-app and voice-agent generations don't count.

Prefer `Retry-After` over computing waits from `reset_at`.

## Error envelope

Every non-2xx response uses the bare envelope:

```json
{ "error": { "code": "snake_case", "message": "...", "<extras>": "..." } }
```

| HTTP | `code` | Meaning |
| --- | --- | --- |
| 401 | `unauthorized` | Missing / malformed / unknown / revoked token |
| 403 | `forbidden` | Anonymous Supabase user attempting to mint an API token |
| 404 | `not_found` | Resource doesn't exist OR is owned by another user (cross-user access never returns 403 — it returns 404) |
| 409 | `conflict` | Duplicate token name on `POST /v1/public/tokens` |
| 409 | `not_ready` | `GET /v1/public/courses/{job_id}` while the job is not yet `SUCCESS` |
| 422 | `validation_error` | Body failed schema validation; details in `error.details`. Unknown fields also → 422 |
| 429 | `rate_limit_exceeded` | Per-user 24h cap exceeded |
| 500 | `internal_error` | Server-side failure; safe to retry with back-off |

Both `409 conflict` and `409 not_ready` share the HTTP status — branch on `error.code`, not the status alone.

## Endpoint summary

| Method | Path | Auth | Success | Errors |
| --- | --- | --- | --- | --- |
| `GET` | `/v1/public/auth-config` | none | 200 `{supabase_url, supabase_anon_key}` | — |
| `GET` | `/v1/public/whoami` | API token | 200 `{user_id, token_id}` | 401 |
| `POST` | `/v1/public/tokens` | JWT | 201 token-create response | 401, 403, 409, 422 |
| `GET` | `/v1/public/tokens` | JWT | 200 token-list response | 401 |
| `DELETE` | `/v1/public/tokens/{id}` | JWT | 204 | 401, 404 |
| `POST` | `/v1/public/courses` | API token | 202 course-create response | 401, 422, 429, 500 |
| `GET` | `/v1/public/courses/{job_id}/status` | API token | 200 status response | 401, 404 |
| `GET` | `/v1/public/courses/{job_id}` | API token | 200 result response | 401, 404, 409 not_ready |
| `GET` | `/v1/public/courses/{job_id}?include_partial=true` | API token | 200 result response (may have null fields mid-generation) | 401, 404, 409 not_ready (ERROR jobs only) |
