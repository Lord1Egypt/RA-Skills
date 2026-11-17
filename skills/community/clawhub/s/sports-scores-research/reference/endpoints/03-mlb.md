# sports-scores-research — endpoint reference — MLB

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**66 endpoints across 1 platform group(s).**

## MLB (66)

### `mlb_discovery`

- **HTTP:** `GET /mlb/discovery`
- **What:** Discover MLB sections and Stats API values. Returns MLB.com's live navigation tree, including hidden nodes labeled with visibility, and the MLB-only value sets for leagues, divisions, game types, roster types, standings types, stat groups, supported stat types, leader categories, MLB Pipeline prospect filters, league-stats hitter positions and player pools, and observed Baseball Savant leaderboard categories and filters including Top Performers, ABS Challenges, Expected Statistics, Outs Above Average, Arm Strength, Arm Value, Home Runs, Percentile Rankings, Pitch Movement, Rolling Windows, Pitcher Arm Angle, Year-to-Year Changes, Catcher Blocking, Catcher Framing, Catcher Throwing, First Base Receiving, and Fielding Run Value. Use these values to discover sections and supported filters before calling MLB endpoints.
- **Params:** _none_

### `mlb_editorial_feed`

- **HTTP:** `GET /mlb/editorial-feed`
- **What:** Get an MLB.com editorial feed. Returns a paginated first-party MLB.com news, video, or selection feed. Slugs are dynamic and not a complete closed topic catalog; discover current topic suggestions with mlb-search and sections with mlb-discovery. Feed items retain upstream Article, ShortContent, VSMContent, or Video fields.
- **Params:** `language` (string, optional) — Feed locale; `limit` (integer, optional) — Items per page (1-100); `skip` (integer, optional) — Number of items to skip (0-100000); `slug` (string, **required**) — MLB feed or selection slug, such as mlb-news-list or sel-vvc-mlb-stories

### `mlb_game`

- **HTTP:** `GET /mlb/game`
- **What:** Get an MLB game feed. Returns an MLB game summary by numeric `id`. The response has the status, both teams with records and score, inning-by-inning runs, probable pitchers, winning, losing and save pitchers, and team box-score totals. It does not include the full play-by-play. Use the play-by-play endpoint for that.
- **Params:** `id` (string, **required**) — Numeric MLB game id

### `mlb_game_boxscore`

- **HTTP:** `GET /mlb/game-boxscore`
- **What:** Get an MLB player boxscore. Returns the player box score for an MLB game by numeric `id`. For the home and away teams it lists each player used with position, batting order and batting, pitching and fielding stats, plus team totals.
- **Params:** `id` (string, **required**) — Numeric MLB game id

### `mlb_game_play_by_play`

- **HTTP:** `GET /mlb/game-play-by-play`
- **What:** Get MLB game play-by-play. Returns the at-bats of an MLB game by numeric `id`. Each play has its inning and half, batter, pitcher, event and description, and a list of individual pitch and event records with timing and pitch data. The response includes a `total` count of plays.
- **Params:** `id` (string, **required**) — Numeric MLB game id

### `mlb_league_leaders`

- **HTTP:** `GET /mlb/league-leaders`
- **What:** Get MLB league leaders. Returns ranked MLB leader entries for one or more validated categories. Use mlb-discovery for all accepted categories, groups, and game type codes.
- **Params:** `categories` (string, **required**) — Comma-separated MLB leader category names; values are listed in mlb-discovery; `game_type` (string, optional) — MLB game type; `group` (string, optional) — Stat group; `league_id` (string, optional) — MLB league id; `limit` (integer, optional) — Leaders per category (1-100); `season` (integer, optional) — Four-digit season; defaults to current year

### `mlb_league_stats`

- **HTTP:** `GET /mlb/league-stats`
- **What:** Get ranked MLB league statistics. Returns ranked MLB stat splits across both leagues. `group` is required (`hitting`, `pitching`, `fielding`, `catching`, `running`, `game`, `team` or `streak`). `season` defaults to the current year and `stat_type` to `season`. Narrow with `league_id`, `team_id`, `position`, `player_pool`, and page with `limit` (1 to 100) and `offset` (0 to 10000).
- **Params:** `end_date` (string, optional) — End date for byDateRange stat types; requires start_date; `game_type` (string, optional) — MLB game type; `group` (string, **required**) — Stat group; `league_id` (string, optional) — MLB league id; `limit` (integer, optional) — Results to return (1-100); `offset` (integer, optional) — Zero-based result offset (0-10000); `opponent_player_id` (string, optional) — Required by vsPlayer stat types; `opponent_team_id` (string, optional) — Required by vsTeam stat types; `player_pool` (string, optional) — Qualified-player pool; `position` (string, optional) — Hitter position; use only with group=hitting; `season` (integer, optional) — Four-digit season; defaults to current year; `start_date` (string, optional) — Start date for byDateRange stat types; requires end_date; `stat_type` (string, optional) — Stats API stat type; defaults to season; `team_id` (string, optional) — Optional MLB team id; discover current team ids with mlb_teams

### `mlb_player`

- **HTTP:** `GET /mlb/player`
- **What:** Get an MLB player. Returns an MLB player by numeric `id`. The response has the full name, position, bats and throws sides, birth date, city and country, current age, height, weight, jersey number, MLB debut date, active flag and current team. Unknown players return `404`.
- **Params:** `id` (string, **required**) — Numeric MLB player id

### `mlb_player_stats`

- **HTTP:** `GET /mlb/player-stats`
- **What:** Get MLB player season statistics. Returns one MLB player's statistics. `id` and `group` (`hitting`, `pitching`, `fielding`, `catching`, `running`, `game`, `team` or `streak`) are required. `season` defaults to the current year and `stat_type` to `season`. Other `stat_type` values cover career, game logs and splits. Use `start_date` with `end_date` for date ranges.
- **Params:** `end_date` (string, optional) — End date for byDateRange stat types; requires start_date; `game_type` (string, optional) — MLB game type; `group` (string, **required**) — Stat group; `id` (string, **required**) — Numeric MLB player id; `opponent_player_id` (string, optional) — Required by vsPlayer stat types; `opponent_team_id` (string, optional) — Required by vsTeam stat types; `season` (integer, optional) — Four-digit season; defaults to current year; `start_date` (string, optional) — Start date for byDateRange stat types; requires end_date; `stat_type` (string, optional) — Stats API stat type; defaults to season

### `mlb_prospect_rankings`

- **HTTP:** `GET /mlb/prospect-rankings`
- **What:** Get MLB Pipeline curated prospect rankings. Returns MLB Pipeline's curated Top 100, Top 30 by Team, Top 10 by Position, Draft Top 200, or International Top 50 ranking. The anonymous first-party page embeds full ranked data. Search, sort, team filtering on Top 100, and pagination are applied to the extracted rows. Use mlb_discovery for the exact view, year, team, position, and sort values.
- **Params:** `limit` (integer, optional) — Rows per page (1-250); `offset` (integer, optional) — Zero-based row offset; `position` (string, optional) — Required for view=position; `q` (string, optional) — Case-insensitive player-name substring; `sort` (string, optional) — Local sort field; `sort_dir` (string, optional) — Local sort direction; `team_filter` (string, optional) — Optional organization filter for view=top100; use a team slug from mlb_discovery.; `team_slug` (string, optional) — Required for view=team; one of the MLB Pipeline team ranking slugs. See mlb_discovery.; `view` (string, optional) — Ranking view; `year` (integer, optional) — Ranking year

### `mlb_prospect_stats`

- **HTTP:** `GET /mlb/prospect-stats`
- **What:** Get MLB Pipeline prospect statistics and rankings. Returns MLB Pipeline prospect stats from the anonymous first-party prospect tables. Supports the Top 100, all-prospect, or one-team list; batter/pitcher views; validated date periods and minimum thresholds; and local name/position filters. Use mlb_discovery for date periods, minimum thresholds, and positions. Team ids come from mlb_teams.
- **Params:** `date_range` (string, optional) — Prospect table period; `limit` (integer, optional) — Rows to return (1-100); `list_type` (string, optional) — Prospect pool; `min_pa` (integer, optional) — Minimum PA threshold; `offset` (integer, optional) — Zero-based row offset; `player_type` (string, optional) — Player table; `position` (string, optional) — Position filter; `q` (string, optional) — Case-insensitive player-name substring; `team_id` (string, optional) — Optional MLB team id; selects that team's prospect list and overrides list_type

