# ClawHub review — 2026-11-07

Fixed quoted-attribute injection in SVG titles/node IDs/share cards and gallery filename links. Inline gallery JSON now encodes HTML-significant characters so a string cannot close the script element. Parser-based tests assert exact data round-trips, absence of attacker event attributes and no additional script elements. These tests are not a live browser execution test.

Validation now uses a unique temporary directory and cleans only that directory. Repo extraction and git comparisons are intentional local reads. Subprocess calls use argument arrays, not shell interpolation. Diagram fixture text is example content, not skill invocation policy. No publication or upload is performed by the renderer.

A follow-up scan found Git option injection in revision arguments. Version 1.8.3 rejects option-like revisions, resolves names with rev-parse --end-of-options, and sends only validated object IDs to diff. It disables external diff/textconv execution and honors the selected repository root. Regression tests include a file-truncation payload and valid commit/worktree changes.
