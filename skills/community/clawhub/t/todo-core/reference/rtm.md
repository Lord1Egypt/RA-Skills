# Requirements traceability (RTM, optional)

Loaded by `/todo-plan`, `/todo-add` and `/todo-continue` only when an RTM exists. Part of the `todo` core skill. A project without an RTM loses nothing: no command asks for one, creates one, or fails because it is missing.

## Where it lives (resolution)

1. `docs/RTM.md`, when the file exists. It wins even if README.md also has an RTM section.
2. Otherwise the `## RTM` section of README.md (the heading line is exactly `## RTM`; the section ends at the next `## ` heading).
3. Otherwise there is no RTM: skip everything below. The skills never create one on their own; the user opts in by creating `docs/RTM.md` or an `## RTM` section (a plan or add run may offer it once, never twice).

`tools/todo-rtm.sh [repo-root]` in the todo-skills repository (optional, read-only, not shipped in the plugin) prints the resolved location and checks the rules below, including R3: the same Req ID in two rows is reported as a duplicate mapping.

## Format

A Markdown table with these columns; extra prose around it is ignored:

```markdown
| Req | Requirement | Tasks | Verification |
|---|---|---|---|
| R-001 | Refresh returns a new token and rejects the old one | FEAT-002, FEAT-002.1 | tests/auth/refresh.test.ts |
```

- **Req** is a stable ID (`R-001`), never renumbered or reused.
- **Tasks** lists task IDs only. It never holds markers, status or text copied from TODO.md: the task's marker in TODO.md (or its entry in CHANGELOG.md) is the only state. An ID stays in the row after the task is drained; it resolves through CHANGELOG.md.
- **Verification** names the test files or ids that prove the requirement, taken from the tasks' `Done when` commands. It may be empty while the tasks are open.

## Rules for the commands

- `/todo-plan` and `/todo-add`: when the work implements a listed requirement, link the root with `Ref: <rtm path>#R-001` (anchors are free text) and show the proposed RTM row change (new row or the new task IDs appended to Tasks) in the same confirmation. Write it only on a yes. Work that maps to no requirement gets no row; do not invent requirements.
- `/todo-continue`, step 10 (complete): when a node's `Done when` tests prove a row, add their paths or ids to its Verification cell, in the same commit as the node's files (an RTM edit is a node file like a documentation-drift edit, not a backlog file). A root's drain keeps the IDs in the row; the CHANGELOG entry's `Ref:` already carries the RTM link.
- A dropped task ID is removed from Tasks in the same change (`/todo-plan --revise`, `/todo-update --status drop`).
- Never put task state, dates or design text in the RTM; link `docs/` for that.