### `mlb_schedule`

- **HTTP:** `GET /mlb/schedule`
- **What:** Get the MLB schedule and scores. Returns MLB games, teams, scores, status, probable pitchers, venue, and series information for one date or date range, optionally filtered to a team.
- **Params:** `date` (string, optional) — Single date in YYYY-MM-DD format; `end_date` (string, optional) — Range end in YYYY-MM-DD format; `game_type` (string, optional) — Game type; `start_date` (string, optional) — Range start in YYYY-MM-DD format; `team_id` (string, optional) — Numeric MLB team id

### `mlb_search`

- **HTTP:** `GET /mlb/search`
- **What:** Search MLB players, teams, and content topics. Returns the same anonymous MLB typeahead categories used by MLB.com: player suggestions, team suggestions, content topics, and search terms. Queries need at least three characters.
- **Params:** `q` (string, **required**) — Search text; 3-100 characters

### `mlb_standings`

- **HTTP:** `GET /mlb/standings`
- **What:** Get MLB standings. Returns American League and National League standings, including source-provided expected, home/away, last-ten, ranking, and elimination fields when available, using any supported standings type returned by mlb_discovery.
- **Params:** `date` (string, optional) — Snapshot date in YYYY-MM-DD format; returns standings as of that date; `season` (integer, optional) — Four-digit season; defaults to current year; `type` (string, optional) — Standings type

### `mlb_statcast`

- **HTTP:** `GET /mlb/statcast-leaders`
- **What:** Get Baseball Savant Statcast leaderboard data. Returns the standard anonymous Baseball Savant Statcast leaderboard for batters, pitchers, teams, or pitcher teams. Supports the page's season, team, batter position, minimum batted-ball event, and sortable metric filters, plus local pagination. Use mlb_discovery for exact filter sets. Other Baseball Savant leaderboard pages are listed there but are not represented by this route.
- **Params:** `limit` (integer, optional) — Rows per page (1-500); `min_bbe` (string, optional) — Minimum batted-ball event threshold; `offset` (integer, optional) — Zero-based row offset; `position` (string, optional) — Batter position; `sort` (string, optional) — Sort field; `sort_dir` (string, optional) — Sort direction; `team_id` (string, optional) — Optional MLB team id from mlb_teams; `type` (string, optional) — Leaderboard row type; `year` (integer, optional) — Season; current season back 11 seasons

### `mlb_statcast_abs_challenges`

- **HTTP:** `GET /mlb/statcast-abs-challenges`
- **What:** Get Baseball Savant ABS challenge rankings. Returns Baseball Savant's ABS challenge table with repeated season, game type, split, challenging-team, opponent-team, pitch-type, and shadow-zone filters, plus challenger type, level, thresholds, leverage, pitch location, breakeven, and split-year controls. Filter values are live-verified and listed by /mlb/discovery. The entire filtered table is returned; UI-only drawer details and client-side sorting are not separate source filters.
- **Params:** `ball_strike` (string, optional) — Pitch location; empty selects All; `breakeven` (string, optional) — Challenge breakeven band; empty selects All; `challenge_team_ids` (array, optional) — Challenging MLB team ids; `challenge_type` (string, optional) — Challenge board group; `data_count` (string, optional) — Challenge count or run value; `data_mode` (string, optional) — Challenges made or against; `game_types` (array, optional) — Game type codes; `level` (string, optional) — Competition level; `leverage` (string, optional) — Leverage bucket; empty selects All; `min_challenges` (string, optional) — Minimum challenges made; `min_opponent_challenges` (string, optional) — Minimum challenges against; `opponent_team_ids` (array, optional) — Opponent MLB team ids; `pitch_types` (array, optional) — Pitch type codes; `seasons` (array, optional) — Season values; `shadow_zones` (array, optional) — Shadow zone codes; `split_year` (string, optional) — Separate year groups; `splits` (array, optional) — Split dimensions

### `mlb_statcast_active_spin`

- **HTTP:** `GET /mlb/statcast-active-spin`
- **What:** Get Baseball Savant Active Spin rows. Returns pitcher Active Spin table rows for the selected season/calculation method, minimum pitch count, and throwing hand. Table sorting and pagination are applied locally. The player search only highlights pitchers in the first-party SVG visualization; the SVG chart and CSV download remain outside this JSON table contract.
- **Params:** `hand` (string, optional) — Pitcher throwing hand; omit for both; `limit` (integer, optional) — Rows per page (1-500); `min` (string, optional) — Minimum total pitches; `offset` (integer, optional) — Zero-based row offset; `sort` (string, optional) — Local table sort field; `sort_dir` (string, optional) — Sort direction; `year` (string, optional) — Season and calculation method

### `mlb_statcast_arm_angle`

- **HTTP:** `GET /mlb/statcast-arm-angle`
- **What:** Get Baseball Savant Pitcher Arm Angle rows. Returns Pitcher Arm Angle table rows and the matching MLB-average reference. Supports season, team, game type, pitch type, hand, batter side, pitch-count thresholds, date range, and up to four group-by selectors. Table sorting and pagination run locally. Visualization-only controls, animation, and CSV output are separate formats.
- **Params:** `bat_side` (string, optional) — Batter side; omit for both.; `date_end` (string, optional) — Inclusive end date, YYYY-MM-DD.; `date_start` (string, optional) — Inclusive start date, YYYY-MM-DD.; `game_types` (array, optional) — Game type codes; defaults to R.; `group_by` (array, optional) — Up to four grouping fields.; `limit` (integer, optional) — Rows per page (1-500).; `min` (string, optional) — Minimum total pitches; defaults to q.; `min_group_pitches` (string, optional) — Minimum pitches per group; defaults to 1.; `offset` (integer, optional) — Zero-based row offset (0-5000).; `pitch_hand` (string, optional) — Pitcher throwing hand; omit for both.; `pitch_types` (array, optional) — Pitch type codes; defaults to FF.; `seasons` (array, optional) — Seasons; at most three may be combined. Defaults to 2026.; `sort` (string, optional) — Local table sort field; defaults to arm_angle.; `sort_dir` (string, optional) — Local sort direction; defaults to asc.; `teams` (array, optional) — MLB team ids; omit for all teams.

### `mlb_statcast_arm_strength`

- **HTTP:** `GET /mlb/statcast-arm-strength`
- **What:** Get Baseball Savant Arm Strength leaderboard data. Returns the player or team Arm Strength leaderboard with verified year, team, position metric, minimum throws, local sort, and pagination filters. The player detail route returns individual throw records.
- **Params:** `limit` (integer, optional) — Rows per page (1-500); `min_throws` (string, optional) — Minimum throws; `offset` (integer, optional) — Zero-based row offset; `position` (string, optional) — Position metric; `sort` (string, optional) — Local sort field; `sort_dir` (string, optional) — Sort direction; `team_id` (string, optional) — MLB team id; `type` (string, optional) — Leaderboard row type; `year` (string, optional) — Season or all years

### `mlb_statcast_arm_strength_player`

- **HTTP:** `GET /mlb/statcast-arm-strength-player`
- **What:** Get Baseball Savant player throw details. Returns the individual Arm Strength throw records for one player, by positive `player_id`. `year` can be 2020 to 2026, or `9999` for all years, and defaults to the current verified season. Each throw has its year, fielder id, position, the measured arm-strength value and a play id.
- **Params:** `player_id` (string, **required**) — Positive MLB player id; `year` (string, optional) — Season or all years

### `mlb_statcast_arm_value`

- **HTTP:** `GET /mlb/statcast-arm-value`
- **What:** Get Baseball Savant Extra Bases Run Value leaderboard data. Returns the Arm Value section's complete embedded table, including its Run, Fld, Pit, team, and league views, filters, local sorting, and pagination. Expanded player rows are available from mlb-statcast-arm-value-details. The JSON rows contain the same selected records as the upstream CSV export.
- **Params:** `end_year` (integer, optional) — End season, 2016 through current season; must be >= start_year; `game_type` (string, optional) — Game type; `key_base_out` (string, optional) — Baserunner situation; `limit` (integer, optional) — Rows per page (1-500); `minimum_opps` (string, optional) — Minimum opportunities; `offset` (integer, optional) — Zero-based row offset; `q` (string, optional) — Case- and accent-insensitive local substring on the displayed row name; up to 100 characters; `sort` (string, optional) — Local table sort field; `sort_dir` (string, optional) — Local sort direction; `split` (string, optional) — Return one row per season; `start_year` (integer, optional) — Start season, 2016 through current season; `team_id` (string, optional) — MLB team id from mlb_discovery, split for All Teams Split by Team, or empty for All Teams; `type` (string, optional) — Leaderboard view; `with_team_only` (string, optional) — Team-roster membership for a selected team

