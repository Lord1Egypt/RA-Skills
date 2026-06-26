# Release Pipeline Master Plan. April 5 Status.

**Date:** 2026-04-05
**Filed by:** cc-mini (with Parker, Lēsa)
**Repo:** wip-ai-devops-toolbox-private (pipeline source), wip-ldm-os-private (filing location)
**Priority:** critical
**Status:** consolidation. Zero fixes shipped. All phases are follow-up work.

## Superseded / Consolidated By

This plan is consolidated into `ai/product/bugs/release-pipeline/2026-04-24--codex--canary-release-pipeline-master-plan.md`.

Keep this file for historical context and incident detail. Use the 2026-04-24 canary release pipeline master plan as the current implementation map.

## Cross-references

**This plan is tied to:**
- `ai/product/bugs/guard/2026-04-05--cc-mini--guard-master-plan.md` — the guard-side bugs. Phases 3, 4, 5, 8 of the guard master plan ARE this plan's phases. They are pipeline problems, not guard problems, so they live here. The guard plan covers the guard-specific fixes (Phases 1, 2, 6, 7).
- `ai/product/bugs/bridge/2026-04-05--cc-mini--bridge-master-plan.md` — section 5.5 "Pipeline flow-through gaps" flagged these same issues two days ago. Still unfixed.
- `ai/product/bugs/release-pipeline/archive/2026-03-27--cc-mini--version-mismatch-deploy-gap.md` — prior instance of deploy-gap bug.
- `ai/product/bugs/release-pipeline/archive/2026-03-31--cc-mini--installer-dependency-resolution.md` — related install-side bug.
- `ai/product/bugs/release-pipeline/archive/2026-03-31--cc-mini--installer-deploy-order.md` — related install-side bug.

## Context

The `wip-release` tool runs the release pipeline for the WIP DevOps Toolbox and its sub-tools. Every time we ship a guard fix, a release pipeline bug makes it 5x harder than it should be. Today's session hit at least four of them in sequence and burned approximately $900 of Opus tokens on what should have been a 30-second task.

This plan enumerates the pipeline bugs, their blast radius, and the forward plan to fix each. It is the pipeline-side companion to the guard master plan. Shipping the guard fix today required manually working around every one of the bugs listed here.

## Today's release pipeline incidents (in order)

### Incident 1. wip-release ran on a worktree branch instead of main

**What happened.** I invoked `wip-release alpha` from inside `.worktrees/wip-ai-devops-toolbox-private--cc-mini--guard-stash-allow/`. The tool did not check which branch it was on. It bumped the root `package.json` version, updated CHANGELOG.md, created a release commit on the worktree branch (not main), tagged it, and attempted to push. The tag step failed because a prior local-only tag already claimed the version number.

**Root cause.** `wip-release` does not validate that it is running on main/master. It runs wherever it is invoked.

**Blast radius.** Creates orphan commits on feature branches that look like release commits but never land on main. Confuses git history. Tag numbers get used up on commits that are never pushed. Next release invocation sees the stale tags and fails.

**Workaround today.** I had to:
1. Abort the merge
2. Delete the orphan worktree
3. Clean up the stale local tags
4. Re-run wip-release from main

### Incident 2. Stale local tags from prior failed releases

**What happened.** `v1.9.71-alpha.4` and `v1.9.71-alpha.5` existed as local tags in the wip-ai-devops-toolbox-private repo but had never been pushed to remote. `wip-release alpha` tries to bump `1.9.71-alpha.4 -> 1.9.71-alpha.5`, hits the existing tag, and fails.

**Root cause.** Prior failed release attempts left local tags behind. `wip-release` does not clean up its own turds. There is no "resume from failed release" flow and no validation that the target version's tag does not already exist locally.

**Blast radius.** Once the failure happens, the pipeline is stuck. You cannot retry without either deleting the stale tags (which feels destructive) or bumping to a higher version (which skips version numbers and confuses users).

