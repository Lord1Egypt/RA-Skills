# sports-scores-research — endpoint reference — DraftKings Sportsbook

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**12 endpoints across 1 platform group(s).**

## DraftKings Sportsbook (12)

### `draftkings_event`

- **HTTP:** `GET /draftkings/sportsbook/event`
- **What:** DraftKings Sportsbook event. Returns one event's metadata (league id, sport id, teams, status, start time). `event_id` is a numeric DraftKings event identifier (find it from an event's DraftKings Sportsbook page, or from the `id` field of an event returned by /draftkings/sportsbook/odds). The returned `league_id` is accepted by /draftkings/sportsbook/odds and /draftkings/sportsbook/futures. This endpoint does not include betting markets/odds.
- **Params:** `event_id` (string, **required**) — Numeric DraftKings event id

### `draftkings_event_context`

- **HTTP:** `GET /draftkings/sportsbook/event-context`
- **What:** DraftKings Sportsbook event context. Returns public sport, league, and event navigation identifiers for a numeric DraftKings event id. Use it to associate an event with DraftKings Sportsbook's public sport and league navigation.
- **Params:** `event_id` (string, **required**) — Numeric DraftKings event id

### `draftkings_event_markets`

- **HTTP:** `GET /draftkings/sportsbook/event-markets`
- **What:** DraftKings Sportsbook event markets. Returns one event's betting markets and selections for a specific market category. `event_id` is a numeric DraftKings event identifier (find it from the `id` field of an event returned by /draftkings/sportsbook/odds). `subcategory_id` selects the market category (e.g. game lines, a player-prop category, an alternate-line category) -- find one from the `subcategory_id` field on a market returned by /draftkings/sportsbook/odds. An empty `markets` list is a valid response when the category has no markets currently posted for this event.
- **Params:** `event_id` (string, **required**) — Numeric DraftKings event id; `subcategory_id` (string, **required**) — Numeric DraftKings market subcategory id

### `draftkings_featured_leagues`

- **HTTP:** `GET /draftkings/sportsbook/featured-leagues`
- **What:** DraftKings Sportsbook featured leagues. Returns public DraftKings Sportsbook leagues currently marked as featured in its sport navigation. Each item includes its numeric `id`, capability `tags`, live-offer status, and upstream featured ordering. Use the `id` as `league_id` with /draftkings/sportsbook/odds and /draftkings/sportsbook/futures.
- **Params:** _none_

### `draftkings_futures`

- **HTTP:** `GET /draftkings/sportsbook/futures`
- **What:** DraftKings Sportsbook futures. Returns league-level futures markets and selections for a specific DraftKings market category. `league_id` is a numeric DraftKings league identifier and `subcategory_id` is a numeric futures category identifier. An empty `events` list is a valid response when the category has no markets currently posted for that league.
- **Params:** `league_id` (string, **required**) — Numeric DraftKings league id; `subcategory_id` (string, **required**) — Numeric DraftKings futures market subcategory id

### `draftkings_league_events`

- **HTTP:** `GET /draftkings/sportsbook/league-events`
- **What:** DraftKings Sportsbook league event directory. Returns a DraftKings Sportsbook league's current public event directory, including event IDs, teams or other participants, start times, status, and public availability tags. Supply a numeric `league_id` from /draftkings/sportsbook/leagues, /draftkings/sportsbook/quick-links, /draftkings/sportsbook/featured-leagues, or /draftkings/sportsbook/event. This endpoint does not include betting markets or odds.
- **Params:** `league_id` (string, **required**) — Numeric DraftKings league id

### `draftkings_leagues`

- **HTTP:** `GET /draftkings/sportsbook/leagues`
- **What:** DraftKings Sportsbook sports and leagues. Returns DraftKings Sportsbook's current public sport and league directory. Each league `id` is accepted as `league_id` by /draftkings/sportsbook/odds and /draftkings/sportsbook/futures.
- **Params:** _none_

### `draftkings_live`

- **HTTP:** `GET /draftkings/sportsbook/live`
- **What:** DraftKings Sportsbook live events. Returns the live events currently shown by DraftKings Sportsbook, including score state, period, primary markets, and market categories that can be used with /draftkings/sportsbook/event-markets. An empty `events` list is valid when DraftKings has no live events at request time.
- **Params:** _none_

### `draftkings_odds`

- **HTTP:** `GET /draftkings/sportsbook/odds`
- **What:** DraftKings Sportsbook odds. Returns the primary betting markets (moneyline, spread, total) for every upcoming event in a DraftKings Sportsbook league. `league_id` is a numeric DraftKings league identifier (find it from a league's DraftKings Sportsbook page). An empty `events` list is a valid response when nothing is currently scheduled.
- **Params:** `league_id` (string, **required**) — Numeric DraftKings league id

### `draftkings_quick_links`

- **HTTP:** `GET /draftkings/sportsbook/quick-links`
- **What:** DraftKings Sportsbook quick links. Returns the ordered league shortcuts currently prioritized on DraftKings Sportsbook's public home page. Each item includes a numeric `league_id` accepted by /draftkings/sportsbook/odds and /draftkings/sportsbook/futures.
- **Params:** _none_

### `draftkings_team`

- **HTTP:** `GET /draftkings/sportsbook/team`
- **What:** DraftKings Sportsbook team. Returns stable team metadata embedded in a public DraftKings Sportsbook team page. Supply `team_id`, `sport`, and `slug` from an item returned by /draftkings/sportsbook/teams. Allowed `sport` values: `football`, `hockey`, `basketball`, `baseball`.
- **Params:** `slug` (string, **required**) — Lowercase DraftKings team slug; `sport` (string, **required**) — Sport: football, hockey, basketball, baseball; `team_id` (string, **required**) — Numeric DraftKings team id

### `draftkings_teams`

- **HTTP:** `GET /draftkings/sportsbook/teams`
- **What:** DraftKings Sportsbook league teams. Returns the teams listed on DraftKings Sportsbook's public Teams page for one league. Allowed `league` values: `nfl`, `nhl`, `nba`, `cbb`, `mlb`, `cfb`.
- **Params:** `league` (string, **required**) — League: nfl, nhl, nba, cbb, mlb, cfb
