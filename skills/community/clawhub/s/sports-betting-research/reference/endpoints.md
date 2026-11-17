# sports-betting-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**134 endpoints across 4 platform group(s).**

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

## SofaScore (109)

### `sofascore_categories`

- **HTTP:** `GET /sofascore/categories`
- **What:** SofaScore categories for a sport. Returns every category (country or region, such as England or International) SofaScore lists for a sport, with id, name, slug, flag, optional two-letter code, and priority, highest priority first. Use a category `id` with category-tournaments (its competitions) and with scheduled-events (its fixtures on a date). The `sport` enum accepts `american-football`, `aussie-rules`, `badminton`, `bandy`, `baseball`, `basketball`, `beach-volley`, `cricket`, `darts`, `esports`, `floorball`, `football`, `futsal`, `handball`, `ice-hockey`, `mma`, `minifootball`, `padel`, `rugby`, `snooker`, `table-tennis`, `tennis`, `volleyball`, and `waterpolo`. Slugs are not unique across categories, so identify a category by `id`.
- **Params:** `sport` (string, **required**) — Sport key

### `sofascore_category_tournaments`

- **HTTP:** `GET /sofascore/category-tournaments`
- **What:** SofaScore competitions in a category. Returns the competitions (unique tournaments) inside one category, most followed first. Each `id` is the competition id the tournament-seasons, standings, tournament-rounds, and round-events endpoints take. Get the category `id` from the categories endpoint. An empty `tournaments` list is a valid response: some categories exist without any competitions. Returns 404 for an unknown category id.
- **Params:** `id` (string, **required**) — Numeric SofaScore category id from the categories endpoint

### `sofascore_draft`

- **HTTP:** `GET /sofascore/draft`
- **What:** SofaScore league draft. Returns the draft attached to a league season: the upcoming or just-held `draft` and the `previous_draft`, each with its year, start and end time, status, the draft `rounds` (the valid `round` values for draft-picks) and whether the lottery is complete. The `league` enum accepts `nba` and `nfl`. Get `season` from tournament-seasons (NBA competition id 132, NFL 9464). A season without a draft, or a season id that does not belong to the league, returns 404. A season whose draft is not scheduled yet returns only `previous_draft`.
- **Params:** `league` (string, **required**) — League whose draft to return; `season` (string, **required**) — Numeric SofaScore season id of the league

### `sofascore_draft_picks`

- **HTTP:** `GET /sofascore/draft-picks`
- **What:** SofaScore league draft picks. Returns one round of a league draft: each pick with the overall and in-round number, the drafting team, and the drafted prospect (name, position, college or club, top-prospect flag and the player id when SofaScore has one), plus the teams that hold no pick in that round. The `league` enum accepts `nba` (rounds 1 and 2) and `nfl` (rounds 1 to 7); other rounds return 400. Get `year` from the draft endpoint's `draft.year` and `previous_draft.year`; SofaScore keeps only recent drafts, so an older year returns 404. Returns 404 when SofaScore has no picks for that year and round.
- **Params:** `league` (string, **required**) — League whose draft to return; `round` (integer, **required**) — Draft round: 1 to 2 for nba, 1 to 7 for nfl; `year` (string, **required**) — Four-digit draft year

### `sofascore_esports_game`

- **HTTP:** `GET /sofascore/esports-game`
- **What:** SofaScore esports game detail. Returns one resource of one esports game from SofaScore, chosen with `part`: `statistics` (team totals such as kills, towers and barracks for Dota 2, gold and drakes for League of Legends), `lineups` (every player with hero or champion and per-player statistics such as net worth, gold or ADR), `bans` (banned heroes or champions per side) and `rounds` (Counter-Strike round history with outcome, winner and side per round, including overtime). Only the requested block is returned. Get the game id from sofascore-event-esports-games. Statistics and bans exist for Dota 2 and League of Legends only (404 for Counter-Strike), rounds fill for Counter-Strike only (an empty list otherwise) and lineups work for all three. Returns 404 when SofaScore has no such data for the game.
- **Params:** `id` (string, **required**) — Numeric SofaScore esports game id from sofascore-event-esports-games; `part` (string, **required**) — Which resource of the game to return

### `sofascore_event`

- **HTTP:** `GET /sofascore/event`
- **What:** SofaScore event detail. Returns one SofaScore match by event id: home and away teams and scores, status, start time, tournament, attendance and winner code, plus venue and referee when SofaScore has them. An unknown or malformed id surfaces as an upstream error.
- **Params:** `id` (string, **required**) — Numeric SofaScore event (match) id

### `sofascore_event_at_bat_pitches`

- **HTTP:** `GET /sofascore/event-at-bat-pitches`
- **What:** SofaScore event at-bat pitches. Returns every pitch of one baseball at-bat from SofaScore, in pitch order: the ball-strike-out count, outcome code, pitch type and name, speed in kilometres per hour, zone, plate location, strike-zone bounds, batter and pitcher hand, the score, and for balls put in play the hit type, trajectory, hardness and location plus runner movements and fielder credits. Get the at-bat id (`at_bat_id`) from sofascore-event-at-bats for the same event. Returns 404 when SofaScore has no pitches for that at-bat, which includes an at-bat id that does not belong to the event.
- **Params:** `at_bat_id` (string, **required**) — Numeric at-bat id from sofascore-event-at-bats for the same event; `id` (string, **required**) — Numeric SofaScore baseball event (match) id

### `sofascore_event_at_bats`

- **HTTP:** `GET /sofascore/event-at-bats`
- **What:** SofaScore event at-bats. Returns a baseball match's at-bat timeline from SofaScore, in play order: for each plate appearance the inning and half (`top` or `bottom`), pitcher, hitter, their teams, when it ended and the home and away win probabilities before and after it. Use an at-bat `id` with sofascore-event-at-bat-pitches to read its pitches. Returns 404 when SofaScore has no at-bat data for the match, which includes matches that have not started and sports other than baseball.
- **Params:** `id` (string, **required**) — Numeric SofaScore baseball event (match) id

### `sofascore_event_average_positions`

- **HTTP:** `GET /sofascore/event-average-positions`
- **What:** SofaScore event average positions. Returns every player's average position on the pitch during a football match (`average_x` and `average_y` on SofaScore's 0-100 pitch scale, plus the number of touches behind it) for the home and away sides, and the substitutions with their minute. Returns 404 when SofaScore has no positional data for the match, which includes unstarted matches and sports other than football.
- **Params:** `id` (string, **required**) — Numeric SofaScore event (match) id

### `sofascore_event_baseball_top_performers`

- **HTTP:** `GET /sofascore/event-baseball-top-performers`
- **What:** SofaScore event baseball top performers. Returns a baseball match's top performers from SofaScore: each pitcher or batter (`role`) with a rating, their team and a snake_case map of the statistics that earned the mention (for example pitching strike outs, batting home runs and runs batted in). Returns 404 when SofaScore has no top performers for the match, which includes matches that have not started and sports other than baseball.
- **Params:** `id` (string, **required**) — Numeric SofaScore baseball event (match) id

### `sofascore_event_best_players`

- **HTTP:** `GET /sofascore/event-best-players`
- **What:** SofaScore event best players. Returns a match's best-rated players per side, the overall top-rated list, and the player of the match (each with team and value) from SofaScore. Covers football (value is the match rating, label `rating`) and ice hockey (label `pts`, value the points scored; a goalkeeper with no points has no numeric `value` and carries SofaScore's dash in `value_text`). The basketball, baseball and tennis matches checked returned no summary. Returns 404 when SofaScore has no best-players summary for the match, which includes matches that have not started, sports without one and fixtures without rated players.
- **Params:** `id` (string, **required**) — Numeric SofaScore event (match) id

### `sofascore_event_comments`

- **HTTP:** `GET /sofascore/event-comments`
- **What:** SofaScore event commentary. Returns a match's text commentary (minute, type, text, and the players involved, plus the running score on scoring lines) from SofaScore, newest first. Works for football and basketball matches that have commentary. An empty `comments` list is a valid response (a live match with no lines yet). Returns 404 when SofaScore has no commentary for the match, which includes matches that have not started.
- **Params:** `id` (string, **required**) — Numeric SofaScore event (match) id

### `sofascore_event_esports_games`

- **HTTP:** `GET /sofascore/event-esports-games`
- **What:** SofaScore event esports games. Returns the games (maps) of an esports match from SofaScore: each game's id, status, start time, length in seconds, winner, score per side (kills for Dota 2 and League of Legends, rounds with half and overtime split for Counter-Strike), the map for Counter-Strike, and whether complete statistics exist. Use a game `id` with sofascore-esports-game to read its statistics, lineups, bans or rounds. Returns 404 when SofaScore has no games for the event, which includes sports other than esports.
- **Params:** `id` (string, **required**) — Numeric SofaScore esports event (match) id

### `sofascore_event_graph`

- **HTTP:** `GET /sofascore/event-graph`
- **What:** SofaScore event momentum graph. Returns a match's momentum graph as minute and value points (positive values favour the home side) plus period length information, from SofaScore. Covers football, ice hockey and basketball. An empty `points` list is a valid response (a live match that has just started). Returns 404 when SofaScore has no momentum graph for the match, which includes matches that have not started and sports without one such as tennis and baseball.
- **Params:** `id` (string, **required**) — Numeric SofaScore event (match) id

### `sofascore_event_h2h`

- **HTTP:** `GET /sofascore/event-h2h`
- **What:** SofaScore event head-to-head. Returns the historical head-to-head win/draw record between a match's two teams (and managers, when available) from SofaScore.
- **Params:** `id` (string, **required**) — Numeric SofaScore event (match) id

### `sofascore_event_highlights`

