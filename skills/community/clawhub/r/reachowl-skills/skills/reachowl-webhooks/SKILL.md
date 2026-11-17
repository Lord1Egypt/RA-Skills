---
name: reachowl-webhooks
description: "Send ReachOwl events to other apps with webhooks: new keyword-monitor posts, sent messages, replies, accepted friend requests, and failures. Use when the user wants notifications in Slack, a CRM, Zapier, Make, n8n, or their own server when something happens in ReachOwl, or wants to list, change, or remove webhooks."
license: MIT
compatibility: Requires the ReachOwl MCP server (https://reachowl.com/mcp).
metadata:
  author: ReachOwl
  version: "1.1.0"
  homepage: https://reachowl.com
  tags: reachowl, webhooks, integrations, zapier, n8n, notifications
---

# ReachOwl Webhooks

## Before you start

- Requires the ReachOwl MCP server connected with the user's token. If a tool reports a missing token, run the `reachowl-auth` flow.

## MCP tools

| Tool | Purpose |
|------|---------|
| `list_events` | Event catalog — the only source of valid event ids/slugs |
| `list_webhooks` | Existing webhooks |
| `create_webhook` | `{ url, events, campaign_id?, id? }` |
| `update_webhook` | `{ id, url?, events?, campaign_id? }` |
| `delete_webhook` | `{ id }` |

## Workflow

1. `list_events` and pick the events the user wants.
2. `create_webhook { url, events, campaign_id? }` — `campaign_id` limits campaign events to one campaign.
3. Confirm with `list_webhooks`.

Common events (check `list_events` for the current list):

- `contact-is-sent-a-message`, `contact-reply-to-your-message`
- `contact-is-sent-a-friend-request`, `contact-accept-your-friend-request`
- `contact-failed-process`
- `keyword-monitor-found-a-post`

## keyword-monitor-found-a-post

- Fires once per scan that stores new posts, with at most **2** posts in `posts[]` (`new_posts` gives the full count).
- Ignores `campaign_id`.
- Payload: `{ event, mention: { id, name, type, keywords }, new_posts, posts: [{ id, url, text, … }] }`.
- Use `list_mention_posts` to fetch the rest.

## Example

```
User: Send new keyword-monitor posts to https://hooks.example.com/reachowl
→ list_events
→ create_webhook { url: "https://hooks.example.com/reachowl", events: ["keyword-monitor-found-a-post"] }
→ list_webhooks
```
