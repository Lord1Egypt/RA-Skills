# twitch-category-opportunity-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**7 endpoints across 1 platform group(s).**

## Twitch (7)

### `twitch_channel`

- **HTTP:** `GET /twitch/channel`
- **What:** Get a Twitch channel's profile and live status. Returns a Twitch channel's profile (partner status, team, last broadcast title) plus its current live status (started time and game/category, when live).
- **Params:** `login` (string, **required**) — Twitch channel login (the lowercase URL slug, e.g. caedrel for twitch.tv/caedrel)

### `twitch_clips`

- **HTTP:** `GET /twitch/clips`
- **What:** Get a Twitch channel's clips. Returns a Twitch channel's clips (last 7 days), most-viewed first: title, view count, duration, curator, and the game it was recorded under.
- **Params:** `limit` (integer, optional) — Number of clips to return (default 20, max 100); `login` (string, **required**) — Twitch channel login (the lowercase URL slug, e.g. caedrel for twitch.tv/caedrel)

### `twitch_schedule`

- **HTTP:** `GET /twitch/schedule`
- **What:** Get a Twitch channel's broadcast schedule. Returns a Twitch channel's upcoming broadcast schedule -- planned segments with title, start/end time, and game/category -- starting today. A channel with no schedule configured returns an empty segments list, not an error.
- **Params:** `channel` (string, **required**) — Twitch channel login (the lowercase URL slug); `weeks` (integer, optional) — Number of weeks ahead to return, starting today (default 1, max 4)

### `twitch_search`

- **HTTP:** `GET /twitch/search`
- **What:** Search Twitch channels and games/categories. Returns mixed category and channel matches for a query -- live channels include current viewer count and stream title. Sourced from Twitch's own search-typeahead surface (a capped suggestion list, not a fully paginated results page).
- **Params:** `limit` (integer, optional) — Number of results to return (default 10, max 30); `query` (string, **required**) — Search text (category/game name or channel name)

### `twitch_streams`

- **HTTP:** `GET /twitch/streams`
- **What:** Get the top live streams for a Twitch game/category. Returns the top currently-live streams for a Twitch game/category, ranked by viewer count: title, viewer count, broadcaster, and tags.
- **Params:** `game` (string, **required**) — Twitch game/category slug (the lowercase URL slug from twitch.tv/directory/category/{slug}); `limit` (integer, optional) — Number of streams to return (default 20, max 100)

### `twitch_top_games`

- **HTTP:** `GET /twitch/top-games`
- **What:** Get Twitch's top games/categories. Returns the top games/categories site-wide, ranked by total current viewers across all live streams under each one.
- **Params:** `limit` (integer, optional) — Number of games to return (default 20, max 100)

### `twitch_videos`

- **HTTP:** `GET /twitch/videos`
- **What:** Get a Twitch channel's videos (VODs). Returns a Twitch channel's past-broadcast videos (VODs), ranked by view count: title, view count, length, publish date, and the game it was recorded under.
- **Params:** `limit` (integer, optional) — Number of videos to return (default 20, max 100); `login` (string, **required**) — Twitch channel login (the lowercase URL slug, e.g. lck for twitch.tv/lck)
