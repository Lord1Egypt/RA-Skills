# sports-scores-research — endpoint reference — Sportskeeda

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**48 endpoints across 1 platform group(s).**

## Sportskeeda (48)

### `sportskeeda_article`

- **HTTP:** `GET /sportskeeda/article`
- **What:** Get a Sportskeeda article. Returns public article metadata and body paragraphs for a Sportskeeda article slug. Discovered slugs may contain case-preserving percent-encoded characters. A canonical Sportskeeda URL remains accepted for existing clients. Provide exactly one of slug or url; use /sportskeeda/sections and /sportskeeda/sitemaps for topic discovery.
- **Params:** `slug` (string, optional) — Sportskeeda article path without host; preferred over url; `url` (string, optional) — Canonical Sportskeeda article URL; alternative to slug

### `sportskeeda_author`

- **HTTP:** `GET /sportskeeda/author`
- **What:** Get a Sportskeeda author profile. Returns a Sportskeeda author's profile, looked up by `slug` (for example `sripad`) or canonical `url`; at least one is required. The response has the name and the articles listed on the profile, each with title and URL, and can also carry `biography`, `role` and `image_url`.
- **Params:** `slug` (string, optional) — Sportskeeda author slug, e.g. sripad; `url` (string, optional) — Canonical Sportskeeda /author/<slug> URL; alternative to slug

### `sportskeeda_college_basketball_schedule`

- **HTTP:** `GET /sportskeeda/college-basketball-schedule`
- **What:** Get Sportskeeda college basketball games for a date. Returns all games and published scores for the requested date and season from Sportskeeda's first-party JSON feed. Discover valid season values with college-basketball-schedule-options. The upstream conference filter is currently unreliable and this endpoint does not accept it.
- **Params:** `date` (string, **required**) — Game date in YYYY-MM-DD format; `season` (integer, **required**) — Season starting year returned by college-basketball-schedule-options

### `sportskeeda_college_basketball_schedule_options`

- **HTTP:** `GET /sportskeeda/college-basketball-schedule-options`
- **What:** Discover college basketball schedule seasons and date window. Reads Sportskeeda's current college basketball schedule configuration. It returns every season from the published minimum through the current schedule season and the date-picker window. The conference selector is shown by the site, but its current-season feed metadata is incomplete.
- **Params:** `season` (integer, optional) — A season starting year from the live seasons list; defaults to the current schedule season

### `sportskeeda_cricket_commentary`

- **HTTP:** `GET /sportskeeda/cricket-commentary`
- **What:** Get Sportskeeda cricket ball-by-ball commentary. Returns the current commentary feed. To page to older events, pass a 24-character lowercase hexadecimal cursor from an event in /sportskeeda/cricket-match's commentary field (the full feed may contain zero-filled IDs); language then selects an upstream language. The match page's commentary selector offers en, hi, ta, te, and bho. Language without cursor is rejected because the upstream feed ignores it.
- **Params:** `cursor` (string, optional) — Nonzero 24-character lowercase hexadecimal commentary ID from /sportskeeda/cricket-match commentary; `language` (string, optional) — Older-comment language; valid only with cursor; `slug` (string, **required**) — Host-free match path returned by /sportskeeda/schedule

### `sportskeeda_cricket_match`

- **HTTP:** `GET /sportskeeda/cricket-match`
- **What:** Get a Sportskeeda cricket match center. Returns the public scorecard, innings, teams, squads, player data, and latest commentary for a cricket match slug discovered from /sportskeeda/schedule. Betting fields are excluded.
- **Params:** `slug` (string, **required**) — Host-free match path returned by /sportskeeda/schedule

### `sportskeeda_depth_chart`

- **HTTP:** `GET /sportskeeda/depth-chart`
- **What:** Get the NFL depth chart for all teams. Returns every team and listed position/player from the live NFL depth chart. Players and team detail pages include slugs when Sportskeeda links them.
- **Params:** `slug` (string, **required**) — Must be nfl/depth-chart

### `sportskeeda_draft_picks`

