---
name: voxrn
description: Place phone calls, send SMS, search contacts, and run agent dispatches via Voxrn. Bridges any OpenClaw-bridged chat (Slack, Telegram, iMessage, WhatsApp, Discord, more) to a real PSTN.
metadata: {"clawdbot":{"emoji":"📞","requires":{"bins":["openclaw"]},"links":{"home":"https://voxrn.com","docs":"https://voxrn.com/docs/integrations/openclaw"}}}
---

# Voxrn 📞

Voxrn is a browser-native voice + SMS platform with an MCP-driven agent runtime. This skill registers Voxrn as an outbound MCP server in your OpenClaw workspace, so the agent can place calls, send messages, manage contacts, and watch live agent sessions from any bridged chat.

## When to use this skill

Reach for these tools when the user asks to:
- **place a phone call** — "call my plumber", "ring the front desk", "dial +1 415 555 0188"
- **send a text message** — "text Mina that I'm running 5 min late"
- **find a contact** — "what's the number for Atlas Freight?"
- **save someone to contacts** — "save +1 415 555 0188 as Front Desk"
- **see what's on the wire** — "are any agent calls running?"
- **end a runaway agent call** — "kill the call to Mina"
- **check the balance** — "what's my Voxrn balance"

## Tool catalog

| Tool | Args | Use it for |
|---|---|---|
| `call.place` | `{ to: E.164, taskBrief?: string, voiceProfileId?: string }` | Dial out — agent runs the call following the task brief |
| `call.list_active` | none | Show currently-live calls in the workspace |
| `call.end` | `{ callSid: string }` | Hard-kill an active call by SID |
| `transcript.stream` | `{ callSid: string }` | Subscribe to live captions for a call |
| `message.send` | `{ to: E.164, body: string }` | Send an SMS |
| `contact.search` | `{ q: string }` | Free-text search across name, number, tag |
| `contact.upsert` | `{ name, number, tags?, notes? }` | Create or update a contact |
| `balance.check` | none | Read the workspace balance in USD |

## Configuration

Set these env vars (or use OpenClaw's secrets manager):

```bash
export VOXRN_API_KEY="vxk_..."   # mint at https://voxrn.com/enterprise/dashboard/agents
export VOXRN_BASE_URL="https://voxrn.com"  # optional; defaults to prod
```

Or:

```bash
openclaw config secrets set voxrn_api_key vxk_...
```

The skill's `mcp.json` reads `${VOXRN_API_KEY}` at MCP-registration time so the secret never reaches the agent's prompt window.

## Conventions the agent should follow

- **Confirm the destination first.** If the user says "call Atlas", run `contact.search { q: "Atlas" }` and ask which match before placing the call.
- **Quote the cost before running `call.place`.** Default rate-card multiplier is 1.25× over carrier; international calls can be more. Either ask "ok if this costs ~$X for a 2-minute call?" or run `balance.check` first.
- **Pass the user's prose into `taskBrief`.** Don't reformat — the brief travels straight to the agent runtime.
- **Confirm before `call.end`** unless the user explicitly said "kill it now". Action is destructive and audit-logged.
- **Never echo the API key.** The skill registers the server with `${VOXRN_API_KEY}` so the agent never sees the secret.

## Examples

### Place a call

> *User:* call my plumber and ask if Thursday morning works for the kitchen sink

```text
agent: contact.search { q: "plumber" }
→ [{ id: "c-12", name: "Atlas Plumbing", number: "+14155551234", tags: ["plumber"] }]

agent: balance.check {}
→ { usd: 23.40 }

agent: "Calling Atlas Plumbing at +1 415 555 1234 to ask about Thursday morning availability. Estimated cost: ~$0.04. Going ahead."

agent: call.place {
  to: "+14155551234",
  taskBrief: "Call Atlas Plumbing on the user's behalf. Ask if Thursday morning is available to fix a kitchen sink leak. If yes, confirm a 9am window. If no, ask what's their next opening this week."
}
→ { callSid: "CAabc...", reservedUsd: 0.04 }

agent: "Call placed. SID CAabc... — I'll let you know when it ends."
```

### End a call

> *User:* kill the call to Mina, the agent's stuck

```text
agent: call.list_active {}
→ [{ callSid: "CAxyz...", to: "+14155557890", durationSeconds: 142, billedUsd: 0.05 }]

agent: "I see one active call to +1 415 555 7890 — duration 2:22, $0.05 spent. End it?"
user: yes
agent: call.end { callSid: "CAxyz..." } → { ok: true }
```

### Send an SMS follow-up

> *User:* text Mina that the meeting moved to 2pm tomorrow

```text
agent: contact.search { q: "Mina" }
→ [{ id: "c-1", name: "Mina Hart", number: "+14155557890" }]

agent: message.send { to: "+14155557890", body: "Hey Mina — meeting moved to 2pm tomorrow. — Sent via Voxrn" }
→ { messageSid: "SMabc...", segments: 1, billedUsd: 0.0079 }

agent: "Sent."
```

## Troubleshooting

- **`401 Unauthorized` from a Voxrn tool** — your API key is wrong, expired, or the workspace it belongs to has been removed. Mint a fresh key at https://voxrn.com/enterprise/dashboard/agents → API keys.
- **Calls succeed but the agent says nothing** — destination might have hit voicemail or returned `caller_audio_failed`. Check `call.list_active` for state. The Voxrn live monitor mirrors this view at `https://voxrn.com/enterprise/dashboard/agents`.
- **`balance.check` returns 0** — top up the workspace via Stripe or USDC at `https://voxrn.com/account → Billing`.

## See also

- [Voxrn docs — MCP overview](https://voxrn.com/docs/agents/mcp)
- [Voxrn docs — OpenClaw integration](https://voxrn.com/docs/integrations/openclaw)
- [Voxrn API reference](https://voxrn.com/docs/mcp)
- [OpenClaw — outbound MCP servers](https://docs.openclaw.ai/cli/mcp)
