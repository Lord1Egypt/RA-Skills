# Graph API

## Contents

- Paper search
- Bulk paper search
- Paper batch
- Author search
- Author batch
- Working rules

## Paper Search

Use `GET /graph/v1/paper/search` for interactive search and query refinement.

- Best for smaller result sets and iterative exploration.
- Supports query text plus filters such as year, fields of study, publication types, open-access constraints, and sort options when supported by the endpoint.
- Keep `fields` minimal.

## Bulk Paper Search

Use `GET /graph/v1/paper/search/bulk` for broad retrieval jobs.

- Best for literature harvesting, screening sets, and downstream export.
- Uses continuation-token pagination rather than normal offset paging.
- Save raw records to JSONL before flattening them to CSV or spreadsheets.
- The bundled script `scripts/semantic_scholar_bulk_search.py` implements retries, continuation handling, and CSV export.

## Paper Batch

Use `POST /graph/v1/paper/batch` when paper IDs are already known.

- Better than issuing many single-record calls.
- Useful after search, recommendations, or external ID collection.
- Ask only for required fields.

## Author Search

Use `GET /graph/v1/author/search` to discover candidate authors by name.

- Use this before author batch fetches when only names or loose clues are known.
- Expect ambiguity for common names; use affiliation, topic, or publication clues where available.

## Author Batch

Use `POST /graph/v1/author/batch` when author IDs are known.

- Efficient for pulling metadata for many authors at once.
- Keep returned fields tight.

## Working Rules

- Prefer Graph API for live, user-facing retrieval tasks.
- Use bulk search instead of repeated interactive search calls when the goal is corpus construction.
- Batch endpoints are the default once IDs are known.
- For endpoint-specific parameter details, verify against the live docs before relying on a rarely used filter.
