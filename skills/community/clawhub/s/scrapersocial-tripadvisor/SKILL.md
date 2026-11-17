---
name: tripadvisor-api
version: 1.0.4
description: Tripadvisor data toolkit via ScraperSocial — property and attraction search plus full review listings.
license: MIT-0
author: ScraperSocial
homepage: https://scrapersocial.com
repository: https://github.com/nikhonit/social-media-api-skills
tags:
  - tripadvisor
  - travel
  - reviews
  - hotels
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

# Tripadvisor API skill

Read public Tripadvisor data as clean JSON. This Tripadvisor API skill does two things: search for hotels, restaurants and attractions, and pull the reviews for one. Review text is the valuable part — it is the most detailed public record of what guests actually experienced at a property.

This skill wraps **2 live Tripadvisor endpoints** from the [ScraperSocial](https://scrapersocial.com) API. Public data only, returned as clean JSON.

## When to use this skill

- You are researching a hotel, restaurant or attraction and want its reviews summarised.
- You are benchmarking a property against competitors on rating and review themes.
- A user pastes a Tripadvisor link and asks whether the place is any good.

### Do not use this skill when

- **You need live availability or pricing.** Not covered — this is listings and reviews, not a booking API.
- **You manage the property.** Tripadvisor's own management centre gives owners more.
- **You are pulling every review for a large hotel.** Reviews are charged per item; scope with `--limit`.

## Setup

```bash
export SCRAPERSOCIAL_KEY=sk_live_...   # https://scrapersocial.com/app/keys
```

Signing up at [scrapersocial.com/signup](https://scrapersocial.com/signup) includes 100 free credits, no card required.

## Permissions and scope

These scripts do exactly three things and nothing else: read one environment variable (`SCRAPERSOCIAL_KEY`), send HTTPS requests to `https://api.scrapersocial.com` (the host is a constant in the code, not configurable), and print JSON. They run as `node scripts/<name>.js` with no other shell use, no file writes and no persistence. `call_endpoint.js` accepts only the 2 documented `/v1/tripadvisor/` paths in the table below and refuses anything else before a request is made.

## Scripts

| Script | What it does | Input | Credits |
|---|---|---|---|
| `get_reviews.js` | List Tripadvisor reviews. | url | 3 credits per review |
| `search.js` | List Tripadvisor search. | query | 3 credits per place |
| `call_endpoint.js` | Call any `/v1/tripadvisor/` endpoint directly | path + params | varies |

Every script also accepts `--limit`, `--cursor`, `--fields`, `--format` and `--fresh`. `--limit` is clamped to 50: above that the API returns an async job instead of data.

## Example

```bash
node skills/tripadvisor-api/scripts/search.js "hotels in Lisbon"
```

Every response uses the same envelope:

```json
{ "data": {}, "meta": { "count": 20, "next_cursor": "..." }, "request_id": "a18e4ef88ad4b00b" }
```

`meta` appears on paginated endpoints only. Keep `request_id` — support traces calls with it.

## Endpoints

| Endpoint | Input | Returns | Credits | Paginated |
|---|---|---|---|---|
| `/v1/tripadvisor/reviews` | url | review | 3 credits per review | yes |
| `/v1/tripadvisor/search` | query | place | 3 credits per place | yes |

Costs shown per item for paginated endpoints, per call otherwise. Failed calls are not charged.

## FAQ

### How do I get Tripadvisor reviews as JSON?

`get_reviews.js` with the property URL, 3 credits per review returned. Use `--limit` and `--cursor` to page.

### How do I find a property without its URL?

`search.js` with a query returns matching properties at 3 credits each.

### Does this include hotel prices or availability?

No. Listings and reviews only.

### Is this an official Tripadvisor API?

No. ScraperSocial is independent and not affiliated with Tripadvisor. It returns publicly available data only.

## Links

- [Tripadvisor data on ScraperSocial](https://scrapersocial.com)
- [All 33 platform skills](https://github.com/nikhonit/social-media-api-skills)
- [OpenAPI spec](https://scrapersocial.com/openapi.json) · [llms.txt](https://scrapersocial.com/llms.txt)

## Disclaimer

ScraperSocial is an independent product and is not affiliated with, endorsed by, or sponsored by any platform named in this repository. All product names, logos and brands are property of their respective owners. These skills return only publicly available data.
