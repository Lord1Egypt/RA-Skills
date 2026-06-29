---
name: zoho-desk
description: Zoho Desk API integration with managed OAuth. Manage support tickets, track conversations, list departments and agents, handle contacts and organizations. Use this skill when users want to create support tickets, view ticket conversations, manage customer support workflows, or check agent and department details.
---

# Zoho Desk

![Zoho Desk](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/zoho-desk.svg)

Customer support from chat -- create tickets, view conversations, manage contacts, departments, and agents.

Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=zoho-desk), an integration hub for OpenClaw that handles hosted OAuth flows and credentials so you don't need to configure Zoho Desk API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Zoho Desk |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Zoho Desk |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Zoho Desk API    │
│   (User Chat)   │     │   (OAuth)    │     │                  │
└─────────────────┘     └──────────────┘     └──────────────────┘
```

## Install

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

## Quick Start

1. **List organizations**: `zoho_desk_list_organizations` -- discover your org and portal URLs.
2. **List tickets**: `zoho_desk_list_tickets` -- view open support tickets.
3. **Create a ticket**: `zoho_desk_create_ticket` -- open a new support request.

## Authentication

Zoho Desk uses managed OAuth via ClawLink. No API keys needed. Connect at [claw-link.dev/dashboard?add=zoho-desk](https://claw-link.dev/dashboard?add=zoho-desk).

## Connection Management

**List connections**: `clawlink_list_integrations` -- confirm Zoho Desk is connected.

**Verify**: Call `zoho_desk_list_organizations` to test access.

**Reconnect**: If you see auth errors, reconnect at [claw-link.dev/dashboard?add=zoho-desk](https://claw-link.dev/dashboard?add=zoho-desk).

## Security & Permissions

Read operations (list tickets, get conversations) run safely. Write operations (create ticket, update tasks) require confirmation.

## Tool Reference

### Ticket Operations

| Tool | Description | Mode |
|------|-------------|------|
| `zoho_desk_list_tickets` | List tickets with optional filters | Read |
| `zoho_desk_get_ticket` | Get details of a specific ticket | Read |
| `zoho_desk_create_ticket` | Create a new support ticket | Write |
| `zoho_desk_get_ticket_resolution` | Get the resolution for a ticket | Read |
| `zoho_desk_list_ticket_conversations` | List all conversations for a ticket | Read |
| `zoho_desk_get_ticket_latest_thread` | Get the most recent thread on a ticket | Read |
| `zoho_desk_get_ticket_thread` | Get a specific thread within a ticket | Read |

### Contact Operations

| Tool | Description | Mode |
|------|-------------|------|
| `zoho_desk_list_contacts` | List contacts with filters and pagination | Read |
| `zoho_desk_get_contact` | Get details of a specific contact | Read |
| `zoho_desk_get_contacts_by_ids` | Fetch multiple contacts by IDs | Read |
| `zoho_desk_list_contact_accounts` | List accounts associated with a contact | Read |

### Agent Operations

| Tool | Description | Mode |
|------|-------------|------|
| `zoho_desk_get_agent` | Get details of a specific agent | Read |
| `zoho_desk_get_agents_count` | Get total agent count with optional filters | Read |

### Department Operations

| Tool | Description | Mode |
|------|-------------|------|
| `zoho_desk_list_departments` | List all departments | Read |
| `zoho_desk_get_department` | Get details of a specific department | Read |
| `zoho_desk_get_departments_count` | Get total department count | Read |
| `zoho_desk_get_department_logo` | Download a department's logo | Read |
| `zoho_desk_upload_department_logo` | Upload/update a department logo | Write |
| `zoho_desk_list_teams_in_department` | List teams within a department | Read |

### Organization Operations

| Tool | Description | Mode |
|------|-------------|------|
| `zoho_desk_list_organizations` | List organizations the user belongs to | Read |

### Role Operations

| Tool | Description | Mode |
|------|-------------|------|
| `zoho_desk_list_roles` | List all roles | Read |
| `zoho_desk_list_roles_by_ids` | List roles by specific IDs | Read |

### Task Operations

| Tool | Description | Mode |
|------|-------------|------|
| `zoho_desk_update_many_tasks` | Update multiple tasks in a single call | Write |

## Code Examples

**List open tickets**

```json
{ "tool": "zoho_desk_list_tickets" }
```

**Create a support ticket**

```json
{
  "tool": "zoho_desk_create_ticket",
  "args": {
    "subject": "Cannot access account",
    "description": "User unable to log in since Monday",
    "departmentId": "123456789",
    "contactId": "987654321"
  }
}
```

**Get the latest conversation on a ticket**

```json
{
  "tool": "zoho_desk_get_ticket_latest_thread",
  "args": { "ticketId": "abc123" }
}
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm `zoho-desk` is connected.
2. Call `clawlink_list_tools --integration zoho-desk` to see the live catalog.
3. Call `zoho_desk_list_organizations` to get org details.
4. Use department and contact IDs for ticket creation.

## Execution Workflow

```
Read Flow:  User asks for tickets → clawlink resolves connection → Zoho Desk API → results displayed
Write Flow: User wants to create ticket → confirmation prompt → clawlink resolves connection → Zoho Desk API → ticket created
```

## Notes

- Creating a ticket requires a `departmentId`. Use `zoho_desk_list_departments` to discover IDs.
- Ticket creation returns `id` and `webUrl` for downstream chaining.
- Use `zoho_desk_get_contacts_by_ids` to batch-fetch multiple contacts efficiently.

## Related Skills

- **Zoho CRM** (`zoho`) -- Full Zoho CRM suite
- **Zoho Bigin** (`zoho-bigin`) -- Small business CRM
- **Zoho Inventory** (`zoho-inventory`) -- Stock and order management
- **Zoho Invoice** (`zoho-invoice`) -- Invoicing and billing
- **Zoho Mail** (`zoho-mail`) -- Business email

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| 401 Unauthorized | Token expired; reconnect at the dashboard |
| 404 Not Found | Invalid ticket, contact, or department ID |
| 400 Bad Request | Missing required fields for ticket creation |

## Troubleshooting

### Tools Not Visible
Run `openclaw gateway restart` after installing the plugin. Start a fresh chat session.

### Cannot Create Ticket
Ensure you have the correct `departmentId` from `zoho_desk_list_departments`.

## Resources

- Zoho Desk API Docs: https://www.zoho.com/desk/developer-help/api/
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=zoho-desk
- ClawLink Docs: https://docs.claw-link.dev/openclaw

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=zoho-desk)** -- an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
