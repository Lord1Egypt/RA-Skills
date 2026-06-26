# Example 04 — Multi-Step Research Workflow

Decompose a broad question into sub-questions, run several searches, extract the strongest sources, and synthesize a cited brief.

## User request

> "Write me a short briefing on the current state of solid-state batteries for electric vehicles: who the leaders are, the main technical hurdles, and expected timelines."

## Agent reasoning summary

- The question has three distinct facets (leaders, hurdles, timelines) — I will decompose and search each separately for better coverage.
- After gathering candidate sources, I will extract the highest-scoring ones to get full text rather than relying on short snippets.
- I will synthesize across sources and cite each claim.

## Tavily operation to use

Use **search** (multiple calls, one per sub-question) to discover sources, then **extract** on the top-ranked unique URLs to get `raw_content` for synthesis.
Why: search casts a wide net per facet; extract gives faithful full text for the few sources worth quoting. This two-stage pattern reduces hallucination and improves citation accuracy.

## Request shape

Step 1 — three searches (one per sub-question):

```json
{ "query": "leading companies developing solid-state batteries for EVs 2026", "search_depth": "advanced", "include_answer": true, "max_results": 6 }
```
```json
{ "query": "technical challenges solid-state battery dendrites manufacturing scale", "search_depth": "advanced", "max_results": 6 }
```
```json
{ "query": "solid-state battery EV commercialization timeline expected production year", "search_depth": "advanced", "max_results": 6 }
```

Step 2 — extract the top unique URLs surfaced across the three searches:

```json
{
  "urls": [
    "https://example.com/ssb-leaders",
    "https://example.com/ssb-challenges",
    "https://example.com/ssb-timeline"
  ],
  "extract_depth": "advanced"
}
```

## Response handling

1. For each search, sort `results` by `score`, filter `score >= 0.5`.
2. Pool all surviving results, then deduplicate by normalized URL across the three searches (the same source may appear in more than one facet).
3. Select the top ~3-5 unique, highest-scoring URLs that collectively cover all three facets.
4. Extract those URLs; parse `results[].raw_content`, and note any `failed_results`.
5. Synthesize each facet's paragraph strictly from extracted `raw_content` (and high-score `content` snippets where extraction failed).
6. Keep a map of claim -> source URL throughout, so citation numbers stay stable.

## Citation behavior

- Each unique source URL gets one stable citation number, assigned once and reused.
- Claims drawn from extracted text cite the URL that was extracted.
- If a facet relies on a search snippet (because extract failed for that URL), cite the search result URL instead and note nothing special — the URL is the source either way.

## Final answer pattern

```
Briefing: Solid-State Batteries for EVs

Leaders. Several automakers and specialists are racing to commercialize solid-state cells, with [Company A] and [Company B] reporting pilot lines. [1]

Technical hurdles. The main obstacles are dendrite formation at the lithium-metal anode and the difficulty of manufacturing thin, defect-free solid electrolytes at scale. [2]

Timelines. Most public roadmaps target limited production toward the latter part of the decade, with mass-market EV deployment expected afterward. [3]

Sources:
[1] Solid-State Battery Leaders — https://example.com/ssb-leaders
[2] Solid-State Battery Challenges — https://example.com/ssb-challenges
[3] Solid-State Battery Timeline — https://example.com/ssb-timeline
```

## Common failure mode

Running a single broad search ("solid-state batteries EV") and trying to answer all three facets from a handful of shallow snippets. Coverage is uneven, timelines get vague, and some claims end up uncited or invented.

Another failure: extracting too many URLs (e.g., all 18 pooled results), wasting credits and diluting the synthesis.

## Improved version

- Decompose into the three explicit sub-questions and search each.
- Pool, dedup, and score-filter before selecting only the 3-5 best URLs to extract.
- Synthesize from extracted `raw_content`, keeping one stable citation per source.
- Handle `failed_results` by falling back to that URL's search snippet.

```json
{ "query": "leading companies developing solid-state batteries for EVs 2026", "search_depth": "advanced", "include_answer": true, "max_results": 6 }
```

> Verification needed: confirm best-practice limits on number of URLs per extract call at https://docs.tavily.com
