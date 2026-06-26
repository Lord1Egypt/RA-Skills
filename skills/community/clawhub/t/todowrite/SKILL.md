---
name: todowrite
metadata:
  author: es6kr
  version: "0.1.0"
depends-on: [wip]
description: Route TODO checklists to the right storage. session - in-session tracking via /wip, file - persistent TODO (fix_plan.md, TODO.md), issue - team-shared via GitHub Issues. "TODO management", "checklist", "todowrite", "fix_plan cleanup", "register as issue" triggers.
---

# TodoWrite

Route TODO checklists to the appropriate storage based on context.

## Routing Decision

```
New TODO arrives
  ├─ Only needed this session → /wip (TaskCreate/TodoWrite)
  ├─ Persists beyond session → file (fix_plan.md, TODO.md)
  └─ Team-shared → issue (GitHub Issues)
```

## Topics

| Topic | Storage | Lifetime | Tool |
|-------|---------|----------|------|
| session | TaskCreate/TodoWrite | Session | → `/wip` skill |
| file | fix_plan.md, TODO.md | While file exists | Write/Edit |
| issue | GitHub Issues | Permanent | `gh issue create` |

## Session → /wip

Current session task tracking is handled by the `wip` skill:

```
/wip    # Track session work with TodoWrite/TaskCreate
```

## File-based TODO

### fix_plan.md (Ralph projects)

```markdown
## Pending

- [ ] Item 1 — description
- [ ] Item 2 — description

## Completed

- [x] Done item — (completed: 2026-04-03, commit abc1234)
```

**Rules:**
- Move to `Completed` section on completion + timestamp
- Mark blocked items with `[BLOCKED]` tag
- Mark skipped items with `[SKIPPED]` tag

### TODO.md (General projects)

```markdown
# TODO

## High Priority
- [ ] Urgent item

## Normal
- [ ] Regular item

## Done
- [x] Completed item (2026-04-03)
```

## Issue-based TODO

Team-shared TODOs go to GitHub Issues:

```bash
# Create issue (user approval required)
gh issue create --title "Item" --body "Description"

# List issues
gh issue list --label "todo"
```

**Note:** `gh issue create` only runs when user explicitly says "create an issue".

## Routing Examples

| Situation | Route | Reason |
|-----------|-------|--------|
| "Run this 5-step deploy" | `/wip` (session) | Session tracking is sufficient |
| "Fix this bug later" | file (fix_plan.md) | Persists beyond session |
| "Assign this to Jinju" | issue (GitHub) | Team sharing needed |
| "Note this from the review" | file (fix_plan.md) | Outside current PR scope |
