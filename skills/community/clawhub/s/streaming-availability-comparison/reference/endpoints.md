# streaming-availability-comparison — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**8 endpoints across 1 platform group(s).**

## JustWatch (8)

### `justwatch_episode_offers`

- **HTTP:** `GET /justwatch/episode/offers`
- **What:** Get JustWatch episode offers. Returns the streaming offers for one JustWatch episode `id` (`tse` followed by digits) across one to five comma-separated country codes in `countries` (default `US`), with `language` defaulting to `en`. Each country entry lists offers by provider, monetization type, presentation type, price and currency, with the episode details. An unknown id returns `404`.
- **Params:** `countries` (string, optional) — One to five comma-separated two-letter country codes; `id` (string, **required**) — Raw JustWatch episode id matching tse[0-9]+; `language` (string, optional) — Two-letter language code

### `justwatch_provider_titles`

- **HTTP:** `GET /justwatch/provider/titles`
- **What:** Get JustWatch provider titles. Returns popular movies and shows available on one streaming provider, by JustWatch provider short name such as `nfx`, for a country (default `US`) and language (default `en`). Filter to movies or shows with `type` and cap results with `limit` (default 20, max 50). Each title has its name, year, type, poster, JustWatch URL and offers with price, currency and monetization type.
- **Params:** `country` (string, optional) — Two-letter country code; `language` (string, optional) — Two-letter language code; `limit` (integer, optional) — Maximum results, defaults to 20 and clamps to 50; `provider` (string, **required**) — JustWatch provider short name; `type` (string, optional) — Title type: all, movie, show

### `justwatch_providers`

- **HTTP:** `GET /justwatch/providers`
- **What:** Get JustWatch providers. Lists the streaming providers JustWatch tracks in a country. `country` is a two-letter code and defaults to `US`. Each provider has its id, clear name, short name, technical name and an absolute icon URL. An invalid country returns `400`.
- **Params:** `country` (string, optional) — Two-letter country code

### `justwatch_search`

- **HTTP:** `GET /justwatch/search`
- **What:** Search JustWatch titles. Searches JustWatch titles. Country must be a two-letter ISO code such as `US`; language must be a two-letter code such as `en`.
- **Params:** `country` (string, optional) — Two-letter country code; `language` (string, optional) — Two-letter language code; `limit` (integer, optional) — Maximum results, defaults to 10 and clamps to 25; `query` (string, **required**) — Search query

### `justwatch_season_episodes`

- **HTTP:** `GET /justwatch/season/episodes`
- **What:** Get JustWatch season episodes. Lists the episodes of a JustWatch season given as `season_id` (`tss` followed by digits), with `country` defaulting to `US` and `language` to `en`. Each episode has its number, title, description and streaming offers with provider, price and currency. Path, URL and poster appear only when JustWatch has them for that episode. An unknown season returns `404`.
- **Params:** `country` (string, optional) — Two-letter country code; `language` (string, optional) — Two-letter language code; `season_id` (string, **required**) — Raw JustWatch season id matching tss[0-9]+

### `justwatch_show_seasons`

- **HTTP:** `GET /justwatch/show/seasons`
- **What:** Get JustWatch show seasons. Lists the seasons of a JustWatch show given as `show_id` (`ts` followed by digits, such as `ts287292`), with `country` defaulting to `US` and `language` to `en`. Each season has its number, title, year, description, path and poster. The show itself comes back with genres, scoring, runtime and offers. An unknown show returns `404`.
- **Params:** `country` (string, optional) — Two-letter country code; `language` (string, optional) — Two-letter language code; `show_id` (string, **required**) — Raw JustWatch show id matching ts[0-9]+

### `justwatch_title_by_id`

- **HTTP:** `GET /justwatch/title/by-id`
- **What:** Get JustWatch title by raw id. Looks up a JustWatch movie or show by its raw `id` (`tm` or `ts` followed by digits, such as `tm92641`), with `country` defaulting to `US` and `language` to `en`. Returns the title, year, genres, runtime, content rating, description, scoring, and offers with provider, monetization type, price and currency. A valid id with no match returns `404`.
- **Params:** `country` (string, optional) — Two-letter country code; `id` (string, **required**) — Raw JustWatch movie/show id matching tm[0-9]+ or ts[0-9]+; `language` (string, optional) — Two-letter language code

### `justwatch_title_offers`

- **HTTP:** `GET /justwatch/title/offers`
- **What:** Get JustWatch title offers. Returns the streaming offers for a JustWatch movie or show `id` across one to five comma-separated country codes in `countries` (default `US`), with `language` defaulting to `en`. Each country entry has its offers (provider, monetization type, presentation type, price, currency) and the title details. An unknown id returns `404`.
- **Params:** `countries` (string, optional) — One to five comma-separated two-letter country codes; `id` (string, **required**) — Raw JustWatch movie/show id matching tm[0-9]+ or ts[0-9]+; `language` (string, optional) — Two-letter language code
