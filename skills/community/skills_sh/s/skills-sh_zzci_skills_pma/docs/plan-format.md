# Plan Format Reference

This document defines the plan management format for the `docs/plan/` directory, including ID rules and initialization templates.

## Table of Contents

- [Directory Structure](#directory-structure)
- [Index Entry Format](#index-entry-format)
- [Detail File Format](#detail-file-format)
- [Plan ID Rules](#plan-id-rules)
- [Status Markers](#status-markers)
- [Update Rules](#update-rules)
- [Index Templates](#index-templates)

## Directory Structure

```text
docs/plan/
├── index.md          # Plan index (one line per plan)
└── PLAN-NNN.md       # Plan detail files (one per plan)
```

## Index Entry Format

Each plan in `index.md` is a single-line link with creation date and no sub-fields.

```markdown
- [ ] [**PLAN-001 Short plan title**](PLAN-001.md) `YYYY-MM-DD`
```

All detailed information goes in the corresponding detail file.

## Detail File Format

Create the detail file atomically when adding a new plan line to `index.md`.

### English Template

```markdown
# PLAN-001 Short plan title

- **status**: draft
- **createdAt**: YYYY-MM-DD HH:mm
- **approvedAt**: (pending)
- **relatedTask**: PREFIX-NNN

## Context

Investigation findings and current state: which files/modules are involved, call chains, existing logic.

## Proposal

Specific changes: what to modify and how to modify it. Include code snippets.

## Risks

Side effects, potential bugs, migration needs.

## Scope

Estimated scope of changes.

## Alternatives

(If multiple approaches exist, list comparisons here.)

## Annotations

(User annotations and responses. Keep all history.)
```

### Detail File Update Rules

- Allowed detail `status` values: `draft`, `implementing`, `completed`, `rejected`
- Approved: set `status` to `implementing`, set `approvedAt` to current timestamp
- Completed: set `status` to `completed`
- Rejected: set `status` to `rejected`, add reason to annotations
- User annotations: append to annotations and keep all history

## Plan ID Rules

- Format: `PLAN-NNN` (fixed prefix `PLAN` + zero-padded 3-digit sequence)
- Sequence starts from `001`, incrementing globally
- Once assigned, never reuse or renumber
- Each ID maps to exactly one file: `docs/plan/PLAN-NNN.md`

## Status Markers

| Marker | Meaning | Detail file `status` |
|------|------|------|
| `[ ]` | Draft / Pending review | `draft` |
| `[-]` | Approved / Implementing | `implementing` |
| `[x]` | Completed | `completed` |
| `[~]` | Rejected / Abandoned | `rejected` |

## Update Rules

- **`index.md`**: Update only checkbox markers (for example, `[ ]` -> `[-]`). Never delete plan lines.
- **Detail files**: Update status, approvedAt, and annotations in place. Never delete existing sections.
- New plans append to the end of `index.md`.
- Plan IDs are permanent.

## Index Templates

### English Template

```markdown
# Project Name - Plan Index

> Updated: YYYY-MM-DD

## Usage

Each plan is a single line linking to its detail file. All detailed information lives in `docs/plan/PLAN-NNN.md`.

### Format

- [ ] [**PLAN-001 Short plan title**](PLAN-001.md) `YYYY-MM-DD`

### Status Markers

| Marker | Meaning |
|--------|---------|
| `[ ]`  | Draft / Pending review |
| `[-]`  | Approved / Implementing |
| `[x]`  | Completed |
| `[~]`  | Rejected / Abandoned |

### Rules

- Only update the checkbox marker; never delete the line.
- New plans append to the end.
- See each `PLAN-NNN.md` for full details.

---

## Plans

```
