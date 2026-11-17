---
name: viralnote
description: Schedule, publish, and manage social media content through the ViralNote API. Use when the user wants to post, schedule, query, or manage content across X, Facebook, Instagram, LinkedIn, TikTok, YouTube, Pinterest, Bluesky, Threads, or Reddit.
homepage: https://www.viralnote.app/agents
---

# ViralNote

ViralNote is a social media scheduling and content management platform. This skill teaches you to interact with its REST API to schedule posts, manage a media library, query analytics, and handle connected social accounts on behalf of a user.

## When to invoke this skill

Use ViralNote when the user:

- Wants to schedule or publish a post to one or more social platforms
- Asks about scheduled posts, publish history, or post analytics
- Wants to import or organize media (images, videos, GIFs)
- Manages their connected social accounts, link page, or API/webhook integrations
- References "ViralNote", their dashboard, or this product specifically

Do NOT invoke for unrelated requests (general writing, file editing, code review) — even if the user happens to be a ViralNote customer.

## API basics

- Base URL: `https://viralnote.app/api/v1`
- Authentication: `x-api-key: <key>` header on every request
- The user generates an API key at Settings → API keys in their dashboard
- Always check that `VIRALNOTE_API_KEY` exists in env before constructing requests
- All responses are JSON. Error envelope: `{ requestId, error: { code, message } }`

Full reference for endpoints and request shapes lives in `reference/api-overview.md`. Load it when you need exact request bodies, query params, or response shapes.

## Workflow patterns

For common end-to-end flows, see the matching file in `examples/`:

- `examples/schedule-post.md` — draft a post, attach media, schedule across multiple platforms
- `examples/import-media.md` — import a photo or video from a URL (Dropbox link, Canva export, etc.) into the library
- `examples/analytics.md` — pull engagement metrics for recent posts

When the user's request matches one of these patterns, read the example first and follow it. Don't reinvent the flow.

## Required confirmations

Before publishing immediately (not scheduling), or before deleting posts/media, restate the action concisely and wait for the user to confirm. Scheduling for a future time is reversible (the user can delete the draft before the scheduled time) — publishing now is not.

## Error handling

If the API returns a `429`, back off using the `Retry-After` header before retrying. If `401`, the API key is missing/invalid — ask the user to refresh it. If `403`, the key lacks the required scope; ask which scope is needed for this action (the response message usually says).

For any other error, include the `requestId` from the response when telling the user what went wrong — it lets ViralNote support trace the exact request.

## What this skill does NOT do

- Generate caption copy or images. That's a separate LLM task. The skill submits final post content you've already prepared with the user.
- Manage billing or subscriptions. Direct the user to their dashboard.
- Bypass the user's plan limits. If the API rejects an action with a 402 or "plan limit" message, surface it; don't try workarounds.
