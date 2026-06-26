# TOOL.md

Base URL: `https://app.humeo.com`

## Purpose

This is the internal execution playbook for the skill.

- Use this file for implementation and sequencing.
- Do not expose internal route names, token fields, headers, IDs, or command templates to users unless they explicitly ask for debugging.
- Keep user-facing responses outcome-first and creator-friendly.
- Do not create local script files (`.sh`, `.ps1`, `.bat`) as a workaround for normal flows.

## Runtime Auth

- Use `Authorization: Bearer <humeo_pat_...>` for normal runtime.
- For POST endpoints, always set `Content-Type: application/json` on the request.
- PAT bearer auth is the default and only supported runtime auth flow.
- Prefer persistent local PAT storage at `~/.videoclaw_personal_mcp_token` to avoid repeated token refresh prompts.
- If PAT is missing or invalid, ask the user to paste the PAT directly, then store it at `~/.videoclaw_personal_mcp_token` from the OpenClaw runtime.
- For hook and teleprompter flows, PAT plus normal app params is sufficient.
- To check setup without exposing the token value, call `GET|POST /api/mcp/auth/personal-token/status`.
- `personal-token/status` validates only the Bearer token sent in the request.

## Setup Help

- If the Humeo PAT is missing:
  - first check `GET|POST /api/mcp/auth/personal-token/status`
  - if `bearerProvided=true` and `tokenValid=true`, reuse current setup and do not ask for a new token
  - if token is missing/invalid, ask user to paste the PAT directly in chat
  - once received, OpenClaw agent must write the token to `~/.videoclaw_personal_mcp_token`
  - OpenClaw agent must set permission mode `600` on that file
  - retry `GET|POST /api/mcp/auth/personal-token/status` after writing the file
  - only if the user does not yet have a PAT, direct them to `https://app.humeo.com/profile/mcp` to create one
  - never echo full PAT back in messages; if needed, acknowledge with masked preview only
- If upload-post publishing is requested and no upload-post key is configured:
  - tell the user to get the key from upload-post.com
  - tell them to store it in the operator's secret store or local secure config
  - do not hardcode it into this skill
- Be proactive about setup.

## Workflow Suggestion Triggers (User-Facing)

Use these as default "next step" prompts in normal runtime:

- After hooks are generated or a hook is selected:
  - ask: "Do you want to do a hook-only take and freestyle it, have a conversation with the AI coach, or build a full teleprompter script together?"
- After a hook is selected and user wants speed:
  - ask: "Want me to draft the teleprompter script from this hook and open your recording link now?"
- When upload is complete and processing result is ready:
  - ask: "Preview is ready. Do you want the preview link so we can make edits, or should I render the video directly?"
- After render download URL is ready:
  - ask publishing follow-up only if upload-post is configured.

## Internal Traversal Policy (Agent-Facing)

Use this ordering to decide what to do first:

1. If topic is time-sensitive, run short research first, then generate hooks/scripts.
2. Keep continuity: selected hook -> script (optional) -> recording link.
3. When recording is uploaded, explicitly trigger processing. Do not assume another UI path will always do this.
4. Share preview before final download by default.
5. Queue final render only when user asks for final file/render.
6. Offer publishing only when upload-post config exists.
7. For tone continuity, fetch transcript excerpts via `GET|POST /api/mcp/interviews/transcripts/context`, then pass compact context as `transcriptText`.

## Core Endpoints (Internal)

