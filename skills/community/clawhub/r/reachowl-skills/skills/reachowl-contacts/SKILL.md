---
name: reachowl-contacts
description: "List and inspect the leads (contacts) inside ReachOwl campaigns and add or delete CRM notes on them. Use when the user asks who is in a campaign, wants a lead's details or conversation notes, wants to log a note like 'replied yes', or needs to verify that an import worked."
license: MIT
compatibility: Requires the ReachOwl MCP server (https://reachowl.com/mcp).
metadata:
  author: ReachOwl
  version: "1.1.0"
  homepage: https://reachowl.com
  tags: reachowl, crm, leads, contacts, notes
---

# ReachOwl Contacts & Notes

## Before you start

- Requires the ReachOwl MCP server connected with the user's token. If a tool reports a missing token, run the `reachowl-auth` flow.

## MCP tools

| Tool | Purpose |
|------|---------|
| `list_contacts` | `{ campaign_id?, page? }` — omit `team_id` |
| `get_contact` | `{ id }` — detail including notes |
| `add_contact_note` | `{ contact_id, content, id? }` — pass `id` to edit an existing note |
| `delete_note` | `{ id }` — note id |

## Workflow

1. Scope to one campaign with `list_contacts { campaign_id }` whenever you know it (find it with `list_campaigns`).
2. Use `get_contact { id }` for the full record and existing notes.
3. Log outcomes with `add_contact_note { contact_id, content }`.
4. To **add** contacts, use `add_campaign_contacts` from `reachowl-campaigns` — these tools only read and annotate.

## Rules

- Report only fields the API returned; don't invent emails, phones, or statuses.
- Results are paginated; keep paging when the user asks for "all" contacts.

## Example

```
User: Show the contacts in campaign 18312 and note that Ali replied yes
→ list_contacts { campaign_id: 18312 }
→ get_contact { id: 456 }
→ add_contact_note { contact_id: 456, content: "Replied yes — wants pricing" }
```
