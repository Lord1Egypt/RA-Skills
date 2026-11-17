# yahoo-network-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**87 endpoints across 8 platform group(s).**

## Yahoo Autos (3)

### `yahoo_autos_article`

- **HTTP:** `GET /yahoo-autos/article`
- **What:** Yahoo Autos article content. Returns a single Yahoo Autos article's full content: title, description, author, publish/update time, section, image, keywords, original publisher, and body paragraphs. Accepts a canonical autos.yahoo.com article URL, such as one returned by the home or category story streams.
- **Params:** `url` (string, **required**) — Canonical autos.yahoo.com article URL

### `yahoo_autos_category`

- **HTTP:** `GET /yahoo-autos/category`
- **What:** Yahoo Autos section story stream. Returns a Yahoo Autos section's editorial story feed: title, destination URL, category, and thumbnail image for each story, with page-based pagination. Sourced from Yahoo Autos's own server-rendered section pages.
- **Params:** `category` (string, **required**) — Yahoo Autos section; `page` (integer, optional) — 1-based page number, defaults to 1

### `yahoo_autos_home`

- **HTTP:** `GET /yahoo-autos/home`
- **What:** Yahoo Autos homepage story stream. Returns Yahoo Autos's homepage editorial story feed: title, destination URL, category, and thumbnail image for each story. Sourced from Yahoo Autos's own server-rendered homepage.
- **Params:** _none_

## Yahoo Entertainment (3)

### `yahoo_entertainment_article`

- **HTTP:** `GET /yahoo-entertainment/article`
- **What:** Yahoo Entertainment article content. Returns a single Yahoo Entertainment article's full content: title, description, author, publish/update time, section, image, keywords, original publisher, and body paragraphs. Accepts a canonical www.yahoo.com/entertainment/ article URL, such as one returned by the home or category story streams.
- **Params:** `url` (string, **required**) — Canonical www.yahoo.com/entertainment/ article URL

### `yahoo_entertainment_category`

- **HTTP:** `GET /yahoo-entertainment/category`
- **What:** Yahoo Entertainment section story stream. Returns a Yahoo Entertainment section's editorial story feed: title, destination URL, category, and thumbnail image for each story, with page-based pagination. Sourced from Yahoo Entertainment's own server-rendered section pages.
- **Params:** `category` (string, **required**) — Yahoo Entertainment section; `page` (integer, optional) — 1-based page number, defaults to 1

### `yahoo_entertainment_home`

- **HTTP:** `GET /yahoo-entertainment/home`
- **What:** Yahoo Entertainment homepage story stream. Returns Yahoo Entertainment's homepage editorial story feed: title, destination URL, category, and thumbnail image for each story. Sourced from Yahoo Entertainment's own server-rendered homepage.
- **Params:** _none_

## Yahoo Health (3)

### `yahoo_health_article`

- **HTTP:** `GET /yahoo-health/article`
- **What:** Yahoo Health article content. Returns a single Yahoo Health article's full content: title, description, author, publish/update time, section, image, keywords, original publisher, and body paragraphs. Accepts a canonical health.yahoo.com article URL, such as one returned by the home or category story streams.
- **Params:** `url` (string, **required**) — Canonical health.yahoo.com article URL

### `yahoo_health_category`

- **HTTP:** `GET /yahoo-health/category`
- **What:** Yahoo Health section story stream. Returns a Yahoo Health section's editorial story feed: title, destination URL, category, and thumbnail image for each story, with page-based pagination. Sourced from Yahoo Health's own server-rendered section pages.
- **Params:** `category` (string, **required**) — Yahoo Health section; `page` (integer, optional) — 1-based page number, defaults to 1

### `yahoo_health_home`

- **HTTP:** `GET /yahoo-health/home`
- **What:** Yahoo Health homepage story stream. Returns Yahoo Health's homepage editorial story feed: title, destination URL, category, and thumbnail image for each story. Sourced from Yahoo Health's own server-rendered homepage.
- **Params:** _none_

## Yahoo Life (2)

### `yahoo_life_article`

- **HTTP:** `GET /yahoo-life/article`
- **What:** Yahoo Life article content. Returns a single Yahoo Life article's full content: title, description, author, publish/update time, section, image, keywords, original publisher, and body paragraphs. Accepts a canonical www.yahoo.com/lifestyle article URL, such as one returned by the home story stream.
- **Params:** `url` (string, **required**) — Canonical www.yahoo.com/lifestyle article URL

### `yahoo_life_home`

- **HTTP:** `GET /yahoo-life/home`
- **What:** Yahoo Life homepage story stream. Returns Yahoo Life's homepage editorial story feed: title, destination URL, and thumbnail image for each story. Sourced from Yahoo Life's own server-rendered homepage.
- **Params:** _none_

## Yahoo News (7)

### `yahoo_news_article`

- **HTTP:** `GET /yahoo-news/article`
- **What:** Yahoo News article content. Returns a single Yahoo News article's full content: headline, description, author, publish/update time, section, image, keywords, original publisher, and body paragraphs. Accepts a canonical yahoo.com/news article URL, such as one returned by the home or category story streams.
- **Params:** `url` (string, **required**) — Canonical www.yahoo.com/news article URL

### `yahoo_news_category`

- **HTTP:** `GET /yahoo-news/category`
- **What:** Yahoo News section story stream. Returns a Yahoo News section's story stream: title, destination URL, summary, source, publish time, comment count, and thumbnail images for each story. Sourced from Yahoo News's own server-rendered section pages.
- **Params:** `category` (string, **required**) — Yahoo News section

