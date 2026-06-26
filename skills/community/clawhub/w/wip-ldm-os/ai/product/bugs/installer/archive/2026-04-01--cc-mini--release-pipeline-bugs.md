# Bugs: Release Pipeline v2

**Date:** 2026-04-01
**Filed by:** cc-mini
**Related:** #239 (release pipeline v2)

## Bug 1: Version comparison thinks alpha is a downgrade

**Severity:** Medium
**Where:** `bin/ldm.js` (self-update check and status display)

After installing `v0.4.73-alpha.1`, the installer shows:
```
CLI is outdated: v0.4.73-alpha.1 installed, v0.4.72 available.
Run: npm install -g @wipcomputer/wip-ldm-os@0.4.72
```

It's suggesting a DOWNGRADE from alpha to stable. The semver comparison doesn't understand that `0.4.73-alpha.1` is newer than `0.4.72`.

**Fix:** Use proper semver comparison. `0.4.73-alpha.1` > `0.4.72` in semver. The comparison likely uses string comparison or only compares the base version without the prerelease suffix. Use a semver library or implement proper prerelease-aware comparison.

**Files:** `bin/ldm.js` (search for version comparison, `npm view`, `cmdStatus`)

## Bug 2: Release cooldown blocks alpha/beta installs

**Severity:** Low
**Where:** `wip-branch-guard/guard.mjs` (lines 322-334)

The guard blocks `npm install -g` within 5 minutes of any release. This makes sense for stable releases (don't immediately install what you just published). But it also blocks alpha and beta installs, which is the whole point of the prerelease workflow. You release alpha, then immediately want to install it to test.

**Fix:** Check if the install command targets a prerelease tag (`@alpha`, `@beta`). If so, skip the cooldown. The cooldown only applies to `@latest` installs after a stable release.

**Files:** `wip-branch-guard/guard.mjs` (the `npm install -g` cooldown section)

## Bug 3: Sub-tool npm packages don't update with parent toolbox

**Severity:** Low (workaround exists)
**Where:** Toolbox release pipeline

When `wip-release patch` runs on the toolbox, it publishes the parent package (`@wipcomputer/wip-ai-devops-toolbox@1.9.68`) to npm. But individual sub-tool packages (`@wipcomputer/wip-release`, `@wipcomputer/wip-repos`, etc.) are published by `deploy-public` from the public repo. Without `deploy-public`, the sub-tools stay at the old version.

This means `wip-release --version` shows `1.9.67` even though the toolbox is at `1.9.68`. The installed CLI is the sub-tool package, not the parent.

**Fix options:**
1. `wip-release` publishes sub-tool packages to npm directly (not just the parent)
2. The installer installs sub-tools from the parent package instead of individual packages
3. Accept this as expected: sub-tools update on `deploy-public` (stable releases)

Option 3 is probably fine. Alpha/beta tracks don't need sub-tool CLI updates. The repo version works. Only stable releases need the CLIs updated.

**Workaround:** Run `wip-release` from the repo (`node tools/wip-release/cli.js`) instead of the installed CLI. This uses the latest code without needing a sub-tool npm update.