- `GET|POST|DELETE /api/mcp/auth/personal-token`
- `GET|POST /api/mcp/auth/personal-token/status`
- `POST /api/mcp/hooks/create`
- `POST /api/mcp/teleprompter/scripts/create`
- `POST /api/mcp/recording-link/create`
- `GET /api/mcp/interviews/status`
- `POST /api/mcp/interviews/status`
- `GET|POST /api/mcp/interviews/transcripts/context`
- `POST /api/mcp/interviews/process`
- `GET /api/mcp/interviews` — list/search interviews and their results
- `GET /api/mcp/edits/state` — read current edit state (segments, words, overrides)
- `POST /api/mcp/edits/apply` — apply an edit via natural language instruction (LLM-powered)
- `POST /api/mcp/interviews/custom-edit` — create a new custom edit variant from a prompt
- `GET /api/mcp/interviews/custom-edit` — poll custom edit generation status
- `POST /api/mcp/renders/request`
- `POST /api/mcp/renders/download`
- `POST /api/mcp/calendar/add`
- `GET /api/mcp/calendar/list`
- `PATCH /api/mcp/calendar/{id}` — update topic, notes, targetDate, recordingMode, reminderMinutes, cronJobId
- `DELETE /api/mcp/calendar/{id}` — returns cronJobId for cleanup
- `GET /api/mcp/calendar/{id}` — fetch one calendar item by id (owner-only), used by one-shot reminder crons
- `PATCH /api/mcp/calendar/{id}/status`
- `POST /api/mcp/calendar/{id}/prepare`
- `POST /api/mcp/calendar/{id}/reminded`
- `GET /api/mcp/calendar/due`

Transcript context support:

- `GET|POST /api/mcp/interviews/transcripts/context` returns transcript excerpts from both:
  - `interview_transcripts`
  - `hook_transcripts`
- Use this endpoint when script quality depends on matching the user's voice from previous recordings.

## User Response Translation Layer

Always translate internal operations into plain language:

- "hook generation" -> "I created hook options"
- "teleprompter script create" -> "I drafted your script"
- "magicLink" -> "recording link"
- "status polling" -> "checking upload and processing progress"
- "render request/download polling" -> "generating your clip and checking when it is ready"

Avoid these terms in normal replies:

- endpoint
- payload
- auth header
- token internals
- raw id field names (`hookItemId`, `scriptId`, etc.)
- curl/bash/powershell commands

Also avoid these response patterns in normal runtime:

- "I created a shell script for you"
- "Run this local helper script first"
- "Save this script and execute it"

Allowed exception:

- If user explicitly asks for technical debugging, provide precise implementation details.

## Exact MCP Payloads

### `POST /api/mcp/teleprompter/scripts/create`

Allowed body:

```json
{
  "prompt": "optional when scriptText is provided",
  "scriptText": "optional when prompt is provided",
  "title": "optional",
  "durationSeconds": 45,
  "tone": "optional",
  "audience": "optional",
  "callToAction": "optional",
  "hookItemId": "optional",
  "hookText": "optional",
  "transcriptText": "optional"
}
```

Rules:

- Send `scriptText` if the script is already written.
- Send `prompt` if Humeo should generate the script.
- If user asks for "script for this hook", pass `hookItemId` when available.
- If only raw hook copy is available, pass `hookText`.
- If transcript context exists, pass `transcriptText` for continuity.
- Send at least one of `scriptText`, `prompt`, `hookItemId`, `hookText`, or `transcriptText`.

### `POST /api/mcp/recording-link/create`

Allowed body:

```json
{
  "mode": "full | idea | hook | teleprompter",
  "interviewId": "optional for full or idea",
  "hookRunId": "optional fallback hook identifier",
  "hookItemId": "preferred hook identifier for hook mode",
  "scriptId": "required for teleprompter",
  "id": "optional fallback identifier",
  "hookIndex": 0,
  "titleHook": "optional"
}
```

Rules:

- For hook recording links, prefer `hookItemId`.
- `hookRunId` and `id` are fallback hook identifiers only.
- For teleprompter links, `scriptId` is required.
- For full or idea flows, `interviewId` may be provided or generated.
- Treat returned `magicLink` as the source of truth.

### `POST /api/mcp/interviews/process`

Allowed body:

```json
{
  "interviewId": "optional when another identifier is used",
  "hookItemId": "optional hook identifier",
  "scriptId": "optional script identifier"
}
```

Rules:

- Send one of `interviewId`, `hookItemId`, or `scriptId`.
- Prefer `interviewId` when already known.
- Hook recordings can use `hookItemId`.
- Teleprompter recordings can use `scriptId`.

### `GET|POST /api/mcp/auth/personal-token/status`

No request body required.

Response includes:

- `bearerProvided` (an `Authorization: Bearer` token was sent)
- `tokenValid` (provided Bearer token is currently valid)
- `reason` (`ok`, `missing_bearer`, `token_invalid`, `token_expired`, `token_revoked`, `profile_not_found`)
- `actor` when valid

Rules:

- Use this status endpoint before asking users to rotate or recreate PAT.
- Do not expose or echo raw token values in user-facing messages.
- If `bearerProvided=true` and `tokenValid=true`, continue normally.

### `GET|POST /api/mcp/interviews/transcripts/context`

Allowed body:

```json
{
  "limit": 8,
  "maxWordsPerTranscript": 900,
  "maxTotalWords": 3000,
  "includeInterviewTranscripts": true,
  "includeHookTranscripts": true,
  "excludeInterviewIds": ["optional-id"],
  "excludeHookRunIds": ["optional-id"]
}
```

Rules:

- Default to both transcript sources enabled.
- Use word caps to control context size:
  - `maxWordsPerTranscript`: cap per returned item
  - `maxTotalWords`: global cap across all returned items
- Prefer newest transcripts first.
- Use `excludeInterviewIds` and `excludeHookRunIds` to avoid reusing context from the current recording.
- Use returned `items[].excerpt` as style/voice context for script generation.

## Research Tooling

- This skill does not ship a scraper script.
- Use whatever web search, browser, or scraping capability exists in the current OpenClaw environment.
- If no browsing or scraping tool is available, do not pretend research was performed. Tell the user you can continue with general knowledge or they can enable a browsing tool for live research.

### Google News search pattern

```text
https://news.google.com/search?q=<topic>&hl=en-US&gl=US&ceid=US%3Aen
```

## Hook Flow (Execution)

1. Call `POST /api/mcp/hooks/create` with the user prompt.
2. Show the full first batch (normally up to 10 hooks).
3. If the user asks for more, call the same endpoint with `hookGenerationId` and show the next batch.
4. If the user picks a hook, resolve and persist the real `hookItemId`.
5. Ask lane choice:
   - hook-only + freestyle
   - AI coach conversation
   - full teleprompter script
6. If user picks hook-only or AI coach conversation:
   - call `POST /api/mcp/recording-link/create` with `{ "mode": "hook", "hookItemId": "<id>" }`.
   - send only the returned `magicLink`.
   - poll status with `GET /api/mcp/interviews/status?hookItemId=<id>`.
7. If user picks full teleprompter script:
   - run teleprompter flow first, then create teleprompter recording link.

## Teleprompter Flow (Execution)

1. If the user asks for a script based on the selected hook, call `POST /api/mcp/teleprompter/scripts/create` with `hookItemId` (or at least `hookText` as a fallback) so script generation preserves hook context. Include `transcriptText` when available.
2. If the agent already has a fully written script (e.g. drafted in conversation with the user), pass it as `scriptText` — this skips OpenRouter entirely and stores it directly: `{ "scriptText": "<full script text>" }`.
3. Otherwise call `POST /api/mcp/teleprompter/scripts/create` with `prompt` and optional helpers for AI generation.
4. Call `POST /api/mcp/recording-link/create` with `{ "mode": "teleprompter", "scriptId": "<id>" }`.
5. Send only the returned `magicLink`.
6. Poll status with `GET /api/mcp/interviews/status?scriptId=<id>`.

### When to use scriptText vs prompt

- `scriptText` — use when the script has already been written and agreed upon in conversation. Reliable, no LLM dependency.
- `prompt` — use when the user wants AI to generate a script from a topic or hook. Subject to OpenRouter availability.

### Hook-to-Script Continuity