### `yahoo_news_comment_replies`

- **HTTP:** `GET /yahoo-news/comments/replies`
- **What:** Yahoo News comment replies. Returns a page of a comment's replies: author, body, reaction counts, and pin status, with sort order and cursor-based pagination. Sourced from Yahoo's own comment platform gateway.
- **Params:** `comment_id` (string, **required**) — Parent comment id (the id field returned by /yahoo-news/comments); `content_id` (string, **required**) — Article id (the id field returned by home/category/article); `count` (integer, optional) — Number of replies to return, default 10, clamped to 1..50; `cursor` (string, optional) — Pagination cursor from a previous response's next_cursor; `sort` (string, optional) — Sort order, defaults to newest

### `yahoo_news_comments`

- **HTTP:** `GET /yahoo-news/comments`
- **What:** Yahoo News article comments. Returns a page of an article's top-level comments: author, body, reaction counts, reply count, and pin status, with sort order and cursor-based pagination. Sourced from Yahoo's own comment platform gateway.
- **Params:** `content_id` (string, **required**) — Article id (the id field returned by home/category/article); `count` (integer, optional) — Number of comments to return, default 10, clamped to 1..50; `cursor` (string, optional) — Pagination cursor from a previous response's next_cursor; `sort` (string, optional) — Sort order, defaults to top

### `yahoo_news_home`

- **HTTP:** `GET /yahoo-news/home`
- **What:** Yahoo News homepage story stream. Returns Yahoo News's homepage "need to know" story stream: title, destination URL, summary, source, publish time, comment count, and thumbnail images for each story. Sourced from Yahoo News's own server-rendered homepage.
- **Params:** _none_

### `yahoo_news_related`

- **HTTP:** `GET /yahoo-news/related`
- **What:** Yahoo News related articles. Returns a page of articles Yahoo recommends alongside a given article -- the "you may also like" strip at the bottom of an article page -- with cursor-based pagination. Sourced from Yahoo's own recommendation gateway.
- **Params:** `content_id` (string, **required**) — Article id (the id field returned by home/category/article); `count` (integer, optional) — Number of related articles to return, default 10, clamped to 1..50; `cursor` (string, optional) — Pagination cursor from a previous response's next_cursor

### `yahoo_news_suggest`

- **HTTP:** `GET /yahoo-news/suggest`
- **What:** Yahoo News search autocomplete suggestions. Returns Yahoo News search-box autocomplete suggestions for the required partial query `q`, as a flat list of suggested news search terms in `suggestions`. `count` sets how many (default 10, clamped to 1 to 20). A query with no matches returns an empty array, not an error. The response also has `query` and `fetched_at`.
- **Params:** `count` (integer, optional) — Number of suggestions to return, default 10, clamped to 1..20; `q` (string, **required**) — Partial search query to autocomplete

## Yahoo Shopping (13)

### `yahoo_shopping_article`

- **HTTP:** `GET /yahoo-shopping/article`
- **What:** Yahoo Shopping article content. Returns a single Yahoo Shopping article's full content: title, description, author, publish/update time, section, image, keywords, original publisher, and body paragraphs. Accepts a canonical shopping.yahoo.com article URL, such as one returned by the home or category story streams.
- **Params:** `url` (string, **required**) — Canonical shopping.yahoo.com article URL

### `yahoo_shopping_author`

- **HTTP:** `GET /yahoo-shopping/author`
- **What:** Yahoo Shopping author profile and article archive. Fetches one Yahoo Shopping contributor profile and a page of the author's article archive. Use the author slug from author_url in /yahoo-shopping/article; page follows Yahoo's path-segment pagination. Article cards may link to sibling publishers such as AOL.
- **Params:** `author` (string, **required**) — Yahoo Shopping author slug; use author_url from /yahoo-shopping/article; `page` (integer, optional) — 1-based article archive page, defaults to 1

### `yahoo_shopping_categories`

- **HTTP:** `GET /yahoo-shopping/categories`
- **What:** Yahoo Shopping navigation and article shortcuts. Returns the live editorial sections and nested topics accepted by /yahoo-shopping/category, plus the current direct article shortcuts in the Gift Ideas and Shopping Guides menus. Those article links are not extra category or filter values. Stores and Shopping Lists have separate directory endpoints.
- **Params:** _none_

### `yahoo_shopping_category`

- **HTTP:** `GET /yahoo-shopping/category`
- **What:** Yahoo Shopping section story stream. Returns the story cards displayed by a Yahoo Shopping section or nested topic, with page-based pagination. Some curated sections include cross-category or sibling Yahoo links. Use /yahoo-shopping/categories to discover the complete parent/topic taxonomy.
- **Params:** `category` (string, **required**) — Yahoo Shopping section; `page` (integer, optional) — 1-based page number, defaults to 1; `subcategory` (string, optional) — Nested topic slug valid under its parent category; see /yahoo-shopping/categories

### `yahoo_shopping_experts`

- **HTTP:** `GET /yahoo-shopping/experts`
- **What:** Yahoo Shopping featured expert roster. Returns the contributor cards in the public "More Yahoo experts" carousel on Yahoo Shopping's team profile. Use yahoo-shopping-author for one contributor's profile and paginated article archive.
- **Params:** _none_

### `yahoo_shopping_home`

- **HTTP:** `GET /yahoo-shopping/home`
- **What:** Yahoo Shopping homepage story stream. Returns Yahoo Shopping's homepage editorial story feed: title, destination URL, category, and thumbnail image for each story. Page follows Yahoo's own path-segment pagination. This is Yahoo's shopping buying-guide/deals content site, not a product-results API.
- **Params:** `page` (integer, optional) — 1-based page number, defaults to 1

