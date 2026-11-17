---
title: "ldm install <path> downgrades the ldm CLI to an older registry version while acknowledging the repo is newer"
status: open
priority: P1
owner: unassigned
reviewer: Installer CC Partner
repo: wip-ldm-os-private
created: 2026-07-05
---

## What happened

2026-07-04, on the origin machine, with the ldm CLI at 0.4.85-alpha.30 and the local repo tagged v0.4.85-alpha.31 (unpublished on npm at the time):

`ldm install /Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private` printed:

```
+ CLI: ldm, wip-ldm-os, wip-install, ldm-scaffold, ldm-boot-install, lesa installed from registry (v0.4.84, repo has v0.4.85-alpha.31)
```

It DOWNGRADED the live CLI from alpha.30 to 0.4.84 (a stable older than the running prerelease), sourced "from registry," while explicitly printing that the repo in hand was newer. The downgraded CLI then ran with pre-fix hook-registration code and appended a duplicate SessionStart boot-hook entry (the exact bug alpha.31 fixed), compounding the machine state the newer version would have repaired.

## Why it matters

- Version immutability/monotonicity: an install action must never silently move a tool BACKWARD, least of all the installer itself.
- A local-path install is the developer's explicit "use THIS code" instruction; resolving the CLI from the registry instead inverts the user's intent.
- The downgrade is self-amplifying: older installer code reintroduces bugs the newer code fixes, during the very install meant to deliver the fix.

## Fix

1. In the target-self-update path for `ldm install <path>`: when the path's package version is newer than (or equal to) both the installed CLI and the registry candidate, deploy the CLI from the path. Never select a candidate older than the currently installed version without an explicit `--allow-downgrade` flag.
2. Guard rail regardless of source: any CLI deploy that would lower the semver of the running `ldm` prints a loud DOWNGRADE warning and requires the flag.
3. Regression test: fixture with installed prerelease X, registry stable < X, local path > X; assert path wins and no downgrade occurs; assert `--allow-downgrade` is required to go backward.

## Related

- `2026-05-11--codex--targeted-install-skips-ldm-self-update.md` (the self-update preflight this path runs through)
- `2026-07-05--cc-mini--installer-alpha-prefers-stale-npm-over-local-tag.md` (sibling source-resolution bug, same night)
