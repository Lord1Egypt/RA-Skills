---
name: trustloop
description: AI governance layer — logs, audits, and enforces kill-switch rules on agent tool calls. Built by trustloop.live.
license: MIT-0
metadata:
  openclaw:
    requires:
      env:
        - TRUSTLOOP_API_KEY
    primaryEnv: TRUSTLOOP_API_KEY
    homepage: https://trustloop.live
    tags:
      - governance
      - audit
      - compliance
      - security
      - mcp
---

# TrustLoop — AI Governance for Your Agent

**Operator:** trustloop.live (Soji Muyiwa, UK) — same owner as the Railway host.
**Privacy:** Only tool name and arguments are sent. TrustLoop automatically masks PII (emails, phone numbers) and redacts secrets (API keys, tokens) before storing. No file contents or conversation history are transmitted.
**Open dashboard:** app.trustloop.live shows everything logged — full transparency.

## Before Sensitive Tool Calls

Before calling any tool that is destructive, external, financial, or bulk in nature, check with TrustLoop:

```bash
curl -s -X POST https://api.trustloop.live/api/intercept \
  -H "Content-Type: application/json" \
  -H "x-api-key: $TRUSTLOOP_API_KEY" \
  -d '{"tool_name": "<tool>", "arguments": <args_json>}'
```

**Important — before sending arguments:** Strip or mask any raw passwords, tokens, or private keys from the arguments object. Send only the fields needed to describe the action (e.g. recipient, subject, file path — not credentials).

If response is `{"allowed": false}` — stop and inform the user. Do not execute.
If response is `{"allowed": true}` — proceed.

## Which Tools Require a Check

- Deleting, moving, or overwriting files
- Sending emails, messages, or notifications
- Any financial transaction or payment
- Posting to social media or external services
- Bulk operations (more than 5 records)
- Running shell commands that modify the system

## Setup

1. Sign up free at app.trustloop.live
2. Copy your API key from the dashboard
3. `export TRUSTLOOP_API_KEY=tl_your_key_here`

Data retention, privacy policy, and security docs: trustloop.live
Full API reference (rules, kill-switches, approvals): see `api-reference.md`
