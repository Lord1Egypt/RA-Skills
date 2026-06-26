# weread-import design

## Positioning

`weread-import` is a reusable CLI for exporting WeRead highlights and notes into Markdown files.
A thin AgentSkill wrapper can sit on top, but the core project remains a standalone tool.

## Design goals

- Export WeRead highlights and notes into readable Markdown
- Write into any user-chosen directory
- Work well with Obsidian without hard-binding to a specific vault
- Prefer stable API-based syncing over DOM scraping
- Keep output deterministic and merge-friendly
- Stay safe to publish as an open-source project

## Core choices

### API first

Primary path:
- `/api/user/notebook`
- `/web/book/bookmarklist`
- `/web/review/list`

### Output is filesystem-first

The tool writes to a user-provided directory such as:

- `--output /absolute/path`
- `WEREAD_OUTPUT=/absolute/path`

Obsidian is treated as a normal Markdown target, not as a hard dependency.

### Auth model

Supported cookie flows:

1. Manual
   - `--cookie`
   - `WEREAD_COOKIE`
2. Browser extraction
   - `--cookie-from browser`
3. Guided manual retrieval
   - documented cookie-copy steps

Browser-backed detail syncing has one extra rule:

- in `--cookie-from browser` mode, book detail APIs should reuse the browser context
- `bookmarklist` / `review/list` are more reliable when fetched after entering the book reader context
- validation should distinguish cookie validity from browser-context-specific failures

### Merge model

The project tracks note state by `bookmarkId` / `reviewId` and classifies merge results as:

- added
- updated
- retained
- deleted

Deleted content is archived into `## 已删除` instead of being removed silently.

### Output model

Markdown output is structured for both reading and machine-friendly diff / merge:

- YAML frontmatter for structured metadata
- chapter-grouped highlights and reviews
- hidden metadata comments for IDs and sync-relevant fields
- deleted archive section with stable heading hierarchy

## Open-source constraints

- no private cookie values in logs or docs
- no hardcoded personal vault paths in runtime behavior
- deterministic output structure
- user-facing docs for cookie retrieval, output selection, and common workflows
- release validation should run in an isolated staging skill directory, not by overwriting a live agent installation
