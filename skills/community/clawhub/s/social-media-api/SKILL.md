---
name: social-media-api
version: 1.0.4
description: One skill for ScraperSocial's public social media and web data API — discover every documented endpoint across 33 sources (social networks plus Amazon, Google, app stores, review sites and prediction markets) and call any of them by path. Personal-contact endpoints are excluded.
license: MIT-0
author: ScraperSocial
homepage: https://scrapersocial.com
repository: https://github.com/nikhonit/social-media-api-skills
tags:
  - social-media-api
  - mcp
  - agent-skills
  - api
  - web-scraping
  - social-media
allowed-tools: Bash(node:*)
metadata:
  openclaw:
    primaryEnv: SCRAPERSOCIAL_KEY
    homepage: https://scrapersocial.com
    requires:
      env:
        - SCRAPERSOCIAL_KEY
    network:
      allow:
        - api.scrapersocial.com
    shell:
      only: scripts/*.js
---

# Social media & web data API skill

One skill that reaches every source ScraperSocial covers. Most are social networks (TikTok, Instagram, LinkedIn, YouTube, X, Reddit, Threads, Facebook and more); the catalogue also includes public web data that is not social media: Amazon products and reviews, Google Search, Maps, News, Trends, Finance and Shopping, the App Store and Google Play, Tripadvisor, Trustpilot and Polymarket. Instead of installing a skill per platform, this one lists the whole documented catalogue and calls any entry by path. Endpoints that return a person's contact details are deliberately not callable from here; see Personal data below.

`list_endpoints.js` reads a bundled snapshot, so discovery is free and works without an API key. Only `call_endpoint.js` spends credits.

This skill reaches **225 of the 227 documented endpoints across 33 sources** in one place, instead of one skill per platform. The 2 endpoints that return personal contact details are listed but not callable from here.

## When to use this skill

- You do not know which platform a request will need until you see it.
- You want one tool in the agent's context rather than 33.
- You need an endpoint that has no dedicated script in its platform skill.
- You are exploring what the API can do before committing to a specific skill.

### Do not use this skill when

- **You already know the platform.** The dedicated skill has argument validation, section flags and platform-specific guidance on what not to do. Prefer `tiktok-api` over this for TikTok work.
- **You want guidance on cost or privacy for a specific platform.** That lives in the per-platform skill, where it can be specific.
- **You are looping over many endpoints to see what sticks.** Every call costs credits. Use `list_endpoints.js` — which is free — to decide first.

## Setup

```bash
export SCRAPERSOCIAL_KEY=sk_live_...   # https://scrapersocial.com/app/keys
```

## Permissions and scope

These scripts do exactly three things and nothing else: read one environment variable (`SCRAPERSOCIAL_KEY`), send HTTPS requests to `https://api.scrapersocial.com` (the host is a constant in the code, not configurable), and print JSON. They run as `node scripts/<name>.js` with no other shell use, no file writes and no persistence. `call_endpoint.js` accepts only paths present in the bundled `endpoints.json` catalogue, never the personal-contact endpoints below, and refuses anything else before a request is made.

## Personal data

Two catalogue entries return a named person's contact details: `/v1/google_maps/contacts` and `/v1/linkedin/profile-contact`. This skill refuses to call them, and it drops the `include_email` parameter that some profile endpoints accept, so no request made from here returns an email address or phone number. They remain visible in `list_endpoints.js` output with `personalData: true` so an agent can explain why a request was declined. Anyone with a lawful basis to process a specific person's contact data should use the platform skill (for example `linkedin-api`), which documents the requirement and the cost. Everything else this skill returns is public data.

## Scripts

| Script | What it does | Credits |
|---|---|---|
| `list_endpoints.js` | List every endpoint, filterable by platform or keyword | free, no key needed |
| `call_endpoint.js` | Call any documented endpoint by path (personal-contact endpoints excluded) | the endpoint's own cost |

```bash
node skills/social-media-api/scripts/list_endpoints.js --search transcript
node skills/social-media-api/scripts/call_endpoint.js /v1/github/profile --handle torvalds
```

## Platforms

| Platform | Path segment | Endpoints |
|---|---|---|
| Amazon | `/v1/amazon/` | 4 |
| App Store | `/v1/app_store/` | 6 |
| Bluesky | `/v1/bluesky/` | 3 |
| Facebook | `/v1/facebook/` | 23 |
| GitHub | `/v1/github/` | 11 |
| Google | `/v1/google/` | 5 |
| Google Finance | `/v1/google_finance/` | 3 |
| Google Maps | `/v1/google_maps/` | 4 |
| Google News | `/v1/google_news/` | 1 |
| Google Play | `/v1/google_play/` | 4 |
| Google Shopping | `/v1/google_shopping/` | 1 |
| Google Trends | `/v1/google_trends/` | 2 |
| Hacker News | `/v1/hackernews/` | 4 |
| Instagram | `/v1/instagram/` | 23 |
| Kwai | `/v1/kwai/` | 3 |
| LinkedIn | `/v1/linkedin/` | 38 |
| Linkme | `/v1/linkme/` | 1 |
| Linktree | `/v1/linktree/` | 1 |
| Naver | `/v1/naver/` | 4 |
| Pinterest | `/v1/pinterest/` | 3 |
| Polymarket | `/v1/polymarket/` | 1 |
| Reddit | `/v1/reddit/` | 8 |
| Snapchat | `/v1/snapchat/` | 1 |
| Spotify | `/v1/spotify/` | 6 |
| Threads | `/v1/threads/` | 5 |
| TikTok | `/v1/tiktok/` | 16 |
| TikTok Shop | `/v1/tiktokshop/` | 5 |
| Tripadvisor | `/v1/tripadvisor/` | 2 |
| Trustpilot | `/v1/trustpilot/` | 1 |
| Truth Social | `/v1/truthsocial/` | 2 |
| Twitch | `/v1/twitch/` | 3 |
| X (Twitter) | `/v1/twitter/` | 7 |
| YouTube | `/v1/youtube/` | 26 |

## FAQ

### How do I find the right endpoint?

`list_endpoints.js --search transcript` filters by keyword, `--platform tiktok` filters by platform. It reads a local snapshot, so it costs nothing and needs no key.

### How do I call an endpoint?

`call_endpoint.js /v1/github/profile --handle torvalds`. Any flag after the path is passed through as a query parameter, so `--limit`, `--cursor`, `--fields`, `--format` and `--fresh` all work.

### Is the bundled endpoint list always current?

It is a snapshot generated from the live OpenAPI spec when the repo was last built. `call_endpoint.js` only accepts paths that are in that snapshot, so an endpoint added to the API after the last build is refused until the repo is rebuilt. That is intentional: the callable surface is exactly what this file documents.

### Can this skill fetch someone's email or phone number?

No. The two endpoints that return personal contact details (`/v1/linkedin/profile-contact` and `/v1/google_maps/contacts`) are excluded from `call_endpoint.js`, and the `include_email` parameter is stripped before any request is sent. If you have a lawful basis to process a specific person's contact data, use the `linkedin-api` skill, which documents the requirements and the cost; this skill will not do it.

### Should I use this or the per-platform skills?

Per-platform when you know the platform — they carry the guardrails. This one when you do not, or when you need an endpoint no script wraps.

## Disclaimer

ScraperSocial is an independent product and is not affiliated with, endorsed by, or sponsored by any platform named in this repository. All product names, logos and brands are property of their respective owners. These skills return only publicly available data.
