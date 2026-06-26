# Public-facing API endpoints used by this skill

All endpoints are public, unauthenticated, and live under Target's
public-facing web aggregations host (see `scripts/_common.py` for the
exact base URL).

Every request must include `?key=<public-key>`. The default key
(`9f36aeafbe60771e321a7cc95a78140772ab3e96`) is baked into Target's web JS
bundle. Override with the `TARGET_API_KEY` env var if Target rotates it.

Responses are GraphQL-shaped JSON. **HTTP `206 Partial Content` is a normal
success code** for some operations (notably `plp_search_v2`); the shared
client treats `200` and `206` identically.

## Operations

| Op | Script | Purpose | Required params |
| --- | --- | --- | --- |
| `plp_search_v2` | `scripts/search.py` | Keyword or category search | `keyword` or `category`, `visitor_id`, `store_id`, `pricing_store_id`, `channel`, `count`, `offset`, `page` |
| `pdp_client_v1` | `scripts/pdp.py` | Product detail by TCIN | `tcin`, `store_id`, `pricing_store_id`, `channel` |
| `product_summary_with_fulfillment_v1` | `scripts/summary.py` | Multi-TCIN summary + fulfillment | `tcins` (CSV), `store_id`, `pricing_store_id`, `channel` |
| `fiats_v1` | `scripts/fulfillment.py` | Per-store stock + pickup ETA near a ZIP | `tcin`, `nearby` (ZIP), `radius`, `limit`, `requested_quantity`, `channel` |
| `nearby_stores_v1` | `scripts/stores.py` | Find stores near a ZIP/city | `place`, `limit`, `within` |
| `product_review_v1` | `scripts/reviews.py` | Review summary stats by TCIN | `tcin`, `channel` |

## Removed / deprecated

- `pdp_fulfillment_v1` → returns **HTTP 410 Gone**. Use `fiats_v1`.
- A typeahead/autocomplete operation almost certainly exists, but the name
  is not currently known. All guesses returned 400/410. Out of scope for v1.

## Field paths discovered the hard way

- Search product brand: `item.primary_brand.name` (NOT `item.enrichment.brand_info.brand_name`).
- Search/PDP primary image: `item.enrichment.image_info.primary_image.url`.
- PDP price for a single item is flat (`current_retail`, `reg_retail`).
  The `current_retail_min`/`current_retail_max` fields only appear on
  parent products with variants.
- PDP rating count: `ratings_and_reviews.statistics.review_count`.
- `nearby_stores_v1` returns no lat/lon. State lives in
  `mailing_address.region` (2-letter) or `mailing_address.state` (full).
- `product_summary_with_fulfillment_v1` does **not** return price. Combine
  with `pdp_client_v1` if price is needed per TCIN.
- `product_review_v1` returns only the review count + secondary attribute
  config — no review text. Full review bodies require a separate
  Bazaarvoice-style endpoint on `r2d2.target.com` (out of scope).

## Required headers

The shared client (`scripts/_common.py`) sends:

- `User-Agent` (override with `TARGET_USER_AGENT`)
- `Accept: application/json`
- `Origin: https://www.target.com`
- `Referer: https://www.target.com/`

Some operations 400 without a plausible Referer/Origin.

## Cart handoff (anonymous guest)

Three endpoints power `scripts/cart_link.py`. All three are reverse-engineered
from Target's web bundle (`cart-e306ccebbaa3178e.js` + module 41861 — the
constant `b1: "access_token"` confirmed the URL param name).

### 1. Mint a 24h anonymous bearer

```
POST https://gsp.target.com/gsp/oauth_tokens/v2/client_tokens?key=<KEY>
Content-Type: application/json

{"client_id": "ecom-web-1.0.0", "grant_type": "anonymous"}
```

Returns a JWT (`iss: MI6`, `sut: G` for guest, scope `ecom.none,openid`,
`exp` ~24h out). `client_id` is the only one that works for the public
key; `password`/`client_credentials` are rejected, `authorization_code`
needs a code. Auth host is `gsp.target.com` — `api.target.com/gsp/...`
returns 404.

### 2. Add items to the bound guest cart

```
POST https://carts.target.com/web_checkouts/v1/cart_items?key=<KEY>
Authorization: Bearer <token>
Content-Type: application/json

{
  "cart_type": "REGULAR",
  "cart_id": "<omit on first call; pass returned cart_id on subsequent>",
  "cart_item": {"tcin": "<TCIN>", "quantity": <n>, "channel": "WEB"}
}
```

Returns `cart_id`, `cart_item_id`, real `current_price`/`unit_price`,
return policies, etc. Valid `cart_type` values:
`[REGULAR, PARTIAL, RESTOCK, BTC, SFL, BTS, GUEST_SHIPT, SHIPT, STARBUCKS, MARKETPLACE, NONE]`.

The batch endpoint `web_checkouts/v1/multiple_cart_items` exists but
**rejects anonymous `MI6` tokens with 401** — stick with one POST per TCIN.

Other tempting endpoints that also reject anonymous tokens:
- `api.target.com/one_click_carts/v1/add-to-cart` — partner-only, 401
- `carts.target.com/web_checkouts/v1/lite_carts` — `MI6 is not an accepted token issuer`

### 3. Browser handoff URL

```
https://www.target.com/cart?access_token=<TOKEN>
```

The `/cart` SPA reads `access_token` from the query string, mints its
own session token, decodes our token's `sub` as `external_guest_id`,
then calls `POST carts.target.com/web_checkouts/v1/external_cart_merges`
with `{cart_type: "REGULAR", external_cart_id, external_guest_id}`.
The server merges items into the browser's session cart and the SPA
lands on `/cart`.

The dead pattern `/co-cart?TCIN=...&quantity=...` no longer works —
renders an empty cart. Do not use it.

## Sources

The API access pattern documented here was reconstructed entirely from
public information. See:

- https://gist.github.com/LumaDevelopment/f2a34a202fed6ab5a7f3a31282834943
