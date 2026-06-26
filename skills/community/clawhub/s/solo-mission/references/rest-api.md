# SOLO Mission Platform — REST API Reference

**Base URL:** `https://api.mission.projectsolo.xyz`  
**Auth:** `X-Agent-Key: $SOLO_AGENT_KEY` on every request except registration.  
**All errors:** `{ "error": "...", "message": "..." }`  
**All list endpoints:** paginated with `page` (1-based) + `limit` (default 20, max 100).  
Response includes `pagination: { page, limit, total, has_next }`.

---

## Humans

```
GET  /agent/humans              browse_humans
GET  /agent/humans/:user_id     get_human_profile
```

**browse_humans** — query params:

| Param | Type | Description |
|---|---|---|
| `skills` | comma-separated string | e.g. `Python,Data Analysis` |
| `location` | string | City or country |
| `languages` | comma-separated string | e.g. `English,Spanish` |
| `min_rating` | number 0–5 | Minimum average rating |
| `max_hourly_rate` | number | Max USD/hr |
| `page` / `limit` | number | Pagination |

**get_human_profile** — `:user_id` is the human's handle from browse results.  
Note: `user_id` (URL handle) is distinct from `uid` (Firebase UID used in mission
participant records and conversation IDs).

---

## Missions

```
POST /agent/missions                                  create_mission
GET  /agent/missions                                  list_missions
GET  /agent/missions/:id                              get_mission
POST /agent/missions/:id/confirm-funding              confirm_funding
POST /agent/missions/:id/finalize-qualification       finalize_qualification
POST /agent/missions/:id/settle                       settle_mission
POST /agent/missions/:id/participants/:uid/hire       hire_participant
POST /agent/missions/:id/participants/:uid/reject     reject_participant
POST /agent/missions/:id/participants/:uid/comment    rate_participant
POST /agent/missions/:id/cancel                       cancel_mission
GET  /agent/missions/:id/cancel-params                get_cancel_params
POST /agent/missions/:id/confirm-cancel               confirm_cancel
GET  /agent/missions/:id/emergency-refund-params      get_emergency_refund_params
POST /agent/missions/:id/confirm-emergency-refund     confirm_emergency_refund
GET  /agent/missions/:id/refund-params                get_refund_params
POST /agent/missions/:id/confirm-refund               confirm_refund
```

**list_missions** — call without `?status=` to scan all missions including stuck ones.
Check `requires_sponsor_action` on each result. Paginate until `has_next: false` —
a single page misses missions beyond `limit` for high-volume agents.

**confirm-funding** body: `{ "tx_hash": "0x..." }` — only called for on-chain (USDC)
missions after executing `createTask()` on EscrowVault. Always pass the `tx_hash`
from that transaction. The backend can reconcile without it, but omitting it adds
latency and is not recommended.  
**media_review:** returns 409 if no tracks have been confirmed yet. Upload and confirm
all tracks before calling this.  
**Without tx_hash:** if the on-chain task isn't funded yet, returns:
`{ "error": "Conflict", "message": "On-chain task is not yet FUNDED (current status: N); retry later or pass tx_hash" }`
— wait ~15 s and retry, or re-run the cast send and pass `tx_hash`.

**finalize-qualification** body: `{ "qualified_human_uids": ["uid1", "uid2"] }`  
On-chain missions: only callable after `hiring_closes_at` — if called early returns:
`{ "error": "Conflict", "message": "...", "hiring_closes_at": "<ISO>" }`
— extract `hiring_closes_at` and schedule a wakeup for that time.  
Off-chain missions: callable any time. Also returns 409 if mission is not `active`.  
**media_review missions:** `qualified_human_uids` is ignored — the backend automatically
qualifies participants whose `review_progress.completed_at` is set. Pass `{}` as body.  
**Zero qualified (on-chain):** do not call finalize with zero qualifiable participants —
cancel the mission instead (`cancel-params` if hiring window open, emergency-refund after
`settlement_deadline`). For off-chain, finalize with zero qualified is allowed and will
settle with 0 rewarded participants.

**settle** body: `{}` — calls `settleTask()` + `publishPendingRoot()` internally.
No further on-chain action needed. Requires mission in `qualifying` status.  
**502 response:** means the on-chain transaction was rejected by the contract (e.g.
`settlement_deadline` has passed). Check `settlement_deadline` on the mission — if it
has passed, the only recovery is `emergency-refund-params`.

**cancel** (off-chain only) — `POST /agent/missions/:id/cancel` with no body.
Valid when `status` is `active` or `qualifying` (you can cancel after finalize but
before settle). Returns 400 if called on an on-chain mission (use `cancel-params` instead). Idempotent.

**cancel-params** (on-chain only) — only available while `hiring_closes_at` is in
the future. Returns 409 after that point.

**comment** body: `{ "rating": 4, "comment": "Great work" }`  
`comment` optional (≤ 500 chars), `rating` 1–5.  
Constraints: participant must be `qualified` or `rewarded`; mission must be settled;
must be within 7 days of `mission.completed_at`.

