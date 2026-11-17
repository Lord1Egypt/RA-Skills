---
name: reachowl-mentions
description: "Social listening with ReachOwl keyword monitors: track keywords across Facebook groups, Instagram, Reddit (subreddits), and Quora, and review the posts found. Use when the user wants brand monitoring, keyword alerts, to find people asking for a product or service, to discover relevant discussions, or to see posts a monitor found."
license: MIT
compatibility: Requires the ReachOwl MCP server (https://reachowl.com/mcp). Facebook group and Instagram monitors need a connected account in ReachOwl.
metadata:
  author: ReachOwl
  version: "1.1.0"
  homepage: https://reachowl.com
  tags: reachowl, social-listening, keyword-monitoring, brand-monitoring, facebook-groups, reddit, quora
---

# ReachOwl Keyword Monitors (Social Listening)

## Before you start

- Requires the ReachOwl MCP server connected with the user's token. If a tool reports a missing token, run the `reachowl-auth` flow.

## MCP tools

| Tool | Purpose |
|------|---------|
| `list_mentions` | List monitors (omit `team_id`) |
| `get_mention` | `{ id }` |
| `create_or_update_mention` | `{ body }` — create (no `id`) or update (with `id`) |
| `delete_mention` | `{ id }` |
| `list_mention_posts` | `{ mention_id, page? }` — posts the monitor found |
| `delete_mention_post` | `{ id }` — remove one found post |
| `list_groups` | `{ search?, page?, limit? }` — synced Facebook groups (ids for `groups`) |
| `list_app_states` | Connected accounts (for `executor_id`) |

## Create a monitor

Body fields:

| Field | Notes |
|-------|-------|
| `team_id` | Required on create (from `get_user`) |
| `type` | `facebook_groups` · `instagram` · `subreddits` · `quora` |
| `keywords` | Array of phrases, e.g. `["looking for a realtor", "recommend an agent"]` |
| `name` | Label shown in the app |
| `status` | `1` on, `0` off |
| `groups` | `facebook_groups` only: ReachOwl group ids from `list_groups` |
| `executor_id` | `facebook_groups` / `instagram`: the connected account that scans (`list_app_states`). Reddit and Quora scan server-side; leave it out |

```json
{
  "body": {
    "team_id": 7715,
    "type": "facebook_groups",
    "name": "Realtor requests – Lahore",
    "keywords": ["looking for a realtor", "need a property dealer", "recommend an agent"],
    "groups": [111, 222],
    "executor_id": 3807,
    "status": 1
  }
}
```

Disable or edit: `create_or_update_mention { body: { id: 12, status: 0 } }`.

## Review results

1. `list_mention_posts { mention_id }` — each post has its `url`, `text`, and author details when available.
2. Summarize what people are asking for and highlight the strongest buying signals.
3. Remove noise with `delete_mention_post { id }`.

## Next steps

- Turn found posts into outreach: `reachowl-signal-outreach`.
- Get new posts pushed to another system: `reachowl-webhooks` with event `keyword-monitor-found-a-post` (sends at most 2 new posts per scan and ignores webhook `campaign_id`).

## Tips

- Use phrases people write when they have a need ("anyone know a…", "looking for…") rather than just your brand name.
- Scans are periodic, so new monitors take time to return posts.