### `yahoo_shopping_shopping_list`

- **HTTP:** `GET /yahoo-shopping/shopping-list`
- **What:** Yahoo Shopping curated list items. Returns one curated Yahoo Shopping list's items: product title, direct destination URL, image, seller, currency, price, and sale price for each item. Sourced from the list page's own product cards. Use GET /yahoo-shopping/shopping-lists to find a list's slug.
- **Params:** `list` (string, **required**) — List slug from GET /yahoo-shopping/shopping-lists

### `yahoo_shopping_shopping_lists`

- **HTTP:** `GET /yahoo-shopping/shopping-lists`
- **What:** Yahoo Shopping curated shopping-lists directory. Returns Yahoo Shopping's curated shopping-lists directory: a slug, title, and image for each themed list (e.g. "Cooling Essentials", "Back to School"). Use a list's slug with GET /yahoo-shopping/shopping-list to read its items.
- **Params:** _none_

### `yahoo_shopping_sitemap`

- **HTTP:** `GET /yahoo-shopping/sitemap`
- **What:** Yahoo Shopping sitemap archive or date page. Reads a canonical Yahoo Shopping sitemap index, section archive, or date page. Responses contain section archives, monthly archive links, day links, or article links depending on the page. Yahoo's date pages currently have broken previous/next links; this endpoint reports observed links and does not synthesize continuation.
- **Params:** `url` (string, **required**) — Canonical shopping.yahoo.com sitemap page URL from /yahoo-shopping/sitemaps or a prior response

### `yahoo_shopping_sitemaps`

- **HTTP:** `GET /yahoo-shopping/sitemaps`
- **What:** Yahoo Shopping sitemap section index. Returns the public sitemap's full set of section and seasonal archive links. Use /yahoo-shopping/sitemap to read an archive or date page.
- **Params:** _none_

### `yahoo_shopping_store`

- **HTTP:** `GET /yahoo-shopping/store`
- **What:** Yahoo Shopping retailer store deals. Returns one retailer's current deals on Yahoo Shopping: product title, direct retailer product URL, image, brand, currency, price, and sale price for each offer. Sourced from the retailer's shopping.yahoo.com store page's own structured product data -- not a keyword search, a fixed set of currently-featured deals for that retailer. Use GET /yahoo-shopping/stores to find a retailer's slug.
- **Params:** `store` (string, **required**) — Retailer slug from GET /yahoo-shopping/stores

### `yahoo_shopping_stores`

- **HTTP:** `GET /yahoo-shopping/stores`
- **What:** Yahoo Shopping retailer store directory. Returns Yahoo Shopping's retailer store directory: a slug, display name, and logo image for each retailer with a dedicated store page (e.g. Amazon, Target, Best Buy). Use a store's slug with GET /yahoo-shopping/store to read its current deals.
- **Params:** _none_

### `yahoo_shopping_suggest`

- **HTTP:** `GET /yahoo-shopping/suggest`
- **What:** Yahoo Shopping autocomplete suggestions. Returns suggestions from the typeahead endpoint used by Yahoo Shopping's search box. Yahoo does not expose a working Shopping product-results grid or product filters; this route provides autocomplete only.
- **Params:** `count` (integer, optional) — Upstream suggestion count; omitted defaults to 10, zero/negative values preserve Yahoo's empty-result behavior, and values above 20 are capped; `q` (string, **required**) — Partial search query

## Yahoo Sports (53)

### `yahoo_sports_college_rankings`

- **HTTP:** `GET /yahoo-sports/college-rankings`
- **What:** Yahoo Sports college football and basketball rankings. Returns rankings from Yahoo's public NCAAF, NCAAB, or NCAAW rankings page using the page's own public Graphite rankings operation. Poll Type and Poll Date are validated against the live filter catalog returned in this response. Conference filters are also returned, but are client-side on Yahoo's page and are not applied by this endpoint.
- **Params:** `date` (string, optional) — Exact Poll Date selector value from the live catalog (college football only); `league` (string, **required**) — College ranking league; `poll_type` (string, optional) — Exact Poll Type value from the live rankings filter catalog; defaults to the page's current poll; `tz` (string, optional) — Optional IANA timezone for game times embedded in ranking rows; defaults to UTC

### `yahoo_sports_draft`

- **HTTP:** `GET /yahoo-sports/draft`
- **What:** Yahoo Sports NFL and NBA Draft hub. Returns Yahoo's Drafted Players, Mock Draft, Big Board, or News tab for NFL or NBA, together with the live tab list and exact client-side round/team/position/school/attribute/board selectors shown by that page. The selectors filter data in the browser, so this endpoint returns the complete upstream page data and exposes filter values without applying server-side filters.
- **Params:** `league` (string, **required**) — Yahoo draft league; use yahoo-sports-leagues (draft=true); `view` (string, optional) — Yahoo Draft page: results, mock, big-board, or news; defaults to results

### `yahoo_sports_dropdown_catalog`

- **HTTP:** `GET /yahoo-sports/dropdown-catalog`
- **What:** Yahoo Sports team and category dropdown data. Returns Yahoo's full current menu data for NFL, NHL, NBA, MLB, WNBA, college rank polls, all soccer leagues exposed by the public dropdown operation, and sportsbook-legal states. Team and league objects retain Yahoo's IDs and links for use with matching Yahoo Sports endpoints.
- **Params:** _none_

