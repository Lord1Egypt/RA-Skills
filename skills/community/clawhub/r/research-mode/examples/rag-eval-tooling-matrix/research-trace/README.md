# Research Trace

This directory contains a sanitized trace of the Research Mode task
`example-rag-eval-tooling-xlsx-20260616`.

The trace is included so readers can inspect how a task moved through sources,
findings, bounded iterations, verification, and review-gated finalization.

Sanitization notes:

- Absolute local paths were replaced with placeholders such as
  `<research-root>` and `<research-mode-repo>`.
- Cron payload prompts were omitted from `state.json`.
- Runtime caches, virtual environments, SQLite databases, and transient local
  process files are not included.
- The reviewed output package remains one directory above this trace.
