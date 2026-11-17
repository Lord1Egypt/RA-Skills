---
name: reachowl-comment-automations
description: "Auto-reply to Facebook and Instagram post comments with ReachOwl: when a comment contains a keyword (like 'price' or 'info'), post a public reply and send the commenter a private DM. Use for comment-to-DM funnels, lead magnets, giveaway posts, or to pause, edit, or check activity on a comment automation."
license: MIT
compatibility: Requires the ReachOwl MCP server (https://reachowl.com/mcp) and a connected Facebook or Instagram account in ReachOwl.
metadata:
  author: ReachOwl
  version: "1.1.0"
  homepage: https://reachowl.com
  tags: reachowl, comment-automation, comment-to-dm, facebook-marketing, instagram-marketing, auto-reply
---

# ReachOwl Comment Automations

## Before you start

- Requires the ReachOwl MCP server connected with the user's token. If a tool reports a missing token, run the `reachowl-auth` flow.
- Show the user the reply and DM text before creating an `active` automation.

## MCP tools

| Tool | Purpose |
|------|---------|
| `list_comment_automations` | `{ type?: "facebook" \| "instagram" }` |
| `get_comment_automation` | `{ id }` |
| `create_comment_automation` | `{ body }` |
| `update_comment_automation` | `{ id, body }` |
| `delete_comment_automation` | `{ id }` |
| `list_comment_automation_executions` | `{ id, status?, page?, per_page? }` — reply/DM log |
| `list_app_states` | Connected accounts → `executor_id` |

## Create

| Field | Notes |
|-------|-------|
| `name` | Required |
| `executor_id` | Required — the account that owns or can comment on the post |
| `keywords` | Required — any match triggers, e.g. `["price", "info", "interested"]` |
| `posts` | Required — `[{ "post_url": "https://…" }]` |
| `public_reply_message` | Required — string or array of variants |
| `private_dm_message` | Required — string or array of variants |
| `type` | `facebook` (default) or `instagram` |
| `status` | `active` or `paused` |

Placeholders: `{{name}}`, `{{first_name}}`, `{{last_name}}`.

```json
{
  "body": {
    "name": "Price replies – DHA listing",
    "type": "facebook",
    "executor_id": 3807,
    "status": "active",
    "keywords": ["price", "rate", "how much"],
    "posts": [{ "post_url": "https://www.facebook.com/groups/123/posts/456" }],
    "public_reply_message": ["Thanks {{first_name}}! Sent you the details in DM.", "Check your inbox, {{first_name}} 👋"],
    "private_dm_message": ["Hi {{first_name}}, the asking price is 2.4 crore. Want to book a visit this week?"]
  }
}
```

## Manage

- Pause / resume: `update_comment_automation { id, body: { status: "paused" } }` / `"active"`.
- Watch different posts: `update_comment_automation { id, body: { posts: [{ post_url }] } }` (replaces the list).
- Check results: `list_comment_automation_executions { id, status: "failed" }` — statuses `pending`, `processing`, `completed`, `skipped`, `failed`.

## Good practice

- Provide 2–3 variants for both the reply and the DM so they don't look automated.
