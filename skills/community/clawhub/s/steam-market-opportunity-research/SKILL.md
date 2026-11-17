---
name: steam-market-opportunity-research
description: Evaluate Steam game niches using Crawlora's game catalog, chart and player-count history, live pricing, reviews, and release news. Use for comparable-title studies, positioning and price research, and evidence-backed game opportunity hypotheses.
---

# Steam market opportunity research

Assess a defined game concept against comparable titles, activity, pricing, and
player feedback. Keep observed metrics, third-party estimates, and commercial
hypotheses separate.

## Setup

Set `CRAWLORA_API_KEY` to your key from [crawlora.net](https://crawlora.net).
Run the bundled `scripts/crawlora.sh` from this skill directory or by absolute
path. It sends `x-api-key` to `https://api.crawlora.net/api/v1`; keep the key in
the environment. Read [reference/endpoints.md](reference/endpoints.md) for
selected Steam live tools and stored game, chart, player-count, news, and review data.

## Build and compare a defensible cohort

1. Define the concept's player experience, genre/tags, platform, business model,
   release cohort, and region. Use `/datasets/steam-games/facets` to discover
   dataset labels, then `/datasets/steam-games/search` with `type=game` and the
   relevant filters. `q` searches names/developers/publishers; use `tag` for
   gameplay taxonomy. Live numeric community tag IDs come from `/steam/tags/list`.
2. Inspect candidate titles instead of treating all matches as competitors.
   Separate base games, DLC, demos, free-to-play titles, and unreleased games.
   Resolve `appid`; dataset searches for history use `app_id`, while live
   `/steam/app`, `/steam/reviews`, `/steam/players`, and `/steam/news` use `appid`.
3. Refresh shortlist metadata and prices with `/steam/app` or `/steam/items`
   (up to 100 IDs). Keep `cc` and currency consistent. Prices in cents require
   conversion to major units for display; compare regular versus discounted
   prices separately and retain observation dates.
4. Read `/datasets/steam-playercounts/search?app_id=...` for observed daily
   concurrent-player samples. These are not daily unique users or automatically
   daily peaks. For `/datasets/steam-charts/search`, keep `chart` and `country`
   fixed: `concurrent`, `most_played` (weekly peak), or `top_sellers` (country-
   specific sales ranking). Single-app history uses `app_id` and `sort=date_desc`;
   ordinary latest requests echo `snapshot_date`, which may lag today.
5. Inspect release dates and `/steam/news` before describing activity changes.
   Updates, discounts, and events are possible explanations, not proven causes.
   Match game age and observation windows; an established live-service game's
   concurrent usage is not directly comparable to a short single-player release.
6. Use live `/steam/reviews` for a bounded, comparable sample; preserve language,
   purchase/review filters, playtime, and recommendation IDs. Start with `cursor=*`;
   aggregate `query_summary` totals populate only on that first page. Stored
   `/datasets/steam-reviews/search` emphasizes helpful reviews, not a random sample.
   Report theme counts as unique eligible reviews `n/N`, with short cited examples.

```sh
scripts/crawlora.sh /datasets/steam-games/search \
  type=game tag=Roguelike min_total_reviews=100 page_size=5
# Use a returned appid as app_id when requesting dataset player-count history.
```

## Opportunity brief and limits

Return cohort selection rules, comparable-title table, matched activity series,
prices, review themes, supported positioning gaps, conflicting evidence, and a
next validation step for each opportunity hypothesis.

- Dataset owner ranges/midpoints come from SteamSpy estimates. They are not
  audited sales counts. Do not multiply an owner midpoint by today's price and
  call the result realized revenue; discounts, keys, refunds, and free access differ.
- `review_score` is a 0–1 positive-review ratio; Metacritic uses a different scale.
  Missing chart entries mean unobserved/unranked within coverage, not zero players.
- A daily concurrent count cannot establish retention or unique audience size.
  Do not sum overlapping weekly snapshots or infer revenue from chart positions.
- Dataset pages max at 100 and the result window is 10,000. Stop on repeated
  cursors/pages or the sample bound. Back off on `429`, retry transient `5xx` once,
  stop on `401`/`403`, and check application `code` before interpreting empty data.
