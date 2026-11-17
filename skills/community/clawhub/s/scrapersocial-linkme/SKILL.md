---
name: linkme-api
version: 1.0.4
description: Linkme data toolkit via ScraperSocial — resolve a Linkme page to the links and profile details it publishes.
license: MIT-0
author: ScraperSocial
homepage: https://scrapersocial.com
repository: https://github.com/nikhonit/social-media-api-skills
tags:
  - linkme
  - link-in-bio
  - creator
  - social-media
  - api
  - mcp
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

# Linkme API skill

Read public Linkme pages as clean JSON. This Linkme API skill has a single endpoint: give it a handle and it returns the links and profile details that page publishes, for 1 credit — the quickest way to turn a creator's link-in-bio into structured data.

This skill wraps **1 live Linkme endpoint** from the [ScraperSocial](https://scrapersocial.com) API. Public data only, returned as clean JSON.

## When to use this skill

- You are resolving a creator's link-in-bio into their actual destinations.
- You are building a creator profile and want every channel they link to.
- A user pastes a Linkme handle and asks what is on it.

### Do not use this skill when

- **The page is a Linktree, not a Linkme.** Use the `linktree-api` skill; they are different services.
- **You need analytics for a page you own.** Linkme's own dashboard has those.

## Setup

```bash
export SCRAPERSOCIAL_KEY=sk_live_...   # https://scrapersocial.com/app/keys
```

Signing up at [scrapersocial.com/signup](https://scrapersocial.com/signup) includes 100 free credits, no card required.

## Permissions and scope

These scripts do exactly three things and nothing else: read one environment variable (`SCRAPERSOCIAL_KEY`), send HTTPS requests to `https://api.scrapersocial.com` (the host is a constant in the code, not configurable), and print JSON. They run as `node scripts/<name>.js` with no other shell use, no file writes and no persistence. `call_endpoint.js` accepts only the 1 documented `/v1/linkme/` paths in the table below and refuses anything else before a request is made.

## Scripts

| Script | What it does | Input | Credits |
|---|---|---|---|
| `get_page.js` | Get LinkMe page. | handle | 1 credit |
| `call_endpoint.js` | Call any `/v1/linkme/` endpoint directly | path + params | varies |

Every script also accepts `--limit`, `--cursor`, `--fields`, `--format` and `--fresh`. `--limit` is clamped to 50: above that the API returns an async job instead of data.

## Example

```bash
node skills/linkme-api/scripts/get_page.js <linkme-handle>
```

Every response uses the same envelope:

```json
{ "data": {}, "meta": { "count": 20, "next_cursor": "..." }, "request_id": "a18e4ef88ad4b00b" }
```

`meta` appears on paginated endpoints only. Keep `request_id` — support traces calls with it.

## Endpoints

| Endpoint | Input | Returns | Credits | Paginated |
|---|---|---|---|---|
| `/v1/linkme/page` | handle | page | 1 credit | no |

Costs shown per item for paginated endpoints, per call otherwise. Failed calls are not charged.

## FAQ

### What does the Linkme endpoint return?

`get_page.js` with the handle returns the page's links and profile details, for 1 credit.

### Is this the same as Linktree?

No. Linktree is a separate service with its own skill in this repo, `linktree-api`.

### Is this an official Linkme API?

No. ScraperSocial is independent and not affiliated with Linkme. It returns publicly available page data only.

## Links

- [Linkme data on ScraperSocial](https://scrapersocial.com)
- [All 33 platform skills](https://github.com/nikhonit/social-media-api-skills)
- [OpenAPI spec](https://scrapersocial.com/openapi.json) · [llms.txt](https://scrapersocial.com/llms.txt)

## Disclaimer

ScraperSocial is an independent product and is not affiliated with, endorsed by, or sponsored by any platform named in this repository. All product names, logos and brands are property of their respective owners. These skills return only publicly available data.