- **HTTP:** `GET /sportskeeda/draft-picks`
- **What:** Get all historical NFL team draft picks from Sportskeeda. Reads the complete public draft JSON asset, not only the rows initially visible on the page. Filter by year, round, position or player name. Discover each team's exact filter values with draft-picks-options. Source history and latest available year are published by Sportskeeda and may lag the current season.
- **Params:** `page` (integer, optional) — Page number, 1-1000; default 1; `per_page` (integer, optional) — Records per page, 1-500; default 100; `position` (string, optional) — Exact position from draft-picks-options; `q` (string, optional) — Case-insensitive player-name substring, at most 100 characters; `round` (string, optional) — Exact round from draft-picks-options; historical special labels are accepted; `slug` (string, **required**) — NFL team draft-picks page path without host; `year` (integer, optional) — Year from draft-picks-options; omit for all years

### `sportskeeda_draft_picks_options`

- **HTTP:** `GET /sportskeeda/draft-picks-options`
- **What:** Discover an NFL team's complete Sportskeeda draft filters. Reads the public draft JSON asset named by the team page and returns every available year, round and position, including historical special rounds. Team page slugs are discoverable from page-options on an NFL team overview.
- **Params:** `slug` (string, **required**) — NFL team draft-picks page path without host

### `sportskeeda_event_calendar`

- **HTTP:** `GET /sportskeeda/event-calendar`
- **What:** Get Sportskeeda regional sports calendar events. Returns all events from the embedded Sports Calendar, optionally filtered by an offered region-specific sport, one or more offered months, or an inclusive date range. Discover the current region, sport, and month values through /sportskeeda/event-calendar-options.
- **Params:** `end_date` (string, optional) — Inclusive range end in YYYY-MM-DD; provide together with start_date; `month` (array, optional) — One or more offered calendar months in YYYY-MM format; repeat this parameter for multiple months; `region` (string, optional) — Calendar region; `sport` (string, optional) — Exact sport label offered for the selected region; see event-calendar-options; `start_date` (string, optional) — Inclusive range start in YYYY-MM-DD; provide together with end_date

### `sportskeeda_event_calendar_options`

- **HTTP:** `GET /sportskeeda/event-calendar-options`
- **What:** Discover Sportskeeda calendar regions, sports, and months. Lists the regions (`us` and `india`) of the Sportskeeda event calendar, each with the sport names and `YYYY-MM` months currently on offer. Takes no parameters. Pass the exact `region`, `sport` and `month` values to `/sportskeeda/event-calendar`; no year parameter exists.
- **Params:** _none_

### `sportskeeda_feed`

- **HTTP:** `GET /sportskeeda/feed`
- **What:** Get articles from a Sportskeeda section or topic. Fetches the public article cards for a Sportskeeda section, event, team-news, or player-news slug. Page pagination is accepted only when the source advertises it.
- **Params:** `page` (integer, optional) — Source page, for feeds with pagination; defaults to 1; `slug` (string, **required**) — Sportskeeda path without host, such as wwe, go/epl, or player/jannik-sinner/news

### `sportskeeda_football_data`

- **HTTP:** `GET /sportskeeda/football-data`
- **What:** Get football fixtures and standings. Returns first-party football widget fixtures and standings. Event and optional matchday must be offered by football-options. Omit matchday for the widget's selected round. Scores and standings reflect upstream data, which may be stale.
- **Params:** `event` (string, **required**) — Tournament slug from football-options; current selector: featured, epl, uefa-champions-league, uefa-nations-league, la-liga, ligue-1, mls, bundesliga; `matchday` (string, optional) — Round slug from football-options for the selected event

### `sportskeeda_football_options`

- **HTTP:** `GET /sportskeeda/football-options`
- **What:** Discover football tournaments and matchdays. Lists the live football widget's tournament selector. With event, follows the full previous/next matchday chain and returns every currently offered round slug. The discovered values feed sportskeeda-football-data.
- **Params:** `event` (string, optional) — Live tournament slug; current selector: featured, epl, uefa-champions-league, uefa-nations-league, la-liga, ligue-1, mls, bundesliga. Omit to list tournaments only

### `sportskeeda_guessing_game`

- **HTTP:** `GET /sportskeeda/guessing-game`
- **What:** Get a Sportskeeda daily guessing-game puzzle. Returns the public clues and image metadata for a discovered player-guessing game and ISO date. The answer is omitted so the endpoint does not reveal the active puzzle solution.
- **Params:** `date` (string, **required**) — Puzzle date in YYYY-MM-DD format; `slug` (string, **required**) — Discovered host-free game page path

### `sportskeeda_guessing_game_entities`

- **HTTP:** `GET /sportskeeda/guessing-game-entities`
- **What:** List players for a Sportskeeda guessing game. Returns the live public entity list used by a discovered player-guessing game, including the game-specific team, position, and profile fields.
- **Params:** `slug` (string, **required**) — Discovered host-free game page path

