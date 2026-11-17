---
name: google-maps-api
version: 1.0.4
description: Google Maps data toolkit via ScraperSocial — place details, place search, photos and business contact discovery.
license: MIT-0
author: ScraperSocial
homepage: https://scrapersocial.com
repository: https://github.com/nikhonit/social-media-api-skills
tags:
  - google-maps
  - places
  - local-seo
  - contacts
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

# Google Maps API skill

Read public Google Maps data as clean JSON. This Google Maps API skill returns place details from a Maps URL, searches places by query, pulls the photos attached to a place, and extracts business contact details — the building blocks for local lead lists, store locators and location research.

This skill wraps **4 live Google Maps endpoints** from the [ScraperSocial](https://scrapersocial.com) API. Public data only, returned as clean JSON.

## When to use this skill

- A user pastes a Google Maps link and wants the place's details.
- You are building a local prospect list for a category and area.
- You need contact details for businesses matching a search.
- You want the photos associated with a location.

### Do not use this skill when

- **You need routing, geocoding or a map widget.** Google's Places and Directions APIs do those properly, with a licence that permits display.
- **You are compiling personal data.** `get_contacts.js` returns business contact details; treat the output under GDPR and local law, and do not use it for unsolicited bulk contact where that is restricted.
- **You need reviews.** Business reviews live in the `google-api` skill, not this one.

## Setup

```bash
export SCRAPERSOCIAL_KEY=sk_live_...   # https://scrapersocial.com/app/keys
```

Signing up at [scrapersocial.com/signup](https://scrapersocial.com/signup) includes 100 free credits, no card required.

## Permissions and scope

These scripts do exactly three things and nothing else: read one environment variable (`SCRAPERSOCIAL_KEY`), send HTTPS requests to `https://api.scrapersocial.com` (the host is a constant in the code, not configurable), and print JSON. They run as `node scripts/<name>.js` with no other shell use, no file writes and no persistence. `call_endpoint.js` accepts only the 4 documented `/v1/google_maps/` paths in the table below and refuses anything else before a request is made.

## Scripts

| Script | What it does | Input | Credits |
|---|---|---|---|
| `get_contacts.js` | List Google Maps contacts. | query | 3 credits per place |
| `get_photos.js` | List Google Maps photos. | url | 1 credit per image |
| `get_place.js` | Get Google Maps place. | url | 3 credits |
| `search.js` | List Google Maps search. | query | 2 credits per place |
| `call_endpoint.js` | Call any `/v1/google_maps/` endpoint directly | path + params | varies |

Every script also accepts `--limit`, `--cursor`, `--fields`, `--format` and `--fresh`. `--limit` is clamped to 50: above that the API returns an async job instead of data.

## Example

```bash
node skills/google-maps-api/scripts/search.js "coffee shops in Seattle"
```

Every response uses the same envelope:

```json
{ "data": {}, "meta": { "count": 20, "next_cursor": "..." }, "request_id": "a18e4ef88ad4b00b" }
```

`meta` appears on paginated endpoints only. Keep `request_id` — support traces calls with it.

## Endpoints

| Endpoint | Input | Returns | Credits | Paginated |
|---|---|---|---|---|
| `/v1/google_maps/contacts` | query | place | 3 credits per place | yes |
| `/v1/google_maps/photos` | url | image | 1 credit per image | yes |
| `/v1/google_maps/place` | url | place | 3 credits | no |
| `/v1/google_maps/search` | query | place | 2 credits per place | yes |

Costs shown per item for paginated endpoints, per call otherwise. Failed calls are not charged.

## FAQ

### How do I get place details from a Google Maps URL?

`get_place.js` with the Maps URL returns the place as structured JSON, for 3 credits.

### How do I find places by keyword?

`search.js` with a query, 2 credits per result returned. Use `--limit` to control cost.

### What does the contacts endpoint return?

`get_contacts.js` takes a query and returns business contact details at 3 credits per result. It is business data, not personal profiles — use it accordingly.

### Is this an official Google Maps API?

No. ScraperSocial is independent and not affiliated with Google. If you need to display a map or compute routes, use Google's own Platform APIs.

## Links

- [Google Maps data on ScraperSocial](https://scrapersocial.com)
- [All 33 platform skills](https://github.com/nikhonit/social-media-api-skills)
- [OpenAPI spec](https://scrapersocial.com/openapi.json) · [llms.txt](https://scrapersocial.com/llms.txt)

## Disclaimer

ScraperSocial is an independent product and is not affiliated with, endorsed by, or sponsored by any platform named in this repository. All product names, logos and brands are property of their respective owners. These skills return only publicly available data.
