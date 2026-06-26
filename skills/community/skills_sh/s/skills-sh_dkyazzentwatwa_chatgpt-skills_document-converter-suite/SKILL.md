---
name: document-converter-suite
description: Convert PDFs, Office docs, markdown, HTML, and tables between editable formats. Use for best-effort document conversion, PDF utilities, form filling, and table extraction.
---

# Document Converter Suite

Run best-effort extraction and rebuild workflows across common document formats. Preserve clean structure, not pixel-perfect layout.

## Use This For

- Converting between `pdf`, `docx`, `pptx`, `xlsx`, `txt`, `csv`, `md`, and `html`
- Pulling tables or spreadsheet-style grids into editable outputs
- Running utility PDF operations such as merge, split, rotate, watermark, or page extraction
- Filling simple document or form-style templates

## Workflow

1. Confirm the source format, target format, and whether editability or fidelity matters more.
2. Use `scripts/convert.py` for single documents and `scripts/batch_convert.py` for folders.
3. Use the bundled utility scripts when the user needs a focused PDF or table task:
   - `scripts/pdf_toolkit.py`
   - `scripts/table_extractor.py`
   - `scripts/form_filler.py`
4. Say explicitly when the output is best-effort and likely to lose layout, images, OCR text, or advanced formatting.

## Guardrails

- Do not promise visual fidelity.
- Treat scanned PDFs as OCR problems, not conversion problems.
- Raise safety caps gradually on large sheets or documents instead of processing everything blindly.

## References

- `references/conversion_matrix.md` for supported paths.
- `references/limitations.md` for failure modes and tradeoffs.
