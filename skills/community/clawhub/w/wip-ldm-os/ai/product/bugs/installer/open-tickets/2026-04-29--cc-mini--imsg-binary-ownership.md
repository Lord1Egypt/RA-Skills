---
title: imsg binary at ~/.ldm/bin/imsg has no declared owner
date: 2026-04-29
status: open (parked follow-up from 2026-04-28 thread)
severity: P3
component: ldm-installer
parent-ticket: archive/2026-04-28--cc-mini--ldm-bin-overwrite-wipes-crystal-capture.md
parent-design: ../../plans-prds/archive/2026-04-28--cc-mini--ldm-bin-ownership-manifest-design.md
---

# `imsg` binary ownership

## Context

After the bin ownership manifest landed (#718), every file in `~/.ldm/bin/` is supposed to resolve to a declarer:

- `crystal-capture.sh` → `memory-crystal` (declared in `memory-crystal-private:openclaw.plugin.json#binFiles`)
- `process-monitor.sh`, `ldm-backup.sh`, `ldm-restore.sh`, `ldm-summary.sh`, `backfill-summaries.sh` → `wip-ldm-os` (declared in `wip-ldm-os-private:package.json#wipLdmOs.binFiles`)

There is one more file with no declarer:

```
-rwxr-xr-x   1 lesa  staff  5163600 Apr 19 09:37 /Users/lesa/.ldm/bin/imsg
```

`imsg` is a 5MB compiled binary, not a shell script. It was deployed once on 2026-04-19 and no part of `ldm install` re-deploys it today. `ldm doctor` reports it as a known foreigner (no cron line references it, so the cron-target check doesn't surface it; the manifest just has no entry).

## What needs to happen

Identify which package owns `imsg`, declare it in that package's `binFiles`, and decide whether the file should be tracked under the manifest's auto-restore semantics.

Open questions for the resolution:

1. **Which package owns it?** Likely candidates: `wip-ldm-os` itself (a CLI helper), an iMessage-related extension, or a one-off install that pre-dates the manifest convention.
2. **Should the manifest cover binaries, not just scripts?** The current schema's `executable: true` and source-from-package model fits scripts cleanly. A 5MB binary shipped via npm is heavier than the rest of the manifest assumes. May want a separate `binBinaries` array or accept that the schema covers both.
3. **What's the canonical source?** A binary's `source` would have to be inside the published artifact. Confirm the owner package actually carries it before declaring.

## Acceptance criteria

- [ ] Owner identified and confirmed (`git log` on the install path that originally placed it; `npm pack` of the candidate to check `files` array).
- [ ] Either: declared in that package's manifest with full source path, OR: explicitly marked as out-of-manifest with a comment in the parent design doc.
- [ ] `ldm doctor` no longer reports `imsg` as unknown-owner foreigner.

## Why P3

`imsg` has not gone missing or caused a regression. It's a hygiene gap, not a failure mode. Fix when you (a) touch iMessage tooling or (b) the manifest needs to expand its schema for binaries.