### `yahoo_sports_game`

- **HTTP:** `GET /yahoo-sports/game`
- **What:** Yahoo Sports game boxscore. Returns one source game boxscore with matchup, line score and team stat totals, plus Yahoo's play-by-play and win-probability timeline when available. Event objects retain Yahoo's sport-specific fields. Use league plus game for direct league pages, or league=soccer with the exact game_url from a soccer scoreboard for competitions whose game path is published per match.
- **Params:** `game` (string, optional) — Yahoo game slug for direct league pages; supply game or game_url; `game_url` (string, optional) — Exact game.url from a soccer scoreboard; requires league=soccer and cannot be combined with game; `league` (string, **required**) — League key

### `yahoo_sports_golf_leaderboard`

- **HTTP:** `GET /yahoo-sports/golf-leaderboard`
- **What:** Yahoo Sports golf tournament leaderboard. Returns one golf tournament's full leaderboard (every golfer's rank, to-par score, status, holes-completed-in-current-round, per-round strokes, and a fixed stat set: earnings, eagles, birdies, pars, bogeys, double bogeys), from Yahoo Sports' own public tournament-leaderboard JSON API. Get the `tournament` id from a golf-schedule response's `id` field, e.g. `golf.e.23`.
- **Params:** `season` (integer, optional) — 4-digit season year (a tournament id is reused across years); defaults to the tournament's most recent season; `tournament` (string, **required**) — Yahoo Sports golf tournament id from a golf-schedule response's id field

### `yahoo_sports_golf_player`

- **HTTP:** `GET /yahoo-sports/golf-player`
- **What:** Yahoo Sports golf player profile. Returns one golfer's profile, current-season stats, and tournament-by-tournament history from Yahoo's public player page. Supply the canonical player URL from golf-players or another Yahoo golf response.
- **Params:** `player_url` (string, **required**) — Canonical Yahoo Golf player profile URL

### `yahoo_sports_golf_player_news`

- **HTTP:** `GET /yahoo-sports/golf-player-news`
- **What:** Yahoo Sports golf player news. Returns the story and video edges in one golfer's News tab. Latest mode returns Yahoo's opaque cursor and supports the same upstream cursor POST for subsequent pages.
- **Params:** `cursor` (string, optional) — Opaque next_cursor returned by a previous latest response; `mode` (string, optional) — Top News or Latest; `player_url` (string, **required**) — Canonical Yahoo Golf player URL

### `yahoo_sports_golf_players`

- **HTTP:** `GET /yahoo-sports/golf-players`
- **What:** Yahoo Sports golf player directory. Returns Yahoo's full current-and-retired golfers directory, grouped by last-name initial. The site's A-Z buttons filter the already-loaded list in the browser, so this endpoint returns the complete source list.
- **Params:** _none_

### `yahoo_sports_golf_schedule`

- **HTTP:** `GET /yahoo-sports/golf-schedule`
- **What:** Yahoo Sports golf tournament schedule. Returns a golf tour's tournament schedule for a season (name, dates, status, purse, and venue), from Yahoo Sports' own public sources. The `tour` enum accepts `pga-tour`, `pga-european-tours`, `lpga-tour`, `champions-tour`, `european-tour`, and `korn-ferry-tour`. Korn Ferry Tour schedule data comes from the Golf page's own server-rendered schedule; the other tours use Yahoo's public tournament-schedule JSON API. Each tournament's `id` feeds the golf-leaderboard endpoint's `tournament` parameter.
- **Params:** `season` (integer, optional) — 4-digit season year; defaults to the tour's current season; `tour` (string, **required**) — Golf tour key

### `yahoo_sports_home`

- **HTTP:** `GET /yahoo-sports/home`
- **What:** Yahoo Sports home-page stories. Returns the article cards currently embedded on the Yahoo Sports home page, including each card's title, summary, publisher, publication time, canonical URL, and complete upstream tag list.
- **Params:** _none_

### `yahoo_sports_injury_report`

- **HTTP:** `GET /yahoo-sports/injury-report`
- **What:** Yahoo Sports injury report. Returns Yahoo's current injury table for NFL, NBA, MLB, or NHL. Omit team_id for the page's All Teams view, or provide a Yahoo team ID from yahoo-sports-dropdown-catalog. Each injury row preserves Yahoo's player, position, status, injury description, and start date.
- **Params:** `league` (string, **required**) — League with an injury page; `team_id` (string, optional) — Optional Yahoo team ID from yahoo-sports-dropdown-catalog; omit for All Teams

### `yahoo_sports_league_schedule`

- **HTTP:** `GET /yahoo-sports/league-schedule`
- **What:** Yahoo Sports league schedule games. Returns full game records for the selected date or week from Yahoo's league schedule page. Use yahoo-sports-schedule-catalog for the current seasons, week/phase pairs and NCAA conference/division filter values. The page's own leagueFilter query is applied by Yahoo before the response is parsed.
- **Params:** `date` (string, optional) — Optional date filter in YYYY-MM-DD form; for schedule pages with date tabs; `league` (string, **required**) — Yahoo league key; `leagueFilter` (string, optional) — Exact leagueFilter value from the schedule catalog (NCAAF/NCAAB/NCAAW conference, division or Top 25 option); `season` (integer, optional) — Optional season year from yahoo-sports-schedule-catalog; `seasonPhase` (string, optional) — Optional week phase from the catalog; `week` (integer, optional) — Optional week value from yahoo-sports-schedule-catalog

### `yahoo_sports_leagues`