- **HTTP:** `GET /sofascore/event-highlights`
- **What:** SofaScore event highlights. Returns the highlight videos attached to a match: title, subtitle (for example `Full Highlights`), video `url`, thumbnail, the publish time, whether it is the key highlight, and the countries it is restricted to when SofaScore limits it. `media_type_code` is SofaScore's own numeric code and is returned untranslated. Returns 404 when the match has no highlight videos, which includes matches that have not finished.
- **Params:** `id` (string, **required**) — Numeric SofaScore event (match) id

### `sofascore_event_incidents`

- **HTTP:** `GET /sofascore/event-incidents`
- **What:** SofaScore event incidents. Returns one match's goal, card, substitution, and period timeline from SofaScore. An empty `incidents` list is a valid response before kickoff.
- **Params:** `id` (string, **required**) — Numeric SofaScore event (match) id

### `sofascore_event_innings`

- **HTTP:** `GET /sofascore/event-innings`
- **What:** SofaScore event innings. Returns a cricket match's innings scorecards from SofaScore. Each innings has the batting and bowling teams, runs, wickets, overs in cricket notation (18.4 is 18 overs and 4 balls), extras (wides, no balls, byes, leg byes, penalty), every batter's line (runs, balls, fours, sixes, dismissal with the bowler and fielder, fall-of-wicket score and over), every bowler's figures (overs, maidens, runs, wickets, wides, no balls), the partnerships and a derived fall-of-wickets list. Works for T20, one-day and Test matches (a Test lists up to four innings). Returns 404 when SofaScore has no innings data for the match, which includes matches that have not started and sports other than cricket.
- **Params:** `id` (string, **required**) — Numeric SofaScore cricket event (match) id

### `sofascore_event_lineups`

- **HTTP:** `GET /sofascore/event-lineups`
- **What:** SofaScore event lineups. Returns one match's starting XI and substitutes per side, with formation. Returns 404 when SofaScore has no lineups for the match. A missing-lineup result may be reused for up to two minutes before checking again.
- **Params:** `id` (string, **required**) — Numeric SofaScore event (match) id

### `sofascore_event_managers`

- **HTTP:** `GET /sofascore/event-managers`
- **What:** SofaScore event managers. Returns the two managers (coaches) of a match with their SofaScore ids, names and slugs. The manager `id` works with the manager and manager-events endpoints. Returns 404 when SofaScore lists no managers for the match, which includes tennis matches.
- **Params:** `id` (string, **required**) — Numeric SofaScore event (match) id

### `sofascore_event_odds`

- **HTTP:** `GET /sofascore/event-odds`
- **What:** SofaScore event odds. Returns one match's betting markets and choices. Returns 404 when SofaScore has no odds for the match.
- **Params:** `id` (string, **required**) — Numeric SofaScore event (match) id

### `sofascore_event_player_heatmap`

- **HTTP:** `GET /sofascore/event-player-heatmap`
- **What:** SofaScore event player heatmap. Returns one player's touch locations in a football match as `points`, each an `x` and `y` on SofaScore's 0-100 pitch scale. Get `player_id` from event-lineups. Returns 404 when SofaScore has no heatmap for that player in that match, which includes players who did not play, unstarted matches and sports other than football.
- **Params:** `id` (string, **required**) — Numeric SofaScore event (match) id; `player_id` (string, **required**) — Numeric SofaScore player id that played in the match

### `sofascore_event_player_statistics`

- **HTTP:** `GET /sofascore/event-player-statistics`
- **What:** SofaScore event player statistics. Returns one player's statistics inside one football match (minutes, rating, passes, duels, shots, expected goals, and more) as a snake_case metric map. The set of metrics depends on the player's position, so absent metrics are omitted rather than zero. Get `player_id` from event-lineups. Returns 404 when SofaScore has no statistics for that player in that match.
- **Params:** `id` (string, **required**) — Numeric SofaScore event (match) id; `player_id` (string, **required**) — Numeric SofaScore player id that took part in the match

### `sofascore_event_point_by_point`

- **HTTP:** `GET /sofascore/event-point-by-point`
- **What:** SofaScore event point-by-point. Returns a racket-sport match's point-by-point timeline, with sets and games in play order. Tennis sets list games and each game lists every point with the running score (`0`, `15`, `30`, `40`, `A`, or a plain count in a tie-break), the server, the game winner, a `description` of `ace` or `double_fault` where SofaScore flags it, and break point (`break_point`) or set or match point (`set_or_match_point`) markers per player. Table tennis and badminton sets list their points directly. The ace flag is a lower bound of the match's real ace count. Darts matches are not covered. Returns 404 when SofaScore has no point-by-point data for the match, which includes matches that have not started and sports without it.
- **Params:** `id` (string, **required**) — Numeric SofaScore event (match) id

### `sofascore_event_pregame_form`

- **HTTP:** `GET /sofascore/event-pregame-form`
- **What:** SofaScore event pre-game form. Returns each side's form going into a match: league position, points (football) or win-loss record (basketball) in `value` with the `label` that names it, the average player rating where SofaScore has one, and the recent results (`W`, `D`, `L`) in the order SofaScore returns them. Covers football and basketball; returns 404 when SofaScore has no pre-game form for the match, which includes tennis matches.
- **Params:** `id` (string, **required**) — Numeric SofaScore event (match) id

### `sofascore_event_shotmap`

- **HTTP:** `GET /sofascore/event-shotmap`
- **What:** SofaScore event shot map. Returns every shot in a football or ice hockey match. Football shots carry the shooter, side, outcome (`shot_type`), situation, body part, expected goals (xG and xGOT), minute, and pitch and goal-mouth coordinates. Ice hockey shots carry the shooter, team, side, shot technique (`shot_type`, for example `wrist`), `outcome` (`made`, `saved`, `missed` or `blocked`), `strength` (`even`, `powerplay` or `shorthanded`), period and period clock, rink `coordinates` and, for most shots, `xg`. An empty `shots` list is a valid response (a live match with no shots yet). Returns 404 when SofaScore has no shot map for the match, which includes matches that have not started, basketball and other sports without one, and fixtures without expected-goals coverage.
- **Params:** `id` (string, **required**) — Numeric SofaScore event (match) id

### `sofascore_event_statistics`

- **HTTP:** `GET /sofascore/event-statistics`
- **What:** SofaScore event statistics. Returns one match's statistics (possession, shots, passes, and more, grouped and split by period). Returns 404 when SofaScore has no tracked statistics for the match.
- **Params:** `id` (string, **required**) — Numeric SofaScore event (match) id

### `sofascore_event_team_heatmap`

- **HTTP:** `GET /sofascore/event-team-heatmap`
- **What:** SofaScore event team heatmap. Returns one team's touch locations in a football match as `player_points` (outfield players) and `goalkeeper_points`, each point an `x` and `y` on SofaScore's 0-100 pitch scale. `team_id` must be the home or away team of the event; get both ids from the event endpoint. Returns 404 when SofaScore has no heatmap for that team in that match, which includes teams that did not play it, unstarted matches and sports other than football.
- **Params:** `id` (string, **required**) — Numeric SofaScore event (match) id; `team_id` (string, **required**) — Numeric SofaScore team id of the home or away side

### `sofascore_event_team_streaks`

- **HTTP:** `GET /sofascore/event-team-streaks`
- **What:** SofaScore event team streaks. Returns a match's team streaks and trends: `general` statements about each side's recent matches (for example `Wins` 6 or `No goals conceded` 4) and `head2head` statements about their meetings. Each item names the streak, a `value` that is either a run length (`6`) or a ratio (`5/5`), the `team` it refers to (`home`, `away` or `both`) and, where SofaScore reports it, whether the streak `continued` into this match. Returns 404 when SofaScore lists no streaks for the match, which includes tennis matches.
- **Params:** `id` (string, **required**) — Numeric SofaScore event (match) id

### `sofascore_event_tennis_power`

- **HTTP:** `GET /sofascore/event-tennis-power`
- **What:** SofaScore event tennis power. Returns a tennis match's per-game momentum series: for each game of each set a `value` (positive favours the home player or team, negative the away side) and whether a break of serve `break_occurred`. An empty `games` list is a valid response (a live match with no completed game yet). Returns 404 when SofaScore has no tennis power data for the match, which includes matches that have not started and sports other than tennis.
- **Params:** `id` (string, **required**) — Numeric SofaScore tennis event (match) id

### `sofascore_event_tv_channels`

- **HTTP:** `GET /sofascore/event-tv-channels`
- **What:** SofaScore event TV channels. Returns where a match is broadcast. `available_countries` lists every country that has a broadcast with its channel ids; those country codes are the valid values for `country`. With `country` set (a two-letter ISO 3166-1 alpha-2 code such as `GB`, any case) the response also resolves that country's `channels` to names, using one extra upstream call. A well-formed country code the match is not broadcast in returns 404, and so does a match with no broadcast information.
- **Params:** `country` (string, optional) — Two-letter ISO 3166-1 alpha-2 country code. Omit to list the broadcasting countries only; `id` (string, **required**) — Numeric SofaScore event (match) id

### `sofascore_event_votes`

- **HTTP:** `GET /sofascore/event-votes`
- **What:** SofaScore event votes. Returns a match's community vote tallies: the match result vote (`match_result` with `home`, `away`, `total` and `draw`, where `draw` is absent for two-way sports such as basketball and tennis), both teams to score, which team scores first and who should have won (when SofaScore has opened that vote). A block that holds no votes is omitted. Returns 404 when SofaScore has no votes for the match.
- **Params:** `id` (string, **required**) — Numeric SofaScore event (match) id

### `sofascore_live_events`

