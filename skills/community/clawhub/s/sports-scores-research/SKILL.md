---
name: sports-scores-research
description: Pulls sports scores, standings, rosters, player/team stats, public sports news, editorial, wiki/video content, and betting odds through the Crawlora API — ESPN, SofaScore, MLB, Strava, DraftKings Sportsbook, Cricinfo, and Sportskeeda. Use for scores/stats or explicitly requested public sports-media research; Strava routes and clubs can reveal location-sensitive patterns.
allowed-tools: Bash(scripts/crawlora.sh:*)
---

# Sports & athletics research

Pull live scoreboards, standings, rosters, player/team stats, sportsbook
odds, and endurance-sport routes/clubs across five sports-data sources as
normalized JSON from the Crawlora API — no scraping scoreboard widgets or
stat pages.

## Tool scope and data flow

The optional shell helper is the only command this skill asks to run. It makes
GET requests only to the documented, allowlisted Crawlora routes. When invoked,
it reads `CRAWLORA_API_KEY` and sends it as an `x-api-key` header over HTTPS to
`api.crawlora.net`; it does not send the key to ESPN, SofaScore, Strava, or
other sports sources. It briefly writes a mode-600 curl config under `TMPDIR`
and removes it when the command exits. It does not inspect other environment
variables, enumerate files, install software, or run with elevated privileges.
Queries, public event/player/team identifiers, and requested routes are sent to
Crawlora; avoid confidential research targets.

In addition to score/stat endpoints, this skill includes public sports editorial,
articles, wikis, quizzes, and video surfaces from Cricinfo and Sportskeeda.
Use those sources only when relevant to the user's request. Strava route and
club lookups can expose location-sensitive training patterns; do not use them
to infer someone's home, routine, or sensitive location history.

## When to use this skill

- "What's the score / status of <game> right now?"
- "Show me <team>'s roster / season stats / standing."
- "What's <player>'s stats this season?"
- "Give me the boxscore / play-by-play for <game>."
- "Head-to-head history between <team A> and <team B>."
- For a detailed post-match football performance brief, use football-match-performance-analysis when installed; this skill remains the general scores/stats entry point.
- League news, rankings/polls, or betting-odds snapshots (where exposed).
- "What are the odds / spread / total for <game>?" or "what are the futures
  odds to win <league>?" (DraftKings Sportsbook).
- "Find running/biking/hiking routes in <region>" or "look up this Strava club."

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **ESPN (most sports/leagues)** — `/espn/scoreboard` for today's/a date's
   games (sport+league params); `/espn/teams` / `/espn/team` for team lists
   and detail; `/espn/team-roster` for rosters; `/espn/standings`;
   `/espn/athlete` for a player; `/espn/game-summary` for one game's
   matchup/odds/boxscore; `/espn/news` and `/espn/rankings` (e.g. AP Top 25)
   round it out.
2. **SofaScore (global soccer-first, many sports)** — `/sofascore/search` to
   resolve a team/player/event id; `/sofascore/live-events` for what's live
   right now; `/sofascore/event` (+ `/event-statistics`, `/event-lineups`,
   `/event-incidents`, `/event-odds`, `/event-h2h`) for one match in depth;
   `/sofascore/standings`, `/sofascore/team`, `/sofascore/team-events`,
   `/sofascore/team-players`, `/sofascore/player`.
3. **MLB** — `/mlb/schedule` for games/scores by date; `/mlb/game` (+
   `/mlb/game-boxscore`, `/mlb/game-play-by-play`) for one game's detail;
   `/mlb/standings`, `/mlb/teams`, `/mlb/team-roster`, `/mlb/team-stats`;
   `/mlb/player` + `/mlb/player-stats`; `/mlb/transactions` for
   signings/trades/IL moves; `/mlb/league-stats` for ranked league leaders.
4. **Strava** — `/strava/routes` (requires `sport` — one of `hiking`,
   `road-biking`, `mountain-biking`, `trail-running`, `gravel-biking` —
   plus `country`+`region` slugs) to browse routes; `/strava/routes/detail`
   (`path`) for one route; `/strava/clubs/{id}` for a club; `/strava/challenges`
   for current public challenges.
