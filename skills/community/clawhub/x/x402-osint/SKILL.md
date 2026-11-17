# x402 OSINT Skill

Pay-per-call OSINT for OpenClaw agents: find the public footprint behind a username
or email, paid automatically in USDC on Base via x402. No API keys, no accounts.

## Install

```
openclaw skills install @JienWeng/x402-osint
```

## Prerequisites

- `EVM_PRIVATE_KEY` — a Base wallet funded with a few dollars of USDC. The agent signs
  the x402 payment; the facilitator covers gas (no ETH needed).
- `MAX_SPEND_PER_CALL` — recommended `$0.05` (a full report is $0.05; a lookup is $0.01).

## Activation triggers

- "look up the username <handle>"
- "what accounts is <handle> on"
- "check the email <address>"
- "run an OSINT report on <handle>"
- "profile this handle: <handle>"

## Commands (OpenClaw's x402 auto-handler pays + retries transparently)

| Intent | Request | Price |
|---|---|---|
| Free trial | `GET https://x402-osint.tail66f665.ts.net/trial/osint/{username}` | free |
| Username lookup | `GET https://x402-osint.tail66f665.ts.net/osint/{username}` | $0.01 |
| Identity report | `GET https://x402-osint.tail66f665.ts.net/report/{username}` | $0.05 |
| Email lookup | `GET https://x402-osint.tail66f665.ts.net/email/{address}` | $0.03 |

Every response includes a natural-language `summary` field the agent can use directly.

## MCP alternative (free discovery tools)

```json
{ "mcpServers": { "x402-osint": { "url": "https://x402-osint.tail66f665.ts.net:10000/mcp" } } }
```
Tools: `osint_lookup(username)`, `osint_email(address)`. For depth, use the paid HTTP endpoints.

## Responsible use

Public profiles only. Use for legitimate purposes — recruiting research, prospecting,
due diligence, trust & safety, brand protection, or a person's own exposure audit.
Not for harassment, stalking, or profiling specific individuals without a lawful basis.
