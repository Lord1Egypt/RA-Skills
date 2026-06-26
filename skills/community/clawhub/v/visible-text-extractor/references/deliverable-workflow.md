# deliverable-workflow

## Goal
Give users a near-workbench experience from a single command.

## One-step deliverable flow

Use `scripts/extract_visible_text_deliverable.py` when the user wants a final deliverable instead of raw extraction.

It should produce:
- `*.raw.json` — extraction audit layer
- `*.clean.json` — cleaned structured result
- `*.clean.md` — human-readable markdown
- `*.docx` — Word deliverable

## Best-fit scenarios

- WeChat article -> clean Word doc
- Event poster / screenshot set -> readable report
- Image-heavy page -> readable summary plus docx

## Required behavior

- Preserve raw data for audit, but do not force users to open it
- Default users to the clean markdown/docx outputs
- Keep wording readable and avoid raw OCR noise in the Word deliverable
- Separate confirmed text from uncertain text when needed