### `mlb_statcast_arm_value_details`

- **HTTP:** `GET /mlb/statcast-arm-value-details`
- **What:** Get expanded Baseball Savant Arm Value player plays. Returns the game-level play details displayed when expanding a Run, Fld, or Pit player row in the Arm Value leaderboard. Pass the leaderboard filters used to produce the selected row.
- **Params:** `end_year` (integer, optional) — End season, 2016 through current season; must be >= start_year; `entity_id` (string, **required**) — Positive player id from an Arm Value player row; `game_type` (string, optional) — Game type; `key_base_out` (string, optional) — Baserunner situation; `minimum_opps` (string, optional) — Minimum opportunities; `split` (string, optional) — Split leaderboard records by season; `start_year` (integer, optional) — Start season, 2016 through current season; `team_id` (string, optional) — MLB team id from mlb_discovery, split, or empty; `type` (string, optional) — Player view; `with_team_only` (string, optional) — Team-roster membership for a selected team

### `mlb_statcast_baserunning`

- **HTTP:** `GET /mlb/statcast-baserunning`
- **What:** Get Baseball Savant baserunning leaderboard tables. Returns Baseball Savant Baserunning Run Value, Basestealing, or Extra Bases Taken tables. All filter value sets were read from the live first-party controls; rows are embedded in the page response and searched, sorted, and paged locally. Use mlb_discovery.statcast_baserunning_filters for board-specific groups, thresholds, and sort fields. CSV and visual expansion modes are excluded; this returns the underlying JSON table rows.
- **Params:** `board` (string, **required**) — Baseball Savant table; `game_type` (string, optional) — Game scope; `key_base_out` (string, optional) — Extra Bases Taken situation; `limit` (integer, optional) — Rows per page, 1-500; `n` (string, optional) — Board-specific row threshold; `offset` (integer, optional) — Zero-based row offset; `pitch_hand` (string, optional) — Basestealing pitcher hand; `prior_pk` (string, optional) — Basestealing prior pickoffs; `runner_moved` (string, optional) — Basestealing runner outcome; `search` (string, optional) — Case-insensitive substring in the displayed player or team name; `season_end` (integer, optional) — Inclusive last season; `season_start` (integer, optional) — Inclusive first season; `sort` (string, optional) — Local sort field; accepted values depend on board; `sort_dir` (string, optional) — Local sort direction; `split` (string, optional) — Return separate year rows; `target_base` (string, optional) — Basestealing target base; `team` (string, optional) — MLB team id or split-team rows; `type` (string, optional) — Board group; accepted values depend on board; `with_team_only` (boolean, optional) — Restrict to selected team's active player rows; requires a specific team id

### `mlb_statcast_bat_tracking`

- **HTTP:** `GET /mlb/statcast-bat-tracking`
- **What:** Get Baseball Savant bat-tracking rows. Returns batter, batting-team, pitcher, pitching-team, or league bat-tracking rows with the live page's season, game type, swing threshold, date, side, contact, attack zone, team, pitch, count, and grouping filters. Use mlb_discovery for the same complete value sets. Multi-value filters are passed as repeated query parameters.
- **Params:** `attack_zone` (string, optional) — Attack zone; `bat_side` (string, optional) — Batter side; `contact_type` (string, optional) — Contact type; `counts` (array, optional) — One or more ball-strike counts; `date_end` (string, optional) — Optional date range end in YYYY-MM-DD; `date_start` (string, optional) — Optional date range start in YYYY-MM-DD; `game_type` (string, optional) — Game type; `group_by` (array, optional) — Up to four grouping columns; `is_hard_hit` (string, optional) — Hard-hit filter; `limit` (integer, optional) — Rows per page (1-500); `min_group_swings` (string, optional) — Minimum swings per grouped row; `min_swings` (string, optional) — Minimum swing qualifier; `offset` (integer, optional) — Zero-based row offset; `pitch_hand` (string, optional) — Pitcher hand; `pitch_types` (array, optional) — One or more pitch types; `season_end` (string, optional) — Last season; must be >= season_start; `season_start` (string, optional) — First season; `sort` (string, optional) — Local row sort field; `sort_dir` (string, optional) — Sort direction; `teams` (array, optional) — One or more MLB team ids; `type` (string, optional) — Table row type

### `mlb_statcast_batted_ball`

- **HTTP:** `GET /mlb/statcast-batted-ball`
- **What:** Get Baseball Savant Batted Ball Profile rows. Returns the Batted Ball Profile table for batters, batting teams, pitchers, pitching teams, or league totals. Supports first-party season, game type, split, team, date, side, hand, pitch type, event threshold, and split-group threshold filters. The All-Star A game type is accepted by the live page query although its checkbox is hidden. Sorting and pagination are local. The league-average reference row is returned separately when requested; CSV and visualization controls are outside this JSON contract.
- **Params:** `bat_side` (string, optional) — Batter side; `date_end` (string, optional) — YYYY-MM-DD date range end (2015-04-05 through today); `date_start` (string, optional) — YYYY-MM-DD date range start (2015-04-05 through today); `game_types` (array, optional) — One or more game type codes; `include_league_average` (boolean, optional) — Include the first-party league-average reference row; `limit` (integer, optional) — Rows per page (1-500); `min` (string, optional) — Minimum batted-ball events; `min_split` (string, optional) — Minimum rows per split group; `offset` (integer, optional) — Zero-based row offset; `pitch_hand` (string, optional) — Pitcher throwing hand; `pitch_types` (array, optional) — One or more pitch type codes; `seasons` (array, optional) — One or more seasons; `sort` (string, optional) — Local table sort field; `sort_dir` (string, optional) — Sort direction; `split_year` (string, optional) — Split seasons into separate rows; `splits` (array, optional) — One or more split dimensions; `teams` (array, optional) — One or more MLB team ids; `type` (string, optional) — Row type

### `mlb_statcast_birthday_index`

- **HTTP:** `GET /mlb/statcast-birthday-index`
- **What:** Get Baseball Savant Sarah Langs Birthday Index rows. Returns today's birthday tables for batters and pitchers plus the selected upcoming-birthday table. Type and minimum-games are first-party filters; date must fall inside the live page's season date range. The active-player toggle, sorting, and pagination are applied locally. The MLB Terms of Use notes a private, non-commercial-use boundary and restrictions on redistribution; this endpoint exposes statistical rows only and excludes media, graphics, and CSV.
- **Params:** `date` (string, optional) — Optional birthday date in M-D form; accepted dates are bounded by the current live page season window; `limit` (integer, optional) — Rows per page (1-500); `min_games` (string, optional) — Minimum games played on the birthday; `offset` (integer, optional) — Zero-based row offset (0-5000); `show_inactives` (boolean, optional) — Include inactive and deceased players in upcoming rows; `sort` (string, optional) — Local sort column. Some values are type- or date-specific and invalid combinations are rejected.; `sort_dir` (string, optional) — Local sort direction; omitted values use the selected column's live first-party initial direction; `type` (string, optional) — Upcoming table

### `mlb_statcast_catcher_blocking`

- **HTTP:** `GET /mlb/statcast-catcher-blocking`
- **What:** Get Baseball Savant Catcher Blocking leaderboard rows. Returns catcher, pitcher, catching-team, or league Catcher Blocking rows. Filters cover game type, season range, minimum opportunities, team/stint, and local table sorting. Use mlb_discovery for the exact filter sets. Row detail events are available from mlb-statcast-catcher-blocking-details; chart playback and CSV export controls are not data rows.
- **Params:** `end_year` (integer, optional) — Last season, start_year through current season; `game_type` (string, optional) — Game type; `limit` (integer, optional) — Rows per page (1-500); `min` (string, optional) — Minimum opportunities; applies to Cat and Pit; `offset` (integer, optional) — Zero-based row offset; `sort` (string, optional) — Local sort field from mlb_discovery; `sort_dir` (string, optional) — Local sort direction; `split` (string, optional) — Split rows by season; `start_year` (integer, optional) — First season, 2018 through current season; `team` (string, optional) — Optional team filter: split or an MLB team id from mlb_discovery; `type` (string, optional) — Leaderboard group; `with_team_only` (boolean, optional) — For a specific Cat or Pit team, include only rows for that team; defaults true