- **HTTP:** `GET /yahoo-sports/leagues`
- **What:** Yahoo Sports league catalog. Returns all 24 core league keys, source namespaces, and feature flags, plus the complete supported value sets for player search, injuries, NFL/NBA Draft, college rankings, golf tours, tennis ranking types, and motorsports series. Use dedicated soccer scoreboard, rankings, stats, schedule, bracket, sportsbook, RSS, and dropdown catalogs for live filter values.
- **Params:** _none_

### `yahoo_sports_mma_fight_card`

- **HTTP:** `GET /yahoo-sports/mma-fight-card`
- **What:** Yahoo Sports MMA fight card. Returns the current/next UFC event's full fight card (each bout's fighters, records, rankings, weight class, and card position), from Yahoo Sports' own server-rendered MMA schedule page. This endpoint takes no parameters -- it always returns whichever event Yahoo currently features as next up, not a caller-selected one.
- **Params:** _none_

### `yahoo_sports_mma_schedule`

- **HTTP:** `GET /yahoo-sports/mma-schedule`
- **What:** Yahoo Sports MMA event schedule. Returns the known UFC event calendar (name, date, status), from Yahoo Sports' own server-rendered MMA schedule page. This endpoint is UFC-only and takes no parameters -- Yahoo's own page does not expose Bellator, PFL, ONE Championship, or other promotions from this URL.
- **Params:** _none_

### `yahoo_sports_more_news`

- **HTTP:** `GET /yahoo-sports/more-news`
- **What:** Yahoo Sports More News feed. Returns one page from Yahoo Sports' public More News feed using its page-number routes. Story items preserve the source fields as raw objects. The page exposes no server-side tag, sort, or topic filter; use yahoo-sports-topic-news for a topic-specific page.
- **Params:** `page` (integer, optional) — 1-based Yahoo More News page number; defaults to 1

### `yahoo_sports_motorsports_race`

- **HTTP:** `GET /yahoo-sports/motorsports-race`
- **What:** Yahoo Sports motorsports race results. Returns one race's full driver-by-driver results (finishing position, driver, car/team, points, laps, time), from Yahoo Sports' own server-rendered race page. The `series` enum accepts `f1` and `nascar`. Get the `race` slug from a motorsports-schedule response's race `url` (the last path segment), e.g. `australian-grand-prix-2026-2961`.
- **Params:** `race` (string, **required**) — Yahoo Sports race slug from a motorsports-schedule response's race url; `series` (string, **required**) — Motorsports series key

### `yahoo_sports_motorsports_schedule`

- **HTTP:** `GET /yahoo-sports/motorsports-schedule`
- **What:** Yahoo Sports motorsports season schedule. Returns a series' season race list (name, date, status, laps, distance, pole/race winner, venue), from Yahoo Sports' own server-rendered motorsports schedule page. The `series` enum accepts `f1` and `nascar`.
- **Params:** `season` (integer, optional) — 4-digit season year; defaults to the current season; `series` (string, **required**) — Motorsports series key

### `yahoo_sports_navigation`

- **HTTP:** `GET /yahoo-sports/navigation`
- **What:** Yahoo Sports section navigation. Returns the exact navcat label and URL links Yahoo renders on the home page or one public sports section page. Use section_url from yahoo-sports-home or this response to discover sport-scoped topics and filters.
- **Params:** `section_url` (string, optional) — Full Yahoo Sports page URL; leave blank for home navigation

### `yahoo_sports_network_catalog`

- **HTTP:** `GET /yahoo-sports/network-catalog`
- **What:** Yahoo Sports Network and Watch catalog. Returns every current partner entry from the Yahoo Sports Network menu, including disabled entries, nested destinations and partner attribution, plus the homepage's featured Watch show cards. Each show's list_id is accepted by yahoo-sports-video-headlines.
- **Params:** _none_

### `yahoo_sports_news`

- **HTTP:** `GET /yahoo-sports/news`
- **What:** Yahoo Sports league news. Returns source news articles. For league=soccer, Yahoo exposes a shared cross-competition /soccer/news/ feed and no competition-specific news filter; article tags are preserved verbatim.
- **Params:** `league` (string, **required**) — League key

### `yahoo_sports_newsletter_archive`

- **HTTP:** `GET /yahoo-sports/newsletter-archive`
- **What:** Yahoo Sports newsletter article archive. Returns one page of articles from a newsletter's public archive. Discover current slugs with yahoo-sports-newsletters. The page number maps to Yahoo's own /page/{n}/ archive route; article tags are preserved from the source. Yahoo exposes no archive sort or tag filter. This endpoint does not submit the email subscription form.
- **Params:** `newsletter` (string, **required**) — Newsletter slug from yahoo-sports-newsletters; `page` (integer, optional) — 1-based Yahoo archive page number; defaults to 1

### `yahoo_sports_newsletters`

- **HTTP:** `GET /yahoo-sports/newsletters`
- **What:** Yahoo Sports newsletter catalog. Lists the current public Yahoo Sports newsletter cards, including each newsletter slug, archive URL, and the schedule/description text shown by the site. This is a read-only catalog; it does not subscribe an email address.
- **Params:** _none_

### `yahoo_sports_odds_featured`

- **HTTP:** `GET /yahoo-sports/odds-featured`
- **What:** Yahoo Sports featured odds games. Returns the current featured game cards from Yahoo's public Graphite featuredGameIds operation, including each source game ID for use with yahoo-sports-odds-game.
- **Params:** _none_

### `yahoo_sports_odds_game`

