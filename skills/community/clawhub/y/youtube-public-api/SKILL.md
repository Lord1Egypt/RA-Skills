---
name: youtube-public-api
title: YouTube Public Reads
description: Read-only YouTube data API for video, channel, playlist, comments, related-video, search, and transcript research through ReplyNodes prepaid credits with one long-lived Bearer fetcher key.
version: 2.0.1
mode: readonly
auth: Authorization: Bearer YOUR_FETCHER_KEY
---

# YouTube Public Reads

Read-only YouTube data API for video, channel, playlist, comments, related-video, search, and transcript research through ReplyNodes prepaid credits with one long-lived Bearer fetcher key.

## Setup

1. Create a free ReplyNodes account at https://app.replynodes.com/auth.
2. The Free plan includes 500 one-time credits and does not require payment setup.
3. Open https://app.replynodes.com/developers and create the single long-lived ReplyNodes fetcher API key.
4. Store the secret as REPLYNODES_API_KEY in the agent secret store. Never paste it into chat, commit it, or put it in a URL.
5. Send it on API calls as Authorization: Bearer YOUR_FETCHER_KEY.

Gateway: https://api.replynodes.com

## Authentication

Use one long-lived ReplyNodes fetcher key. Send it on every request as:

```http
Authorization: Bearer YOUR_FETCHER_KEY
```

Store the real key in the agent's secret configuration. Never put it in prompts, source files, logs, URLs, or returned data. The gateway performs shared control-plane scope and entitlement checks.

## Plans and prepaid credits

- Payment mode: `prepaid_credit` only.
- Free: 500 one-time credits.
- Developer: 10,000 credits/month at $19/month.
- Pro: 100,000 credits/month at $99/month.
- Failed or provider-error requests cost zero; monthly credits do not roll over; paid overage requires an explicit cap.

- YouTube transcripts cost 200 credits; standard YouTube reads cost 2 credits.

## Read-only operations

Every operation is an HTTP GET and reads public data only:

- `search` — `GET https://api.replynodes.com/v1/youtube/search`. Search public YouTube videos This operation costs 2 prepaid credits.
- `video` — `GET https://api.replynodes.com/v1/youtube/video/{id}`. Fetch public YouTube video metadata This operation costs 2 prepaid credits.
- `channel` — `GET https://api.replynodes.com/v1/youtube/channel/{id}`. Fetch public YouTube channel metadata This operation costs 2 prepaid credits.
- `comments` — `GET https://api.replynodes.com/v1/youtube/comments/{id}`. Fetch public top-level video comments This operation costs 2 prepaid credits.
- `playlist` — `GET https://api.replynodes.com/v1/youtube/playlist/{id}`. Fetch public playlist metadata and items This operation costs 2 prepaid credits.
- `related` — `GET https://api.replynodes.com/v1/youtube/related/{id}`. Fetch related public videos This operation costs 2 prepaid credits.
- `transcript` — `GET https://api.replynodes.com/v1/youtube/transcript/{id}`. Fetch a public video transcript when available This operation costs 200 prepaid credits.

## Request and response behavior

- Use `https://api.replynodes.com` as the gateway origin.
- Encode path parameters and query values; do not put credentials in query strings.
- Preserve the gateway response envelope and request ID when reporting results.
- Treat unavailable upstream data as unavailable; do not fabricate fields or success.
- Do not retry non-idempotent methods: this package has no non-GET methods.

## Example

```bash
curl -sS https://api.replynodes.com/v1/youtube/capabilities
curl -sS -H "Authorization: Bearer YOUR_FETCHER_KEY" \
  "https://api.replynodes.com/v1/youtube/search"
```

## Safety boundaries

This skill has no write, publish, account, follow, or credential-management operation. It must not be used to claim private data access, unauthenticated access, guaranteed availability, or unsupported pricing.

## Source and validation

The operation list is generated from `services/youtube-fetcher/internal/capabilities/capabilities.go`. `manifest.json`, `references/operations.json`, and `CHECKSUMS.sha256` are generated artifacts; change the catalog or source capability contract and regenerate them together.