**Workaround today.** `git tag -d v1.9.71-alpha.4 v1.9.71-alpha.5` manually, then retry.

### Incident 3. Release commit that conflicts with already-published npm version

**What happened.** Local main in wip-ai-devops-toolbox-private was carrying an unpushed commit `98f45f2 v1.9.71-alpha.5: alpha prerelease`. This commit was created by a prior `wip-release alpha` attempt whose git push was never run. The version it bumps to (`1.9.71-alpha.5`) was, however, SUCCESSFULLY published to npm by that prior attempt. When I ran wip-release today, it tried to publish alpha.5 again and npm rejected with E403 "cannot publish over previously published versions."

**Root cause.** `wip-release` commits the version bump BEFORE publishing to npm. If the publish succeeds but the push fails, local git state records a version number that is already live on npm. Next invocation will collide.

**Blast radius.** Permanent state divergence between local git, remote git, and npm. The "what is the actual current version" question has three different answers.

**Workaround today.** I had to force-move local main back to `origin/main` (non-destructively, via `git checkout origin/main && git branch -f main origin/main && git checkout main`), then re-run wip-release which correctly bumped past alpha.5 to alpha.6.

### Incident 4. Cannot push release commits directly to protected main

**What happened.** `wip-release` bumped the root version, committed, tagged, and npm-published. Then `git push origin main` was rejected by GitHub: "Protected branch update failed. Changes must be made through a pull request."

**Root cause.** `wip-release` assumes it can push directly to main. Main is protected on GitHub (as it should be). The tool was not designed for protected-main workflows.

**Blast radius.** The release commit sits on local main, unpushed. The tag sits on local, unpushed. npm is ahead of git. The human has to manually create a PR, push a branch, merge it, and push tags separately.

**Workaround today.** I created `cc-mini/release-alpha-6` from the current local main tip, pushed the branch, opened PR #318, merged it, then pushed tags separately with `git push origin v1.9.71-alpha.5 v1.9.71-alpha.6`.

### Incident 5. Sub-tool npm packages are not auto-published

**What happened.** I bumped `tools/wip-branch-guard/package.json` from `1.9.71` to `1.9.72` as part of the guard fix. `wip-release alpha` published the root package (`@wipcomputer/wip-ai-devops-toolbox@1.9.71-alpha.6`) but did NOT publish the sub-tool (`@wipcomputer/wip-branch-guard@1.9.72`). I had to manually `npm publish` from the sub-tool directory, which required manually extracting the npm token from 1Password.

**Root cause.** `wip-release` only publishes the root repo. Sub-tools with their own `package.json` and npm package identity are ignored. This is flagged as a warning (not an error) when sub-tool files change without a root version bump.

**Blast radius.** Every guard fix, every branch-guard version bump, requires a manual extra step. Miss it and the npm package stays at the old version. `ldm install` pulls from npm by name, so forgotten sub-tool publishes cause guard regressions on next install.

**Workaround today.** Manual `npm publish --access public --//registry.npmjs.org/:_authToken=$(op item get ...)` from inside `tools/wip-branch-guard/`.

### Incident 6. deploy-public.sh requires explicit args and is a separate manual step

**What happened.** After `wip-release alpha` published to npm, I still had to manually run `bash tools/deploy-public/deploy-public.sh <private-repo-path> <public-github-repo>` to sync the public mirror. The script requires both paths as positional args. It is not integrated into the `wip-release` pipeline for alpha releases.

**Root cause.** `deploy-public.sh` is designed as a standalone script invoked manually. `wip-release` only calls it for stable (patch/minor/major) releases, not alpha/beta.

**Blast radius.** Without the public deploy, `ldm install` (which clones from the public repo) gets stale code even though npm has the new package. Asymmetric deploy state. Flagged in the bridge master plan two days ago. Still not fixed.

**Workaround today.** Manual script invocation with explicit args.