- **HTTP:** `GET /yahoo-sports/odds-game`
- **What:** Yahoo Sports game odds markets. Returns the available moneyline, spread and over/under markets and selections for one game using Yahoo's public Graphite playbookGame operation. Get game_id from yahoo-sports-odds-games, yahoo-sports-odds-trending, or yahoo-sports-odds-featured.
- **Params:** `game_id` (string, **required**) — Yahoo game ID from an odds game list; `tz` (string, optional) — Optional IANA timezone for game time display; defaults to UTC

### `yahoo_sports_odds_games`

- **HTTP:** `GET /yahoo-sports/odds-games`
- **What:** Yahoo Sports current game IDs for an odds league. Returns the current games and their Yahoo game IDs from the public Graphite leagueGameIds operation. A valid current league can return an empty games array during its off-season. Use the sportsbook catalog for the complete league value space.
- **Params:** `league` (string, **required**) — Exact Graphite league value from yahoo-sports-sportsbook-catalog

### `yahoo_sports_odds_trending`

- **HTTP:** `GET /yahoo-sports/odds-trending`
- **What:** Yahoo Sports trending odds games. Returns the current trending game cards from Yahoo's public Graphite trendingGameIds operation, including each source game ID for use with yahoo-sports-odds-game.
- **Params:** _none_

### `yahoo_sports_olympics_medals`

- **HTTP:** `GET /yahoo-sports/olympics-medals`
- **What:** Yahoo Sports Olympics medal count. Returns the current Olympic games' full medal count by country (gold/silver/bronze/total, ranked), from Yahoo Sports' own server-rendered Olympics medals page. This endpoint takes no parameters -- it always returns whichever Olympic games Yahoo currently has medal data for, not a caller-selected prior edition.
- **Params:** _none_

### `yahoo_sports_player`

- **HTTP:** `GET /yahoo-sports/player`
- **What:** Yahoo Sports player detail. Returns one player bio and current-season stats. Use league=soccer for Yahoo's flat soccer player namespace, or a league key from yahoo-sports-leagues; get the numeric player id from a roster record.
- **Params:** `league` (string, **required**) — League key; `player` (string, **required**) — Numeric Yahoo Sports player id

### `yahoo_sports_player_search`

- **HTTP:** `GET /yahoo-sports/player-search`
- **What:** Yahoo Sports player search. Searches Yahoo's public playerSearch operation, as used by the NFL, NBA, MLB, and Golf player pages. Yahoo requires at least three characters and currently hard-codes onActiveRosterOnly=false in these search boxes.
- **Params:** `league` (string, **required**) — Player-search page key; `name` (string, **required**) — Player name or prefix (at least three characters)

### `yahoo_sports_playoff_bracket`

- **HTTP:** `GET /yahoo-sports/playoff-bracket`
- **What:** Yahoo Sports playoff bracket data. Returns Yahoo's public bracket slots, seeds, series and game records for NFL, NBA, MLB, WNBA, college football, men's college basketball or women's college basketball. NBA also includes the page's separate Play-In Tournament bracket. Use yahoo-sports-playoff-bracket-catalog to discover the current season values.
- **Params:** `league` (string, **required**) — Yahoo league key; `season` (integer, optional) — Optional season year from yahoo-sports-playoff-bracket-catalog; defaults to Yahoo's current season

### `yahoo_sports_playoff_bracket_catalog`

- **HTTP:** `GET /yahoo-sports/playoff-bracket-catalog`
- **What:** Yahoo Sports playoff bracket season options. Returns the season choices and any separate tournament selector published by the selected Yahoo playoff bracket page. The supported league set is NFL, NBA, MLB, WNBA, NCAAF, NCAAB and NCAAW.
- **Params:** `league` (string, **required**) — Yahoo league key

### `yahoo_sports_rss_catalog`

- **HTTP:** `GET /yahoo-sports/rss-catalog`
- **What:** Yahoo Sports RSS feed catalog. Returns the complete list of RSS feed keys currently listed on Yahoo Sports' syndication page. Use a key with yahoo-sports-rss-feed.
- **Params:** _none_

### `yahoo_sports_rss_feed`

- **HTTP:** `GET /yahoo-sports/rss-feed`
- **What:** Yahoo Sports RSS feed. Returns every item in one Yahoo Sports RSS feed, including full content:encoded HTML and creator/publisher metadata when present. Feed keys come from yahoo-sports-rss-catalog; no caller limit or date filter is added.
- **Params:** `feed` (string, **required**) — Feed key from yahoo-sports-rss-catalog

### `yahoo_sports_schedule_catalog`

- **HTTP:** `GET /yahoo-sports/schedule-catalog`
- **What:** Yahoo Sports league schedule filter catalog. Returns the current season choices, week/phase pairs and conference/division filters shown by one Yahoo league schedule page. League keys are NFL, NBA, MLB, NHL, WNBA, NCAAF, NCAAB and NCAAW.
- **Params:** `league` (string, **required**) — Yahoo league key

### `yahoo_sports_scoreboard`

- **HTTP:** `GET /yahoo-sports/scoreboard`
- **What:** Yahoo Sports scoreboard. Returns games with teams, score, status, venue and broadcasts from Yahoo Sports. Use a direct league page key from yahoo-sports-leagues, or league=soccer with competition_id from yahoo-sports-soccer-scoreboard to mirror the root competition selector. Root mode supports date and month; direct competition pages support season.
- **Params:** `competition_id` (string, optional) — Exact source competition id from yahoo-sports-soccer-scoreboard; only with league=soccer; `date` (string, optional) — Date as YYYY-MM-DD; defaults to Yahoo Sports' current scoreboard date; `league` (string, **required**) — League key; `month` (integer, optional) — Optional root soccer scoreboard month from 1 to 12; only with league=soccer; `season` (integer, optional) — Optional season year for a direct soccer competition page; discover values from yahoo-sports-soccer-scoreboard

