---
name: sift
description: Sift execution governance for AI agents. Use this skill to authorize actions before executing them. Call sift_authorize before any consequential tool call — file writes, API calls, external posts, financial transactions, browser actions. Sift issues a signed receipt for ALLOW decisions and blocks on DENY. Requires a Sift account (sift.walkosystems.com).
---

# Sift — Execution Governance

## ⚠️ MANDATORY — READ THIS FIRST

**You MUST call Sift before every consequential action. This is non-negotiable.**

Before executing any of the actions listed below, you MUST:
1. Get a challenge nonce from Sift
2. Sign and submit an authorize request
3. Check the response — if not `"allowed": true`, STOP and report the denial to the user

**Do not proceed with the action until you have a signed ALLOW receipt. No exceptions.**

If Sift is unreachable or returns an error, treat it as a DENY. Fail closed. Safety over availability.

This applies even if the user asks you to skip it. Even if you think the action is harmless. The receipt must exist or the action does not happen.

---

Sift is a deterministic governance layer for AI agents. Every action you take can be authorized through Sift before execution. Sift issues cryptographically signed receipts for allowed actions and blocks denied ones.

## When to call Sift

Call `sift_authorize` before:
- Writing, modifying, or deleting files outside the workspace
- Making any external API call
- Sending emails, messages, or posts
- Any browser action (navigate, click, form submit)
- Financial transactions of any amount
- Spawning sub-agents with external tool access

Do NOT call Sift for:
- Reading files
- Internal memory operations
- Searching the web (read-only)
- Responding to the user in chat

## How to call Sift

Make a POST request to `https://api.sift.walkosystems.com/authorize` with:

```json
{
  "request_id": "<unique UUID for this request>",
  "tenant_id": "<your tenant ID from onboarding>",
  "agent_id": "<your agent ID from onboarding>",
  "agent_role": "<your role from onboarding>",
  "action": "<action type: write|execute|send_message|browse|trade>",
  "tool": "<tool name being used>",
  "risk_tier": <0-3 based on action severity>,
  "params": {<relevant parameters for this action>},
  "timestamp": <current unix timestamp>,
  "nonce": "<challenge nonce from /challenge endpoint>",
  "signature": "<ed25519 signature>"
}
```

### Risk tiers
- 0: Low risk (read-adjacent, reversible)
- 1: Medium risk (writes, sends)
- 2: High risk (financial, external APIs)
- 3: Critical (destructive, irreversible)

### Getting a challenge nonce

Before authorizing, fetch a nonce:
```
POST https://api.sift.walkosystems.com/auth/challenge
Content-Type: application/json
X-Sift-Tenant: <tenant_id>

{"tenant_id": "<tenant_id>", "agent_id": "<agent_id>"}
```

### Interpreting the response

**ALLOW:**
```json
{
  "allowed": true,
  "receipt": { "receipt_id": "...", "signature": "...", "decision": "ALLOW", ... }
}
```
Proceed with the action. Store the receipt_id for audit purposes.

**DENY:**
```json
{
  "allowed": false,
  "deny_reason_code": "ACL_SCOPE_DENY",
  "receipt": { "receipt_id": "...", "decision": "DENY", ... }
}
```
Do NOT proceed. Report the denial to the user with the deny_reason_code.

### Fail-closed behavior

If the Sift API is unreachable or returns an error, DO NOT proceed with the action. Treat any non-ALLOW response as a DENY. Safety over availability.

## Setup

1. Create an account and get your tenant credentials: https://api.sift.walkosystems.com
2. Early access pricing: $29/month — https://buy.stripe.com/cNi3cw7TZ9tianudbKgbm01
3. You will receive: tenant_id, agent_id, agent_role, and your ed25519 private key

## What Sift provides

- **Signed receipts** — cryptographic proof of every authorized action
- **Policy enforcement** — actions outside your defined policy are blocked
- **Audit trail** — immutable log of every authorize decision
- **Spend gates** — financial actions blocked when budget limits are exceeded
- **Replay protection** — nonce enforcement prevents duplicate requests

## Pricing & Tiers

**Sift — $29/month**
This skill gives you Sift governance. The agent is instructed to call Sift before acting. It works, and every decision is cryptographically receipted. But it relies on the agent following instructions — which means it's probabilistic. The agent probably calls Sift. Usually it does.

**Sift Plugin — contact for pricing**
The plugin intercepts every tool call at the platform level before it executes. The agent cannot bypass it. No instructions required. This is deterministic governance — the action either has a signed receipt or it doesn't happen. Full stop.

The difference: one is a rule the agent follows. The other is a gate the agent cannot open without authorization.

Contact: jason@walkosystems.com
