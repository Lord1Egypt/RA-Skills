---
title: "ldm install --alpha resolves npm's stale alpha over a newer locally tagged release"
status: open
priority: P1
owner: unassigned
reviewer: Installer CC Partner
repo: wip-ldm-os-private
created: 2026-07-05
---

## What happened

2026-07-04: three repos were released with `wip-release alpha --no-publish` (version bump + git tag, npm publish deferred because the npm token had expired). Local repos sat at tagged v0.4.85-alpha.31 / v0.7.39-alpha.1 / v1.9.73-alpha.13. `ldm install --alpha` then resolved every package from npm's @alpha dist-tags, which still pointed at the previous alphas, and reported "already at" / updated nothing to the new versions. The documented source-resolution order (npm, then local private repo, then GitHub) only falls through when npm is UNREACHABLE, not when npm's answer is OLDER than a locally available release.

## Why it matters

- how-releases-work.md sells the local private repo as the offline/developer source, but in practice it is dead code whenever npm answers at all.
- The developer loop "tag locally, validate via ldm install --alpha, publish when satisfied" is impossible; validation requires publishing first, which inverts the safety ordering.
- It took the 2026-07-04 outage to notice: with npm auth broken, the fixes were tagged and sitting on disk with no sanctioned way to install them.

## Fix

1. Source resolution compares VERSIONS across sources, not just availability: for each source in order, collect the best candidate version; pick the highest (respecting the track), not the first responder.
2. On the alpha/beta tracks, a local private repo whose tagged version is newer than npm's dist-tag wins, with the install summary naming the source: "installed from local repo (vX, npm @alpha has vY)".
3. Stable track keeps npm-first strictness if desired (Parker's call); prerelease tracks are explicitly the developer loop.
4. Regression test: fixture registry entry with npm @alpha at vN and local repo tagged vN+1; assert --alpha installs vN+1 from local and says so.

## Related

- `2026-07-05--cc-mini--installer-path-install-downgrades-cli.md` (sibling: explicit-path resolution also wrong)
- `2026-05-13--cc-mini--installer-registry-source-types-architecture.md` (Phase 2 source-type dispatch is the natural home for the comparison)
