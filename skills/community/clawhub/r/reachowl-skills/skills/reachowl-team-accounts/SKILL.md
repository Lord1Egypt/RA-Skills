---
name: reachowl-team-accounts
description: "See which Facebook, Instagram, and WhatsApp accounts and browsers are connected to ReachOwl, pick the account to run campaigns from, and manage team members (invite, change role, remove). Use when the user asks which accounts they can use, why an account isn't available, or wants to add a teammate to ReachOwl."
license: MIT
compatibility: Requires the ReachOwl MCP server (https://reachowl.com/mcp).
metadata:
  author: ReachOwl
  version: "1.1.0"
  homepage: https://reachowl.com
  tags: reachowl, connected-accounts, team-management
---

# ReachOwl Team & Connected Accounts

## Before you start

- Requires the ReachOwl MCP server connected with the user's token. If a tool reports a missing token, run the `reachowl-auth` flow.

## MCP tools

### Connected accounts (read-only)

| Tool | Purpose |
|------|---------|
| `list_app_states` | Connected social accounts. Their `id` is the `executor_id` / `executor_ids` other tools need |
| `get_app_state` | `{ id }` |
| `list_browsers` | Browsers running the ReachOwl extension |
| `get_browser` | `{ id }` |

### Team

| Tool | Purpose |
|------|---------|
| `list_teams` | `team_id` + teams |
| `list_team_members` | Members |
| `add_team_member` | `{ email, role? }` — invite (roles such as `agent`, `super_admin`) |
| `update_team_member` | `{ body: { id, user_id, status, role } }` |
| `delete_team_member` | `{ id }` — member row id |

## Rules

- Accounts and browsers can't be connected, activated, or disconnected through the API. Send the user to the ReachOwl app or extension (Browsers page) for that, including activating WhatsApp.
- Before any campaign, comment automation, scheduler, or growth plan, resolve the executor with `list_app_states` and match the platform.
- Confirm before removing a team member.

## Example

```
User: Which Instagram accounts can I run a campaign from?
→ list_app_states
→ "You have 2 Instagram accounts: @brand (id 55) and @brand.pk (id 61)."
```