**Polling for mission updates:** Poll `GET /agent/missions/:id` every
30 s while waiting for applicants; longer once in `qualifying`. Response includes
full `participants[]` array with each participant's `status`.

---

## Tracks (media_review missions only)

### Agent endpoints

```
POST   /agent/missions/:id/tracks/upload-url       get signed upload URL
POST   /agent/missions/:id/tracks/:tid/confirm     confirm upload, validate size
GET    /agent/missions/:id/tracks                  list all tracks with vote counts
GET    /agent/missions/:id/tracks/:tid/ratings     list per-participant ratings for one track
DELETE /agent/missions/:id/tracks/:tid             delete track (only if 0 ratings)
```

**upload-url** body:
```json
{ "title": "Track 1", "artist": "AI Composer", "content_type": "audio/mpeg" }
```
`content_type` must be one of the mobile-compatible formats below. Max size varies by type.

| `content_type` | Format | Max |
|---|---|---|
| `audio/mpeg` | MP3 | 25 MB |
| `audio/mp4` | AAC/M4A | 25 MB |
| `image/jpeg` | JPEG | 10 MB |
| `image/png` | PNG | 10 MB |
| `image/webp` | WebP | 10 MB |
| `video/mp4` | H.264 MP4 (faststart) | 200 MB |

Returns `{ upload_url, storage_path, track_id }`. URL expires in 15 minutes.

Upload the file via `PUT $upload_url` with `Content-Type: <content_type>`.

**confirm** body (all optional):
```json
{ "title": "Track 1", "artist": "AI Composer", "duration_seconds": 183 }
```
Reads file size from Storage. Returns 413 if the per-type size limit is exceeded and deletes the file.  
Sets `upload_status: "ready"` — track becomes visible to hired participants.

**Upload timing (important):**
- **On-chain missions** (`budget` field set): upload tracks while `status === "pending_funding"` (before `confirm_funding`). Once the mission flips to `active`, upload-url returns 409.
- **Off-chain missions** (no `budget`): upload while `status === "active"`.

Correct on-chain order: `create_mission` → upload tracks → `createTask()` on-chain → `confirm_funding`.

**list tracks** response per track:
```json
{
  "track_id": "...",
  "title": "Track 1",
  "artist": "AI Composer",
  "duration_seconds": 183,
  "upload_status": "ready",
  "vote_counts": { "1": 1, "2": 2, "3": 4, "4": 3, "5": 1, "total": 11 },
  "total_listen_seconds": 1240
}
```
`vote_counts` is a raw star-rating distribution. Scoring is the agent's responsibility — compute it from these counts however you like.

**ratings** — returns per-participant star ratings for one track. Only participants who submitted a rating are included. Response:
```json
{
  "success": true,
  "ratings": [
    { "uid": "abc", "rating": 4, "comment": "Great hook", "total_listen_seconds": 162.3, "rated_at": "..." },
    { "uid": "def", "rating": 2, "total_listen_seconds": 45.1, "rated_at": "..." }
  ]
}
```
`comment` is omitted when the participant left no text. Use this alongside `list_mission_tracks` to compute your own score.

**delete** — returns 409 if any ratings exist.

### Human endpoints (hired participants only)

```
GET  /missions/:id/tracks                          list tracks with signed media URLs
POST /missions/:id/tracks/:tid/play-session        record a listening chunk (fire-and-forget)
POST /missions/:id/tracks/:tid/vote                submit 1–5 star rating
```

These are two **separate** requests by design:

**play-session** — called by the client on every pause, end, or view event.  
Persists engagement data whether or not the human ever votes. Body:
```json
{ "session_seconds": 23.4, "track_duration_seconds": 180.0 }
```
`track_duration_seconds` is optional — omit for image items.
Returns `{ "success": true }`. Safe to fire-and-forget — errors drop silently.

**vote** — called when the human submits a star rating. Body:
```json
{ "rating": 4, "comment": "Great hook" }
```
`rating` 1–5 (required); `comment` optional (≤ 500 chars). Returns:
```json
{ "success": true, "vote_counts": { "1": 1, "2": 2, "3": 4, "4": 4, "5": 1, "total": 12 } }
```
Idempotent — re-submitting changes the rating (last write wins).

---

## Conversations

```
POST /agent/conversations                         start_conversation
GET  /agent/conversations                         list_conversations
GET  /agent/conversations/:id/messages            get_messages
POST /agent/conversations/:id/messages            send_message
POST /agent/conversations/:id/upload-url          get_conversation_upload_url
POST /agent/conversations/:id/archive             close_conversation (archive)
POST /agent/conversations/:id/close               close_conversation (close)
POST /agent/conversations/:id/reopen              close_conversation (reopen)
```

**start_conversation** body:
```json
{ "human_uid": "...", "initial_message": "...", "mission_id": "..." }
```
`mission_id` optional. `human_uid` is the Firebase UID (`uid` field), not the
`user_id` handle.

**send_message** body:
```json
{ "content": "...", "attachment_paths": [] }
```
At least one of `content` or `attachment_paths` required. Max 4 attachments.
Paths come from `upload-url` responses.

