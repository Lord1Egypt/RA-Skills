# Development Report - Universal Document Ingestion Router

## Date

2026-06-16

## Objective

Develop a lightweight, cross-agent document classifier/router skill that:

- classifies common document files
- routes to available local parsers
- recommends missing parser dependencies
- emits standardized parsed output for future knowledge-base ingestion
- remains lightweight and does not implement the knowledge base itself

## Implementation

Implemented CLI script:

- `scripts/document_classifier_router.py`

Commands:

- `capabilities`
- `classify --input <file>`
- `parse --input <file> --output <dir>`
- `batch --input-dir <dir> --output <dir> --copy-sources`

Output artifacts:

- `document.json`
- `document.md`
- `chunks.jsonl`
- `tables/`
- `batch_summary.json`

## Installed / Available Dependencies

Detected available:

- `markitdown 0.1.5`
- `pymupdf 1.27.1`
- `pypdf 6.12.2`
- `pdfplumber 0.11.9`
- `paddleocr 3.7.0`
- `python-docx`
- `python-pptx`
- `openpyxl 3.1.5`
- `pandas 3.0.1`
- `Pillow`

Missing:

- `LibreOffice headless`

LibreOffice was not installed because this skill is intended to stay lightweight and current tests did not require legacy `.doc/.ppt/.xls` conversion.

## Test Method

Original files were not modified. Samples were copied into:

- `C:\Users\holli\.openclaw\workspace\tmp\universal_doc_router_tests\samples`\n\nBatch test output was written to:

- `C:\Users\holli\.openclaw\workspace\tmp\universal_doc_router_tests\batch_run`\n\nCommand used:

```bash
python tools\universal_document_ingestion_router\document_classifier_router.py batch --input-dir C:\Users\holli\.openclaw\workspace\tmp\universal_doc_router_tests\samples --output C:\Users\holli\.openclaw\workspace\tmp\universal_doc_router_tests\batch_run --copy-sources\n```\n\n## Test Coverage\n\nSeven file types were tested:

- DOCX
- PDF
- PNG
- CSV
- MD
- XLSX
- PPTX

## Batch Result

- Total files: 7
- Parsed successfully: 6
- Blocked/failed: 1
- Errors: 0

Successful:

- DOCX -> `text_native`, route `markitdown_or_python_docx`
- PDF -> `text_native`, route `markitdown`
- CSV -> `tabular`, route `openpyxl_or_csv`
- MD -> `text_native`, route `direct_text`
- XLSX -> `tabular`, route `openpyxl_or_csv`
- PPTX -> `presentation`, route `markitdown_or_python_pptx`

Blocked/failed:

- PNG -> `scanned_or_image`, route `paddleocr`, but OCR returned empty output for the selected small image sample.

This failure was correctly recorded as:

- `status = blocked_or_failed`
- `quality_warnings = ["empty_extraction", "no_parser_succeeded"]`

The router did not fake success, which is the desired behavior for knowledge-base quality.

## Quality Notes

Warnings observed during execution:

- `requests` dependency warning about `urllib3/chardet/charset_normalizer` version compatibility. It did not block parsing.
- PaddleOCR deprecation warning: `use_angle_cls` should eventually be replaced by `use_textline_orientation`.

## Cross-Agent Usability

The skill is usable by OpenClaw, Hermes, Codex, Claude Code, or any agent that can run shell commands because the interface is plain CLI + JSON stdout.

No OpenClaw-only runtime APIs are required by the script.

## Current Status

Functional local skill package created at:

- `C:\Users\holli\.openclaw\workspace\skills\universal-document-ingestion-router`\n\nThe Skill Workshop proposal exists, but automatic apply failed earlier because the platform reported no approval route. Therefore this folder is the concrete usable skill package.

## Recommended Next Improvements

- Add a better OCR image fixture with real text to validate PaddleOCR success path.
- Replace deprecated PaddleOCR parameter.
- Add legacy Office test only if LibreOffice is intentionally installed.
- Add optional `--manifest-only` mode if downstream systems only need JSON.
