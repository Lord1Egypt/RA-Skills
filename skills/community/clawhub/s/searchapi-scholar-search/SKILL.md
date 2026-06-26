---
name: searchapi-scholar-search
description: Academic paper discovery and evidence-oriented web search using a SerpApi/SearchAPI-compatible key. Use when the user asks for Google Scholar retrieval, paper/title/DOI/source verification, related-work discovery, foreign-language literature collection, or structured research leads for reviews, proposals, theses, and faculty/student research tasks; especially when emphasizing paper search over general web search.
metadata: {"openclaw":{"requires":{"bins":["node"],"env":["SERPAPI_API_KEY","SEARCHAPI_API_KEY"]}},"clawdbot":{"emoji":"📚","requires":{"bins":["node"],"env":["SERPAPI_API_KEY","SEARCHAPI_API_KEY"]},"primaryEnv":"SERPAPI_API_KEY"}}
---

# SearchAPI Scholar Search

Use this skill for **paper-first retrieval**. Prefer `scholar-search.mjs` when the user needs academic literature, candidate references, DOI clues, citation signals, or source verification for scholarly work.

This skill is especially good for:
- discovering English-language papers from a topic or question
- finding classic / highly cited papers quickly
- building an initial literature pool for a review, thesis, proposal, or grant application
- checking whether a paper title, source, year, or DOI is plausible
- finding official landing pages, publisher pages, repositories, and supporting evidence on the web

## What this skill can do

### 1) Scholar-based paper retrieval

Run:

```bash
node {baseDir}/scripts/scholar-search.mjs "query"
node {baseDir}/scripts/scholar-search.mjs "query" -n 10 --year-from 2020 --year-to 2026
node {baseDir}/scripts/scholar-search.mjs "query" --mode review
node {baseDir}/scripts/scholar-search.mjs "query" --mode verify
node {baseDir}/scripts/scholar-search.mjs "query" --json
```

Returns, when available:
- paper title
- authors
- publication summary / venue clues
- year
- best verification link
- cited-by count
- snippet
- DOI / DOI URL when detected or enriched
- likely paper type (`review`, `systematic-review`, `primary-study`)
- search refinement suggestions
- verification hints for downstream checking

Modes:
- `shortlist` — default; gives a practical reading shortlist
- `review` — emphasizes likely review/survey-style papers for literature review workflows using heuristic title/snippet detection
- `verify` — emphasizes title/DOI/source verification for a likely candidate paper or claim

Use this first for:
- literature discovery
- related work exploration
- title verification
- DOI/source checking
- identifying representative papers for a topic
- getting better next-step search suggestions

### 2) Evidence-oriented web search

Run:

```bash
node {baseDir}/scripts/web-search.mjs "query"
node {baseDir}/scripts/web-search.mjs "query" --json
```

Use this after Scholar search to find:
- publisher landing pages
- DOI pages
- institutional repositories
- lab/project pages
- author homepages
- non-paper evidence related to a research topic

## Recommended workflow

### A. Build a candidate paper pool

Start with Scholar search using 1-3 focused queries. Example:

```bash
node {baseDir}/scripts/scholar-search.mjs "large language models higher education" -n 8 --year-from 2021 --mode shortlist
```

Then refine queries with:
- synonyms
- narrower task terms
- domain words
- method names
- population or setting constraints
- `review` / `systematic review` when you need overview papers first

### B. Verify promising items

For strong candidates, use Scholar verify mode or web search on:
- exact paper title
- `"paper title" DOI`
- `"paper title" publisher`

This often surfaces the official landing page or repository page.

### C. Normalize outputs for downstream use

After retrieval:
- deduplicate by title / DOI
- keep official or publisher links when possible
- retain cited-by counts only as rough influence signals, not quality guarantees
- convert the final shortlist into the citation format the user needs

## Good query patterns

Use patterns like:
- `"topic keyword" method`
- `"topic keyword" review`
- `"topic keyword" systematic review`
- `"topic keyword" site:doi.org` via web search when verifying DOI presence
- exact title queries in quotes for verification

Examples:

```bash
node {baseDir}/scripts/scholar-search.mjs "intrusion detection deep learning review" -n 10 --year-from 2020 --mode review
node {baseDir}/scripts/scholar-search.mjs "large language models classroom teaching" -n 10 --year-from 2023 --mode shortlist
node {baseDir}/scripts/scholar-search.mjs '"Attention Is All You Need"' --mode verify
node {baseDir}/scripts/web-search.mjs '"Attention Is All You Need" DOI'
```

## Environment variables

The scripts read the first available key from:
- `SERPAPI_API_KEY`
- `SEARCHAPI_API_KEY`

No custom base URL override is exposed in this public edition. The skill uses the default SerpApi endpoint for consistency and auditability.

## Notes

- Prefer Scholar search for literature retrieval; use web search for source verification.
- Keep search batches small to avoid rate limits.
- DOI enrichment may query the public Crossref API when a DOI is not obvious in the search result.
- This skill is best used as the **front end of a literature workflow**: retrieve → verify → deduplicate → format citations.
- Review/survey detection is heuristic, so verify important claims on the destination page.
- For publication or academic writing tasks, do not treat search output as final truth without checking the destination page.
