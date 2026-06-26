# Task Format Reference

This document defines the task management format for the `docs/task/` directory, including ID rules and initialization templates.

## Table of Contents

- [Directory Structure](#directory-structure)
- [Index Entry Format](#index-entry-format)
- [Detail File Format](#detail-file-format)
- [Task ID Rules](#task-id-rules)
- [Status Markers](#status-markers)
- [Priority Levels](#priority-levels)
- [Update Rules](#update-rules)
- [Index Templates](#index-templates)

## Directory Structure

```text
docs/task/
├── index.md          # Task index (one line per task)
└── PREFIX-NNN.md     # Task detail files (one per task)
```

## Index Entry Format

Each task in `index.md` is a single-line link with no sub-fields.

```markdown
- [ ] [**PREFIX-001 Short imperative title**](PREFIX-001.md) `P1`
```

All detailed information goes in the corresponding detail file. `index.md` must not contain description, owner, or other sub-fields.

## Detail File Format

Create the detail file atomically when adding a new task line to `index.md`. This maps cleanly to `TaskCreate` parameters.

### English Template

```markdown
# PREFIX-001 Short imperative title

- **status**: pending
- **priority**: P1
- **owner**: (unassigned)
- **createdAt**: YYYY-MM-DD HH:mm

## Description

What needs to be done, with context and acceptance criteria.

## ActiveForm

Present-continuous description for spinner display.

## Dependencies

- **blocked by**: (none)
- **blocks**: (none)

## Notes

(Implementation notes, progress logs, or related links.)
```

### Detail File Update Rules

- Allowed detail `status` values: `pending`, `in_progress`, `completed`, `closed`
- Claiming: set `status` to `in_progress` and set `owner`
- Completing: set `status` to `completed`, add completion notes if needed
- Closing: set `status` to `closed`, add reason
- In progress: append progress notes to the notes section

## Task ID Rules

- Format: `PREFIX-NNN` (uppercase category prefix + hyphen + zero-padded 3-digit sequence)
- Prefix is a short category abbreviation, for example: `AUTH`, `UI`, `API`, `BUG`, `PERF`, `FEAT`, `REFACTOR`
- Sequence numbers are per-prefix, starting from `001`
- Once assigned, never reuse or renumber
- Each ID maps to exactly one file: `docs/task/PREFIX-NNN.md`

## Status Markers

| Marker | Meaning | TaskUpdate status |
|------|------|-------------------|
| `[ ]` | Pending | `pending` |
| `[-]` | In progress | `in_progress` |
| `[x]` | Completed | `completed` |
| `[~]` | Closed / Won't do | `deleted` |

## Priority Levels

| Tag | Meaning |
|-----|------|
| `P0` | Blocking issue, handle immediately |
| `P1` | High priority, current iteration |
| `P2` | Medium priority, next iteration |
| `P3` | Low priority, to be planned |

## Update Rules

- **`index.md`**: Update only checkbox markers (for example, `[ ]` -> `[x]`). Never delete task lines.
- **Detail files**: Update status, owner, and notes in place. Never delete existing fields.
- New tasks append to the end of `index.md`.
- Task IDs are permanent.

## Index Templates

### English Template

```markdown
# Project Name - Task List

> Updated: YYYY-MM-DD

## Usage

Each task is a single line linking to its detail file. All detailed information lives in `docs/task/PREFIX-NNN.md`.

### Format

- [ ] [**PREFIX-001 Short imperative title**](PREFIX-001.md) `P1`

### Status Markers

| Marker | Meaning |
|--------|---------|
| `[ ]`  | Pending |
| `[-]`  | In progress |
| `[x]`  | Completed |
| `[~]`  | Closed / Won't do |

### Priority: P0 (blocking) > P1 (high) > P2 (medium) > P3 (low)

### Rules

- Only update the checkbox marker; never delete the line.
- New tasks append to the end.
- See each `PREFIX-NNN.md` for full details.

---

## Tasks

```
