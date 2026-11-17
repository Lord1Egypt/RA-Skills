---
title: "~/.ldm repo tracks installer churn: 10K dirty files after one install day; needs a tracking strategy"
status: open
priority: P1
owner: unassigned
reviewer: OS-Level CC Partner
repo: wip-ldm-os-private (fix lands in the dot-ldm repo's .gitignore + ldm install)
created: 2026-07-05
---

## What happened

The 2026-07-05 audit of the tracked `~/.ldm` repo found 3,551 deletions, 7,007 untracked files, and 29 modifications after one day of alpha installs. The installer replaces whole `extensions/<name>/` trees (including `node_modules`), rotates old versions into `_trash/YYYY-MM-DD/`, and rewrites state files; the repo tracks all of it, so every install produces thousands-file drift that nobody can review or sensibly commit.

Consequences: `git status` in `~/.ldm` is useless as a change signal, the safety value of tracking (git as the safety net for config) is drowned in deploy noise, and any future "commit the drift" action risks snapshotting gigabytes of node_modules.

## Fix

1. Decide the tracking contract for `~/.ldm`: git tracks CONFIG and IDENTITY (config.json, agents/*/ SOUL/IDENTITY/CONTEXT/settings, library/ docs and rules, boot config), not DEPLOY ARTIFACTS (extensions/ internals, _trash/, logs/, state/, memory/ sqlite, bin/ shims).
2. Write the .gitignore accordingly; `git rm -r --cached` the newly ignored trees in one reviewed commit (contents stay on disk).
3. `ldm install` gains a post-deploy note when it mutates tracked paths, so intentional tracked changes (rules, boot config) surface for commit while artifact churn stays invisible.
4. Backup coverage check: whatever git stops tracking must be covered by ldm-backup.sh (extensions are reproducible from npm/repos; memory/ sqlite is already backup-owned; verify and document in how-backup-works.md).

## Acceptance

- Fresh `ldm install --alpha` run leaves `git status` in ~/.ldm showing ONLY intentionally tracked changes (ideally zero or a handful of lines).
- The one-time untracking commit is reviewed, with a manifest of what left tracking and where its safety now lives.
- how-backup-works.md and system-directories.md updated.

## Related

- `2026-04-14--cc-mini--library-migration-plus-topology.md` (same repo, same "what lives where" question; do these together)
- `ai/product/bugs/installer/open-tickets/2026-07-05--cc-mini--shared-library-split-brain-boot-deploy.md` (the migration that ticket needs would be a tracked-path change this contract must handle)