### `sportskeeda_guessing_games`

- **HTTP:** `GET /sportskeeda/guessing-games`
- **What:** List Sportskeeda player-guessing games. Lists the player-guessing games currently linked on Sportskeeda. Each has a display `name`, a host-free page `slug` such as `wwe/brainbuster-wwe-player-guessing-game`, and its `game_slug`. Pass `slug` to `/sportskeeda/guessing-game` or `/sportskeeda/guessing-game-entities`. Takes no parameters.
- **Params:** _none_

### `sportskeeda_nba_queries`

- **HTTP:** `GET /sportskeeda/nba-queries`
- **What:** List Sportskeeda NBA player query pages. Pages through the server-rendered questions on Sportskeeda's Top NBA Queries page. Slugs are host-free and can be passed to sportskeeda_page_data for the linked player stats table. The live category directory is returned on every page.
- **Params:** `category` (string, optional) — Optional category id; `limit` (integer, optional) — Page size; 0 or omitted defaults to 100, maximum is 500; `offset` (integer, optional) — Zero-based result offset

### `sportskeeda_news`

- **HTTP:** `GET /sportskeeda/news`
- **What:** Get Sportskeeda's latest news. Returns the current public Sportskeeda news sitemap entries. Use /sportskeeda/sections to discover all navigation groups and sports landing pages, and /sportskeeda/taxonomy-search to search categories, events, teams, players, wiki pages, and wiki tags.
- **Params:** _none_

### `sportskeeda_page_data`

- **HTTP:** `GET /sportskeeda/page-data`
- **What:** Get Sportskeeda structured sports tables. Returns team, player, roster, leaderboard, ranking, depth, playoff, and game-log tables. NFL team stats include team-leader cards, player-category tables, and Basic, Advanced, and Expert team tables. Season and type are accepted only if offered by the selected page; discover their values with page-options. Player game-log seasons use their discovered season-specific path and return every table offered by the page; NFL category tabs are listed by page-options. College-football schedule slugs accept a discovered conference slug and filter the schedule rows; an offered group with no games on that week returns status no_data. The trade value chart has a separate endpoint. A page with no structured tables returns an upstream error.
- **Params:** `conference` (string, optional) — College-football schedule conference slug from page-options; `season` (integer, optional) — Season year offered by this page's page-options filter; `slug` (string, **required**) — Sportskeeda path without host; `type` (string, optional) — Season phase offered by this page's page-options filter; leaderboard pages offer pre, regular, post

### `sportskeeda_page_options`

- **HTTP:** `GET /sportskeeda/page-options`
- **What:** Discover Sportskeeda page menus and filters. Returns the page's live contextual menus, team and ranking links, tabs, schedule views, and every currently offered select-filter value. Leaderboard category and metric values carry their destination slugs. College-football schedule pages expose the client-side conference selector here.
- **Params:** `slug` (string, **required**) — Sportskeeda path without host

### `sportskeeda_player_stats`

- **HTTP:** `GET /sportskeeda/player-stats`
- **What:** Get NFL or NBA player season stats across event phases. Returns the season stats for an NFL or NBA player stats page. Without event_type, returns all event phases offered by that page's selector. NBA data may contain extra phases that the page does not offer; these are excluded. Discover the current event_type values with sportskeeda-page-options for the same slug.
- **Params:** `event_type` (string, optional) — Event phase offered by this player's stats-event-type-dropdown; NFL offers 0,1,2,3 and NBA offers 0,1,2; `slug` (string, **required**) — NFL or NBA player stats path without host

### `sportskeeda_profile`

- **HTTP:** `GET /sportskeeda/profile`
- **What:** Get a Sportskeeda player or team profile. Returns a Sportskeeda player or team profile by host-free `slug`, such as `player/jannik-sinner` or `nfl/green-bay-packers`. The response has its name, `kind`, a description, fact rows as name and value pairs (names vary by sport), and any news cards. A page without fact rows returns an upstream error.
- **Params:** `slug` (string, **required**) — Sportskeeda player or team profile path without host

### `sportskeeda_quiz`

- **HTTP:** `GET /sportskeeda/quiz`
- **What:** Get a Sportskeeda quiz definition. Returns public question prompts and choice text from a quiz page, sorted by question number. The source does not expose correct answers in its anonymous page data; answer checking and user submissions are not included.
- **Params:** `slug` (string, **required**) — Sportskeeda quiz path without host, discovered through /sportskeeda/quizzes

