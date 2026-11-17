# sports-team-player-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**15 endpoints across 1 platform group(s).**

## Flashscore (15)

### `flashscore_entity_news`

- **HTTP:** `GET /flashscore/entity-news`
- **What:** Flashscore news for a team, player, tournament or sport. Returns the article ids of Flashscore's own news layout for one entity: the featured article plus the 25 most recent ones, grouped in the sections Flashscore shows. The layout has no pagination. Resolve the ids with flashscore-news-article (metadata) or flashscore-news-article-body (full text). Teams and players share one layout type. A tournament is a tournament template id (the competition id in event lists); a sport is one of the SPORT entity ids listed by flashscore-news-categories. An id with no news layout returns not found.
- **Params:** `id` (string, **required**) — Eight-character entity id: team or player id, tournament template id, or a SPORT entity id from flashscore-news-categories; `type` (string, **required**) — Entity type

### `flashscore_player`

- **HTTP:** `GET /flashscore/player`
- **What:** Flashscore player profile and career. Returns a player's public profile: name, country, birth date, sport, photo and current team, plus (for team-sport players) position, age, market value, contract expiry, extra details such as height, and career statistics by season, team and competition grouped into league, domestic cups, international cups and national team. Players of individual sports such as tennis return the profile (and ranking text) without a career table.
- **Params:** `id` (string, **required**) — Eight-character Flashscore player id; `slug` (string, optional) — Optional player slug; must match the id when supplied

### `flashscore_player_fixtures`

- **HTTP:** `GET /flashscore/player-fixtures`
- **What:** Flashscore player fixtures. Returns one page of an individual-sport player's upcoming matches (tennis, darts, golf, snooker and similar), soonest first, as structured events. Football, basketball and hockey players have no event list and return an empty list; use flashscore-team-fixtures for their team. Request successive pages until event_count is 0.
- **Params:** `id` (string, **required**) — Eight-character Flashscore player id; `page` (integer, optional) — 1-based page from 1 to 300; defaults to 1

### `flashscore_player_injuries`

- **HTTP:** `GET /flashscore/player-injuries`
- **What:** Flashscore player injury history. Returns a team-sport player's injury history, newest first, with start date, end date (absent while unresolved) and injury type. A player with no recorded injuries returns an empty list. Players of individual sports have no injury page and return not found.
- **Params:** `id` (string, **required**) — Eight-character Flashscore player id; `slug` (string, optional) — Optional player slug; must match the id when supplied

### `flashscore_player_match_log`

- **HTTP:** `GET /flashscore/player-match-log`
- **What:** Flashscore player match log. Returns one page of a football, basketball or hockey player's match log, newest first: each match with date, both sides and scores, competition, the player's rating and labelled statistics (minutes, goals, assists, cards, goalkeeper saves, points, rebounds, time on ice and more depending on the sport). Matches without statistics say why (on the bench, injured, suspended). Page 1 holds the 10 newest matches and every later page 25 older ones; request pages until has_more is false. Players of individual sports return an empty list, use flashscore-player-results for those.
- **Params:** `id` (string, **required**) — Eight-character Flashscore player id; `page` (integer, optional) — 1-based page from 1 to 300; defaults to 1

### `flashscore_player_news`

- **HTTP:** `GET /flashscore/player-news`
- **What:** Flashscore player news. Returns up to 100 recent headlines about a player, aggregated from news publishers, with publisher, publication time and image. Links point to Flashscore's redirect to the publisher. A player without news returns an empty list. A team id returns not found, use flashscore-team-news for teams.
- **Params:** `id` (string, **required**) — Eight-character Flashscore player id

### `flashscore_player_results`

- **HTTP:** `GET /flashscore/player-results`
- **What:** Flashscore player results. Returns one page of an individual-sport player's finished and in-progress matches (tennis, darts, golf, snooker and similar), newest first, as structured events with start time, stage, both sides, score and competition. Competition blocks carry tournament_id and tournament_stage_id for the tournament endpoints. Football, basketball and hockey players have no event list and return an empty list, use flashscore-player-match-log for those. Request successive pages until event_count is 0.
- **Params:** `id` (string, **required**) — Eight-character Flashscore player id; `page` (integer, optional) — 1-based page from 1 to 300; defaults to 1