- **HTTP:** `GET /sofascore/live-events`
- **What:** SofaScore live events. Returns currently live events for a sport. The `sport` enum accepts `american-football`, `aussie-rules`, `badminton`, `bandy`, `baseball`, `basketball`, `beach-volley`, `cricket`, `darts`, `esports`, `floorball`, `football`, `futsal`, `handball`, `ice-hockey`, `mma`, `minifootball`, `padel`, `rugby`, `snooker`, `table-tennis`, `tennis`, `volleyball`, and `waterpolo`; the sports endpoint lists them. An empty `events` list is a valid response when nothing is live right now.
- **Params:** `sport` (string, **required**) — Sport key

### `sofascore_manager`

- **HTTP:** `GET /sofascore/manager`
- **What:** SofaScore manager detail. Returns a manager's (coach's) profile (nationality, birth date, preferred formation, current team and teams, and the career win/draw/loss and goals record). Get a manager id from sofascore-search results of type `manager`.
- **Params:** `id` (string, **required**) — Numeric SofaScore manager id

### `sofascore_manager_events`

- **HTTP:** `GET /sofascore/manager-events`
- **What:** SofaScore manager recent matches. Returns a page of the matches a manager (coach) has recently taken charge of, newest first, across all clubs they managed. Only past matches are available; SofaScore publishes no upcoming list for managers. Returns 404 for a page past the end of the manager's history.
- **Params:** `id` (string, **required**) — Numeric SofaScore manager id; `page` (integer, optional) — Zero-based page number

### `sofascore_mma_card`

- **HTTP:** `GET /sofascore/mma-card`
- **What:** SofaScore MMA card. Returns the bouts of one MMA fight card, main event first, narrowed with `part` to `all` bouts, the `maincard`, the `prelims` or the `earlyprelims`. Each bout has the fighters (country, nickname, ranking where 0 is the champion, record), weight class, scheduled rounds, status, and for finished bouts the winner, win type, final round and fight time. Get `org_id` and `card_id` from sofascore-mma-schedule. Returns 404 when the card is unknown or has no bouts in that segment (for example a card without early prelims).
- **Params:** `card_id` (string, **required**) — Numeric card id (card_id) from sofascore-mma-schedule; `org_id` (string, **required**) — Numeric SofaScore MMA organisation id; `part` (string, **required**) — Which segment of the card to return

### `sofascore_mma_schedule`

- **HTTP:** `GET /sofascore/mma-schedule`
- **What:** SofaScore MMA schedule. Returns the main event of every fight card an MMA organisation holds in one calendar month, with the card id and name, fighters (country, nickname, ranking where 0 is the champion, record), weight class, scheduled rounds, status, and for finished fights the winner, win type and final round. Find organisation ids (UFC 19906, PFL 19910, ONE 20269, Rizin 19905, Fight Nation Championship 20463, KSW 19946, OKTAGON 20258, Absolute Championship Akhmat 20254, Cage Warriors 19909, Dana White's Contender Series 20264, Brave CF 20267, Jungle Fight 20253) with sofascore-categories (sport `mma`) and sofascore-category-tournaments (category 1708). Use the `card_id` with sofascore-mma-card to read every bout. Returns 404 when the organisation has no card in that month or the id is not an MMA organisation.
- **Params:** `month` (string, **required**) — Calendar month as YYYY-MM; `org_id` (string, **required**) — Numeric SofaScore MMA organisation id

### `sofascore_odds_dropping`

- **HTTP:** `GET /sofascore/odds-dropping`
- **What:** SofaScore dropping odds. Returns SofaScore's dropping odds list for a sport: about twenty upcoming events whose odds moved most, each as the usual event summary plus the `choice_name` and `percentage` SofaScore reports for the move (returned as supplied) and the market with opening and current prices (`change` is 1 above the opening price, -1 below it, 0 unchanged). The `sport` enum accepts `all` and the SofaScore sport keys; it defaults to `all`. A sport with no qualifying events at the moment (for example esports when probed) returns 404.
- **Params:** `sport` (string, optional) — Sport key, or all for every sport. Defaults to all

### `sofascore_odds_winning`

- **HTTP:** `GET /sofascore/odds-winning`
- **What:** SofaScore winning odds. Returns SofaScore's winning odds list for a sport: about twenty upcoming events whose favourite SofaScore highlights, each as the usual event summary plus `winning_odds` (fractional), the `expected` and `actual` percentages SofaScore reports for it (returned as supplied) and the full-time market with opening and current prices (`change` is 1 above the opening price, -1 below it, 0 unchanged). The `sport` enum accepts `all` and the SofaScore sport keys; it defaults to `all`. A sport with no qualifying events at the moment (for example baseball, cricket and esports when probed) returns 404.
- **Params:** `sport` (string, optional) — Sport key, or all for every sport. Defaults to all

### `sofascore_player`

- **HTTP:** `GET /sofascore/player`
- **What:** SofaScore player detail. Returns one SofaScore player by numeric `id`: name, short name, position, jersey number, date of birth, height, preferred foot, country, market value and currency, and the current team. `deceased` is `true` for historical players. An unknown or malformed id returns an upstream error.
- **Params:** `id` (string, **required**) — Numeric SofaScore player id

### `sofascore_player_attributes`

- **HTTP:** `GET /sofascore/player-attributes`
- **What:** SofaScore player attributes and characteristics. Returns a football player's attribute scores (0 to 100) for the current year and up to three earlier years (`year_shift` 0 to 3), the average scores for the player's position, and the player's characteristics: playing positions plus strengths and weaknesses, each with SofaScore's numeric `code`, a `key` and `name` such as finishing or aerial duels, and a `rank`. Outfield players carry attacking, technical, tactical, defending and creativity scores; goalkeepers carry saves, anticipation, ball_distribution, aerial and tactical. Combines two SofaScore requests. Returns 404 for players without attribute overviews, which includes non-football players.
- **Params:** `id` (string, **required**) — Numeric SofaScore player id

### `sofascore_player_events`

- **HTTP:** `GET /sofascore/player-events`
- **What:** SofaScore player matches with per-match numbers. Returns one page (30 matches) of a player's matches, each with the player's own numbers merged in: `statistics` (football: rating and minutes_played; basketball: points, rebounds, assists and more), `incident_counts` (goals, assists, yellow and red cards, penalty goals), `on_bench` for an unused substitute and `played_for_team_id` (club or national team). Page 0 is the most recent window and can include upcoming fixtures (status type `notstarted`); matches inside a page run oldest first. Follow `has_next_page` for older pages; a page past the end returns 404.
- **Params:** `id` (string, **required**) — Numeric SofaScore player id; `page` (integer, optional) — Zero-based page number. Defaults to 0

### `sofascore_player_last_year_summary`

- **HTTP:** `GET /sofascore/player-last-year-summary`
- **What:** SofaScore player form over the last year. Returns a player's form timeline over roughly the last year: `summary` entries, each with a `type`, a date and (where it applies) a competition. `event` is a rated match (the rating is in `value` as published and as a number in `rating`, the competition in `tournament_id`); `injury` is an injury period whose `value` is an opaque number; `missing` is a match the player missed; `transfer` is a transfer date. `tournaments` describes the competitions referenced. An empty `summary` is a valid response for a player with no rated appearance in the period.
- **Params:** `id` (string, **required**) — Numeric SofaScore player id

### `sofascore_player_national_team_statistics`

- **HTTP:** `GET /sofascore/player-national-team-statistics`
- **What:** SofaScore player national team record. Returns a player's national team record: for each national team the appearances, goals and debut date. An empty `teams` list is a valid response for a player who never played internationally.
- **Params:** `id` (string, **required**) — Numeric SofaScore player id

### `sofascore_player_penalty_history`

- **HTTP:** `GET /sofascore/player-penalty-history`
- **What:** SofaScore player penalty history. Returns the penalties a player has taken, newest first: the totals (`attempts`, `scored`) and, per penalty, the outcome (`goal`, `miss`, `post` or `save`), the zone of the goal (for example `low-right`, `high-left`, `close-high`), the x and y position in the goal mouth on SofaScore's 0 to 100 scale, the expected-goals value when available and the match. Returns 404 for players with no recorded penalties, such as most goalkeepers and defenders.
- **Params:** `id` (string, **required**) — Numeric SofaScore player id

### `sofascore_player_ratings`

- **HTTP:** `GET /sofascore/player-ratings`
- **What:** SofaScore player match ratings for a season. Returns a player's rating in every match of one competition season, newest first, with the opponent, home or away and the match. The `type` enum accepts `overall`, `home`, `away`, `regular_season` and `playoffs` and defaults to `overall`; football seasons answer `overall` and NBA seasons answer `regular_season` and `playoffs` (the types a season offers are listed by player-statistics-seasons). Returns 404 when SofaScore has no ratings of that type for the combination.
- **Params:** `id` (string, **required**) — Numeric SofaScore player id; `season` (string, **required**) — Numeric SofaScore season id from player-statistics-seasons; `tournament_id` (string, **required**) — Numeric SofaScore unique-tournament (competition) id from player-statistics-seasons; `type` (string, optional) — Statistics view

### `sofascore_player_season_heatmap`

- **HTTP:** `GET /sofascore/player-season-heatmap`
- **What:** SofaScore player season heatmap. Returns a football player's aggregated touch locations over one competition season: `points` with an `x`, `y` and touch `count` on SofaScore's 0-100 pitch scale, the number of `matches` behind it and the matched `events`. Get `tournament_id` and `season` from player-statistics-seasons. The response is large for a full league season. Returns 404 when SofaScore has no heatmap for that player, competition and season, which includes sports other than football and seasons the player did not play.
- **Params:** `id` (string, **required**) — Numeric SofaScore player id; `season` (string, **required**) — Numeric SofaScore season id; `tournament_id` (string, **required**) — Numeric SofaScore unique-tournament (competition) id

### `sofascore_player_season_statistics`

- **HTTP:** `GET /sofascore/player-season-statistics`
- **What:** SofaScore player season statistics. Returns a player's statistics for one competition season (appearances, rating, goals, assists, passing, duels, and more) as a snake_case metric map, plus the team and a rating breakdown when available. The `type` enum accepts `overall`, `home`, `away`, `regular_season`, and `playoffs` and defaults to `overall`; only the types listed for that season by player-statistics-seasons exist (football players have `overall`, `home`, `away`; basketball, ice hockey and baseball players have `regular_season` and `playoffs`). Returns 404 when SofaScore has no statistics of that type for the combination.
- **Params:** `id` (string, **required**) — Numeric SofaScore player id; `season` (string, **required**) — Numeric SofaScore season id from player-statistics-seasons; `tournament_id` (string, **required**) — Numeric SofaScore unique-tournament (competition) id from player-statistics-seasons; `type` (string, optional) — Statistics view

### `sofascore_player_statistical_rankings`

- **HTTP:** `GET /sofascore/player-statistical-rankings`
- **What:** SofaScore player ranking among all players in a season. Returns where a football player ranks against every other player of the competition season for about 78 statistics (goals, assists, rating, expected goals, passes, duels, distance covered and more): the `value`, the `rank` (tied values share a rank), the number of ranked players (`count`) and the tie-broken `order`. Statistics are snake_case and sorted alphabetically. The `type` enum accepts only `overall`, which is also the default; the other statistics views answer 404. Returns 404 for players without a ranking in that season, which includes basketball players.
- **Params:** `id` (string, **required**) — Numeric SofaScore player id; `season` (string, **required**) — Numeric SofaScore season id from player-statistics-seasons; `type` (string, optional) — Statistics view

### `sofascore_player_statistics_seasons`

- **HTTP:** `GET /sofascore/player-statistics-seasons`
- **What:** SofaScore player statistics seasons. Lists the competitions and seasons a player has statistics for, with the statistics `types` available for each season. Use a returned competition id (`unique_tournament_id`), season `id` and one of its `types` with player-season-statistics. The `types` values are `overall`, `home`, `away`, `regular_season`, and `playoffs`. Returns 404 for players with no tracked statistics (for example tennis players).
- **Params:** `id` (string, **required**) — Numeric SofaScore player id

### `sofascore_player_tournaments`

- **HTTP:** `GET /sofascore/player-tournaments`
- **What:** SofaScore player competitions. Lists every competition a player has played in, with id, name, slug, category, sport and gender. It includes competitions without season statistics (cups, friendlies, all-star games) that player-statistics-seasons leaves out. Returns 404 when SofaScore has no competitions for the player.
- **Params:** `id` (string, **required**) — Numeric SofaScore player id

### `sofascore_player_transfers`

- **HTTP:** `GET /sofascore/player-transfers`
- **What:** SofaScore player transfer history. Returns a player's transfer history (clubs moved from and to, date, fee, and SofaScore's numeric transfer type code), newest first. An empty `transfers` list is a valid response for a player who has never moved clubs. Returns 404 when SofaScore has no transfer record for the player (seen for ice hockey and baseball players). The `type_code` values are SofaScore's own opaque codes and are not translated.
- **Params:** `id` (string, **required**) — Numeric SofaScore player id

