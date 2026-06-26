---
name: savenow
description: Save durable notes from the current OpenClaw + Telegram conversation into today's memory/YYYY-MM-DD.md, with a semantic-dedupe preview/apply flow and inline Apply/Cancel buttons. Use for /savenow on Telegram-backed sessions.
user-invocable: true
version: 0.1.1
metadata: {"openclaw":{"requires":{"bins":["node"],"surface":"telegram"},"homepage":"https://docs.openclaw.ai/tools/skills"}}
---

# savenow

Use this skill when the user wants to persist the current conversation into the active agent's daily memory file.

The command name is `/savenow`.

**Scope:** OpenClaw + Telegram only. Relies on `sessions_list` / `sessions_history`, the runtime `MessageThreadId`, and Telegram inline keyboards. Vanilla Claude Code, CLI, and web surfaces are not supported by design.

Supported forms:

- `/savenow` — preview only. Extract candidates, compare semantically against today's memory, show markdown diff + Apply/Cancel inline buttons. **Writes nothing.**
- `/savenow apply` — write the most recent pending preview (within the 30-minute TTL and from the same session/topic).
- `/savenow cancel` — discard the pending preview without writing.
- `/savenow auto` — extract + compare + write directly. Skip preview and buttons.
- `/savenow auto <sessionKey>` — auto on an explicit session.
- `/savenow list` — show same-topic candidate sessions without writing.
- `/savenow <sessionKey>` — preview against an explicit session.

## Goal

Write only durable, high-value notes to `memory/YYYY-MM-DD.md` in the current agent workspace.

Do not patch built-in commands. Do not change Telegram settings. Do not write `MEMORY.md`.

## What counts as durable

Keep:

- resolved root causes and fixes
- stable workflow rules and conventions
- preferences and routing rules
- important system mappings, ids, and file locations
- decisions that will matter again later

Skip:

- chit-chat and acknowledgements
- temporary plans or one-off status updates
- repetitive back-and-forth with no lasting value
- content already saved today in the same or very similar form

## Routing

Inspect the raw command argument first and pick a branch:

| Arg               | Branch                 | Writes?            |
|-------------------|------------------------|--------------------|
| (empty)           | preview                | no                 |
| `list`            | list (unchanged)       | no                 |
| `apply`           | apply                  | yes, from pending  |
| `cancel`          | cancel                 | no, deletes pending|
| `auto`            | auto on resolved session | yes              |
| `auto <key>`      | auto on explicit key   | yes                |
| other token       | explicit-session preview | no               |

## Preview branch — `/savenow` (and explicit-session preview)

1. **Resolve the target session.**
   - If runtime exposes `CommandTargetSessionKey`, use it.
   - If the raw arg is a non-empty value other than `list`/`apply`/`cancel`/`auto`, treat it as the explicit `sessionKey`.
   - Else read the current `MessageThreadId` from runtime, call `sessions_list`, filter strictly:
     - same topic/thread only
     - exclude keys containing `:slash:`
     - exclude `cron`, `hook`, `node` kinds
     - exclude command-only or internal helper sessions
   - If exactly one clear candidate remains, use it. If multiple, pick the newest non-slash real chat session from the same thread.
   - If thread is missing, no same-topic candidate exists, or it stays ambiguous, fail closed and ask the user to rerun `/savenow <sessionKey>`. Do not write.

2. **Read the transcript.** Call `sessions_history` against the resolved target session with `includeTools: false`, `limit: 120..180`.

3. **Read today's memory file (new step).** Use the Read tool on `memory/YYYY-MM-DD.md` so the agent can perform semantic comparison. If the file does not exist yet, proceed as if empty.

