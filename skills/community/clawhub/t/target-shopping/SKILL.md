---
name: target-com-shopper
description: Search Target.com, look up products, check per-store stock and pickup ETAs near a ZIP, and build a deep link that pre-populates a guest cart. Read-only browsing plus an unauthenticated guest-cart builder; no login, no checkout.
version: 0.1.0
metadata:
  openclaw:
    emoji: "🎯"
    homepage: https://github.com/druyang/target-shopper-skill
    requires:
      bins:
        - python3
        - uv
---

# target-com-shopper

Browse Target.com from the assistant. Wraps a handful of Target's
public-facing JSON endpoints (the same ones target.com itself loads) and
one local URL builder that pre-populates a guest cart in the user's browser.

## Disclaimers & limitations

**Unofficial.** Not affiliated with, endorsed by, or sponsored by Target
Corporation. "Target" and the Target bullseye are trademarks of Target
Brands, Inc.; they are used here only to describe the service this skill
talks to.

**Public web endpoints, not a stable API.** The skill calls Target's
public-facing web API (the same JSON endpoints target.com itself loads in
your browser) and `carts.target.com`. These are not a documented public API.
Field shapes, auth keys, throttling, and even endpoint availability can
change without notice; expect breakage and pin the version you tested against.

**No warranty on prices, stock, or pickup ETAs.** Results are point-in-time
snapshots of what the API returned. Prices and availability change
constantly and may differ from what the user actually sees at checkout.
Always direct the user to `buy_url` for the source of truth before they
commit to a purchase.

**Personal / light use only.** Single-shot lookups for a real shopping
task, not bulk scraping, competitive price monitoring, or inventory
mirroring. The in-script throttle (`TARGET_MIN_INTERVAL`, default 1s) is
the floor — do not lower it. See `references/tos-and-etiquette.md`.

**The cart-link feature creates a real server-side guest cart.** It mints
a 24-hour anonymous bearer token against `gsp.target.com` and POSTs TCINs
to `carts.target.com`. Treat the resulting URL like a one-time share link:
it grants ~24h of cart-write access to whoever holds it. No login, payment
info, or shipping address is ever transmitted.

**No checkout, payment, or auth.** Checkout, returns, saved carts, Circle
deals tied to an account, and order history are out of scope and will
stay out of scope. If you need any of those, open target.com in a browser.

## When to use

- "Search Target for X."
- "What's the price / rating / spec on Target product <TCIN or URL>?"
- "Is this in stock near ZIP <z>? When can I pick it up?"
- "Find Target stores near me."
- "Build me a Target cart link for these items."

## When NOT to use

- **Anything requiring login** (saved carts, Circle deals tied to account,
  order history, returns, gift registry edits). This skill is read-only and
  intentionally unauthenticated.
- **Checkout, payment, or shipping addresses.** The skill builds a cart URL
  the user opens in their own browser; everything from there is on them.
- **Bulk scraping or price monitoring.** See `references/tos-and-etiquette.md`.

## Setup (once)

The skill ships as a `uv` project under its own directory. From the skill
root (`~/.openclaw/workspace/skills/target-com-shopper/` at runtime):

```bash
uv sync
```

That's it — runtime is stdlib-only; `uv` is just used for the venv and to
run scripts reproducibly.

## Discover the user's store first

`store_id` shapes every product/price/fulfillment response. **Ask the user
for their ZIP code** (or city) before calling product endpoints, then look
up nearby stores:

```bash
uv run python -m scripts.stores 55403 --limit 5
```

Pick a `store_id` from the results and pass it as `--store-id` to
`search`, `pdp`, and `summary`. (Or set `TARGET_DEFAULT_STORE_ID` in the
environment for the session.) If the user truly doesn't care about
location, the default store (`2281`, San Jose Central) is fine for
keyword search and PDP, but **not** for accurate "in stock today" answers.

## Common tasks

### Search

```bash
uv run python -m scripts.search "wireless earbuds" --count 10 --store-id 1375
uv run python -m scripts.search --category 5xteg --count 10
uv run python -m scripts.search "chicken breast" --category 4tgi7   # keyword AND category
```

`--raw` returns the full API payload. Default trims to `tcin`, `title`,
`brand`, `price`, `rating`, `buy_url`, `image`.

**Fresh-grocery searches:** generic keyword search drowns fresh items in
shelf-stable hits (e.g. "chicken breast" returns canned chicken first).
Combine the keyword with a category N-ID to scope —
see [references/categories.md](references/categories.md) for the curated
list of common N-IDs (Fresh Chicken, Fresh Produce, Herbs & Spices, etc.).

**Building a multi-item shopping list?** The skill has no batched search
endpoint — `plp_search_v2` accepts one query at a time. Fire individual
`scripts.search` calls in parallel from the agent runtime; the in-script
`TARGET_MIN_INTERVAL` throttle (default 1s) protects the upstream. For a
6-item list expect ~6 seconds wall time. Do not lower `TARGET_MIN_INTERVAL`
below 0.5s — see `references/tos-and-etiquette.md`.