### `sofascore_ranking_types`

- **HTTP:** `GET /sofascore/ranking-types`
- **What:** SofaScore ranking catalogue. Lists every ranking available from the sofascore rankings endpoint: the numeric `type` id, a descriptive name, the sport, the gender and the kind of entity that is ranked (`team`, `player` or `unique_tournament`). Covers 32 rankings across football (league coefficients, FIFA national teams, club coefficients), rugby, tennis (ATP and WTA official and live rankings, UTR), padel and MMA (UFC and Fight Nation Championship divisions). The catalogue is a fixed list and costs no upstream request.
- **Params:** _none_

### `sofascore_rankings`

- **HTTP:** `GET /sofascore/rankings`
- **What:** SofaScore rankings. Returns one SofaScore ranking list: the rank, previous rank, points and the ranked team, player or competition, plus when the list was last updated. Choose the `type` id from sofascore-ranking-types, for example 5 for the ATP men's singles ranking or 2 for the FIFA men's national team ranking. Optional `limit` returns only the first rows of long lists (tennis lists hold 500 rows). MMA division rankings use rank 0 for the reigning champion.
- **Params:** `limit` (integer, optional) — Return only the first N rows, 1 to 500. Omit to return every row; `type` (integer, **required**) — Ranking id from sofascore-ranking-types

### `sofascore_referee`

- **HTTP:** `GET /sofascore/referee`
- **What:** SofaScore referee profile. Returns a referee's profile: name, country, sport, career matches officiated and career yellow, red and yellow-red card totals, plus date of birth and first league debut when SofaScore records them. Get the referee id from the `referee.id` of the sofascore-event endpoint or from a sofascore-search result of type referee. Returns 404 for an unknown id.
- **Params:** `id` (string, **required**) — Numeric SofaScore referee id

### `sofascore_referee_events`

- **HTTP:** `GET /sofascore/referee-events`
- **What:** SofaScore referee officiated matches. Returns one page (30 matches) of the matches a referee officiated, most recent first, across every competition. Follow `has_next_page` for older pages; a page past the end returns 404. Only past matches exist (no upcoming list), and the list includes canceled and postponed fixtures (their `status.type` says so), which the career match total of sofascore-referee does not count.
- **Params:** `id` (string, **required**) — Numeric SofaScore referee id; `page` (integer, optional) — Zero-based page number. Defaults to 0

### `sofascore_referee_statistics`

- **HTTP:** `GET /sofascore/referee-statistics`
- **What:** SofaScore referee card statistics. Returns a referee's record per competition: matches officiated, yellow cards, red cards, yellow-red cards and penalties awarded. The per-competition appearances add up to the career matches in sofascore-referee. An empty `competitions` list is valid for a referee with no recorded competitions.
- **Params:** `id` (string, **required**) — Numeric SofaScore referee id

### `sofascore_round_events`

- **HTTP:** `GET /sofascore/round-events`
- **What:** SofaScore round fixtures. Returns fixtures for one round of a competition season. Get `id` from search or category-tournaments, `season` from tournament-seasons, and the round values from tournament-rounds. Round numbers are not unique in cups, and knockout or named rounds return 404 unless the round's `slug` is passed (plus its `prefix` when tournament-rounds lists one): the UEFA Champions League has a qualifying and a league-phase round 1, and a playoff round 636 both with the `Qualification` prefix and without. Plain numbered league rounds need only `round`. `slug` is lowercase letters, digits, and hyphens (up to 64 characters); `prefix` is letters, digits, spaces, and hyphens (up to 64 characters) and is only valid together with `slug`.
- **Params:** `id` (string, **required**) — Numeric SofaScore unique-tournament (competition) id; `prefix` (string, optional) — Round prefix from tournament-rounds, for example Qualification; only valid together with slug; `round` (integer, **required**) — Round number; `season` (string, **required**) — Numeric SofaScore season id; `slug` (string, optional) — Round slug from tournament-rounds, for example round-of-16; required for knockout and named cup rounds

### `sofascore_scheduled_events`

- **HTTP:** `GET /sofascore/scheduled-events`
- **What:** SofaScore events scheduled in a category on a date. Returns the events (matches) in one category, such as a country, that start on a UTC date, ordered by start time. Get the category `id` from the categories endpoint (or `category_id` from scheduled-tournaments). `date` must be a real calendar date written `YYYY-MM-DD` and is a UTC day; to cover a local day in another timezone, request the neighbouring dates and filter on `start_timestamp`. An empty `events` list is a valid response when the category has no fixtures that day. Returns 404 for an unknown category id.
- **Params:** `category_id` (string, **required**) — Numeric SofaScore category id from the categories endpoint; `date` (string, **required**) — UTC calendar date, YYYY-MM-DD

### `sofascore_scheduled_tournaments`

- **HTTP:** `GET /sofascore/scheduled-tournaments`
- **What:** SofaScore tournaments scheduled on a date. Returns one page of the tournaments that have fixtures on a UTC date for a sport, each with the number of events starting that UTC day. This lists competitions, not matches: use scheduled-events with a tournament's `category_id` for the matches, or its `unique_tournament_id` with the tournament-seasons and round endpoints. `date` must be a real calendar date written `YYYY-MM-DD`. Pages are one-based; follow `has_next_page`. The `sport` enum accepts `american-football`, `aussie-rules`, `badminton`, `bandy`, `baseball`, `basketball`, `beach-volley`, `cricket`, `darts`, `esports`, `floorball`, `football`, `futsal`, `handball`, `ice-hockey`, `mma`, `minifootball`, `padel`, `rugby`, `snooker`, `table-tennis`, `tennis`, `volleyball`, and `waterpolo`. An empty `tournaments` list is a valid response for a date with no fixtures or a page past the last one.
- **Params:** `date` (string, **required**) — UTC calendar date, YYYY-MM-DD; `page` (integer, optional) — One-based page number; defaults to 1; `sport` (string, **required**) — Sport key

### `sofascore_search`

- **HTTP:** `GET /sofascore/search`
- **What:** SofaScore universal search. Searches SofaScore for teams, players, and competitions matching a free-text query. An empty `results` list is a valid response when nothing matches.
- **Params:** `q` (string, **required**) — Free-text search query

### `sofascore_search_typed`

