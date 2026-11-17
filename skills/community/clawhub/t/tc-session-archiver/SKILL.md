---
name: session-archiver
description: Archive and organize completed OpenClaw session logs into structured markdown notes for long-term memory retention. Use when wrapping up a long session, consolidating work logs, or preparing daily memory files for review.
metadata: { "openclaw": { "emoji": "📦" } }
---

# Session Archiver

Turn raw session transcripts into clean, searchable markdown archives.

## When to use

- End of a long work session — distill key decisions, actions taken, and open items
- Preparing a daily memory file (`memory/YYYY-MM-DD.md`) from conversation history
- Archiving a completed project thread for future reference

## What it does

1. **Extracts** key events, decisions, and action items from session text
2. **Tags** entries with categories (decision, action, blocker, insight)
3. **Writes** structured markdown to a target file (default: `memory/YYYY-MM-DD.md`)

## Prerequisites

- `read` access to the session transcript or conversation text
- Write access to the target archive file
- The `date` command for timestamping

## Steps

### 1. Read the source material

```
read path/to/session-log.md
```

If the session is this session, summarize from memory instead of re-reading.

### 2. Extract structured entries

Parse the text into categorized bullets:

- **Decisions** — choices made, with rationale
- **Actions** — things done, with outcome
- **Blockers** — what stopped progress, resolution status
- **Insights** — lessons learned, patterns noticed

### 3. Write to archive file

Format:

```markdown
# YYYY-MM-DD Session Log

## Decisions
- [decision description] — rationale

## Actions
- [action description] — result

## Blockers
- [blocker description] — resolved/unresolved

## Insights
- [insight description]
```

Write to `memory/YYYY-MM-DD.md` (append if file exists).

### 4. Cross-reference

If a decision has a linked PR, file, or external URL, include it inline. Use absolute workspace paths for local files.

## Notes

- Never archive secrets, tokens, or private credentials — redact first
- Keep entries terse; this is an index, not a transcript
- If the session is still active, note what's still in progress rather than finishing prematurely
