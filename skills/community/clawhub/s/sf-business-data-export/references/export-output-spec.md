# Export Output Spec

Use this file when assembling the final deliverables for business users.

## Required Outputs

For a review-oriented export, produce:
- one `.xlsx` file per object unless consolidation is explicitly requested
- field catalog CSVs with API name, label, and source metadata
- object-level `.soql` files
- one manifest CSV summarizing all generated files

## Excel Requirements

Excel files should:
- use Chinese labels for the header row when labels are available
- preserve technical identifiers such as record ids and owner ids
- include scope-explaining columns such as owner name, sales team, sales group, and parent owner context when relevant
- avoid Report-style truncation and row limits

## Manifest Requirements

The manifest should contain at least:
- object
- output file path
- row count
- column count

## Review Package Guidance

Optimize for business review, not just technical completeness.

Prefer:
- readable headers
- enough contextual columns to explain why a record is included
- stable filenames by object

Do not force business users to cross-reference raw SOQL to understand the file.

## Default Directory Shape

Recommended layout:

```text
analysis/
├── layout_field_catalog.csv
├── ObjectName.fields.csv
├── soql/
│   └── ObjectName.soql
└── excel_exports/
    ├── ObjectName.xlsx
    └── export_manifest.csv
```

If the project uses another output root, keep the same relative structure unless the user asks otherwise.
