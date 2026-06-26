# QwryAI Agent Access

Connect OpenClaw to a paid QwryAI workspace through QwryAI's read-only MCP and public API integration layer.

## What It Does

- Lists QwryAI chatbots.
- Reads conversation and message history.
- Searches chatbot knowledge.
- Shows tenant analytics overview.
- Reports account, plan, scope, and read-only capability context.

It cannot send replies, resolve conversations, edit chatbots, manage users, change billing, or perform admin actions.

## Setup

1. In QwryAI, open **Settings > Security > Developer & Agent Access**.
2. Confirm the workspace has an active paid QwryAI subscription.
3. Generate a read-only API key.
4. Configure OpenClaw with:

```bash
export QWRYAI_API_KEY=<your-qwryai-api-key>
export QWRYAI_MCP_URL=https://api.qwryai.com/mcp
export QWRYAI_API_URL=https://api.qwryai.com/public/v1
```

`QWRYAI_API_KEY` is required and sensitive. `QWRYAI_MCP_URL` and `QWRYAI_API_URL` are optional endpoint overrides; the defaults use QwryAI's hosted production API.

## MCP Configuration

QwryAI uses a hosted remote HTTPS MCP endpoint. It is not a local stdio MCP server, so OpenClaw, Cursor, and custom clients should connect to `https://api.qwryai.com/mcp` with an Authorization header.

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

## Claude

Claude should use OAuth instead of an API key:

```text
https://api.qwryai.com/mcp-oauth
```

Do not paste a QwryAI API key into Claude. Claude should open QwryAI sign-in and approval, then receive a scoped OAuth token.

## Security

QwryAI enforces access with the tenant's current active subscription plan. Downgrades, inactive subscriptions, suspended tenants, revoked API keys, expired API keys, revoked OAuth tokens, and expired OAuth tokens stop API, MCP, OAuth, and CLI access at validation time.

ClawHub does not bill for this skill. Customers use their existing paid QwryAI plan, and QwryAI validates access on every API, MCP, OAuth, and CLI request.

## Review Notes

- Required credential metadata is declared in the manifest: `QWRYAI_API_KEY`.
- Network access is limited to `https://api.qwryai.com`.
- V1 is read-only and must not call write, billing, user-management, or admin actions.
- The skill stores no secrets. Users provide credentials through their local OpenClaw environment or secret manager.