- If the user says "script for that hook", do not ask for a new generic topic.
- Reuse selected hook context and generate script directly from that selection.
- Include transcript context when available so script tone and points stay aligned.

### Repurpose and Tone-Match

- If the user asks for another version in a similar voice, prefer script generation with transcript context.
- First, call `GET|POST /api/mcp/interviews/transcripts/context`.
- Build a compact transcript context block from the returned `items[].excerpt` and pass it into:
  - `POST /api/mcp/teleprompter/scripts/create` as `transcriptText`
- If no transcript items are returned, ask for a short sample paragraph in the user's preferred speaking style.

## Content Shortcut (Execution)

If the user wants content on a topic:

1. Research live sources when a browsing tool is available.
2. Read at least 2 relevant sources for time-sensitive claims.
3. Turn findings into either:
   - stronger hook-generation input, or
   - teleprompter-ready script input
4. If user asked for hooks first, call `POST /api/mcp/hooks/create` with enriched prompt details.
5. If user asked for script, call `POST /api/mcp/teleprompter/scripts/create`.
6. Create recording link via `POST /api/mcp/recording-link/create`.
7. Continue standard processing and preview flow.

## Script Generation Failure Recovery

- If script generation fails due transient provider issues, retry once automatically.
- If retry still fails, give a concise user-facing explanation and offer to:
  - retry again, or
  - draft directly from selected hook text or transcript context.
- Do not switch to shell-script workaround flows.

## Recording Link Rules

- Do not manually construct recording links when `magicLink` is available.
- Preserve `mcpPersonalToken` when present in a returned link.
- If a returned link is missing required params for its mode, retry recording-link creation once before replying.
- Send links as plain clickable URLs on their own line.

## Editing Flow

### Find an interview
1. Poll `GET /api/mcp/interviews/status` using the best identifier you have:
   - `?interviewId=<id>`
   - `?hookItemId=<id>`
   - `?scriptId=<id>`
2. When recording is uploaded, call `POST /api/mcp/interviews/process`.
3. Poll status again and resolve `interviewId` plus latest `interviewResultId`.
4. Share preview link first:
   `https://app.humeo.com/clips/output-variants?id=<interviewId>`
5. Ask:
   - "Preview is ready. Do you want the preview link so we can make edits, or should I render the video directly?"
6. If user wants final file/render, continue with render flow.
7. If user stays in preview mode, do not queue render yet.

Before editing, find the right interview using:

```
GET /api/mcp/interviews
```

**Query params** (all optional):

| Param | Description |
|---|---|
| `search` | Search interview titles (case-insensitive partial match) |
| `status` | Filter by status: `completed`, `rendering`, `editing`, `uploaded`, etc. |
| `interviewId` | Get a single interview by ID (returns `{ interview }` instead of list) |
| `page` | Page number (default 1, 20 per page) |

**Examples:**
- List all completed: `GET /api/mcp/interviews?status=completed`
- Search by topic: `GET /api/mcp/interviews?search=bootstrapping`
- Get specific: `GET /api/mcp/interviews?interviewId=<uuid>`

**Response (list):**
```json
{
  "interviews": [
    {
      "id": "uuid",
      "title": "Bootstrapping a personal brand from zero",
      "status": "completed",
      "createdAt": "2026-03-01T...",
      "updatedAt": "2026-03-01T...",
      "results": [
        { "id": "uuid", "title": "Full Edit", "resultType": "super_video", "status": "completed" },
        { "id": "uuid", "title": null, "resultType": "minimal_edit", "status": "ready" }
      ]
    }
  ],
  "total": 5,
  "page": 1,
  "pageSize": 20
}
```

Use `results[].id` as the `interviewResultId` for the edit and render endpoints. Pick the result with `status: "ready"` or `"completed"` and the desired `resultType`.

### Create custom edit variant

Creates a **new video variant** from a prompt. Unlike `POST /api/mcp/edits/apply` (which tweaks words/segments on an existing result), this re-selects which parts of the transcript to include — generating an entirely new segmentation.

