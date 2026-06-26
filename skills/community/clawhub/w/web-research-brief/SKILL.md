---
name: research-assistant
description: Structured web research and synthesis. Use when the user needs to investigate a topic, compare options, gather sources, or produce a research brief. Triggers on phrases like "research", "look into", "find out about", "compare", "what's the latest on", "deep dive", or "literature review".
---

# Research Assistant

Systematic web research → source extraction → structured synthesis.

## Workflow

1. **Scope** — Clarify the research question and constraints (time range, region, language, depth). If ambiguous, infer from context and state assumptions.
2. **Search** — Use `web_search` with targeted queries. Run 2-4 queries with varied phrasing to reduce blind spots. Prefer `freshness` filter for time-sensitive topics.
3. **Fetch** — Use `web_fetch` on the most relevant results. Extract key claims, data points, and source URLs. Skip paywalled or low-value pages quickly.
4. **Synthesize** — Organize findings into a structured brief (see Output Format).
5. **Cite** — Every factual claim must include a source URL. Flag unsourced claims explicitly.

## Search Strategy

- Start broad, then narrow with domain-specific terms
- For comparisons: search each option independently, then "X vs Y" queries
- For technical topics: include version numbers or date ranges
- For regional info: set `country` and `language` parameters on `web_search`
- If initial results are thin, rephrase or switch to a different angle before concluding "no results"

## Output Format

```markdown
# Research Brief: [Topic]

## Summary
2-4 sentence executive summary.

## Key Findings
1. **[Finding]** — [1-line detail]. [Source](url)
2. **[Finding]** — [1-line detail]. [Source](url)

## Comparison (if applicable)
| Criterion | Option A | Option B |
|-----------|----------|----------|
| ... | ... | ... |

## Open Questions
- [Unresolved item 1]
- [Unresolved item 2]

## Sources
- [Title](url) — retrieved [date]
- [Title](url) — retrieved [date]
```

## Quality Checks

- At least 3 distinct sources for any claim
- No fabricated URLs — every link must come from actual search/fetch results
- Flag recency: note if a source is > 1 year old
- If results are contradictory, present both sides rather than picking one
