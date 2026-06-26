# v1.9.71-alpha.7

## wip-release: three hardening fixes for the release pipeline

Ships three related wip-release fixes in one release, each targeting a release-pipeline master-plan phase. See `ai/product/bugs/release-pipeline/2026-04-05--cc-mini--release-pipeline-master-plan.md` for the full context (7 incidents we hit today while trying to ship a single guard fix, 8 phases of forward work).

### Phase 1: refuse non-main invocations (was Incident 1)

Earlier today `wip-release alpha` ran from a feature worktree because `releasePrerelease()` had no worktree check at all (only `release()` and `releaseHotfix()` did). The result was a botched release commit on the worktree branch, never pushed to main, plus a cascade of downstream pipeline failures.

**Fix.** Extract a shared `enforceMainBranchGuard(repoPath, skipWorktreeCheck)` helper. Call it from all three release functions (`release`, `releaseHotfix`, `releasePrerelease`). The helper enforces two independent conditions:

1. **Linked worktree check.** If `git rev-parse --git-dir` resolves under `.git/worktrees/`, refuse with a ready-to-paste `cd <main-tree>` recovery command.
2. **Current branch check.** Even from the main working tree, `git branch --show-current` must be `main` or `master`. Refuse with `git checkout main && git pull && wip-release <track>` recovery command.

Both conditions bypassable via `--skip-worktree-check` for break-glass scenarios.

### Phase 2: tag collision pre-flight (was Incident 2)

Earlier today the pipeline also failed mid-release because `v1.9.71-alpha.4` and `v1.9.71-alpha.5` existed as local-only tags from prior failed releases. `wip-release alpha` tried to bump to alpha.5, hit the existing tag, and aborted. The release tool had no recovery path.

**Fix.** New `checkTagCollision(repoPath, newVersion)` helper runs after the main-branch guard, before the version bump. It distinguishes two cases:

1. **Tag exists on origin remote.** Legitimate prior release; refuses with a clear message.
2. **Tag exists locally but NOT on origin.** Stale leftover from a failed release; refuses but prints the safe recovery command: `git tag -d <tag> && wip-release <track>`.

Both cases log a clear error before any state mutation.

### Phase 8: sub-tool version drift becomes an error (was Incident 8)

Previously, if `tools/<sub-tool>/` files changed since the last git tag but `tools/<sub-tool>/package.json` version did not bump, `wip-release` printed a WARNING and proceeded. This silently shipped at least one "committed but never deployed" bug today: the guard fix had new code in `tools/wip-branch-guard/guard.mjs` but the same version, so `ldm install` ignored the sub-tool on redeploy.

**Fix.** New `validateSubToolVersions(repoPath, allowSubToolDrift)` helper replaces the three in-line duplicated drift checks in `release`, `releaseHotfix`, and `releasePrerelease`. Sub-tool drift without a version bump is now a hard refusal unless the caller passes `--allow-sub-tool-drift`.

## New CLI flags

- `--allow-sub-tool-drift` — Allow release even if a sub-tool's files changed since the last tag without a version bump. Default behavior is to refuse.

## Files changed

- `tools/wip-release/core.mjs`: new `enforceMainBranchGuard`, `logMainBranchGuardFailure`, `checkTagCollision`, `validateSubToolVersions` helpers. Inline checks in `release`, `releaseHotfix`, `releasePrerelease` replaced with calls to the helpers. `allowSubToolDrift` threaded through all three signatures.
- `tools/wip-release/cli.js`: parses `--allow-sub-tool-drift`, passes it to all three release functions. `skipWorktreeCheck` now also passed to `releasePrerelease` (was missing). Help text updated.
- `tools/wip-release/package.json`: version bump to 1.9.72.
- `CHANGELOG.md`: entry added.

## Verified

- From a feature worktree: `wip-release alpha --dry-run` refuses with concrete `cd <main-tree>` recovery command. Same for `patch` and `hotfix`.
- `--skip-worktree-check` bypass works.
- Module imports cleanly via `node -e "import('./tools/wip-release/core.mjs')"`.

## Known limitation (follow-up)

The tag collision and sub-tool drift checks run in live release mode, not in dry-run preview. Dry-run still shows "would bump" for a version that would actually fail later. Follow-up: move both checks before the dry-run short-circuit so preview is a faithful preflight. Tracked in the release-pipeline master plan as a small cleanup.

## Cross-references

- `ai/product/bugs/release-pipeline/2026-04-05--cc-mini--release-pipeline-master-plan.md` Phases 1, 2, 8
- `ai/product/bugs/guard/2026-04-05--cc-mini--guard-master-plan.md` Phases 3, 4 (partial, not all covered here; auto-publish sub-tool remains deferred to a follow-up PR)
- `ai/product/bugs/master-plans/bugs-plan-04-05-2026-002.md` Wave 2 phases 4, 5, 11
