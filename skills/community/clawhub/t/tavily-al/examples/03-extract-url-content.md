# Example 03 — Extract URL Content

The user supplies specific URLs. The agent uses **extract** (not search), handles `failed_results`, and summarizes with a citation to each URL.

## User request

> "Summarize these two articles for me: https://example.com/ai-report-2026 and https://example.com/ai-funding-q1 (and also https://broken.example.com/missing if it works)."

## Agent reasoning summary

- The user already provided exact URLs — there is nothing to search for.
- Extract pulls the page text directly, which is more faithful than re-searching.
- One URL may be unreachable, so I must inspect `failed_results` and tell the user what could not be fetched.

## Tavily operation to use

Use the **extract** endpoint (`POST https://api.tavily.com/extract`).
Why: extract takes a list of URLs and returns their `raw_content`. Using search here would be wrong — it would re-rank the open web instead of reading the pages the user named.

## Request shape

```http
POST https://api.tavily.com/extract
Authorization: Bearer <TAVILY_API_KEY>
Content-Type: application/json
```

```json
{
  "urls": [
    "https://example.com/ai-report-2026",
    "https://example.com/ai-funding-q1",
    "https://broken.example.com/missing"
  ],
  "extract_depth": "basic"
}
```

> Verification needed: confirm whether `urls` also accepts a single string in addition to an array, and confirm `extract_depth` allowed values, at https://docs.tavily.com

## Response handling

Representative response (truncated):

```json
{
  "results": [
    {
      "url": "https://example.com/ai-report-2026",
      "title": "State of AI 2026",
      "raw_content": "The 2026 report finds enterprise AI adoption reached 78%..."
    },
    {
      "url": "https://example.com/ai-funding-q1",
      "title": "AI Funding Q1 2026",
      "raw_content": "Q1 2026 venture funding into AI startups totaled $24B..."
    }
  ],
  "failed_results": [
    {
      "url": "https://broken.example.com/missing",
      "error": "Could not fetch the URL (404 / unreachable)"
    }
  ]
}
```

Parsing steps:
1. Iterate `results`; each has the source `url`, a `title`, and `raw_content`.
2. Summarize from `raw_content` only — do not invent details not present in the text.
3. Iterate `failed_results`; collect every `url` that failed and its `error`.
4. Report failures explicitly instead of silently dropping them.
5. If `raw_content` is very long, summarize per-document, keeping one citation per source URL.

## Citation behavior

- Each successfully extracted URL becomes one citation `[n]`, keyed to its own `url`.
- Failed URLs are NOT given a citation number; they are listed in a separate "Could not retrieve" note.
- Because the user provided the URLs, cite the exact URL the user gave (after normalization).

## Final answer pattern

```
Here is a summary of the articles I could retrieve:

- State of AI 2026: enterprise AI adoption reached 78% in 2026. [1]
- AI Funding Q1 2026: Q1 2026 venture funding into AI startups totaled $24B. [2]

Could not retrieve:
- https://broken.example.com/missing (404 / unreachable)

Sources:
[1] State of AI 2026 — https://example.com/ai-report-2026
[2] AI Funding Q1 2026 — https://example.com/ai-funding-q1
```

## Common failure mode

Ignoring `failed_results` and presenting a summary as if all URLs were read, or falling back to web search for the broken URL and quietly substituting different content the user never asked for. This misleads the user about coverage and provenance.

## Improved version

- Always read both `results` and `failed_results`.
- Summarize strictly from `raw_content`; never fill gaps from memory.
- Surface failures with their `error` so the user can decide whether to re-share or fix the link.
- Optionally retry a failed URL once with `extract_depth: "advanced"` before declaring it unreachable.

```json
{
  "urls": [
    "https://example.com/ai-report-2026",
    "https://example.com/ai-funding-q1",
    "https://broken.example.com/missing"
  ],
  "extract_depth": "advanced"
}
```
