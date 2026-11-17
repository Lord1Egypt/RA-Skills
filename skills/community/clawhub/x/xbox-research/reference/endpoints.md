# xbox-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**5 endpoints across 1 platform group(s).**

## Xbox (5)

### `xbox_browse`

- **HTTP:** `GET /xbox/browse`
- **What:** Browse the Xbox catalog, with optional sort and filters. Returns one page of the full Xbox storefront catalog (games, add-ons, and subscriptions), optionally sorted and/or filtered. With no sort/filter parameters, returns the store's own default (relevance) order. Multiple values for a repeatable filter (genre, price, platform, subscription, age_rating, multiplayer, technical_features, handheld_compatibility) match ANY of them (logical OR); different filter fields combine as logical AND. Cursor-paginated, fixed at 25 items per page.
- **Params:** `accessibility` (array, optional) — Accessibility-feature filter (repeatable); `age_rating` (array, optional) — ESRB age-rating filter (repeatable); `cursor` (string, optional) — Opaque pagination cursor from a previous response's next_cursor; `genre` (array, optional) — Genre filter (repeatable); `handheld_compatibility` (array, optional) — Handheld compatibility filter (repeatable); `locale` (string, optional) — Display locale (BCP-47); `multiplayer` (array, optional) — Multiplayer-mode filter (repeatable); `platform` (array, optional) — Platform filter (repeatable); `price` (array, optional) — Price-band filter (repeatable); `sort` (string, optional) — Sort order; `subscription` (array, optional) — Subscription filter, by the subscription's own product id (repeatable); `supported_language` (array, optional) — Supported-language filter, by BCP-47 tag (repeatable); `technical_features` (array, optional) — Technical-feature filter (repeatable)

### `xbox_collection`

- **HTTP:** `GET /xbox/collection`
- **What:** Get one page of a curated Xbox collection. Returns one page of a named, editorially curated Xbox collection (e.g. Top Free Games, Top Paid Games, Optimized for Series X|S, Xbox Play Anywhere). Pages forward via an opaque cursor: pass the previous response's next_cursor to fetch the next page. This is a partial, non-exhaustive list of known collection ids -- there is no discovery endpoint for the full set.
- **Params:** `cursor` (string, optional) — Opaque pagination cursor from a previous response's next_cursor; `id` (string, **required**) — Curated collection to fetch; `locale` (string, optional) — Display locale (BCP-47)

### `xbox_game`

- **HTTP:** `GET /xbox/game`
- **What:** Get Xbox catalog details for a single product. Returns Xbox catalog details for a single product id: title, description, publisher, categories, supported platforms, content rating, price, preorder status, media (box art, poster, hero art), trailers, and which subscriptions (e.g. Game Pass) include it.
- **Params:** `locale` (string, optional) — Display locale (BCP-47); `product_id` (string, **required**) — Xbox catalog product id

### `xbox_reviews`

- **HTTP:** `GET /xbox/reviews`
- **What:** Get ratings and reviews for an Xbox catalog product. Returns a product's aggregate star-rating breakdown (average, total, and per-star counts) and up to item_count written reviews, optionally sorted and/or filtered to one star rating. A product with no reviews yet (e.g. a pre-order) returns a null ratings summary and an empty reviews list, not an error.
- **Params:** `item_count` (integer, optional) — Number of reviews to return (1-25); `locale` (string, optional) — Display locale (BCP-47); `order_by` (string, optional) — Review sort order; `product_id` (string, **required**) — Xbox catalog product id; `star_filter` (integer, optional) — Only return reviews with this exact star rating (1-5); omit for all ratings

### `xbox_search`

- **HTTP:** `GET /xbox/search`
- **What:** Search the Xbox catalog, with optional sort and filters. Returns one page of Xbox search results for a keyword, scoped to a category (games, add-ons, or hardware) and optionally sorted/filtered with the same parameters as /xbox/browse. Cursor-paginated.
- **Params:** `accessibility` (array, optional) — Accessibility-feature filter (repeatable); `age_rating` (array, optional) — ESRB age-rating filter (repeatable); `category` (string, optional) — Result category; `cursor` (string, optional) — Opaque pagination cursor from a previous response's next_cursor; `genre` (array, optional) — Genre filter (repeatable); `handheld_compatibility` (array, optional) — Handheld compatibility filter (repeatable); `locale` (string, optional) — Display locale (BCP-47); `multiplayer` (array, optional) — Multiplayer-mode filter (repeatable); `platform` (array, optional) — Platform filter (repeatable); `price` (array, optional) — Price-band filter (repeatable); `query` (string, **required**) — Search keyword; `sort` (string, optional) — Sort order; `subscription` (array, optional) — Subscription filter, by the subscription's own product id (repeatable); `supported_language` (array, optional) — Supported-language filter, by BCP-47 tag (repeatable); `technical_features` (array, optional) — Technical-feature filter (repeatable)
