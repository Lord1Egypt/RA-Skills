# Example 02 — Search With Multi-Source Citations

A richer answer assembled from several sources, with inline `[1][2]` markers and a sources list ranked by score.

## User request

> "What are the main health benefits of regular cardiovascular exercise? Give me a sourced summary."

## Agent reasoning summary

- The user explicitly wants a sourced summary, so I need multiple credible results, not just an `answer` string.
- I will use one search with a slightly larger `max_results`, then rank by `score`.
- Each distinct claim should map to the source that supports it.

## Tavily operation to use

Use the **search** endpoint (`POST https://api.tavily.com/search`).
Why: a broad informational question best served by several ranked web results that I can quote and cite. `include_answer` gives me a synthesis to sanity-check my own summary against.

## Request shape

```http
POST https://api.tavily.com/search
Authorization: Bearer <TAVILY_API_KEY>
Content-Type: application/json
```

```json
{
  "query": "health benefits of regular cardiovascular exercise",
  "search_depth": "advanced",
  "include_answer": true,
  "max_results": 8
}
```

## Response handling

Representative response (truncated):

```json
{
  "answer": "Regular cardio improves heart health, lowers blood pressure, aids weight management, and supports mental health.",
  "results": [
    { "title": "Exercise and the Heart", "url": "https://www.heart.org/cardio", "content": "Aerobic exercise lowers resting heart rate and blood pressure...", "score": 0.93, "raw_content": null },
    { "title": "Physical Activity Guidelines", "url": "https://www.cdc.gov/physical-activity", "content": "150 minutes/week reduces cardiovascular disease risk...", "score": 0.88, "raw_content": null },
    { "title": "Exercise for Mental Health", "url": "https://www.nih.gov/exercise-mental-health", "content": "Aerobic activity reduces anxiety and depressive symptoms...", "score": 0.81, "raw_content": null },
    { "title": "Random fitness blog", "url": "https://example-blog.com/cardio", "content": "...", "score": 0.32, "raw_content": null }
  ]
}
```

Parsing steps:
1. Sort `results` by `score` descending.
2. Filter out results with `score < 0.5` (drops the blog at 0.32).
3. Deduplicate by normalized URL (strip protocol, trailing slash, `www.`, query params). Keep the higher-scoring duplicate.
4. Assign stable citation numbers `[1]`, `[2]`, `[3]` in ranked order.
5. Group claims by which source's `content` supports them; attach the matching marker.
6. Cross-check your written summary against `answer` — if they disagree, prefer the claim backed by a concrete source.

## Citation behavior

- Inline markers `[n]` appear immediately after each claim they support.
- A claim supported by two sources gets `[1][2]`.
- The sources list is ordered by `score` (highest first) and numbered to match the inline markers.
- Only sources that survive the score filter and are actually used appear in the list.

## Final answer pattern

```
Regular cardiovascular exercise offers several well-documented benefits:

- It strengthens the heart and lowers resting heart rate and blood pressure. [1]
- Meeting activity guidelines (about 150 minutes/week) reduces the risk of cardiovascular disease. [2]
- It also supports mental health by reducing anxiety and depressive symptoms. [3]

Sources (ranked by relevance):
[1] Exercise and the Heart — https://www.heart.org/cardio
[2] Physical Activity Guidelines — https://www.cdc.gov/physical-activity
[3] Exercise for Mental Health — https://www.nih.gov/exercise-mental-health
```

## Common failure mode

Writing a fluent multi-claim summary but attaching a single blanket citation at the end, or citing the low-score blog (0.32) alongside authoritative sources. Readers cannot tell which source backs which claim, and a weak source pollutes the answer.

## Improved version

- Filter by `score >= 0.5` before composing.
- Map each individual claim to its supporting source with its own marker.
- Rank the sources list by `score` so the strongest evidence is listed first.

```json
{
  "query": "health benefits of regular cardiovascular exercise",
  "search_depth": "advanced",
  "include_answer": true,
  "max_results": 8
}
```

> Verification needed: confirm whether `score` is always returned and its exact range with https://docs.tavily.com
