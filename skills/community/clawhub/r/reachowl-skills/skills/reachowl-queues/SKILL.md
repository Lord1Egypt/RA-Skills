---
name: reachowl-queues
description: "Look up and retry ReachOwl message queue items for a specific lead in a campaign. Use when a DM, friend request, or follow-up failed or is stuck, when the user asks whether a message was sent to someone, or wants to resend or reschedule a step."
license: MIT
compatibility: Requires the ReachOwl MCP server (https://reachowl.com/mcp).
metadata:
  author: ReachOwl
  version: "1.1.0"
  homepage: https://reachowl.com
  tags: reachowl, message-queue, retry, follow-ups
---

# ReachOwl Queues

Each contact in a campaign has queue rows, one per step (`-1`, `0`, `1`, `2`). Look up first, confirm, then update.

## Before you start

- Requires the ReachOwl MCP server connected with the user's token. If a tool reports a missing token, run the `reachowl-auth` flow.

## MCP tools

| Tool | Purpose |
|------|---------|
| `lookup_queues` | `{ campaign_id, audience_id? \| member_id? \| profile_url?, step? }` |
| `update_queue` | `{ body }` — usually `{ id, retry: true }` |

## Workflow

1. `lookup_queues` with `campaign_id` **plus one of** `audience_id`, `member_id`, or `profile_url`.
   - WhatsApp `member_id`: `923001234567@c.us`.
2. Show the user the matching rows (step, failed, status, message). If several match, ask which one.
3. Retry: `update_queue { body: { id, retry: true } }`.
   Other fields you can set in `body`: `message` (override text), `scheduled_at` (reschedule), `failed`, `sent`, `status`.

## Rules

- Don't retry repeatedly when the failure is permanent (account disconnected, profile not found); report the cause instead.
- To change message copy for everyone, edit the campaign (`reachowl-campaigns`), not individual queues.

## Example

```
User: Retry the WhatsApp message to +92 300 1234567 on campaign 18312
→ lookup_queues { campaign_id: 18312, member_id: "923001234567@c.us" }
→ update_queue { body: { id: 789, retry: true } }
```
