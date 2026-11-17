---
name: socialapis
description: Get public Facebook and Instagram data (pages, posts, comments, groups, photo albums, Meta Ads Library, Marketplace listings, Instagram profiles, posts, reels and locations) through the SocialAPIs REST API or its MCP server. Use when the user wants to look up, monitor, compare or analyze public Facebook or Instagram content, competitors' ads, or Marketplace listings, or wants code that does.
---

# SocialAPIs: Facebook & Instagram data

SocialAPIs returns public Facebook and Instagram data as JSON. No Meta developer app or OAuth: one API key.

- REST base URL: `https://api.socialapis.io` (all endpoints are `GET` with query parameters)
- MCP server (hosted): `https://mcp.socialapis.io/mcp`, or local `npx -y @socialapis/mcp`
- Full endpoint list with parameters and prices: [references/endpoints.md](references/endpoints.md)
- OpenAPI spec: https://socialapis.io/openapi.json

## Setup

1. The user needs an API key from https://socialapis.io/dashboard (free plan: 200 credits a month, no card).
2. Read it from the environment, `SOCIALAPIS_API_KEY`. **Never** hard-code it, print it, or ask the user to paste it into the chat. If it's missing, tell the user to set it.
3. Send it in the **`x-api-token` header**. Never put the key in a URL or query string.

If SocialAPIs MCP tools are already available in this session (tools named `facebook_page`, `facebook_ads`, `instagram_profile`, …), use them instead of raw HTTP. Each takes an `action` argument; the tool description lists the actions and their inputs.

## Making a call

```bash
curl -s -H "x-api-token: $SOCIALAPIS_API_KEY" \
  "https://api.socialapis.io/facebook/pages/details?link=https://www.facebook.com/nike"
```

```python
import os, requests

r = requests.get(
    "https://api.socialapis.io/instagram/profile/details",
    params={"username": "nike"},
    headers={"x-api-token": os.environ["SOCIALAPIS_API_KEY"]},
    timeout=120,
)
r.raise_for_status()
data = r.json()
```

Official SDKs if the user is writing an app: Python `pip install socialapis-sdk`, JavaScript `npm install socialapis-sdk`, Go `go get github.com/SocialAPIsHub/socialapis-go`. For n8n there's the `n8n-nodes-socialapis` community node.

## Choosing the endpoint

| The user wants | Call |
|---|---|
| A page's profile: followers, category, contact info | `/facebook/pages/details?link=<page url>` |
| A page's recent posts | `/facebook/pages/posts?link=<page url>&limit=9` (3-9 per call) |
| A page by name, not URL | `/facebook/search/pages?query=<name>`, then use the returned link |
| One post's text, reactions, comments count | `/facebook/posts/details?link=<post url>` |
| Views, video URLs or audio of a reel/video post | `/facebook/posts/details/extended?link=<post url>` |
| Comments on a post | `/facebook/posts/comments?link=<post url>` |
| A public group's info / posts | `/facebook/groups/details` / `/facebook/groups/posts` with `link=<group url>` |
| A page's or group's photo albums | `/facebook/pages/albums?profile_id=…` (ID from `/facebook/pages/id`) or `/facebook/groups/albums?group_id=…` (ID from `/facebook/groups/id`), then `/facebook/albums/items?album_id=…` for the photos and videos |
| Ads a brand is running | `/facebook/ads/search?query=<brand or keyword>&country=<ISO code>` |
| Which advertisers use a keyword | `/facebook/ads/keywords?query=<keyword>` |
| Marketplace listings near a city | `/facebook/marketplace/city-coordinates?city=<city>`, then `/facebook/marketplace/search` with the latitude/longitude |
| An Instagram profile | `/instagram/profile/details?username=<username>` |
| An Instagram profile's posts / reels | `/instagram/profile/posts?username=…` / `/instagram/profile/reels?user_id=…` |
| An Instagram profile's story highlights | `/instagram/profile/highlights?user_id=<pk>`, then `/instagram/highlight/details?highlight_id=…` |
| One Instagram post | `/instagram/post/details?shortcode=<code from /p/<code>/>` |
| Credits left | `/usage` (free) |

Check [references/endpoints.md](references/endpoints.md) for every parameter before calling an endpoint you haven't used.

## Things that matter

- **Instagram has two IDs per profile.** `/instagram/user/id` returns both: the long `user_id` (e.g. `17841401474538262`) for `/instagram/profile/posts` and `/instagram/profile/reels`, and the short `pk` (e.g. `528817151`) for `/instagram/profile/highlights`, which still takes it in a parameter named `user_id`. Using the wrong one returns nothing.

- **Credits:** most calls cost 1 credit; some cost more (each endpoint says so). Responses include the headers `X-SocialAPIs-Credits-Deducted` and `X-SocialAPIs-Credits-Remaining`, and most bodies have a `meta` block with the same numbers. Before a large batch, check `/usage` and tell the user roughly what it will cost.
- **Pagination:** list endpoints return a small page plus `end_cursor`. Pass it back as `end_cursor` for the next page. Stop when it's missing or the user has enough.
- **Slow calls:** scrapes can take up to ~90 seconds. Use a timeout of at least 120 s and don't fire hundreds of calls in parallel; plans have rate limits (`/usage/limits`).
- **Errors:**
  - `401`: missing or invalid key.
  - `403`: out of credits, or the account is paused.
  - `429`: rate limit; wait and retry with backoff.
  - `502` / `504`: the source failed or timed out; retry once later.
  - Failed calls are not charged.
- **Not available:** private content, Instagram hashtag search, Instagram comments, Facebook user profiles. Only Facebook and Instagram are supported today; say so rather than guessing at other platforms.

## Use the data responsibly

Only public data is returned. Don't use it to track or profile private individuals, spam people, or for anything unlawful; the user is responsible for complying with data-protection law (GDPR, CCPA) for what they collect. See https://socialapis.io/terms.