### `sportskeeda_quiz_categories`

- **HTTP:** `GET /sportskeeda/quiz-categories`
- **What:** List current Sportskeeda quiz categories. Lists the quiz categories currently linked from Sportskeeda's quiz hub, each with a `name` and a host-free `slug` such as `cricket/quiz`. Pass a `slug` to `sportskeeda-quizzes`. Takes no parameters, and the list changes with the site, so fetch it rather than assuming fixed categories.
- **Params:** _none_

### `sportskeeda_quizzes`

- **HTTP:** `GET /sportskeeda/quizzes`
- **What:** List quizzes in a Sportskeeda category. Returns public quiz cards for one category path discovered through /sportskeeda/quiz-categories. The source currently renders its first quiz page; page pagination is not exposed because the visible page links currently repeat the same cards.
- **Params:** `slug` (string, **required**) — Sportskeeda quiz category path without host

### `sportskeeda_salary_cap`

- **HTTP:** `GET /sportskeeda/salary-cap`
- **What:** Get NFL team salary-cap figures from Sportskeeda. Returns the source's published season, team totals, every player cap scenario and expanded salary breakdown. The site's player search and sortable columns are applied to the complete server-rendered rows. The published season may lag the current season.
- **Params:** `order` (string, optional) — Sort direction; requires sort_by; default asc; `q` (string, optional) — Case-insensitive player-name substring, at most 100 characters; `slug` (string, **required**) — NFL team salary-cap page path without host; `sort_by` (string, optional) — Sortable column; omit to preserve source order

### `sportskeeda_schedule`

- **HTTP:** `GET /sportskeeda/schedule`
- **What:** Get Sportskeeda fixtures and results. Returns a Sportskeeda fixtures or schedule page by host-free `slug`, such as `nfl/schedule` or `cricket/schedule`. Cricket and football give `matches` with teams, time, status, score, competition, venue and result; other sports give `tables` with `columns` and `rows`. An empty fixture widget returns `status` `no_matches`.
- **Params:** `slug` (string, **required**) — Sportskeeda schedule path without host

### `sportskeeda_sections`

- **HTTP:** `GET /sportskeeda/sections`
- **What:** Discover Sportskeeda sections and topics. Returns the live parent/child navigation tree, including external destinations marked explicitly, plus every public sports landing URL from Sportskeeda's sports sitemap.
- **Params:** _none_

### `sportskeeda_sitemap_items`

- **HTTP:** `GET /sportskeeda/sitemap-items`
- **What:** Page through a Sportskeeda sitemap. Returns canonical URLs and host-free path slugs from one sitemap discovered by /sportskeeda/sitemaps. Returned path slugs preserve case and percent-encode unusual characters. A sitemap_url remains accepted for existing callers. Provide exactly one; the source is checked against the live index and robots sitemap list on each call.
- **Params:** `limit` (integer, optional) — Page size from 1 to 500; defaults to 100; `offset` (integer, optional) — Zero-based item offset; `sitemap_url` (string, optional) — Exact sitemap URL; alternative to slug; `slug` (string, optional) — Sitemap slug returned by /sportskeeda/sitemaps; preferred

### `sportskeeda_sitemaps`

- **HTTP:** `GET /sportskeeda/sitemaps`
- **What:** Discover Sportskeeda sitemap sources. Returns Sportskeeda's current public sitemaps. Pass a returned slug to /sportskeeda/sitemap-items to page through its complete URL set.
- **Params:** _none_

### `sportskeeda_standings`

- **HTTP:** `GET /sportskeeda/standings`
- **What:** Get Sportskeeda standings or rankings. Returns Sportskeeda standings or rankings tables for a host-free `slug`, such as `nfl/standings`, with column labels, rows, linked cell slugs and view slugs. `season` (starting year, 2013 to 2026) applies only to college basketball standings. The current college basketball season returns `status` `no_data` with empty `tables`.
- **Params:** `season` (integer, optional) — College basketball season starting year; live values from standings-options; `slug` (string, **required**) — Sportskeeda standings or rankings path without host

### `sportskeeda_standings_options`

