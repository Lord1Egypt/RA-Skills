---
name: scopeblind-passport
description: >
  Signed access control for your OpenClaw agent. Wraps MCP tool calls through
  protect-mcp to add per-tool policies, signed receipts, and trust tiers.
  Every action your agent takes produces a cryptographic receipt — independently
  verifiable by anyone, without trusting ScopeBlind.
metadata:
  emoji: 🛡️
  requires:
    bins:
      - npx
      - curl
    env: []
  install: |
    npm install -g protect-mcp@latest @scopeblind/passport@latest
  license: MIT-0
  allowed-tools:
    - Bash
    - Read
    - Write
---

# ScopeBlind Passport — Signed Access Control for Your Agent

## What This Skill Does

This skill wraps your OpenClaw agent's MCP tool calls through `protect-mcp`, adding:

- **Shadow mode** — logs every tool call with a signed receipt (blocks nothing by default)
- **Per-tool policies** — block, rate-limit, or require approval for specific tools
- **Signed receipts** — Ed25519-signed, JCS-canonicalized proof of every decision
- **Trust tiers** — available for advanced configurations to gate tool access by verified track record
- **Local daily digest** — human-readable summary of what your agent did

> Any platform can log what its agents do. Very few will let you verify those logs without trusting them.

## When to Use This Skill

Use this skill when:

- You want to know what your agent did while you weren't watching
- You need signed, tamper-proof proof of agent actions for compliance or auditing
- You want to block dangerous tools (delete_database, send_email_as_ceo, rm_rf)
- You want rate limits on expensive or risky operations
- You want a daily summary of your agent's activity

## Do NOT Use This Skill When

- You only want basic OpenClaw built-in allowlists (those work fine for simple cases)
- You don't need signed cryptographic proof (just want logs, not receipts)

## Setup

### Fast path (recommended)

If you already have an OpenClaw config, generate a passported wrapper pack first:

```bash
npx @scopeblind/passport wrap --runtime openclaw --config ./openclaw.json --policy email-safe
```

That writes:

- `wrapped-config.json`
- `manifest.json`
- `passport.bundle.json`
- `protect-mcp.json`
- `keys/gateway.json`
- `VERIFY.md`

Copy the `mcpServers` entries from `wrapped-config.json` into your OpenClaw config.

### First Run (generates signing keys + default policy)

```bash
npx protect-mcp init
```

This creates:
- `keys/gateway.json` — Ed25519 signing keypair (in current directory)
- `protect-mcp.json` — default shadow-mode policy (logs everything, blocks nothing)

### Wrapping Your MCP Servers

For each MCP server your agent uses, wrap it through protect-mcp. In your OpenClaw MCP config:

**Before:**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "node",
      "args": ["filesystem-server.js"]
    }
  }
}
```

**After:**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["protect-mcp", "--policy", "protect-mcp.json", "--", "node", "filesystem-server.js"]
    }
  }
}
```

That's it. Every tool call now produces a signed receipt.

### Applying a Policy Pack

To move from shadow mode to enforce mode, copy a policy template and add `--enforce`:

```bash
# Copy a policy template
cp policies/email-safe.json protect-mcp.json
```

Then update your MCP config args to include `--enforce`:
```json
"args": ["protect-mcp", "--policy", "protect-mcp.json", "--enforce", "--", "node", "server.js"]
```

See the `policies/` directory for pre-built templates.

## Commands

When the user asks you to perform these actions, execute them:

### "Show my passport" / "What's my agent identity?"

```bash
npx protect-mcp status
```

Display the output, which shows:
- Total decisions (allow/deny/rate-limited)
- Time range of activity
- Top tools used
- Trust tiers seen

### "What did you do today?" / "Show my daily report"

```bash
npx protect-mcp digest --today
```

Display the local summary, which includes:
- Actions taken (allowed, blocked, awaiting approval)
- Tools used and frequency
- Trust tier status
- Blocked tools with reasons

### "Show my receipts" / "Prove what you did"

```bash
npx protect-mcp receipts --last 20
```

Shows the 20 most recent decisions with tool name, decision, and timestamp.

### "Why was that blocked?"

When a tool call is blocked or rate-limited, explain:
- Which policy rule triggered the block
- The agent's current trust tier
- What tier would be needed to use that tool
- How to request an approval or policy change

## Approval Flow

When protect-mcp blocks a high-risk action that has `require_approval: true` in the policy, it returns:

```
REQUIRES_APPROVAL: The tool "send_email" requires human approval before execution.
Tell the user you need their approval to use "send_email" and will retry when granted.
Do NOT retry this tool call until the user explicitly approves it.
```

**When you receive this response:**

1. Tell the user: "I need your approval to use [tool_name]. Should I proceed?"
2. Wait for the user to respond with approval.
3. When the user approves, grant the approval by running:

```bash
# For one-time approval (scoped to this specific request):
curl -s -X POST http://127.0.0.1:9876/approve -H 'Content-Type: application/json' -d '{"request_id":"REQUEST_ID","tool":"TOOL_NAME","mode":"once","nonce":"NONCE"}'

# For always-allow this tool (session-scoped, 24h TTL):
curl -s -X POST http://127.0.0.1:9876/approve -H 'Content-Type: application/json' -d '{"tool":"TOOL_NAME","mode":"always","nonce":"NONCE"}'
```

Replace `REQUEST_ID`, `TOOL_NAME`, and `NONCE` with the values from the REQUIRES_APPROVAL response.

4. After granting approval, retry the original tool call. It will now succeed.

**When the user denies:** Tell them the action was blocked and explain what was prevented.

### Check current approvals:

```bash
curl -s http://127.0.0.1:9876/approvals
```

## Policy Packs

Pre-built policies are available in the `policies/` directory:

| Pack | What it does |
|------|-------------|
| `shadow.json` | Log everything, block nothing (default) |
| `web-browsing-safe.json` | Rate-limit browsing, require approval for forms, block JS |
| `email-safe.json` | Read freely, require approval to send, block delete |
| `strict.json` | Block everything except reads (read-only mode) |

## Verification

Every receipt is independently verifiable. The MIT-licensed verifier requires zero trust in ScopeBlind.

### Quick test (no receipts needed)

```bash
npx @veritasacta/verify --self-test
```

### Getting receipts to verify

Receipts are available from the local HTTP status server while protect-mcp is running:

```bash
# Get the most recent receipt
curl -s http://127.0.0.1:9876/receipts/latest | jq -r '.receipt' > receipt.json

# Get all recent receipts
curl -s http://127.0.0.1:9876/receipts | jq -r '.receipts[0].receipt' > receipt.json
```

If the local status server is unavailable, use the persisted receipt file:

```bash
tail -n 1 .protect-mcp-receipts.jsonl > receipt.json
```

### Verifying a receipt

```bash
# Get the public key from status (shown under "Passport Identity")
npx protect-mcp status

# Verify with the public key
npx @veritasacta/verify receipt.json --key <public-key-hex>
```

The verifier checks Ed25519 signatures against public keys. No API calls, no accounts, no ScopeBlind servers involved.

## Links

- [protect-mcp on npm](https://www.npmjs.com/package/protect-mcp)
- [@veritasacta/verify on npm](https://www.npmjs.com/package/@veritasacta/verify)
- [Documentation](https://www.scopeblind.com/docs)
- [GitHub](https://github.com/scopeblind/protect-mcp)
