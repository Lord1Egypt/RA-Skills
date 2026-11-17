---
name: tiktok-trend-research
description: Build evidence-backed TikTok trend briefs from current feeds, Creative Center rankings, hashtag data, and Explore categories through Crawlora. Use for trend discovery, country/period comparisons, and topic or hashtag momentum; use tiktok-ad-research for paid-ad analysis.
---

# TikTok trend research

Produce a dated, sample-aware view of what TikTok is surfacing for a topic,
hashtag, category, country, or period. Distinguish TikTok's different trend
surfaces: a recommended feed, Creative Center rankings, hashtag activity, and
Explore are not interchangeable measurements.

## Setup and requests

Set `CRAWLORA_API_KEY` to a key from [crawlora.net](https://crawlora.net), then
run the helper bundled with this skill. It sends `x-api-key` to
`https://api.crawlora.net/api/v1`; keep the key in the environment. Read
[`reference/endpoints.md`](reference/endpoints.md) for exact parameters.

```sh
Set `CRAWLORA_API_KEY` in the environment before running the helper.
scripts/crawlora.sh /tiktok/creative-center/hashtags country_code=US period=7 | jq '.'
scripts/crawlora.sh /tiktok/creative-center/videos country_code=US period=7 sort_by=engagement organic_only=true | jq '.'
scripts/crawlora.sh /tiktok/mobile/trending/categories count=10
scripts/crawlora.sh /tiktok/mobile/music/trending count=10
scripts/crawlora.sh /tiktok/mobile/music/beats
scripts/crawlora.sh /tiktok/mobile/music/collections
```

Inspect both HTTP success and the JSON envelope, including nested upstream
`code` values. A `2xx` response with no usable data is not automatically a
successful trend observation.

## Workflow

1. Clarify the topic or hashtag, country, lookback period, surface, requested
   sample size, and whether paid content should be excluded. Record retrieval
   time because trend results change.
2. Choose the matching surface:
   - `/tiktok/trending` for TikTok's current recommended feed; it has no
     geography or historical-period control.
   - `/tiktok/creative-center/hashtags` for ranked hashtags by country and
     period (`7` or `30` days).
   - `/tiktok/creative-center/videos` for ranked videos by country and period,
     sorted by `views`, `engagement`, or `six_second_views`; use
     `organic_only=true` when the brief is organic-only.
   - `/tiktok/search` for keyword-matched videos when the brief starts from a
     topic rather than a known hashtag.
   - `/tiktok/search/hashtag` to discover candidate hashtags, then
     `/tiktok/hashtag/{name}` and `/tiktok/hashtags` to resolve a hashtag id and
     inspect its listed videos.
   - `/tiktok/category` followed by `/tiktok/explore/{id}` for a category feed.
     Do not describe an Explore feed as a global trend ranking.
   - `/tiktok/mobile/feed` for a personalized, region-dependent For You sample;
     it has no country or historical-period filter and is not a global ranking.
   - `/tiktok/mobile/music/trending` or `/tiktok/mobile/music/pick` for current
     mobile sound charts; use a returned `music_id` with `/tiktok/mobile/music/posts`
     to inspect a bounded video sample. That route ignores `count` upstream, so
     continue with its returned cursor.
   - `/tiktok/mobile/music/beats` for a one-page beats/songs chart and
     `/tiktok/mobile/music/collections` for the app's sound-collection feed.
     The beats route has no paging fields; collections' cursor is not a verified
     continuation token, so report both as bounded page samples.
   - `/tiktok/mobile/trending/categories` and `/tiktok/mobile/trending/effects`
     for current app discovery feeds. These are not Creative Center rankings,
     fixed topic taxonomies, or cross-market comparable counts.
3. For a topic brief, use search/hashtag discovery first, then validate a
   bounded set of returned video ids with `/tiktok/post/{id}`. Use identifiers
   returned by the API; do not invent ids from captions or display names.
4. Compare countries or topics only when the surface, period, sort, and filters
   match. Deduplicate by stable hashtag or video id and stop at the requested
   bound or the returned pagination terminal state.
5. Report the observed ranking/activity, source links or ids, filters, sample
   size, and retrieval time. Separate the measured signal from explanations or
   content recommendations.

For mobile-only surfaces, preserve any returned host/region context and the
cursor. They have no explicit country or date-window selector, so don't compare
them with a country/period-specific Creative Center sample as if the scope
matched.

## Interpretation and limits

- Anonymous Creative Center access is partial: hashtag requests return at most
  three records, while video requests return only page one (four videos), even
  when the response reports a larger upstream total. Do not call that total
  accessible coverage.
- Creative Center video availability is uneven. US, JP, ID, VN, and TH have
  reliably returned populated samples; a valid empty result in another market
  can be genuine upstream no-data. Do not retry it indefinitely or claim an
  outage without corroboration.
- `engagement_rate` and `six_seconds_vtr` are ratios, not percentages. Keep
  period-scoped and lifetime fields separate. Counts and ranks are surface-
  specific and do not establish reach across all TikTok.
- Hashtag `viewCount`/`videoCount` and search results reflect TikTok's current
  index. They are not a complete historical archive. A search match is not
  proof that every returned video is about the intended brand or topic.
- Missing fields are unknown, not zero. A valid empty sample is an observation
  to report with its filters, not a reason to fabricate a conclusion.
- Do not claim to have watched a video's hook, heard its audio, or judged its
  visual format unless the environment actually exposed the media. Signed media
  URLs may expire.

## Reliability and output

Use bounded pagination. On `429`, back off; retry one transient `5xx` when
useful. Stop on `401`/`403` and report the access limitation. Preserve partial
results when enrichment fails, labeling which observations are missing.

Return a concise table or brief with `surface`, topic/hashtag, country, period,
rank or metric, source URL/id, retrieval time, and coverage caveats. Call
patterns “observed in this sample”; label forecasts, content ideas, and causal
claims as hypotheses.
