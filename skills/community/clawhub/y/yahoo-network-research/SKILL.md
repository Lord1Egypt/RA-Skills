---
name: yahoo-network-research
description: Researches Yahoo's editorial content network — Autos, Entertainment, Health, Life, News, Shopping, Sports, and Tech — via the Crawlora API, returning clean JSON. Each vertical shares a home/category story-stream plus full-article-content pattern; Yahoo Sports adds deeper sports-data endpoints (scoreboards, standings, team/player/roster, golf, MMA, motorsports, tennis, Olympics). Use when the user wants a Yahoo section's story feed, a Yahoo article's full content, Yahoo News comments, Yahoo Shopping deals/lists, or Yahoo Sports scores/standings/schedules. Yahoo Finance and Yahoo Search are covered by their own separate skills, not this one.
allowed-tools: Bash(scripts/crawlora.sh:*)
---

# Yahoo network research

## Tool scope and data flow

Use the bundled `scripts/crawlora.sh` helper only for this skill's documented routes in `reference/endpoints.md`; the helper enforces its exact route and method allowlist. It reads `CRAWLORA_API_KEY` from the environment and sends it as an `x-api-key` header over HTTPS to `api.crawlora.net`. It stores the key in a mode-600 curl config under `TMPDIR` and removes it when the command exits. It reads `TMPDIR` only to choose that temporary config location; it does not inspect other environment variables or enumerate files, install software, or run with elevated privileges.

Pull story feeds and full article content across Yahoo's editorial content
network — Autos, Entertainment, Health, Life, News, Shopping, Sports, and
Tech — as normalized JSON from the Crawlora API, with no HTML scraping of
yahoo.com. This is distinct from Yahoo Finance and Yahoo Search, which have
their own separate skills.

## When to use this skill

- "What's on Yahoo News right now?" / "pull Yahoo's [section] story feed."
- "Give me the full text of this Yahoo article."
- "What are people saying in the comments on this Yahoo News story?"
- "What's the scoreboard / standings for [league] on Yahoo Sports?"
- "What's the PGA Tour schedule / a golf tournament's leaderboard?"
- "Who's fighting at the next UFC event?" / F1 or NASCAR race results / ATP
  or WTA tennis rankings and scores.
- "What deals is Yahoo Shopping featuring for [retailer]?"

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Simple content verticals (Autos, Entertainment, Health, Tech)** — each
   follows the same shape: `/yahoo-{vertical}/home` for the homepage story
   stream (title, destination URL, category, thumbnail), `/yahoo-{vertical}/category`
   (`category`, paginated with `page`) for one section's stream, and
   `/yahoo-{vertical}/article` (`url`) for a story's full content (title,
   description, author, publish/update time, section, image, keywords,
   original publisher, body paragraphs) — pass a destination URL straight
   from a home/category response.
2. **Yahoo Life** — the same pattern minus a category tier: `/yahoo-life/home`
   for the homepage stream, `/yahoo-life/article` (`url`) for full content.
3. **Yahoo News** — home/category/article plus comment reading:
   `/yahoo-news/home` and `/yahoo-news/category` (`category`) return the
   "need to know" story stream with summary, source, publish time, and
   comment count; `/yahoo-news/article` (`url`) returns full article
   content; `/yahoo-news/comments` (`content_id`, an article id from
   home/category/article) returns top-level comments with cursor
   pagination, and `/yahoo-news/comments/replies` (`comment_id`+`content_id`)
   walks one comment's replies; `/yahoo-news/suggest` (`q`) returns
   search-box autocomplete suggestions.
4. **Yahoo Shopping** — home/category/article plus its own store/list
   directories: `/yahoo-shopping/home` and `/yahoo-shopping/category`
   (`category`) for the editorial story feed, `/yahoo-shopping/article`
   (`url`) for full content; `/yahoo-shopping/stores` lists retailer slugs
   (Amazon, Target, Best Buy, etc.) for `/yahoo-shopping/store` (`store`),
   which returns that retailer's currently-featured deals; `/yahoo-shopping/shopping-lists`
   lists curated list slugs for `/yahoo-shopping/shopping-list` (`list`),
   which returns that list's items. This is a deals/buying-guide content
   site, not a searchable product catalog.
