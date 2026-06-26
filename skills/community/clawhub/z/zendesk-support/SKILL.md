---
name: zendesk-support
description: Manage Zendesk support tickets, users, organizations, macros, and helpdesk workflows via the Zendesk REST API. Use this skill when users want to search tickets, create support workflows, manage macros, or automate helpdesk operations.
---

# Zendesk

![Zendesk](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/zendesk.svg?v=2)

Access Zendesk via the REST API with managed OAuth authentication. Search users and tickets, review macros, and manage support workflows from chat.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=zendesk-support) for hosted connection flows and credentials so you do not need to configure Zendesk API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Zendesk |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Zendesk |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   Zendesk REST │
│   (User Chat)   │     │   (OAuth)    │     │      API         │
└─────────────────┘     └──────────────┘     └──────────────────┘
          │                       │                       │
          │  1. Install Plugin    │                       │
          │  2. Pair Device       │                       │
          │  3. Connect Zendesk  │                       │
          │                       │  4. Secure Token      │
          │                       │  5. Proxy Requests    │
          │                       │                       │
          ▼                       ▼                       ▼
    ┌──────────┐           ┌──────────┐           ┌──────────┐
    │  SKILL   │           │ Dashboard│           │ Zendesk  │
    │  File    │           │ Auth     │           │ Console  │
    └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Zendesk again."

## Quick Start

```bash
# List integrations
clawlink_list_integrations

# List Zendesk tools
clawlink_list_tools --integration zendesk

# Search for a specific tool
clawlink_search_tools --query "ticket" --integration zendesk
```

## Authentication

All Zendesk tool calls are authenticated automatically by ClawLink using the user's connected Zendesk account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Zendesk API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=zendesk and connect Zendesk.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `zendesk` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration zendesk
```

**Response:** Returns the live tool catalog for Zendesk.

### Reconnect

If Zendesk tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=zendesk
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration zendesk`

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Zendesk is connected.
2. Call `clawlink_list_tools --integration zendesk` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `zendesk`.
5. If no Zendesk tools appear, direct the user to https://claw-link.dev/dashboard?add=zendesk.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call │
│                                                             │
│  Example: List tickets → Search → Show results             │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  list → get → describe → preview → confirm → call           │
│                                                             │
│  Example: Describe tool → Preview changes → User approves   │
│           → Execute update                                  │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Tool Reference

### Tickets

| Tool | Description | Mode |
|------|-------------|------|
| `zendesk_list_tickets` | List tickets with filtering and pagination | Read |
| `zendesk_get_ticket` | Get a single ticket by ID | Read |
| `zendesk_create_zendesk_ticket` | Create a new support ticket | Write |
| `zendesk_update_ticket` | Update an existing ticket | Write |
| `zendesk_delete_ticket` | Permanently delete a ticket | Write |
| `zendesk_create_many_tickets` | Bulk create up to 100 tickets | Write |

### Users& Organizations

| Tool | Description | Mode |
|------|-------------|------|
| `zendesk_list_users` | List users with filtering | Read |
| `zendesk_get_user` | Get a user by ID | Read |
| `zendesk_create_zendesk_user` | Create a new user | Write |
| `zendesk_create_or_update_user` | Create or update a user | Write |
| `zendesk_list_zendesk_organizations` | List organizations | Read |
| `zendesk_create_zendesk_organization` | Create an organization | Write |

### Macros & Automations

| Tool | Description | Mode |
|------|-------------|------|
| `zendesk_apply_zendesk_macro` | Preview macro effects on a ticket | Read |
| `zendesk_list_macros` | List available macros | Read |
| `zendesk_create_automation` | Create a new automation rule | Write |
| `zendesk_create_trigger` | Create a new trigger | Write |

### Views & Search

| Tool | Description | Mode |
|------|-------------|------|
| `zendesk_list_views` | List saved views | Read |
| `zendesk_create_views_preview` | Preview view results | Read |
| `zendesk_search_tickets` | Search tickets by query | Read |
| `zendesk_autocomplete_users` | Autocomplete user search | Read |

### Attachments & Comments

| Tool | Description | Mode |
|------|-------------|------|
| `zendesk_create_zendesk_attachments` | Upload a file attachment | Write |
| `zendesk_list_comments` | List comments on a ticket | Read |
| `zendesk_create_comment` | Add a comment to a ticket | Write |

## Code Examples

### List recent tickets

```bash
clawlink_call_tool --tool "zendesk_list_tickets" \
  --params '{
    "status": "open",
    "max_per_page": 20
  }'
```

### Get a single ticket

```bash
clawlink_call_tool --tool "zendesk_get_ticket" \
  --params '{
    "ticket_id": 12345
  }'
```

### Create a ticket

```bash
clawlink_call_tool --tool "zendesk_create_zendesk_ticket" \
  --params '{
    "subject": "Support request",
    "comment": {"body": "Issue description"},
    "priority": "normal",
    "requester_id": 12345
  }'
```

### Preview a macro

```bash
clawlink_call_tool --tool "zendesk_apply_zendesk_macro" \
  --params '{
    "ticket_id": 12345,
    "macro_id": 67890
  }'
```

## Security & Permissions

- Access is scoped to the connected Zendesk account's data and permissions.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (deleting tickets, users, organizations) are marked as high-impact and must be confirmed.
- Bulk operations affect multiple records and require extra scrutiny before confirmation.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration zendesk`. |
| Missing connection | Zendesk is not connected. Direct the user to https://claw-link.dev/dashboard?add=zendesk. |
| `RecordNotFound` | Ticket, user, or organization does not exist. Check the ID. |
| `CreateConflict` | Resource already exists. Use update instead of create. |
| `InvalidArgument` | Invalid parameter or missing required field. Review the tool schema. |
| `Write rejected` | User did not confirm a write action. Always confirm before executing writes. |

### Troubleshooting: Tools Not Visible

1. Check that the ClawLink plugin is installed:
   ```bash
   openclaw plugins list
   ```
2. If the plugin is installed but tools are missing, tell the user to send `/new` as a standalone message to reload the catalog.
3. If a fresh chat does not help, run:
   ```bash
   openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
   openclaw gateway restart
   ```
4. After restart, tell the user to send `/new` again and retry.

### Troubleshooting: Invalid Tool Call

1. Ensure the integration slug is exactly `zendesk`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Zendesk REST API Docs](https://developer.zendesk.com/api-reference/)
- [Zendesk API Reference](https://developer.zendesk.com/api-reference/ticketing/introduction/)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=zendesk-support
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=zendesk-support)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
