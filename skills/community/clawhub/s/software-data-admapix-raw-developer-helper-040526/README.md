# AdMapix Raw Data Developer Helper

## What It Does

Design and harden AdMapix-style raw data workflows for creative, app, ranking, revenue, and analytics datasets before they become dashboards or agent tools.

This package was generated from demand signals in run `20260623-040526` and then rewritten for publication with domain-specific workflow guidance instead of generic task scaffolding.

## Best For

Data engineers, growth analysts, skill authors, and agent builders adapting popular admapix-style raw data workflows.

## Workflow Summary

1. Identify raw sources, refresh cadence, entity keys, metrics, dimensions, privacy constraints, and target consumers.
2. Create a source-to-table map that separates immutable raw captures from cleaned views, feature extracts, and presentation layers.
3. Specify validation rules for required columns, date ranges, currency, locale, creative IDs, app IDs, duplicate rows, and missing metrics.
4. Plan failure handling for API quota, partial exports, schema drift, backfill gaps, and vendor naming changes.
5. Recommend lightweight local implementation steps using CSV, JSON, SQLite, or DuckDB before heavier warehouse work.
6. Return an audit trail with source, transform version, row counts, anomalies, and consumer-facing caveats.

## Deliverables

- A raw-to-clean data model for AdMapix-style inputs.
- Validation checks for schema drift, duplicates, missing values, and metric consistency.
- A local script or pseudocode plan for ingestion and normalization.
- A reliability checklist for publishing the workflow as an agent skill.

## Quality Bar

- Raw data remains reproducible and separate from cleaned outputs.
- Every transform records source, timestamp, row count, and known anomalies.
- The workflow handles partial data, schema drift, and quota failures explicitly.
- The recommended implementation can run on ordinary CPU hardware.

## Trigger Examples

- `Use $software-data-admapix-raw-developer-helper to design a raw data layer for ad creative exports.`
- `Clean this app-ranking CSV without losing the original source data.`
- `Create validation checks for an AdMapix-style analytics skill.`

## Files

- `SKILL.md`: English skill instructions.
- `SKILL.zh-CN.md`: Chinese skill instructions.
- `README.md`: English user-facing guide.
- `README.zh-CN.md`: Chinese user-facing guide.
- `references/requirement-plan.md`: Demand evidence and scoring details.
- `agents/openai.yaml`: Default invocation metadata.
