---
name: twitch-research
description: Pulls structured Twitch data — channel profile and live status, clips, VODs, VOD chat replay, broadcast schedule, team rosters, top games, and search — via the Crawlora API as clean JSON, with no scraping or Twitch API OAuth setup. Use when the user gives a Twitch channel/game/team and wants live status, clips, VODs, chat replay, schedule, or discovery of streamers/categories.
---

# Twitch research

Resolve Twitch channels, games/categories, and teams, and pull live status,
clips, VODs, VOD chat replay, schedules, and search results as normalized
JSON from the Crawlora API — no Twitch developer app, no OAuth, no scraping.

## When to use this skill

- "Is <channel> live right now, and what are they playing?"
- "Get the top clips from <channel>."
- "What did chat say during <VOD>?" / VOD chat replay lookups.
- "What's <channel>'s upcoming schedule?"
- "Who's live in <game/category> right now?" or top games site-wide.
- "Who's on <team>'s roster, and who's currently live?"
- "Search Twitch for a channel or category."

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Resolve the channel login.** A Twitch URL `https://twitch.tv/<login>`
   gives the channel login directly (it's already the lowercase URL slug) —
   no separate id-lookup step is needed.
2. **Profile + live status:** `/twitch/channel login=<login>`.
3. **Content for that channel:** `/twitch/clips login=<login>` (recent
   clips), `/twitch/videos login=<login>` (VODs), `/twitch/schedule
   channel=<login>` (upcoming broadcasts).
4. **VOD chat:** once you have a VOD id (from `/twitch/videos` or a
   `twitch.tv/videos/{id}` URL), page through its chat replay with
   `/twitch/vod-comments video=<id>`, advancing `offset` from the last
   comment's `offset_seconds` to keep paginating.
5. **Team rosters:** `/twitch/team team=<slug>` for a team's members and
   who's currently live.
6. **Discovery** (no channel needed up front): `/twitch/search
   query=<text>` to find channels/games by name; `/twitch/top-games` for
   what's trending site-wide; `/twitch/streams game=<slug>` for the top
   live streams under one game/category.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Channel profile + live status:
scripts/crawlora.sh /twitch/channel login=caedrel | jq '.'

# Clips and VODs for a channel:
scripts/crawlora.sh /twitch/clips login=caedrel limit=10 | jq '.data'
scripts/crawlora.sh /twitch/videos login=lck limit=10 | jq '.'

# Top games, then top streams under one:
scripts/crawlora.sh /twitch/top-games limit=10 | jq '.'
scripts/crawlora.sh /twitch/streams game=league-of-legends limit=10 | jq '.'

# VOD chat replay, paginating by offset_seconds:
scripts/crawlora.sh /twitch/vod-comments video=1234567890 offset=0 | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Twitch
endpoint this skill uses (method, path, params, description).

## Examples

- **Channel digest:** `/twitch/channel` (live status) + `/twitch/clips` +
  `/twitch/schedule` for one login → a single "what's this streamer up to"
  summary.
- **VOD moment-finder:** `/twitch/videos` to find the VOD id →
  `/twitch/vod-comments` starting at `offset=0`, paging forward by the last
  comment's `offset_seconds` → scan chat for reactions around a timestamp.
- **Category browse:** `/twitch/top-games` for the top categories →
  `/twitch/streams game=<slug>` on the one of interest → surface the top
  live streamers under it by viewer count.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public Twitch pages/GraphQL surface; respect
  Twitch's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- `login`/`channel` params are the lowercase URL slug (e.g. `caedrel` for
  `twitch.tv/caedrel`), not a display name — lowercase before calling.
- `/twitch/schedule` returns an empty segments list, not an error, when a
  channel has no schedule configured.
- `/twitch/search` is sourced from Twitch's search-typeahead surface — a
  capped suggestion list (`limit` max 30), not a fully paginated results page.
- `/twitch/vod-comments` paginates by re-requesting with `offset` set to the
  last returned comment's `offset_seconds` — there's no separate page token.
