---
name: semantic-scholar
description: Search, retrieve, and organize scholarly metadata with the Semantic Scholar APIs. Use when Codex needs to find papers or authors, build paper sets from complex queries, fetch records in batch by IDs, get related-paper recommendations from seed papers, or decide between Graph API, Recommendations API, and Datasets API workflows for Semantic Scholar.
---

# Semantic Scholar

## Overview

Choose the right Semantic Scholar API workflow before writing code or issuing requests. Prefer small, field-scoped online calls for interactive search, `paper/search/bulk` for large retrieval jobs, recommendations when the user already has seed papers, and datasets only for offline or release-based data pulls.

## Workflow Decision Tree

Start by classifying the task:

- Use the Graph API for live paper or author lookup, metadata retrieval, query refinement, and batch fetches by known IDs.
- Use the Recommendations API when the user already has one or more relevant papers and wants similar or related work.
- Use the Datasets API when the user needs offline snapshots, release-to-release diffs, or corpus-scale ingestion rather than interactive search.

Then choose the endpoint pattern:

- Use `paper/search` for normal interactive search, smaller result sets, ranking, and iterative query tuning.
- Use `paper/search/bulk` for large result collection; it uses continuation-token pagination and is the default for broad literature harvesting.
- Use `paper/batch` or `author/batch` when the user already has IDs and wants metadata efficiently.
- Use `author/search` for author discovery by name or affiliation-like clues.
- Use recommendations for "papers like this one" workflows.

## Operating Rules

- Request only the fields needed for the task. Semantic Scholar explicitly supports field projection; smaller field lists are faster and less error-prone.
- Prefer API key authentication via `SEMANTIC_SCHOLAR_API_KEY` when available, especially for repeated or larger jobs.
- Handle pagination explicitly. `paper/search` and `author/search` are interactive search flows; `paper/search/bulk` uses continuation tokens.
- Add retry and backoff for `429` and transient `5xx` responses.
- Preserve raw results before flattening or post-processing them.
- For broad discovery, write Boolean-rich queries instead of a single brittle phrase. Use exact phrases only when the user asks for them.
- Do not route normal search tasks to Datasets API. Use datasets only when the user truly needs offline release files or diffs.

## Typical Workflows

### Search papers interactively

Use this for "find papers about X", "search by title keywords", or "filter by year/citations/open access".

- Start with `paper/search` if the user expects inspection and refinement.
- Keep `fields` minimal.
- If the search must collect many records, switch to `paper/search/bulk`.
- Read [references/query-recipes.md](references/query-recipes.md) for query patterns.
- Read [references/graph-api.md](references/graph-api.md) for endpoint details.

### Harvest a broad paper set

Use this for literature review corpora, screening spreadsheets, or downstream ranking.

- Prefer `scripts/semantic_scholar_bulk_search.py`.
- Save raw output to JSONL and only then export CSV if the user needs tabular review.
- Expose query, year filter, sort, and field selection as parameters instead of hardcoding them.

### Fetch by known IDs

Use `paper/batch` or `author/batch` when IDs are already known from previous steps or user input.

- Batch fetch is usually better than repeated single-record lookups.
- Ask for only the fields required for the analysis or export.

### Expand from seed papers

Use recommendations when the user says things like "find papers similar to this", "expand from these seed papers", or "build a related-work set".

- Use the Recommendations API instead of trying to approximate similarity with a new keyword query.
- Keep the seed-paper IDs and result set separate from keyword-search results so provenance stays clear.
- Read [references/recommendations-api.md](references/recommendations-api.md).

### Pull datasets or release diffs

Use the Datasets API only for offline ingestion or change tracking between releases.

- Read [references/datasets-api.md](references/datasets-api.md).
- Confirm storage expectations before downloading large files.
- Document the exact release identifiers used in the workflow.

## References

- Read [references/api-overview.md](references/api-overview.md) first when deciding which API family to use.
- Read [references/graph-api.md](references/graph-api.md) for paper and author search, batch, pagination, and field projection.
- Read [references/recommendations-api.md](references/recommendations-api.md) for related-paper workflows.
- Read [references/datasets-api.md](references/datasets-api.md) for release, download, and diff workflows.
- Read [references/query-recipes.md](references/query-recipes.md) for Boolean query templates and search heuristics.

## Script

- Use [scripts/semantic_scholar_bulk_search.py](scripts/semantic_scholar_bulk_search.py) for broad paper harvesting with retries, continuation-token pagination, JSONL output, and optional CSV export.
- Use [scripts/paper_batch_fetch.py](scripts/paper_batch_fetch.py) to fetch paper metadata in batches from known paper IDs.
- Use [scripts/author_batch_fetch.py](scripts/author_batch_fetch.py) to fetch author metadata in batches from known author IDs.
- Use [scripts/recommend_papers.py](scripts/recommend_papers.py) to retrieve recommendation results from seed paper IDs.
- Use [scripts/smoke_test_live.sh](scripts/smoke_test_live.sh) to run one live end-to-end smoke test across all four API scripts.
