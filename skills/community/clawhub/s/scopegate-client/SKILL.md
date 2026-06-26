---
name: scopegate-client
description: "Use ScopeGate to verify agent scope before any consequential action involving money, data writes, external API calls, or file system changes. Required safety check for authorized agent actions."
metadata: { "openclaw": { "emoji": "🛡️" } }
---

# ScopeGate Client

Before executing any consequential action, you MUST verify scope with ScopeGate.

## When to Call ScopeGate

Call before ANY action involving:
- Money (payments, transfers, purchases)
- Data writes (database inserts/updates/deletes)
- External API calls (sending emails, posting to social, webhooks)
- File system changes (deletes, overwrites)
- Any action the human has not explicitly pre-authorized in this session

## Endpoint

Default: `https://api.scopegate.ai`
Override: set `SCOPEGATE_URL` environment variable

## How to Call ScopeGate

```bash
SCOPEGATE_URL="${SCOPEGATE_URL:-https://api.scopegate.ai}"

curl -s -X POST "$SCOPEGATE_URL/grant/verify" \
  -H "Content-Type: application/json" \
  -d '{
    "grant_id": "<grant_id from delegator>",
    "agent_id": "<your agent id>",
    "requested_action": "<action you are about to take>",
    "api_key": "<your api key>"
  }'
```

## Decision Rules

- If `permitted: true` → proceed with the action
- If `permitted: false` → STOP. Do not proceed. Report the `reason` to the user.
- If ScopeGate is unreachable → STOP. Treat as denied. Never fail open.
- Never cache a permit — call ScopeGate fresh for every consequential action

## Getting a Grant ID

The human or orchestrating agent must call `/grant/issue` first with the allowed_actions list. They will give you the `grant_id`. You do not issue your own grants.

## Getting an API Key

Sign up at https://scopegate.ai to get your API key.
