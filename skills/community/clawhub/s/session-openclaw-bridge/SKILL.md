---
name: session-openclaw-bridge
description: Configure, validate, and troubleshoot a Session Messenger ↔ n8n ↔ OpenClaw bridge for two-way text messaging and image exchange when the hosted relay supports attachments. Use when setting up or repairing the n8n/OpenClaw side of a Session relay, importing or patching the n8n workflow, validating relay endpoints like /health, /poll, and /send, checking whether the deployed relay matches the expected API, confirming attachment capability for photos/files, or preparing the integration for publication on ClawHub.
---

# Session ↔ OpenClaw bridge

Use this skill to manage the OpenClaw and n8n side of a Session Messenger relay.

## Scope

Handle:
- n8n workflow generation/import/patching
- relay health validation
- endpoint verification for `/health`, `/poll`, `/send`, and attachment download when present
- mismatch detection between deployed relay and expected API
- OpenClaw endpoint wiring guidance
- packaging the skill for reuse or publication

Do not assume the Session relay should implement OpenClaw chat generation internally. Keep the model:
- relay handles Session connectivity and exposes HTTP endpoints
- n8n orchestrates polling, filtering, and reply delivery
- OpenClaw generates replies

## Primary files

Read these when needed:
- `references/openclaw-session-relay-workflow.json` — n8n workflow template
- `references/release.md` — shared publication version for the skill and relay project
- `scripts/validate_relay.py` — probe relay endpoints and summarize readiness

## Expected relay API

Expected minimum HTTP API:
- `GET /health`
- `GET /poll?since=<seq>&limit=<n>`
- `POST /send`

Optional attachment endpoint for image/file workflows:
- `GET /attachment/:messageId/:attachmentId`

Expected `/health` fields for a correct modern deployment:
- `ok`
- `sessionId`
- `inboundEnabled`
- `queued`
- `lastSeq`

If `/poll` returns 404 or `/health` omits the inbound queue fields, treat the deployed relay as an older/wrong build.

## n8n workflow model

Preferred flow:
1. Cron trigger
2. Poll Session relay `/poll`
3. Extract next cursor
4. Split messages
5. Filter allowed sender
6. POST message text to OpenClaw endpoint
7. POST reply to relay `/send`

The relay is text-first but may support image/file exchange when its `/health` capabilities and implementation confirm attachment receive/send support. Do not promise calls or live media.

## OpenClaw endpoint note

Do not invent the OpenClaw HTTP endpoint. Confirm the actual endpoint and payload shape before activation.

## Packaging

Current shared release version: `0.1.0`

Package with:
```bash
scripts/package_skill.py /home/openclaw/.openclaw/workspace/skills/session-openclaw-bridge
```

If preparing for ClawHub, ensure:
- the skill release version matches the hosted relay project version
- the packaged skill contains only:
  - `SKILL.md`
  - minimal scripts
  - references actually used by the skill
