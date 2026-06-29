---
name: xpert
description: Grow on X (Twitter) with Xpert — connect over MCP or REST, then draft, rewrite, schedule, analyze, and reply in the user's own voice. Authenticate via OAuth 2.1 with dynamic client registration.
version: 1.0.2
license: MIT-0
homepage: https://xpert.so
---

# Xpert — grow on X

Xpert is an X (Twitter) growth tool. It learns a user's writing voice from their
existing posts, then helps generate ideas and hooks, write and rewrite posts,
schedule them, track engagement, and reply to their audience. This skill teaches
an agent how to connect to Xpert and operate it on a user's behalf.

## Endpoints
- **MCP server (Streamable HTTP):** `https://mcp.xpert.so/mcp`
- **MCP server (legacy SSE):** `https://mcp.xpert.so/sse`
- **REST API base:** `https://api.xpert.so`
- **Human sign-in / consent:** `https://app.xpert.so`

Discovery metadata:
- MCP Server Card: `https://xpert.so/.well-known/mcp/server-card.json`
- Authorization Server: `https://api.xpert.so/.well-known/oauth-authorization-server`
- Protected Resource Metadata: `https://mcp.xpert.so/.well-known/oauth-protected-resource`

## Authenticate (OAuth 2.1)
Xpert is its own OAuth 2.1 Authorization Server. No pre-registration is needed:

1. **Register** a client with Dynamic Client Registration (RFC 7591):
   `POST https://api.xpert.so/api/auth/oauth2/register`.
2. Run **authorization code + PKCE**. The user signs in and consents in the
   browser at `https://app.xpert.so` (X / email login).
3. Send a `resource` indicator (RFC 8707) of `https://mcp.xpert.so` (for MCP) or
   `https://api.xpert.so` (for REST) to receive a JWT access token for it.
4. Call with `Authorization: Bearer <token>`.

## Scopes
- `read` — profile, accounts, posts, analytics, trends, drafts, suggestions
- `write` — drafts, AI generation, scheduling and publishing
- `engage` — monitors, reply suggestions, approval queue, automation
- `dm` — direct-message outreach campaigns
- `admin` — manage API keys and X account connections

## What you can do
Over MCP you get typed tools, including:
- `get_me` — current user + active X account
- `compose_post` / `create_draft` — generate or save a post/thread in the user's voice
- `rewrite_text` — rewrite a draft
- `schedule_post` — schedule a draft for a future time
- `list_scheduled_posts`, `publish_now`
- `list_trends`, `get_trend` — niche-relevant trends
- `analytics_overview`, `analytics_growth` — performance
- `list_engagement_items`, `suggest_engagement_reply` — reply to the audience
- `xpert_api_call` — a generic escape hatch to any Xpert REST endpoint

## Example tasks
- "Draft three posts in my voice about <topic> and schedule the best one for my
  peak time tomorrow." → `compose_post` ×3, review, `schedule_post`.
- "Summarize how my last 30 posts performed and what's working." →
  `analytics_overview` + `analytics_content`.
- "Find trends in my niche and write a hook for the strongest one." →
  `list_trends` → `get_trend` → `compose_post`.

## Notes
- Credits are metered per AI action; check the user's balance via the billing
  surface if a call returns `402 insufficient_credits`.
- Always show generated content to the user for approval before publishing.
