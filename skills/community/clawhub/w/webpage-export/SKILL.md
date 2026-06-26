---
name: webpage-export
description: Export webpages into clean local TXT, DOCX, and PDF files with source metadata, fallback extraction logic, and browser-assisted recovery for difficult pages. Useful for archiving articles, policy pages, WeChat posts, official notices, and other webpages before downstream analysis or sharing.
---

# Webpage Export

Use this skill to turn a webpage URL into local files that downstream agents can archive, send, or reference.

## Core workflow

1. Run `scripts/export_webpage.py <url>` to create a TXT snapshot first.
2. Treat TXT as the baseline extracted record.
3. Add `--docx` when the user wants a Word document.
4. Add `--pdf` when Chrome/Chromium is available and the user wants a PDF.
5. Keep the generated JSON metadata file; it records extraction quality, paths, warnings, and partial-failure status for downstream agents.
6. Save outputs to an explicit `--outdir` when the user provides one; otherwise let the script use its local default export folder under the current working directory.
7. For accuracy-sensitive work, keep original title, original URL, and extracted source metadata.

## Commands

### TXT only

```bash
python3 scripts/export_webpage.py "<url>"
```

### TXT + DOCX

```bash
python3 scripts/export_webpage.py "<url>" --docx
```

### TXT + PDF

```bash
python3 scripts/export_webpage.py "<url>" --pdf
```

### TXT + DOCX + PDF with explicit output folder

```bash
python3 scripts/export_webpage.py "<url>" --docx --pdf --outdir ./exports/temp
```

## Runtime requirements

- Requires `python3`.
- Requires `curl` for baseline webpage fetching.
- PDF export requires Chrome or Chromium.
- Browser-assisted fallback requires `node` and the `playwright` package.
- DOCX export on macOS requires `textutil`.

## Safety and execution notes

- This skill fetches arbitrary URLs and may use a headless browser for difficult pages.
- Browser-assisted fallback executes page JavaScript and should be used only when needed.
- Prefer explicit `--outdir` values for production or shared environments.

## What the script does

- Fetch the page with `curl`
- Extract title/source/publish-time when available
- Try multiple body candidates before falling back to a full-page text snapshot
- Score extraction quality and emit warnings for suspicious/partial results
- Strip HTML into readable text for a TXT snapshot
- Convert TXT to DOCX using `textutil` on macOS
- Render webpage to PDF using Chrome/Chromium headless printing when available
- Emit a JSON metadata file with status, paths, word count, quality, and warnings

## Format choice

- Prefer **TXT** as the baseline extracted record.
- Prefer **DOCX** when the user wants an editable or shareable document.
- Prefer **PDF** when the user wants page-like rendering or easier direct viewing.
- For important work, do not treat PDF as the only source of truth.

## Chrome/Chromium PDF path

When the user wants PDF, prefer Chrome/Chromium headless printing because it preserves Chinese text and webpage layout better than ad-hoc PDF generation.

Read `references/chrome-pdf-guide.md` when:
- you need the exact Chrome PDF logic
- PDF output is incomplete or suspicious
- Chrome emits warnings and you need to judge whether the result is still usable
- you need fallback decisions

## Accuracy and fallbacks

Read `references/accuracy-and-fallbacks.md` when:
- source accuracy matters
- webpage metadata is incomplete
- a field cannot be extracted cleanly
- you need fallback behavior after a partial extraction

## Delivery decisions

Read `references/delivery-rules.md` when:
- deciding whether to deliver TXT, DOCX, PDF, or a combination
- preparing files for downstream agents or user delivery
- choosing archive placement under the local workspace

## Limitations

- Some highly dynamic or anti-bot pages may extract only partially.
- PDF depends on Chrome/Chromium being installed.
- DOCX depends on macOS `textutil`.
- If a page is blocked in lightweight fetch mode, use this skill's curl-based extraction path before giving up.

## Accuracy rule

Accuracy is the top standard. Keep original title, original URL, and extracted source metadata. If any field is uncertain, mark it as missing instead of guessing.
