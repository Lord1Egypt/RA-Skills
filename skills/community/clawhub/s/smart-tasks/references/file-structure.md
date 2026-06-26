# File Structure Reference

## Directory Layout

```
tasks/
├── INDEX.md              # Active task summary (read every session)
├── .meta.json            # Counter and metadata
├── active/               # In-progress tasks
│   ├── T-001_example.md
│   └── T-002_another.md
├── done/                 # Completed tasks (recent 30 days)
│   └── T-003_finished.md
└── archive/              # Long-term storage
    └── 2026-Q1/
        └── T-004_old.md
```

## File Naming Convention

Pattern: `{ID}_{slug}.md`

- **ID**: `T-NNN` — zero-padded 3-digit counter from `.meta.json`
- **slug**: kebab-case English summary of the title
  - Korean titles → brief English translation
  - Max ~40 chars for the slug portion
- Examples:
  - `T-001_aaai-review.md`
  - `T-012_midterm-grading.md`
  - `T-023_weekly-lab-meeting-prep.md`

The ID prefix enables quick lookup and sort. The slug provides human readability.

## INDEX.md Format

```markdown
# Tasks Index

> Last updated: 2026-04-02
> Active: 5 | Overdue: 1 | Due this week: 3

## 🔴 Overdue

| ID | Title | Due | Priority | Category |
|----|-------|-----|----------|----------|
| T-001 | AAAI Review | 2026-03-31 | high | Research |

## 🟡 Due This Week

| ID | Title | Due | Priority | Category |
|----|-------|-----|----------|----------|
| T-002 | Midterm Exam Prep | 2026-04-05 | high | Teaching |
| T-003 | Paper Feedback | 2026-04-04 | medium | Research |

## 📋 Later

| ID | Title | Due | Priority | Category |
|----|-------|-----|----------|----------|
| T-004 | KCC Draft Review | 2026-04-15 | medium | Research |

## 📊 Summary

Brief status note or weekly highlight.
```

### Section Rules

- **🔴 Overdue**: `due < today` and `status == active`
- **🟡 Due This Week**: `today <= due <= end_of_week(Sunday)`
- **📋 Later**: `due > end_of_week` or no due date
- Rows sorted by `due` ascending within each section
- Header counters must match actual row counts

### Empty State

When a section has no tasks, show `_None_` instead of an empty table.

## .meta.json Format

```json
{
  "nextId": 1,
  "created": "2026-04-02",
  "categories": []
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `nextId` | number | Next available task number. Increment after each create. |
| `created` | string | Date the task system was initialized (YYYY-MM-DD). |
| `categories` | string[] | Known categories (user-defined, accumulated over time). |

### Usage

1. Read `.meta.json` before creating a task.
2. Use `nextId` to form the ID: `T-{padded nextId}`.
3. Increment `nextId` and write back.
4. If the task introduces a new category, append it to `categories`.

### ID Padding

- `nextId: 1` → `T-001`
- `nextId: 12` → `T-012`
- `nextId: 100` → `T-100`
- `nextId: 1000` → `T-1000` (4 digits OK when exceeding 999)

## Archive Structure

```
archive/
└── YYYY-QN/          # Quarter-based folders
    ├── T-005_old-task.md
    └── T-006_another-old.md
```

Quarter mapping: Q1 = Jan–Mar, Q2 = Apr–Jun, Q3 = Jul–Sep, Q4 = Oct–Dec.
Use the completion date to determine the quarter folder.
