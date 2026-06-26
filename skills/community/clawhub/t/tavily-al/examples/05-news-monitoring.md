# Example 05 — News Monitoring

Fresh-news answer using `topic: "news"` with `time_range`, deduplication, recency awareness, and dated citations.

## User request

> "What are the latest developments in EU AI regulation this past week?"

## Agent reasoning summary

- The user wants recent news, not evergreen background — I must scope to fresh sources.
- Tavily's `topic: "news"` plus a `time_range` filter targets recency.
- I will dedup near-identical wire stories and cite publication dates so the user can judge freshness.

## Tavily operation to use

Use the **search** endpoint with `topic: "news"` and a `time_range`.
Why: the news topic biases toward news publishers and recent items, and `time_range` constrains the window. Plain search without these would surface stale, evergreen pages.

## Request shape

```http
POST https://api.tavily.com/search
Authorization: Bearer <TAVILY_API_KEY>
Content-Type: application/json
```

```json
{
  "query": "EU AI Act regulation developments",
  "topic": "news",
  "time_range": "week",
  "search_depth": "advanced",
  "include_answer": true,
  "max_results": 10
}
```

> Verification needed: confirm the exact accepted values for `time_range` (e.g., "day", "week", "month") and whether a `published_date` field is returned per result at https://docs.tavily.com

## Response handling

Representative response (truncated):

```json
{
  "answer": "This week the EU advanced implementation guidance for the AI Act...",
  "results": [
    { "title": "EU issues AI Act guidance", "url": "https://news-a.example.com/eu-ai-guidance", "content": "On 2026-05-28 the Commission published...", "score": 0.91, "published_date": "2026-05-28", "raw_content": null },
    { "title": "Commission clarifies AI rules", "url": "https://news-b.example.com/eu-ai-rules", "content": "Reuters: the EU clarified obligations...", "score": 0.86, "published_date": "2026-05-27", "raw_content": null },
    { "title": "EU issues AI Act guidance (syndicated)", "url": "https://mirror.example.com/eu-ai-guidance", "content": "On 2026-05-28 the Commission published...", "score": 0.71, "published_date": "2026-05-28", "raw_content": null }
  ]
}
```

Parsing steps:
1. Sort by `score` descending; filter `score >= 0.5`.
2. Deduplicate: collapse near-identical stories. Detect duplicates by (a) normalized URL, and (b) very similar `title`/`content` with the same `published_date` (the syndicated mirror is a dup of `[1]`). Keep the highest-scoring instance.
3. Sort the survivors by `published_date` (newest first) for presentation, since recency matters.
4. Capture each item's `published_date` for the citation.
5. If items span several days, group or note the date range so the user understands the window.

## Citation behavior

- Every cited item includes its publication date inline or in the sources list.
- Dedup happens before numbering, so syndicated copies do not get separate citation numbers.
- The sources list shows date alongside title and URL so freshness is visible at a glance.

## Final answer pattern

```
Latest EU AI regulation developments (past week, as of 2026-05-31):

- On 2026-05-28, the Commission published new implementation guidance for the AI Act. [1]
- On 2026-05-27, regulators clarified provider obligations under the Act. [2]

Sources:
[1] EU issues AI Act guidance (2026-05-28) — https://news-a.example.com/eu-ai-guidance
[2] Commission clarifies AI rules (2026-05-27) — https://news-b.example.com/eu-ai-rules
```

## Common failure mode

Omitting `topic: "news"`/`time_range` and returning months-old articles as "latest", or listing the same wire story three times because syndicated mirrors were not deduplicated. Dates are also frequently dropped, so the user cannot tell how fresh the information is.

## Improved version

- Always set `topic: "news"` and an explicit `time_range` for "latest"/"this week" requests.
- Dedup syndicated copies before assigning citation numbers.
- Sort survivors newest-first and show `published_date` in every citation.
- State the "as of" date so recency is unambiguous.

```json
{
  "query": "EU AI Act regulation developments",
  "topic": "news",
  "time_range": "week",
  "search_depth": "advanced",
  "include_answer": true,
  "max_results": 10
}
```
