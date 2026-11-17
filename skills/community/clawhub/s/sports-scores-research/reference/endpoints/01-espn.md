# sports-scores-research — endpoint reference — ESPN

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**9 endpoints across 1 platform group(s).**

## ESPN (9)

### `espn_athlete`

- **HTTP:** `GET /espn/athlete`
- **What:** ESPN athlete. Returns one athlete's bio/overview (name, position, jersey, physicals, current team). The `sport` enum accepts `football`, `basketball`, `baseball`, `hockey`, and `soccer`. The `league` enum accepts `nfl`, `college-football`, `nba`, `wnba`, `mens-college-basketball`, `womens-college-basketball`, `mlb`, `nhl`, `eng.1`, `esp.1`, `ita.1`, `ger.1`, `fra.1`, `usa.1`, and `uefa.champions`; it must be valid for the chosen sport.
- **Params:** `athlete` (string, **required**) — Numeric ESPN athlete (player) id; `league` (string, **required**) — League key (must be valid for the sport); `sport` (string, **required**) — Sport key

### `espn_game_summary`

- **HTTP:** `GET /espn/game-summary`
- **What:** ESPN game summary. Returns one game's matchup, betting odds, and boxscore stat totals. The `sport` enum accepts `football`, `basketball`, `baseball`, `hockey`, and `soccer`. The `league` enum accepts `nfl`, `college-football`, `nba`, `wnba`, `mens-college-basketball`, `womens-college-basketball`, `mlb`, `nhl`, `eng.1`, `esp.1`, `ita.1`, `ger.1`, `fra.1`, `usa.1`, and `uefa.champions`; it must be valid for the chosen sport. Get an `event` id from the scoreboard endpoint.
- **Params:** `event` (string, **required**) — Numeric ESPN event (game) id; `league` (string, **required**) — League key (must be valid for the sport); `sport` (string, **required**) — Sport key

### `espn_news`

- **HTTP:** `GET /espn/news`
- **What:** ESPN league news. Returns recent news articles (headline, description, link) for a league. The `sport` enum accepts `football`, `basketball`, `baseball`, `hockey`, and `soccer`. The `league` enum accepts `nfl`, `college-football`, `nba`, `wnba`, `mens-college-basketball`, `womens-college-basketball`, `mlb`, `nhl`, `eng.1`, `esp.1`, `ita.1`, `ger.1`, `fra.1`, `usa.1`, and `uefa.champions`; it must be valid for the chosen sport.
- **Params:** `league` (string, **required**) — League key (must be valid for the sport); `sport` (string, **required**) — Sport key

### `espn_rankings`

- **HTTP:** `GET /espn/rankings`
- **What:** ESPN poll rankings. Returns poll rankings (e.g. AP Top 25) for a college league. Rankings are only published for college leagues: the `sport` enum accepts `football` and `basketball`, and the `league` enum accepts `college-football`, `mens-college-basketball`, and `womens-college-basketball`.
- **Params:** `league` (string, **required**) — College league key; `sport` (string, **required**) — Sport key

### `espn_scoreboard`

- **HTTP:** `GET /espn/scoreboard`
- **What:** ESPN scoreboard. Returns games (scores, schedule, status, and odds when available) for a sport and league. The `sport` enum accepts `football`, `basketball`, `baseball`, `hockey`, and `soccer`. The `league` enum accepts `nfl`, `college-football`, `nba`, `wnba`, `mens-college-basketball`, `womens-college-basketball`, `mlb`, `nhl`, `eng.1`, `esp.1`, `ita.1`, `ger.1`, `fra.1`, `usa.1`, and `uefa.champions`; it must be valid for the chosen sport. The `seasontype` enum accepts `1` (preseason), `2` (regular season), `3` (postseason), and `4` (offseason).
- **Params:** `dates` (string, optional) — Date or range as YYYYMMDD, YYYYMMDD-YYYYMMDD, or YYYY; defaults to the current scoreboard; `league` (string, **required**) — League key (must be valid for the sport); `seasontype` (integer, optional) — Season type; `sport` (string, **required**) — Sport key; `week` (integer, optional) — Week number (football leagues)

### `espn_standings`

- **HTTP:** `GET /espn/standings`
- **What:** ESPN standings. Returns league standings grouped by conference/division. The `sport` enum accepts `football`, `basketball`, `baseball`, `hockey`, and `soccer`. The `league` enum accepts `nfl`, `college-football`, `nba`, `wnba`, `mens-college-basketball`, `womens-college-basketball`, `mlb`, `nhl`, `eng.1`, `esp.1`, `ita.1`, `ger.1`, `fra.1`, `usa.1`, and `uefa.champions`; it must be valid for the chosen sport. The `seasontype` enum accepts `1` (preseason), `2` (regular season), and `3` (postseason).
- **Params:** `league` (string, **required**) — League key (must be valid for the sport); `season` (integer, optional) — Four-digit season year; defaults to the current season; `seasontype` (integer, optional) — Season type; `sport` (string, **required**) — Sport key

### `espn_team`

- **HTTP:** `GET /espn/team`
- **What:** ESPN team detail. Returns one team's detail (identity, colors, record, standing summary). The `sport` enum accepts `football`, `basketball`, `baseball`, `hockey`, and `soccer`. The `league` enum accepts `nfl`, `college-football`, `nba`, `wnba`, `mens-college-basketball`, `womens-college-basketball`, `mlb`, `nhl`, `eng.1`, `esp.1`, `ita.1`, `ger.1`, `fra.1`, `usa.1`, and `uefa.champions`; it must be valid for the chosen sport.
- **Params:** `league` (string, **required**) — League key (must be valid for the sport); `sport` (string, **required**) — Sport key; `team` (string, **required**) — Team id (numeric) or abbreviation

### `espn_team_roster`

- **HTTP:** `GET /espn/team-roster`
- **What:** ESPN team roster. Returns a team's roster (players with position, jersey, age, and experience) plus head coach. The `sport` enum accepts `football`, `basketball`, `baseball`, `hockey`, and `soccer`. The `league` enum accepts `nfl`, `college-football`, `nba`, `wnba`, `mens-college-basketball`, `womens-college-basketball`, `mlb`, `nhl`, `eng.1`, `esp.1`, `ita.1`, `ger.1`, `fra.1`, `usa.1`, and `uefa.champions`; it must be valid for the chosen sport.
- **Params:** `league` (string, **required**) — League key (must be valid for the sport); `sport` (string, **required**) — Sport key; `team` (string, **required**) — Team id (numeric) or abbreviation

### `espn_teams`

- **HTTP:** `GET /espn/teams`
- **What:** ESPN team list. Returns the full team list for a sport and league. The `sport` enum accepts `football`, `basketball`, `baseball`, `hockey`, and `soccer`. The `league` enum accepts `nfl`, `college-football`, `nba`, `wnba`, `mens-college-basketball`, `womens-college-basketball`, `mlb`, `nhl`, `eng.1`, `esp.1`, `ita.1`, `ger.1`, `fra.1`, `usa.1`, and `uefa.champions`; it must be valid for the chosen sport.
- **Params:** `league` (string, **required**) — League key (must be valid for the sport); `sport` (string, **required**) — Sport key
