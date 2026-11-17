# Boot hook payload trim: default caps + staleness cutoff + summary line

Task 4b of the CC speedup master plan (PR #1087). Shrinks the SessionStart boot-hook context payload that every Claude Code session pays for on boot.

## What changed

`src/boot/boot-hook.mjs` now trims its own payload, with all defaults active in code so they reach existing installs without any config change (the installer preserves an existing user `boot-config.json` and never overwrites it):

1. **Per-step default line caps.** Steps that do not set `maxLines` in `boot-config.json` now get a code default: `sharedContext` 80, `soul` 80, `context` 60, `repoLocations` 80. When a file is truncated, the injected content ends with a marker that names the full path so the rest can be read on demand. Any per-step `maxLines` in config still wins.

2. **Staleness cutoff for most-recent steps.** If the newest journal is older than `stalenessDays` (default 14), its body is NOT injected: a single line with the path, date, and age is emitted instead. This stops a four-months-old "most recent" journal from being re-injected every session. `daily-logs` steps have the same guard via `dailyLogStalenessDays` (default 2); day files are today/yesterday by construction, so it is defensive.

3. **One-line payload summary.** The last line of every boot payload now reads, e.g.: `== Boot payload: 26691 bytes, 485 lines, 8 sections. Capped: Step 2, Step 3, Step 7, Step 9. Stale/path-only: Step 8. Missing: none. ==`. Future slowness triage is now trivial.

`src/boot/boot-config.json` and `shared/boot/boot-config.json` (seed templates) document the new optional keys (`stalenessDays`, `dailyLogStalenessDays`, and explicit per-step `maxLines`) with the same defaults. Template changes only reach fresh installs; existing installs rely on the code defaults above.

`src/boot/README.md` documents the caps, staleness behavior, summary line, and new config keys.

## Before / after

Measured on a fixture shaped like the real 2026-07-04 session (SOUL 12.3KB, SHARED-CONTEXT 12.2KB, CC journal 4.9KB dated 2026-03-02, CC daily 4.7KB, Parker journal 4.4KB dated 2026-06-23, repo-locations 4.2KB, CONTEXT 2.4KB), using the SAME deployed-style config for both runs (no config changes):

- **Before (origin/main hook):** 46170 bytes (45.1 KB), 851 lines
- **After (new hook, code defaults active):** 26828 bytes (26.2 KB), 487 lines
- **Saved:** 18.9 KB, 41.9% reduction

The four-months-old CC journal drops to a path-only line (stale); the 11-day-old Parker journal is kept but line-capped at 80.

## Tests

`npm run test:boot-payload-trim` (new, `scripts/test-boot-payload-trim.mjs`). Six cases, all passing:

- uncapped-by-config step gets the code default cap + a truncation marker naming the full path
- per-step `maxLines` in config overrides the default
- a stale most-recent journal emits a path-only line, body not injected
- a fresh most-recent journal is injected in full
- the payload summary line is present with capped/stale steps listed
- `maxTotalLines` still stops the loop early

Also `node --check` on the changed `.mjs`, JSON validation on both config templates, and a fallback run confirming `getDefaultConfig()` still exits 0 when no `boot-config.json` is present.

## Scope / not touched

- `src/boot/installer.mjs` is intentionally untouched to stay conflict-free with open PR #1086.
- No deployed files under `~/.ldm`, `~/.openclaw`, `~/.claude` were modified. Merge -> Deploy -> Install pipeline unchanged.