### Product detail

```bash
uv run python -m scripts.pdp 89827259 --store-id 1375
```

Returns title, brand, price, bullets, images, promotions, variant TCINs.

### Multi-product fulfillment summary

For a shortlist (e.g. comparing 3–5 candidates) use `summary` instead of
calling `pdp` N times — one round trip:

```bash
uv run python -m scripts.summary 89827259 94783927 --zip 55403 --store-id 1375
```

Note: `summary` does **not** return price. Combine with `pdp` if needed.

### Per-store stock & pickup ETA

```bash
uv run python -m scripts.fulfillment 89827259 --zip 55403 --radius 25 --only-available
```

### Find nearby stores

```bash
uv run python -m scripts.stores "Minneapolis, MN" --limit 5
uv run python -m scripts.stores 55403 --within 25
```

### Build a cart deep link

This actually pre-populates the recipient's cart. Behind the scenes the
script mints a 24h anonymous guest token (`gsp.target.com`), creates a
real server-side cart by POSTing each TCIN to `carts.target.com`, writes
a local HTML redirect file, and tries to launch the user's default
browser at:

```
https://www.target.com/cart?access_token=<TOKEN>
```

When the browser opens it, target.com merges the items into the session
cart and lands on `/cart`. No login required.

```bash
uv run python -m scripts.cart_link 89827259 94783927 --quantities 1 2
uv run python -m scripts.cart_link 89827259                 # qty defaults to 1
uv run python -m scripts.cart_link 111 222 333 --quantities 2  # qty=2 for all
uv run python -m scripts.cart_link 89827259 --refresh-token    # force new token
uv run python -m scripts.cart_link 89827259 --no-open          # just write the file
uv run python -m scripts.cart_link 89827259 --cart-file ~/Downloads/cart.html
```

> **CRITICAL — DO NOT inline the `url` field into your chat reply.** The
> token is ~600 characters. Most chat UIs truncate URLs of that length,
> which silently breaks the cart handoff (the recipient lands on `/cart`
> with an invalid `access_token` and an empty basket). Always hand off
> via:
>
> 1. `auto_opened: true` — the script already launched the user's
>    browser; just confirm in the reply.
> 2. `cart_file` — short local path (e.g. `/tmp/target-com-shopper/cart-XXX.html`).
>    Tell the user to open that file if the browser didn't launch.
> 3. `shopping_list_markdown` — clickable per-item PDP links as a fallback,
>    in case the auto-merge fails. Each link is short and click-safe.
>
> The skill emits `url_preview` (truncated for logging) and `url_length`
> so you can see at a glance how oversized the raw URL is. The full `url`
> stays in the output for programmatic callers, but treat it as private.

**Treat the URL like a one-time share link.** It contains a bearer token
that grants ~24h of cart-write access. Do not commit it, do not paste it
into long-lived chat history. The skill caches the token under
`$TMPDIR/target-com-shopper/anonymous-token.json` (mode 0600) and reuses it
across calls until ~10 min before expiry.

Output JSON includes `cart_file`, `auto_opened`, `cart_id`, `guest_id`,
`total_cart_item_quantity`, `items_added` (with per-item `title`,
`unit_price`, `current_price`), `items_failed`, `shopping_list_markdown`,
`shopping_list_text`, `token_expires_in_hours`, `url_length`,
`url_preview`, `url_warning`, and `url`. If any TCIN fails to add, it
appears under `items_failed` and the script exits 2.

## Reviews

```bash
uv run python -m scripts.reviews 89827259
```

Returns the **review count and average rating only.** Full review text is
not exposed by `product_review_v1` — point the user at `buy_url` to read
reviews on target.com.

## Environment variables

| Var | Default | Purpose |
| --- | --- | --- |
| `TARGET_API_KEY` | baked-in public key | Override if Target rotates the public web key. Not a secret. |
| `TARGET_DEFAULT_STORE_ID` | `2281` | Fallback store when `--store-id` is omitted. |
| `TARGET_USER_AGENT` | `target-com-shopper-skill/0.1 ...` | UA string sent on every request. |
| `TARGET_HTTP_TIMEOUT` | `10` | Seconds. |
| `TARGET_MIN_INTERVAL` | `1.0` | Minimum seconds between requests (politeness throttle). |
| `TARGET_LIVE_TESTS` | unset | Set to `1` to enable live-network tests. |

## Tests

```bash
uv run pytest                           # offline only (default)
TARGET_LIVE_TESTS=1 uv run pytest -m live -v   # hit the real API
```

## References

- `references/endpoints.md` — every API operation used, required params,
  field-path gotchas.
- `references/categories.md` — curated Target category N-IDs (grocery,
  fresh meat, produce, spices, etc.) for use with `scripts.search --category`.
- `references/status-codes.md` — what 206/400/410/429/5xx mean here.
- `references/tos-and-etiquette.md` — be a polite client.