Use this when:
- The user wants a different take ("make a 30-second highlight", "focus on the emotional parts", "just the actionable advice")
- The user wants to restructure what content is shown, not just trim/fix words

```
POST /api/mcp/interviews/custom-edit
```

**Body:**
```json
{
  "interviewId": "uuid",
  "prompt": "Create a punchy 30-second highlight focusing on the most confident moments",
  "presetKey": "tight_highlight"
}
```

| Field | Required | Description |
|---|---|---|
| `interviewId` | Yes | The interview to create a variant for |
| `prompt` | Yes | Freeform prompt describing the desired edit (max 4000 chars) |
| `presetKey` | No | Optional preset: `tight_highlight`, `best_moments`, `authority_style`, `emotional_story`, `actionable_advice`, `spicy_takes` |

**Response (immediate — generation runs in background):**
```json
{
  "success": true,
  "interviewResultId": "uuid",
  "customEditId": "uuid",
  "status": "processing"
}
```

### Poll custom edit status

```
GET /api/mcp/interviews/custom-edit?resultId=<interviewResultId>
```

**Response:**
```json
{
  "success": true,
  "interviewResultId": "uuid",
  "title": "Confident Founder Highlights",
  "status": "ready",
  "reasoning": "Selected the three strongest statements about scaling..."
}
```

Status values: `processing` → `ready` | `failed`

**Workflow:**
1. `POST /api/mcp/interviews/custom-edit` — returns `interviewResultId` immediately
2. Poll `GET /api/mcp/interviews/custom-edit?resultId=<id>` until status is `ready` or `failed` (typically 10-30s)
3. Once `ready`, use the `interviewResultId` with `GET /api/mcp/edits/state` and `POST /api/mcp/edits/apply` for fine-tuning
4. Render with `POST /api/mcp/renders/request`

### Read edit state

After processing completes and an `interviewResultId` is available, you can edit the video transcript before rendering.

```
GET /api/mcp/edits/state?interviewResultId=<id>
```

**Response:**
```json
{
  "interviewResultId": "uuid",
  "interviewId": "uuid",
  "selectedTheme": "journal",
  "totalDurationSeconds": 62.5,
  "editedDurationSeconds": 48.3,
  "enabledControls": { "filler": true, "silence": false },
  "version": 1,
  "segments": [
    {
      "index": 0,
      "clip_segment_id": "a1b2c3d4-...",
      "type": "main_content",
      "description": "Founder origin story",
      "startSeconds": 0.0,
      "endSeconds": 18.5,
      "isExcluded": false,
      "words": [
        { "index": 0, "text": "Hello", "startSeconds": 0.1, "endSeconds": 0.5, "isRemoved": false },
        { "index": 1, "text": "um", "startSeconds": 0.6, "endSeconds": 0.8, "isRemoved": true, "removedReason": "user" }
      ]
    }
  ]
}
```

### Apply edit (LLM-powered)

```
POST /api/mcp/edits/apply
```

**Body:**
```json
{
  "interviewResultId": "uuid",
  "instruction": "Remove the first 10 seconds and fix 'gonna' to 'going to' everywhere"
}
```

The `instruction` field accepts any natural language edit request (max 2000 chars). The server-side LLM translates it to edit overrides.

**What instructions can do:**
- Remove/restore words, time ranges, or entire segments (by index, timestamp, or word match)
- Fix caption text (single word at a specific time, or global find/replace)
- Reorder segments by telling the two time ranges or segment numbers
- Split, merge, or duplicate segments
- Toggle filler word or silence gap removal
- Undo the last edit
- Reset all edits
- Any combination in a single instruction

**Scoped word matching:** When you say "change 'hello' at 6-12s", only the 'hello' in that time range is affected — not 'hello' at other timestamps.

**Success response:**
```json
{
  "success": true,
  "summary": "3 word(s) removed; 1 segment(s) excluded",
  "newVersion": 2
}
```

