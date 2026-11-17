---
name: reachowl-post-scheduler
description: "Schedule and auto-post content to multiple Facebook groups with ReachOwl's post scheduler: create posting schedules, set intervals or calendar times, pause, edit posts, clone, and clear pending posts. Use for Facebook group marketing, community posting, or sharing an announcement across many groups."
license: MIT
compatibility: Requires the ReachOwl MCP server (https://reachowl.com/mcp) and a connected Facebook account with synced groups in ReachOwl.
metadata:
  author: ReachOwl
  version: "1.1.0"
  homepage: https://reachowl.com
  tags: reachowl, facebook-groups, post-scheduler, community-posting, social-media-scheduling
---

# ReachOwl Post Scheduler (Facebook groups)

## Before you start

- Requires the ReachOwl MCP server connected with the user's token. If a tool reports a missing token, run the `reachowl-auth` flow.
- Show the user the final post text and the target groups, and get a yes, before creating a scheduler that is on.

## MCP tools

| Tool | Purpose |
|------|---------|
| `list_groups` | `{ search?, page?, limit? }` — groups synced in the user's account |
| `list_app_states` | Connected Facebook accounts → `executor_id` |
| `list_post_schedulers` | `{ page?, per_page? }` |
| `get_post_scheduler` | `{ id }` |
| `create_post_scheduler` | `{ body }` |
| `update_post_scheduler` | `{ id, body }` |
| `delete_post_scheduler` | `{ id }` |

## Create a scheduler

| Field | Notes |
|-------|-------|
| `name` | Required |
| `executor_id` | Required — Facebook account from `list_app_states` |
| `team_id` | Recommended (from `get_user`) |
| `group_urls` | Required — array (or comma-separated string) of `https://www.facebook.com/groups/…` URLs. Preferred over `group_ids` |
| `schedule_type` | `interval` or `calendar` |
| `interval` | Minutes between posts (interval mode) |
| `time` / `calendar_items` | `HH:MM` and calendar payload (calendar mode) |
| `posts` | Required — `[{ "text": "…" }]`, one or more posts |
| `clone_from` | Copy an existing scheduler id instead of building one |

```json
{
  "body": {
    "name": "Open house – June",
    "executor_id": 3807,
    "team_id": 7715,
    "group_urls": [
      "https://www.facebook.com/groups/123456789",
      "https://www.facebook.com/groups/lahore-property"
    ],
    "schedule_type": "interval",
    "interval": 20,
    "posts": [
      { "text": "Open house this Saturday in DHA Phase 6 — 3-bed, 10 marla. Comment or DM for the address." }
    ]
  }
}
```

## Manage

- Pause or resume: `update_post_scheduler { id, body: { status: 0 } }` / `{ status: 1 }`.
- Remove pending posts: `update_post_scheduler { id, body: { delete_queue_ids: [101, 102] } }`.
- Replace posts: send `posts` again (include `id` on posts you keep).
- Duplicate: `create_post_scheduler { body: { clone_from: 88 } }`.

## Errors

- `422` "groups were not found": the group isn't synced. Use `list_groups` to see what's available, or ask the user to sync groups from their connected Facebook browser.

## Good practice

- Write a slightly different version for each group's audience instead of one identical post everywhere, and respect each group's rules.
- Use a 15–30 minute `interval` rather than posting to many groups at once.
- To turn an article or announcement into group posts, see `reachowl-content-distribution`.
