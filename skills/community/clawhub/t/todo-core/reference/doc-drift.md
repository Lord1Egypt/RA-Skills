# Documentation drift: searching and reporting

Read on demand from `todo-continue` ("Documentation drift"), only when the node changed a public interface. Part of the `todo` core skill.

- Search README.md and `docs/` (not `docs/plans/`) for each changed name with `grep -rnF -- '<name>' README.md docs`.
- Report every hit as an actionable reference, one line each: `<file>:<line>: <name> - <what to change>` (for example `docs/REFERENCE.md:48: --worktree - flag renamed to --tree`). Update the hits that fit within the task line (`Docs: updated <file>` for the CHANGELOG entry; no git: the root's `State: docs:`); give the rest as `/todo-add "update <file>:<line> for <name>" --type task --from <ID>` commands in the report. Only a hit the `Done when` or the Definition of Done names blocks the node. Uses grep only; no new tool.
