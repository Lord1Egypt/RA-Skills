---
name: telegram-instant-messenger
description: "Telegram Instant Messenger: Two-way Telegram messaging through the shared @AgentPMT_bot with budget-scoped chat binding. Use when an agent needs telegram instant messenger, instant two way telegram chat with zero setup, send alerts and notifications to users or teams, customer support and helpdesk automation, collect feedback and survey responses via chat, get updates, offset, limit through AgentPMT-hosted remote tool calls. Discovery terms: telegram instant messenger."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/telegram-instant-messenger
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/telegram-instant-messenger"}}
---
# Telegram Instant Messenger

## Freshness
Last updated: `2026-06-09`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Two-way Telegram messaging through the shared @AgentPMT_bot with budget-scoped chat binding. If not connected, the tool returns `status: connection_required` with `chat_url`, `otp_code`, and `start_command` (for example `/start 123456`). Open `chat_url`, send `start_command` exactly, then send any follow-up message to bind. After binding, send/receive text, photos, and documents with unread cursor controls and File Manager ingestion.

## Product Instructions
### Telegram Instant Messenger

Two-way messaging through the shared AgentPMT Telegram bot.

#### User Setup

The shared tool binds each budget to one Telegram user/chat via a short 6-digit OTP.

1. Call any action (`send_message`, `send_photo`, `send_document`, or `get_updates`)
2. The tool checks whether the budget is already bound
3. If not bound, it returns `status: connection_required` with `chat_url`, `otp_code`, and `start_command`
4. User opens `chat_url` and sends `start_command` exactly (example: `/start 123456`)
5. User sends any follow-up message in the same chat
6. On every request while unbound, the tool checks Telegram updates for a matching `/start <otp_code>` and binds immediately when found

#### Shared Bot Scope

For the shared AgentPMT bot, each budget is scoped to one Telegram chat.

- `chat_id` is not accepted in shared-tool requests
- Outbound actions automatically use the stored scoped chat from the budget binding
- `get_updates` automatically filters to the bound chat/user once connected

#### Actions

##### `send_message`
Required: `text`

##### `send_photo`
Provide one of:
- `photo` (URL, Telegram file_id, or base64)
- `photo_file_id` (AgentPMT File Manager file_id)

##### `send_document`
Provide one of:
- `document` (URL, Telegram file_id, or base64)
- `document_file_id` (AgentPMT File Manager file_id)

If using base64 `document`, `filename` is required.

##### `get_updates`
Optional:
- `offset`, `limit` (1-100), `timeout` (0-60), `allowed_updates`
- `unread_only`, `cursor_offset`, `mark_as_read`
- `ingest_files_to_manager`, `ingest_max_files`, `ingest_expiration_days`

When not yet connected, this action returns `status: connection_required` with `chat_url`, `otp_code`, and `start_command`.

#### File Manager Flows

- Send from File Manager: use `photo_file_id` or `document_file_id`
- Save inbound Telegram media: set `ingest_files_to_manager: true` on `get_updates`
- Ingested uploads are returned in `ingested_files` with new File Manager `file_id` values

#### Shared Optional Params (send actions)

`parse_mode`, `caption`, `reply_markup`, `disable_notification`, `protect_content`, `message_thread_id`

## When To Use
- Use this skill for `Telegram Instant Messenger` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: telegram instant messenger, instant two way telegram chat with zero setup, send alerts and notifications to users or teams, customer support and helpdesk automation, collect feedback and survey responses via chat, get updates, offset, limit.
- Supported action names: `get_updates`, `send_document`, `send_message`, `send_photo`.

## Use Cases
- Instant two-way Telegram chat with zero setup
- Send alerts and notifications to users or teams
- Customer support and helpdesk automation
- Collect feedback and survey responses via chat
- Share reports and documents through Telegram
- Build conversational AI workflows on Telegram
- Send photos and media to users
- Prototype Telegram automations quickly

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `4`.
x402 availability: not enabled for this product.

- `get_updates` (action slug: `get-updates`): Fetch incoming updates with persisted cursor and optional media ingestion into File Manager. Returns deep link binding instructions when budget is not yet connected. Price: `2` credits. Parameters: `allowed_updates`, `cursor_offset`, `ingest_expiration_days`, `ingest_files_to_manager`, `ingest_max_files`, `limit`, `mark_as_read`, `offset`, plus 2 more.
- `send_document` (action slug: `send-document`): Send a document to the budget's bound Telegram chat via URL/file_id/base64 or File Manager file_id. Price: `2` credits. Parameters: `caption`, `disable_notification`, `document`, `document_file_id`, `filename`, `message_thread_id`, `parse_mode`, `protect_content`.
- `send_message` (action slug: `send-message`): Send a text message to the budget's bound Telegram chat (shared AgentPMT bot). Price: `2` credits. Parameters: `disable_notification`, `message_thread_id`, `parse_mode`, `protect_content`, `reply_markup`, `text`.
- `send_photo` (action slug: `send-photo`): Send a photo to the budget's bound Telegram chat via URL/file_id/base64 or File Manager file_id. Price: `2` credits. Parameters: `caption`, `disable_notification`, `message_thread_id`, `parse_mode`, `photo`, `photo_file_id`, `protect_content`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "telegram-instant-messenger"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "telegram-instant-messenger"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "telegram-instant-messenger"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "telegram-instant-messenger"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "telegram-instant-messenger"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "telegram-instant-messenger"
  }
}
```

## Call This Tool
Product slug: `telegram-instant-messenger`

Marketplace page: https://www.agentpmt.com/marketplace/telegram-instant-messenger

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Telegram-Instant-Messenger",
    "arguments": {
      "action": "get_updates",
      "allowed_updates": [
        "example allowed update"
      ],
      "cursor_offset": 1,
      "ingest_expiration_days": 7,
      "ingest_files_to_manager": true,
      "ingest_max_files": 10,
      "limit": 100,
      "mark_as_read": true,
      "offset": 1
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "telegram-instant-messenger",
  "parameters": {
    "action": "get_updates",
    "allowed_updates": [
      "example allowed update"
    ],
    "cursor_offset": 1,
    "ingest_expiration_days": 7,
    "ingest_files_to_manager": true,
    "ingest_max_files": 10,
    "limit": 100,
    "mark_as_read": true,
    "offset": 1
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `get_updates` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/telegram-instant-messenger
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
