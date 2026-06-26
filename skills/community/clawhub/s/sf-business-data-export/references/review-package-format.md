# Review Package Format

This reference defines the minimum structure of a review-ready export package.

## Required Artifacts Per Object

- field catalog file
- object-level SOQL file
- exported `.xlsx` file unless the user explicitly requested another format

## Required Package Artifact

- manifest file summarizing object outputs and validation results

## Field Catalog Minimum Columns

- `object_api_name`
- `field_api_name`
- `field_label`
- `field_source`
- `included_in_export`
- `is_key_field`
- `status`
- `status_reason`

## Manifest Minimum Columns

- `object_api_name`
- `status`
- `failure_category`
- `failure_stage`
- `failure_reason`
- `field_catalog_path`
- `soql_path`
- `export_path`
- `field_coverage_ratio`
- `expected_field_count`
- `exported_field_count`
- `query_row_count`
- `raw_row_count`
- `deduped_row_count`
- `export_row_count`
- `column_count`
- `next_action`

## Status Rules

- use `success` only when the object passes DoD validation
- use `failed` when the object cannot meet input, metadata, query, export, or validation requirements
- do not mark partial outputs as `success`

## Reviewer Expectations

A business reviewer should be able to answer these questions from the package without re-running the export:

- Which objects were requested?
- Which objects succeeded?
- Which objects failed?
- Which fields were expected and actually exported?
- Which query was used?
- What row counts were validated?
- What should happen next if something failed?