### `flashscore_player_transfers`

- **HTTP:** `GET /flashscore/player-transfers`
- **What:** Flashscore player transfer history. Returns a team-sport player's club history, newest first, with date, type such as Loan or Free agent, fee text and the clubs on each side. A player with no recorded transfers returns an empty list. Players of individual sports have no transfers page and return not found.
- **Params:** `id` (string, **required**) — Eight-character Flashscore player id; `slug` (string, optional) — Optional player slug; must match the id when supplied

### `flashscore_search`

- **HTTP:** `GET /flashscore/search`
- **What:** Flashscore search. Searches the same public entity index used by Flashscore's search box. Results can include teams, players, and tournament templates across supported sports.
- **Params:** `q` (string, **required**) — Search phrase (2 to 80 characters)

### `flashscore_team`

- **HTTP:** `GET /flashscore/team`
- **What:** Flashscore team profile. Returns a team's public profile: name, country, sport, logo, the stadium and capacity shown on its summary page, and the competitions of its recent and upcoming fixtures. Use a team id from flashscore-search, a Flashscore team URL, a match endpoint's team ids, or flashscore-team-squad and flashscore-player. A player id returns not found.
- **Params:** `id` (string, **required**) — Eight-character Flashscore team id

### `flashscore_team_fixtures`

- **HTTP:** `GET /flashscore/team-fixtures`
- **What:** Flashscore team fixtures. Returns one page of a team's upcoming matches, soonest first, as structured events with start time, both sides and competition. Event ids work with the flashscore match endpoints. Request successive pages until event_count is 0; a page past the end returns an empty list.
- **Params:** `id` (string, **required**) — Eight-character Flashscore team id; `page` (integer, optional) — 1-based page from 1 to 300; defaults to 1

### `flashscore_team_news`

- **HTTP:** `GET /flashscore/team-news`
- **What:** Flashscore team news headlines. Returns up to 100 recent headlines that Flashscore aggregates from news publishers for a team: title, publisher, publication time, image and a Flashscore link that redirects to the publisher's article. These are third-party headlines, separate from Flashscore's own articles in flashscore-news. Article text is not included.
- **Params:** `id` (string, **required**) — Eight-character Flashscore team id

### `flashscore_team_results`

- **HTTP:** `GET /flashscore/team-results`
- **What:** Flashscore team results. Returns one page of a team's finished and in-progress matches, newest first, as structured events with start time, stage, both sides, score and competition. Event ids work with the flashscore match endpoints. Request successive pages until event_count is 0; a page past the end returns an empty list.
- **Params:** `id` (string, **required**) — Eight-character Flashscore team id; `page` (integer, optional) — 1-based page from 1 to 300; defaults to 1

### `flashscore_team_squad`

- **HTTP:** `GET /flashscore/team-squad`
- **What:** Flashscore team squad. Returns a team's squad grouped by position (goalkeepers, defenders, and so on, plus the coach) with each person's jersey number, age, country (or club, for national teams), injury or absence note and season statistics. The default scope totals all competitions; the scopes list in every response names the per-competition scopes accepted by the scope parameter. Sports without a squad page return not found.
- **Params:** `id` (string, **required**) — Eight-character Flashscore team id; `scope` (string, optional) — Squad statistics scope key from the scopes list of a previous response (for example overall-all or league-SY30SsKF); defaults to overall-all; `slug` (string, optional) — Optional team slug; must match the id when supplied

### `flashscore_team_transfers`

- **HTTP:** `GET /flashscore/team-transfers`
- **What:** Flashscore team transfers. Returns one page (30 rows) of a team's transfer history, newest first: date, direction (in or out), type such as Loan or Transfer, fee text, the player and the clubs on each side. Filter by type to see arrivals or departures only. Request successive pages until transfer_count is 0.
- **Params:** `id` (string, **required**) — Eight-character Flashscore team id; `page` (integer, optional) — 1-based page from 1 to 300; defaults to 1; `type` (string, optional) — Transfer direction filter; defaults to all