### `mlb_statcast_catcher_blocking_details`

- **HTTP:** `GET /mlb/statcast-catcher-blocking-details`
- **What:** Get Baseball Savant Catcher Blocking play details. Expands a Catcher Blocking Cat, Pit, or Pitching Team table row into paginated play-location events. entity_id must come from the matching leaderboard rows and other filters must match that row query. League rows have no detail feed.
- **Params:** `end_year` (integer, optional) — Last season, start_year through current season; `entity_id` (string, **required**) — Entity id from a Cat, Pit, or Pitching Team leaderboard row; `game_type` (string, optional) — Game type; `limit` (integer, optional) — Rows per page (1-500); `offset` (integer, optional) — Zero-based row offset; `split` (string, optional) — Split details by season; `start_year` (integer, optional) — First season, 2018 through current season; `team` (string, optional) — Optional team id or split selector from mlb_discovery; `type` (string, optional) — Row group; `with_team_only` (boolean, optional) — For a specific Cat or Pit team, include only rows for that team; defaults true

### `mlb_statcast_catcher_framing`

- **HTTP:** `GET /mlb/statcast-catcher-framing`
- **What:** Get Baseball Savant Catcher Framing leaderboard rows. Returns the Catcher Framing table for catcher, catching-team, batter, batting-team, pitcher, or league groups. Supports observed game, season, one-team, pitch/result minimum, date, bat-side, pitch-hand, pitch-type, ball/strike, and call-model filters, plus local sort and pagination. Use mlb_discovery for exact enum values; chart-only groupings and player comparison controls are excluded.
- **Params:** `ball_strike` (string, optional) — Pitch location relative to strike zone; `bat_side` (string, optional) — Batter side; `call` (string, optional) — Framing model; `date_end` (string, optional) — Inclusive end date; `date_start` (string, optional) — Inclusive start date; `game_type` (string, optional) — Game type; `limit` (integer, optional) — Rows per page (1-500); `min_pitches` (string, optional) — Minimum pitches; `min_results` (integer, optional) — Minimum results; `offset` (integer, optional) — Zero-based row offset; `pitch_hand` (string, optional) — Pitcher hand; `pitch_type` (string, optional) — Single pitch type; `season_end` (integer, optional) — Last season; `season_start` (integer, optional) — First season; `sort` (string, optional) — Local sort field; `sort_dir` (string, optional) — Local sort direction; `team` (string, optional) — Optional single MLB team id; `type` (string, optional) — Table group

### `mlb_statcast_catcher_framing_details`

- **HTTP:** `GET /mlb/statcast-catcher-framing-details`
- **What:** Get Baseball Savant Catcher Framing pitch-event details. Returns paginated pitch events for a Catcher Framing entity_id. Repeat the leaderboard filters used to obtain the entity; league aggregate rows have no detail feed. The upstream detail response may be large, so use limit and offset.
- **Params:** `ball_strike` (string, optional) — Pitch location relative to strike zone; `bat_side` (string, optional) — Batter side; `call` (string, optional) — Framing model; `date_end` (string, optional) — Inclusive end date; `date_start` (string, optional) — Inclusive start date; `entity_id` (string, **required**) — Entity id from a Catcher Framing leaderboard row; `game_type` (string, optional) — Game type; `limit` (integer, optional) — Rows per page (1-500); `min_pitches` (string, optional) — Minimum pitches; `min_results` (integer, optional) — Minimum results; `offset` (integer, optional) — Zero-based row offset; `pitch_hand` (string, optional) — Pitcher hand; `pitch_type` (string, optional) — Single pitch type; `season_end` (integer, optional) — Last season; `season_start` (integer, optional) — First season; `team` (string, optional) — Optional single MLB team id; `type` (string, optional) — Table group; league details are unavailable

### `mlb_statcast_catcher_pop_time`

- **HTTP:** `GET /mlb/statcast-catcher-pop-time`
- **What:** Get Baseball Savant Catcher Pop Time leaderboard. Returns catchers ranked by pop-time metrics, filtered by season, team, and minimum steal attempts to second or third. Sort and pagination are applied locally.
- **Params:** `limit` (integer, optional) — Rows to return (1-500); `min2b` (string, optional) — Minimum attempts to second base; `min3b` (string, optional) — Minimum attempts to third base; `offset` (integer, optional) — Zero-based offset; `sort` (string, optional) — Sort field from mlb_discovery; `sort_dir` (string, optional) — Sort direction; `team_id` (string, optional) — MLB team id; `year` (string, optional) — Season from 2015 through 2026

### `mlb_statcast_catcher_stance`

- **HTTP:** `GET /mlb/statcast-catcher-stance`
- **What:** Get Baseball Savant Catcher Stance rows. Returns the public Catcher Stance table for catchers, catching teams, batters, batting teams, pitchers, or league totals. Supports the live year, game, date, threshold, team, pitch type, batter/pitcher hand, knee posture, grouping, sorting, and pagination controls. Grouping accepts up to four values. Use mlb_discovery for exact value sets. Chart series and page-local search/column toggles are not included.
- **Params:** `bat_side` (string, optional) — Batter side; omit for all; `date_end` (string, optional) — End date YYYY-MM-DD; `date_start` (string, optional) — Start date YYYY-MM-DD; `game_type` (string, optional) — Game type; `group_by` (array, optional) — Up to four grouping dimensions; none disables grouping; `knee_code` (string, optional) — Knee posture; `limit` (integer, optional) — Rows per page (1-500); `min_pitches` (string, optional) — Minimum pitches; `min_results` (string, optional) — Minimum results; `offset` (integer, optional) — Zero-based row offset; `pitch_hand` (string, optional) — Pitcher hand; omit for all; `pitch_types` (array, optional) — One or more pitch types; `season_end` (string, optional) — Last season; must be >= season_start; `season_start` (string, optional) — First season; `sort` (string, optional) — Local row sort field; `sort_dir` (string, optional) — Sort direction; `teams` (array, optional) — One or more MLB team ids; `type` (string, optional) — Table entity type

### `mlb_statcast_catcher_throwing`

- **HTTP:** `GET /mlb/statcast-catcher-throwing`
- **What:** Get Baseball Savant Catcher Throwing leaderboard rows. Returns catcher, catching-team, or league caught-stealing and throw-quality rows with the public season, game, attempt-threshold, target-base, split-years, team, and roster-membership filters. Table sorting and pagination are applied locally. Catcher rows can be expanded with mlb-statcast-catcher-throwing-details. CSV, charts, and page-local display controls are excluded.
- **Params:** `game_type` (string, optional) — Game type; `limit` (integer, optional) — Rows per page (1-500); `minimum` (string, optional) — Minimum steal attempts; `offset` (integer, optional) — Zero-based row offset; `season_end` (string, optional) — Last season; must be >= season_start; `season_start` (string, optional) — First season; `sort` (string, optional) — Local sort field; `sort_dir` (string, optional) — Local sort direction; `split` (string, optional) — Split results by season; `target_base` (string, optional) — Throw target; `team` (string, optional) — Empty for all teams, split for team stints, or an MLB team id; `type` (string, optional) — Table group; `with_team_only` (boolean, optional) — For a selected team, include only catchers on that team

### `mlb_statcast_catcher_throwing_details`

- **HTTP:** `GET /mlb/statcast-catcher-throwing-details`
- **What:** Get Catcher Throwing attempt details. Returns per-attempt play records expanded from a Catcher Throwing catcher row. Supply the entity_id from a Cat row and the row's year/team when it represents a season or team stint. Details are ungrouped source attempts, paginated locally.
- **Params:** `entity_id` (integer, **required**) — Positive catcher id from a Cat row; `game_type` (string, optional) — Game type; `limit` (integer, optional) — Rows per page (1-500); `minimum` (string, optional) — Minimum steal attempts; `offset` (integer, optional) — Zero-based row offset; `split` (string, optional) — Split rows by season; `target_base` (string, optional) — Throw target; `team` (string, optional) — Empty, split, or team id from the corresponding leaderboard row; `with_team_only` (boolean, optional) — Team roster membership filter; `year` (integer, optional) — Season

