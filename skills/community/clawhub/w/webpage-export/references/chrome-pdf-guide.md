# Chrome PDF Guide

## Why prefer Chrome/Chromium for PDF

Use Chrome/Chromium headless printing as the preferred PDF path when the goal is to preserve webpage layout with better Chinese rendering and fewer乱码 issues than ad-hoc PDF generation.

Compared with plain text PDF generation, Chrome PDF is better for:
- WeChat articles
- Official policy pages
- Long-form web articles
- Pages where the user expects visual page fidelity

## Standard command pattern

The script wraps this pattern internally:

```bash
'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' \
  --headless=new \
  --disable-gpu \
  --no-first-run \
  --virtual-time-budget=15000 \
  --print-to-pdf=/path/to/output.pdf \
  '<url>'
```

## When to use Chrome PDF

Use Chrome PDF when:
- the user explicitly asks for PDF
- the page contains Chinese text and plain PDF generation caused乱码 before
- the page is primarily a normal article/detail page
- layout fidelity matters more than editability

## When NOT to rely on Chrome PDF alone

Do not rely on Chrome PDF alone when:
- you still need structured text extraction for summarization or database fields
- the page is heavily dynamic and content may not finish loading in time
- the page is access-controlled and requires login/cookies not available in headless mode
- the page contains attachments that should be downloaded separately instead of merely rendered

In those cases:
- still keep TXT as the extraction baseline
- optionally keep DOCX for editable delivery
- treat PDF as one output, not the only source of truth

## Required companion outputs

For accuracy-sensitive work, keep at least:
- TXT snapshot
- original URL
- title/source metadata

For user delivery, optionally add:
- DOCX
- PDF

## Common issues

### 1. PDF generated successfully but content is incomplete

Likely cause:
- page did not finish rendering before print

Action:
- increase `--virtual-time-budget`
- re-run once
- if still incomplete, inspect the page with browser-assisted workflow

### 2. Chrome prints the shell page but not the article body

Likely cause:
- dynamic rendering, anti-bot behavior, or blocked resources

Action:
- keep TXT extraction result
- record that browser/manual review is needed
- do not pretend the PDF is complete if the article body is missing

### 3. Chrome path not found

Check these common locations:
- `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
- `/Applications/Chromium.app/Contents/MacOS/Chromium`

If neither exists:
- install Chrome/Chromium
- fall back to TXT/DOCX until PDF path is restored

### 4. Console warnings appear during headless print

Some Chrome/macOS warnings do not block PDF generation.
Judge by outcome:
- if PDF file is generated and content is correct, treat as success
- if file is missing or content is broken, treat as failure and fall back

## Success criteria

A Chrome-generated PDF is only considered valid when:
- the file exists
- Chinese text renders correctly
- the main body is present
- title/source can still be matched against the original page

If any of these fail, keep TXT/DOCX and mark PDF as failed or incomplete.
