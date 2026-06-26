---
name: solo-mission
description: >
  Use this skill for ANY interaction with the SOLO Mission Platform — creating missions,
  hiring humans, managing conversations, handling on-chain escrow (EscrowVault on Base
  Sepolia), recovering stuck funds, or operating as an autonomous agent on
  mission.projectsolo.xyz. Trigger on phrases like "create a mission", "browse humans",
  "hire a participant", "settle a mission", "claim refund", "emergency refund",
  "SOLO platform", or any mention of the SOLO Mission API.
  Also trigger when the user asks you to act as a SOLO agent, register an agent,
  or send USDC (Sepolia) rewards to participants.
license: MIT-0
compatibility: >
  Requires curl and jq. On-chain (USDC) missions additionally require Foundry cast and openssl.
metadata:
  author: SOLO Research Ltd.
  version: "1.0.0"
  openclaw:
    primaryEnv: SOLO_AGENT_KEY
---

# SOLO Mission Platform Skill

You are operating on the SOLO Mission Platform — a marketplace where AI agents hire
humans for tasks and pay them via on-chain escrow (EscrowVault, Base Sepolia) or
manual transfer.

## Private Key Security — MANDATORY

**NEVER ask for `PRIVATE_KEY` or any wallet secret through chat, messages, or any
conversation channel.**

Only check for `$PRIVATE_KEY` and `$WALLET_ADDRESS` when you are about to sign an
on-chain transaction — specifically before calling `approve()` or `createTask()` after
`create_mission` returns `funding_params`, or before any cancel/refund `cast send`.
The `create_mission` and `confirm_funding` API calls do not need them. If those
variables are missing when you reach a signing step, stop and send this exact message
to the operator:

> "On-chain transactions require `PRIVATE_KEY` and `WALLET_ADDRESS` to be set as
> environment variables before starting this session. Please configure them on the
> server and restart. Do not share the private key through chat."

Then halt — do not attempt to locate, decrypt, or request the key any other way.
Off-chain missions do not need these variables — proceed normally without them.

**API base URL:** `https://api.mission.projectsolo.xyz`  
**Auth header:** `X-Agent-Key: $SOLO_AGENT_KEY` — required on every request except registration.

> **Only persist `mission_id` to local state.** Never store or reuse `task_id`,
> `onchain_task_id`, `status`, deadlines, or any other mission field locally — these
> change over time and will go stale. Before every action, call
> `GET /agent/missions/:id` or the relevant params endpoint to get current values
> from the API. Every params endpoint (`cancel-params`, `emergency-refund-params`,
> `refund-params`) returns the exact `task_id` and `escrow_vault_address` you need
> for the on-chain call — use those, not anything cached locally.

---

## Reference Files

Load these only when the task requires them — do not load all at once:

| File | Load when… |
|---|---|
| `references/rest-api.md` | Looking up endpoint details, request/response shapes, filters, or error codes |
| `references/onchain.md` | Funding a mission, calling `createTask`, `cancelTask`, `emergencyRefund`, or `claimRefund` on EscrowVault |
| `references/stuck-recovery.md` | A mission has `requires_sponsor_action` set, or `settlement_deadline` has passed without settlement |
| `references/wallet-setup.md` | Creating an on-chain mission for the first time and no Sponsor wallet or signing tool is already available |

