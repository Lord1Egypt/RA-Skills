---
name: worldloops
description: Agent Execution Guard by WorldLoops — a safe-by-default responsibility layer for AI agents that turns scattered work signals into governed open loops while preserving externalWrite:false.
version: "1.12.0"
homepage: https://github.com/swit001/worldloops
metadata: {"openclaw":{"requires":{"bins":["node","npm"]},"envVars":[{"name":"WORLDLOOPS_API_BASE_URL","required":false,"description":"Optional WorldLoops API base URL override. Defaults to https://api.worldloops.ai."},{"name":"WORLDLOOPS_API_KEY","required":false,"description":"Optional bearer token for hosted WorldLoops API."}],"emoji":"🌐","homepage":"https://github.com/swit001/worldloops","skillKey":"worldloops","tags":["openclaw","clawhub","agentic-ai","world-model","executable-world","open-loops","open-loop-management","workflow","human-in-the-loop","safe-by-default","auditable-runtime","stateful-loop-management","agent-execution-guard","execution-governance","execution-contracts","proposal-engine","workflow-governance"]}}
---

# Agent Execution Guard

Agent Execution Guard is a WorldLoops skill for OpenClaw.

It turns signals from tools, messages, and workflows into governed open loops:

Signal → Open Loop → Proposal → Approval → Local Transition → Receipt

It helps agents avoid unsafe or premature execution by keeping action proposals inside a safe, auditable boundary.

---

## Why it matters

Most agents answer from a snapshot.
WorldLoops tracks what remains unresolved.

When an email, calendar event, Slack message, or GitHub notification implies unfinished responsibility, Agent Execution Guard surfaces it as a governed open loop — not a silent side effect.

Every proposed action requires approval before any local transition is committed.
No external system is changed.
`externalWrite:false` is preserved throughout.

---

## Quick Start

```bash
clawhub install worldloops
cd ~/.openclaw/workspace/skills/worldloops
npm run demo
```

### Optional Safety Check

```bash
npm run doctor
```

---

## Example demo output

```bash
npm run demo
```

```
🦞 Agent Execution Guard

🚨 High — Gmail callback requested
State: open

Proposal:
Review claim context and decide whether to call back or prepare a written response. This is a local planning action only — do not initiate any call, email, or external communication without an explicit decision.

Adjudication:
requires_approval

✅ Safe
externalWrite:false
No email, draft, call, or external change made.
```

---

## Safety posture

Agent Execution Guard does not send emails.
Agent Execution Guard does not post chat messages.
Agent Execution Guard does not create calendar events.
Agent Execution Guard does not modify external systems.

```
✅ 0 emails sent
✅ 0 calendar events changed
✅ 0 chat messages posted
✅ 0 files modified
✅ 0 project changes made
✅ externalWrite:false enforced
```

OpenClaw reads signals.
WorldLoops guards execution.

WorldLoops does not need to own every connector.
If a host agent can read a signal, it can pass it to Agent Execution Guard.

OpenClaw observes and interprets source signals (Gmail, Calendar, Slack, GitHub) into `ObservedSignal[]`.
WorldLoops reads those OpenClaw-authored interpreted observations and adjudicates their lifecycle state — into active open loops, attached context, suppression receipts, and transitions.
WorldLoops does not connect to Gmail, Calendar, or Slack directly. `externalWrite:false` is preserved throughout.

---

## OpenClaw Signal Handoff

OpenClaw reads. Agent Execution Guard governs.

No connectors added.
No OAuth added.
No external write.

A host agent (OpenClaw, gog, or any other) reads signals from Gmail, Calendar, Slack, or GitHub.
It places the already-read payload as a local JSON file.
Agent Execution Guard receives that payload, normalizes it into an `AdapterSignal`, and produces a governed receipt.

```
OpenClaw / gog reads Gmail / Calendar / Slack / GitHub
    ↓
already-read payload → .worldloops/inbox/openclaw-gmail-live.json
    ↓
npm run guard:gmail -- --input .worldloops/inbox/openclaw-gmail-live.json --compact
    ↓
Agent Execution Guard
    ↓
governed open loop → proposal → receipt
externalWrite:false
```