5. **DraftKings Sportsbook** — `/draftkings/sportsbook/leagues` to list
   sports/leagues (get a `league_id`), then `/draftkings/sportsbook/odds`
   (`league_id`) for every upcoming event's moneyline/spread/total.
   `/draftkings/sportsbook/live` for live events; `/draftkings/sportsbook/event`
   (+ `/event-markets` with `subcategory_id`) for one event's full market
   detail; `/draftkings/sportsbook/futures` (`league_id`+`subcategory_id`)
   for futures markets. `/draftkings/sportsbook/teams` and `/team` cover
   team lookups.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# ESPN scoreboard + team:
scripts/crawlora.sh /espn/scoreboard sport=basketball league=nba | jq '.'
scripts/crawlora.sh /espn/team-roster sport=basketball league=nba team=lal | jq '.'

# SofaScore live + match detail:
scripts/crawlora.sh /sofascore/live-events sport=football | jq '.'
scripts/crawlora.sh /sofascore/event id=<event-id> | jq '.'

# MLB:
scripts/crawlora.sh /mlb/schedule date=2026-08-10 | jq '.'
scripts/crawlora.sh /mlb/player-stats id=<mlb-id> group=hitting | jq '.'

# Strava:
scripts/crawlora.sh /strava/challenges | jq '.'
scripts/crawlora.sh /strava/routes sport=hiking country=<country-slug> region=<region-slug> | jq '.'

# DraftKings Sportsbook odds:
scripts/crawlora.sh /draftkings/sportsbook/leagues | jq '.'
scripts/crawlora.sh /draftkings/sportsbook/odds league_id=<league-id> | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every ESPN,
SofaScore, MLB, Strava, and DraftKings Sportsbook endpoint this skill uses.

## Examples

- **Live game tracker:** `/espn/scoreboard` or `/sofascore/live-events`
  polled on an interval to report score changes as they happen.
- **Pre-game brief:** `/sofascore/event-h2h` (history) +
  `/draftkings/sportsbook/odds` or `/sofascore/event-odds` (market
  expectation) + both teams' `/sofascore/team-events` (recent form).
- **Post-match performance brief:** use
  `football-match-performance-analysis` when installed for a sourced narrative
  across SofaScore statistics, incidents, and lineups.
- **Season stat leaders:** `/mlb/league-stats` or `/espn/rankings` for
  top performers, then `/mlb/player-stats` / `/espn/athlete` for the detail.
- **Roster/transaction watch:** `/mlb/team-roster` + `/mlb/transactions` to
  track who's been added or dropped this week.
- **Title-odds tracking:** `/draftkings/sportsbook/futures` for a league's
  championship/award odds, compared against `/espn/rankings` for the
  editorial consensus.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public scoreboard/stats pages; odds are informational,
  not a betting service.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **ESPN and SofaScore cover many sports/leagues** via `sport`/`league`
  params — check `reference/endpoints.md` for the accepted values before
  assuming a league is supported.
- Live-score endpoints reflect the source's own update cadence — poll rather
  than assume sub-second freshness.
- **Strava's `country`/`region` are platform-specific slugs**, not free-text
  names — the exact slug format isn't in the tool schema; verify a working
  value at [crawlora.net/docs](https://crawlora.net/docs?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills)
  or the [playground](https://crawlora.net/playground?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills)
  if `/strava/routes` 404s — `/strava/challenges` needs no params and is a
  safe starting point.

## Cricinfo and Sportskeeda editorial and sports data

Cricinfo supplies public cricket scorecards, commentary, profiles, records, and
articles; use its discovery endpoints to identify available tournaments and
series. These are editorial/provider snapshots, not an official league record.

Sportskeeda adds news/articles, author and topic coverage, supported football
and other sports-data surfaces, plus community and media pages. Inspect the endpoint reference for each route's
specific league, section, and identifier requirements; discover options with
`sportskeeda_football_options` before selecting a football view. Editorial depth
charts and news reports are not official roster announcements or live score feeds.
Do not carry ESPN/SofaScore IDs into Sportskeeda.

```sh
scripts/crawlora.sh /sportskeeda/football-options
```

For FotMob player/football analysis use `fotmob-research`; for Flashscore or
LiveScore match lookups use `multi-sport-match-research` when installed. The
bundled helper here retains only the providers in its own endpoint reference.