**Error responses:**
- `400` — invalid body, or no previous edit to undo
- `404` — result not found or not owned by user
- `409` — concurrency conflict (re-fetch state and retry once)
- `500` — LLM or server error

### Supported edit features

#### 1. Remove/restore segments, words, or sentences
- By segment number: `Exclude segment 2`
- By time range: `Remove 10 to 15 seconds`
- By word match at timestamp: `Remove the word 'actually' near 8 seconds`
- Restore: `Bring back segment 2` or `Restore the word 'actually' near 8 seconds`

#### 2. Duplicate a segment
- `Duplicate segment 1` — creates an exact copy with the same audio/video and transcript words, inserted right after the original.

#### 3. Reorder segments
- `Swap segment 0 and segment 2`
- `Move the segment at 10-20s before the segment at 0-10s`

#### 4. Replace a word
- Single: `Change 'hello' to 'hola' at 6 seconds` — only the 'hello' near 6s is changed.
- Global: `Replace all 'gonna' with 'going to'` — changes every occurrence.

#### 5. Toggle filler/silence removal
- `Enable filler word removal`
- `Disable silence removal`

#### 6. Custom edits via prompt
- Any natural language edit instruction is sent to the server-side LLM, which produces the correct edit overrides and saves them to the DB (same format as edits made from the Humeo manual editor UI).

#### 7. Merge segments
- `Merge segments 1 and 2` — combines their clips and words into one segment. Can be unmerged later.

#### 8. Undo last change
- `Undo` or `Undo last change` — instantly restores the previous edit state (no LLM call needed). Supports one level of undo/redo (sending undo again will redo).

### Non-destructive editing rules

- All edits are reversible. "Remove" = hide/disable, not destroy.
- Segments → excluded (toggle eye icon). Can be re-included.
- Words → strikethrough/disabled. Can be restored.
- When the user says "remove", "cut", or "delete" → send it as the instruction. The LLM handles the non-destructive mapping.

### Edit workflow

1. Call `GET /api/mcp/edits/state?interviewResultId=<id>` to see current state.
2. Call `POST /api/mcp/edits/apply` with a natural language instruction.
3. Check `success` in response. On `409`, re-fetch state and retry once.
4. Optionally re-read state to confirm changes.
5. Proceed to render when satisfied.

### Example edit instructions

| User says | Instruction to send |
|---|---|
| Remove the intro | `Exclude the first segment` |
| Cut 10-15 second part | `Remove the part from 10 to 15 seconds` |
| Remove 'hello' at 6s | `Remove the word 'hello' near 6 seconds` |
| Clean up fillers | `Enable filler word removal` |
| Disable silence gaps | `Disable silence removal` |
| Fix "their" to "there" at 15s | `Fix the word 'their' to 'there' around 15 seconds` |
| Replace all "gonna" | `Replace all occurrences of 'gonna' with 'going to'` |
| Duplicate the second clip | `Duplicate segment 1` |
| Move last segment first | `Move the last segment to the beginning` |
| Swap segment 0 and 2 | `Swap segment 0 and segment 2` |
| Merge first two segments | `Merge segments 0 and 1` |
| Undo that | `Undo` |
| Start fresh | `Reset all edits to the original state` |

## Processing And Render Flow

1. Poll `GET /api/mcp/interviews/status` with the best available identifier (`interviewId`, `hookItemId`, or `scriptId`).
2. When the interview is uploaded, call `POST /api/mcp/interviews/process`.
3. Poll `GET /api/mcp/interviews/status` again and resolve `interviewResultId` from returned `results`.
4. (Optional) Edit the transcript using the Editing Flow above.
5. Queue render with `POST /api/mcp/renders/request`.
6. Poll `POST /api/mcp/renders/download` until a signed `url` is returned.

## Preview-First Delivery

- Before the user confirms download, share preview links only.
- Default preview page:
  `https://app.humeo.com/clips/output-variants?id=<interviewId>`
- If the user asks the agent to download and send the file, then fetch it and deliver it in chat.
- Do not proactively download and upload files without explicit user request.