5. **Yahoo Sports** — the deepest vertical, 18 endpoints:
   - **Scores & standings:** `/yahoo-sports/scoreboard` (`league`, optional
     `date`), `/yahoo-sports/standings` (`league`), `/yahoo-sports/game`
     (`league`+`game` slug from a scoreboard/team-schedule `url`).
   - **Teams & players:** `/yahoo-sports/team`, `/yahoo-sports/team-roster`,
     `/yahoo-sports/team-schedule` (all `league`+`team` slug from
     scoreboard/standings), `/yahoo-sports/player` (`league`+`player` id
     from a roster response), `/yahoo-sports/news` (`league`) for recent
     articles.
   - **Golf:** `/yahoo-sports/golf-schedule` (`tour`, optional `season`) for
     a tour's tournaments, `/yahoo-sports/golf-leaderboard` (`tournament` id
     from the schedule, optional `season`) for one tournament's full
     leaderboard.
   - **MMA:** `/yahoo-sports/mma-schedule` and `/yahoo-sports/mma-fight-card`
     (both no params) — always the next/current UFC event only.
   - **Motorsports:** `/yahoo-sports/motorsports-schedule` (`series`:
     `f1`/`nascar`, optional `season`), `/yahoo-sports/motorsports-race`
     (`series`+`race` slug from the schedule) for one race's results.
   - **Tennis:** `/yahoo-sports/tennis-rankings` (`type`),
     `/yahoo-sports/tennis-schedule` and `/yahoo-sports/tennis-scoreboard`
     (both no params, fixed current-season/current-snapshot data).
   - **Olympics:** `/yahoo-sports/olympics-medals` (no params) — current
     games' medal count only.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# News: category feed, then full article content
scripts/crawlora.sh /yahoo-news/category category="politics" | jq '.'
scripts/crawlora.sh /yahoo-news/article url="https://www.yahoo.com/news/<slug>.html" | jq '.'

# Sports: scoreboard, standings, and a golf tournament leaderboard
scripts/crawlora.sh /yahoo-sports/scoreboard league="nfl" | jq '.'
scripts/crawlora.sh /yahoo-sports/standings league="nba" | jq '.'
scripts/crawlora.sh /yahoo-sports/golf-leaderboard tournament="golf.e.23" | jq '.'

# Shopping: retailer deals
scripts/crawlora.sh /yahoo-shopping/stores | jq '.'
scripts/crawlora.sh /yahoo-shopping/store store="target" | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Yahoo Autos,
Entertainment, Health, Life, News, Shopping, Sports, and Tech endpoint this
skill uses.

## Examples

- **Section digest:** `/yahoo-news/category` (`category="politics"`) for the
  story stream, then `/yahoo-news/article` on each destination URL for full
  text; add `/yahoo-news/comments` (`content_id`) to see reader reaction.
- **League snapshot:** `/yahoo-sports/scoreboard` for today's games, plus
  `/yahoo-sports/standings` for the same `league`, to summarize where every
  team sits.
- **Golf/tennis schedule lookup:** `/yahoo-sports/golf-schedule` (`tour="pga-tour"`)
  to find an upcoming tournament's `id`, then `/yahoo-sports/golf-leaderboard`
  once it's underway; or `/yahoo-sports/tennis-schedule` for the season
  calendar and `/yahoo-sports/tennis-rankings` (`type="mens-singles"`) for
  current rankings.
- **Article pull from a feed:** `/yahoo-entertainment/home` or
  `/yahoo-health/category` to get a story's destination URL, then
  `/yahoo-entertainment/article` / `/yahoo-health/article` (`url`) for its
  full body.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public Yahoo network story/article/sports pages.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **Article endpoints need a canonical URL, not a guess** — pull it from the
  matching vertical's own `home`/`category` (or, for News/Shopping, `article`)
  response's destination URL field; hand-constructed URLs aren't guaranteed
  to resolve.
- **`category` values are per-vertical section strings** particular to each
  site's own navigation (e.g. Autos/Entertainment/Health/Shopping/Tech
  sections, News sections like `"politics"`) — read them off the vertical's
  own home/category response or site navigation rather than assuming they
  match across verticals.
- **Yahoo Sports is the deepest vertical** — beyond the core
  game/scoreboard/standings/team/player set, it has dedicated sub-endpoints
  for golf (schedule + leaderboard), MMA (UFC-only, next event only),
  motorsports (F1/NASCAR schedule + race results), tennis (rankings,
  season schedule, live scoreboard), and Olympics (current games' medal
  count) — several of these (MMA, tennis schedule/scoreboard, Olympics
  medals) take no parameters and always return Yahoo's current snapshot,
  not a caller-selected date/edition.
- Yahoo Finance and Yahoo Search are **out of scope for this skill** — see
  their own separate skills.
