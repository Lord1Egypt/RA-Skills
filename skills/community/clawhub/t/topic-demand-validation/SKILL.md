---
name: topic-demand-validation
description: Validate broad topic, problem, audience, or content demand by comparing autocomplete, Google Trends, search results, and sampled discussion. For a physical product launch hypothesis that needs marketplace listings, prices, and review evidence, use consumer-product-opportunity; use brand-mention-research for a known entity's mentions.
---

# Topic demand validation

Build an evidence brief about what people search for, what is changing, what already ranks, and what a bounded public discussion sample says. Keep those signals separate: they answer different questions and do not establish sales, market size, or future growth.

## Scope and inputs

Ask for or infer the topic, product/content decision, target market and language, time window, and any excluded sources. If geography or period is unspecified, state the chosen defaults before collecting. Keep the scope narrow enough to compare consistently.

Use this workflow for category, problem, audience, or content-topic discovery. For one query’s autocomplete or SERP, use the focused SERP workflow. For a named brand’s mentions and reputation, use brand-mention-research.
For a physical consumer-product launch decision that needs visible competitor listings, price ranges, and product-review evidence, use consumer-product-opportunity instead.

## Collect comparable evidence

- [ ] Expand one or a few seed phrases with Google Suggest. Save the exact prefix, country, language, returned completions, and collection time. Suggestions reveal query phrasing; they are not search-volume estimates.
- [ ] Compare no more than five selected terms in one Google Trends request. Keep geography, range, category, search type, and locale consistent. Use rising queries or related topics to discover candidates, then compare those candidates in a shared request. If a term has zero or missing data, preserve that status; do not treat it as zero demand.
- [ ] Inspect a bounded SERP sample with Bing and/or Brave for the highest-value query clusters. Record each exact query, country/language, rank, title, URL, and result type. Search results show what surfaced for that query at collection time, not the size of the market.
- [ ] Sample one or more relevant social sources—Reddit, TikTok, or YouTube—using focused queries. Record the query, filters, time, pagination, result IDs, dates, and how many sampled results are actually relevant. Reddit's time filter applies to top/comments sorts; do not claim that new plus a time value enforces a date window. TikTok search has no date filter here: filter returned dates locally and mark unknown dates. YouTube offers upload-date filters, but results remain a selected sample. Search feeds may be noisy or incomplete; narrow a query or community when needed, and stop when the sample cannot support the question.
- [ ] Open only selected relevant posts/videos for context. Read comments or captions/transcripts when they materially clarify the expressed need. Deduplicate within each platform and distinguish top-level posts from comments. Do not turn sampled posts, views, or comment counts into unique audience reach.

Use a modest first pass when the user has not set a budget: one Trends comparison of up to five terms, a small set of autocomplete prefixes, one or two SERP queries per important cluster, and a bounded first page of social results. Expand only when the initial evidence is relevant and the decision needs it. Successful API calls are billable; agree a wider collection budget with the user before multiplying searches or paging deeply.

## Interpret without blending unlike metrics

- Treat autocomplete as candidate phrasing and intent. Google says predictions reflect real searches but also factors such as language, location, and current interest; they are not a simple popularity list.
- Treat Trends as a sampled, normalized relative index for the selected query context. Compare terms in the same request. Do not compare independently scaled series as if they share a numeric scale, or translate index values into query counts.
- Treat SERP results as a time- and location-bound sample of what ranks, not exhaustive competition or demand.
- Treat social results as observed examples. Label relevant, ambiguous, and irrelevant matches; classify themes from the actual post/comment text. A failed or irrelevant search is a coverage limit, not proof that no one is discussing the topic.
- Do not invent a combined numeric “demand score.” Synthesize support, counter-signals, source coverage, and unresolved questions in words. Separate measured evidence from a testable hypothesis.

## Deliverable

Return a compact brief with:

1. Scope: topic, market/language, date window, sources, query list, and sampling limits.
2. Search intent: autocomplete phrase clusters and the intent each suggests.
3. Search movement: Trends terms, settings, relative timeline, and rising/related queries where available.
4. Search competition: representative ranked results, domains, and result formats.
5. Discussion sample: relevant/ambiguous/irrelevant counts, themes, dates, links, and any sampled comments or transcript evidence.
6. Synthesis: evidence for, evidence against, missing coverage, and one concrete next validation step. State whether the evidence supports exploring, testing, or holding the idea; do not claim commercial validation from these signals alone.

## Failure handling

Check application code as well as HTTP status. Stop on authentication errors. For a 429 or retryable 503, honor Retry-After and retry once at most; do not rotate credentials, fan out repeated requests, or bypass a challenge. If a source returns an empty/404 result or mostly irrelevant content, report the search and its limit as “not validated in this sample,” not “no demand.”

## Examples

~~~sh
scripts/crawlora.sh /google/suggest q="meal prep for shift workers" country=us lang=en count=10
scripts/crawlora.sh -X POST /google/trends/explore/interest-over-time '{"keywords":["meal prep for shift workers","night shift meal prep"],"geo":"US","time_range":"today 12-m","type":"web"}'
scripts/crawlora.sh /bing/search q="meal prep for shift workers" count=10 country=us lang=en
scripts/crawlora.sh /reddit/search q="meal prep for shift workers" sort=top time=year limit=10
scripts/crawlora.sh /tiktok/search keyword="meal prep for shift workers" count=10
scripts/crawlora.sh /youtube/search q="meal prep for shift workers" type=video sort_by=relevance
~~~

Read reference/endpoints.md for the selected endpoints, exact methods, parameters, and request shapes. Use the bundled scripts/crawlora.sh helper; it sends CRAWLORA_API_KEY as a header and does not put the key in the URL.