### Incident 7. deploy-public.sh's sub-tool npm publishes all failed silently

**What happened.** `deploy-public.sh` attempted to publish 13 sub-tool packages to npm at the end of its run. Every single one failed with "non-fatal" errors. The specific failure mode was not surfaced in the output. Some of these may be redundant with my manual wip-branch-guard publish; others were legitimate attempts to republish packages that already had current versions.

**Root cause.** Unclear. Possibly auth failure (the script tries to publish without the token argument that wip-release passes), possibly version conflicts, possibly unchanged packages that don't need republishing. The script swallows the error details.

**Blast radius.** Every deploy-public run produces 10+ "non-fatal" failures in the output. Noise fatigue. Real failures get lost. Debugging is hard because the specific error is hidden.

**Workaround today.** None. I ignored them because the critical sub-tool (wip-branch-guard) was already published manually.

### Incident 8. Sub-tool version drift warnings, not errors

**What happened.** If I had forgotten to bump `tools/wip-branch-guard/package.json` when I changed guard.mjs, `wip-release` would have emitted a WARNING and proceeded. The new guard code would have been committed and merged, but never picked up by `ldm install` because the sub-tool version would still be 1.9.71. The guard fix would be in git but not in npm.

**Root cause.** `wip-release` treats sub-tool version bumps as advisory, not mandatory.

**Blast radius.** Silent "committed but never deployed" class of bugs. The repo looks updated, the git log shows the fix, but users installing from npm get the old version forever.

**Not hit today** (I remembered to bump), but this is the trap I would fall into on any future guard fix if I forget.

## What we lost today

- **Approximately $900 of Opus tokens** on the guard loop + pipeline workaround chain
- **About 60 minutes of Parker's wall time**
- **Trust between Parker and the agent** (harder to measure, but real)
- **Context** (we spent the whole session in workaround-land instead of on actual product work)

These are not theoretical costs. They are direct damages from the release pipeline state.

## The plan forward (phased)

### Phase 1. wip-release refuses non-main invocations (Incident 1)

- **File:** `tools/wip-release/core.mjs` or equivalent entry point in `wip-ai-devops-toolbox-private`
- **Change:** at the start of the release pipeline, check `git branch --show-current`. If not `main` or `master`, refuse with a clear error pointing at the correct workflow: `git checkout main && git pull && wip-release`.
- **Size:** approximately 10-15 lines plus a test case
- **Risk:** low. There is a `--skip-worktree-check` flag already so the validation can use the same code path.
- **Verification:** run `wip-release alpha` from a worktree. Expect: hard error with clear message. Run from main. Expect: normal pipeline.

### Phase 2. wip-release cleans up its own stale tags on failure (Incident 2)

- **File:** `tools/wip-release/core.mjs` bump+tag section
- **Change:** before attempting to tag, check if the target tag already exists locally. If yes, check if it is on any remote branch. If not, delete the stale local tag (after confirming with the user or via a `--reuse-stale-tags` flag). If yes, refuse with a clear error explaining the collision.
- **Alternative:** on any failure mid-pipeline, roll back tags and commits that were created in this run. Requires a "checkpoint" at the start of each release.
- **Size:** medium, 50-100 lines plus tests
- **Risk:** medium. Tag cleanup is destructive to tag refs. Must be safe against deleting tags that belong to pushed releases.

### Phase 3. wip-release publishes to npm BEFORE committing the bump (Incident 3)

- **Current order:** bump -> commit -> tag -> push -> npm publish
- **Proposed order:** bump -> npm publish -> (on success) commit -> tag -> push
- **Why:** if npm publish fails, git state is still clean. No orphan commits. If the push fails after successful publish, the commit can be recreated from a branch without the bump being wasted.
- **Alternative:** keep current order but add rollback-on-publish-failure that discards the uncommitted bump.
- **File:** `tools/wip-release/core.mjs`
- **Size:** medium, 30-50 lines
- **Risk:** the "publish before commit" model changes the tool's semantics. Need to think through what happens if the publish succeeds but the tool crashes before committing.