### `yahoo_sports_section_stream`

- **HTTP:** `GET /yahoo-sports/section-stream`
- **What:** Yahoo Sports public section article stream. Returns one page from the public article stream embedded by a Yahoo Sports section page. The service reads the page's current list ID and source parameters from Flight data, then mirrors Yahoo's POST /api/content/ request. Items remain raw AssetRef objects, preserving nested content, tags, provider metadata, and new upstream fields. Use a section_url discovered from yahoo-sports-navigation; current examples include /indycar/ and /motogp/. Pages without an article stream are rejected. The only exposed page selector is Yahoo's integer pageOffset; it defaults to the page's embedded initial offset. Use page_info.start + page_info.count to request the next page. No server-side tag, sort, or category filter is added because the page does not expose one on this stream.
- **Params:** `page_offset` (integer, optional) — Exact upstream pageOffset. Defaults to the section page's initial offset; use page_info.start + page_info.count for the next page; `section_url` (string, **required**) — Full HTTPS Yahoo Sports article-list URL from yahoo-sports-navigation

### `yahoo_sports_soccer_scoreboard`

- **HTTP:** `GET /yahoo-sports/soccer-scoreboard`
- **What:** Yahoo Sports all-competition soccer scoreboard. Returns games and the live competition/season selector from Yahoo's combined soccer scoreboard. The optional competition_id mirrors Yahoo's client-side competition dropdown over the preloaded game list; it is not sent upstream. Use the returned id values rather than inventing a competition filter.
- **Params:** `competition_id` (string, optional) — Exact source competition id from this response's competitions catalog; mirrors the page's client-side selector; `date` (string, optional) — Date as YYYY-MM-DD; defaults to Yahoo Sports' current soccer scoreboard date; `month` (integer, optional) — Optional Yahoo soccer scoreboard month number (1–12); may be combined with date

### `yahoo_sports_sportsbook_catalog`

- **HTTP:** `GET /yahoo-sports/sportsbook-catalog`
- **What:** Yahoo Sports odds page filter catalog. Returns every league option displayed by Yahoo's public odds page and distinguishes the page's client-side Trending/Soccer groups from the 15 Graphite leagueGameIds values. Use odds-games for one league's game IDs, odds-trending-games or odds-featured-games for those feeds, and odds-game for one game's available markets.
- **Params:** _none_

### `yahoo_sports_standings`

- **HTTP:** `GET /yahoo-sports/standings`
- **What:** Yahoo Sports standings. Returns grouped standings from a Yahoo Sports standings page. Use a league whose standings flag is true in yahoo-sports-leagues. Soccer standings can use a season from yahoo-sports-soccer-scoreboard; competitions without a source table are excluded.
- **Params:** `league` (string, **required**) — League key; `season` (integer, optional) — Optional soccer standings season from yahoo-sports-soccer-scoreboard

### `yahoo_sports_stats`

- **HTTP:** `GET /yahoo-sports/stats`
- **What:** Yahoo Sports league stats table. Returns one complete Yahoo stats table (the embedded data can contain up to 200 rows), plus the live tabs, filters and sort-stat catalog. Pagination in Yahoo's table is client-side; no page or offset parameter is added.
- **Params:** `cutTypeIds` (string, optional) — Split/situation id from stats-discovery, e.g. HOME; `league` (string, **required**) — Stats league key; `leagueStructure` (string, optional) — Structure id from stats-discovery, e.g. nba.struct.conf.1; `pageType` (string, optional) — Stats page type; defaults to individual; `positionIds` (string, optional) — Position id from stats-discovery, e.g. POINT_GUARD; `qualified` (boolean, optional) — Qualified leaders filter, when listed by stats-discovery; `selectedTable` (integer, optional) — Tab id from the response's tabs list; defaults to 0; `sortStatId` (string, optional) — Sort id from the response's sort_stat_ids, e.g. TOTAL_REBOUNDS_PER_GAME; `week` (integer, optional) — Week number from stats-discovery; pair with weekSeasonPhase; `weekSeasonPhase` (string, optional) — Phase value paired with week, e.g. REGULAR_SEASON or POSTSEASON

### `yahoo_sports_stats_catalog`

- **HTTP:** `GET /yahoo-sports/stats-catalog`
- **What:** Yahoo Sports stats league catalog. Lists the exact league keys and stats page templates with current embedded stats data. Use this catalog before yahoo-sports-stats-discovery and yahoo-sports-stats.
- **Params:** _none_

### `yahoo_sports_stats_discovery`

- **HTTP:** `GET /yahoo-sports/stats-discovery`
- **What:** Yahoo Sports stats tabs and filters. Returns the live tab ids, filter parameters and values, and sort-stat ids for one Yahoo league stats page. This is the discovery surface for selectedTable, qualified, leagueStructure, positionIds, cutTypeIds, sortStatId, week, and weekSeasonPhase.
- **Params:** `league` (string, **required**) — Stats league key; `pageType` (string, optional) — Stats page type; defaults to individual

### `yahoo_sports_team`

- **HTTP:** `GET /yahoo-sports/team`
- **What:** Yahoo Sports team detail. Returns one team detail record. Use league=soccer for Yahoo's flat soccer team namespace, or a league key from yahoo-sports-leagues for its own team page. Team slugs come from scoreboard or standings records.
- **Params:** `league` (string, **required**) — League key; `team` (string, **required**) — Yahoo Sports team slug

