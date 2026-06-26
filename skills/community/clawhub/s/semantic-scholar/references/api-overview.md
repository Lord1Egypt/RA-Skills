# Semantic Scholar API Overview

## API Families

- Graph API: interactive paper and author search, metadata lookup, and batch fetch by IDs.
- Recommendations API: related-paper retrieval from seed paper IDs.
- Datasets API: offline data downloads by release, including incremental diffs between releases.

## Selection Guide

- Choose Graph API when the user wants live search, filtering, ranking, author lookup, or metadata retrieval for a manageable set of records.
- Choose Recommendations API when the user already has relevant papers and wants adjacent literature.
- Choose Datasets API when the user needs corpus-scale offline files or release-to-release changes.

## Cross-Cutting Practices

- Authenticate with `x-api-key` via `SEMANTIC_SCHOLAR_API_KEY` when available.
- Use field projection aggressively. Ask only for fields needed by the task.
- Add retry and backoff around `429` and temporary `5xx` failures.
- Record exact endpoint, parameters, and release identifiers so results are reproducible.
- Preserve raw API output before flattening or filtering it.

## Typical User Requests

- "Find papers about agentic materials discovery from 2020 onward" -> Graph API search or bulk search.
- "Fetch metadata for these paper IDs" -> Graph API batch.
- "Find similar papers to these seed articles" -> Recommendations API.
- "Download the latest papers dataset and compare it with the prior release" -> Datasets API.
