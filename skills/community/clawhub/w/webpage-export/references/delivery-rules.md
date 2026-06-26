# Delivery Rules

## Output priority

Choose outputs based on the real request, but follow this priority logic:

1. TXT = baseline extraction record
2. DOCX = editable/shareable output
3. PDF = layout-preserving output

For accuracy-sensitive work, do not deliver only PDF without keeping TXT or source metadata.

## Recommended combinations

### If the user says "extract webpage content"

Deliver:
- TXT
- extracted metadata summary in chat if useful

### If the user says "make it a Word file"

Deliver:
- TXT
- DOCX

### If the user says "make it a PDF"

Deliver:
- TXT
- PDF

### If the user says "archive this webpage"

Deliver/store:
- TXT
- original URL
- metadata
- optionally DOCX/PDF

## Accuracy first

Never optimize for format over correctness.

If PDF looks pretty but content is incomplete, prefer the TXT/DOCX as the trustworthy output and explicitly note the PDF issue.

## Storage guidance

Recommended root:
`./exports/` or another explicit folder chosen for the task.

Typical usage:
- `temp/` for tests and intermediate exports
- `raw/` for original download artifacts
- `processed/` for cleaned and finalized deliverables