### Accepted local payload formats

Agent Execution Guard can consume local payloads in these forms:

- **AdapterSignal JSON** — fully normalized signal with `source`, `sourceType`, `text`, `observedAt`, `externalWrite:false`
- **OpenClaw-style handoff payloads** — already-normalized payloads from OpenClaw host agents
- **gog-style Gmail payloads** — `{ "messages": [...] }` output from gog Gmail reads
- **gog-style Calendar payloads** — `{ "events": [...] }` output from gog Calendar reads
- **Slack host/plugin payloads** — `{ "channel": "...", "messages": [...] }` output from Slack host tools

gog and OpenClaw read Gmail, Calendar, and Slack.
Agent Execution Guard only consumes the local JSON output they produce.
No Gmail, Calendar, or Slack API call is made by WorldLoops.
`externalWrite:false` is preserved throughout.

### Local handoff directory

Host agents should place payloads here:

```
.worldloops/inbox/openclaw-gmail-live.json
.worldloops/inbox/openclaw-calendar-live.json
.worldloops/inbox/openclaw-slack-live.json
.worldloops/inbox/openclaw-github-live.json
```

The `.worldloops/inbox/` directory is created automatically on first run and is gitignored by default.

Redacted payload examples are in `examples/handoff/`.

---

## OpenClaw + WorldLoops

OpenClaw is excellent at observing possible signals from user-facing queries such as "What did I miss?" or "What should I do today?"

WorldLoops starts after observation.

It takes OpenClaw-observed candidate signals and adjudicates whether they are real open loops, suppressing noise such as promotional messages, FYI-only updates, duplicates, and weak evidence. Accepted signals become stateful open loops that can move through To Do, Doing, Done, Snoozed, or Escalated.

### Run

```bash
npm run openclaw:intake -- --input scripts/fixtures/openclaw-signal-intake/mixed-observations.json
```

### OpenClaw Observation Adapter contract

```
observedBy        "openclaw"
observationIntent new_loop | state_transition | noise | related_context | evidence
source            gmail | slack | calendar | github | manual
sourceId          source-unique identifier for deduplication
title             human-readable signal title
text              full signal text
timestamp         ISO 8601
actor             sender / requester (optional)
dueAt             deadline (optional)
evidence          source-specific fields (subject, snippet, channel, location…)
confidence        0.0–1.0 (optional; < 0.4 → needs_review)
relatedContext    null | { existingLoopKey, type, note } | { observationId, type }
```

### Adjudication verdicts

```
accepted          → open loop created (todo)
suppressed        → receipt saved, no loop
attached_context  → context noted, no loop
needs_review      → flagged, no loop
state_transition  → existing loop updated (done | escalated | snoozed)
```

### Morning Brief — state-management surface

The intake run produces a morning brief showing loop lifecycle:

```
- 1 loop still open
- 1 loop closed by new evidence
- 1 loop escalated
- 6 observed signals suppressed as noise
```

---

## Daily Brief

Get a single compact summary of Gmail, Calendar, and Slack handoff payloads in one command.

OpenClaw/gog/host tools read Gmail, Calendar, and Slack.
Agent Execution Guard reads only local payload files.
No Gmail, Calendar, or Slack API call is made by WorldLoops.
`externalWrite:false` is preserved.

### How it works

1. Host tools (OpenClaw, gog, or Slack plugin) read your Gmail, Calendar, and Slack.
2. They save the already-read payloads as local JSON files in `.worldloops/inbox/`.
3. Agent Execution Guard reads those local files and produces one compact Daily Brief.

```
.worldloops/inbox/openclaw-gmail-live.json      ← Gmail payload
.worldloops/inbox/openclaw-calendar-live.json   ← Calendar payload
.worldloops/inbox/openclaw-slack-live.json      ← Slack payload
```

### Run

```bash
npm run guard:daily
npm run brief:daily
```

### Preferences