4. **Extract `0..5` candidate memory entries.** Each entry must be specific, reusable, short, self-contained. For each candidate, perform **semantic comparison against existing sections in the memory file** and assign an `action`:

   - `"add"` — net-new durable note
   - `"merge"` — substantial overlap with an existing section; adds new bullets to it (set `merge_target_title` to the exact existing title)
   - `"skip"` — semantically already covered, or not durable enough

   JSON shape (write to `temp/savenow-entries.json`):

   ```json
   [
     {
       "candidate_index": 0,
       "title": "Gateway token mismatch fix",
       "bullets": [
         "Resolved `unauthorized: gateway token mismatch` by updating `gateway.cmd` and the related env variables.",
         "Next time a similar error appears, check token and env alignment first."
       ],
       "action": "add",
       "reason": ""
     },
     {
       "candidate_index": 1,
       "title": "Telegram inline button rules",
       "bullets": ["Inline keyboards use a single-row, 3-button layout."],
       "action": "merge",
       "merge_target_title": "Telegram UI conventions",
       "reason": "New rule belongs to the same existing topic."
     }
   ]
   ```

   Backward-compat: `{ "title": "...", "bullets": [...] }` without `action` is treated as `"add"`.

5. **Run the preview script** from the workspace root:

   ```text
   node "{baseDir}/scripts/preview-diff.mjs" \
     --entries-file "temp/savenow-entries.json" \
     --memory-path "memory/YYYY-MM-DD.md" \
     --pending-file "temp/savenow-pending.json" \
     --session-key "<resolved sessionKey>" \
     --message-thread-id "<MessageThreadId>" \
     --ttl-minutes 30
   ```

6. **Pipe the script's stdout to the chat as the user-facing reply.**

7. **Render a Telegram inline keyboard** below the markdown reply, two buttons in a single row:

   - `✅ Apply` → callback `/savenow apply`
   - `❌ Cancel` → callback `/savenow cancel`

   If the script reports 0 candidates, do not render the keyboard (nothing to apply).

## Apply branch — `/savenow apply`

1. Read `temp/savenow-pending.json`. Reject with a one-liner if:
   - file is missing → `"No pending preview, run /savenow first."`
   - `expiresAt < now` → `"Preview expired (X min ago), rerun /savenow."`
   - `sessionKey` or `messageThreadId` mismatches the current runtime → `"Pending preview is from a different topic. Rerun /savenow here."`

2. Run the merge script using `entriesFile` from the pending JSON:

   ```text
   node "{baseDir}/scripts/merge-daily-memory.mjs" --entries-file "<pending.entriesFile>"
   ```

3. On success delete `temp/savenow-pending.json` (and the entries file if you wish to clean up).

4. Reply briefly (no buttons):

   ```text
   Saved to memory/2026-05-15.md: Gateway token mismatch fix (+2 bullets to "Telegram UI conventions").
   Mini summary: saved gateway auth fix and a Telegram button rule.
   ```

   Mention added titles, merged titles (with bullet counts), and any `fallbackAdded` / `fallbackSkipped` events from the script's JSON output.

## Cancel branch — `/savenow cancel`

1. If `temp/savenow-pending.json` exists, delete it. Also delete `temp/savenow-entries.json` if it exists.
2. Reply: `Pending preview cancelled. Nothing written.`
3. If there was no pending file, reply: `No pending preview to cancel.` (not an error.)

## Auto branch — `/savenow auto [sessionKey]`

1. Run steps 1–4 from the preview branch (resolve session, pull transcript, read today's memory, extract candidates with actions).
2. Skip the preview script and pending file.
3. Run the merge script directly:

   ```text
   node "{baseDir}/scripts/merge-daily-memory.mjs" --entries-file "temp/savenow-entries.json"
   ```

4. Reply with the same "Saved to memory/… + mini summary" format. No buttons.

## List branch — `/savenow list`

Call `sessions_list` and return same-topic candidate sessions only. Do not write.

## Memory file format

```text
# YYYY-MM-DD

## HH:MM - Short title
- bullet
- bullet
```

For merges, the script appends new bullets in-place to the matched section and adds a trailing `- (merged HH:MM)` marker bullet. A second merge into the same section replaces the previous marker rather than stacking.

## Important constraints

- Default `/savenow` never writes — it previews and shows Apply/Cancel buttons.
- Only auto-resolve within the current topic/thread. If unresolvable, fail closed.
- Do not fall back to a global "most recent session" guess.
- Let the merge script handle same-day dedup, in-place merges, and file creation.
- Do not manually append markdown yourself unless the script is unavailable.
- Always include the mini summary line after a successful `apply` or `auto`.
- Inline buttons only on the preview branch and only when the script reports ≥1 candidate.