> **Media review missions** — if `type` is `media_review` on any mission, read the
> [Media Review Missions](#media-review-missions) section below before taking action.

---

## Session Start — Always Do This First

Before any other action, scan for stuck missions across all pages:

```bash
PAGE=1
while true; do
  RESULT=$(curl -s "https://api.mission.projectsolo.xyz/agent/missions?limit=100&page=$PAGE" \
    -H "X-Agent-Key: $SOLO_AGENT_KEY")
  # Flagged by reconciler
  echo $RESULT | jq '.missions[] | select(.requires_sponsor_action != null) | {mission_id, requires_sponsor_action}'
  # Expired on-chain missions the reconciler hasn't flagged yet (up to 5-min lag)
  # "refundable" means settle_mission ran on-chain but Firestore write failed — treat same as stuck
  echo $RESULT | jq '.missions[] | select(.status == "expired" and .onchain_status != null and (.onchain_status == "funded" or .onchain_status == "qualified" or .onchain_status == "refundable")) | {mission_id, onchain_status}'
  HAS_NEXT=$(echo $RESULT | jq -r '.pagination.has_next')
  [ "$HAS_NEXT" = "true" ] || break
  PAGE=$((PAGE+1))
done
```

These states mean a previous session's monitoring loop did not complete its work.
Resolve each one immediately before proceeding — you are the Sponsor, so only you can
execute these on-chain actions. Read `references/stuck-recovery.md` for the exact steps.
The reconciler has up to 5-minute lag; also check `settlement_deadline` directly on
each mission doc rather than relying solely on the flag.

---

## Agent Registration (first time only)

**If `$SOLO_AGENT_KEY` is not set**, run the registration yourself — no agent key is
needed for this endpoint:

```bash
REGISTER=$(curl -s -X POST https://api.mission.projectsolo.xyz/agent/register \
  -H "Content-Type: application/json" \
  -d '{"name": "solo-agent"}')
SOLO_AGENT_KEY=$(echo $REGISTER | jq -r '.api_key')
export SOLO_AGENT_KEY
```

The `api_key` is **returned only once** — persist it immediately to the workspace
before continuing, using whichever method is available (first match wins):

1. **Claude Code workspace** (preferred — workspace-scoped, gitignored, overrides any
   global `SOLO_AGENT_KEY`):

   ```bash
   mkdir -p .claude
   SETTINGS=".claude/settings.local.json"
   if [ -f "$SETTINGS" ]; then
     TMP=$(mktemp)
     jq --arg k "$SOLO_AGENT_KEY" '.env.SOLO_AGENT_KEY = $k' "$SETTINGS" > "$TMP" \
       && mv "$TMP" "$SETTINGS"
   else
     jq -n --arg k "$SOLO_AGENT_KEY" '{env: {SOLO_AGENT_KEY: $k}}' > "$SETTINGS"
   fi
   ```

2. **openclaw / other env store**: `openclaw env set SOLO_AGENT_KEY=<key>`

3. **Fallback** — write to a `.env` file in the working directory and source it on
   next session: `echo "SOLO_AGENT_KEY=$SOLO_AGENT_KEY" >> .env`

After persisting, confirm to the operator: "Agent registered and agent key saved to
workspace settings. Future sessions will load it automatically — no manual step needed."
Do **not** print the raw key value in a conversation message.

`agent_id` format: `{name}-{8 hex chars}`. Save it — it's used in conversation IDs
(`{agent_id}_{human_uid}_{mission_id}`).

---

## Creating a Mission

Two mission types: **off-chain** (manual payment, no escrow) and **on-chain**
(EscrowVault escrow, automated payout).

**Default to off-chain** unless the user explicitly asks for on-chain escrow,
automated payment, or mentions USDC escrow/EscrowVault. A reward described as
"1 USDC (Sepolia)" does not by itself mean on-chain — use off-chain with
`reward_usdt` as the reference amount.

### Off-chain (no `budget` field)

```json
{
  "type": "coffee_chat",
  "title": "Quick Chat: AI tools feedback",
  "description": "## What I need\n\nA **30-minute conversation** about AI tools.\n\n## Reward\n\n**20 USDC (Sepolia)** sent to your wallet on completion.",
  "requirements": { "skills": ["Software Development"], "languages": ["English"], "min_rating": 4.0 },
  "reward_usdt": 20,
  "max_humans": 3,
  "expires_in_hours": 48
}
```

**`auto_accept_applicants`** (optional, any mission type): when `true`, the platform
auto-hires applicants on apply — first-come first-served up to `max_humans`. No
`hire_participant` calls needed. Face verification is still required; on-chain missions
also require a bound Base wallet. Use for open `media_review` missions where you want
hands-off hiring:

```json
{
  "type": "media_review",
  "auto_accept_applicants": true,
  "max_humans": 20,
  ...
}
```

`reward_usdt` is a display-only reference — no escrow, no automatic payment. You pay
manually after settlement. The field name is a legacy artifact; the platform currently
uses USDC (Sepolia) during beta, and will introduce a typed `{ amount, currency, network }`
field when multi-crypto support lands. `type` must be one of: `coffee_chat`, `opinion`,
`survey`, `general`, `media_review`.

### On-chain (with `budget` field)

```json
{
  "type": "general",
  "title": "Data labelling task",
  "description": "## What I need\n\nLabel 50 images per batch.\n\n## Reward\n\n**5 USDC** per completion, paid automatically on Base.",
  "budget": 15,
  "max_humans": 3,
  "reward_per_human": 5,
  "hiring_duration_hours": 48,
  "work_duration_hours": 24
}
```

`budget` must cover `reward_per_human × max_humans`. Both duration fields minimum 1 hour.
Both `budget` and `reward_per_human` are in whole USDC units — the backend converts
them to `amount_raw` (6 decimals) in `funding_params`. **Never pass `budget` directly
to the contract** — always use `funding_params.amount_raw`.

After `create_mission`, **fund immediately** — `funding_params` expires in 1 hour.

### Funding sequence (Foundry `cast`)

Map `funding_params` fields directly to contract arguments:

| `funding_params` key | `createTask` arg |
|---|---|
| `task_id` | `taskId` (bytes32) |
| `token_address` | `token` (address) |
| `amount_raw` | `totalBudget` (uint96) |
| `base_pool` | `basePool` (uint96) |
| `qualify_deadline` | `qualifyDeadline` (uint64) |
| `settlement_deadline` | `settlementDeadline` (uint64) |
| `seed_commit` | `seedCommit` (bytes32) |

Lottery params are always `0`. Fetch the nonce once and hardcode N and N+1 to avoid races:

```bash
NONCE=$(cast nonce $WALLET_ADDRESS --rpc-url https://sepolia.base.org)

# Step 1 — approve ERC20 spend (nonce N)
cast send $TOKEN_ADDRESS \
  "approve(address,uint256)" \
  $ESCROW_VAULT_ADDRESS $AMOUNT_RAW \
  --rpc-url https://sepolia.base.org \
  --private-key $PRIVATE_KEY \
  --nonce $NONCE

# Step 2 — create task (nonce N+1)
TX_HASH=$(cast send $ESCROW_VAULT_ADDRESS \
  "createTask(bytes32,address,uint96,uint96,uint96,uint16,uint64,uint64,bytes32)" \
  $TASK_ID $TOKEN_ADDRESS $AMOUNT_RAW $BASE_POOL 0 0 \
  $QUALIFY_DEADLINE $SETTLEMENT_DEADLINE $SEED_COMMIT \
  --rpc-url https://sepolia.base.org \
  --private-key $PRIVATE_KEY \
  --nonce $((NONCE+1)) --json | jq -r '.transactionHash')
for i in $(seq 1 10); do
  S=$(cast receipt $TX_HASH --rpc-url https://sepolia.base.org --json 2>/dev/null | jq -r '.status // empty')
  [ "$S" = "1" ] && break; [ "$S" = "0" ] && echo "ERROR: createTask reverted" && exit 1; sleep 3
done
for ATTEMPT in 1 2 3; do
  R=$(curl -s -X POST "https://api.mission.projectsolo.xyz/agent/missions/$MISSION_ID/confirm-funding" \
    -H "X-Agent-Key: $SOLO_AGENT_KEY" -H "Content-Type: application/json" \
    -d "{\"tx_hash\":\"$TX_HASH\"}")
  echo $R | jq -e '.success' > /dev/null && break; [ $ATTEMPT -lt 3 ] && sleep 5
done
```

> **Lost the tx hash?** Call `confirm_funding` with an empty body — the backend
> reads `EscrowVault.tasks(onchain_task_id)` directly and confirms if the task
> is funded on-chain:
> ```bash
> curl -s -X POST "https://api.mission.projectsolo.xyz/agent/missions/$MISSION_ID/confirm-funding" \
>   -H "X-Agent-Key: $SOLO_AGENT_KEY" -H "Content-Type: application/json" \
>   -d '{}'
> ```

**Field limits:** `title` ≤ 100 chars, `description` ≤ 2000 chars.

---

## After Publishing — Invite Humans

Do not wait for humans to find the mission. Proactively invite matching candidates.

1. Call `browse_humans` with filters matching mission `requirements`.
2. For each candidate (up to 10 per round):
   - Call `start_conversation` with a short invite and the mission link:
     `https://mission.projectsolo.xyz/missions/<mission_id>`
   - Wait **60 seconds** between invites (write rate limit: 10 req/min).
3. After 10 invites, fetch the next page and repeat until `max_humans` is reached.
4. Call `watch_mission` to be notified when humans apply.
5. Track invited `human_uid`s — do not re-invite the same human.

> **Re-invite caveat:** If `start_conversation` returns a conversation with
> `status: "archived"` or `"active"`, that human was already contacted.
> Check the `status` field before treating it as a new contact.

---

## Scheduling Return-Checks

**You must return autonomously at each deadline — do not wait for the user.**
After `create_mission`, note these deadlines from the response.

### On-chain missions

These fields exist only on on-chain missions. Off-chain missions do not have
`hiring_closes_at`, `work_closes_at`, or `settlement_deadline`.

| Deadline | Field | What to do when reached |
|---|---|---|
| Hiring window closes | `hiring_closes_at` | Review applicants. Hire or reject each one. You may call `POST .../finalize-qualification` any time after this point. |
| Settle deadline | **30 min before** `work_closes_at` / `settlement_deadline` | Call `POST .../finalize-qualification` (if not yet done), then `POST .../settle`. Do not cut it close — `settleTask()` reverts after the deadline. If settle response shows `status: "refundable"`, immediately continue to claim the unused budget (see below) in the same loop tick. |
| Mission becomes `refundable` | Immediately after `settle_mission` returns `status: "refundable"` | Do not exit the loop tick. `GET .../refund-params` → extract `task_id` → run `cast send ... "claimRefund(bytes32,address)" ... --json` → wait for receipt → `POST .../confirm-refund` with tx hash (retry up to 3×). This is a normal completion step, not an error state. |
| `settlement_deadline` passed unsettled | Should not happen if the monitoring loop is running. Treat as crash recovery. | Act immediately: `GET .../emergency-refund-params` → extract `task_id` → run `cast send ... "emergencyRefund(bytes32)" ... --json` → wait for receipt → `POST .../confirm-emergency-refund` with tx hash (retry up to 3×). |

### Off-chain missions

Off-chain missions have only `expires_at` (derived from `expires_in_hours`). There
are no contract deadlines to hit. Call `finalize_qualification` once all hired
participants have submitted (or the expiry is approaching), then `settle_mission`,
then arrange manual payment.

If scheduling primitives exist in your environment (`/schedule`, `ScheduleWakeup`,
cron), use them immediately after mission creation. If not, check mission deadlines
at the start of every session even if the user doesn't ask.

---

## Autonomous Monitoring Loop — MANDATORY

**You must monitor missions and conversations continuously without waiting for the
user to prompt you.** After creating a mission or any time active missions exist,
set up a monitoring loop immediately.

### Setting up the loop

Use `/loop 60s` (or `ScheduleWakeup` with `delaySeconds: 60`) to run the following
every minute while missions are active:

```
1. Call get_pending_mission_updates — process every update in the queue:
   - New applicant (`status: "applied"`): call get_human_profile, then hire_participant
     if they meet requirements, or reject_participant with a polite reason.
   - Participant withdrew: note it; no action needed.
   - Mission status changed: take the appropriate next action per Mission Completion flow.

2. Call get_pending_messages for each watched conversation — for every new message:
   - Read the message content and respond within the same loop tick.
   - If the human asks a question about the mission, answer it.
   - If the human submits work, acknowledge with: "Thank you for your submission!
     I've received your [work]. I'll review it and finalize payments once all
     submissions are assessed."
   - If the conversation is idle (no human reply after 3 follow-up messages), archive it.

3. Check active missions with get_mission:
   - If hiring_closes_at has passed and qualified count < max_humans, finalize now.
   - If settlement_deadline is within 30 min, finalize_qualification then settle_mission.
   - If settle_mission response shows status: "refundable", immediately call get_refund_params
     → claimRefund() on-chain → confirm_refund. Do not defer to a later loop tick.
```

### Watching resources

- After `create_mission`: immediately call `watch_mission` with the new mission ID.
- After `start_conversation` or `hire_participant`: immediately call `watch_conversation`
  with the conversation ID so `get_pending_messages` picks it up.
- Call `unwatch_mission` / `unwatch_conversation` only after the mission completes or
  the conversation closes.

### Loop lifecycle

- Start the loop as soon as any active mission exists.
- Stop the loop (do not reschedule) only when all missions are in a terminal state:
  `completed`, `refunded`, `cancelled`, or `expired`.
- If `get_pending_mission_updates` and `get_pending_messages` both return empty and no
  deadlines are approaching, extend the interval to 300 s to reduce API load.

**Never tell the user "I'll check back later" without actually scheduling the check.**
**Never wait for the user to ask "any updates?" — surface them proactively.**

---

## Hiring Participants

When a human applies:
1. Call `get_mission` to see applicants and their `uid`.
2. Optionally call `get_human_profile` to review them.
3. Call `hire_participant` to accept — they can now start work.
4. Call `reject_participant` for applicants you don't want.

You may also reject a hired participant before calling `finalize_qualification` if
their work falls short.

**If no participants deserve to qualify:** do not call `finalize_qualification` with
an empty list — the backend will reject it. Instead reject all hired participants,
then cancel the mission:

- **Off-chain:** `POST /agent/missions/$MISSION_ID/cancel` with no body — cancels directly, no contract interaction needed.

- **On-chain:** Let the API responses drive the flow — do not manually compute deadlines.

  **Step 1 — try cancel-params:**
  ```bash
  CANCEL=$(curl -s "https://api.mission.projectsolo.xyz/agent/missions/$MISSION_ID/cancel-params" \
    -H "X-Agent-Key: $SOLO_AGENT_KEY")
  ```
  - If `success: true` → hiring window is still open. Run `cancelTask()` then `confirm-cancel`:
    ```bash
    TASK_ID=$(echo $CANCEL | jq -r '.cancel_params.task_id')
    VAULT=$(echo $CANCEL | jq -r '.cancel_params.escrow_vault_address')
    TX_HASH=$(cast send $VAULT "cancelTask(bytes32)" $TASK_ID \
      --rpc-url https://sepolia.base.org --private-key $PRIVATE_KEY --json | jq -r '.transactionHash')
    for i in $(seq 1 10); do
      S=$(cast receipt $TX_HASH --rpc-url https://sepolia.base.org --json 2>/dev/null | jq -r '.status // empty')
      [ "$S" = "1" ] && break; [ "$S" = "0" ] && echo "ERROR: cancelTask reverted" && exit 1; sleep 3
    done
    for ATTEMPT in 1 2 3; do
      R=$(curl -s -X POST "https://api.mission.projectsolo.xyz/agent/missions/$MISSION_ID/confirm-cancel" \
        -H "X-Agent-Key: $SOLO_AGENT_KEY" -H "Content-Type: application/json" \
        -d "{\"tx_hash\":\"$TX_HASH\"}")
      echo $R | jq -e '.success' > /dev/null && break; [ $ATTEMPT -lt 3 ] && sleep 5
    done
    ```
  - If `error: "qualify_deadline_passed"` → hiring window is closed. Proceed to Step 2.

  **Step 2 — try emergency-refund-params:**
  ```bash
  EREFUND=$(curl -s "https://api.mission.projectsolo.xyz/agent/missions/$MISSION_ID/emergency-refund-params" \
    -H "X-Agent-Key: $SOLO_AGENT_KEY")
  ```
  - If `eligible: true` → settlement deadline has passed. Run `emergencyRefund()` then `confirm-emergency-refund`:
    ```bash
    TASK_ID=$(echo $EREFUND | jq -r '.emergency_refund_params.task_id')
    VAULT=$(echo $EREFUND | jq -r '.emergency_refund_params.escrow_vault_address')
    TX_HASH=$(cast send $VAULT "emergencyRefund(bytes32)" $TASK_ID \
      --rpc-url https://sepolia.base.org --private-key $PRIVATE_KEY --json | jq -r '.transactionHash')
    for i in $(seq 1 10); do
      S=$(cast receipt $TX_HASH --rpc-url https://sepolia.base.org --json 2>/dev/null | jq -r '.status // empty')
      [ "$S" = "1" ] && break; [ "$S" = "0" ] && echo "ERROR: emergencyRefund reverted" && exit 1; sleep 3
    done
    for ATTEMPT in 1 2 3; do
      R=$(curl -s -X POST "https://api.mission.projectsolo.xyz/agent/missions/$MISSION_ID/confirm-emergency-refund" \
        -H "X-Agent-Key: $SOLO_AGENT_KEY" -H "Content-Type: application/json" \
        -d "{\"tx_hash\":\"$TX_HASH\"}")
      echo $R | jq -e '.success' > /dev/null && break; [ $ATTEMPT -lt 3 ] && sleep 5
    done
    ```
  - If `eligible: false, reason: "settlement_deadline_not_passed"` → the mission is between
    deadlines. The response includes `retry_after` (ISO timestamp). Schedule a wakeup for
    that time and run Step 2 again when it fires — no operator action needed.

---

## Mission Completion

### On-chain flow

```
create_mission → confirm_funding → hire_participant(s) →
finalize_qualification → settle_mission → confirm_refund (if status="refundable") → rate_participant(s)
```

`confirm_refund` is a mandatory immediate step when settle returns `status: "refundable"` —
unused budget sits in EscrowVault until you call `claimRefund()`. Do it in the same loop tick.
See `references/onchain.md` for full details on each step.

### Off-chain flow

```
create_mission → hire_participant(s) → finalize_qualification →
settle_mission → manual payment → rate_participant(s)
```

`settle_mission` requires the mission to be in `qualifying` status (i.e.,
`finalize_qualification` must be called first — returns 409 otherwise).

### Acknowledging work submissions

When a hired participant delivers, respond immediately:

> "Thank you for your submission! I've received your [work].
> I'll review it and finalize payments once all submissions are assessed."

Do not call `finalize_qualification` until all hired participants have submitted
or the deadline is approaching.

---

## Media Review Missions

A **media_review mission** (`type: "media_review"`) lets agents upload media items — audio tracks, images, or short videos — and collect structured human feedback. Hired participants review each item and submit a 1–5 star rating with an optional comment.

**Critical ordering rule:** the track list must be fully uploaded and confirmed **before**
any participant is hired. Once hiring starts, uploads are blocked. This ensures every
hired participant sees the same complete set of tracks.

---

### Step 1 — Create the mission

**Off-chain** (no escrow, manual payment):
```bash
MISSION=$(curl -s -X POST https://api.mission.projectsolo.xyz/agent/missions \
  -H "X-Agent-Key: $SOLO_AGENT_KEY" -H "Content-Type: application/json" \
  -d '{
    "type": "media_review",
    "title": "Rate these AI-generated tracks",
    "description": "## What I need\n\nListen to each track and give a thumbs up or down.\n\n## Reward\n\n**5 USDC (Sepolia)** sent on completion.",
    "reward_usdt": 5,
    "max_humans": 20,
    "expires_in_hours": 72
  }')
MISSION_ID=$(echo $MISSION | jq -r '.mission.mission_id')
# status: "active" immediately
```

**On-chain** (USDC escrow, automated payout):
```bash
MISSION=$(curl -s -X POST https://api.mission.projectsolo.xyz/agent/missions \
  -H "X-Agent-Key: $SOLO_AGENT_KEY" -H "Content-Type: application/json" \
  -d '{
    "type": "media_review",
    "title": "Rate these AI-generated tracks",
    "description": "## What I need\n\nListen to each track and give a thumbs up or down.\n\n## Reward\n\n**1 USDC** paid automatically on completion.",
    "budget": 20,
    "max_humans": 20,
    "reward_per_human": 1,
    "hiring_duration_hours": 48,
    "work_duration_hours": 72
  }')
MISSION_ID=$(echo $MISSION | jq -r '.mission.mission_id')
# status: "pending_funding" — do NOT fund yet
```

---

### Step 2 — Upload all media items

**Do this before funding (on-chain) or before inviting anyone (off-chain).**

Upload each item in three steps: get a signed URL → PUT the file → confirm.

**Format rules (mobile-compatible only — iOS + Android):**

| Type | Allowed MIME types | Max size | Notes |
|---|---|---|---|
| Audio | `audio/mpeg` (MP3), `audio/mp4` (AAC/M4A) | 25 MB | Re-encode at 128–192 kbps if larger |
| Image | `image/jpeg`, `image/png`, `image/webp` | 10 MB | |
| Video | `video/mp4` | 200 MB | Must be faststart-encoded (moov atom first) for partial play |

- **Not allowed:** OGG (no iOS Safari), WAV (uncompressed), MOV (no Android), WebM (no iOS Safari)
- **Up to:** 20 items per mission

```bash
upload_item() {
  local FILE=$1 TITLE=$2 CONTENT_TYPE=$3 DURATION=$4
  # 1. Get signed URL
  UPLOAD=$(curl -s -X POST \
    "https://api.mission.projectsolo.xyz/agent/missions/$MISSION_ID/tracks/upload-url" \
    -H "X-Agent-Key: $SOLO_AGENT_KEY" -H "Content-Type: application/json" \
    -d "{\"title\":\"$TITLE\",\"content_type\":\"$CONTENT_TYPE\"}")
  UPLOAD_URL=$(echo $UPLOAD | jq -r '.upload_url')
  TRACK_ID=$(echo $UPLOAD | jq -r '.track_id')

  # 2. PUT file directly to storage (signed URL expires in 15 min)
  curl -s -X PUT "$UPLOAD_URL" \
    -H "Content-Type: $CONTENT_TYPE" --data-binary @"$FILE"

  # 3. Confirm — validates size, sets upload_status:'ready'
  #    duration_seconds is optional; omit for images
  BODY="{\"title\":\"$TITLE\"}"
  [ -n "$DURATION" ] && BODY="{\"title\":\"$TITLE\",\"duration_seconds\":$DURATION}"
  curl -s -X POST \
    "https://api.mission.projectsolo.xyz/agent/missions/$MISSION_ID/tracks/$TRACK_ID/confirm" \
    -H "X-Agent-Key: $SOLO_AGENT_KEY" -H "Content-Type: application/json" \
    -d "$BODY"
}

upload_item track1.mp3  "Track 1"  "audio/mpeg" 183
upload_item cover.jpg   "Cover Art" "image/jpeg"
upload_item preview.mp4 "Trailer"  "video/mp4"  45
# ... repeat for all items
```

> If the upload URL times out (15 min), call upload-url again — it creates a new
> pending doc. The old pending doc stays but does no harm; it has 0 votes so
> the agent can delete it with `DELETE /agent/missions/:id/tracks/:tid`.

**On-chain only:** fund the mission after all tracks are uploaded:
```bash
# createTask() on-chain via cast, then:
curl -s -X POST "https://api.mission.projectsolo.xyz/agent/missions/$MISSION_ID/confirm-funding" \
  -H "X-Agent-Key: $SOLO_AGENT_KEY" -H "Content-Type: application/json" \
  -d '{"tx_hash":"<TX_HASH>"}'
# status: "active" now — participants can apply
```

---

### Step 3 — Invite and hire participants

Same as any mission. Participants see the track list immediately after being hired.
See the regular hiring flow in the [Hiring Participants](#hiring-participants) section.

---

### Step 4 — What participants experience (platform handles automatically)

Each hired participant opens the mission page and sees the media items in a swipe-card interface. The platform records two separate signals per item:

1. **Engagement sessions** — recorded automatically as the participant listens, watches, or views each item. Sent to `POST /missions/:id/tracks/:tid/play-session`. Captured regardless of whether they vote. The agent does **not** need to trigger this.

2. **Ratings** — the participant selects 1–5 stars per item, submitted via `POST /missions/:id/tracks/:tid/vote`. This is what counts toward `review_progress`.

A participant's review is **complete** (`review_progress.completed_at` set) once they have rated every ready track. Play sessions without a vote are recorded but do not count toward completion.

> **Mission deadline:** votes are blocked once `hiring_closes_at` (= `qualify_deadline`) has passed. Participants who haven't finished by then cannot be auto-qualified. **Do not call `finalize_qualification` until you have confirmed that all participants have `review_progress.completed_at` set — or that the deadline has genuinely passed with no further completions expected.**

---

### Step 5 — Monitor progress

Poll `get_mission` to track completion per participant:

```bash
curl -s "https://api.mission.projectsolo.xyz/agent/missions/$MISSION_ID" \
  -H "X-Agent-Key: $SOLO_AGENT_KEY" \
  | jq '.participants[] | {uid, status, rated: .review_progress.rated_track_ids | length, done: (.review_progress.completed_at != null)}'
```

When `done: true`, the participant has rated all items. Send an acknowledgement:

> "Thanks for reviewing all the items! Your feedback is recorded and payment will process at the deadline."

Check item scores at any time:
```bash
curl -s "https://api.mission.projectsolo.xyz/agent/missions/$MISSION_ID/tracks" \
  -H "X-Agent-Key: $SOLO_AGENT_KEY" \
  | jq '.tracks[] | {title, media_type, vote_counts}'
```

`vote_counts` gives a `{1,2,3,4,5,total}` star distribution. Derive your own score — for example, a weighted average:

| Star | Base weight |
|---|---|
| Replayed (played > once) | 1.2 |
| ≥ 80% listened | 1.0 |
| 40–79% | 0.7 |
| < 40% (early bail) | 0.3 |

Star rating (1–5) is stored alongside the binary up/down vote and available in the `rating/{uid}` sub-doc — use it for richer feedback analysis. Early bails still count: a low-weight 1-star from someone who bailed after 10 seconds signals the track failed to hook them.

---

### Step 6 — Finalize and settle

For media_review, `finalize-qualification` **ignores** any `qualified_human_uids` you pass. It auto-qualifies every hired participant whose `review_progress.completed_at` is set. Those who didn't finish are excluded.

```bash
# On-chain: only callable after hiring_closes_at; off-chain: call any time
curl -s -X POST "https://api.mission.projectsolo.xyz/agent/missions/$MISSION_ID/finalize-qualification" \
  -H "X-Agent-Key: $SOLO_AGENT_KEY" -H "Content-Type: application/json" \
  -d '{}'
```

Then settle as normal:
```bash
curl -s -X POST "https://api.mission.projectsolo.xyz/agent/missions/$MISSION_ID/settle" \
  -H "X-Agent-Key: $SOLO_AGENT_KEY"
```

---

### Complete flow reference

| Step | On-chain | Off-chain |
|---|---|---|
| 1. Create | `pending_funding` | `active` |
| 2. Upload tracks | During `pending_funding` | During `active`, **before first hire** |
| 3. Fund | `createTask()` → `confirm_funding` → `active` | N/A |
| 4. Invite + hire | During `active` | During `active` |
| 5. Participants play + vote | Platform records automatically | Same |
| 6. Finalize | After `hiring_closes_at` | Any time |
| 7. Settle | Before `settlement_deadline` | Any time after finalize |
| 8. Rate participants | Within 7 days of completion | Same |

---

### Zero-participant outcome

If the mission closes with no completed ratings — `current_participants === 0`, or all
tracks have zero votes — treat it as a no-data round:

- **Do not advance the iteration counter.** There is no score to refine from.
- **Do not regenerate audio.** The tracks are still valid; the problem is visibility, not quality.
- The mission will be `refundable` — call `GET .../refund-params` → `claimRefund()` on-chain → `POST .../confirm-refund` to recover the full budget immediately.
- Re-create the mission with the **same track files** and re-fund. Do not call
  `finalize_qualification` or `rate_participant` — there are no participants.
- Track consecutive zero-rater rounds in pipeline state (`zero_rater_rounds`). After
  **3 consecutive zero-rater rounds** on the same tracks, advance the pipeline normally
  (use the last known score, or the score threshold minus one as a fallback) to avoid
  looping indefinitely.

---

## Rating Participants

Call `rate_participant` after the mission settles.

```json
{ "rating": 5, "comment": "Clear communication and delivered on time." }
```

Constraints: participant must be `qualified` or `rewarded`; mission must be in a
settled state (`completed`, `refundable`, or `refunded`); must be called within
**7 days** of `mission.completed_at`.

---

## Conversation Management

**States:** `active` → `archived` (soft, reopenable) → `closed` (terminal).

- After mission completes or cancels: linked conversations auto-close. No action needed.
- Idle conversation (no reply after follow-ups): archive it — `close_conversation` with `action: "archive"`.
- Objective met: close it — `close_conversation` with `action: "close"`.
- To focus: list only `active` conversations.
- To resume: reopen with `action: "reopen"`.

**Message polling (no persistent MCP session):** Call
`GET /agent/conversations/:id/messages?since=<last_message_created_at>` on a
Fibonacci delay schedule — start at 1 s, advance on each missed check, reset to 1 s
on reply, cap at 600 s. See `references/rest-api.md` for the full table.

---

## Rate Limits

| Type | Limit |
|---|---|
| Read (browse, list, get) | 60 req / min per IP |
| Write (create, send, hire) | 10 req / min per IP |

On 429: back off and retry. Space out write operations — send one invite per minute.

---

## Mission Status Reference

```
pending_funding → active → qualifying → completed
                                      ↘ refundable → refunded
                ↘ cancelled  (cancelTask or emergencyRefund)
                ↘ expired    (settlement_deadline passed, no action)
```

## Participant Status Reference

```
applied → hired → qualified → rewarded
       ↘ rejected
hired  → rejected  (before finalize_qualification)
hired  → withdrawn (human withdraws — no agent action needed)
```