- **HTTP:** `GET /sportskeeda/standings-options`
- **What:** Discover Sportskeeda college standings seasons and conferences. Lists the seasons and conferences available for Sportskeeda college basketball standings. `slug` is required and must be `college-basketball/college-basketball-standings`. Without `season` you get all offered season years and the current season's conferences; with it, that season's conferences, each with a name and a slug usable as the standings `slug`.
- **Params:** `season` (integer, optional) — A live-offered starting year; selects its conference list; `slug` (string, **required**) — College basketball standings slug

### `sportskeeda_taxonomy_search`

- **HTTP:** `GET /sportskeeda/taxonomy-search`
- **What:** Search Sportskeeda categories and entities. Calls Sportskeeda's anonymous frontend taxonomy search across categories, events, teams, players, wiki pages, and wiki tags. The upstream UI always searches all six types; the q phrase is sanitized and capped at 100 characters just like the site.
- **Params:** `q` (string, **required**) — Search phrase; punctuation is replaced with spaces and the result is capped at 100 characters

### `sportskeeda_topic`

- **HTTP:** `GET /sportskeeda/topic`
- **What:** Get a Sportskeeda topic or entity overview's full content. Returns ordered prose, headings, lists, tables, images and embeds from a public topic, event, team or player overview page, plus available byline, modification text and related stories. Discover slugs with /sportskeeda/sitemap-items using tags.xml, tournaments.xml, teams.xml, players.xml or us-sitemap.xml. Pages without a CMS body return an upstream error.
- **Params:** `slug` (string, **required**) — Canonical Sportskeeda topic, event, team or player path without host

### `sportskeeda_trade_values`

- **HTTP:** `GET /sportskeeda/trade-values`
- **What:** Get NFL redraft or dynasty trade values. Reads the same anonymous JSON asset as the public chart. Returns source update time, ranks, values, and linked player slugs. The All position includes all source rows, including positions not displayed as chart sections. Discover current chart and filter choices with page-options.
- **Params:** `limit` (integer, optional) — Page size from 1 to 500; `offset` (integer, optional) — Zero-based player offset; `position` (string, optional) — Displayed position section; defaults to All; `scoring` (string, optional) — Scoring system; defaults to ppr; `slug` (string, **required**) — Chart path without host; `superflex` (boolean, optional) — Use superflex chart; defaults to false

### `sportskeeda_transactions`

- **HTTP:** `GET /sportskeeda/transactions`
- **What:** Get complete monthly NFL league or team transactions. Reads the first-party public transaction feed in month-sized windows, avoiding its 10000-row broad-range cap. Discover accepted seasons, months, and team slugs with sportskeeda-transactions-options.
- **Params:** `month` (string, **required**) — MMYYYY month code from transactions-options for the selected season; current live union is listed here; `page` (integer, optional) — Page number, 1-1000; default 1; `per_page` (integer, optional) — Records per page, 1-500; default 100; `season` (integer, optional) — Season start year; current live choices: 2020,2021,2022,2023,2024,2025,2026; defaults to current; `slug` (string, optional) — Host-free page slug; nfl/transactions or an NFL team transactions slug

### `sportskeeda_transactions_options`

- **HTTP:** `GET /sportskeeda/transactions-options`
- **What:** List NFL transaction seasons, months and team slugs. Discovers the complete live NFL transaction season list, months for the selected season, and all team transaction page slugs. Use these values with sportskeeda-transactions.
- **Params:** `season` (integer, optional) — Season start year; current live choices: 2020,2021,2022,2023,2024,2025,2026; defaults to current

### `sportskeeda_video`

- **HTTP:** `GET /sportskeeda/video`
- **What:** Get Sportskeeda video metadata. Returns metadata for one Sportskeeda video page by host-free `slug`, such as `cricket/sunil-naraine-batting-cpl`: its id, title, poster image, stream URL and, when available, a description. A page without a video player returns an upstream error, and stream availability can depend on geography.
- **Params:** `slug` (string, **required**) — Individual Sportskeeda video page path without host

### `sportskeeda_videos`

- **HTTP:** `GET /sportskeeda/videos`
- **What:** List Sportskeeda videos and channels. Lists video cards from Sportskeeda's main video library, or from a listing given by `slug` (default `videos`, for example `go/epl/videos`). Items have a title, slug, URL, and thumbnail, duration and channel when present. The response also lists channels with their slugs. An empty or blocked listing returns an upstream error.
- **Params:** `slug` (string, optional) — Video listing path without host; defaults to videos

### `sportskeeda_wiki_activity`