## Publishing Flow (Execution)

- Upload target API: `POST https://api.upload-post.com/api/upload`
- Auth format: `Authorization: Apikey <key>`
- Method: `multipart/form-data`
- Default platforms (if configured): Instagram and YouTube
- Never hardcode or expose API key or managed-user handle.

### Upload command template (Internal reference only)

```powershell
$apiKey = "<upload-post-api-key>"
$videoPath = "<local path to mp4>"
$title = "<title>"
$user = "<managed user handle>"

curl.exe `
  -H "Authorization: Apikey $apiKey" `
  -F "video=@$videoPath" `
  -F "title=$title" `
  -F "user=$user" `
  -F "platform[]=instagram" `
  -F "platform[]=youtube" `
  -X POST https://api.upload-post.com/api/upload
```

### Upload workflow

1. Ensure render is downloaded to a local MP4.
2. Ask for title if unclear from hook or script.
3. Use upload-post only when operator configured API key and managed user.
4. Report per-platform success or failure from API response.

## Testing the Calendar & Reminders

### Quick end-to-end test

1. **Add a test item due today:**
   ```
   POST /api/mcp/calendar/add
   { "topic": "Test reminder", "recordingMode": "teleprompter", "targetDate": "<today ISO>" }
   ```

2. **Verify it shows as due:**
   ```
   GET /api/mcp/calendar/due?withinHours=24
   ```
   Should return `count: 1` with your test item.

3. **Manually trigger the cron:**
   ```bash
   openclaw cron run videoclaw-daily-calendar-reminder
   ```
   The isolated agent runs immediately. Check Telegram — the reminder should arrive within ~30 seconds.

4. **Verify reminded_at was stamped:**
   ```
   GET /api/mcp/calendar/due?withinHours=24
   ```
   Should now return `count: 0` (item is in 20h cooldown).

5. **Clean up:** `PATCH /api/mcp/calendar/{id}/status` with `{ "status": "skipped" }`.

### Checking cron run history
```bash
openclaw cron runs --id videoclaw-daily-calendar-reminder --limit 5
```

### Checking all cron jobs
```bash
openclaw cron list
```

### Temporarily disabling
Set `enabled: false` in `~/.openclaw/cron/jobs.json` for the job entry, then restart OpenClaw.

---

## Calendar Notification System

Three layers of notifications — all created during First-Time Setup (see SKILL.md), all bearer-authenticated via PAT from local token file, never hardcoded.

### Credentials file

```
~/.videoclaw_personal_mcp_token
humeo_pat_...
```

### Notification channel preference

Stored in `~/.openclaw/workspace/USER.md` under `## Notifications`:
```
## Notifications
- Preferred reminder channel: telegram
```
Used by the heartbeat when creating per-event crons, and set in daily/weekly cron delivery at setup time.

### 1. Heartbeat — per-event reminder crons

Runs every ~30 min in the main session. Scans `planned` items, creates one-shot crons for any that have a future `reminderFiresAt` but no `cronJobId`. See `HEARTBEAT.md` for the full logic.

### 2. Daily digest cron

Job ID: `videoclaw-daily-calendar-reminder` · fires at user's chosen morning time

- GET `/api/mcp/calendar/due?withinHours=24` — finds items due today
- Prepares handoff links, stamps `reminded_at`, sends one grouped message
- Quiet hours respected: 23:00–08:00 → skip sending

**CLI:** `openclaw cron run videoclaw-daily-calendar-reminder`

### 3. Weekly summary cron

