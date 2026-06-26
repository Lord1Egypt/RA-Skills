# Data Contract

The scripts in this skill produce stable local artifacts so other tools can consume WeRead data without re-opening the browser every time.

## `output/weread/shelf.json`

Top-level fields:

- `capturedAt`: ISO timestamp
- `page`: page diagnostics, title, URL, and body text snippet from the visible shelf page
- `books`: de-duplicated shelf items with title, href, guessed book id, dataset attributes, and nearby text
- `rawCandidates`: lower-confidence DOM matches kept for debugging when `--debug-dom` is enabled

## `output/weread/books/<slug>.json`

Top-level fields:

- `capturedAt`: ISO timestamp
- `sourceUrl`: URL used for capture
- `page`: page diagnostics and visible page headings
- `metadata`: title, subtitle, author, intro, cover, page headings
- `toc`: chapter-like links or headings that look navigable
- `notes`: note, highlight, bookmark, or review-like blocks visible in DOM
- `content`: scroll-captured paragraphs and combined markdown-friendly text

## `output/weread/reflections/<slug>.json`

Purpose:

- store user-authored or OpenClaw-polished reflections separately from raw capture
- survive future `export-obsidian` runs
- provide a stable append-only history for personal reading thoughts

Top-level fields:

- `title`: resolved book title
- `slug`: book slug used for file naming
- `entries`: reflection history

Entry fields:

- `createdAt`: ISO timestamp
- `updatedAt`: ISO timestamp
- `mode`: `raw` or `polished`
- `content`: markdown-friendly reflection prose

## `output/obsidian/weread-shelf.md`

Purpose:

- quick shelf review
- entry point for downstream prompts
- manual selection of the next book to sync deeply

## `output/obsidian/books/<slug>.md`

Purpose:

- durable per-book knowledge artifact
- can be read by Obsidian or any LLM tool
- includes prompt-ready sections for OpenClaw/Feishu workflows
- merges any saved reflections into the `读后感与我的卡片` section

Suggested downstream prompt pattern:

1. Read the Markdown note for a specific book.
2. Summarize the current chapter and key claims.
3. Extract questions worth discussing.
4. Write permanent notes or daily notes back into the vault.