### `yahoo_sports_team_roster`

- **HTTP:** `GET /yahoo-sports/team-roster`
- **What:** Yahoo Sports team roster. Returns one team roster. Use league=soccer for Yahoo's flat soccer team namespace, or a league key from yahoo-sports-leagues. Team slugs come from team or scoreboard records.
- **Params:** `league` (string, **required**) — League key; `team` (string, **required**) — Yahoo Sports team slug

### `yahoo_sports_team_schedule`

- **HTTP:** `GET /yahoo-sports/team-schedule`
- **What:** Yahoo Sports team schedule. Returns one team schedule. Use league=soccer for Yahoo's flat soccer team namespace, or a league key from yahoo-sports-leagues. Team slugs come from team or scoreboard records.
- **Params:** `league` (string, **required**) — League key; `team` (string, **required**) — Yahoo Sports team slug

### `yahoo_sports_tennis_rankings`

- **HTTP:** `GET /yahoo-sports/tennis-rankings`
- **What:** Yahoo Sports tennis rankings. Returns an ATP/WTA singles/doubles ranking list (rank, points, player name, country, age), from Yahoo Sports' own server-rendered rankings page. The `type` enum accepts `mens-singles`, `womens-singles`, `mens-doubles`, and `womens-doubles`. No stable player id is available in this list.
- **Params:** `type` (string, **required**) — Rankings type

### `yahoo_sports_tennis_schedule`

- **HTTP:** `GET /yahoo-sports/tennis-schedule`
- **What:** Yahoo Sports tennis tournament schedule. Returns the full season tennis tournament calendar (name, gender, match type, surface, dates, status, venue, and champion where decided), from Yahoo Sports' own server-rendered tournaments page. This endpoint takes no parameters -- it always returns Yahoo's current full-season snapshot (season/gender/match-type filtering happens client-side on Yahoo's own page, not server-side).
- **Params:** _none_

### `yahoo_sports_tennis_scoreboard`

- **HTTP:** `GET /yahoo-sports/tennis-scoreboard`
- **What:** Yahoo Sports tennis scoreboard. Returns a snapshot of current/recently-completed tennis matches across the tour (tournament, round, players, per-set scores, winner, and status), from Yahoo Sports' own server-rendered tournaments page. This endpoint takes no parameters -- it is a fixed-size "what's happening right now" snapshot, not a by-date query.
- **Params:** _none_

### `yahoo_sports_topic_news`

- **HTTP:** `GET /yahoo-sports/topic-news`
- **What:** Yahoo Sports topic news. Returns the current article list for a public Yahoo Sports root or sport-scoped topic page. Topic slugs are open-ended; article tags are returned exactly as Yahoo embeds them.
- **Params:** `topic` (string, optional) — Open-ended root topic slug; `topic_url` (string, optional) — Full Yahoo Sports topic URL, including sport-scoped topic pages such as /golf/topic/lpga-tour/

### `yahoo_sports_video_headlines`

- **HTTP:** `GET /yahoo-sports/video-headlines`
- **What:** Yahoo Sports video headlines. Returns video cards from Yahoo's public storyheadlines list. Use a list_id from yahoo-sports-video-list-catalog or a Yahoo video-show page; count supports the page's observed values 1 and 6.
- **Params:** `count` (integer, optional) — Yahoo page request count: 1 or 6. Defaults to 6.; `list_id` (string, **required**) — Yahoo video list UUID from a Watch or video-show page

### `yahoo_sports_video_list_catalog`

- **HTTP:** `GET /yahoo-sports/video-list-catalog`
- **What:** Yahoo Sports video-list catalog. Lists the current video-list IDs embedded in Yahoo Sports' desktop Watch page. Use each list_id with yahoo-sports-video-headlines; IDs are discovered dynamically and may change.
- **Params:** _none_

### `yahoo_sports_watch_schedule`

- **HTTP:** `GET /yahoo-sports/watch-schedule`
- **What:** Yahoo Sports TV schedule. Returns the current program schedule exposed by Yahoo Sports' Watch page. The source request has no date, league, season, sort, or pagination parameter.
- **Params:** _none_

## Yahoo Tech (3)

### `yahoo_tech_article`

- **HTTP:** `GET /yahoo-tech/article`
- **What:** Yahoo Tech article content. Returns a single Yahoo Tech article's full content: title, description, author, publish/update time, section, image, keywords, original publisher, and body paragraphs. Accepts a canonical tech.yahoo.com article URL, such as one returned by the home or category story streams.
- **Params:** `url` (string, **required**) — Canonical tech.yahoo.com article URL

### `yahoo_tech_category`

- **HTTP:** `GET /yahoo-tech/category`
- **What:** Yahoo Tech section story stream. Returns a Yahoo Tech section's editorial story feed: title, destination URL, category, and thumbnail image for each story, with page-based pagination. Sourced from Yahoo Tech's own server-rendered section pages.
- **Params:** `category` (string, **required**) — Yahoo Tech section; `page` (integer, optional) — 1-based page number, defaults to 1

### `yahoo_tech_home`

- **HTTP:** `GET /yahoo-tech/home`
- **What:** Yahoo Tech homepage story stream. Returns Yahoo Tech's homepage editorial story feed: title, destination URL, category, and thumbnail image for each story. Sourced from Yahoo Tech's own server-rendered homepage.
- **Params:** _none_
