# Output Schema

The wrapper returns JSON with these top-level fields:

- `package`: requested PyPI package name.
- `resolved_versions`: resolved `from`, `to`, and original `range` expression.
- `mode`: current execution mode. The implemented values are `git`, `archive`, or `error`.
- `source`: repository source details.
- `auth`: whether a GitHub token was supplied.
- `commits`: commit-level evidence.
- `reviews`: PR-level evidence.
- `file_changes`: file-level diff evidence.
- `file_changes[*].patch`: git diff-style text excerpt. Python and Markdown patches are kept whole; non-Python/Markdown added or removed files only keep headers; other non-Python/Markdown patches may be truncated.
- `metadata_changes`: Python requirement, license, classifier, or packaging metadata changes.
- `dependency_changes`: dependency additions, removals, and version changes.
- `breaking_signals`: high-risk change indicators.
- `truncation`: whether evidence was truncated.
- `warnings`: non-fatal execution notes.
- `errors`: fatal or partial-failure messages.

When summarizing, rely on evidence instead of guessing. If a field is empty, do not invent content.
