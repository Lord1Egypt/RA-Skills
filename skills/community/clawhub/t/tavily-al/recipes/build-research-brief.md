# Recipe: Build a Research Brief

## Goal
Produce a structured, multi-section research brief on a topic, grounded in multiple Tavily sources, with clear sections, citations, and a sources appendix.

## When to use
- The user wants more than a one-line answer: an overview, key facts, perspectives, and open questions.
- The topic benefits from multiple sub-queries and corroboration across domains.
- Do NOT use for a single direct question (`answer-with-sources.md`) or a single-URL summary (`extract-and-summarize.md`).

## Inputs
| Input | Required | Description |
|-------|----------|-------------|
| `topic` | Yes | The subject of the brief. |
| `TAVILY_API_KEY` | Yes | From environment. Never hardcode. |
| `sections` | No | Desired sections (default: Overview, Key facts, Perspectives, Risks/Open questions). |
| `freshness` | No | If recency matters, use `topic:"news"` + `time_range`. |
| `depth` | No | Number of sub-queries (default 3–5). |

## Steps
1. **Read `TAVILY_API_KEY`** from environment; abort if missing.
2. **Decompose the topic** into 3–5 focused sub-queries (see `prompts/query-planning.md`), one per intended section/angle.
3. **Search each sub-query** via `POST https://api.tavily.com/search` (`search_depth:"advanced"`, modest `max_results`). Validate status each time.
4. **Collect and dedupe** results across sub-queries; rank by `score`; prefer diverse, independent domains.
5. **Extract** full `raw_content` for the highest-value 3–6 URLs to ground specific claims.
6. **Evaluate sources** (see `prompts/source-evaluation.md`): drop weak/low-score/single-source claims.
7. **Draft each section**, synthesizing strictly from retrieved content, attaching `[n]` citations to every factual claim.
8. **Hallucination-check** (`prompts/hallucination-check.md`) the whole brief.
9. **Assemble** the brief with a title, sections, and a numbered sources appendix.

## Output format
```
# Research Brief: <topic>

## Overview
<grounded paragraph with [n] citations>

## Key Facts
- <fact> [n]

## Perspectives
<differing viewpoints, each cited>

## Risks / Open Questions
- <open question or uncertainty>

## Sources
[1] Title — https://example.com/a
[2] Title — https://example.com/b
```

## Example
Topic: "State of solid-state EV batteries, 2025." Decompose into: (1) current production status, (2) leading companies, (3) technical barriers, (4) recent announcements (`topic:"news"`). Search each, extract top sources, then write the four sections with citations.

## Edge cases
- **Sub-query returns nothing:** Reformulate or merge with an adjacent angle; note any gap in coverage.
- **Conflicting claims across sources:** Surface the conflict in "Perspectives" with both citations.
- **Thin overall evidence:** State limitations explicitly rather than overstating.
- **429 mid-process:** Back off; continue with what was gathered and flag incomplete sections.

## Production notes
- Budget calls: a handful of `advanced` searches plus a few targeted extracts is usually enough; avoid extracting every result.
- Reuse one source across sections rather than re-searching the same fact.
- Keep a running map of `claim -> source[n]` to make the hallucination check fast.
- > Verification needed: confirm best practices for batching searches/extracts at scale with https://docs.tavily.com
