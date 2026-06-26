---
summary: "Refactor options (next wins)"
read_when:
  - Planning cleanup work
  - Touching retry/logging/output plumbing
---

# Refactor options (next wins)

Small wins

- “List + page” helper: generic wrapper for `--max/--page` + `nextPageToken` output.
- Standardize list headers: consistent column naming (ID/NAME/EMAIL/etc).
- “Output row” helpers: centralize `sanitizeTab` use for tabular output.

Medium wins

- Drive “export format” registry: single map for docs/sheets/slides format help + validation.
- Shared “service bootstrap” helpers: reduce per-command boilerplate for `requireAccount` + `newXService`.
- Test harness helpers: one fake Google API server util (Drive/Gmail/Calendar/Tasks) with common JSON assertions.

Bigger wins

- API client retry unification: one retry stack (transport vs explicit); delete the other; push logs behind `--verbose`.
- Command grouping / UX: consolidate “download/export” story; ensure help text + flags match across services.