- **HTTP:** `GET /sofascore/search-typed`
- **What:** SofaScore search by entity type. Searches SofaScore for one entity type and returns up to 20 ranked results per page: `events` (matches), `teams`, `players` (with team and position), `managers`, `referees`, `venues` (with city and capacity) and `unique_tournaments` (competitions with category). Page with the zero-based `page`; an empty page means there are no further results. The optional `sport` filter (any key listed by sofascore/sports, such as `football`, `basketball`, `tennis` or `mma`) narrows `teams`, `players`, `managers` and `unique_tournaments`, and is rejected for `events`, `referees` and `venues`, which ignore it. Use the returned ids with the matching endpoints (team, player, manager, venue, tournament-seasons, event).
- **Params:** `page` (integer, optional) — Zero-based page number. Defaults to 0; `q` (string, **required**) — Search text, up to 128 characters; `sport` (string, optional) — Restrict teams, players, managers or unique_tournaments to one sport; `type` (string, **required**) — Entity type to search

### `sofascore_season_events`

- **HTTP:** `GET /sofascore/season-events`
- **What:** SofaScore season fixtures and results. Returns one page (about 30 events) of every fixture or result of a competition season, with the round of each event. The `direction` enum accepts `next` (upcoming fixtures) and `last` (finished results). Follow `has_next_page` to read further pages: a page past the end, a direction with no events (for example `next` in a finished season) and a season id that does not belong to the competition all answer 404. Get `id` from search and `season` from tournament-seasons.
- **Params:** `direction` (string, **required**) — Upcoming fixtures or finished results; `id` (string, **required**) — Numeric SofaScore unique-tournament (competition) id; `page` (integer, optional) — Zero-based page number. Defaults to 0; `season` (string, **required**) — Numeric SofaScore season id

### `sofascore_sports`

- **HTTP:** `GET /sofascore/sports`
- **What:** SofaScore supported sports. Lists every sport key the SofaScore endpoints accept (the `sport` enum of live-events, categories, and scheduled-tournaments), with live and total event counts when available. The list is fixed and always complete; if the live counts cannot be read, `counts_available` is `false` and the per-sport counts are omitted instead of failing the call. Counts are also omitted for a sport the count feed does not cover (for example `mma`). Accepted sport keys: `american-football`, `aussie-rules`, `badminton`, `bandy`, `baseball`, `basketball`, `beach-volley`, `cricket`, `darts`, `esports`, `floorball`, `football`, `futsal`, `handball`, `ice-hockey`, `mma`, `minifootball`, `padel`, `rugby`, `snooker`, `table-tennis`, `tennis`, `volleyball`, `waterpolo`.
- **Params:** _none_

### `sofascore_stage`

- **HTTP:** `GET /sofascore/stage`
- **What:** SofaScore motorsport and cycling stage. Returns one stage from SofaScore's stage hierarchy: a season (Formula 1 2026), an event (a Grand Prix weekend, a NASCAR race, a rally, a cycling race), a session (practice, qualifying, sprint, race) or a cycling stage. The response has its type (`Season`, `Event`, `Practice`, `Qualifying`, `Qualifying part`, `Race`, `Sprint race`, `Sprint qualifying`, `Practice part`, `Stage`), status (`finished`, `notstarted`, `canceled`), start time, country, competition, parent stage (the season of an event, the event of a session), the winner once decided, and circuit, weather and race facts where published (laps, race distance, lap record, safety car, NASCAR cautions, rally special stages, cycling route). `info` fields are omitted when not published, never zero. A season has no status. Stage ids and competition ids are different id spaces. Returns 404 for an unknown stage id.
- **Params:** `id` (string, **required**) — Numeric SofaScore stage id from stage-schedule, stage-seasons or stage-substages

### `sofascore_stage_categories`

- **HTTP:** `GET /sofascore/stage-categories`
- **What:** SofaScore motorsport and cycling categories and competitions. Lists the categories SofaScore keeps for a stage sport, each with its competitions. For `motorsport` that is the racing series (Formula 1, MotoGP, Moto2, Moto3, Superbike, NASCAR with its Cup, Truck and Xfinity competitions, WRC, Formula E, Indycar, DTM); for `cycling` it is Cycling Men and Cycling Women. Use a competition `id` with stage-seasons to list its seasons. Some categories exist without any competition (for example Motocross, Speedway, WEC) and return an empty `competitions` list. Motorsport and cycling are not available on the match-based endpoints (live-events, categories, scheduled-events); they use the stage endpoints. The `sport` enum accepts `motorsport` and `cycling`.
- **Params:** `sport` (string, **required**) — Stage sport key

### `sofascore_stage_driver_performance`

- **HTTP:** `GET /sofascore/stage-driver-performance`
- **What:** SofaScore motorsport race progress per driver. Returns every competitor's progress through a finished race or rally. For circuit races (Formula 1, MotoGP and similar) `laps` lists the position at the end of each lap, starting with lap 0 for the grid, plus the tyre compound and a `pit_stop` flag where published; the lap a driver retired has `retired` set and no position. For rallies `stage_positions` lists the overall position after each special stage. The response also repeats the stage itself. It is published for races and sprints of some series (verified for Formula 1, MotoGP and WRC) and not for practice, qualifying, NASCAR, cycling, events or seasons, which return 404. Returns 404 for an unknown id.
- **Params:** `id` (string, **required**) — Numeric SofaScore stage id of a finished race, sprint or rally

### `sofascore_stage_featured`

- **HTTP:** `GET /sofascore/stage-featured`
- **What:** SofaScore featured motorsport and cycling events. Returns the events SofaScore features for a stage sport right now: a mix of the latest finished events (with `winner` and result facts such as laps and circuit) and the next upcoming ones, across series such as Formula 1, MotoGP, Moto2, Moto3, Superbike, NASCAR and cycling races. Each event carries its competition, season name, parent season stage and country. Use an event `id` with stage-substages for its sessions or stages and stage-standings for results. The `sport` enum accepts `motorsport` and `cycling`.
- **Params:** `sport` (string, **required**) — Stage sport key

### `sofascore_stage_schedule`

- **HTTP:** `GET /sofascore/stage-schedule`
- **What:** SofaScore motorsport and cycling events around a date. Returns the events SofaScore lists for a stage sport around a UTC date: Grand Prix weekends, NASCAR race weekends, rallies and cycling races, each with its country, competition, every session start time (`session_start_timestamps`) and the session SofaScore highlights (`session`: the live, next or latest one). The list is not a strict one-day filter. It holds the events in progress on the date plus the next upcoming ones, and a quiet date still returns the next events; use `on_date`, which is true when a session of the event starts inside the requested UTC day, to separate them. Schedule rows carry no event status or winner: use `session.status`, or pass the event `id` to stage for the event detail and to stage-substages for its sessions. `date` must be a real calendar date written `YYYY-MM-DD`. An empty `stages` list is valid when nothing is in progress or scheduled nearby. The `sport` enum accepts `motorsport` and `cycling`.
- **Params:** `date` (string, **required**) — UTC calendar date, YYYY-MM-DD; `sport` (string, **required**) — Stage sport key

### `sofascore_stage_seasons`

- **HTTP:** `GET /sofascore/stage-seasons`
- **What:** SofaScore seasons of a motorsport or cycling competition. Returns the seasons of one stage competition, newest first, for example Formula 1 2026 (id 214140) back to 1950. A season `id` is a stage id: pass it to stage-substages for the race calendar and to stage-standings for the championship table. The season still in progress has no `end_timestamp`. Get the competition `id` from stage-categories (for example 40 for Formula 1, 17 for MotoGP, 18 for the NASCAR Cup Series, 9 for Cycling Men). Competition ids and stage ids are different id spaces, so a competition id passed to stage returns an unrelated stage. Returns 404 for an unknown competition id.
- **Params:** `id` (string, **required**) — Numeric SofaScore competition id from stage-categories

### `sofascore_stage_standings`

- **HTTP:** `GET /sofascore/stage-standings`
- **What:** SofaScore motorsport and cycling stage standings. Returns one classification of a stage. For a race or sprint it is the result (position, grid, race time, gap, interval, laps, laps led, pit stops, tyre stints, fastest lap, points, retirement status); for practice and qualifying the timing order (`time` is the best lap); for a cycling stage the stage result with time gaps; for an event the event aggregate; for a season the championship table (points, victories, races started, pole positions, podiums, fastest laps; NASCAR adds top 5, top 10 and races not finished). `competitor` returns drivers and riders, `team` returns constructors and teams, which only some seasons and events publish (verified for the Formula 1 and MotoGP seasons and the Formula 1 event; races, NASCAR, WRC and cycling return 404 for `team`). Rows are in upstream order. `position` is omitted for competitors who did not finish or set no time, and `gap` is `DNF` for a retirement. The parent session of a split qualifying has no standings; use the ids of its parts from stage-substages. Fields a classification does not publish are omitted. Returns 404 for an unknown id, a stage that has no results yet, or a kind of stage without that classification. The `type` enum accepts `competitor` and `team`.
- **Params:** `id` (string, **required**) — Numeric SofaScore stage id of a season, event, session or cycling stage; `type` (string, **required**) — Classification kind

### `sofascore_stage_substages`

- **HTTP:** `GET /sofascore/stage-substages`
- **What:** SofaScore children of a motorsport or cycling stage. Returns the children of a stage in upstream order. For a season it is the race calendar: every event with status (`finished`, `notstarted`, `canceled`), dates, round, circuit and winner. For an event it is the sessions: practices, qualifying, sprint qualifying, sprint and race for a Grand Prix, the numbered stages of a cycling race or rally. Qualifying and practice sessions list their `parts`, and the part ids carry the timing results (the parent session of a split qualifying has no standings of its own). Use a child `id` with stage for detail, stage-standings for its results and stage-driver-performance for race progress. A race, session or cycling stage has no children and returns 404, as does an unknown id.
- **Params:** `id` (string, **required**) — Numeric SofaScore stage id of a season or an event

### `sofascore_standings`

