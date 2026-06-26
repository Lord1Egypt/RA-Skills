---
name: x402geo-skill
description: Use when an agent needs to run GEO/SEO audits through x402geo.com with payment gating, status tracking, and report delivery via MCP or ACP.
---

# x402geo MCP + ACP Skill

## Purpose

Use this skill to run a full user-facing GEO/SEO audit flow on https://x402geo.com:

1. Collect user email + target URL.
2. Create a payment-required audit request.
3. Return payment link and audit redirect/progress URL to the user.
4. Track job progress until completion.
5. Deliver report summary and public report link.

## Integration Modes

Use one of these modes:

- MCP: `POST https://x402geo.com/api/mcp` (JSON-RPC 2.0 tools)
- ACP: `https://x402geo.com/api/acp/*` REST endpoints

If your agent supports tool-calling well, prefer MCP.
If your agent is workflow/REST oriented, prefer ACP.

## Required User Inputs

Collect these first:

- `email`: user email for payment and audit association
- `url`: full website URL to audit (for example `https://example.com`)

## ACP Flow (Recommended for explicit payment lifecycle)

### Step 1: Create payment request

Request:

```http
POST https://x402geo.com/api/acp/jobs
Content-Type: application/json

{
  "email": "user@example.com",
  "requirements": {
    "url": "https://example.com",
    "report_depth": "standard"
  }
}
```

Expected response fields:

- `status` = `payment_required`
- `checkout_url` (payment link)
- `email`
- `target_url`

Agent action:

- **If agentic wallet is funded**: notify the user that a funded agentic wallet is detected and ask for confirmation before paying (e.g. "I found a funded agentic wallet. Would you like me to pay automatically using it?"). Only proceed with `mcp__agentcash__fetch` (see **Payment: Agentic Wallet** section) after the user confirms. Do not show the checkout URL if the user confirms.
- **If wallet unavailable or unfunded**: return `checkout_url` to user, tell them to complete payment, and explain this starts the audit flow.

### Step 2: Start paid audit

After payment (or directly in local/dev setups where paywall is disabled), call:

```http
GET https://x402geo.com/api/acp/jobs/start?url=https%3A%2F%2Fexample.com&email=user%40example.com
```

Expected response fields:

- `job_id`
- `progress_url`
- `results_url`
- `report_url`
- `status`

Agent action:

- Return `progress_url` as the audit status URL.
- Keep `job_id` for tracking.
- Return `report_url` as the final public report link placeholder.

### Step 3: Track progress

Poll either endpoint until complete:

- `GET /api/acp/jobs/{jobId}`
- `GET /api/acp/resources/audit-status?jobId={jobId}`

State mapping:

- `pending` / `in_progress`: keep polling
- `completed`: proceed to deliverable fetch
- `failed`: stop and report error_reason to user

### Step 4: Read and return report

Fetch deliverable:

```http
GET https://x402geo.com/api/acp/jobs/{jobId}/deliverable
```

Notes:

- Returns `409` while audit is not complete.
- Returns `deliverable` object when complete.

Agent action:

- Summarize key findings and recommendations for user.
- Provide `report_url` from status/start response as the public report link.

## MCP Flow (Tool-calling agents)

Endpoint:

- `POST https://x402geo.com/api/mcp`

Protocol methods:

- `initialize`
- `tools/list`
- `tools/call`

Primary tools:

- `create_geo_audit` with `url` and optional `email`
- `get_audit_status` with `jobId`
- `get_report_links` with `jobId`

MCP workflow:

1. Check agentic wallet via `mcp__agentcash__get_balance`. If funded, notify the user and ask for confirmation (e.g. "I found a funded agentic wallet. Would you like me to pay automatically using it?"). Only use `mcp__agentcash__fetch` to call `create_geo_audit` (see **Payment: Agentic Wallet** section below) after the user confirms.
2. If wallet unavailable, unfunded, or user declines, call `create_geo_audit` normally. If `status=payment_required`, return `paymentUrl` to user and ask them to complete payment.
3. After payment (automatic or manual), get `jobId` from the response and call `get_audit_status`.
4. When `done`, call `get_report_links` and return `reportPage`.

## Payment: Agentic Wallet (Preferred, Confirm First)

Before falling back to a manual checkout link, check if the AgentCash MCP wallet is available and funded. If it is, notify the user and ask for their confirmation before proceeding.

### Check wallet readiness

Call the AgentCash MCP tool:

```
mcp__agentcash__get_balance
```

- If USDC balance is sufficient to cover the audit cost (typically $1–5 USDC), ask the user: "I found a funded agentic wallet. Would you like me to pay automatically using it?"
- Only proceed after the user confirms.
- If balance is zero or insufficient, fall back to the manual payment flow and provide the `checkout_url`.

### Automatic payment via AgentCash MCP

Use `mcp__agentcash__fetch` to call the x402-gated audit endpoint. The wallet handles the USDC payment on Base automatically.

**ACP payment example:**

```
mcp__agentcash__fetch(
  url: "https://x402geo.com/api/acp/jobs",
  method: "POST",
  body: { "email": "user@example.com", "requirements": { "url": "https://example.com", "report_depth": "standard" } }
)
```

**MCP payment example:**

```
mcp__agentcash__fetch(
  url: "https://x402geo.com/api/mcp",
  method: "POST",
  body: { "jsonrpc": "2.0", "method": "tools/call", "params": { "name": "create_geo_audit", "arguments": { "url": "https://example.com", "email": "user@example.com" } }, "id": 1 }
)
```

On success, parse the response and continue to Step 2 (start audit). Let the user know the payment was completed.

If `mcp__agentcash__fetch` returns insufficient balance or authentication errors:

- Call `mcp__agentcash__list_accounts` to surface a deposit link to the user.
- Fall back to returning the manual `checkout_url`.

### Wallet setup errors — what to tell the user

Only surface wallet issues to the user when automatic payment is impossible:

- "Insufficient balance" → "Your agentic wallet needs more USDC. I can send you a deposit link, or provide a direct payment link instead."
- "Not authenticated" → "The agentic wallet isn't set up. I can send you the payment link to complete it manually."

Always inform the user of payment outcomes — whether paid via agentic wallet or manual checkout.

## Agent Output Contract

At minimum, send user:

- Payment step: if agentic wallet is available, ask for confirmation before paying; otherwise provide `checkout_url` or `paymentUrl` for manual payment
- Tracking step: `progress_url` or status page URL
- Completion step: concise summary + public `report_url`/`reportPage`

If processing fails, send:

- current status
- provider error message
- exact next action user should take