Default schedule: **09:00 local time**, default delivery channel: **local**.

View preferences:

```bash
npm run brief:preferences
```

Change delivery time:

```bash
npm run brief:preferences:set -- --time 08:30
```

Set delivery channel:

```bash
npm run brief:preferences:set -- --channel local
npm run brief:preferences:set -- --channel telegram
npm run brief:preferences:set -- --channel slack
npm run brief:preferences:set -- --channel discord
npm run brief:preferences:set -- --channel sms
npm run brief:preferences:set -- --channel email
```

Daily Brief delivery channels include local, Telegram, Slack, Discord, SMS, and email.
When referring only to chat-style channels: messenger channels such as Telegram, Slack, and Discord.

### Delivery

Generate and deliver the brief:

```bash
npm run brief:deliver
npm run brief:deliver -- --dry-run
npm run brief:deliver -- --channel telegram
```

Delivery notes:
- Channel `local` prints the brief to stdout.
- Remote channels (Telegram, Slack, Discord, SMS, email) require a host scheduler or integration to be active.
- If no integration is active, the command exits 0 with a delivery-ready message and the brief text.
- WorldLoops does not install cron, launchd, or background daemons.
- A host scheduler (e.g. OpenClaw) may call `npm run brief:deliver` at the configured time.

### Example output — payloads connected

```
🦞 Agent Execution Guard Daily Brief

Sources:
✅ Gmail
✅ Calendar
✅ Slack

Open loops:

⚠️ Gmail — Review requested
From: Test Reviewer <reviewer@example.com>
Subject: Please review the submitted document
Why: review request detected
Evidence: "Please review the submitted document and send updates by EOD."
Action: Review the submitted document or reply if needed
Adjudication: requires_approval

📅 Calendar — Important context
Event: Flight to Seoul (KE 24)
When: May 21, 12:40 PM local time
Location: SFO
Reason: travel event detected, no action proposed

💬 Slack — Action requested
From: Dana
Channel: #product
Why: review or approval request detected
Evidence: "Can you review this before release?"
Action: Review and comment
Adjudication: requires_approval

✅ Safe
externalWrite:false
No email, draft, calendar event, Slack message, or external change made.

Daily Brief schedule: 09:00 local time — Delivery channel: local
To change: npm run brief:preferences:set -- --time HH:MM
```

### Example output — Gmail no-action with samples

Promotional emails (airline offers, newsletters, discount campaigns, rewards updates) and messages with "no action required" are automatically suppressed and do not generate open loops:

```
📧 Gmail — No actionable loop detected
Checked: 2 messages
Sample:
- From: promotions@airline.example.com / Subject: Earn double miles this weekend — promotion
- From: noreply@rewards.example.com / Subject: Your rewards balance: 12,450 miles
Reason: promotional or informational message; no reply, approval, review, deadline, or follow-up request detected
```

Flight and airport calendar events appear as important context without becoming approval-required tasks:

```
📅 Calendar — Important context
Event: Departure to ICN — Korean Air KE 24
When: May 21, 12:40 PM local time
Location: SFO Terminal 2, Gate G1
Reason: travel event detected, no action proposed
```

### Example output — Slack not connected

```
⬜ Slack — not connected
Reason: no Slack payload found
Next: configure OpenClaw channels.slack, then save payload to:
.worldloops/inbox/openclaw-slack-live.json
```

### Example output — payloads not connected yet

```
🦞 Agent Execution Guard Daily Brief

No local handoff payloads found yet.

Add payloads here:
- Gmail: .worldloops/inbox/openclaw-gmail-live.json
- Calendar: .worldloops/inbox/openclaw-calendar-live.json
- Slack: .worldloops/inbox/openclaw-slack-live.json

Then run:
npm run guard:daily

Source systems stay untouched.
externalWrite:false

Daily Brief schedule: 09:00 local time — Delivery channel: local
```

---

## Current commands

For everyone:

```bash
npm run demo
npm run guard:demo
npm run wow
npm run doctor
```

For Daily Brief (all sources combined):

