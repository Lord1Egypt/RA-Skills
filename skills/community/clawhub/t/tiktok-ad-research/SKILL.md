---
name: tiktok-ad-research
description: Research TikTok Creative Center Top Ads by brand, market, industry, and objective through Crawlora. Use for competitor-ad comparisons, creative briefs, messaging and format analysis, and inspection of public ad-performance charts.
---

# TikTok ad research

Build a sourced comparison of TikTok Top Ads and explain which creative ideas
are supported by observed content and public performance signals. Top Ads is a
selected collection of high-performing auction ads, not every advertiser's campaigns.

## Setup and requests

Set `CRAWLORA_API_KEY` to your key from [crawlora.net](https://crawlora.net).
Run the bundled `scripts/crawlora.sh` from this skill directory or by absolute
path. It sends `x-api-key` to `https://api.crawlora.net/api/v1` and prints JSON.
Keep the key in the environment. Read [reference/endpoints.md](reference/endpoints.md)
for the ten Top Ads endpoints and their exact parameters.

## Workflow

1. Determine the brands/product keywords, market, objective, lookback period,
   and requested sample size from the brief. Discover current industry,
   objective, language, and country IDs through `/tiktok/top-ads/filters`;
   use `/locations` and `/location-info` when the geography needs clarification.
2. Search `/tiktok/top-ads/list`, keeping market, period, and objective consistent
   across competitors. `period` is `7`, `30`, or `180`; `limit` is at most 100.
   `order_by` accepts `for_you`, `impression`, `ctr`, `play_2s_rate`,
   `play_6s_rate`, `cvr`, or `like`. State the sort because it changes the sample.
3. Deduplicate by Top Ads material ID and fetch `/tiktok/top-ads/detail` for a
   bounded shortlist. **Use the returned material ID**, not a TikTok video ID.
   Recommendations and spotlight ads can widen discovery, but mark them as
   supplemental rather than silently mixing them into a matched comparison.
4. Use `/tiktok/top-ads/analysis` when performance over the ad's duration matters.
   Metrics are `retain_ctr`, `retain_cvr`, `click_cnt`, `convert_cnt`, and
   `play_retain_cnt`; `period_type` is `7`, `30`, or `180`. Match metric and
   period across ads before comparing charts or percentiles.
5. Inspect the actual creative when the environment supports video/image viewing.
   If only metadata is accessible, limit conclusions to title/copy and returned
   fields. Do not claim to have watched a hook or heard audio from metadata alone.
6. Summarize recurring messaging, format, offer, and call-to-action patterns with
   linked examples. Present proposed creative tests as hypotheses; public charts
   do not establish what caused conversion performance.

```sh
scripts/crawlora.sh /tiktok/top-ads/filters
scripts/crawlora.sh /tiktok/top-ads/list \
  keyword=skincare country_code=US period=30 limit=10 order_by=ctr
```

## Output and interpretation

Return a comparison with `material_id`, available advertiser/title, source link,
country, objective, lookback, duration, observed messaging/format, returned
performance fields, and retrieval time. Preserve metric labels and units as
reported; a percentile is not a raw CTR, spend estimate, or ROI.

- Keyword results may mention a brand without belonging to it. Verify advertiser
  identity where available and mark uncertain matches.
- No matches means none in the queried Top Ads sample, not that the competitor
  is inactive. Describe the filters and coverage rather than claiming all ads.
- Keep signed media URLs as returned; they may expire. Retain material IDs and
  source-page links when available so the research can be repeated.
- The response can contain nested upstream `code`/`msg`/`data`. Check both the
  Crawlora envelope and any upstream code before treating `materials` as results.
  Stop at `pagination.has_more=false` or the agreed sample bound.
- On `429`, back off; retry a transient `5xx` once. Stop on `401`/`403` and
  report the source limitation. Preserve a partial comparison if only some
  details/charts load, clearly marking missing observations.