### Phase 4. wip-release handles protected main via automatic PR flow (Incident 4)

- **Change:** if `git push origin main` fails with "protected branch", automatically create a branch with the release commit, push it, open a PR, and merge it (using the same `gh pr create` + `gh pr merge --merge --delete-branch` pattern that worked today).
- **File:** `tools/wip-release/core.mjs` push section
- **Size:** medium, 50 lines plus tests. The PR title and body should reference the version, changelog entry, and release notes.
- **Risk:** medium. PR-merged release commits have a merge commit in history instead of a clean linear commit. Historians might prefer the linear style. Parker's call.

### Phase 5. wip-release auto-publishes changed sub-tool npm packages (Incident 5)

- **Change:** during the release pipeline, scan `tools/*/package.json` for sub-tools whose source files (tracked by git) have changed since the last release tag. For each changed sub-tool:
  1. Verify its `package.json` version was bumped in this release commit (otherwise error out — see Phase 8)
  2. Run `npm publish` for that sub-tool directory with the same auth token used for the root publish
  3. Include the sub-tool publish result in the pipeline summary
- **File:** `tools/wip-release/core.mjs` npm publish section
- **Size:** medium-large, 100-150 lines plus tests. Needs to iterate over sub-tools, diff against last release, handle publish failures independently.
- **Risk:** medium. Sub-tools can have their own tag conventions. Not all sub-tools are npm packages. Need an allowlist or package.json introspection.

### Phase 6. wip-release runs deploy-public.sh for alpha/beta releases (Incident 6)

- **Change:** extend wip-release to call `deploy-public.sh` at the end of the alpha/beta flows. Use a `--no-deploy-public` flag to opt out.
- **File:** `tools/wip-release/core.mjs` final step
- **Size:** small, 20-30 lines plus tests
- **Risk:** low. deploy-public is idempotent (it creates a PR and merges it).

### Phase 7. deploy-public.sh surfaces real errors on sub-tool npm publish failures (Incident 7)

- **Change:** when sub-tool npm publish fails inside deploy-public.sh, capture the actual error message and print it with the package name. Do not swallow with "non-fatal." Either: (a) make the failures genuinely non-fatal but loud, or (b) make them fatal and stop the pipeline.
- **File:** `tools/deploy-public/deploy-public.sh` npm publish loop
- **Size:** small, 20 lines
- **Risk:** low.

### Phase 8. Sub-tool version bumps are ERRORS, not warnings (Incident 8)

- **Change:** when wip-release detects that a sub-tool's source files changed but its `package.json` version did not bump, emit an ERROR and abort. Not a warning.
- **File:** `tools/wip-release/core.mjs` sub-tool validation section
- **Size:** trivial. Change WARN to ERROR, add a `--allow-sub-tool-drift` opt-out flag.
- **Risk:** low, but will surface forgotten bumps that currently ship silently.

## Files that matter

- `repos/ldm-os/devops/wip-ai-devops-toolbox-private/tools/wip-release/core.mjs` (main pipeline)
- `repos/ldm-os/devops/wip-ai-devops-toolbox-private/tools/wip-release/cli.js` (CLI entry)
- `repos/ldm-os/devops/wip-ai-devops-toolbox-private/tools/deploy-public/deploy-public.sh` (public sync script)
- `repos/ldm-os/devops/wip-ai-devops-toolbox-private/tools/wip-release/package.json` (sub-tool version)
- Related guard code: `repos/ldm-os/devops/wip-ai-devops-toolbox-private/tools/wip-branch-guard/guard.mjs` (for coordinated protections)

## Related tickets and commits