```bash
npm run guard:daily
npm run brief:daily
npm run guard:daily -- --details
npm run brief:daily -- --inbox scripts/fixtures/inbox
npm run brief:daily -- --inbox scripts/fixtures/inbox --details
npm run brief:preferences
npm run brief:preferences:set -- --time 08:30
npm run brief:preferences:set -- --channel telegram
npm run brief:deliver
npm run brief:deliver -- --dry-run
npm run brief:deliver -- --channel telegram
```

For governed adapter invocation (already-read OpenClaw payloads):

```bash
npm run guard:adapter -- --source gmail --input <payload.json>
npm run guard:adapter -- --source gmail --input <payload.json> --compact
npm run guard:gmail -- --input <payload.json>
npm run guard:calendar -- --input <payload.json>
npm run guard:slack -- --input <payload.json>
npm run guard:github -- --input <payload.json>
```

For compact chat-friendly output:

```bash
npm run doctor:mobile
```

For developers:

```bash
npm run wow:developer
npm run loop:list
npm run loop:transition -- <loopId> doing "started local follow-up"
npm run loop:summary
npm run loop:review
npm run proposal:list
npm run proposal:show -- <proposalId>
npm run proposal:decide -- <proposalId> approve
npm run plan:list
npm run contract:list
npm run state:check
npm run receipts:verify
npm run state:repair
npm run capability:show
```

For adapter developers:

```bash
npm run adapter:validate -- examples/adapters/slack-message.json
npm run adapter:test -- examples/adapters/slack-message.json
npm run brief:reconcile -- --adapter-signal examples/adapters/slack-message.json
```

All commands preserve `externalWrite:false` and do not write to Gmail, Calendar, Slack, GitHub, or any external system.

---

## Updating

```
clawhub update worldloops
```

Force reinstall:

```
clawhub install worldloops --force
```

---

## Agent Runtime Instructions

The following section is for OpenClaw agents, not end users.

### Daily Brief routing

When the user asks for any of the following:
- Daily Brief
- morning brief
- daily summary
- today's open loops
- what did I miss
- open loops today
- Agent Execution Guard Daily Brief
- brief me

Run immediately — do not search the workspace first:

```bash
npm run --silent guard:daily
```

Return only the command output. Do not narrate the command unless the user asks.
Do not show tool search steps.
Do not inspect package.json first for Daily Brief requests.

For fixture-based Daily Brief examples:

```bash
npm run --silent brief:daily -- --inbox scripts/fixtures/inbox
```

For details mode (source identifiers):

```bash
npm run --silent guard:daily -- --details
npm run --silent brief:daily -- --inbox scripts/fixtures/inbox --details
```

For delivery-ready checks:

```bash
npm run --silent brief:deliver -- --channel telegram
```

### Demo routing

When the user asks for a demo, guard demo, execution guard demo, Agent Execution Guard demo, real signal governance demo, WorldLoops guard demo, or open-loop demo, run:

```bash
npm run --silent demo
```

Return only the compact Agent Execution Guard output.

### Runtime invocation

When the user asks you to run this skill, do the following:

1. Change into the skill directory: `{baseDir}`
2. Run the command with `--silent`
3. Use provided local payload files when available
4. If no payload files are provided, use the included fixture files
5. Return the result directly
6. Do not modify external systems

Safe default command from the skill directory:

```
npm run --silent demo
```

For Daily Brief (all local inbox sources combined):

```
npm run --silent guard:daily
npm run --silent brief:deliver
npm run --silent brief:deliver -- --dry-run
npm run --silent brief:deliver -- --channel telegram
```

For Daily Brief preferences:

```
npm run --silent brief:preferences
npm run --silent brief:preferences:set -- --time HH:MM
npm run --silent brief:preferences:set -- --channel <channel>
```

For local payload handoff:

```
npm run --silent guard:gmail -- --input <payload.json> --compact
npm run --silent guard:calendar -- --input <payload.json> --compact
npm run --silent guard:slack -- --input <payload.json> --compact
npm run --silent guard:github -- --input <payload.json> --compact
```