### `mlb_statcast_expected`

- **HTTP:** `GET /mlb/statcast-expected`
- **What:** Get Baseball Savant Expected Statistics. Returns the separate Expected Statistics leaderboard with batter, pitcher, and team views; season, team, batter-position, BIP/PA qualifier and threshold filters; local metric sorting; and pagination. League-average values are returned separately.
- **Params:** `filter_type` (string, optional) — Minimum qualifier type; `limit` (integer, optional) — Rows per page (1-500); `minimum` (string, optional) — Minimum BIP/PA threshold; `offset` (integer, optional) — Zero-based row offset; `position` (string, optional) — Batter position; only supported for type=batter; `sort` (string, optional) — Sort field; `sort_dir` (string, optional) — Sort direction; `team_id` (string, optional) — Optional MLB team id from mlb_teams; `type` (string, optional) — Leaderboard view; `year` (integer, optional) — Season from 2015 through the current season

### `mlb_statcast_fielding_run_value`

- **HTTP:** `GET /mlb/statcast-fielding-run-value`
- **What:** Get Baseball Savant Fielding Run Value rows. Returns fielding run value for fielder, fielding-team, batter, batting-team, or pitcher views. Dates and grouping dimensions follow the first-party leaderboard. Minimum 0.1 is available only for fielder and fielding-team views; the batting/pitching views omit it. Sorting and pagination are applied locally. CSV and player-page visualizations are outside this table contract.
- **Params:** `date_end` (string, optional) — End date, YYYY-MM-DD, from 2018-03-29 through today; `date_start` (string, optional) — Start date, YYYY-MM-DD, from 2018-03-29 through today; `game_type` (string, optional) — Game type; `group_by` (array, optional) — Repeated split dimensions; `limit` (integer, optional) — Rows per page (1-500); `minimum` (string, optional) — Total minimum; 0.1 only for fielder and fielding-team; `minimum_split` (string, optional) — Minimum within each split; 0.1 only for fielder and fielding-team; `offset` (integer, optional) — Zero-based row offset (0-5000); `position` (string, optional) — Position / position group; `season_end` (string, optional) — Last season; must be >= season_start; `season_start` (string, optional) — First season; `sort` (string, optional) — Local sort field; `sort_dir` (string, optional) — Local sort direction; `team_id` (array, optional) — Repeated MLB team ids; `type` (string, optional) — Table type

### `mlb_statcast_first_base_receiving`

- **HTTP:** `GET /mlb/statcast-first-base-receiving`
- **What:** Get Baseball Savant First Base Receiving leaderboards. Returns first baseman, throwing fielder, fielding team, batting team, or league receiving rows. Includes season/game selections, threshold and group filters, team/date/hand/height/outcome filters, and validated page-local split filters and sorting. Per-play source records are available through mlb-statcast-first-base-receiving-details. 3D trajectory visualizations are not included.
- **Params:** `bin_time_X10[]` (array, optional) — Time bins; `dateEnd` (string, optional) — Inclusive end date (YYYY-MM-DD); `dateStart` (string, optional) — Inclusive start date (YYYY-MM-DD); `fielder_3_hand` (string, optional) — First baseman batting hand; `gameType[]` (array, optional) — Game types; `is_hit_into_play_field_out` (string, optional) — Field-out flag; `limit` (integer, optional) — Rows per page, 1-500; `min` (string, optional) — Minimum opportunities; `minSplit` (string, optional) — Minimum opportunities within each group; `min_height_in_inches` (string, optional) — Minimum fielder height, inches; `offset` (integer, optional) — Zero-based row offset; `runners_on_cd[]` (array, optional) — Base occupancy codes; `season[]` (array, optional) — Season values; `sortColumn` (string, optional) — Local sort field; `sortDirection` (string, optional) — Local sort direction; `splitYear` (string, optional) — Year split selector; `split[]` (array, optional) — Group dimensions; `team[]` (array, optional) — MLB team ids; `throw_height_code[]` (array, optional) — Throw heights; `throw_location_code_full[]` (array, optional) — Throw outcomes; `throw_pos_id[]` (array, optional) — Throwing position ids; `type` (string, optional) — Leaderboard group

### `mlb_statcast_first_base_receiving_details`

- **HTTP:** `GET /mlb/statcast-first-base-receiving-details`
- **What:** Get a player's First Base Receiving play records. Returns per-play records backing an individual first-base receiving leaderboard row, including game/play ids, outcome codes, receiving OAA, expected out rate, timing, and field coordinates. This is tabular JSON; the separate 3D skeletal visualization route is excluded.
- **Params:** `bin_time_X10[]` (array, optional) — Time bins; `dateEnd` (string, optional) — Inclusive end date (YYYY-MM-DD); `dateStart` (string, optional) — Inclusive start date (YYYY-MM-DD); `fielder_3_hand` (string, optional) — First baseman batting hand; `gameType[]` (array, optional) — Game types; `is_hit_into_play_field_out` (string, optional) — Field-out flag; `limit` (integer, optional) — Rows per page, 1-500; `min` (string, optional) — Minimum opportunities; `minSplit` (string, optional) — Grouped opportunity threshold; `min_height_in_inches` (string, optional) — Minimum fielder height; `offset` (integer, optional) — Zero-based row offset; `player_id` (integer, **required**) — Positive MLB player id; `runners_on_cd[]` (array, optional) — Base occupancy codes; `season[]` (array, optional) — Season values; `splitYear` (string, optional) — Year split selector; `split[]` (array, optional) — Group dimensions; `team[]` (array, optional) — MLB team ids; `throw_height_code[]` (array, optional) — Throw heights; `throw_location_code_full[]` (array, optional) — Throw outcomes; `throw_pos_id[]` (array, optional) — Throwing position ids; `type` (string, optional) — Leaderboard group

### `mlb_statcast_home_runs`

- **HTTP:** `GET /mlb/statcast-home-runs`
- **What:** Get Baseball Savant Home Runs Tracking. Returns Batter or Pitcher Home Runs Tracking rows. Year, team id, minimum home runs, and Standard/Adjusted mode are first-party filters. The first-party table sorts client-side; this endpoint applies a named local sort and pagination. Use mlb_discovery for the exact filter sets. Per-player home-run plays are available from mlb-statcast-home-runs-details; trajectory images, video media, and CSV downloads are separate representations.
- **Params:** `cat` (string, optional) — Trajectory mode; `limit` (integer, optional) — Rows per page (1-500); `min` (string, optional) — Minimum home run total; `offset` (integer, optional) — Zero-based row offset; `player_type` (string, optional) — Table type; `sort` (string, optional) — Local sort column; `sort_dir` (string, optional) — Local sort direction; `team` (string, optional) — MLB team id; blank selects all teams; `year` (string, optional) — Season

### `mlb_statcast_home_runs_details`

- **HTTP:** `GET /mlb/statcast-home-runs-details`
- **What:** Get Baseball Savant Home Runs play details. Returns the home-run plays expanded from one batter or pitcher leaderboard row, with event measurements and park outcomes. Provide the exact player id, player type, year, and mode from the row. Play identifiers and source links are returned; trajectory images, video media, and CSV output are not included.
- **Params:** `cat` (string, optional) — Trajectory mode; `limit` (integer, optional) — Rows per page (1-500); `offset` (integer, optional) — Zero-based row offset; `player_id` (string, **required**) — Positive MLB player id from mlb-statcast-home-runs; `player_type` (string, optional) — Table type; `year` (string, optional) — Season

### `mlb_statcast_oaa`

