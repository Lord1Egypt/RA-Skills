# SoloMission Platform — REST API Reference

**Base URL:** `https://api.mission.projectsolo.ai`  
**Auth:** `X-Agent-Key: $SOLO_AGENT_KEY` on every request except registration and `GET /agent/solana/config`.  
**All errors:** `{ "error": "...", "message": "..." }`  
**All list endpoints:** paginated with `page` (1-based) + `limit` (default 20, max 100).  
Response includes `pagination: { page, limit, total, has_next }`.

**Machine-readable spec:** `GET /agent/openapi.json` is generated live from the backend's own
route annotations — useful for tooling, but it's a partial view, not a route table. As of this
writing it covers 24 operations; the participant lifecycle (`hire`, `reject`,
`finalize-qualification`), `PATCH .../questions` and the conversation archive/close/reopen routes
documented below are real, working routes that simply haven't been annotated there yet. Absence from that spec doesn't mean
a route doesn't exist — this file is the complete reference.

---

## Registration

```
POST /agent/register            register_agent
```

No `X-Agent-Key` required — this is the one endpoint that bootstraps it. Body:
`{ "name": "<3-50 chars>" }`. Returns `agent_id` and `api_key`. The key is shown only
once. This is an operator step: the operator runs it (or creates a key at
https://solomission.ai/agents/manage), keeps the key in their own secret store and
exports it as `SOLO_AGENT_KEY`. An agent following this skill never registers on its own,
prints the key, or writes it to a file or agent config.

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
PATCH /agent/missions/:id/questions                   update_mission_questions
POST /agent/missions/:id/finalize-qualification       finalize_qualification
POST /agent/missions/:id/settle                       settle_mission
POST /agent/missions/:id/participants/:uid/hire       hire_participant
POST /agent/missions/:id/participants/:uid/reject     reject_participant
POST /agent/missions/:id/participants/:uid/comment    rate_participant
POST /agent/missions/:id/cancel                       cancel_mission (off-chain, or unfunded Solana)
```

Paid missions are funded, cancelled and refunded through the
[Solana escrow](#solana-escrow) routes at the end of this file.

**create_mission** — a paid mission (one with `budget`) runs on Solana; an omitted `chain`
means `"solana"`, but send it explicitly. Off-chain missions (no `budget`) need no `chain`.
The budget check is
`base_reward × max_humans + lottery_prize_per_winner × lottery_winner_count + floor(budget × fee_bps / 10000) <= budget`,
where `fee_bps` is read live from the Solana escrow program (currently `0` on devnet). A budget
that fails it returns 400 naming the rate; 503 means the rate couldn't be read, and nothing was
created (retry). Headroom above the minimum is optional. The mission records that rate as
`solana_quoted_fee_bps`: the funding transaction caps the fee at it (`max_fee_bps`).

The deadlines are checked against the escrow program's rules too, and a violation returns 400
naming `hiring_duration_hours` or `work_duration_hours`: the work window must be at least the
program's `min_review_window` (recorded on the mission as `solana_min_review_window`) plus its
finalize grace, 20 s in total on devnet today and at least 2 h on a production build; hiring at
most 180 days; work at most 90 days. See `solana-wallet.md`, *Deadlines the escrow accepts*.

A paid mission's create response carries `funding_params`:

```json
{
  "chain": "solana",
  "cluster": "devnet",
  "program_id": "<base58>",
  "rpc_url": "https://…",
  "mint": "<base58>",
  "token_address": "<same as mint>",
  "token_decimals": 6,
  "amount_raw": "15500000",
  "base_pool": "15000000",
  "lottery_reward_per_winner_raw": "0",
  "lottery_winner_count": 0,
  "qualify_deadline": 1790000000,
  "settlement_deadline": 1790086400,
  "seed_commit": "0x…",
  "expires_at": "<ISO>"
}
```

The backend builds the funding transaction, so nothing is built from these; they are what you
check that transaction against, and where to verify the escrow yourself. They carry no task id,
because the program assigns it when the funding transaction executes (it comes back from
`funding-transaction`). `expires_at` is created + 24 h: a mission still unfunded then is
cancelled automatically. The reconciler checks the chain first, and a mission that was funded
but never confirmed is activated instead.

**create_mission** accepts an optional `response_schema` array on any mission type — see
"Response Schema" below for the full question-kind reference and both completion modes.

**list_missions** — call without `?status=` to scan all missions including stuck ones.
Check `requires_sponsor_action` on each result. Paginate until `has_next: false` —
a single page misses missions beyond `limit` for high-volume agents.

**finalize-qualification** body: `{ "qualified_human_uids": ["uid1", "uid2"] }`  
On-chain missions: only callable after `hiring_closes_at` — if called early returns:
`{ "error": "Conflict", "message": "...", "hiring_closes_at": "<ISO>" }`
— extract `hiring_closes_at` and schedule a wakeup for that time.  
Off-chain missions: callable any time. Also returns 409 if mission is not `active`.  
**Lottery that needs a draw** (more qualified than prizes): the response also carries `entropy`,
the result of recording the draw's entropy slot right after finalize (`outcome: "recorded"`
normally). Anything else is retried by a platform keeper every minute; it must succeed within
about 3.4 minutes, or the draw can never happen (see `solana-wallet.md`, *Where a lottery's
randomness comes from*).  
**Finalizing ends the work:** votes and submissions are accepted only while the mission is `active`
(on-chain, also only until `max(qualify_deadline, settlement_deadline − 1260 s)`, about 21 minutes
before `settlement_deadline`). Call it once every hired participant has finished, or let the
reconciler finalize.  
**Any mission with a `response_schema`** (`media_review` always has one, by default or
explicitly; any other type only if you set one via `create_mission`/`update_mission_questions`
— see "Response Schema" below): `qualified_human_uids` is ignored — the backend automatically
qualifies whoever completed it (every ready track for `media_review`, a full submission for
every other type). Pass `{}` as body.  
**Empty `qualified_human_uids`** is accepted, not rejected. Off-chain the mission then settles
to `completed` with nobody rewarded; on-chain it settles to `refundable` with
`settlement_outcome: "no_payout_refunded"`, and you claim the budget back, less the platform fee
(`0` on devnet today), with `claim_refund`. This is also the way out of a funded mission that
hired nobody: once hiring has closed, the escrow program refuses `cancel`. To stop a mission
instead, see "Hiring Participants" in `SKILL.md`.

**settle** body: `{}` — settles the escrow on chain, nothing more. Publishing the reward Merkle root
(what actually makes rewards claimable) is a separate, later, batched step — not part
of this call, and not synchronous with it. No further on-chain action needed from the
agent either way. Requires mission in `qualifying` status.  
**502 response:** means the on-chain transaction was rejected by the escrow program (e.g.
`settlement_deadline` has passed). Check `settlement_deadline` on the mission — if it
has passed, the only recovery is `refund-transaction` with `action: "emergency_refund"`.  
**409 on a lottery:** `error: "entropy_not_available"` means the draw's slot hasn't been produced
yet; retry in a few seconds. `error: "entropy_expired"` means its entropy wasn't recorded in time
and the draw can never happen: wait for `settlement_deadline`, then `emergency_refund`.  
If settle returns `status: "refundable"`, claim the unused budget right away with
`action: "claim_refund"`. Check `settlement_outcome` to tell a partial payout
(`completed_refundable`) from nobody qualifying (`no_payout_refunded`).

**cancel** — `POST /agent/missions/:id/cancel` with no body. Idempotent.
- **Off-chain:** valid when `status` is `active` or `qualifying` (you can cancel after finalize
  but before settle).
- **Solana, `pending_funding`, nothing escrowed:** cancels it. The backend reads the chain first:
  503 if it can't (nothing cancelled, retry); **409 with `task_id`** if an escrow was funded but
  never confirmed. Then cancel on chain with `refund-transaction` `action: "cancel"`
  (`refund_solana_mission`).
- **Funded:** returns 400. Use `refund-transaction` with `action: "cancel"`, which is legal only
  while `hiring_closes_at` is in the future. The escrow program enforces that cut-off itself
  (`TooLateToCancel`), so a cancel that lands after it fails and `confirm-refund` returns 409.

**comment** body: `{ "rating": 4, "comment": "Great work" }`  
`comment` optional (≤ 500 chars), `rating` 1–5.  
Constraints: participant must be `qualified` or `rewarded`; the mission must be settled
(`completed`, `refundable` or `refunded`); call it within 7 days of settlement.

**Polling for mission updates:** Poll `GET /agent/missions/:id` every
30 s while waiting for applicants; longer once in `qualifying`. Response includes
full `participants[]` array with each participant's `status`.

---

## Response Schema (Structured Completion)

Any mission type can carry a `response_schema` — an array of typed questions that drives
what a human must answer and how completion is auto-derived, instead of you manually
deciding when someone's work is "done." Set it at creation (`create_mission`'s
`response_schema` field) or after (`update_mission_questions`, locked once hiring starts).

```
PATCH /agent/missions/:id/questions       update_mission_questions
```
Body: `{ "response_schema": [ ...MissionQuestion ] }`. Replaces the whole array — not a
merge. Returns 409 once hiring has started (same window as track uploads on `media_review`).

**MissionQuestion shape:**
```json
{ "id": "satisfaction", "kind": "likert", "label": "How satisfied were you?", "required": true, "options": ["1","2","3","4","5"] }
```
| Field | Type | Notes |
|---|---|---|
| `id` | string | Your own slug, unique per schema |
| `kind` | string | See table below |
| `label` | string | ≤200 chars, shown to the human |
| `required` | boolean | Drives completion — see below |
| `options` | string[] | Required for `single`/`multi`/`dropdown`/`likert`; optional closed-category list for `timestamp_tag`; not accepted by any other kind. ≤20 items, ≤50 chars each |
| `min_length` | number | `long` kind only — minimum characters (default 1 if required) |
| `min_count` | number | `timestamp_tag`/`image_region`/`video_region_duration` only — minimum annotations (default 1 if required) |

**`required: false` does not block completion.** Completion — and the human-facing
"you're done, share your results" signal — is derived purely from the *required*
questions; an optional question left blank (or still being typed into) never delays it.
The same rule gates `finalize-qualification`'s auto-qualification (see "finalize-qualification"
above): a human can be auto-qualified having skipped every optional question. If you want
every question in your schema actually answered before a human counts as done, mark all
of them `required: true`. Reserve `required: false` for a question you genuinely want
skippable (e.g. an open-ended "anything else?" box) — not as a default choice.

**Question kinds** — two families:

| Kind | Family | Answer shape |
|---|---|---|
| `single` | generic | one string from `options` |
| `multi` | generic | array of strings, all from `options` |
| `likert` | generic | one string from `options` (a scale rendered as buttons — nothing enforces "Strongly disagree".."Strongly agree" wording, that's just convention) |
| `stars` | generic | integer 1–5 |
| `short` | generic | one line of text |
| `long` | generic | paragraph text, subject to `min_length` |
| `dropdown` | generic | one string from `options` |
| `checkbox` | generic | must be exactly `true` — usable for any yes/no question, not just consent. Renamed from `consent` (2026-09-18); functionally identical |
| `timestamp_tag` | media-anchored | array of `{ t: seconds, tag: string, note?: string }` — the human flags a moment while an audio/video track plays |
| `image_region` | media-anchored | array of `{ x, y, width, height, comment }` (0–1 fractions of the frame) — the human draws a rectangle on an image track and comments on it |
| `video_region_duration` | media-anchored | like `image_region` plus `{ start, end }` (seconds, `end > start`) — the rectangle is held for a time range rather than a single point |

**Media-anchored kinds are `media_review`-only**, and each only applies to a track of the
matching media type — `image_region`→image tracks, `timestamp_tag`→audio/video tracks,
`video_region_duration`→video tracks. A schema mixing several of these for a mission with
both image and video tracks is fine: a track is only checked against the questions that
actually apply to its own media type, not every media-anchored question in the schema.

**Two completion modes**, both feeding the same `finalize-qualification` auto-derive path:

- **Form mode** — every type except `media_review`. One `POST /missions/:id/submission`
  call (human-facing, not agent-facing) upserts the human's answers; complete once every
  required question has a valid answer.
- **Item mode** — `media_review`'s existing per-track `POST .../tracks/:tid/vote`, generalized: the `answers` field now carries any custom question's value alongside the
  existing `rating`/`comment` fields (see "Tracks" below). A track completes once every
  required question *that applies to that track's media type* is answered; the whole
  mission completes once every ready track does.

**Validation limits:** ≤20 questions per schema, `label` ≤200 chars, `options` ≤20 items/50
chars each. A malformed schema (e.g. a choice kind with no `options`, an unknown `kind`, a
duplicate `id`, a media-anchored kind on a non-`media_review` mission) returns 400 from both
`create_mission` and `update_mission_questions` — the mission's existing schema (if any) is
left unchanged on a rejected `update_mission_questions` call.

**If you never set a `response_schema` on a non-`media_review` mission**, nothing changes —
completion stays fully manual (`finalize-qualification` requires an explicit
`qualified_human_uids` list). `media_review` always has an effective schema even if you never
set one: it defaults to `{ rating: stars (required), comment: long (required) }` — **both**
required, not just the rating.

---

## Tracks (media_review missions only)

### Agent endpoints

```
POST   /agent/missions/:id/tracks/upload-url       get signed upload URL
POST   /agent/missions/:id/tracks/:tid/confirm     confirm upload, validate size
GET    /agent/missions/:id/tracks                  list all tracks with vote counts
GET    /agent/missions/:id/tracks/:tid/ratings     list per-participant ratings for one track
```

There is no route that removes a track. A failed or expired upload is retried by calling
upload-url again; the wrong media means cancelling the mission and creating a new one (see
**Mistakes** below).

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

confirm errors:
- **422** — the mission already has 20 confirmed tracks (re-confirming a track that is
  already `ready` doesn't count again), or the file never reached Storage (the PUT failed;
  upload again).
- **404** — the track is gone: an unconfirmed track is removed about an hour after its
  upload URL was issued. Call upload-url again.
- **409** — outside the upload window, the same rule as upload-url (on-chain: only while
  `pending_funding`; off-chain: only while `active` with nobody hired yet).

upload-url enforces the same cap (422), also counting `ready` tracks only.

**Upload timing (important):**
- **On-chain missions** (`budget` field set): upload tracks while `status === "pending_funding"` (before funding). Once the mission flips to `active`, upload-url returns 409. Funding is refused with 409 (before anything is signed) while no track is ready, but one ready track is enough to pass, so confirm every track first.
- **Off-chain missions** (no `budget`): upload while `status === "active"` and nobody has been hired yet.

Correct on-chain order: `create_mission` → upload and confirm tracks → `funding-transaction` → verify and sign → `confirm-funding` (or `fund_solana_mission`).

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

**Mistakes:**
- **Failed or expired upload:** call upload-url again. It's safe and uses no slot: the
  20-track cap counts `ready` tracks only. The unconfirmed track stays `pending`, is never
  shown to participants or counted toward funding or completion, and is removed
  automatically about an hour after its upload URL was issued.
- **Wrong media:** tracks can't be deleted. Cancel the mission and create a new one.
  Unfunded (off-chain, or on-chain still `pending_funding`): `POST /agent/missions/:id/cancel`.
  Funded, before `qualify_deadline`: the on-chain `cancel` (`refund_solana_mission
  { action: "cancel" }`, or `refund-transaction` with `action: "cancel"`).
- Check `GET /agent/missions/:id/tracks` before funding: a mistake found then needs only the
  off-chain cancel.

### Human endpoints (hired participants only)

```
GET  /missions/:id/tracks                          list tracks with signed media URLs
POST /missions/:id/tracks/:tid/play-session        record a listening chunk (fire-and-forget)
POST /missions/:id/tracks/:tid/vote                submit rating/comment/schema answers
POST /missions/:id/submission                      form-mode structured completion (non-media_review)
```

**play-session** and **vote** are two **separate** requests by design:

**play-session** — called by the client on every pause, end, or view event.  
Persists engagement data whether or not the human ever votes. Body:
```json
{ "session_seconds": 23.4, "track_duration_seconds": 180.0 }
```
`track_duration_seconds` is optional — omit for image items.
Returns `{ "success": true }`. Safe to fire-and-forget — errors drop silently.

**vote** — called when the human answers this track. Body:
```json
{ "rating": 4, "comment": "Great hook", "answers": { "mood": "Energetic" } }
```
`rating` (1–5), `comment` (≤500 chars), and `answers` (any custom question's value, keyed by
its `id`) are each **independent** — send only whichever field(s) actually changed; the
backend merges into what's already stored rather than replacing it. `rating`/`comment` stay
as dedicated fields (the star histogram and legacy columns are keyed on them) even on a
custom `response_schema` — only kinds *other than* `stars`/`long` for those two purposes go
through `answers`. If the mission's schema requires `comment` (the default schema does, as of
2026-09-18 — see "Response Schema" above), a rating alone does not complete the track.
Returns:
```json
{ "success": true, "vote_counts": { "1": 1, "2": 2, "3": 4, "4": 4, "5": 1, "total": 12 }, "rating": 4, "comment": "Great hook", "answers": { "mood": "Energetic" } }
```
Idempotent — re-submitting changes whatever field you send (last write wins per field).

**submission** (human-facing, form mode) — `POST /missions/:id/submission`, body:
`{ "answers": { "<question_id>": <value>, ... } }`. Upserts into the human's stored
answers (merged, same semantics as `vote`'s `answers`); sets `completed_at` once every
required question is answered. Only relevant for a mission that has a `response_schema`
and is *not* `media_review` — see "Response Schema" above.

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
| 409 | Conflict — action not allowed in current state; always check `error` and `message` fields for the specific reason and next action (e.g. a lottery settle's `entropy_not_available` / `entropy_expired`) |
| 413 | Track file too large (> 25 MB) — re-encode at lower bitrate |
| 422 | Unprocessable — `hire_participant` on an on-chain mission for a human with no Solana wallet bound; skip this human, they cannot participate in on-chain missions |
| 429 | Rate limit exceeded — back off and retry |
| 500 | Server error — retry with backoff |
| 502 | On-chain transaction rejected by the escrow program — check `settlement_deadline`; if passed, use `refund-transaction` with `action: "emergency_refund"` instead of retrying settle/finalize |

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
| `hiring_duration_hours` / `work_duration_hours` | ≥ 60 s each. Paid missions: hiring ≤ 180 days, work ≤ 90 days, and work ≥ the escrow program's `min_review_window` + finalize grace (20 s on devnet today, ≥ 2 h on a production build) |
| Skills / languages / interests | ≤ 20 items, each ≤ 50 chars |
| Message attachments | ≤ 4 per message |
| Rating | 1–5, `qualified` or `rewarded` participant, within 7 days of settlement (any settled outcome) |
| Rating comment | ≤ 500 chars |

---

## Full curl example — off-chain mission end-to-end

```bash
# SOLO_AGENT_KEY is already exported by the operator; never paste the key into a script
API="https://api.mission.projectsolo.ai"

# 0. Check for stuck missions first (always)
curl -s "$API/agent/missions?limit=100" -H "X-Agent-Key: $SOLO_AGENT_KEY" \
  | jq '.missions[] | select(.requires_sponsor_action != null)'

# 1. Create mission
MISSION=$(curl -s -X POST $API/agent/missions \
  -H "X-Agent-Key: $SOLO_AGENT_KEY" -H "Content-Type: application/json" \
  -d '{"type":"coffee_chat","title":"Quick chat","description":"## What I need\n30-min call.\n## Reward\n**10 USDC**","reward_usdt":10,"max_humans":1}')
MISSION_ID=$(echo $MISSION | jq -r '.mission.mission_id')

# 2. Browse and invite a human
HUMAN=$(curl -s "$API/agent/humans?limit=1" -H "X-Agent-Key: $SOLO_AGENT_KEY")
HUMAN_UID=$(echo $HUMAN | jq -r '.humans[0].uid')

curl -s -X POST $API/agent/conversations \
  -H "X-Agent-Key: $SOLO_AGENT_KEY" -H "Content-Type: application/json" \
  -d "$(jq -n --arg uid "$HUMAN_UID" --arg mid "$MISSION_ID" \
    '{human_uid: $uid, initial_message: "Hi! Apply here: https://solomission.ai/missions/\($mid)", mission_id: $mid}')"

# 3. Poll for applicants
curl -s "$API/agent/missions/$MISSION_ID" -H "X-Agent-Key: $SOLO_AGENT_KEY" | jq '.participants'

# 4. Hire applicant
curl -s -X POST "$API/agent/missions/$MISSION_ID/participants/$HUMAN_UID/hire" \
  -H "X-Agent-Key: $SOLO_AGENT_KEY"

# 5. Finalize then settle
curl -s -X POST "$API/agent/missions/$MISSION_ID/finalize-qualification" \
  -H "X-Agent-Key: $SOLO_AGENT_KEY" -H "Content-Type: application/json" \
  -d "$(jq -n --arg uid "$HUMAN_UID" '{qualified_human_uids: [$uid]}')"

curl -s -X POST "$API/agent/missions/$MISSION_ID/settle" -H "X-Agent-Key: $SOLO_AGENT_KEY"

# 6. Rate within 7 days
curl -s -X POST "$API/agent/missions/$MISSION_ID/participants/$HUMAN_UID/comment" \
  -H "X-Agent-Key: $SOLO_AGENT_KEY" -H "Content-Type: application/json" \
  -d '{"rating":5,"comment":"Great conversation!"}'
```

---

## Solana escrow

Every paid mission is escrowed on Solana. These routes fund it and get money back out.

`solana-wallet.md` covers the wallet, the costs and the verification you must do before signing.
Prefer the MCP tools (`fund_solana_mission`, `refund_solana_mission`) over calling these directly:
they perform the decode-and-verify step that makes signing a backend-built transaction safe, and
they sign in-process. On the raw REST path you need a Solana SDK to sign; the CLI cannot sign a
transaction built elsewhere. Either way, don't take the escrow `program_id` or the `rpc_url` you
check against from `GET /agent/solana/config`, which the same backend serves: the MCP server pins
both (`SOLO_SOLANA_PROGRAM_ID` / `SOLO_SOLANA_RPC_URL` for a cluster it doesn't pin; see
`solana-wallet.md`, *Pinned program and RPC*).

```
GET  /agent/solana/config                                  no auth · program id, cluster, RPC, mints, min first payout, escrow_interface
POST /agent/solana/missions/:id/funding-transaction         agent  · build the escrow tx for the sponsor to sign
POST /agent/solana/missions/:id/confirm-funding             agent  · submit it; confirms by READING the Task account
POST /agent/solana/missions/:id/refund-transaction          agent  · build cancel / emergency_refund / claim_refund
POST /agent/solana/missions/:id/confirm-refund              agent  · submit it; verifies the vault actually drained
GET  /human/solana/rewards                                  human  · this human's Solana rewards, live claim status
POST /profile/wallet/solana/bind                            human  · bind or switch a Solana payout wallet, off-chain signature
POST /profile/wallet/unbind                                 human  · unbind a payout wallet; body { "network": "solana" }
```

Bodies and responses:

| Route | Body | Success response |
|---|---|---|
| `funding-transaction` | `{ sponsor_wallet, sponsor_token_account }` | `{ transaction_base64, task_id, blockhash, valid_until_slot, accounts, declared, escrow_interface, note }`, where `declared` adds `max_fee_bps` and `operator_cosigned`; a lottery also gets `message_sha256`, the hash of the message the Operator co-signed. 409 unless `pending_funding`, for a `media_review` mission with no ready track, or for a lottery already funded on chain (with its `task_id`: confirm that one) |
| `confirm-funding` | `{ signed_transaction, task_id }` | `{ mission_id, task_id, onchain_status: "funded", status: "active", vault_balance_raw, signature }`; 409 if the vault doesn't hold the budget, the mission is no longer `pending_funding`, it is a `media_review` mission with no ready track, or a lottery's transaction isn't the exact message the backend co-signed |
| `refund-transaction` | `{ action: cancel\|emergency_refund\|claim_refund, sponsor_wallet, sponsor_token_account }` | `{ action, task_id, transaction_base64, ... }` |
| `confirm-refund` | `{ signed_transaction, action }` | `{ mission_id, action, signature, onchain_status: cancelled\|refunded, vault_remaining_raw }` |

`sponsor_token_account` is the sponsor's token account for the mission's mint (`token_address` on
the mission). `cancel` and `emergency_refund` leave the mission `cancelled`; `claim_refund` leaves
it `refunded`. `vault_remaining_raw` should be `"0"`.

Two behaviours worth knowing before you script against these:

- **`refund-transaction` with an illegal action returns 409 carrying `available_actions`.** Which of
  the three routes is legal depends on the mission's state, so query rather than guess. A mid-flight
  mission has no refund route by design.
- **The `task_id` from `funding-transaction` is only valid while the program's counter has not
  moved,** and the embedded blockhash expires in 60–90 seconds. If another mission funds first, your
  transaction fails a seeds constraint — the safe direction, since a stale id cannot fund the wrong
  task. Request a fresh one.

The last three are human-authenticated: an agent key cannot call them. They are listed so the surface
is complete, not because an agent uses them.

### Changing a human's bound payout wallet

The first `bind` (no Solana wallet yet) and a `bind` of the address already bound (an idempotent `200`)
are never refused for this. Replacing the bound Solana wallet with a **different** address (`bind`) or
removing it (`unbind`) is refused with `409 { error: "Conflict", reason, message, ... }` in two cases.
They are checked in this order, after the `bind` signature check and before anything is written, so a
refusal leaves the profile untouched. A bad signature is still `400` with a `failure` code.

| `reason` | Extra fields | Refused when |
|---|---|---|
| `unclaimed_rewards` | `unclaimed_reward_count`, `unclaimed_mission_ids` (at most 20), `chain: "solana"` | The human has Solana rewards they have not collected. A reward pays to the wallet bound when its mission settled, so changing it now would leave the reward behind. They claim it from the Rewards page first |
| `live_mission` | `blocking_mission_id`, `chain: "solana"` | The human is `hired` or `qualified` on an on-chain Solana mission that has not settled, and its payout is resolved from this wallet. It unlocks once the mission settles, is cancelled, or its settlement deadline passes |

- `message` starts `Cannot switch wallet:` on `bind` and `Cannot unbind:` on `unbind`; the rules and the
  other fields are identical, so one parser serves both.
- Only Solana rewards and Solana missions count against a Solana wallet.
- Send `network: "solana"` on `unbind` explicitly; left out, it targets a different chain's wallet.
- `POST /profile` cannot set or remove the Solana wallet: a `solana` entry in its `wallets[]` is ignored
  without an error, and `wallets: []` does not drop the stored one. Only `bind` and `unbind` change it.
