# Accuracy and Fallbacks

## Accuracy rules

- Preserve the original title whenever possible; do not rewrite it for storage.
- Preserve the original URL.
- Keep source/account/publisher separate from your own summary.
- If publish time is not directly extractable, mark it as missing instead of guessing.
- Treat PDF generation as a rendering task, not a content-understanding task.

## Export order

1. Export TXT first. This is the ground-truth extracted text snapshot.
2. Export DOCX next when the user wants an editable/shareable document.
3. Export PDF with Chrome/Chromium when the user wants page-like fidelity.

## Fallbacks

- If PDF fails, still keep TXT and DOCX.
- If webpage extraction is partial, keep the URL and note that extraction needs browser/manual review.
- If the page is dynamic or anti-bot protected, use browser-assisted inspection before claiming the page is unavailable.
- Treat `STATUS=partial` as usable-but-incomplete output: keep the TXT and metadata JSON, then decide whether a browser-assisted retry is worth it.
- Use the JSON metadata file as the authoritative machine-readable summary of success, partial success, warnings, and output paths.
- Prefer browser-rendered DOM fallback when static HTML extraction is too short or obviously shell-like; record whether fallback was used and do not hide the difference between static and browser-rendered text.

## Storage

Default archive root:
a local `webpage-exports/` folder under the current working directory, unless the task explicitly sets another output path.

Recommended subdirectories:
- `raw/` for original downloads
- `processed/` for cleaned outputs
- `temp/` for testing or intermediate exports
