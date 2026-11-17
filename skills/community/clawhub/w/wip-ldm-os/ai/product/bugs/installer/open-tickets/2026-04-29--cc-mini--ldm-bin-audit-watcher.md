---
title: Audit watcher for writes/deletes to ~/.ldm/bin/ (forensic capture)
date: 2026-04-29
status: open (parked future-forensics ticket from 2026-04-28 thread)
severity: P3
component: ldm-installer
parent-ticket: archive/2026-04-28--cc-mini--ldm-bin-overwrite-wipes-crystal-capture.md
---

# Audit watcher for `~/.ldm/bin/`

## Context

The 2026-04-28 capture-shim outage left a forensic gap that we couldn't close after the fact: `~/.ldm/bin/crystal-capture.sh` disappeared, but neither the LDM CLI's `deployScripts()` nor the OpenClaw upgrade procedure (`open-claw-upgrade-private`) actually touches `~/.ldm/bin/` per their respective code. Both code paths read clean. So the original "LDM install wiped the file" framing is not supported by either codebase.

That means whatever delete vector ran on Apr 28 is unidentified and probably unknowable now. There's no audit log of writes to `~/.ldm/bin/`, no mtime history per file, no record of which process touched what. Future similar incidents will hit the same wall.

This is a future-proofing ticket: add a lightweight audit watcher so the next time something in `~/.ldm/bin/` changes, we know who did it.

## What needs to exist

A small daemon that watches `~/.ldm/bin/` for filesystem events (create, delete, modify, chmod) and records each event to an append-only log with:

- Timestamp (ISO 8601, milliseconds)
- Event type (`create | delete | modify | chmod`)
- Path
- Optionally: `lsof`-style attribution of which pid had the file open at event time, plus the pid's command line

Log location: `~/.ldm/logs/bin-audit.log`. Rotated weekly, kept 30 days. Compressed.

Implementation candidates (rough order of preference):

1. **macOS `fs_usage`** as a LaunchAgent. Filters output to writes/deletes under `~/.ldm/bin/`. Simplest. Already root-tier visibility on macOS.
2. **Node + `chokidar` + `lsof` shell-out.** Cross-platform. Higher complexity. Misses pid attribution when the writer exits before we look.
3. **`fswatch` + a small bash wrapper.** Middle ground.

Recommendation: option 1 for the Mac mini. Trade off cross-platform later if needed.

## Acceptance criteria

- [ ] LaunchAgent (or equivalent) emits one log line per filesystem event under `~/.ldm/bin/`.
- [ ] Each log line carries a timestamp, event type, path, and (best-effort) writer pid + command line.
- [ ] `ldm doctor` surfaces the watcher health (running / not running / log size).
- [ ] Log rotation prevents unbounded growth.
- [ ] Optional: integration with the bin manifest (`lib/bin-manifest.mjs`) so events tagged "expected manifest write" don't pollute the audit signal.

## Why P3

The 2026-04-28 outage is closed. The failure class is self-healing now (PR #718, #124, #127). This watcher gives us the missing evidence next time something similar happens. It's prevention against future ambiguity, not against current breakage.

Worth doing before the next major LDM install / upgrade cycle. After that, it's "good to have" rather than "would have helped."