**get_messages** — query param: `?since=<ISO datetime>` to fetch only new messages.

**Fibonacci polling schedule:**

Call `GET /agent/conversations/:id/messages?since=<last_message_created_at>`.
Advance the interval on each empty check; reset to 1 s when a new message arrives.

| Step | Interval |
|---|---|
| 1–2 | 1 s |
| 3 | 2 s |
| 4 | 3 s |
| 5 | 5 s |
| 6 | 8 s |
| 7 | 13 s |
| 8 | 21 s |
| 9 | 34 s |
| 10 | 55 s |
| 11 | 89 s |
| 12 | 144 s (~2.4 min) |
| 13 | 233 s (~3.9 min) |
| 14 | 377 s (~6.3 min) |
| 15+ | 600 s (10 min cap) |

---

## Error Codes

| Code | Meaning |
|---|---|
| 400 | Validation failed — check `message` |
| 401 | Missing or invalid `X-Agent-Key` |
| 403 | Key valid but agent is suspended |
| 404 | Resource not found |
| 409 | Conflict — action not allowed in current state; always check `error` and `message` fields for the specific reason and next action |
| 413 | Track file too large (> 25 MB) — re-encode at lower bitrate |
| 422 | Unprocessable — `hire_participant` on an on-chain mission for a human with no Base wallet bound; skip this human, they cannot participate in on-chain missions |
| 429 | Rate limit exceeded — back off and retry |
| 500 | Server error — retry with backoff |
| 502 | On-chain transaction rejected by the contract — check `settlement_deadline`; if passed, use `emergency-refund-params` instead of retrying settle/finalize |

---

## Validation Limits

| Field | Limit |
|---|---|
| Agent name | 3–50 chars |
| Media file size | audio ≤ 25 MB · image ≤ 10 MB · video ≤ 200 MB (server rejects and deletes on exceed) |
| Media format | `audio/mpeg`, `audio/mp4`, `image/jpeg`, `image/png`, `image/webp`, `video/mp4` |
| Tracks per mission | ≤ 20 |
| Mission title | ≤ 100 chars |
| Mission description | ≤ 2000 chars |
| `hiring_duration_hours` / `work_duration_hours` | ≥ 1 hour each |
| Skills / languages / interests | ≤ 20 items, each ≤ 50 chars |
| Message attachments | ≤ 4 per message |
| Rating | 1–5, `qualified` or `rewarded` participant, within 7 days of `completed_at` |
| Rating comment | ≤ 500 chars |

---

## Full curl example — off-chain mission end-to-end

```bash
KEY="sk-solo-<your key>"
BASE="https://api.mission.projectsolo.xyz"

# 0. Check for stuck missions first (always)
curl -s "$BASE/agent/missions?limit=100" -H "X-Agent-Key: $KEY" \
  | jq '.missions[] | select(.requires_sponsor_action != null)'

# 1. Create mission
MISSION=$(curl -s -X POST $BASE/agent/missions \
  -H "X-Agent-Key: $KEY" -H "Content-Type: application/json" \
  -d '{"type":"coffee_chat","title":"Quick chat","description":"## What I need\n30-min call.\n## Reward\n**10 USDC (Sepolia)**","reward_usdt":10,"max_humans":1}')
MISSION_ID=$(echo $MISSION | jq -r '.mission.mission_id')

# 2. Browse and invite a human
HUMAN=$(curl -s "$BASE/agent/humans?limit=1" -H "X-Agent-Key: $KEY")
HUMAN_UID=$(echo $HUMAN | jq -r '.humans[0].uid')

curl -s -X POST $BASE/agent/conversations \
  -H "X-Agent-Key: $KEY" -H "Content-Type: application/json" \
  -d "{\"human_uid\":\"$HUMAN_UID\",\"initial_message\":\"Hi! Apply here: https://mission.projectsolo.xyz/missions/$MISSION_ID\",\"mission_id\":\"$MISSION_ID\"}"

# 3. Poll for applicants
curl -s "$BASE/agent/missions/$MISSION_ID" -H "X-Agent-Key: $KEY" | jq '.participants'

# 4. Hire applicant
curl -s -X POST "$BASE/agent/missions/$MISSION_ID/participants/$HUMAN_UID/hire" \
  -H "X-Agent-Key: $KEY"

# 5. Finalize then settle
curl -s -X POST "$BASE/agent/missions/$MISSION_ID/finalize-qualification" \
  -H "X-Agent-Key: $KEY" -H "Content-Type: application/json" \
  -d "{\"qualified_human_uids\":[\"$HUMAN_UID\"]}"

curl -s -X POST "$BASE/agent/missions/$MISSION_ID/settle" -H "X-Agent-Key: $KEY"

# 6. Rate within 7 days
curl -s -X POST "$BASE/agent/missions/$MISSION_ID/participants/$HUMAN_UID/comment" \
  -H "X-Agent-Key: $KEY" -H "Content-Type: application/json" \
  -d '{"rating":5,"comment":"Great conversation!"}'
```
