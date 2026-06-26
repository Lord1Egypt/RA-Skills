# End-to-End Usage

This document shows a minimal local workflow for the bundled scripts.

## Workspace Setup

Set a skill root first so the commands do not depend on one user's home directory layout.

```bash
SKILL_ROOT="${CODEX_HOME:-$HOME/.codex}/skills/sf-business-data-export"
```

## Preflight Check

Run the preflight before relying on local Salesforce access or output paths.

```bash
python3 "$SKILL_ROOT/scripts/preflight_check.py" \
  --output-dir /tmp/sf-business-data-export
```

If you need to verify a specific org alias:

```bash
python3 "$SKILL_ROOT/scripts/preflight_check.py" \
  --target-org my-org-alias \
  --output-dir /tmp/sf-business-data-export
```

## Goal

Starting from one export object, produce:

- a normalized metadata bundle
- a field catalog CSV
- a validation summary JSON
- a review manifest CSV

## Sample Inputs

Use the sample files in `references/examples/`:

- `page-fields.txt`
- `field-catalog-spec.json`
- `describe-opportunity.json`
- `validation-input.json`
- `manifest-input.json`

## Step 0: Collect Metadata Inputs

Offline example using the bundled sample `describe` and page-visible fields:

```bash
python3 "$SKILL_ROOT/scripts/collect_metadata.py" \
  --sobject Opportunity \
  --describe-input "$SKILL_ROOT/references/examples/describe-opportunity.json" \
  --page-fields-file "$SKILL_ROOT/references/examples/page-fields.txt" \
  --output /tmp/sf-business-data-export/metadata_bundle.json
```

Org-backed example when Salesforce CLI auth is available:

```bash
python3 "$SKILL_ROOT/scripts/collect_metadata.py" \
  --sobject Opportunity \
  --target-org my-org-alias \
  --field-source current_page \
  --explicit-fields-file "$SKILL_ROOT/references/examples/page-fields.txt" \
  --output /tmp/sf-business-data-export/metadata_bundle.json
```

Expected output:

- `/tmp/sf-business-data-export/metadata_bundle.json`

## Step 1: Build the Field Catalog

```bash
python3 "$SKILL_ROOT/scripts/build_field_catalog.py" \
  --spec "$SKILL_ROOT/references/examples/field-catalog-spec.json" \
  --describe "$SKILL_ROOT/references/examples/describe-opportunity.json" \
  --output /tmp/sf-business-data-export/field_catalog.csv
```

Expected output:

- `/tmp/sf-business-data-export/field_catalog.csv`

## Step 2: Validate Export Results

```bash
python3 "$SKILL_ROOT/scripts/validate_export_results.py" \
  --input "$SKILL_ROOT/references/examples/validation-input.json" \
  --output /tmp/sf-business-data-export/validation_results.json
```

Expected output:

- `/tmp/sf-business-data-export/validation_results.json`

## Step 3: Write the Review Manifest

```bash
python3 "$SKILL_ROOT/scripts/write_review_manifest.py" \
  --input "$SKILL_ROOT/references/examples/manifest-input.json" \
  --output /tmp/sf-business-data-export/review_manifest.csv
```

Expected output:

- `/tmp/sf-business-data-export/review_manifest.csv`

## How These Files Fit Together

1. Build the field catalog after the field baseline and final export field set are known.
2. Run validation after SOQL execution and export row counting are complete.
3. Write the review manifest after object-level status, failure details, and output paths are known.

## Adapting For Real Exports

- replace the sample `describe` JSON with actual Salesforce `describe` output
- replace the sample spec with object-specific expected fields, exported fields, and key fields
- replace validation and manifest input JSON with actual export results
- keep object-level outputs even when validation fails so the review package remains inspectable