- wipcomputer/wip-ai-devops-toolbox-private#317 merged today (guard fix, hit Phases 1-5 of this plan during deploy)
- wipcomputer/wip-ai-devops-toolbox-private#318 merged today (release commit bundled as PR due to Incident 4)
- wipcomputer/wip-ai-devops-toolbox#245 (public mirror PR from deploy-public.sh)
- Archived release-pipeline bugs under `ai/product/bugs/release-pipeline/archive/`
- Bridge master plan section 5.5 (prior flagging of same issues)

## Sibling plan

All of this is tied to the guard master plan at `ai/product/bugs/guard/2026-04-05--cc-mini--guard-master-plan.md`. That plan has its own 8 phases covering the guard-specific work. Phases 3, 4, 5, 8 of the guard plan are the SAME as Phases 1, 5, 6, 8 of this plan (same underlying incidents, filed under different folders for discoverability). When tackling any phase, check both plans so you do not ship a half-fix that resolves one symptom but leaves the other side open.

The split is deliberate. Someone searching `ai/product/bugs/guard/` for guard issues should find the guard plan with its 8 phases, some of which point at the release pipeline for the deeper fix. Someone searching `ai/product/bugs/release-pipeline/` for pipeline issues should find this plan with its 8 phases covering every incident we hit today.

## Open questions for Parker

- Should Phase 3 (publish before commit) be the new default, or opt-in? Changing the order changes the mental model of the release pipeline.
- Should Phase 4 (PR-flow for protected main) use merge commits or squash merges for releases? Current convention is `--merge` (no squash), but a release commit as a merge commit adds a layer.
- For Phase 5 (sub-tool auto-publish), which sub-tools are IN scope? The toolbox has ~13 sub-tools. All of them? Or an allowlist?
- Is there appetite for a bigger refactor of `wip-release` into a proper state machine with resumable steps? Half of today's incidents come from the tool not recovering gracefully from mid-pipeline failures. Opinionated answer: yes, but scope it as Phase 9 after the targeted fixes land.

## Verification end-to-end

After all 8 phases ship:

1. Running `wip-release alpha` from a worktree refuses with clear error (Phase 1)
2. Running `wip-release alpha` from main after a prior failed release cleans up stale tags and proceeds (Phase 2)
3. An npm publish collision is handled gracefully: git state reverts, user sees a clear error, next invocation bumps past the collision (Phase 3)
4. `wip-release alpha` from main pushes the release via automatic PR flow when main is protected (Phase 4)
5. A guard sub-tool change triggers auto-publish of `@wipcomputer/wip-branch-guard` at the new version during the main release (Phase 5)
6. `wip-release alpha` runs `deploy-public.sh` as its final step without a manual second command (Phase 6)
7. Any sub-tool npm publish failure surfaces a real error message, not "non-fatal" (Phase 7)
8. A sub-tool source change without a version bump causes `wip-release` to abort with a clear error (Phase 8)
9. End-to-end: a full guard fix ships via one `wip-release alpha` command, with no manual steps, no stale-tag loops, no E403 npm errors, no protected-branch pushes, no manual deploy-public invocation. Estimated time: under 60 seconds. Today it took 60 minutes.

## Notes and constraints

- Each phase gets its own PR. Do not bundle them.
- Every PR respects the worktree -> branch -> commit -> push -> PR -> merge -> wip-release flow
- Every PR includes test coverage in `tools/wip-release/test.sh` (or equivalent)
- Every PR updates CHANGELOG.md with a clear entry
- All three contributors on every commit
- No em dashes

## Session cost reference

- Today: 60 minutes of wall time, approximately $900 of Opus tokens (across all incidents)
- Prior sessions with similar pipeline symptoms: unknown cumulative cost, but the bridge master plan notes a $40 overnight loop from a different incident in the same cluster
- Estimated time savings after all 8 phases ship: approximately 30-55 minutes per release, approximately $700-850 per incident avoided
- ROI: ships in under a day of focused work. Recovers cost in one release cycle.
