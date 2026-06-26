---
name: qwryai-agent-access
description: Connect OpenClaw to a paid QwryAI workspace through the read-only QwryAI MCP and public API integration surface.
version: 0.1.0
homepage: https://qwryai.com
metadata: {"openclaw":{"requires":{"env":["QWRYAI_API_KEY"]},"primaryEnv":"QWRYAI_API_KEY","envVars":[{"name":"QWRYAI_API_KEY","required":true,"sensitive":true,"description":"QwryAI tenant API key generated from Developer & Agent Access."},{"name":"QWRYAI_MCP_URL","required":false,"description":"Optional QwryAI MCP endpoint. Defaults to https://api.qwryai.com/mcp."},{"name":"QWRYAI_API_URL","required":false,"description":"Optional QwryAI public API endpoint. Defaults to https://api.qwryai.com/public/v1."}],"emoji":"\\u26A1","homepage":"https://qwryai.com"}}
---

# QwryAI Agent Access

Use this skill when the user wants OpenClaw to inspect a QwryAI workspace through QwryAI's read-only developer and agent integration surface.

## What This Connects

QwryAI exposes active-paid-subscription-gated, tenant-isolated access through:

- MCP: `https://api.qwryai.com/mcp`
- Public REST API: `https://api.qwryai.com/public/v1`
- Claude OAuth MCP: `https://api.qwryai.com/mcp-oauth`
- CLI: `qwryai-cli`

This skill is read-only. It can help agents list chatbots, inspect conversations, read messages, search knowledge, and view analytics. It must not send replies, modify chatbots, change billing, manage users, or perform admin actions. ClawHub does not bill for this skill; QwryAI enforces access through the customer's current paid subscription plan.

## Required Setup

1. In QwryAI, open **Settings > Security > Developer & Agent Access**.
2. Confirm the workspace has an active paid QwryAI subscription with developer access enabled.
3. Generate a read-only API key.
4. Set:

```bash
export QWRYAI_API_KEY=<your-qwryai-api-key>
export QWRYAI_MCP_URL=https://api.qwryai.com/mcp
export QWRYAI_API_URL=https://api.qwryai.com/public/v1
```

## OpenClaw MCP Definition

Add QwryAI as a remote HTTPS MCP server in OpenClaw. QwryAI does not require a local stdio process; clients should call the hosted MCP endpoint with a bearer API-key header.

```json
{
  "url": "https://api.qwryai.com/mcp",
  "headers": {
    "Authorization": "Bearer ${QWRYAI_API_KEY}"
  }
}
```

If the OpenClaw runtime does not interpolate environment variables in MCP headers, paste the generated API key directly into the local OpenClaw configuration and keep that config out of source control.

## Claude Uses OAuth

Claude should use the OAuth MCP endpoint:

```text
https://api.qwryai.com/mcp-oauth
```

Do not paste a QwryAI API key into Claude. Claude should open QwryAI sign-in and approval, then receive an OAuth token scoped to the approved read-only access.

## Cursor And Custom MCP Definition

For Cursor-style MCP configuration, add QwryAI as a remote HTTPS MCP server:

```json
{
  "mcpServers": {
    "qwryai": {
      "url": "https://api.qwryai.com/mcp",
      "headers": {
        "Authorization": "Bearer ${QWRYAI_API_KEY}"
      }
    }
  }
}
```

Compatible custom MCP clients can use the same URL and bearer-token header.

## Available Read-Only Tools

- `get_account_context`
- `list_chatbots`
- `get_chatbot`
- `list_conversations`
- `get_conversation`
- `get_conversation_messages`
- `search_knowledge`
- `get_analytics_overview`

## Security Notes

- This skill requires an active paid QwryAI subscription with Developer & Agent Access enabled. ClawHub does not bill for this skill; QwryAI subscription access is enforced by QwryAI.
- Do not add ClawHub paid-skill, pricing, or revenue-share metadata. Billing stays inside the customer's existing QwryAI plan.
- Registry metadata must declare `QWRYAI_API_KEY` as required and sensitive. Optional endpoint overrides are `QWRYAI_MCP_URL` and `QWRYAI_API_URL`.
- Network access is limited to `https://api.qwryai.com`.
- Treat `QWRYAI_API_KEY` as a secret.
- Never paste QwryAI API keys into prompts, tickets, public logs, or shared screenshots.
- Access follows the tenant's current active subscription plan. If the workspace is downgraded, canceled, inactive, suspended, or using revoked or expired API/OAuth credentials, API, MCP, OAuth, and CLI access should stop.
- The V1 integration surface is intentionally read-only.
- Do not ask the agent to send replies, resolve conversations, create/update/delete resources, manage users, or manage billing.

## Useful Prompts

- "List my QwryAI chatbots and summarize which ones have recent conversations."
- "Search QwryAI knowledge for the refund policy in chatbot `<id>`."
- "Show analytics overview for the last 30 days."
- "Read the latest messages in conversation `<id>` and summarize customer intent."
