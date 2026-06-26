---
name: weread-obsidian
description: Sync WeRead shelf state, reading progress, visible book content, and note-ready Markdown into a local workspace using the user's logged-in Chrome session. Use when the user wants to inspect WeRead bookshelf status, capture book metadata or text for a specific book, or prepare WeRead material for Obsidian, Feishu, or OpenClaw note workflows.
---

# WeRead Obsidian Skill

Use this skill when the user wants a bridge between WeRead and their note workflow.

## What this skill does

- Pulls shelf-level data from `https://weread.qq.com/web/shelf` through the user's existing Chrome login session
- Captures a single book's page state and visible reading content into JSON
- Exports Markdown files that are easy for Obsidian, Feishu bots, or OpenClaw to consume
- Supports chat-friendly shortcuts for syncing by book title and appending polished reflections back into the matching Obsidian note
- Uses a least-privilege default: visible DOM only, no browser storage dump, and Obsidian writes only through `obsidian-cli`

## Preconditions

1. The user must already be logged into WeRead in Chrome.
2. Chrome remote debugging must be enabled at `chrome://inspect/#remote-debugging`.
3. The local CDP proxy from the `web-access` skill must be available on `http://localhost:3456`.

## Workflow

1. Pull the bookshelf snapshot:

```bash
node scripts/fetch-shelf.mjs
```

This writes `output/weread/shelf.json`.

2. Capture one book:

```bash
node scripts/fetch-book.mjs --book-url "https://weread.qq.com/..."
```

This writes `output/weread/books/<slug>.json`.

3. Export Markdown for note-taking:

```bash
node scripts/export-obsidian.mjs --shelf output/weread/shelf.json --book output/weread/books/<slug>.json
```

This writes Markdown under `output/obsidian/`.

4. Publish Markdown into Obsidian through `obsidian-cli`:

```bash
node scripts/publish-obsidian.mjs --dir output/obsidian
```

This writes notes into the default vault configured in `obsidian-cli`, or the vault passed with `--vault`.

## Shortcut commands

When the user gives a book title and wants the note synced end to end, prefer:

```bash
node scripts/sync-book-by-title.mjs --title "书名" --vault claw_notes
```

This refreshes the shelf snapshot, resolves the closest matching book title, fetches that book, exports Markdown, and publishes the book note into Obsidian.

When the user wants to add reading reflections to an existing book note, first polish the user's rough wording into concise note prose, then write it back with:

```bash
node scripts/add-book-reflection.mjs --title "书名" --reflection "润色后的读后感" --vault claw_notes
```

This stores the reflection as sidecar data under `output/weread/reflections/`, re-renders the book Markdown, and republishes the note so later syncs do not wipe the reflection section.

## Natural-language triggers

- If the user says “同步《书名》笔记”, “把这本书同步到 Obsidian”, or “按书名抓这本书”, use `sync-book-by-title.mjs`.
- If the user says “帮我给这本书加一段读后感”, “润色后写回 Obsidian”, or “把这些感想整理进笔记”, rewrite the reflection first, then use `add-book-reflection.mjs`.
- If the requested book has not been synced yet, run the title-based sync first, then append the reflection.

## Installability

This repository is structured as a self-contained skill repo.

- Install the repository root as the skill source.
- Runtime commands should call files in `scripts/` directly.
- The repo-root `package.json` only provides local developer aliases and is not required by the skill logic itself.

## Operating guidance

- Default to shelf sync plus one-book content sync. Do not bulk-export every book's full text unless the user explicitly asks and understands the risk.
- Prefer using a real book URL captured from the shelf or copied from the browser instead of guessing a reader URL pattern.
- For title-based sync, prefer exact title matches first; if matching is ambiguous, surface the top candidates before taking action.
- The content capture is intentionally conservative: it records visible or scroll-loaded text from a single page flow so the downstream note system can summarize, annotate, and ask follow-up questions.
- Do not collect cookies, browser storage, or unrelated local application config.
- If WeRead changes its DOM, inspect the saved JSON first; the scripts already preserve raw page clues for follow-up repairs.

## Outputs

- `output/weread/shelf.json`: bookshelf snapshot, candidate book links, storage hints, page diagnostics
- `output/weread/shelf.json`: bookshelf snapshot and page diagnostics from visible DOM
- `output/weread/books/*.json`: per-book metadata, visible content, notes/highlights candidates, diagnostics
- `output/weread/reflections/*.json`: user-authored or polished reflections that should survive future exports
- `output/obsidian/*.md`: Markdown notes ready for vault ingestion or LLM conversation
- Obsidian vault notes: created through `obsidian-cli create --overwrite`

## Downstream use

- Obsidian can ingest the Markdown files directly.
- If `obsidian-cli` is available, publish the generated Markdown into the vault and let OpenClaw continue working from vault notes instead of raw export files.
- Feishu or OpenClaw can read the generated Markdown or JSON and turn it into prompts, summaries, or reading-note conversations.
- The recommended pattern is: sync data locally first, then let the downstream agent reason over files instead of talking to WeRead live on every request.