- **HTTP:** `GET /sofascore/standings`
- **What:** SofaScore standings. Returns a league table for a competition season. The `type` enum accepts `total`, `home`, and `away`. Get `id` from search and `season` from tournament-seasons.
- **Params:** `id` (string, **required**) — Numeric SofaScore unique-tournament (competition) id; `season` (string, **required**) — Numeric SofaScore season id; `type` (string, **required**) — Standings variant

### `sofascore_team`

- **HTTP:** `GET /sofascore/team`
- **What:** SofaScore team detail. Returns one SofaScore team by numeric `id`: name, short name, country, sport, manager, venue with its city and capacity, primary colour, and national-team flag. `tournament_id` and `tournament_name` give the team's primary competition, such as its domestic league. An unknown id returns an upstream error.
- **Params:** `id` (string, **required**) — Numeric SofaScore team id

### `sofascore_team_achievements`

- **HTTP:** `GET /sofascore/team-achievements`
- **What:** SofaScore team trophies. Returns the trophies a team has won: the total and, per competition, the number won and the winning seasons (newest first, with the season id where SofaScore tracks it). Some competitions, such as US leagues, report a count with an empty or shorter `seasons` list. Returns 404 when SofaScore records no achievements for the team.
- **Params:** `id` (string, **required**) — Numeric SofaScore team id

### `sofascore_team_events`

- **HTTP:** `GET /sofascore/team-events`
- **What:** SofaScore team fixtures. Returns a page of a team's upcoming or recent fixtures. The `direction` enum accepts `next` and `last`. An empty `events` list is a valid response when there is no fixture on that page.
- **Params:** `direction` (string, **required**) — Fixture direction; `id` (string, **required**) — Numeric SofaScore team id; `page` (integer, optional) — Zero-based page number

### `sofascore_team_goal_distributions`

- **HTTP:** `GET /sofascore/team-goal-distributions`
- **What:** SofaScore team goals by match minute. Returns a football team's goals scored and conceded per block of match minutes (1-15, 16-30, 31-45, 46-60, 61-75, 76-90) for one competition season, in three views: `overall`, `home` and `away`, each with the matches played and the goal totals. A block with no goals is returned as 0. Returns 404 for non-football teams and for a team and season that do not belong together.
- **Params:** `id` (string, **required**) — Numeric SofaScore team id; `season` (string, **required**) — Numeric SofaScore season id; `tournament_id` (string, **required**) — Numeric SofaScore unique-tournament (competition) id of a football competition

### `sofascore_team_near_events`

- **HTTP:** `GET /sofascore/team-near-events`
- **What:** SofaScore team previous and next match. Returns a team's last played match and its next scheduled match with teams, competition, status, score and start time. Either side can be missing (a team with no upcoming fixture returns only `previous_event`). Returns 404 when SofaScore has neither. For full fixture lists use team-events.
- **Params:** `id` (string, **required**) — Numeric SofaScore team id

### `sofascore_team_of_the_week`

- **HTTP:** `GET /sofascore/team-of-the-week`
- **What:** SofaScore team of the week. Returns one team of the week: the formation and the selected players with their SofaScore rating, team and, for round and weekly selections, the match the rating was earned in. Get the `period` id from sofascore-team-of-the-week-periods; a period that does not belong to the given competition season is rejected with 400.
- **Params:** `id` (string, **required**) — Numeric SofaScore unique-tournament (competition) id; `period` (string, **required**) — Numeric period id from sofascore-team-of-the-week-periods; `season` (string, **required**) — Numeric SofaScore season id

### `sofascore_team_of_the_week_periods`

- **HTTP:** `GET /sofascore/team-of-the-week-periods`
- **What:** SofaScore team of the week periods. Lists the periods of a competition season for which SofaScore published a team of the week, newest first: league rounds (`round`), weekly time spans (`timespan`) and season-level selections (`season`, such as an NBA regular season or playoff team). Use a returned period `id` with sofascore-team-of-the-week. An empty list is valid when no team of the week has been published yet. Get `id` from search and `season` from tournament-seasons.
- **Params:** `id` (string, **required**) — Numeric SofaScore unique-tournament (competition) id; `season` (string, **required**) — Numeric SofaScore season id

### `sofascore_team_performance`

- **HTTP:** `GET /sofascore/team-performance`
- **What:** SofaScore team recent performance. Returns a team's most recent matches (about ten, oldest first) with SofaScore's per-match performance value in `points`: higher is better and a heavy defeat is negative. An event SofaScore gave no value for has no `points`. An empty `events` list is a valid response for a team with no recent matches.
- **Params:** `id` (string, **required**) — Numeric SofaScore team id

### `sofascore_team_player_statistics`

- **HTTP:** `GET /sofascore/team-player-statistics`
- **What:** SofaScore team player statistics. Returns the statistics of every player in a team's squad for one competition season, each as a snake_case metric map (appearances, minutes, rating, goals, assists, passing and duel metrics for football; points, rebounds and assists for basketball), in SofaScore's order. The `type` enum accepts `overall`, `home`, `away`, `regular_season` and `playoffs` and defaults to `overall`; only the types listed for that season by team-player-statistics-seasons exist (football `overall`, `home`, `away`; NBA `regular_season`, `playoffs`). A metric SofaScore did not record is omitted rather than returned as 0. Returns 404 when SofaScore has no statistics of that type for the combination.
- **Params:** `id` (string, **required**) — Numeric SofaScore team id; `season` (string, **required**) — Numeric SofaScore season id from team-player-statistics-seasons; `tournament_id` (string, **required**) — Numeric SofaScore unique-tournament (competition) id from team-player-statistics-seasons; `type` (string, optional) — Statistics view

### `sofascore_team_player_statistics_seasons`

- **HTTP:** `GET /sofascore/team-player-statistics-seasons`
- **What:** SofaScore team player statistics seasons. Lists the competitions and seasons for which SofaScore has per-player statistics for a team, with the statistics `types` available in each season (`overall`, `home`, `away`, `regular_season`, `playoffs`). Use it to find the `tournament_id`, `season` and `type` accepted by team-player-statistics and team-top-players. Football teams offer `overall`, `home` and `away`; NBA teams offer `regular_season` and `playoffs`. Returns 404 when SofaScore has no player statistics for the team.
- **Params:** `id` (string, **required**) — Numeric SofaScore team id

### `sofascore_team_players`

- **HTTP:** `GET /sofascore/team-players`
- **What:** SofaScore team players. Returns a team's full squad from SofaScore by team id: each player's name, position, jersey number, date of birth, height, country and preferred foot, plus SofaScore's market value estimate and its currency when available.
- **Params:** `id` (string, **required**) — Numeric SofaScore team id

### `sofascore_team_rankings`

- **HTTP:** `GET /sofascore/team-rankings`
- **What:** SofaScore team rankings. Returns every ranking a team or tennis player appears in: for a tennis player the ATP or WTA ranking, its live version and the UTR rating, for a football club the UEFA club coefficient by year. Each ranking carries its `type_id` (the same ids the rankings endpoint takes), name, sport, category and last update, and `rows` with the `position`, `points`, previous and best position where SofaScore reports them. Returns 404 when the id appears in no ranking.
- **Params:** `id` (string, **required**) — Numeric SofaScore team id (a tennis player id for tennis)

### `sofascore_team_season_statistics`

- **HTTP:** `GET /sofascore/team-season-statistics`
- **What:** SofaScore team season statistics. Returns a team's statistics for one competition season (goals, shots, passing, duels, discipline, and the matching conceded-side metrics) as a snake_case metric map. The `type` enum accepts `overall`, `home`, `away`, `regular_season`, and `playoffs` and defaults to `overall`; only the types listed for that season by team-statistics-seasons exist (football teams have `overall` only; basketball, ice hockey and baseball teams have `regular_season` and `playoffs`). Returns 404 when SofaScore has no statistics of that type for the combination.
- **Params:** `id` (string, **required**) — Numeric SofaScore team id; `season` (string, **required**) — Numeric SofaScore season id from team-statistics-seasons; `tournament_id` (string, **required**) — Numeric SofaScore unique-tournament (competition) id from team-statistics-seasons; `type` (string, optional) — Statistics view

### `sofascore_team_statistics_seasons`

- **HTTP:** `GET /sofascore/team-statistics-seasons`
- **What:** SofaScore team statistics seasons. Lists the competitions and seasons a team has statistics for, with the statistics `types` available for each season. Use a returned competition id (`unique_tournament_id`), season `id` and one of its `types` with team-season-statistics. The `types` values are `overall`, `home`, `away`, `regular_season`, and `playoffs`. Returns 404 for teams with no tracked statistics.
- **Params:** `id` (string, **required**) — Numeric SofaScore team id

### `sofascore_team_top_players`

- **HTTP:** `GET /sofascore/team-top-players`
- **What:** SofaScore team top players. Returns a team's best players for every statistic category SofaScore ranks within the team and season (rating, goals, assists, expected goals, tackles, saves and more for football; points, rebounds and assists for basketball), each as a ranked list with player, team and value. The category set depends on the sport, so the response lists every category it holds. The `type` enum accepts `overall`, `regular_season` and `playoffs`: football competitions publish `overall`, the NBA publishes `regular_season` and `playoffs`, and a type the competition does not publish answers 404. Optional `limit` caps the rows per category (up to 50); the payload is large without it.
- **Params:** `id` (string, **required**) — Numeric SofaScore team id; `limit` (integer, optional) — Rows per category, 1 to 50. Omit to return every row; `season` (string, **required**) — Numeric SofaScore season id from team-player-statistics-seasons; `tournament_id` (string, **required**) — Numeric SofaScore unique-tournament (competition) id from team-player-statistics-seasons; `type` (string, optional) — Statistics scope