- **HTTP:** `GET /sportskeeda/wiki-activity`
- **What:** List accepted edits for a Sportskeeda Wiki page. Returns the public accepted activity history for one Wiki article, with bounded pagination and the page's live sort fields. The source page slug is obtained from sportskeeda-wiki-pages.
- **Params:** `limit` (integer, optional) — Activity items per page; `page` (integer, optional) — 1-based page; `slug` (string, **required**) — Host-free Wiki page path_slug from sportskeeda-wiki-pages; `sort` (string, optional) — Sort direction; `sort_by` (string, optional) — Activity sort field

### `sportskeeda_wiki_article`

- **HTTP:** `GET /sportskeeda/wiki-article`
- **What:** Get a Sportskeeda Wiki article. Returns the rendered article title, metadata, and body paragraphs. Pass the path_slug returned by sportskeeda-wiki-pages; URL and host input are not accepted.
- **Params:** `slug` (string, **required**) — Host-free Wiki page path_slug from sportskeeda-wiki-pages

### `sportskeeda_wiki_categories`

- **HTTP:** `GET /sportskeeda/wiki-categories`
- **What:** List Sportskeeda Wiki categories. Returns the nested category menu of one Sportskeeda Wiki project, chosen by `wiki` (`minecraft`, `terraria`, `naruto`, `tiktok`, `youtube`, `gta`, `one-piece` or `sk-communities`). Each category has a title, slug, `path_slug`, taxonomy id, sequence and `children`. Category names, ids and paths change over time.
- **Params:** `wiki` (string, **required**) — Project slug returned by sportskeeda-wiki-options

### `sportskeeda_wiki_contributors`

- **HTTP:** `GET /sportskeeda/wiki-contributors`
- **What:** List contributors to a Sportskeeda Wiki page. Returns public accepted contributors for one Wiki article. The source page slug is obtained from sportskeeda-wiki-pages; user IP and private account fields are never returned.
- **Params:** `limit` (integer, optional) — Contributors per page; `page` (integer, optional) — 1-based page; `slug` (string, **required**) — Host-free Wiki page path_slug from sportskeeda-wiki-pages; `sort` (string, optional) — Sort direction; `sort_by` (string, optional) — Contributor sort field

### `sportskeeda_wiki_issues`

- **HTTP:** `GET /sportskeeda/wiki-issues`
- **What:** List reported issues for a Sportskeeda Wiki page. Returns public opened or closed issues for one Wiki article. The upstream also returns submitter IP addresses; this endpoint deliberately omits them.
- **Params:** `limit` (integer, optional) — Issues per page; `page` (integer, optional) — 1-based page; `slug` (string, **required**) — Host-free Wiki page path_slug from sportskeeda-wiki-pages; `status` (string, optional) — Issue status

### `sportskeeda_wiki_options`

- **HTTP:** `GET /sportskeeda/wiki-options`
- **What:** List Sportskeeda Wiki projects. Lists the Sportskeeda Wiki projects, each with a `slug`, display `name`, `taxonomy_id` and `taxonomy_slug`. Current slugs are `minecraft`, `terraria`, `naruto`, `tiktok`, `youtube`, `gta`, `one-piece` and `sk-communities`. Use a `slug` with `wiki-categories` and `wiki-pages`. Takes no parameters.
- **Params:** _none_

### `sportskeeda_wiki_pages`

- **HTTP:** `GET /sportskeeda/wiki-pages`
- **What:** Search and paginate Sportskeeda Wiki pages. Returns catalog pages for one Wiki project. Use path_slug as the preferred host-free slug for sportskeeda-wiki-article. total_items is the record count; the upstream field named total_pages is mislabelled and does not mean page count.
- **Params:** `limit` (integer, optional) — Items per page; `page` (integer, optional) — 1-based catalog page; `search` (string, optional) — Title or page search text; sent upstream as searchText; `sort` (string, optional) — Sort direction; `sort_by` (string, optional) — Catalog field to sort by; `wiki` (string, **required**) — Project slug returned by sportskeeda-wiki-options

### `sportskeeda_wiki_summary`

- **HTTP:** `GET /sportskeeda/wiki-summary`
- **What:** Get community counts for a Sportskeeda Wiki page. Returns accepted contributor and activity totals plus the open-issue count for one Wiki article. The source page slug is obtained from sportskeeda-wiki-pages.
- **Params:** `slug` (string, **required**) — Host-free Wiki page path_slug from sportskeeda-wiki-pages
