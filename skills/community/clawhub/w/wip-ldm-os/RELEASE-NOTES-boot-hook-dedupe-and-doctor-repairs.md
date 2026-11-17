The boot hook installer no longer accumulates duplicate SessionStart entries in `~/.claude/settings.json`. `configureSessionStartHook()` now owns the full set of boot-hook entries: it collapses duplicates to one, updates the surviving entry in place, and persists updates to disk. The previous update path modified settings in memory and reported success without writing, so command-path and timeout changes silently never landed. Repeat installs with an identical entry are now a true no-op that does not touch the file.

`ldm doctor` gains two settings.json health checks. Duplicate hook entries (same event, matcher, and hook commands registered more than once) are reported, and `ldm doctor --fix` collapses them to one. Invalid `model` values are reported and removed under `--fix` with a pointer to re-pick the model in Claude Code; invalid means control characters (such as a real ESC 0x1B from an ANSI fragment persisted by a terminal paste) or impossible length, never a visible-charset judgment... printable bracketed IDs like `claude-fable-5[1m]` are legitimate 1M-context variants and pass untouched. Both fixes write a timestamped `settings.json.bak-*` backup before the first mutation, and a malformed settings.json is skipped with a warning instead of rewritten.

Background: 10 duplicate SessionStart boot-hook entries were found on the origin machine on 2026-07-04, each running the ~45KB boot context injection once per session start, experienced as Claude Code "running slow." Regression coverage: `scripts/test-boot-hook-registration.mjs` and `scripts/test-doctor-hook-dedupe.mjs`.

Tickets:
- `ai/product/bugs/installer/open-tickets/2026-07-04--cc-mini--installer-sessionstart-hook-duplicate-registration.md`
- `ai/product/bugs/installer/open-tickets/2026-07-04--cc-mini--boot-hook-update-in-place-never-persists.md`
- `ai/product/bugs/guard/2026-07-04--cc-mini--no-blessed-recipe-for-live-settings-remediation.md` (doctor-owned repair shape; guard whitelist remains open)
