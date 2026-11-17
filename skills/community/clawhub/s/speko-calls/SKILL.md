---
name: speko-calls
description: Place and monitor outbound AI phone calls through Speko. This skill dials real telephone numbers and costs real money, so it needs its own platform credential and asks the user to confirm the number and the purpose before every call. Use when explicitly asked to call someone, ring a number, run an outbound voice campaign, or check the status, recording or transcript of a call that was already placed. For transcription, speech synthesis or model routing with no dialing involved, use the speko skill instead.
metadata:
  openclaw:
    requires:
      bins: [curl, jq]
      env: [SPEKO_PLATFORM_API_KEY]
---

# Speko calls

This skill dials real phones. Treat every call as irreversible: it rings a physical device,
it can reach a stranger, it is billed, and it cannot be recalled once connected.

It is deliberately separate from the `speko` skill. Speech, transcription and model routing
need only the router key and place no calls; dialing needs the **platform** key, which is a
higher-impact credential. Keeping them apart means installing speech support never grants
calling ability.

## Credential

`SPEKO_PLATFORM_API_KEY` — a **platform** key, from the Speko dashboard. Host is
`https://api.speko.dev/v1`.

This is not the router key the `speko` skill uses. The two do not cross: a router key returns
401 here, and a platform key returns 401 on `api.speko.ai`. Keys are also environment-scoped,
so a staging key fails against production.

**Only supply this key in an environment where dialing is approved, audited and expected.**
If it is absent, this skill is not eligible and no calling instruction is in play.

## Before every call

Do all four. Do not skip one because the request looked explicit.

1. **State the number back** in full E.164 and get an unambiguous yes. Never dial a number you
   inferred, completed, or guessed a country code for.
2. **State the purpose** — what the agent will say and why — and get agreement on it.
3. **Check the hour** at the destination. Do not cold-call outside normal waking hours.
4. **Stop at one call** unless the user asked for more, by number, one at a time. Never loop
   over a list without per-number confirmation.

Refuse, and say plainly why, if the request is to dial an emergency line, a premium-rate
number, a number the user does not appear to have a relationship with, or any recipient at
volume. Decline impersonation of a real person or organisation on the call.

## List the numbers you can call from

```bash
curl -s https://api.speko.dev/v1/phone-numbers \
  -H "Authorization: Bearer $SPEKO_PLATFORM_API_KEY" | jq '.[] | {id, e164, direction}'
```

Returns a **bare JSON array**, not an object. The path is kebab-case — `/v1/phone_numbers`
404s. `from` on a call must be a number the organisation owns. If it owns exactly one outbound
number, use it; if several, ask which; if none, say one has to be provisioned first.

## Place the call

```bash
curl -s https://api.speko.dev/v1/sessions/phone \
  -H "Authorization: Bearer $SPEKO_PLATFORM_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "to": "+15551234567",
    "from": "+15557654321",
    "intent": { "language": "en" },
    "systemPrompt": "You are calling to confirm a delivery window. Be brief.",
    "firstMessage": "Hi, this is an assistant calling about your delivery."
  }'
```

Only `to` is required and it is regex-checked as E.164. Supply either `agentId` for a
pre-built agent or `intent` for an ad-hoc call — an ad-hoc call needs no agent created in
advance. Also accepts `voice`, `telephony`, `llm`, `ttsOptions`, `sttOptions`, `webhookTags`
and `metadata`. Returns `{sessionId, callControlId, roomName, status, to, from}`.

**To prove a request body without ringing anyone**, post it with a deliberately invalid `to`
and read the validation error, or with a bogus `agentId` for a `404 AGENT_NOT_FOUND`. Do that
first when you are unsure about the shape.

## Follow the call

```bash
curl -s https://api.speko.dev/v1/calls/$ID \
  -H "Authorization: Bearer $SPEKO_PLATFORM_API_KEY" | jq '{status, duration_seconds, ended_at}'

curl -s https://api.speko.dev/v1/calls/$ID/report \
  -H "Authorization: Bearer $SPEKO_PLATFORM_API_KEY" | jq '{summary, outcome, cost_micro_usd}'
```

Call ids are UUIDs. `/report` carries `summary`, `outcome`, `structured_data`, a turn-by-turn
`transcript.entries[]`, and cost. **`structured_data` echoes the dialed number back**, so
anything that redacts phone numbers has to account for it too.

## Gotchas

- `GET /v1/calls/{unknown-id}` returns **500, not 404**. A 500 here usually means the id is
  wrong, not that the platform is down. Re-check the id before escalating.
- Validation errors are uniform: `{"error":"Invalid request","code":"VALIDATION_ERROR","issues":[…]}`.
- A recording may not exist yet immediately after a call ends; `recording_status` says so.
- Never paste this key into a shell command that gets logged. Read it from the environment.
