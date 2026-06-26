# Release Notes: wip-ldm-os v0.4.62

Closes #236, #237, #238, #239, #240

## Five bug fixes, one new command

This release fixes five bugs filed between Mar 18 and Mar 29. All five were discovered during a session where a simple task (removing a stale extension) cascaded into discovering that the installer, backup system, LaunchAgents, and CLI flag parser all had gaps. Every fix was merged, tested from the repo, and verified before release.

## What changed

### ldm install: parent package dedup + ghost cleanup (#238, #240)

The installer was showing 12 individual sub-tool updates instead of one `wip-ai-devops-toolbox` update. And `-private` extensions (like `wip-xai-grok-private` and `wip-xai-x-private`) lingered as ghosts after the public versions were installed.

Root cause for the ghosts: the installer cloned public repos but the package.json inside had `-private` names, so directories got the wrong suffix. The registry recorded the public source URL but deploy paths pointed to `-private` directories.

Fix: parent package detection deduplicates sub-tools into one update. Ghost cleanup removes `-private` registry entries and renames mismatched directories to their public names (moved to `_trash/`, never deleted).

### ldm backup command (#237)

The backup system had dead triggers competing (broken cron entry, old LaunchAgent pointing to deleted iCloud path), no way to run a backup on demand, and a size guard that silently failed on macOS (used Linux `du --exclude` flags).

Fix: dead triggers disabled on install. `ldm backup` command added with `--dry-run`, `--list`, `--pin "reason"`, and `--unpin`. Size guard rewritten for macOS (`du -I` instead of `--exclude`). Dry-run shows all backup targets with sizes.

### LaunchAgents managed by installer (#236)

LaunchAgent plists were manually placed with hardcoded paths, logs to `/tmp/` (cleared on reboot), and no PATH env var. Healthcheck still pointed to the old iCloud path.

Fix: plist templates in `shared/launchagents/` with `{{HOME}}` placeholders. `ldm install` deploys them to `~/Library/LaunchAgents/` with placeholder replacement. `ldm doctor` checks all 3 managed agents (plist exists, matches template, loaded via launchctl).

### --dryrun flag parsing (#239)

`ldm install --dry run` (space instead of hyphen) installed a random npm package called "runjs". `ldm install --dryrun` (no hyphen) ran a full install instead of dry run.

Fix: argument normalization before flag parsing. `--dryrun`, `--dry run`, and `--dry` are all treated as `--dry-run`. The word "run" is no longer passed to the package install logic.

### Ghost directory cleanup (#240)

The ghost cleanup from #238 removed registry entries but left the actual directories on disk. Extensions with `-private` path mismatches weren't cleaned up.

Fix: ghost cleanup now also moves directories to `_trash/`. Path mismatches (registry says `wip-xai-x` but paths point to `wip-xai-x-private`) are detected and renamed.