### `sofascore_team_tournaments`

- **HTTP:** `GET /sofascore/team-tournaments`
- **What:** SofaScore team competitions. Lists the competitions a team plays in, each with id, name, slug, category and sport. By default (`all=false`) it returns the competitions the team currently takes part in; with `all=true` it returns every competition the team has been recorded in, including friendlies and older tournaments. Competition ids can be used as `tournament_id` elsewhere in the SofaScore endpoints; use team-player-statistics-seasons for the seasons that have statistics. Returns 404 when SofaScore has no competitions for the team.
- **Params:** `all` (boolean, optional) — false returns current competitions, true returns every recorded competition; `id` (string, **required**) — Numeric SofaScore team id

### `sofascore_team_transfers`

- **HTTP:** `GET /sofascore/team-transfers`
- **What:** SofaScore team transfers. Returns a team's recent incoming (`transfers_in`) and outgoing (`transfers_out`) transfers with player, clubs, date, fee, and SofaScore's numeric transfer type code. Empty lists are valid for a quiet transfer window. Returns 404 when SofaScore has no transfer record for the team (seen for ice hockey and baseball teams). The `type_code` values are SofaScore's own opaque codes and are not translated.
- **Params:** `id` (string, **required**) — Numeric SofaScore team id

### `sofascore_tennis_player_grand_slam_results`

- **HTTP:** `GET /sofascore/tennis-player-grand-slam-results`
- **What:** SofaScore tennis player grand slam results. Returns a tennis player's best round at each grand slam (Australian Open, Roland Garros, Wimbledon and US Open) for the last five editions: per edition the `year`, the `season_id`, the best `round` reached and whether the player won it (`winner`). A year without a `round` means no result is recorded for that edition. `id` is the SofaScore team id of a tennis player (tennis players are teams in SofaScore); get it from search or rankings. Returns 404 for ids that are not tennis players.
- **Params:** `id` (string, **required**) — Numeric SofaScore team id of a tennis player

### `sofascore_tournament_cuptree`

- **HTTP:** `GET /sofascore/tournament-cuptree`
- **What:** SofaScore competition knockout tree. Returns the knockout tree(s) of a cup or playoff competition season: every round with its ties, each tie's participants (team or player, seed, winner flag, the earlier tie it advanced from), result and score strings (a shoot-out is appended, such as `1 (4)`), match ids and start time, plus the final and third-place tie. Tennis competitions return two trees (main draw and qualifying). League seasons have no tree and answer 404, as does a season id that does not belong to the competition. Get `id` from search or tournaments-with-feature and `season` from tournament-seasons; pass the returned `event_ids` to the event endpoints.
- **Params:** `id` (string, **required**) — Numeric SofaScore unique-tournament (competition) id of a cup or playoff competition; `season` (string, **required**) — Numeric SofaScore season id

### `sofascore_tournament_info`

- **HTTP:** `GET /sofascore/tournament-info`
- **What:** SofaScore competition info. Returns a competition's metadata (name, sport, category, tier, title holder, most titles, current season dates, divisions above and below, linked competitions). When `season` is given it also returns that season's aggregates: number of competitors and, for football competitions, goals, home wins, away wins, draws, yellow and red cards and the promoted teams. Get `id` from search and `season` from tournament-seasons.
- **Params:** `id` (string, **required**) — Numeric SofaScore unique-tournament (competition) id; `season` (string, optional) — Numeric SofaScore season id. Omit for competition metadata only

### `sofascore_tournament_player_of_the_season`

- **HTTP:** `GET /sofascore/tournament-player-of-the-season`
- **What:** SofaScore player of the season. Returns the player SofaScore names player of the season for a finished competition season: the player, their team, shirt number, average rating, appearances and the statistics scope (`overall`, or `regular_season` for the NBA). A season that is still running, has not been awarded, or does not belong to the competition answers 404. Get `id` from search and `season` from tournament-seasons or tournament-winners.
- **Params:** `id` (string, **required**) — Numeric SofaScore unique-tournament (competition) id; `season` (string, **required**) — Numeric SofaScore season id of a finished season

### `sofascore_tournament_player_statistics`

- **HTTP:** `GET /sofascore/tournament-player-statistics`
- **What:** SofaScore season player statistics table. Returns one page of a football competition season's player statistics table, sortable by a statistic. `order` chooses the statistic to sort by, `direction` the sort direction (`desc` or `asc`), `accumulation` whether values are season totals, per-game averages or per-90-minute averages (`total`, `perGame`, `per90`), and `group` which statistic columns each row carries (`summary`, `attack`, `defence`, `passing`, `goalkeeper`). Page with `limit` (up to 100) and `offset`; `has_next_page` shows whether more rows follow. Optional filters narrow the table: `team` (team ids), `nationality` (SofaScore nationality codes), `position` (`G`, `D`, `M`, `F`), `min_appearances` and `min_minutes`; several filters combine (AND) and several values of one filter are alternatives (OR). The team ids and nationality codes of a season come from tournament-statistics-info. A filter that matches nobody returns an empty `players` list. Other sports return no rows (404). Get `id` from search and `season` from tournament-seasons.
- **Params:** `accumulation` (string, optional) — How statistics are accumulated. Defaults to total; `direction` (string, optional) — Sort direction. Defaults to desc; `group` (string, optional) — Statistic columns returned. Defaults to summary; `id` (string, **required**) — Numeric SofaScore unique-tournament (competition) id of a football competition; `limit` (integer, optional) — Rows per page, 1 to 100. Defaults to 20; `min_appearances` (integer, optional) — Keep players with at least this many appearances, 0 to 1000. Omit for no minimum; `min_minutes` (integer, optional) — Keep players with at least this many minutes played, 0 to 100000. Omit for no minimum; `nationality` (array, optional) — Nationality codes to keep, comma separated, up to 20 (codes from tournament-statistics-info); `offset` (integer, optional) — Rows to skip. Defaults to 0; `order` (string, optional) — Statistic to sort by. Defaults to rating; `position` (array, optional) — Position codes to keep, comma separated; `season` (string, **required**) — Numeric SofaScore season id; `team` (array, optional) — Team ids to keep, comma separated, up to 20 (ids from tournament-statistics-info or tournament-teams)

### `sofascore_tournament_rounds`

- **HTTP:** `GET /sofascore/tournament-rounds`
- **What:** SofaScore competition season rounds. Returns the rounds of a competition season and the current round. Round numbers are not unique in cups: the UEFA Champions League has both a qualifying and a league-phase round 1, and the same playoff round number with and without a `prefix`. To fetch a round's fixtures, pass its `round` to round-events together with its `slug` and, when present, its `prefix`; knockout and named rounds return 404 from round-events without the slug. Plain numbered rounds (a league's round 1 to 38) have no slug. Get `id` from category-tournaments or search and `season` from tournament-seasons. Returns 404 when SofaScore has no rounds for the season (for example a season that has not started).
- **Params:** `id` (string, **required**) — Numeric SofaScore unique-tournament (competition) id; `season` (string, **required**) — Numeric SofaScore season id from tournament-seasons

### `sofascore_tournament_seasons`

- **HTTP:** `GET /sofascore/tournament-seasons`
- **What:** SofaScore competition seasons. Returns the season list for a competition. Use a returned season id with the standings and round-events endpoints.
- **Params:** `id` (string, **required**) — Numeric SofaScore unique-tournament (competition) id

### `sofascore_tournament_statistics_info`

- **HTTP:** `GET /sofascore/tournament-statistics-info`
- **What:** SofaScore player statistics table filters. Returns what the tournament-player-statistics table of a football competition season can be filtered by: the season's teams (ids for the `team` filter), the nationality codes (for the `nationality` filter; SofaScore uses `EN`, `SX`, `WA` and `NX` for the home nations), the position codes `G`, `D`, `M` and `F` (for the `position` filter), and the statistic columns of each `group` value (`summary`, `attack`, `defence`, `passing`, `goalkeeper`). Other sports answer 404. Get `id` from search and `season` from tournament-seasons.
- **Params:** `id` (string, **required**) — Numeric SofaScore unique-tournament (competition) id of a football competition; `season` (string, **required**) — Numeric SofaScore season id

### `sofascore_tournament_team_of_the_season`

- **HTTP:** `GET /sofascore/tournament-team-of-the-season`
- **What:** SofaScore team of the season. Returns the team of the season SofaScore selected for a finished competition season: the formation, when it was created and the selected players (11 in football, 5 in basketball) with position, shirt number, team and average rating. A season that is still running, has no selection, or does not belong to the competition answers 404. Get `id` from search and `season` from tournament-seasons or tournament-winners.
- **Params:** `id` (string, **required**) — Numeric SofaScore unique-tournament (competition) id; `season` (string, **required**) — Numeric SofaScore season id of a finished season

### `sofascore_tournament_teams`

- **HTTP:** `GET /sofascore/tournament-teams`
- **What:** SofaScore teams of a competition season. Returns every team (or, for tennis and other individual sports, every player) entered in a competition season, with id, name, short name, name code, country, gender, type (`0` team, `1` individual player) and, for individual players, the current ranking. Use the team ids with team, team-players and the `team` filter of tournament-player-statistics. A season id that does not belong to the competition, or a field not yet decided, answers 404. Get `id` from search and `season` from tournament-seasons.
- **Params:** `id` (string, **required**) — Numeric SofaScore unique-tournament (competition) id; `season` (string, **required**) — Numeric SofaScore season id

### `sofascore_tournament_top_players`