- **HTTP:** `GET /mlb/statcast-oaa`
- **What:** Get Baseball Savant Outs Above Average. Returns the separate Outs Above Average leaderboard for fielders, fielding teams, batters, batting teams, or pitchers. Supports season range, split years, team, monthly range, attempts, position, detailed fielder roles, local sorting, and pagination.
- **Params:** `end_year` (integer, optional) — End season from 2016 through the current season; `limit` (integer, optional) — Rows per page (1-500); `minimum` (string, optional) — Minimum attempts; `offset` (integer, optional) — Zero-based row offset; `position` (string, optional) — Position filter; `range` (string, optional) — Time range; `roles` (string, optional) — Comma-separated detailed fielder role ids. Values: 32,30,31,77,71,70,72,78,43,42,40,41,46,87,81,82,89,64,62,60,61,98,91,90,92,99,51,50,52; `sort` (string, optional) — Sort field; `sort_dir` (string, optional) — Sort direction; `split` (string, optional) — Return one row per season in a year range; `start_year` (integer, optional) — Start season from 2016 through the current season; `team_id` (string, optional) — Optional MLB team id from mlb_teams; `type` (string, optional) — Leaderboard view

### `mlb_statcast_park_factors`

- **HTTP:** `GET /mlb/statcast-park-factors`
- **What:** Get Baseball Savant Statcast Park Factors rows. Returns season, venue, distance, distance-all, raw, or dimensions rows from Baseball Savant. Query filters are conditional on type and are live-echo validated; local sorting and pagination are applied to returned rows. The fence-stat and allDiffs controls only change display columns and do not change row data; CSV and linked venue detail pages are separate surfaces.
- **Params:** `bat_side` (string, optional) — Optional batter side for year, venue, or raw mode; `condition` (string, optional) — Park condition for year and venue modes; `limit` (integer, optional) — Rows per page (1-500); `offset` (integer, optional) — Zero-based row offset; `parks` (string, optional) — Park population selector; `rolling` (string, optional) — Rolling year count for year and venue modes; `sort` (string, optional) — Local row field present in the selected mode's data; `sort_dir` (string, optional) — Local sort direction; `stat` (string, optional) — Venue mode metric; `type` (string, optional) — Park Factors table mode; `year` (string, optional) — Mode-specific season; see endpoint markdown and mlb_discovery for exact values

### `mlb_statcast_percentile`

- **HTTP:** `GET /mlb/statcast-percentile`
- **What:** Get Baseball Savant Percentile Rankings. Returns batter or pitcher percentile rankings. Type, season, and team are first-party table filters. Repeated pctl filters, table sorting, and pagination are applied locally to the embedded rows. Use mlb_discovery for exact type-specific fields, comparators, seasons, and team ids. CSV is a separate download.
- **Params:** `limit` (integer, optional) — Rows per page (1-500); `offset` (integer, optional) — Zero-based row offset; `pctl` (array, optional) — Repeated field-comparator-value filter from the type-specific field set in mlb_discovery; value range 0-100; `sort` (string, optional) — Local sort field from the type-specific set in mlb_discovery; `sort_dir` (string, optional) — Local sort direction; `team` (string, optional) — MLB team id; blank selects all teams; `type` (string, optional) — Table type; `year` (string, optional) — Season

### `mlb_statcast_pitch_arsenal`

- **HTTP:** `GET /mlb/statcast-pitch-arsenal`
- **What:** Get Baseball Savant Pitch Arsenal Stats. Returns pitcher or batter pitch-level arsenal leaderboards. Season, team, pitch type, minimum PA, and minimum-pitch qualification filters are replayed against the anonymous first-party table; sorting and pagination are applied locally. Use mlb_discovery for the full selector set. Player rows can be expanded with mlb-statcast-pitch-arsenal-details.
- **Params:** `limit` (integer, optional) — Rows per page (1-500); `min_pa` (string, optional) — Minimum plate appearances; `min_pitches` (string, optional) — Minimum pitches; q means qualified; `offset` (integer, optional) — Zero-based row offset; `pitch_type` (string, optional) — Pitch code; blank means all pitch types; `sort` (string, optional) — Local sort field; `sort_dir` (string, optional) — Local sort direction; `team_id` (string, optional) — MLB team id from mlb_teams; `type` (string, optional) — Row type; `year` (string, optional) — Season

### `mlb_statcast_pitch_arsenal_details`

- **HTTP:** `GET /mlb/statcast-pitch-arsenal-details`
- **What:** Get Baseball Savant Pitch Arsenal play details. Returns game-level pitches expanded from one batter or pitcher pitch-arsenal row. Supply player_id, player_type, year, and the row's pitch_type. The upstream's min_ab request parameter is ignored, so it is not exposed. Rows include play_id values used by Baseball Savant's video pages; this endpoint returns play data and identifiers, not video media.
- **Params:** `limit` (integer, optional) — Rows per page (1-500); `offset` (integer, optional) — Zero-based row offset; `pitch_type` (string, **required**) — Pitch type from the selected row; `player_id` (string, **required**) — Positive MLB player id from mlb-statcast-pitch-arsenal; `player_type` (string, optional) — Row type; `year` (string, optional) — Season

### `mlb_statcast_pitch_arsenals`

- **HTTP:** `GET /mlb/statcast-pitch-arsenals`
- **What:** Get Baseball Savant Pitch Arsenals. Returns pitcher pitch speed, percentage, or spin rankings by pitch class. Year, minimum-pitch threshold, and hand are first-party filters. Team filtering and table sorting are applied locally because the page JavaScript applies them after receiving the embedded rows. Use mlb_discovery for exact values. CSV and pitch movement visualizations remain separate representations.
- **Params:** `hand` (string, optional) — Throwing hand; omit for all pitchers; `limit` (integer, optional) — Rows per page (1-500); `min_pitches` (string, optional) — Minimum pitches; `offset` (integer, optional) — Zero-based row offset; `sort` (string, optional) — Local sort column; `sort_dir` (string, optional) — Local sort direction; `team` (string, optional) — Current MLB team abbreviation; applied locally; `type` (string, optional) — Metric; `year` (string, optional) — Season

### `mlb_statcast_pitch_movement`

- **HTTP:** `GET /mlb/statcast-pitch-movement`
- **What:** Get Baseball Savant Pitch Movement rows. Returns pitcher-level pitch movement table rows for the selected season, pitch type, throwing hand, and minimum pitch count. Sorting and pagination are applied locally. The page's X/Z visualization axes and CSV download are separate presentation formats and are not returned by this JSON table contract.
- **Params:** `hand` (string, optional) — Pitcher throwing hand; omit for both; `limit` (integer, optional) — Rows per page (1-500); `min` (string, optional) — Minimum pitch count; `offset` (integer, optional) — Zero-based row offset; `pitch_type` (string, optional) — Pitch class; `sort` (string, optional) — Local table sort field; `sort_dir` (string, optional) — Sort direction; `year` (string, optional) — Season

### `mlb_statcast_pitch_tempo`

- **HTTP:** `GET /mlb/statcast-pitch-tempo`
- **What:** Get Baseball Savant Pitch Tempo rows. Returns pitcher, batter, pitching-team, batting-team, or league tempo rows. Season, game type, minimum pitch, team, year comparison, and team membership options mirror the live first-party controls; q and sorting are applied locally before pagination. Use mlb_discovery for exact value sets.
- **Params:** `game_type` (string, optional) — Game type; `limit` (integer, optional) — Rows per page (1-500); `n` (string, optional) — Minimum pitch count; `offset` (integer, optional) — Zero-based row offset; `q` (string, optional) — Case-insensitive local entity-name filter; `season_end` (string, optional) — Last season; must be >= season_start; `season_start` (string, optional) — First season; `sort` (string, optional) — Local sort field; `sort_dir` (string, optional) — Sort direction; `split` (string, optional) — Compare seasons separately; `team` (string, optional) — Optional MLB team id; `type` (string, optional) — Table group; `with_team_only` (string, optional) — Team membership mode; requires team

### `mlb_statcast_pitch_tempo_player`

- **HTTP:** `GET /mlb/statcast-pitch-tempo-player`
- **What:** Get a player's Pitch Tempo detail rows. Returns game-level Pitch Tempo detail rows for one pitcher or batter. `entity_id` is required, taken from a Pitch Tempo result. `type` is `Pit` (default) or `Bat`, `season_start` and `season_end` run from 2010 to 2026 and default to the current year, and `game_type` is `Regular` (default), `Playoff` or `All`. Rows hold elapsed seconds, counts and frequencies; empty when nothing matches.
- **Params:** `entity_id` (string, **required**) — Numeric entity id from a Pitch Tempo row; `game_type` (string, optional) — Game type; `season_end` (string, optional) — Last season; must be >= season_start; `season_start` (string, optional) — First season; `type` (string, optional) — Entity type

