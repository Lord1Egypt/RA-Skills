---
title: "Installer dedup leaves orphaned hook entries in agent settings files"
status: open
priority: P1
owner: unassigned
reviewer: Installer CC Partner
repo: wip-ldm-os-private
created: 2026-05-14
---

## What it does

When the installer dedups a duplicate registry entry and moves the duplicate directory to `~/.ldm/_trash/`, it ALSO removes any hook entries in agent settings files (`~/.claude/settings.json`, `~/.openclaw/openclaw.json`, `~/.ldm/agents/*/settings.json`) that reference paths inside the moved directory.

## What it fixes

Alpha.30 dedup-trash migration (PR #955) moved `~/.ldm/extensions/package/` to `~/.ldm/_trash/` but Claude Code's `settings.json` still had two hook entries pointing at `~/.ldm/extensions/package/guard.mjs`. The hooks didn't crash (Claude Code skips missing hooks with a warning) but `ldm doctor` flagged them as stale. On Parker's 2026-05-13 dogfood install, this surfaced as "2 actionable issues" right after a successful install, eroding trust that the dedup was clean.

## How to dogfood

1. Paste the install prompt into a fresh AI session on a machine with known duplicate hook configs (this scenario; Parker's machine before alpha.30 had it).
2. Say install.
3. After install: `ldm doctor` should report ZERO stale-hook issues. Today (alpha.30) it reports 2 stale hooks because the cleanup is incomplete.
4. Verify: `grep ~/.claude/settings.json` for any paths under `~/.ldm/extensions/<deduplicated-name>/`. Should be empty.

## Fix

The migration's `executeDirectoryMoves` should also:

1. Take the agent-settings file paths as input (Claude Code, OpenClaw, per-agent settings).
2. For each moved directory, scan those settings files for hook entries referencing the old directory path.
3. Remove the stale entries (or rewrite them to point at the canonical directory if a 1:1 canonical replacement exists, like `package` → `wip-branch-guard`).
4. Surface the cleanup in the install summary.

## Acceptance

- Migration scans Claude Code `settings.json` + OpenClaw `openclaw.json` + per-agent settings for hook entries referencing moved directories.
- Stale entries get removed (or remapped to the canonical) before the install completes.
- `ldm doctor` reports 0 stale-hook issues immediately after install.
- Regression test simulates the `package` → `wip-branch-guard` dedup with both hooks present; asserts the `package` hook entry is removed and the `wip-branch-guard` hook entry is untouched.
- **Dry-run preview**: `ldm install --dry-run` shows the planned hook-config edits without writing any settings file.
- **Backup before mutation**: every settings/config file the migration touches gets a timestamped `.bak-<ISO-timestamp>` backup written before the mutation, same pattern as `registry.json.bak-*`.
- **Preserve unrelated config exactly**: unknown keys, ordering, and formatting are preserved to the extent the existing parser/writer allows. The migration touches only the hook entries it has reason to remove.
- **Skip-with-warning on errors**: on malformed JSON, missing files, permission failures, or unsupported config shape, skip that file with an explicit warning in the install summary rather than partially writing it. No partial mutations.
- **Regression coverage**: the test suite includes the happy path (valid `settings.json` with a stale hook entry, mutated cleanly) AND at least one skipped-file path (malformed JSON triggers the skip-with-warning behavior, no mutation).

## Out of scope

- The LaunchAgent plist drift that doctor also flagged (separate issue; not caused by dedup).
- A broader hook-config validation tool. This ticket just makes dedup clean up after itself.

## Related

- PR #955 / alpha.30 dedup-trash fix (parent; this is the incomplete-cleanup follow-up).
- `2026-05-13--cc-mini--installer-dedup-reverts-between-installs.md` (where the dedup-trash fix was implemented).
