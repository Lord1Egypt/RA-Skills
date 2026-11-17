# sports-scores-research — endpoint reference — Strava

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**4 endpoints across 1 platform group(s).**

## Strava (4)

### `strava_challenges`

- **HTTP:** `GET /strava/challenges`
- **What:** Strava's public challenge gallery. Returns Strava's public challenge gallery: the currently promoted challenge plus every gallery section (partner challenges, and one section per sport such as run/ride), each with its challenges' goal, duration, and cover art. Public data, sourced from Strava's own challenge gallery.
- **Params:** _none_

### `strava_club`

- **HTTP:** `GET /strava/clubs/{id}`
- **What:** A Strava club's public profile. Returns a Strava club's public profile: name, verified/private flags, location, description, member count, and cover/avatar images. Only the base public profile is returned -- discussion, leaderboard, member list, and recent-activity data require a logged-in Strava session and are not available. Public data, sourced from Strava's own server-rendered club page.
- **Params:** `id` (string, **required**) — Strava club ID

### `strava_route_detail`

- **HTTP:** `GET /strava/routes/detail`
- **What:** A single Strava route's detail page. Returns a single Strava route's detail: type, difficulty, distance, elevation gain, estimated time, and summary. `path` is the relative route path returned by `/strava/routes` results (e.g. `hiking/usa/colorado/boulder/mallory-cave_5171952737974445730`). Public data, sourced from Strava's own server-rendered route pages.
- **Params:** `path` (string, **required**) — Relative route path, from a /strava/routes result's path field

### `strava_routes`

- **HTTP:** `GET /strava/routes`
- **What:** Strava route-index listing for a sport, country, and region. Returns a page of Strava's public route recommendations for a sport, country, and region (state, or state/city). `sport` values: `hiking`, `road-biking`, `mountain-biking`, `trail-running`, `gravel-biking`. Public data, sourced from Strava's own server-rendered route pages.
- **Params:** `country` (string, **required**) — Country slug, e.g. usa; `page` (integer, optional) — Page number, starting at 1; `region` (string, **required**) — Region slug: a state (colorado) or state/city (colorado/boulder); `sport` (string, **required**) — Route sport. Allowed values: hiking, road-biking, mountain-biking, trail-running, gravel-biking