### `mlb_statcast_pitch_timer`

- **HTTP:** `GET /mlb/statcast-pitch-timer`
- **What:** Get Baseball Savant Pitch Timer infraction rows. Returns the Pitch Timer Infractions table for pitchers, batters, catchers, teams, or opposing teams. Filters for type, season, minimum pitches, and zero-infraction rows are upstream-backed; entity search, table sorting, and pagination are applied locally. The chart ordering is included as view metadata; the endpoint returns table rows, not the SVG chart.
- **Params:** `chart_sort` (string, optional) — Chart ordering metadata; `include_zeroes` (string, optional) — Include entities without infractions; `limit` (integer, optional) — Rows per page (1-500); `min_pitches` (string, optional) — Minimum pitches; `offset` (integer, optional) — Zero-based row offset; `q` (string, optional) — Local case-insensitive entity-name substring filter; `season` (string, optional) — Season; `sort` (string, optional) — Local table sort field; `sort_dir` (string, optional) — Sort direction; `type` (string, optional) — Entity group

### `mlb_statcast_player_details`

- **HTTP:** `GET /mlb/statcast-player-details`
- **What:** Get expanded standard Baseball Savant Statcast player plays. Returns the game-level pitch or batted-ball rows shown when expanding a batter or pitcher row in the standard Statcast leaderboard, including matchup, date, event, exit velocity, launch angle, distance, play id, and video availability.
- **Params:** `player_id` (string, **required**) — Positive MLB player id from a batter or pitcher row; `player_type` (string, optional) — Player row type; `year` (integer, optional) — Season from 2015 through the current season

### `mlb_statcast_rolling`

- **HTTP:** `GET /mlb/statcast-rolling`
- **What:** Get Baseball Savant Rolling Windows rows. Returns the six embedded Batter/Pitcher rolling-window tables, filtered by metric, role, and plate-appearance window. Each group is sorted by the selected metric delta in the same direction as the first-party page and paginated independently. The upstream page has no season, team, or game-type filters.
- **Params:** `limit` (integer, optional) — Rows per group (1-500); `metric` (string, optional) — Displayed metric; `offset` (integer, optional) — Zero-based row offset per group (0-5000); `role` (string, optional) — Optional player role; omit for both; `window_pa` (string, optional) — Optional rolling plate-appearance window; omit for all

### `mlb_statcast_run_value`

- **HTTP:** `GET /mlb/statcast-run-value`
- **What:** Get Baseball Savant Run Value rows. Returns batting or pitching Run Value rows from the Swing-Take leaderboard. Filters are cold-replay verified; sorting and pagination are applied locally. The Bat-side R/L selector was verified to leave the embedded rows byte-identical and is omitted. The page's visual charts and CSV export are separate formats.
- **Params:** `group` (string, optional) — Row group; `leverage` (string, optional) — Run-value method; `limit` (integer, optional) — Rows per page (1-500); `min` (string, optional) — Minimum plate appearances; `offset` (integer, optional) — Zero-based row offset; `sort` (string, optional) — Local table sort field; supported set varies by view; `sort_dir` (string, optional) — Sort direction; `sub_type` (string, optional) — Conditional subtype: Swing/Take; pitch name; or Heart/Shadow/Chase/Waste; `team` (string, optional) — MLB numeric team id; omit for all teams; `type` (string, optional) — Table view; `year` (string, optional) — Season, All, or Career

### `mlb_statcast_running_game`

- **HTTP:** `GET /mlb/statcast-running-game`
- **What:** Get Baseball Savant Running Game leaderboards. Returns the Running Game table for pitchers, pitching teams, or league. Season/game, hand, runner movement, target base, prior pickoff count, minimum opportunities, team, and team-stint controls are live-verified; named sorting, player/team search, and pagination are applied locally. Per-play records are available from mlb-statcast-running-game-details. The expanded-column toggle returns the same source fields, and the first-party CSV download is not a separate JSON response mode.
- **Params:** `game_type` (string, optional) — Game scope; `limit` (integer, optional) — Rows per page, 1-500; `n` (string, optional) — Minimum pitcher opportunities; `offset` (integer, optional) — Zero-based row offset; `pitch_hand` (string, optional) — Pitcher's throwing hand; `prior_pk` (string, optional) — Prior pickoff/disengagement count; `runner_moved` (string, optional) — Runner movement outcome; `search` (string, optional) — Case-insensitive substring of the displayed player or team name; `season_end` (integer, optional) — Inclusive last season; `season_start` (integer, optional) — Inclusive first season; `sort` (string, optional) — Local table sort field; `sort_dir` (string, optional) — Local sort direction; `split` (string, optional) — Return separate year rows; `target_base` (string, optional) — Target base; `team` (string, optional) — MLB team id, or split team stints; `type` (string, optional) — Leaderboard group; `with_team_only` (boolean, optional) — Restrict pitcher rows to the selected team; only valid with one specific team id

### `mlb_statcast_running_game_details`

- **HTTP:** `GET /mlb/statcast-running-game-details`
- **What:** Get Baseball Savant Running Game play details. Returns individual attempted-running plays expanded from a pitcher or pitching-team Running Game row. Pass its entity_id and repeat the same table filters. For team-stint rows, pass that row's team id; League rows do not expose a detail feed.
- **Params:** `entity_id` (integer, **required**) — Positive player or team entity id from the Running Game leaderboard; `game_type` (string, optional) — Game scope; `limit` (integer, optional) — Play rows per page, 1-500; `n` (string, optional) — Minimum pitcher opportunities; `offset` (integer, optional) — Zero-based play-row offset; `pitch_hand` (string, optional) — Pitcher's throwing hand; `prior_pk` (string, optional) — Prior pickoff/disengagement count; `runner_moved` (string, optional) — Runner movement outcome; `season_end` (integer, optional) — Inclusive last season; `season_start` (integer, optional) — Inclusive first season; `split` (string, optional) — Return separate year rows; `target_base` (string, optional) — Target base; `team` (string, optional) — One MLB team id; use the row's team id for split-team rows; `type` (string, optional) — Detail group; `with_team_only` (boolean, optional) — Restrict player rows to selected team; only valid with a specific team and Pit type

### `mlb_statcast_sprint_speed`

- **HTTP:** `GET /mlb/statcast-sprint-speed`
- **What:** Get Baseball Savant Sprint Speed player rows. Returns player Sprint Speed rows from the Baseball Savant leaderboard. The source filters season range, position, and minimum competitive runs; team filtering and sorting are applied locally. Use mlb_discovery for every closed value set.
- **Params:** `limit` (integer, optional) — Rows per page (1-500); `max_season` (string, optional) — Last season; must be >= min_season; `min_season` (string, optional) — First season; `minimum_runs` (string, optional) — Minimum competitive runs; `offset` (integer, optional) — Zero-based row offset; `position` (string, optional) — Position code; omitted is All Positions; `sort` (string, optional) — Local sort field; `sort_dir` (string, optional) — Sort direction; `team_id` (string, optional) — MLB team id

### `mlb_statcast_sprint_speed_teams`

- **HTTP:** `GET /mlb/statcast-sprint-speed-teams`
- **What:** Get Baseball Savant Sprint Speed team rows. Returns team-level Sprint Speed rows. Season is selected upstream; team filtering and sorting are applied locally because the first-party page embeds every team before its client-side filter. Use mlb_discovery for all accepted seasons, teams, and sort fields.
- **Params:** `limit` (integer, optional) — Rows per page (1-500); `offset` (integer, optional) — Zero-based row offset; `season` (string, optional) — Season or all seasons; `sort` (string, optional) — Local sort field; `sort_dir` (string, optional) — Sort direction; `team` (string, optional) — Optional first-party team selector abbreviation

### `mlb_statcast_swing_path`

