---
title: "Installer re-registers SessionStart boot hook on every install: 11 duplicate entries on Parker's machine"
status: open
priority: P1
owner: unassigned
reviewer: Installer CC Partner
repo: wip-ldm-os-private
created: 2026-07-04
---

## What happened

On 2026-07-04 Parker reported Claude Code sessions running visibly slow. Investigation found `~/.claude/settings.json` had **11 entries in the `hooks.SessionStart` array**: 10 identical copies of the LDM OS boot hook plus 1 branch-guard entry.

```
"SessionStart": [
  { "matcher": "*", "hooks": [{ "command": "node /Users/lesa/.ldm/shared/boot/boot-hook.mjs", ... }] },
  { "hooks": [{ "command": "node /Users/lesa/.ldm/extensions/wip-branch-guard/guard.mjs", ... }] },
  { "matcher": "*", "hooks": [{ "command": "node /Users/lesa/.ldm/shared/boot/boot-hook.mjs", ... }] },
  ... 8 more identical boot-hook entries ...
]
```

Every new Claude Code session ran the boot script 10 times in a row. The boot hook emits ~45KB of boot context per run, so session start was slow and the context injection was multiplied. Parker experienced this as "you are running so slow."

## Root cause hypothesis

`ldm install`'s hook deployment appends the SessionStart hook entry to `~/.claude/settings.json` without checking whether an identical entry already exists. Every install (including alpha/beta validation installs, which are frequent on this machine) adds another copy. The count roughly tracks the number of installs since the boot hook shipped.

Needs confirmation in `lib/deploy.mjs` (or wherever hook registration lives): find the append site and verify there is no exact-match idempotency check.

## Manual remediation already applied (machine state, not the fix)

On 2026-07-04, CC deduped Parker's `~/.claude/settings.json` manually: 11 SessionStart entries down to 2 (one boot hook, one branch guard). Backup at `~/.claude/settings.json.bak-2026-07-04`. The bug remains in the installer; the duplicates will start accumulating again on the next `ldm install` until this ticket ships.

## Fix

1. **Idempotent registration.** Before appending a hook entry to any agent settings file (`~/.claude/settings.json`, `~/.openclaw/openclaw.json`, `~/.ldm/agents/*/settings.json`), check for a structurally identical entry (same event, matcher, command). If present, skip. If present but stale (e.g. different timeout), update in place rather than append.
2. **Dedupe existing state.** `ldm doctor` gets a duplicate-hook check; `ldm doctor --fix` collapses exact-duplicate hook entries, keeping one. Same backup-before-mutation pattern as the dedup-orphans ticket: timestamped `.bak-*` before any settings write.
3. **Surface it.** Install summary reports "hook already registered, skipped" and doctor reports "N duplicate hook entries collapsed."

## Acceptance

- Running `ldm install` twice in a row on a fixture HOME produces exactly one SessionStart boot-hook entry, byte-identical settings on the second run.
- `ldm doctor` on a fixture with 10 duplicate boot-hook entries reports them; `--fix` collapses to 1 and writes a timestamped backup first.
- Regression test covers: fresh install (entry added), repeat install (no duplicate), duplicate-laden settings (doctor detects, fix collapses, unrelated hooks and unknown keys preserved).
- No partial writes: malformed settings JSON skips with a warning, same skip-with-warning contract as `2026-05-14--cc-mini--installer-dedup-orphans-hook-configs.md`.

## Out of scope

- Orphaned/stale hook path cleanup (owned by `2026-05-14--cc-mini--installer-dedup-orphans-hook-configs.md`).
- OpenClaw plugin hook registration, unless inspection shows the same append-without-check pattern there; if it does, note it and either fold in or file a sibling ticket.

## Related

- `2026-05-14--cc-mini--installer-dedup-orphans-hook-configs.md` (same settings-file mutation surface; that one removes stale entries, this one stops duplicate registration).
- `2026-05-14--cc-mini--ldm-doctor-fix-crash-startsWith.md` (doctor `--fix` reliability; the dedupe pass added here must not land on top of a crashing fix loop).

## Update 2026-07-05 (adoption note)

This ticket was written Friday morning in the installer-hook-dedup session and adopted into main on 2026-07-05. Its scope has since split and largely shipped:

- Idempotent registration + persist: FIXED in `src/boot/installer.mjs` (PR #1086, shipped v0.4.85-alpha.31/32).
- `ldm doctor` dedupe with backup: SHIPPED same PR; collapsed the origin machine's duplicates on 2026-07-05.
- The remaining accumulation vector is the SECOND registrar: see `2026-07-05--cc-mini--deploy-hook-ownership-misses-boot-hook.md`. This ticket closes to archive when that one ships.
