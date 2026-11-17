---
name: reachowl-api
description: "Make a raw authenticated call to the ReachOwl V1 REST API through the ReachOwl MCP server when no named ReachOwl tool covers the request, such as a query parameter or field the named tools don't expose. Use only after checking the other ReachOwl skills."
license: MIT
compatibility: Requires the ReachOwl MCP server (https://reachowl.com/mcp).
metadata:
  author: ReachOwl
  version: "1.1.0"
  homepage: https://reachowl.com
  tags: reachowl, api, rest
---

# ReachOwl API Escape Hatch

## Before you start

- Requires the ReachOwl MCP server connected with the user's token. If a tool reports a missing token, run the `reachowl-auth` flow.

## MCP tool

| Tool | Purpose |
|------|---------|
| `api_request` | `{ method, path, query?, body? }` — `path` must start with `/api/v1/` |

## Rules

1. Prefer the named tools; use this only when they can't express the request.
2. Use documented V1 paths only: `campaigns`, `contacts`, `notes`, `queues`, `groups`, `mentions`, `post-scheduler`, `profile-growth`, `stages`, `message-templates`, `browsers`, `app-states`, `teams`, `team`, `events`, `webhooks`, `comment-automations`, `user`.
3. Confirm with the user before any `POST`, `PUT`, `PATCH`, or `DELETE`.
4. The rate limit is 120 requests per minute.
5. The same rules apply as with named tools — for example, add contacts with `POST /api/v1/campaigns/{id}/contacts`, never by creating a new campaign.

## Example

```
User: Search my synced groups for "mortgage", 50 per page
→ api_request { method: "GET", path: "/api/v1/groups", query: { search: "mortgage", limit: 50 } }
```
