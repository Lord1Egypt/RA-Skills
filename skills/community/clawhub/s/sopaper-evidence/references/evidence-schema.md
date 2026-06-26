# Evidence Schema

Use this schema to capture evidence in a way that can later support paper writing.

## Required fields

- `id`: stable short identifier such as `E01`
- `statement`: the exact claim, observation, or fact being captured
- `classification`: one of `verified_fact`, `project_evidence`, `inference`, `unverified`
- `source_type`: paper, repo, benchmark, dataset, official_doc, local_result, local_code, note, or other clear label
- `source_title`: paper title, page title, file name, or artifact name
- `source_locator`: URL, DOI, arXiv link, benchmark URL, or local file path
- `date`: publication date, access date, or experiment run date if known
- `relevance`: why this matters for the user's paper
- `limitations`: where the evidence does not apply, or what remains unknown

## Recommended fields

- `authors_or_owner`
- `venue`
- `metric`
- `task`
- `dataset_or_benchmark`
- `supports_claims`
- `contradicts_claims`
- `notes`

## Classification rules

### `verified_fact`

Use when the statement is supported directly by a primary source.

Example:
- A benchmark page defines the evaluation metric
- A paper reports a specific result table

### `project_evidence`

Use when the statement is supported by the user's own project artifacts.

Example:
- Internal experiment table shows a 12% improvement on task success
- Local config proves which ablation settings were run

### `inference`

Use when the statement is a reasonable interpretation built from verified evidence, but is not stated directly by a source.

Example:
- Several papers suggest real-world transfer remains difficult for this task

### `unverified`

Use when the statement may be true but has not yet been checked against a reliable source.

## Minimal evidence entry

```md
- id: E01
  statement: "Benchmark X evaluates long-horizon mobile manipulation with success rate."
  classification: verified_fact
  source_type: benchmark
  source_title: "Benchmark X"
  source_locator: "https://example.com/benchmark-x"
  date: "2025-06-01"
  relevance: "Useful for framing OpenClaw evaluation."
  limitations: "Need to verify whether OpenClaw tasks align exactly with benchmark task definitions."
```

## Usage rule

Do not let writing depend on `unverified` items. Use them only as search leads until they are upgraded or discarded.
