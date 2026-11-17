---
name: reachowl-profile-growth
description: "Grow an Instagram profile with ReachOwl profile growth plans that auto-like and repost niche posts found by hashtag, keyword search, or Explore, on a daily limit and weekly schedule. Use when the user wants Instagram growth, engagement automation, or to create, pause, resume, or edit an Instagram growth plan."
license: MIT
compatibility: Requires the ReachOwl MCP server (https://reachowl.com/mcp) and a connected Instagram account in ReachOwl.
metadata:
  author: ReachOwl
  version: "1.1.0"
  homepage: https://reachowl.com
  tags: reachowl, instagram-growth, instagram-automation, engagement, hashtags
---

# ReachOwl Profile Growth (Instagram)

Instagram only — `facebook` returns `422`.

## Before you start

- Requires the ReachOwl MCP server connected with the user's token. If a tool reports a missing token, run the `reachowl-auth` flow.

## MCP tools

| Tool | Purpose |
|------|---------|
| `list_profile_growth` | `{ type?: "instagram", page? }` |
| `get_profile_growth` | `{ id, include_posts? }` |
| `create_profile_growth` | `{ body }` |
| `update_profile_growth` | `{ id, body }` |
| `delete_profile_growth` | `{ id }` |
| `list_app_states` | Connected Instagram accounts → `executor_ids` |

## Create a plan

| Field | Notes |
|-------|-------|
| `name`, `team_id` | Required |
| `type` | `instagram` |
| `source_type` | `post_hashtag` · `post_search` · `post_explore` |
| `post_url` | The hashtag or keyword (not needed for `post_explore`) |
| `executor_ids` | Required — Instagram account ids |
| `engage_react` / `engage_repost` | Like / repost; at least one must be true |
| `limit` | Daily engagements, 1–50 (default 15) |
| `scan_limit` | Posts to discover, 1–500 |
| `status` | `draft` · `running` · `paused` · `completed` |
| `timezone`, `schedule` | e.g. `"UTC"`, `[{ "day": "monday", "start": "09:00", "end": "17:00" }]` |
| `start_date` / `end_date` | Optional date range |

```json
{
  "body": {
    "name": "Marketing niche growth",
    "team_id": 7715,
    "type": "instagram",
    "source_type": "post_hashtag",
    "post_url": "digitalmarketing",
    "executor_ids": [55],
    "engage_react": true,
    "engage_repost": false,
    "limit": 15,
    "status": "running"
  }
}
```

## Manage

- Pause / resume: `update_profile_growth { id, body: { status: "paused" } }` / `"running"`. Don't recreate the plan.
- Change hours: `update_profile_growth { id, body: { timezone, schedule } }`.
- See engaged posts: `get_profile_growth { id, include_posts: true }`.

## Good practice

- Start at a low `limit` (10–15) on new or recently connected accounts.