- **HTTP:** `GET /mlb/statcast-swing-path`
- **What:** Get Baseball Savant Swing Path and Attack Angle rows. Returns batter, batting-team, or league Swing Path and Attack Angle rows with the first-party season, game, swing, team, date, side, contact, hard-hit, attack-zone, and pitcher-hand filters. Use mlb_discovery for exact values.
- **Params:** `attack_zone` (string, optional) — Attack zone; `bat_side` (string, optional) — Batter side; `contact_type` (string, optional) — Contact type; `date_end` (string, optional) — Optional range end in YYYY-MM-DD; `date_start` (string, optional) — Optional range start in YYYY-MM-DD; `game_type` (string, optional) — Game type; `is_hard_hit` (string, optional) — Hard-hit filter; `limit` (integer, optional) — Rows per page (1-500); `min_group_swings` (string, optional) — Minimum swings per group; `min_swings` (string, optional) — Minimum swing threshold; `offset` (integer, optional) — Zero-based row offset; `pitch_hand` (string, optional) — Pitcher hand; `season_end` (string, optional) — Last season; must be >= season_start; `season_start` (string, optional) — First season; `sort` (string, optional) — Local sort field; `sort_dir` (string, optional) — Sort direction; `team_id` (string, optional) — Optional MLB team id; `type` (string, optional) — Row type

### `mlb_statcast_swing_timing`

- **HTTP:** `GET /mlb/statcast-swing-timing`
- **What:** Get Baseball Savant Swing Timing and Miss Distance rows. Returns batter, batting-team, pitcher, pitching-team, or league rows with the page's season, game type, pitch-group, split, team, date, swing, contact, zone, pitch hand/type, count, timing-axis, and timing-flag filters. Sorting is local. Use mlb_discovery for exact values.
- **Params:** `attack_zone` (string, optional) — Attack zone; `bat_side` (string, optional) — Batter side; `contact_type` (string, optional) — Contact type; `counts` (array, optional) — One or more ball-strike counts; `date_end` (string, optional) — Optional range end in YYYY-MM-DD; `date_start` (string, optional) — Optional range start in YYYY-MM-DD; `flags` (array, optional) — Positive timing flags; `game_types` (array, optional) — One or more game types; `limit` (integer, optional) — Rows per page (1-500); `min_split` (string, optional) — Minimum swings per split group; `min_swings` (string, optional) — Minimum swing threshold; `not_flags` (array, optional) — Excluded timing flags; `offset` (integer, optional) — Zero-based row offset; `pitch_hand` (string, optional) — Pitcher hand; `pitch_types` (array, optional) — One or more pitch type codes; `seasons` (array, optional) — One or more seasons; `sort` (string, optional) — Local sort field; `sort_dir` (string, optional) — Sort direction; `split_year` (string, optional) — Split years into separate rows; `splits` (array, optional) — One or more split dimensions; `swing_timing_x` (array, optional) — Tied-up, centered, or flailed; `swing_timing_y` (array, optional) — Early, on-time, or late; `swing_timing_z` (array, optional) — Under, lined-up, or over; `teams` (array, optional) — One or more MLB team ids; `type` (string, optional) — Row type

### `mlb_statcast_swing_timing_details`

- **HTTP:** `GET /mlb/statcast-swing-timing-details`
- **What:** Get Baseball Savant Swing Timing player details. Returns the four anonymous per-swing detail arrays expanded from a batter or pitcher Swing Timing row. Pass the row_id uniqueId from mlb-statcast-swing-timing and repeat its type and table filters so split values can be mapped to the upstream detail query.
- **Params:** `attack_zone` (string, optional) — Attack zone; `bat_side` (string, optional) — Batter side; `contact_type` (string, optional) — Contact type; `counts` (array, optional) — Ball-strike counts; `date_end` (string, optional) — Filter end date in YYYY-MM-DD format; `date_start` (string, optional) — Filter start date in YYYY-MM-DD format; `flags` (array, optional) — Positive swing timing flags; `game_types` (array, optional) — Game-type filters; `min_split` (string, optional) — Minimum group swings; `min_swings` (string, optional) — Minimum swings; `not_flags` (array, optional) — Excluded swing timing flags; `pitch_hand` (string, optional) — Pitcher hand; `pitch_types` (array, optional) — Pitch type codes; `row_id` (string, **required**) — Unique row id from mlb-statcast-swing-timing, including any selected split values; `seasons` (array, optional) — Season filters; `split_year` (string, optional) — Include year in the row grouping; `splits` (array, optional) — Split dimensions; `swing_timing_x` (array, optional) — Tied-up/flail axis values; `swing_timing_y` (array, optional) — Early/late axis values; `swing_timing_z` (array, optional) — Over/under axis values; `teams` (array, optional) — MLB team ids; `type` (string, **required**) — Player row type

### `mlb_statcast_top_performers`

- **HTTP:** `GET /mlb/statcast-top-performers`
- **What:** Get Baseball Savant Top Performers. Returns every current Top Performers card for the selected season, including batter and pitcher rankings across batting, batted-ball, expected-stat, fielding, catching, running, and pitch-metric views. The page exposes a season selector but no per-card filters; use the specialist Statcast endpoints for complete filtered leaderboards.
- **Params:** `year` (integer, optional) — Season from 2015 through the current season; defaults to the current season

### `mlb_statcast_year_to_year`

- **HTTP:** `GET /mlb/statcast-year-to-year`
- **What:** Get Baseball Savant Year-to-Year Changes. Returns one of Baseball Savant's Year-to-Year Changes tables for batters, pitchers, batting teams, or pitching teams. Select one of the live statistic types and comparison start years; the page data contains available yearly values and differences. Table sorting and pagination are applied locally. Use mlb_discovery for all accepted group, type, and year values.
- **Params:** `group` (string, optional) — Table group; `limit` (integer, optional) — Rows per page (1-500); `offset` (integer, optional) — Zero-based row offset (0-5000); `sort` (string, optional) — Local sortable column; name_display_last_first, year_YYYY, TYPE_YYYY, or TYPE_diff_YYYY. Defaults to the selected metric's difference for the selected comparison year.; `sort_dir` (string, optional) — Sort direction; defaults to Batter descending and Pitcher ascending; `type` (string, optional) — Statistic type; `year` (string, optional) — Comparison start year; compares this season with the following year

### `mlb_team_roster`

- **HTTP:** `GET /mlb/team-roster`
- **What:** Get an MLB team roster. Returns a team's players, jersey numbers, positions, and roster status. The roster_type parameter accepts every value in the live MLB value set returned by mlb_discovery.
- **Params:** `roster_type` (string, optional) — Roster type; `season` (integer, optional) — Four-digit season; defaults to current year; `team_id` (string, **required**) — Numeric MLB team id

### `mlb_team_stats`

- **HTTP:** `GET /mlb/team-stats`
- **What:** Get MLB team season statistics. Returns one MLB team's statistics. `team_id` and `group` (`hitting`, `pitching`, `fielding`, `catching`, `running`, `game`, `team` or `streak`) are required. `season` defaults to the current year and `stat_type` to `season`. Other `stat_type` values cover splits and logs. Use `start_date` with `end_date` for date ranges.
- **Params:** `end_date` (string, optional) — End date for byDateRange stat types; requires start_date; `game_type` (string, optional) — MLB game type; `group` (string, **required**) — Statistics group; `opponent_player_id` (string, optional) — Required by vsPlayer stat types; `opponent_team_id` (string, optional) — Required by vsTeam stat types; `season` (integer, optional) — Four-digit season; `start_date` (string, optional) — Start date for byDateRange stat types; requires end_date; `stat_type` (string, optional) — Stats API stat type; defaults to season; `team_id` (string, **required**) — Numeric MLB team id

### `mlb_teams`

- **HTTP:** `GET /mlb/teams`
- **What:** List MLB teams. Lists the 30 MLB clubs for a `season` (four-digit year, default the current year). Each team has its id, name, club name, location, abbreviation, league, division, venue, first year of play and active flag.
- **Params:** `season` (integer, optional) — Four-digit season; defaults to current year

### `mlb_transactions`

- **HTTP:** `GET /mlb/transactions`
- **What:** List MLB transactions. Lists MLB transactions between `start_date` and `end_date`, both required in `YYYY-MM-DD` format. Covers signings, trades, options, assignments, injured-list moves and releases. Narrow with `team_id` or `player_id`. Each entry has the date, effective date, type, description, player, and from and to teams, with a total `count`.
- **Params:** `end_date` (string, **required**) — Range end in YYYY-MM-DD format; `player_id` (string, optional) — Numeric MLB player id; `start_date` (string, **required**) — Range start in YYYY-MM-DD format; `team_id` (string, optional) — Numeric MLB team id