- **HTTP:** `GET /sofascore/tournament-top-players`
- **What:** SofaScore season top players. Returns a competition season's top players for every statistic category SofaScore ranks (for football about 30 categories such as rating, goals, assists, expected goals, tackles and saves; for basketball points, rebounds, assists and more), each with the ranked players, their team and the value. The category set depends on the sport and competition, so the response lists every category it holds. The `type` enum accepts `overall`, `regular_season` and `playoffs`: football competitions publish `overall`, the NBA publishes `regular_season` and `playoffs`, and a type the competition does not publish answers 404. Optional `limit` caps the rows per category (up to 50). Get `id` from search and `season` from tournament-seasons.
- **Params:** `id` (string, **required**) — Numeric SofaScore unique-tournament (competition) id; `limit` (integer, optional) — Rows per category, 1 to 50. Omit to return every row; `season` (string, **required**) — Numeric SofaScore season id; `type` (string, optional) — Statistics scope. Defaults to overall

### `sofascore_tournament_top_teams`

- **HTTP:** `GET /sofascore/tournament-top-teams`
- **What:** SofaScore season top teams. Returns a competition season's top teams for every team statistic category SofaScore ranks (for football about 30 categories such as average rating, goals scored, possession, shots and clean sheets; for basketball points, pace, ratings and more), each with the ranked teams and the value. The category set depends on the sport and competition, so the response lists every category it holds. The `type` enum accepts `overall`, `regular_season` and `playoffs`: football competitions publish `overall`, the NBA publishes `regular_season`, and a type the competition does not publish answers 404. Optional `limit` caps the rows per category (up to 50). Get `id` from search and `season` from tournament-seasons.
- **Params:** `id` (string, **required**) — Numeric SofaScore unique-tournament (competition) id; `limit` (integer, optional) — Rows per category, 1 to 50. Omit to return every row; `season` (string, **required**) — Numeric SofaScore season id; `type` (string, optional) — Statistics scope. Defaults to overall

### `sofascore_tournament_venues`

- **HTTP:** `GET /sofascore/tournament-venues`
- **What:** SofaScore venues of a competition season. Returns every venue used by a competition season with id, name, capacity, city, state (US), coordinates and the `hidden` flag. Use the venue ids with venue and venue-events. A season id that does not belong to the competition answers 404. Get `id` from search and `season` from tournament-seasons.
- **Params:** `id` (string, **required**) — Numeric SofaScore unique-tournament (competition) id; `season` (string, **required**) — Numeric SofaScore season id

### `sofascore_tournament_winners`

- **HTTP:** `GET /sofascore/tournament-winners`
- **What:** SofaScore past winners of a competition. Returns one page (10 seasons, newest first) of a competition's past winners: the year, the season id and the winning team or player. Follow `has_next_page` and pass `page` (zero-based) for older seasons; a page past the last one and an unknown competition both answer 404. Get `id` from search; the returned `season_id` works with every season-scoped endpoint.
- **Params:** `id` (string, **required**) — Numeric SofaScore unique-tournament (competition) id; `page` (integer, optional) — Zero-based page number. Defaults to 0

### `sofascore_tournaments_with_feature`

- **HTTP:** `GET /sofascore/tournaments-with-feature`
- **What:** SofaScore competitions that carry a feature. Returns SofaScore's short list (up to 10) of the most followed competitions of a sport that carry one feature. The `feature` enum accepts `cuptree` (knockout tree, for tournament-cuptree), `standings` (league table), `totw` (team of the week) and `power_rankings`. The `sport` enum accepts `american-football`, `aussie-rules`, `badminton`, `bandy`, `baseball`, `basketball`, `beach-volley`, `cricket`, `darts`, `esports`, `floorball`, `football`, `futsal`, `handball`, `ice-hockey`, `minifootball`, `rugby`, `snooker`, `table-tennis`, `tennis`, `volleyball` and `waterpolo` (`mma` and `padel` are not supported). The list is fixed by SofaScore and cannot be paged or searched; a sport with no such competition returns an empty list. Use search-typed with `type` `unique_tournaments` to find other competitions.
- **Params:** `feature` (string, **required**) — Competition feature; `sport` (string, **required**) — Sport key

### `sofascore_trending_events`

- **HTTP:** `GET /sofascore/trending-events`
- **What:** SofaScore trending events. Returns the events trending in one country across every sport (live, recent and upcoming), each as the usual event summary plus its `sport` key. `country` is a two-letter ISO 3166-1 alpha-2 code such as `GB` or `US` (any case); SofaScore serves a trending list per country, and a code it does not serve returns 404. The list is about twenty events and changes through the day.
- **Params:** `country` (string, **required**) — Two-letter ISO 3166-1 alpha-2 country code

### `sofascore_trending_players`

- **HTTP:** `GET /sofascore/trending-players`
- **What:** SofaScore trending players. Returns a sport's trending top players: standout performers from recent matches with the player, team, the match and that match's numbers as a snake_case metric map (`rating`, `minutes_played`, `goals` and more; the metric set depends on the sport and position). The `sport` enum accepts `football` and `basketball`, the sports for which SofaScore publishes this list. Returns 404 when SofaScore has no trending players for the sport right now.
- **Params:** `sport` (string, **required**) — Sport key

### `sofascore_venue`

- **HTTP:** `GET /sofascore/venue`
- **What:** SofaScore venue. Returns one venue (stadium or arena): name, capacity, city, country, coordinates, its home teams, the venue-wide match totals (matches, goals, home and away win shares, and for football cards and corners per game) and a per-sport record in `sports`, most matches first. `hidden` venues, such as NBA arenas, have no venue-wide match list in venue-events and are listed per competition season instead. An unknown venue id answers 404. Get `id` from search-typed with `type` `venues`, from tournament-venues or from an event's venue.
- **Params:** `id` (string, **required**) — Numeric SofaScore venue id

### `sofascore_venue_events`

- **HTTP:** `GET /sofascore/venue-events`
- **What:** SofaScore matches at a venue. Returns one page (up to 30) of the matches played (`direction` `last`, newest page first) or scheduled (`next`) at a venue, as match summaries. Without `tournament` and `season` it lists every match at the venue, optionally narrowed by `sport` (`all`, or any key listed in the venue's `sports`, such as `football`, `rugby`, `basketball`, `mma`); with both it lists that competition season's matches at the venue and `sport` must be omitted. Hidden venues (see venue) have no venue-wide list and answer 404 without `tournament` and `season`. A direction with no matches, a sport the venue never hosted and a page past the last one also answer 404; follow `has_next_page`.
- **Params:** `direction` (string, **required**) — Upcoming matches or finished matches; `id` (string, **required**) — Numeric SofaScore venue id; `page` (integer, optional) — Zero-based page number. Defaults to 0; `season` (string, optional) — Numeric season id; with tournament, lists that competition season's matches at the venue; `sport` (string, optional) — Sport filter for the venue-wide list. Defaults to all; `tournament` (string, optional) — Numeric unique-tournament id; with season, lists that competition season's matches at the venue

## Flashscore (4)

### `flashscore_match_odds`

- **HTTP:** `GET /flashscore/match-odds`
- **What:** Flashscore match bookmaker odds comparison. Returns bookmaker odds for a match in one viewer market, grouped by betting type and scope with every bookmaker's priced outcomes, opening odds, handicap or total lines, and a selection label. Bookmakers and prices depend on the market, so pick geo (and subdivision for US or CA) from flashscore-odds-geos. A market with no licensed bookmakers returns empty lists. Promotional bonus text is not included.
- **Params:** `betting_type` (string, optional) — Optional filter to one betting type; `geo` (string, optional) — Viewer market country code from flashscore-odds-geos; defaults to GB; `id` (string, **required**) — Eight-character Flashscore match id; `scope` (string, optional) — Optional filter to one scope; `subdivision` (string, optional) — US state (with geo US) or Canadian province (with geo CA) code from flashscore-odds-geos; rejected with any other geo

### `flashscore_odds_geos`

- **HTTP:** `GET /flashscore/odds-geos`
- **What:** Flashscore odds markets, subdivisions and odds enums. Lists every country code accepted by flashscore-match-odds and flashscore-match-tv (with whether bookmakers were found for it when verified), the US states and Canadian provinces that change the bookmaker list, and every betting type, scope and handicap type that can appear in odds responses.
- **Params:** _none_

### `flashscore_team_outright_odds`

- **HTTP:** `GET /flashscore/team-outright-odds`
- **What:** Flashscore team title odds. Returns the title odds bookmakers list for a team in one viewer market, grouped by the competitions it is priced in (league, cup, European competition) with every bookmaker's price and last movement. Pick geo (and subdivision for US or CA) from flashscore-odds-geos. A team with no listed title odds returns empty lists; a player id returns not found.
- **Params:** `geo` (string, optional) — Viewer market country code from flashscore-odds-geos; defaults to GB; `id` (string, **required**) — Eight-character Flashscore team id; `subdivision` (string, optional) — US state (with geo US) or Canadian province (with geo CA) code from flashscore-odds-geos; rejected with any other geo

### `flashscore_tournament_outright_odds`

- **HTTP:** `GET /flashscore/tournament-outright-odds`
- **What:** Flashscore competition winner odds. Returns the title odds bookmakers list for one competition season in one viewer market, grouped by participant with every bookmaker's price and last movement. The provider lists only the top favourites (three in every competition checked), so this is a favourites market, not the full field. Bookmakers depend on the market: pick geo (and subdivision for US or CA) from flashscore-odds-geos. A market with no listed odds returns empty lists. Use the season-level tournament_id from event competition blocks or flashscore-tournament-archive-seasons.
- **Params:** `geo` (string, optional) — Viewer market country code from flashscore-odds-geos; defaults to GB; `subdivision` (string, optional) — US state (with geo US) or Canadian province (with geo CA) code from flashscore-odds-geos; rejected with any other geo; `tournament_id` (string, **required**) — Eight-character season-level tournament id (tournament_id of an event competition block or of a season)