Job ID: `videoclaw-weekly-summary` · fires every Sunday at 9AM (user's timezone)

- Fetches `recorded`, `planned`, and `skipped` items
- Sends a single week-in-review message: completed, upcoming, skipped counts + topics

**CLI:** `openclaw cron run videoclaw-weekly-summary`

### reminded endpoint

- `POST /api/mcp/calendar/{id}/reminded` — stamps `reminded_at` on the item
- No body required
- Returns `{ success: true, remindedAt: "<iso>" }`
- **Only needed for per-event one-shot crons** that fetch a specific item by ID. The `/due` endpoint atomically stamps `reminded_at` on every item it returns, so the daily digest cron does not need to call this separately.

## Content Calendar Flow

### Adding an item

1. Always ask for `recordingMode` if not provided. Valid: `hook`, `teleprompter`, `full`, `idea`.
2. Always ask for `reminderMinutes` if `targetDate` is provided. Default: 30. Range: 5–1440.
3. Body: `{ topic, recordingMode, notes?, targetDate?, reminderMinutes? }`
4. `targetDate` must be ISO 8601 (e.g. `"2026-03-25T09:00:00Z"`).
5. Response includes `reminderFiresAt` — use this as the `at` value when creating the per-event cron.
6. After add: create one-shot cron + store `cronJobId` via PATCH (see SKILL.md Per-Event Reminder Crons).

### Listing / reviewing

- `GET /api/mcp/calendar/list?status=planned` — default view
- Response includes `daysUntilTarget` (negative = overdue) and `handoffReady` flag.

### Preparing a recording link

- `POST /api/mcp/calendar/{id}/prepare` — generates handoff link based on stored `recordingMode`:
  - `hook` → runs hook generation from the topic, picks first hook, creates handoff link
  - `teleprompter` → generates script from topic, creates teleprompter handoff link
  - `full` / `idea` → creates handoff directly
- Stores `handoffUrl` and `handoffExpiresAt` back on the calendar row.
- Returns `{ handoffUrl, expiresAt, mode, item }`.
- **Send the returned `handoffUrl` directly — never construct recording links manually.**

### Updating an item (topic, date, mode)

- `PATCH /api/mcp/calendar/{id}` — body can include any of: `topic`, `notes`, `targetDate`, `recordingMode`
- Only provided fields are updated — omitted fields are left unchanged
- Use this when the user reschedules a recording or corrects the topic
- `targetDate` accepts any ISO 8601 string, or `null` to clear the date

### Updating status

- `PATCH /api/mcp/calendar/{id}/status` — body: `{ status, hookGenerationId?, scriptId?, interviewId? }`
- Statuses: `planned → scripted → recorded → published → skipped`
- When the user replies "done" after recording, call this with `{ status: "recorded" }`.

### Checking due items (used by heartbeat/cron)

- `GET /api/mcp/calendar/due?withinHours=24`
- Returns `planned` items due within the window, excluding those reminded within the last 20h.
- Each item includes `handoffReady: true/false` — use `/prepare` if `false`.
- `/due` atomically stamps `reminded_at` for all returned items; use `GET /api/mcp/calendar/{id}` for one-item checks in one-shot reminder jobs.

### Calendar rules

- Never add a calendar item without a `recordingMode`. Ask the user first.
- Never manually construct recording URLs from calendar data. Always use `/prepare`.
- Deliver reminders via Telegram with a direct clickable link on its own line.
- Respect quiet hours (23:00–08:00) — skip sending during this window.

## Telegram Constraint

- Telegram is the command, status, and delivery channel.
- The browser recording page is the recording interface.

## Response Style

- Sound human and calm.
- Do not narrate low-level internal actions line by line.
- Do not expose implementation chatter unless the user explicitly asks.
- Avoid lines like:
  - "Let me verify the PAT and kick this off."
  - "Now let me research this."
  - "Looks like the API wants either a prompt or scriptText field."
  - "Now creating the recording link."
- Prefer lines like:
  - "I found a strong angle for this."
  - "Your script is ready."
  - "Open this to record."
  - "Your preview is ready."
  - "If you want me to download the final file, I can send it here."
  - "You still need one thing: a PAT from `https://app.humeo.com/profile/mcp`."
- If live research is unavailable, say so in one plain sentence and move forward with the next-best path.
- If something fails, summarize it cleanly in one human sentence and move to the next action.
