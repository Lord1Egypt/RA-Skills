---
name: work-productivity-multi-search-workflow-helper
description: Coordinate multi-source web and repository search. Use when the user needs query expansion, source diversity, deduped findings, evidence grading, citation planning, or a repeatable search workflow across search engines, forums, docs, code hosts, and registries.
---

# Work Productivity Multi Search Workflow Helper

Use this skill when one search query is not enough and the user needs a disciplined way to gather corroborated evidence from multiple source families.

Read `references/requirement-plan.md` if you need the source evidence behind this skill.

## Search Plan

Start by defining:

- The decision the search should support.
- Required freshness, geography, language, or source type.
- Trusted primary sources and sources to treat as anecdotal.
- Minimum evidence count and diversity target.

## Workflow

1. Convert the user's question into 3-6 query variants: exact phrase, synonym, problem wording, tool name, error text, and negative query.
2. Assign each query to suitable source families such as official docs, GitHub issues, forums, news, package registries, academic search, or Chinese-language communities.
3. Record results with title, URL, date, source family, and why the result matters.
4. Deduplicate repeated pages, syndicated posts, and same-author reposts.
5. Grade evidence as primary, implementation signal, user pain, market signal, or weak anecdote.
6. Produce a short synthesis that distinguishes confirmed facts from plausible leads and gaps.

## Guardrails

- Do not inflate confidence from many copies of the same source.
- Prefer official documentation or primary repository evidence for technical claims.
- Note stale pages and date mismatches.
- Preserve links so the user can audit the evidence trail.

## Outputs

- Search matrix with queries, sources, and findings.
- Deduplicated evidence list with source-family coverage.
- Recommendation or answer with confidence and open gaps.
- Reusable query set for follow-up searches.

## Validation Checklist

- At least two source families are used when the question allows it.
- Duplicates and weak evidence are labeled.
- Dates are captured for time-sensitive topics.
- The final answer does not overstate what the evidence supports.

## Triggers

Keywords: multi search, evidence, source diversity, query expansion, corroborate, citations, research sweep, market scan.

Example requests:

- `Search across sources and tell me whether this tool demand is real.`
- `Use $work-productivity-multi-search-workflow-helper to build a deduped evidence table.`
- `Find primary docs, GitHub issues, and community posts for this error.`