### OpenClaw observation write-back

When the user asks any of the following — or anything with the same intent:
- "What should I do today?"
- "What did I miss?"
- "Any follow-ups I'm missing?"
- daily brief, morning brief, open loops check

Perform your normal high-quality observation: read full message content, search memory for existing open loops, resolve actor identities, extract deadlines from natural language, and prioritize what matters to the user.

After surfacing candidates, write them as `ObservedSignal[]` to:

```
.worldloops/inbox/openclaw-observations.json
```

This is a local workspace file write only. No external system is called.

**Do not tell WorldLoops to reinterpret raw Gmail, Calendar, or Slack payloads.** WorldLoops adjudicates the interpreted observations you write here — it does not re-read source inboxes.

**Shape of each item (`ObservedSignal`):**

```json
{
  "id": "openclaw-<source>-<sourceId>",
  "source": "gmail" | "slack" | "calendar" | "github" | "manual",
  "sourceId": "<message or event ID from the source>",
  "observedBy": "openclaw",
  "userQuery": "<the question the user asked>",
  "observationIntent": "new_loop" | "state_transition" | "noise" | "related_context" | "evidence",
  "title": "<your interpreted action title — not a copy of the raw subject line>",
  "text": "<one-sentence synthesis of why this matters to the user>",
  "timestamp": "<ISO 8601>",
  "actor": "<resolved name or email — not a raw Slack user ID>",
  "dueAt": "<ISO 8601 deadline extracted from natural language, else omit>",
  "evidence": {
    "<raw field from source>": "<value>"
  },
  "confidence": 0.0–1.0,
  "relatedContext": null
}
```

For `state_transition` intent, set `relatedContext`:

```json
"relatedContext": {
  "existingLoopKey": "openclaw-<source>-<sourceId of existing loop>",
  "proposedTransition": "done" | "escalated" | "snoozed",
  "note": "<why this closes or escalates the loop>"
}
```

**What you must decide before writing — your interpretation, not shallow heuristics:**
- `observationIntent`: classify using full message content, your memory of open loops, and conversation context
- `title`: a human-readable action title synthesized from the full message — not a copy of the subject line
- `text`: one sentence on why this matters to the user right now
- `dueAt`: extract from natural language ("by Friday" → ISO date of that Friday at 17:00 local)
- `actor`: resolve Slack user IDs and display names to real identities where known
- `confidence`: your assessed certainty given full context, not field presence
- `relatedContext.existingLoopKey`: search memory for existing open loops before marking `state_transition`

**Include noise explicitly.** Promotional email, automated notifications, and informational-only items should be written with `observationIntent: "noise"` rather than omitted — WorldLoops records suppression receipts for them.

To write and validate observations, use the helper command from the skill directory:

```bash
npm run observations:write -- --input <path/to/your-observations.json>
```

This validates the `ObservedSignal[]` shape, creates `.worldloops/inbox/` if needed, and writes to `.worldloops/inbox/openclaw-observations.json`. It will refuse invalid JSON or missing required fields and exit non-zero on error.

After writing, WorldLoops `openclaw:intake` handles all lifecycle management: deduplication, open loop creation, state transitions, suppression receipts.

### Default API

By default, WorldLoops uses:

```
https://api.worldloops.ai
```

You do not need to set `WORLDLOOPS_API_BASE_URL` for the default demo flow.

To use a different backend, set:

```
WORLDLOOPS_API_BASE_URL=https://your-worldloops-api.example.com
```

Optional:

```
WORLDLOOPS_API_KEY=your_api_key
```

### Output

Default output is compact, messenger-friendly Agent Execution Guard output.
Structured JSON remains available through developer-oriented commands where supported.

### Important rules

Do not invent missing source data.
Do not send messages.
Do not send emails.
Do not create drafts.
Do not create or update calendar events.
Do not write to Slack, Gmail, Calendar, GitHub, SMS, or push channels.
Do not implement background daemons.
Do not auto-install cron or launchd.

Return the result directly.
