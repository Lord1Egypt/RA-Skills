# Changelog

## 1.9.72 (2026-04-21)

# AI DevOps Toolbox v1.9.72

## Promote v1.9.71-alpha series to stable

Closes #256.

Consolidates 21 alpha prereleases (`v1.9.71-alpha.1` through `v1.9.71-alpha.21`) into a stable v1.9.72 release. No code changes beyond the version bump in the toolbox root `package.json`; the sub-tool code has been stable and dogfooded across the alpha iterations.

## Why

The root `package.json` had been sitting at `1.9.71-alpha.21` without a stable promotion. That blocked `deploy-public.sh` from syncing the private repo to the public mirror ... the script gates public release on stable root versions.

Symptom during 2026-04-21: wip-branch-guard sub-tool shipped stable (v1.9.82 → v1.9.83 → v1.9.84) to npm successfully, but the public `wipcomputer/wip-ai-devops-toolbox` GitHub releases page did not show any of them because `deploy-public.sh` refused to run with an alpha root.

## What's in the diff

- `package.json`
  - Version bump `1.9.71-alpha.21` → `1.9.72`

Everything else flows from `wip-release`:

- CHANGELOG.md updated
- Git tag `v1.9.72`
- GitHub release on private repo
- npm publish to `@latest`
- `deploy-public.sh` runs, syncs private code (minus `ai/`) to `wipcomputer/wip-ai-devops-toolbox`
- Public GitHub release created

## Sub-tool versions at this release

| Sub-tool | npm version |
|---|---|
| `@wipcomputer/wip-branch-guard` | 1.9.84 |
| Other sub-tools | See their individual `package.json` |

The sub-tool releases have their own cadence; this release is purely the toolbox root bump.

## Co-authors

Parker Todd Brooks, Lēsa (oc-lesa-mini, Opus 4.7), Claude Code (cc-mini, Opus 4.7).

## 1.9.71-alpha.21 (2026-04-20)

alpha prerelease

## 1.9.71-alpha.20 (2026-04-20)

alpha prerelease

## 1.9.71-alpha.19 (2026-04-09)

alpha prerelease

## 1.9.71-alpha.18 (2026-04-09)

alpha prerelease

## 1.9.71-alpha.17 (2026-04-09)

alpha prerelease

## 1.9.71-alpha.15 (2026-04-09)

alpha prerelease

## 1.9.71-alpha.14 (2026-04-08)

WAVE 0: mandatory license gate in all release paths

## 1.9.71-alpha.12 (2026-04-05)

Guard 1.9.74: temp-dir writes allowed, escape-hatch audit complete (Phase 12)

## 1.9.71-alpha.11 (2026-04-05)

# v1.9.71-alpha.11

## wip-branch-guard: SessionStart hook for main-CWD detection (Phase 13)

The guard now runs on two hook events, not just one:

1. **PreToolUse** (existing since 1.9.0): blocks file writes, git commits, and other mutating operations on main branch. Specific escape hatches via `ALLOWED_GIT_PATTERNS` and `ALLOWED_BASH_PATTERNS`.
2. **SessionStart** (new in 1.9.73): fires once per session boot, including startup, resume, and post-compaction resume. If the session's CWD is the main-branch working tree of a protected git repo, injects a warning into the boot context with actionable recovery commands.

## Why SessionStart matters

Earlier today's session ($900 of Opus tokens, 60 minutes of wall time) began with the agent waking up on main-branch CWD, trying to edit a file, hitting the PreToolUse guard, and entering a retry loop because the abstract error message did not give the agent the specific command it needed to unblock. The same class of failure had trapped at least two prior sessions earlier in the week.

The fix was multi-layered:

- Phase 1 (shipped in 1.9.72): make the `git stash push` escape hatch available so there's always a native way out
- Phase 2, 4, 6-11 (shipped today): fix the release pipeline so guard fixes actually reach the runtime
- **Phase 13 (this release): prevent the loop from starting in the first place by warning at session boot**

## What the SessionStart hook does

On every session boot, the guard checks if the CWD is in a git repo, reads the current branch, and:

- **Not in a git repo** → silent exit (nothing to warn about).
- **Not on main or master** → silent exit (feature branches are fine).
- **On main or master** → emits a warning via `hookSpecificOutput.additionalContext` that includes:
  - The repo path
  - A list of existing linked worktrees (first 10) with ready-to-paste `cd <path>` commands for each, annotated with the branch name
  - The template for creating a fresh worktree: `git worktree add .worktrees/<repo>--cc-mini--<feature> -b cc-mini/<feature>`
  - The native `git stash push` escape hatch instructions in case an untracked file blocks `git pull`
  - Pointers to the guard master plan and the bugs-plan-04-05-2026-002 master plan

The warning is informational. It does NOT block session boot. An agent that wakes up on main gets the warning in its initial context so the first time it reaches for a write operation, it already knows the recovery path.

## Implementation

Single-file change to `guard.mjs`. The existing `main()` function now dispatches on `hook_event_name` (falling back to shape detection for older payloads). A new `handleSessionStart(input)` function handles the SessionStart path, exiting the process when it's done.

`package.json` `claudeCode.hooks` now advertises both events. `INSTALL.md` updated with the new two-event wiring.

## New hook wiring

Both events point at the same `guard.mjs` script. Add both to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|NotebookEdit|Bash",
        "hooks": [
          { "type": "command", "command": "node /Users/lesa/.ldm/extensions/wip-branch-guard/guard.mjs", "timeout": 5 }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          { "type": "command", "command": "node /Users/lesa/.ldm/extensions/wip-branch-guard/guard.mjs", "timeout": 5 }
        ]
      }
    ]
  }
}
```

## Files changed

- `tools/wip-branch-guard/guard.mjs`: new `handleSessionStart(input)`, event dispatcher in `main()`, worktree enumeration helper
- `tools/wip-branch-guard/package.json`: 1.9.72 -> 1.9.73, `claudeCode.hook` -> `claudeCode.hooks` (array of two entries)
- `tools/wip-branch-guard/INSTALL.md`: complete rewrite with new two-event wiring, what each event does, and test invocations for both
- `tools/wip-branch-guard/test.sh`: three new SessionStart test cases (main tree warns, feature branch silent, non-git silent)
- `CHANGELOG.md`: entry for 1.9.73

## Verified

- 36/36 test cases pass (33 existing PreToolUse + 3 new SessionStart)
- Manual injection with `echo '{"hook_event_name":"SessionStart","cwd":"...","source":"startup"}' | node guard.mjs` produces expected output
- Manual injection with feature-branch CWD exits silently
- Manual injection with /tmp (non-git) exits silently
- Existing PreToolUse tests unchanged, no regressions

## Cross-references

- `ai/product/bugs/guard/2026-04-05--cc-mini--guard-master-plan.md` Phase 7 (guard master plan's Phase 7 maps to this release)
- `ai/product/bugs/master-plans/bugs-plan-04-05-2026-002.md` Wave 2 phase 13
- Prior guard ships today: 1.9.72 (stash allow), 1.9.73 (this release)
- Settings.json wiring needs to be deployed to `~/.claude/settings.json` for the SessionStart hook to activate. `ldm install` should handle this.

## 1.9.71-alpha.9 (2026-04-05)

# v1.9.71-alpha.8

## wip-release: automatic PR flow for protected main (Phase 4)

When `git push origin main` fails with GitHub's "protected branch" rejection (`GH006: Changes must be made through a pull request`), wip-release now automatically:

1. Creates a release branch `cc-mini/release-v<version>` at the current commit
2. Pushes the branch to origin
3. Opens a PR via `gh pr create` with title `release: v<version>`
4. Merges the PR via `gh pr merge --merge --delete-branch`
5. Pushes the tag separately (tags bypass branch protection on most GitHub setups)
6. Fast-forwards local main so downstream steps (deploy-public, etc.) have a clean state

Previously this was a 4-command manual workflow every release:

```
git branch cc-mini/release-alpha-N
git push -u origin cc-mini/release-alpha-N
gh pr create --base main --head cc-mini/release-alpha-N --title '...'
gh pr merge <pr> --merge --delete-branch
git push origin v<version>
```

Every release. Every time. Eliminated.

## Fallback behavior

If any step of the auto-PR flow fails (gh CLI missing, PR create failure, merge failure, tag push failure), wip-release logs a concrete recovery command for the exact failure mode and continues (non-fatal, matches prior push-failed behavior). The user can always complete the remaining steps manually.

## Direct push still works

If the repo allows direct push to main (typical for private staging repos), wip-release tries direct push first and only falls back to the PR flow on the specific GH006 / "protected branch" error. No behavioral change for unprotected repos.

## Files changed

- `tools/wip-release/core.mjs`: new `pushReleaseWithAutoPr(repoPath, newVersion, level)` and `logPushFailure(result, tag)` helpers. Three push sites in `release()`, `releaseHotfix()`, `releasePrerelease()` migrated to use the helper.
- `tools/wip-release/package.json`: 1.9.72 -> 1.9.73
- `CHANGELOG.md`: entry added

## Verified

- Module imports cleanly via `node -e "import('./tools/wip-release/core.mjs')"`.
- Error detection regex handles GH006 variants: `/protected branch|GH006|Changes must be made through a pull request/i`.
- All three release tracks (stable, prerelease, hotfix) use the same helper.

## Cross-references

- `ai/product/bugs/release-pipeline/2026-04-05--cc-mini--release-pipeline-master-plan.md` Phase 4 (Incident 4)
- `ai/product/bugs/master-plans/bugs-plan-04-05-2026-002.md` Wave 2 phase 7
- Prior ship: alpha.7 closed Phases 1, 2, 8 of the same plan.

## 1.9.71-alpha.8 (2026-04-05)

# v1.9.71-alpha.8

## wip-release: automatic PR flow for protected main (Phase 4)

When `git push origin main` fails with GitHub's "protected branch" rejection (`GH006: Changes must be made through a pull request`), wip-release now automatically:

1. Creates a release branch `cc-mini/release-v<version>` at the current commit
2. Pushes the branch to origin
3. Opens a PR via `gh pr create` with title `release: v<version>`
4. Merges the PR via `gh pr merge --merge --delete-branch`
5. Pushes the tag separately (tags bypass branch protection on most GitHub setups)
6. Fast-forwards local main so downstream steps (deploy-public, etc.) have a clean state

Previously this was a 4-command manual workflow every release:

```
git branch cc-mini/release-alpha-N
git push -u origin cc-mini/release-alpha-N
gh pr create --base main --head cc-mini/release-alpha-N --title '...'
gh pr merge <pr> --merge --delete-branch
git push origin v<version>
```

Every release. Every time. Eliminated.

## Fallback behavior

If any step of the auto-PR flow fails (gh CLI missing, PR create failure, merge failure, tag push failure), wip-release logs a concrete recovery command for the exact failure mode and continues (non-fatal, matches prior push-failed behavior). The user can always complete the remaining steps manually.

## Direct push still works

If the repo allows direct push to main (typical for private staging repos), wip-release tries direct push first and only falls back to the PR flow on the specific GH006 / "protected branch" error. No behavioral change for unprotected repos.

## Files changed

- `tools/wip-release/core.mjs`: new `pushReleaseWithAutoPr(repoPath, newVersion, level)` and `logPushFailure(result, tag)` helpers. Three push sites in `release()`, `releaseHotfix()`, `releasePrerelease()` migrated to use the helper.
- `tools/wip-release/package.json`: 1.9.72 -> 1.9.73
- `CHANGELOG.md`: entry added

## Verified

- Module imports cleanly via `node -e "import('./tools/wip-release/core.mjs')"`.
- Error detection regex handles GH006 variants: `/protected branch|GH006|Changes must be made through a pull request/i`.
- All three release tracks (stable, prerelease, hotfix) use the same helper.

## Cross-references

- `ai/product/bugs/release-pipeline/2026-04-05--cc-mini--release-pipeline-master-plan.md` Phase 4 (Incident 4)
- `ai/product/bugs/master-plans/bugs-plan-04-05-2026-002.md` Wave 2 phase 7
- Prior ship: alpha.7 closed Phases 1, 2, 8 of the same plan.

## 1.9.71-alpha.7 (2026-04-05)

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

## 1.9.71-alpha.6 (2026-04-05)

Guard 1.9.72: allow git stash push on main to unblock native untracked-file escape hatch

## 1.9.71-alpha.5 (2026-04-05)

Guard 1.9.72: allow git stash push on main to unblock native untracked-file escape hatch

## 1.9.72-alpha.1 (2026-04-05)

### wip-branch-guard

Allow `git stash push` / `git stash save` / bare `git stash` on main. Stashing is non-destructive (drop/pop/clear remain blocked in DESTRUCTIVE_PATTERNS). This closes the loop where an untracked file in main's working tree blocks `git pull` and every clearing command (rm, mv, git stash, git clean, git reset) is also blocked, leaving no native escape hatch. Agents and humans lost hours to this.

Error message now points at the stash workaround explicitly so future sessions don't loop:

```
STUCK clearing an untracked file before git pull? Use stash (non-destructive):
  git stash push -u -- <path>
  git pull
  git stash list
```

## 1.9.71-alpha.4 (2026-04-04)

Guard: allow cp/mv/mkdir hotfixes to deployed extensions

## 1.9.71-alpha.3 (2026-04-04)

Guard: allow cp/mv/mkdir hotfixes to deployed extensions (.openclaw|.ldm)/extensions/, add .ldm/extensions/ to shared-state patterns for symmetry with .openclaw/extensions/

## 1.9.71-alpha.2 (2026-04-03)

Guard: allow bootstrap in zero-commit repos

## 1.9.71-alpha.1 (2026-04-01)

File guard: allow harness memory writes, guard v1.9.69

## 1.9.70 (2026-04-01)

### wip-release
- Fix semver NaN bug: `semver.inc()` returns null on prerelease versions, causing NaN propagation through the entire release pipeline
- Add sub-tool independent version validation: detects when sub-tool package.json versions drift from root and warns before publish

### wip-branch-guard
- Add cooldown skip: avoids redundant guard checks within rapid tool sequences
- Add trash pattern exclusion: allows `.Trash` and system cleanup paths through the guard






























## 1.9.69-alpha.1 (2026-04-01)

alpha prerelease

## 1.9.68 (2026-04-01)

# Release Notes: wip-ai-devops-toolbox v1.9.68

Closes #239

## Four-track release pipeline

The release tool now supports four tracks: alpha, beta, hotfix, and stable. This replaces the single-track model where every release was public.

Alpha is silent (no public release notes by default). Beta publishes prerelease notes to the public repo. Hotfix publishes to npm @latest without syncing code to public. Stable is the full deploy: npm + code sync + release notes. Developers can iterate on private, ship betas to testers, and only go public when ready.

Version numbering uses standard semver prereleases: `1.9.68-alpha.1`, `1.9.68-beta.1`. The installer (`ldm install --beta` / `--alpha`) pulls the right tag from npm.

## 1.9.67 (2026-03-31)

# Release Notes: wip-ai-devops-toolbox v1.9.67

**Date:** 2026-03-30

## What changed

### Hardcoded path removal

Two files in the devops toolbox had paths that assumed a specific username or iCloud layout.

**ldm-jobs/backup.sh** referenced `/Users/lesa/Library/Mobile Documents/.../ldm/bin/` to find the `ldm` binary for scheduled backup jobs. This iCloud path was fragile (iCloud sync delays, different usernames). The script now uses `$HOME/.ldm/bin/` which is the standard LDM install location and works on any machine (#301).

**test.sh** (the branch guard test harness) had `/Users/lesa` hardcoded for creating temp directories. It now uses `$HOME` so tests run correctly under any user account (#301).

### Earlier changes included in this release

**v1.9.66** added auto-combine for release notes from batched PRs (#237). When multiple PRs are merged between releases, their individual RELEASE-NOTES files are automatically combined into a single changelog entry.

**v1.9.65** fixed the scaffold-on-main issue (#223) where scaffolding left untracked files that blocked `git pull` on the main working tree.

## Why

The backup job is scheduled via LaunchAgent and runs unattended. If the path to `ldm` is wrong, backups silently fail. Moving to `$HOME/.ldm/bin/` aligns with the standard LDM install path and eliminates the iCloud dependency. The test fix ensures CI and local test runs work for all contributors.

## Issues closed

- #301

## How to verify

```bash
grep -r "/Users/lesa" ldm-jobs/ tools/wip-branch-guard/test.sh
# Should return zero results
```

## 1.9.66 (2026-03-30)

# Release Notes: wip-ai-devops-toolbox v1.9.66

Auto-combine release notes when batching multiple PRs into a single release.

## The story

When multiple PRs merge to main before wip-release runs, the release had no good way to gather all their stories. Each PR might have its own RELEASE-NOTES file committed on the branch, but once the branch merges and the file gets trashed, the next release only sees an empty repo root. The agent had to write a new RELEASE-NOTES file from scratch, losing the narrative that was already reviewed in each PR.

Now wip-release looks back through git history. It finds every merge commit since the last tag, checks each one for RELEASE-NOTES files via `git diff-tree` and `git show`, and combines them into a single document. If only one PR had notes, it uses them as-is (fully backwards compatible). If multiple PRs had notes, it wraps them with per-PR section headers, strips duplicate top-level headings, and collects all issue references into a combined list at the end.

The detection sits at priority 2.5 in the release notes cascade: after the single-file check (RELEASE-NOTES-v{ver}.md on disk) but before the dev-update fallback. A file on disk always wins. The merged-PR scan only kicks in when nothing is found on disk.

## What changed

- New exported function `collectMergedPRNotes()` in `core.mjs` that scans git merge history for RELEASE-NOTES files
- Updated `cli.js` to call it at priority 2.5 in the notes detection cascade
- Updated help text to document the new detection path
- Zero breaking changes. Single-file detection still works exactly as before.

## Issues closed

- Closes #237

## How to verify

```bash
# In any repo with multiple merged PRs since last tag, each having RELEASE-NOTES files:
wip-release patch --dry-run
# Should show: "Combined release notes from N merged PRs"
```

## 1.9.65 (2026-03-29)

# Release Notes: wip-ai-devops-toolbox v1.9.65

**Fix release notes scaffold on protected branches**

When `wip-release patch` runs on main without a RELEASE-NOTES file, it used to scaffold a
template directly in the working tree. On repos with branch guards (pre-commit hooks that
block commits to main), this scaffolded file could not be removed or committed. It would
block `git pull` and leave the working tree dirty. This has happened multiple times across
different repos.

The fix adds a branch check before scaffolding. If the current branch is main or master,
wip-release now prints a clear error telling the user to write release notes on their
feature branch before merging, then exits non-zero without creating any files. The scaffold
behavior still works on feature branches, where it's actually useful.

## Issues closed

- Closes #223

## How to verify

```bash
# On main, without release notes: should error, NOT scaffold
cd any-repo && git checkout main
wip-release patch
# Expected: "Release notes missing. Write RELEASE-NOTES-v*.md on your feature branch before merging."
# Expected: no RELEASE-NOTES file created in working tree

# On a feature branch: should scaffold as before
git checkout -b test/scaffold-check
wip-release patch
# Expected: scaffolded template created
```

## 1.9.64 (2026-03-29)

# Release Notes: wip-ai-devops-toolbox v1.9.64

Closes #295

## Branch guard: allow extension cleanup

The branch guard blocked `rm` on deployed extension directories (`~/.openclaw/extensions/` and `~/.ldm/extensions/`) because those paths live inside git repos. But deployed extensions are managed by `ldm install`, not by hand. When a stale `-private` extension needed to be removed (e.g. `wip-xai-grok-private` replaced by the public `wip-xai-grok`), the agent couldn't clean it up without asking the user to run the command manually.

Added an allowlist pattern for `rm` targeting `.openclaw/extensions/` and `.ldm/extensions/` paths. Same approach as the existing `.ldm/state/` allowlist. The guard still blocks `rm` on actual repo source files.

## 1.9.63 (2026-03-29)

# Release Notes: wip-ai-devops-toolbox v1.9.63

**Fix all wip-release errors: branch cleanup crashes, shell injection, stale remote refs.**

## The story

Every wip-release run produced errors: "fatal: Not a valid object name +", "remote ref does not exist", and shell injection risks from branch names passed through execSync template strings. These were dismissed as "non-blocking" but they cluttered every release output and masked real problems.

Root cause: branch cleanup code (sections 10 and 11) used `execSync` with template strings, which breaks on branch names with special characters and allows shell injection. Also tried to delete remote branches that GitHub already deleted during PR merge.

Fix: replaced all `execSync` template strings with `execFileSync` array args (safe from injection). Added character validation to skip branches with special chars. Wrapped remote delete in try/catch since GitHub PR merge already handles deletion.

## Issues closed

- #231 (continued: release pipeline reliability)

## How to verify

```bash
wip-release patch --dry-run
# Should show no "fatal" or "Not a valid object name" errors
# Guard tests: cd tools/wip-branch-guard && bash test.sh
```

## 1.9.62 (2026-03-29)

# Release Notes: wip-ai-devops-toolbox v1.9.62

**Fix wip-release leaving dirty state on main after every release.**

## The story

wip-release writes to 15+ files during a release (root package.json, 12 sub-tool package.json files, SKILL.md, CHANGELOG.md, product docs, trashed release notes). But gitCommitAndTag() only staged 3 files (package.json, CHANGELOG.md, SKILL.md). The other 12+ files were left modified on disk, uncommitted. This blocked git pull on the next operation and required manual `git checkout -- .` every time.

Fix: stage all files that wip-release modifies. Sub-tool package.json files, product docs (ai/product/), and trashed release notes (_trash/) are now included in the release commit.

## Issues closed

- #231 (wip-release rollback version bumps on failure)

## How to verify

```bash
wip-release patch
git status
# Should show clean working tree after release
```

## 1.9.61 (2026-03-29)

# Release Notes: wip-ai-devops-toolbox v1.9.61

**Add test script for branch guard. Fix node bypass regex.**

## The story

Every guard bug this session (v1.9.56-59) would have been caught by running a test before merging. This release adds test.sh to the guard that pipes test JSON into guard.mjs and verifies allow/deny results. 30 test cases covering destructive commands, quoted strings (Bug 1/3), compound commands (Bug 2), safe commands, and plan files.

Also fixes the node bypass regex: `require('fs').writeFileSync` wasn't caught because the regex looked for `fs.writeFile` literally. Broadened to match `writeFile` after `node -e`.

## Issues closed

- #232 (guard test coverage)

## How to verify

```bash
cd tools/wip-branch-guard && bash test.sh
# Should show: 30 passed, 0 failed, 3 skipped
```

## 1.9.60 (2026-03-29)

# Release Notes: wip-ai-devops-toolbox v1.9.60

**Fix npm package bloat: exclude worktrees and _trash from published tarball.**

## The story

v1.9.59 published 869 files (3.9 MB) to npm because leftover worktree directories and _trash/ were included in the tarball. The .npmignore only excluded ai/ and .DS_Store. Added _trash/, .worktrees/, _worktrees/, .claude/, .wrangler/ to .npmignore. Also cleaned up 10 stale worktrees from previous sessions.

## Issues closed

- #232 (continued cleanup)

## How to verify

```bash
npm pack --dry-run 2>&1 | tail -5
# Should show ~200 files, not 869
```

## 1.9.59 (2026-03-29)

# Release Notes: wip-ai-devops-toolbox v1.9.59

**Fix three bugs in branch guard destructive command handling.**

## The story

v1.9.56 added destructive command blocking but introduced three bugs because the new code was written differently from the existing guard pattern. The existing guard checks allowed patterns before blocked patterns and works per-command. The new code skipped the allowed check and matched against the entire raw command string, causing false positives on quoted text (blocking `gh issue create` when the body mentioned git commands) and false negatives on compound commands (allowing `rm -f file ; echo done` because `echo` is in the allowed list).

Fix: two helper functions that strip quoted content before matching and check each command segment independently. Same pattern as the existing guard code. Also adds `~/.claude/plans/` to the shared state allowlist so plan files are editable.

## Issues closed

- #232 (branch guard three bugs in v1.9.56)

## How to verify

```bash
# These should now be ALLOWED (were false-positive blocked):
# gh issue create --body "use git checkout -- to fix"
# echo "don't run git commit on main"

# These should now be DENIED (were false-negative allowed):
# rm -f file ; echo done  (on main)

# These should still be DENIED:
# git checkout -- file.txt
# python3 -c "open('f').write('x')"
```

## 1.9.58 (2026-03-29)

# Release Notes: wip-ai-devops-toolbox v1.9.58

**Fix deploy-public.sh losing release notes when invoked with relative path.**

## The story

When deploy-public.sh was called with `.` as the private repo path (e.g. `bash scripts/deploy-public.sh . wipcomputer/repo`), the script later cd'd into a temp directory. After that, `cd "."` no longer pointed to the private repo, so `gh release view` failed silently and release notes fell back to the empty "Release vX.Y.Z" default. This has been broken since at least v1.9.51.

Fix: resolve PRIVATE_REPO to an absolute path at startup before any cd happens.

## Issues closed

- #228 (continued from v1.9.57)

## How to verify

```bash
# From a repo directory, run with "." and check public release has real notes:
cd /path/to/private-repo
bash scripts/deploy-public.sh . wipcomputer/public-repo --dry-run
```

## 1.9.57 (2026-03-29)

# Release Notes: wip-ai-devops-toolbox v1.9.57

**deploy-public.sh now excludes .worktrees/ and _worktrees/ from public repo syncs.**

## The story

v1.9.56 accidentally deployed worktree directories (containing embedded git repos) to the public repo. The deploy script's rsync excluded ai/, .git/, _trash/, and other dev artifacts but didn't exclude worktree directories. Added both .worktrees/ (new convention) and _worktrees/ (old convention) to the exclude list.

## Issues closed

- #228 (deploy-public.sh leaks .worktrees/ to public repo)

## How to verify

```bash
# Run deploy-public.sh --dry-run and confirm .worktrees/ is not synced
grep -n "worktrees" scripts/deploy-public.sh
```

## 1.9.56 (2026-03-29)

# Release Notes: wip-ai-devops-toolbox v1.9.56

**Branch guard now blocks destructive git commands on all branches.**

## The story

The branch guard blocked commits and file writes on main, but allowed destructive git commands that destroy uncommitted work. Commands like `git clean -fd`, `git checkout --`, `git stash drop`, and `git reset --hard` slipped through because they were either in the allowed list or not in the blocked list. These commands destroyed Parker's Finder aliases, other agents' uncommitted edits, and user files multiple times on Mar 28-29.

The fix adds a new DESTRUCTIVE_PATTERNS list that fires on ALL branches, not just main. The guard also closes several bypass vectors: `node -e` removed from the allowed list, python/node file-write patterns detected, and `git checkout` narrowed to branch-switching only.

## What changed

- Added DESTRUCTIVE_PATTERNS: git clean -f, git checkout --, git stash drop/pop/clear, git reset --hard, git restore, python/node bypasses
- Removed `git checkout` blanket allow. Now only allows `git checkout <branch>` (switching)
- Removed `git stash drop` from allowed list
- Removed `node -e` from allowed bash patterns (bypass vector)
- Added `git stash show` and `git restore --staged` as safe read-only operations
- Deny message tells agent to use worktrees and safety checkpoints instead

## Issues closed

- #240 (branch guard + harness directories)
- #241 (python bypass detection)
- PR #284

## How to verify

```bash
# These should all be BLOCKED:
# git clean -fd
# git checkout -- somefile
# git stash drop
# git stash pop
# git reset --hard
# python3 -c "open('f','w').write('x')"

# These should still WORK:
# git checkout main (branch switching)
# git stash list (read-only)
# git status, git log, git diff
# Normal worktree workflow
```

## 1.9.55 (2026-03-28)

# Release Notes: wip-ai-devops-toolbox v1.9.55

Force redeploy: .worktrees guard fix.

## The story

v1.9.53 had the guard fix but deploy-public was missed. v1.9.54 force-redeployed but installer had already cached v1.9.54. This version ensures the public repo and npm are in sync so ldm install deploys the correct guard.mjs with .worktrees convention.

## Issues closed

- #240 (partial)

## 1.9.54 (2026-03-28)

# Release Notes: wip-ai-devops-toolbox v1.9.54

Force redeploy: guard files were stale after v1.9.53.

## The story

v1.9.53 published the .worktrees guard fix to npm but ldm install saw the version as current and skipped redeploying the files. The deployed guard.mjs was still the old version. This release forces a version bump so the installer re-deploys.

This is a bug in the installer: it checks version numbers but not file contents. Filed for future fix.

## Issues closed

- #240 (partial: .worktrees convention)

## 1.9.53 (2026-03-28)

# Release Notes: wip-ai-devops-toolbox v1.9.53

**One-line summary of what this release does**

Tell the story. What was broken or missing? What did we build? Why does the user care?
Write at least one real paragraph of prose. Not just bullets. The release notes gate
will block if there is no narrative. Bullets are fine for details, but the story comes first.

## The story

(Write a paragraph here. What was the problem? What does this release fix? Why does it matter?
This is what users read. Make it worth reading.)

## Issues closed

- #282

## How to verify

```bash
# Commands to test the changes
```

## 1.9.52 (2026-03-27)

# Release Notes: wip-ai-devops-toolbox v1.9.52

**Fix branch guard false-blocking bash commands targeting worktree paths**

## What changed

- Branch guard now extracts absolute paths from any bash command (mkdir, cp, mv, touch, etc.) and resolves the git branch from the target path's repo, not the CWD
- `findRepoRoot()` improved to walk up to existing directories for paths that don't exist yet (handles mkdir for new directories)
- Added `.ldm/worktrees` to allowed worktree locations alongside `_worktrees/` and `.claude/worktrees`

## Why

When Claude Code launches from `~/wipcomputerinc/` (on main) and runs bash commands targeting files inside a worktree (e.g., `mkdir -p /path/to/_worktrees/repo--branch/new-dir/`), the guard only knew how to extract paths from `cd` and `git -C` patterns. Any other command fell back to CWD resolution, saw "main", and blocked incorrectly. This caused minutes of wasted time every session.

## Issues closed

- wipcomputer/wip-ldm-os#187

## How to verify

```bash
# From CWD on main, this should no longer be blocked:
# mkdir -p /path/to/_worktrees/repo--branch/new-directory/
# cp file.txt /path/to/_worktrees/repo--branch/
```

## 1.9.51 (2026-03-24)

# Release Notes: wip-ai-devops-toolbox v1.9.51

## Branch Guard: Workspace Files Allowlist (#185)

Added TOOLS.md, MEMORY.md, IDENTITY.md, SOUL.md, WHERE-TO-WRITE.md, HEARTBEAT.md to the shared state allowlist. Both agents can now write to workspace files on main without being blocked.

Previously only SHARED-CONTEXT.md was allowed. This broke Lesa's ability to edit her own workspace files during the migration to ~/wipcomputerinc/.

## TECHNICAL.md: Backup Documentation

Updated LDM Dev Tools.app backup section to reflect the unified backup system. backup.sh now calls `~/.ldm/bin/ldm-backup.sh` (deployed by ldm install from wip-ldm-os-private/scripts/).

## 1.9.50 (2026-03-20)

# Release Notes: wip-ai-devops-toolbox v1.9.50

**wip-release: require product update doc on every release.**

## What changed

New quality gate in wip-release: checks that `ai/dev-updates/product-update/*-product-update.md` was modified since the last release tag. Same pattern as dev-updates, roadmap, and readme-first checks.

The product update doc is a human-readable test guide. Each release entry has: what changed, how it's supposed to work, and how to test. New entries go at the top. Additive only.

## Why

Three repos now have product update docs but nothing enforced keeping them current. Without the gate, the docs will drift immediately (same problem we had with TECHNICAL.md).

## Issues closed

- #220

## How to verify

```bash
wip-release patch --dry-run
# Should warn if product update doc not modified since last release
```

## 1.9.49 (2026-03-20)

# Release Notes: wip-ai-devops-toolbox v1.9.49

**TECHNICAL.md audit: 2 weeks of undocumented features now documented.**

## What changed

Full TECHNICAL.md audit covering v1.9.15 through v1.9.48. Two passes. Key additions:

- **wip-release quality gates:** Technical docs gate, interface coverage gate, product docs auto-sync, all skip flags documented.
- **deploy-public.sh:** Full 8-step pipeline including GitHub Packages publishing, repo URL rewrite, co-author sync.
- **wip-license-guard:** Now documented as both CLI and Claude Code PreToolUse hook (guard.mjs). Enforcement details.
- **wip-branch-guard:** Worktree requirement on branches, non-repo file passthrough, workflow teaching messages.
- **wip-repos claude:** Cross-repo CLAUDE.md ecosystem generator fully documented.
- **Source code table:** Missing files added (guard.mjs, claude.mjs, mcp-server.mjs).
- **Log paths:** Fixed stale /tmp/ references to ~/.ldm/logs/.

## Why

15 releases shipped without TECHNICAL.md updates. Agents reading the docs were missing critical features: release gates, license enforcement hooks, deploy pipeline details.

## Issues closed

- #218

## How to verify

```bash
grep "Interface coverage" TECHNICAL.md    # new gate
grep "guard.mjs" TECHNICAL.md             # license-guard hook
grep "GitHub Packages" TECHNICAL.md       # deploy pipeline
```

## 1.9.48 (2026-03-20)

# Release Notes: wip-ai-devops-toolbox v1.9.48

**Document wip-repos claude command in SKILL.md and TECHNICAL.md.**

## What changed

- SKILL.md: added `wip-repos claude` commands to the wip-repos section
- TECHNICAL.md: full documentation of how the ecosystem generator works, template locations, delimiter convention

## Why

v1.9.47 shipped the `wip-repos claude` command without updating technical docs. Now documented.

## Issues closed

- #212 (docs portion)

## How to verify

```bash
grep "wip-repos claude" SKILL.md TECHNICAL.md
```

## 1.9.47 (2026-03-20)

# Release Notes: wip-ai-devops-toolbox v1.9.47

**New: `wip-repos claude` command + CLAUDE.md templates.**

## What changed

### `wip-repos claude` (Phases 1-3 of the CLAUDE.md plan)

New subcommand that generates cross-repo ecosystem sections in CLAUDE.md files. When an agent opens repo-A, it can't read repo-B. This command pre-generates the context.

```bash
wip-repos claude              # regenerate all repos
wip-repos claude my-repo      # regenerate one repo
wip-repos claude --init       # create CLAUDE.md for repos missing one
wip-repos claude --dry-run    # preview changes
```

Features:
- Reads all repos from manifest, extracts metadata (package.json, SKILL.md, directory structure)
- Generates `## Ecosystem` sections with delimiter comments (`<!-- wip-repos:start/end -->`)
- Hand-written sections are never overwritten
- Relevance filtering: only related repos shown (same category + core repos)
- `--init` creates starter CLAUDE.md from template for repos missing one

### Templates

- `templates/global-claude-md.md` ... universal CLAUDE.md for ~/.claude/CLAUDE.md
- `templates/repo-claude-md.template` ... per-repo starter with ecosystem placeholder

## Why

Agents lose context across repos. They can't read sibling repos at runtime. Pre-generating cross-repo maps into CLAUDE.md solves this without requiring runtime access.

## Issues closed

- #212 (partial: Phases 1-3 of 6)

## How to verify

```bash
wip-repos claude --dry-run
```

## 1.9.46 (2026-03-18)

# Release Notes: wip-ai-devops-toolbox v1.9.46

**Centralized worktree management: guard rule, wip-release prune, Dev Guide convention.**

## What changed

### Guard: worktree path warning (#212)
Branch guard now warns when `git worktree add` creates a worktree outside `_worktrees/`. Shows the convention and suggests `ldm worktree add`. Warning only, not a hard block.

### wip-release: worktree prune (#212)
New step 12 in the release pipeline. After branch cleanup, prunes stale worktrees from `_worktrees/` whose branches are merged into main. Automatic cleanup after every release.

### Dev Guide: _worktrees/ convention (#212)
Documents the centralized worktree convention:
- All worktrees go in `_worktrees/<repo-name>--<branch-suffix>/`
- Use `ldm worktree add` (auto-detects repo, creates in the right place)
- Guard warns about worktrees outside the convention
- `wip-release` auto-prunes merged worktrees

## Why

Worktrees created as repo siblings confused iCloud sync, looked like real repos in directory listings, and were never cleaned up. This session alone created 10+ stale worktrees. The convention keeps them organized and the release pipeline cleans them automatically.

## Issues closed

- #212
- #213

## How to verify

```bash
# Guard warning:
cd /path/to/repo
git worktree add ../my-worktree -b test   # should warn about _worktrees/

# Correct path:
ldm worktree add cc-mini/test             # creates _worktrees/<repo>--cc-mini--test/
```

## 1.9.45 (2026-03-18)

# Release Notes: wip-ai-devops-toolbox v1.9.45

**Guard now teaches the workflow instead of just blocking.**

## What changed

- **Branch guard error messages overhauled (#213).** When the guard blocks a write on main, it now shows the full 8-step process: worktree, branch, commit, push, PR, merge, wip-release, deploy-public. Includes the lesson that release notes go on the feature branch, not as a separate PR.
- **Separate error for "on branch but not in worktree."** Tells the agent to go back to main and create a worktree properly.
- **CLAUDE.md added to shared state allowlist.** Was patched in the deployed guard but missing from source. Now in sync.

## Why

Agents kept getting blocked by the guard and then trying workarounds instead of following the process. The error message said "Use a worktree" but didn't explain the full workflow. Today's session hit this 5+ times. The guard works. The gap was agent knowledge.

## Issues closed

- #213
- #256

## How to verify

```bash
# In any repo on main, try to edit a file. The error should show the full workflow.
# In any repo on a branch (not worktree), try to edit. Should show worktree instructions.
```

## 1.9.44 (2026-03-17)

# Guard non-repo files fix + UTC date fix

Two bugs fixed in one PR.

## Bug 1: Guard blocks files outside git repos (#77)

**Problem:** When Write/Edit targets a file outside any git repo (e.g. `~/.claude/plans/`), `findRepoRoot()` returns null. The guard fell back to CWD (`~/.openclaw` on main) and blocked the operation. Files outside repos aren't the guard's concern.

**Fix:** If `findRepoRoot(filePath)` returns null for Write/Edit operations, allow immediately. The guard only protects git repos from direct-on-main edits.

**File:** `tools/wip-branch-guard/guard.mjs`

## Bug 2: UTC date mismatch in wip-release

**Problem:** Dev-update files are named with local date (e.g. `2026-03-16--cc-mini--...md`). But `new Date().toISOString().split('T')[0]` returns UTC date. After midnight UTC (4 PM PST), the dates diverge. Release notes gate fails to find today's dev-update.

**Fix:** Replaced all three instances of `toISOString()` date extraction with explicit local date construction using `getFullYear()/getMonth()/getDate()`.

**Files:**
- `tools/wip-release/cli.js` (line 80, dev-update detection)
- `tools/wip-release/core.mjs` (line 92, CHANGELOG date)
- `tools/wip-release/core.mjs` (line 582, product docs sync date)

## 1.9.43 (2026-03-17)

# Guard non-repo files fix + UTC date fix

Two bugs fixed in one PR.

## Bug 1: Guard blocks files outside git repos (#77)

**Problem:** When Write/Edit targets a file outside any git repo (e.g. `~/.claude/plans/`), `findRepoRoot()` returns null. The guard fell back to CWD (`~/.openclaw` on main) and blocked the operation. Files outside repos aren't the guard's concern.

**Fix:** If `findRepoRoot(filePath)` returns null for Write/Edit operations, allow immediately. The guard only protects git repos from direct-on-main edits.

**File:** `tools/wip-branch-guard/guard.mjs`

## Bug 2: UTC date mismatch in wip-release

**Problem:** Dev-update files are named with local date (e.g. `2026-03-16--cc-mini--...md`). But `new Date().toISOString().split('T')[0]` returns UTC date. After midnight UTC (4 PM PST), the dates diverge. Release notes gate fails to find today's dev-update.

**Fix:** Replaced all three instances of `toISOString()` date extraction with explicit local date construction using `getFullYear()/getMonth()/getDate()`.

**Files:**
- `tools/wip-release/cli.js` (line 80, dev-update detection)
- `tools/wip-release/core.mjs` (line 92, CHANGELOG date)
- `tools/wip-release/core.mjs` (line 582, product docs sync date)

## 1.9.42 (2026-03-17)

# Guard non-repo files fix + UTC date fix

Two bugs fixed in one PR.

## Bug 1: Guard blocks files outside git repos (#77)

**Problem:** When Write/Edit targets a file outside any git repo (e.g. `~/.claude/plans/`), `findRepoRoot()` returns null. The guard fell back to CWD (`~/.openclaw` on main) and blocked the operation. Files outside repos aren't the guard's concern.

**Fix:** If `findRepoRoot(filePath)` returns null for Write/Edit operations, allow immediately. The guard only protects git repos from direct-on-main edits.

**File:** `tools/wip-branch-guard/guard.mjs`

## Bug 2: UTC date mismatch in wip-release

**Problem:** Dev-update files are named with local date (e.g. `2026-03-16--cc-mini--...md`). But `new Date().toISOString().split('T')[0]` returns UTC date. After midnight UTC (4 PM PST), the dates diverge. Release notes gate fails to find today's dev-update.

**Fix:** Replaced all three instances of `toISOString()` date extraction with explicit local date construction using `getFullYear()/getMonth()/getDate()`.

**Files:**
- `tools/wip-release/cli.js` (line 80, dev-update detection)
- `tools/wip-release/core.mjs` (line 92, CHANGELOG date)
- `tools/wip-release/core.mjs` (line 582, product docs sync date)

## 1.9.41 (2026-03-17)

# Doc enforcement gates for wip-release

**Date:** 2026-03-16
**Closes:** #117, #128

## What changed

Two new pre-release gates in wip-release:

**Technical Docs Gate (#117):** When source code (*.mjs, *.js, *.ts) changed since the last release tag, checks that SKILL.md or TECHNICAL.md was also modified. Catches code shipping without doc updates. Warns on patch, blocks on minor/major. Skip with `--skip-tech-docs-check`.

**Interface Coverage Gate (#128):** For toolbox repos, scans each tool in tools/*/ for actual interfaces (CLI, Module, MCP, OC Plugin, Skill, CC Hook) and compares to the coverage table in README.md and SKILL.md. Reports: tools missing from table, interfaces detected but not marked Y, interfaces marked Y but not detected, tool count mismatches. Warns on patch, blocks on minor/major. Skip with `--skip-coverage-check`.

Both follow the same pattern as existing gates (checkProductDocs, checkStaleBranches). Both run in real and dry-run modes.

## Why

Source code was shipping without doc updates constantly. SKILL.md and TECHNICAL.md fell behind the code. Interface coverage tables drifted from reality. These gates catch it before release instead of after.

## 1.9.40 (2026-03-16)

# Auto-sync product docs version/date on release

**Date:** 2026-03-16
**Closes:** #202

## What changed

wip-release now auto-updates version and date lines in product docs before the release commit. No more stale "Current version: v1.9.1" when you're shipping v1.9.39.

Files updated automatically:
- `ai/product/plans-prds/roadmap.md`: "Current version" and "Last updated"
- `ai/product/readme-first-product.md`: "Last updated" and "What's Built (as of vX.Y.Z)"

Runs between changelog update and git commit (step 3.75). Only touches files that exist. Only updates lines that match the expected patterns.

## Why

These files were stale from v1.9.1 through v1.9.39 (8 days, 38 releases). Nobody remembered to update them. The existing product docs gate warned about it but couldn't fix it. Now it fixes itself.

## 1.9.39 (2026-03-16)

# Wire license-guard as Claude Code PreToolUse hook

**Date:** 2026-03-16
**Closes:** #130

## What changed

license-guard now registers as a Claude Code PreToolUse hook on install. Previously the hook code existed (hook.mjs) but was never wired into the deploy system. Now:

- Renamed hook.mjs to guard.mjs (matches file-guard/branch-guard convention that LDM OS deploy.mjs expects)
- Added `claudeCode.hook` config to package.json (event: PreToolUse, matcher: Bash, timeout: 5)
- On next `ldm install`, the hook auto-registers in ~/.claude/settings.json

The hook blocks git commit and git push when license compliance fails:
- LICENSE file missing
- Copyright doesn't match .license-guard.json config
- CLA.md missing
- README.md missing ## License section
- MIT+AGPL config but LICENSE or README only mentions MIT

Repos without .license-guard.json are not affected (the hook silently passes).

## Also done

- Updated plan statuses: license guard Phase 1 complete, bootstrap LDM OS complete
- Bootstrap LDM OS was already shipped in install.js (lines 740-812)

## 1.9.38 (2026-03-16)

# GitHub Packages publish from public repo

**Date:** 2026-03-16
**Closes:** #193

## What changed

`deploy-public.sh` now publishes to GitHub Packages from the public repo clone after the npm publish step. Previously, GitHub Packages were only published from the private repo during `wip-release`, so they showed on the private repo's Packages tab. Users couldn't see them.

Now packages show on the public repo's Packages tab where users expect to find them. Uses `gh auth token` for authentication (already available from the gh CLI).

## Why

The Packages tab on public repos was empty. Users visiting wipcomputer/wip-ldm-os or wipcomputer/wip-ai-devops-toolbox saw no packages even though they were published. The packages existed but were linked to the private repo.

## 1.9.37 (2026-03-16)

# GitHub Packages publish from public repo

**Date:** 2026-03-16
**Closes:** #193

## What changed

`deploy-public.sh` now publishes to GitHub Packages from the public repo clone after the npm publish step. Previously, GitHub Packages were only published from the private repo during `wip-release`, so they showed on the private repo's Packages tab. Users couldn't see them.

Now packages show on the public repo's Packages tab where users expect to find them. Uses `gh auth token` for authentication (already available from the gh CLI).

## Why

The Packages tab on public repos was empty. Users visiting wipcomputer/wip-ldm-os or wipcomputer/wip-ai-devops-toolbox saw no packages even though they were published. The packages existed but were linked to the private repo.

## 1.9.36 (2026-03-16)

# GitHub Packages publish from public repo

**Date:** 2026-03-16
**Closes:** #193

## What changed

`deploy-public.sh` now publishes to GitHub Packages from the public repo clone after the npm publish step. Previously, GitHub Packages were only published from the private repo during `wip-release`, so they showed on the private repo's Packages tab. Users couldn't see them.

Now packages show on the public repo's Packages tab where users expect to find them. Uses `gh auth token` for authentication (already available from the gh CLI).

## Why

The Packages tab on public repos was empty. Users visiting wipcomputer/wip-ldm-os or wipcomputer/wip-ai-devops-toolbox saw no packages even though they were published. The packages existed but were linked to the private repo.

## 1.9.35 (2026-03-16)

# GitHub Packages publish from public repo

**Date:** 2026-03-16
**Closes:** #193

## What changed

`deploy-public.sh` now publishes to GitHub Packages from the public repo clone after the npm publish step. Previously, GitHub Packages were only published from the private repo during `wip-release`, so they showed on the private repo's Packages tab. Users couldn't see them.

Now packages show on the public repo's Packages tab where users expect to find them. Uses `gh auth token` for authentication (already available from the gh CLI).

## Why

The Packages tab on public repos was empty. Users visiting wipcomputer/wip-ldm-os or wipcomputer/wip-ai-devops-toolbox saw no packages even though they were published. The packages existed but were linked to the private repo.

## 1.9.34 (2026-03-16)

# GitHub Packages publish from public repo

**Date:** 2026-03-16
**Closes:** #193

## What changed

`deploy-public.sh` now publishes to GitHub Packages from the public repo clone after the npm publish step. Previously, GitHub Packages were only published from the private repo during `wip-release`, so they showed on the private repo's Packages tab. Users couldn't see them.

Now packages show on the public repo's Packages tab where users expect to find them. Uses `gh auth token` for authentication (already available from the gh CLI).

## Why

The Packages tab on public repos was empty. Users visiting wipcomputer/wip-ldm-os or wipcomputer/wip-ai-devops-toolbox saw no packages even though they were published. The packages existed but were linked to the private repo.

## 1.9.33 (2026-03-15)

# --version on all CLIs + issue cleanup

**Date:** 2026-03-15
**Closes:** #190, #191, #169, #123, #119

## What changed

All 7 CLI tools now support `--version` and `-v`. Each reads its own `package.json` and prints the version. Previously, `wip-release --version` printed the help text instead of a version number.

Tools updated: wip-release, wip-repos, wip-license-guard, wip-repo-permissions, wip-repo-init, wip-readme-format, wip-file-guard, wip-branch-guard.

wip-license-guard also got a proper README (#169) with all commands, config format, and integration docs.

## Issues closed

- #190: wip-release --version should work
- #191: enforce --version on all CLI tools
- #169: wip-license-guard needs its own README
- #123: Merge/Deploy/Install conflated (enforced across v1.9.25-v1.9.30)
- #119: All destructive tools must have --dry-run (all confirmed)

## 1.9.32 (2026-03-15)

# --version on all CLIs + issue cleanup

**Date:** 2026-03-15
**Closes:** #190, #191, #169, #123, #119

## What changed

All 7 CLI tools now support `--version` and `-v`. Each reads its own `package.json` and prints the version. Previously, `wip-release --version` printed the help text instead of a version number.

Tools updated: wip-release, wip-repos, wip-license-guard, wip-repo-permissions, wip-repo-init, wip-readme-format, wip-file-guard, wip-branch-guard.

wip-license-guard also got a proper README (#169) with all commands, config format, and integration docs.

## Issues closed

- #190: wip-release --version should work
- #191: enforce --version on all CLI tools
- #169: wip-license-guard needs its own README
- #123: Merge/Deploy/Install conflated (enforced across v1.9.25-v1.9.30)
- #119: All destructive tools must have --dry-run (all confirmed)

## 1.9.31 (2026-03-15)

# Release Notes: wip-ai-devops-toolbox v1.9.31

Branch guard no longer blocks global npm operations on main.

## What changed

Moved `npm install -g` and `npm link` from BLOCKED_BASH_PATTERNS to ALLOWED_BASH_PATTERNS in `wip-branch-guard/guard.mjs`. Global npm operations modify `/opt/homebrew/`, not the repo. Local `npm install` (no -g flag) remains blocked.

## Why

During LDM OS v0.4.0 dogfood, a CC session couldn't run `npm install -g @wipcomputer/wip-ldm-os@0.4.0` even after Parker explicitly said "install." The guard was too aggressive. Original intent (issue #137) was to block repo writes on main, not system-level package installs.

## Issues closed

- Closes #188 (branch guard blocks npm install -g)
- Cross-ref: wipcomputer/wip-ldm-os#44

## How to verify

```bash
# On main branch, these should now succeed:
npm install -g @wipcomputer/wip-ldm-os@0.4.0
npm link
# This should still be blocked on main:
npm install
```

## 1.9.30 (2026-03-15)

# Release notes must be a file on disk

**Date:** 2026-03-15

## What changed

wip-release no longer accepts the `--notes` flag. Release notes MUST come from a file on disk:

1. `RELEASE-NOTES-v{version}.md` in repo root (auto-detected)
2. `ai/dev-updates/YYYY-MM-DD--description.md` (auto-detected)
3. `--notes-file=path` (explicit file path)

If no file exists, the release is blocked. The gate scaffolds a template (`RELEASE-NOTES-v{version}.md`) so the agent has something to fill in.

## Why

The `--notes` flag was the root cause of every bad release note. Agents passed one-liners like `--notes="fix bug"` and the gate let them through. Even after we added length checks and changelog detection, agents found ways around it. The flag was an escape hatch that undermined the entire system.

The file-on-disk requirement solves three problems:
1. **Reviewability.** The file is on the branch. It shows up in the PR diff. Parker can read and approve the release notes before merge.
2. **Quality.** Writing a file forces the agent to think about what changed and why. A flag encourages one-liners.
3. **History.** The file is committed to git. The release notes are part of the repo history, not a transient CLI argument.

## What agents need to do

Before running `wip-release`:
1. Write `RELEASE-NOTES-v{version}.md` or `ai/dev-updates/YYYY-MM-DD--description.md`
2. Commit it on the branch
3. The file shows up in the PR for review
4. After merge to main, `wip-release` auto-detects it

If the agent forgets, `wip-release` blocks and scaffolds a template.

## 1.9.29 (2026-03-15)

# Release notes must be a file on disk

**Date:** 2026-03-15

## What changed

wip-release no longer accepts the `--notes` flag. Release notes MUST come from a file on disk:

1. `RELEASE-NOTES-v{version}.md` in repo root (auto-detected)
2. `ai/dev-updates/YYYY-MM-DD--description.md` (auto-detected)
3. `--notes-file=path` (explicit file path)

If no file exists, the release is blocked. The gate scaffolds a template (`RELEASE-NOTES-v{version}.md`) so the agent has something to fill in.

## Why

The `--notes` flag was the root cause of every bad release note. Agents passed one-liners like `--notes="fix bug"` and the gate let them through. Even after we added length checks and changelog detection, agents found ways around it. The flag was an escape hatch that undermined the entire system.

The file-on-disk requirement solves three problems:
1. **Reviewability.** The file is on the branch. It shows up in the PR diff. Parker can read and approve the release notes before merge.
2. **Quality.** Writing a file forces the agent to think about what changed and why. A flag encourages one-liners.
3. **History.** The file is committed to git. The release notes are part of the repo history, not a transient CLI argument.

## What agents need to do

Before running `wip-release`:
1. Write `RELEASE-NOTES-v{version}.md` or `ai/dev-updates/YYYY-MM-DD--description.md`
2. Commit it on the branch
3. The file shows up in the PR for review
4. After merge to main, `wip-release` auto-detects it

If the agent forgets, `wip-release` blocks and scaffolds a template.

## 1.9.28 (2026-03-15)

# Release Notes Quality Gate

**Date:** 2026-03-15

## What changed

wip-release now blocks ALL releases (patch, minor, major) if the release notes are bad. Previously, patch releases only warned. Now they block.

The gate checks:
- Notes must be at least 50 characters
- Notes can't look like a changelog entry ("fix: ...", "add: ...", "update: ...")
- Minor/major still require a file (not --notes flag)

If the gate blocks, it tells you exactly how to fix it: write a RELEASE-NOTES file, write a dev update, or use --notes with at least 50 chars of real description.

## Why

Release notes were consistently garbage. One-liner --notes flags like "Fix bug" or "Update docs" sailed through on patch releases. The warnings were ignored by both humans and agents. Every release page on GitHub had thin, useless notes that didn't explain what changed or why.

## Also in this release

- wip-repo-init templates renamed from ai/ to templates/ so they ship with npm install (deploy-public.sh was stripping them)
- SKILL.md restart notice after install (hooks need session restart)
- SPEC.md and TECHNICAL.md updated with all 17 tools and LDM OS links
- Branch guard matcher fix (catches Bash + NotebookEdit)
- Forced Git Worktrees and Branch Guard sections added to SKILL.md

## 1.9.27 (2026-03-15)

# Release Notes Quality Gate

**Date:** 2026-03-15

## What changed

wip-release now blocks ALL releases (patch, minor, major) if the release notes are bad. Previously, patch releases only warned. Now they block.

The gate checks:
- Notes must be at least 50 characters
- Notes can't look like a changelog entry ("fix: ...", "add: ...", "update: ...")
- Minor/major still require a file (not --notes flag)

If the gate blocks, it tells you exactly how to fix it: write a RELEASE-NOTES file, write a dev update, or use --notes with at least 50 chars of real description.

## Why

Release notes were consistently garbage. One-liner --notes flags like "Fix bug" or "Update docs" sailed through on patch releases. The warnings were ignored by both humans and agents. Every release page on GitHub had thin, useless notes that didn't explain what changed or why.

## Also in this release

- wip-repo-init templates renamed from ai/ to templates/ so they ship with npm install (deploy-public.sh was stripping them)
- SKILL.md restart notice after install (hooks need session restart)
- SPEC.md and TECHNICAL.md updated with all 17 tools and LDM OS links
- Branch guard matcher fix (catches Bash + NotebookEdit)
- Forced Git Worktrees and Branch Guard sections added to SKILL.md

## 1.9.26 (2026-03-15)

Add restart notice after install/update. Hooks need session restart to take effect.

## 1.9.25 (2026-03-14)

Fix branch guard matcher (catches Bash + NotebookEdit). Add Forced Git Worktrees and Branch Guard sections to SKILL.md. Update SPEC.md and TECHNICAL.md with all 17 tools and LDM OS links.

## 1.9.24 (2026-03-14)

Number tools in dry run and already-installed lists. Dogfood iteration.

## 1.9.23 (2026-03-14)

Force verbatim tool list display. AI must show all 17 tools with descriptions, never summarize.

## 1.9.22 (2026-03-14)

All 17 tools listed with descriptions. New section order: Setup, Infrastructure, Repo Management, License, Release. Conversational prompt.

## 1.9.21 (2026-03-14)

Add Already Installed section with tool descriptions. Dogfood fix.

## 1.9.20 (2026-03-14)

Make root package publishable. npm install -g @wipcomputer/wip-ai-devops-toolbox now installs all 12 CLI tools.

## 1.9.19 (2026-03-14)

Add websiteRepo to .publish-skill.json. Auto-publish SKILL.md to website on release. Fix install prompt URLs to use wip- prefix.

## 1.9.18 (2026-03-14)

Rewrite SKILL.md install flow to use ldm install. Conversational AI-guided pattern matching Memory Crystal.

## 1.9.17 (2026-03-14)

Add wip-branch-guard: PreToolUse hook that blocks all writes on main branch. Resolves repo from file path so it works from any CWD. Forces agents to branch or worktree before editing.

## 1.9.16 (2026-03-14)

Add wip-branch-guard: PreToolUse hook that blocks all writes on main branch. Resolves repo from file path so it works from any CWD. Forces agents to branch or worktree before editing.

## 1.9.15 (2026-03-14)

Fix all 5 root causes of truncated release notes (#121). Add --dry-run to readme-license. Update SKILL.md docs for wip-release and wip-license-guard.

## 1.9.14 (2026-03-14)

Add readme-license command to wip-license-guard. Scans all repos, applies standard license block, removes from sub-tools. License Guard now Stable.

## 1.9.13 (2026-03-14)

Release.

## 1.9.12 (2026-03-13)

Add skill publish to website: after every release, SKILL.md is auto-copied to yoursite.com/install/{name}.txt and deployed. Configured per repo with .publish-skill.json. Non-blocking.

## 1.9.11 (2026-03-13)

wip-install bootstraps LDM OS silently when not on PATH

## 1.9.10 (2026-03-13)

# Release Notes: AI DevOps Toolbox v1.9.10

**Fix: Release notes files on disk always beat --notes flag**

v1.9.9 shipped with a one-liner on the GitHub release instead of the full narrative release notes. The RELEASE-NOTES-v1-9-9.md file was sitting right there on disk, but `--notes="short text"` took priority because the auto-detect only ran when `--notes` was absent.

This is exactly the kind of bug that happens when a rule exists in documentation but not in code. "Write release notes on the branch" is in the Dev Guide. The tool ignored them.

## What changed

### Notes priority is now enforced (highest wins):

1. `--notes-file=path` ... explicit file path (always wins)
2. `RELEASE-NOTES-v{ver}.md` ... in repo root (always wins over `--notes` flag)
3. `ai/dev-updates/YYYY-MM-DD*` ... today's dev update (wins over `--notes` flag if longer)
4. `--notes="text"` ... fallback only. Use for repos without release notes files.

If a RELEASE-NOTES file exists on disk, `--notes` is ignored and a warning is printed:

```
! --notes flag ignored: RELEASE-NOTES-v1-9-10.md takes priority
```

Written notes on disk always take priority over a CLI one-liner. The agent wrote the file. The tool should use it.

## Files changed

```
 tools/wip-release/cli.js | ~40 lines rewritten (notes cascade logic)
```

## Install

```bash
git pull origin main
```

## Attribution

Built by Parker Todd Brooks, Lesa, and Claude Opus 4.6 at WIP.computer.

## 1.9.9 (2026-03-13)

Enforce git worktrees as default workflow. wip-release blocks from worktrees, wip-install auto-adds .claude/worktrees/ to .gitignore, Dev Guide worktree section added.

## 1.9.8 (2026-03-13)

wip-install delegates to ldm install when available

## 1.9.7 (2026-03-13)

# Release Notes: AI DevOps Toolbox v1.9.7

## LDM OS Integration

AI DevOps Toolbox now works with LDM OS when it's available.

### wip-install delegates to ldm install

When the `ldm` CLI exists on PATH, `wip-install` delegates to `ldm install`. LDM OS handles the scaffold, interface detection, and extension deployment. The Toolbox's standalone behavior is preserved as a fallback when `ldm` isn't available.

Supports `--dry-run` and `--json` passthrough to `ldm install`.

### LDM OS tip

After standalone installs, the Toolbox prints a tip: "Run `ldm install` to see more skills you can add."

### Universal Installer link

The "Read more about Universal Installer" link now points to the LDM OS docs page. The Universal Installer engine moved to LDM OS. The Toolbox keeps `wip-install` as an entry point that delegates.

### Part of LDM OS

README includes a "Part of LDM OS" section linking back to the LDM OS repo.

## 1.9.6 (2026-03-12)

# v1.9.6 ... Enforcement Gates

Three fixes that move the release pipeline from "suggestions agents forget" to "gates that block."

---

## syncSkillVersion corrupted quoted versions (#71)

Every release was appending the old version instead of replacing it. SKILL.md went from `"1.9.5"` to `"1.9.5".9.4".9.3".9.2".9.1"` over five releases.

Root cause: the regex `"?\S+?"?` used non-greedy matching. For quoted values, it consumed only part of the string, leaving the rest as trailing garbage.

Fix: replaced with `(?:"[^\n]*|\S+)`. Quoted values now match through end of line. Unquoted values use greedy `\S+`. Also fixed the staleness-check regex to extract clean semver from corrupted strings.

**Files changed:**
- `tools/wip-release/core.mjs` ... `syncSkillVersion()` regex fix
- `SKILL.md` ... repaired corrupted version back to `"1.9.5"`

---

## gh pr merge now always deletes branch (#74)

Every `gh pr merge` call in the codebase now includes `--delete-branch`. Previously, deploy-public.sh had a manual 3-line `gh api -X DELETE` cleanup block. That's gone. The flag handles it.

Also verified every merge uses `--merge` (never squash). Dev Guide updated with the new convention.

**Files changed:**
- `scripts/deploy-public.sh` ... added `--delete-branch`, removed manual cleanup
- `tools/deploy-public/deploy-public.sh` ... same
- `DEV-GUIDE-GENERAL-PUBLIC.md` ... updated merge examples
- `ai/DEV-GUIDE-FOR-WIP-ONLY-PRIVATE.md` ... updated merge rules
- `ai/_trash/DEV-GUIDE-private.md` ... updated
- `ai/_sort/_trash/ai_old/_trash/DEV-GUIDE-private.md` ... updated

---

## wip-release blocks on stale remote branches (#75)

New gate in the release pipeline. Before releasing, wip-release checks for remote branches that are fully merged into main but haven't been cleaned up.

- **Patch:** warns with the list of stale branches (non-blocking)
- **Minor/major:** blocks the release. Clean up first.
- **`--skip-stale-check`:** override flag for emergencies

Follows the existing gate pattern: fetches with `--prune`, filters out `origin/main`, `origin/HEAD`, and `--merged-` branches. Fails gracefully if git commands error.

**Files changed:**
- `tools/wip-release/core.mjs` ... `checkStaleBranches()` function, integrated as gate 0.8
- `tools/wip-release/cli.js` ... `--skip-stale-check` flag, help text

---

## Diffstat

```
 10 files changed, 102 insertions(+), 21 deletions(-)
```

## Install

```bash
npm install -g @wipcomputer/wip-ai-devops-toolbox
```

Or update an existing install:
```bash
wip-install wipcomputer/wip-ai-devops-toolbox
```

---

Built by Parker Todd Brooks, Lēsa (OpenClaw, Claude Opus 4.6), Claude Code (Claude Opus 4.6).

## 1.9.5 (2026-03-12)

wip-release: bump sub-tool versions in toolbox repos. Fixes #132.

## 1.9.4 (2026-03-12)

wip-install: detect and migrate existing installs under different names. Fixes #128.

## 1.9.3 (2026-03-12)

Fix: ensure bin executability on installer skip path. Fixes wip-license-guard, wip-license-hook, wip-repo-init, wip-readme-format permission denied after reinstall.

## 1.9.2 (2026-03-12)

# v1.9.2: Distribution Pipeline Fix

The entire distribution pipeline was broken. Tools built but never reached users. 8 of 13 tools weren't on npm. ClawHub publish only shipped the root SKILL.md. deploy-public never ran npm publish. Errors were silent.

This release fixes all of it.

## What changed

### Install fixes (#96, #110)
- CLI binaries now have correct executable permissions (git +x on all bin entry files)
- wip-license-hook dist/ committed to repo (TypeScript build output was gitignored)
- Installer auto-detects TypeScript projects and runs build if dist/ missing
- chmod +x safety net after every npm install -g
- SSH fallback when HTTPS clone fails (private repos)

### SKILL.md spec compliance (#107, #108)
- All 12 SKILL.md files conform to agentskills.io spec
- name field: lowercase-hyphen format matching directory name
- Display names in metadata.display-name
- version, homepage, author in metadata block
- license: MIT on all files
- metadata.openclaw blocks with install instructions and emoji
- New SKILL.md created for wip-license-guard (was missing)

### Distribution pipeline (#97, #100, #104)
- ClawHub publish now iterates all sub-tool SKILL.md files, not just root
- detectSkillSlug reads the name field from SKILL.md frontmatter
- deploy-public.sh runs npm publish from the public clone after code sync
- Handles both single repos and toolbox repos (iterates tools/*)
- Distribution summary at end of release: shows all targets with pass/fail
- syncSkillVersion handles quoted version strings in new metadata format

## Install

```bash
npm install -g @wipcomputer/wip-ai-devops-toolbox
wip-install wipcomputer/wip-ai-devops-toolbox
```

Built by Parker Todd Brooks, Lesa (OpenClaw, Claude Opus 4.6), Claude Code (Claude Opus 4.6).

## 1.9.1 (2026-03-11)

# v1.9.1: Release gates ... product docs and release notes quality enforcement

Agents read the Dev Guide, say "got it," and then release with garbage one-liner notes anyway. Documentation doesn't change behavior. Tools do. This release adds two new gates to `wip-release` that block bad releases before they happen.

## Product docs gate

Every PR is supposed to include updated product docs: a dev update, roadmap changes, and readme-first updates. This was documented in the Dev Guide as a manual checklist. Nobody followed it.

`wip-release` now checks three things before publishing:

1. **Dev update exists.** Looks in `ai/dev-updates/` for a file from the last 3 days. If you did work worth releasing, you should have written about it.
2. **Roadmap was updated.** Checks `ai/product/plans-prds/roadmap.md` via `git diff` against the last tag. If the roadmap doesn't reflect what just shipped, it's stale.
3. **Readme-first was updated.** Same check on `ai/product/readme-first-product.md`. The product bible should always describe what's actually built.

Repos without an `ai/` directory are skipped silently. This only applies to repos that have adopted the `ai/` folder standard.

For **patch** releases: warns but doesn't block. Hotfixes shouldn't be held up by docs.
For **minor/major** releases: blocks the release. You can't ship a meaningful feature with stale product docs.

`--skip-product-check` overrides for exceptional cases.

## Release notes quality gate

On 2026-03-11, the other CC session released memory-crystal v0.7.4. It read the Dev Guide (which now explicitly says "write a RELEASE-NOTES file on the branch"). It said it understood. Then it ran `wip-release patch --notes="MCP fix and agent ID config"` and published a one-liner to GitHub. The old `warnIfNotesAreThin()` function printed a warning to console. The agent ignored it.

The root cause was architectural, not behavioral. The warning ran at step 8 of the pipeline, AFTER the version was already bumped, committed, tagged, and pushed. By the time the warning appeared, the damage was done. And it was a warning, not a gate. Agents don't read warnings.

The fix:
- `checkReleaseNotes()` replaces `warnIfNotesAreThin()`. It runs before the version bump, not after.
- The CLI now tracks `notesSource`: where the notes came from (`file`, `dev-update`, `flag`, or `none`).
- For minor/major releases: if notes came from a bare `--notes` flag instead of a `RELEASE-NOTES-v{version}.md` file, the release is **blocked**. The agent gets explicit instructions: "Write RELEASE-NOTES-v{version}.md (dashes not dots), commit it, then release."
- For patch releases: warns if notes are short, but doesn't block.

## Both gates follow the same pattern

The existing license compliance gate (step 0) checks `.license-guard.json` and blocks if licensing is wrong. The new product docs gate (step 0.5) and release notes gate (step 0.75) work the same way: check early, block before any changes, show status in `--dry-run`, give clear instructions on how to fix it.

The MCP server was also updated with `skipProductCheck` and `notesSource` passthrough so agents calling wip-release via MCP get the same enforcement.

## 1.9.0 (2026-03-11)

README Formatter (section-based staging + deploy), Repo Init (ai/ directory scaffolding), Dev Guide overhaul with release notes workflow

## 1.8.2 (2026-03-11)

# v1.8.2: Clean up release notes after release

RELEASE-NOTES files were piling up in the repo root. `wip-release` consumed them for the GitHub release and CHANGELOG but never cleaned up.

Now after consuming the file, `wip-release` moves all `RELEASE-NOTES-v*.md` files to `_trash/` as part of the version bump commit. We never delete anything.

`deploy-public.sh` also now excludes `_trash/` so these files stay private.

## 1.8.1 (2026-03-11)

# v1.8.1: Fix CLI install when package name changed

When a tool's npm package gets renamed but the binary name stays the same, `npm install -g` fails with EEXIST. The stale symlink from the old package blocks the new one.

The installer now detects this: if the binary is a symlink pointing to a different package, it removes the stale link and retries. Only affects symlinks, only when the target doesn't match the package being installed.

Found on `wip-license-hook` (renamed from `@wipcomputer/license-hook` to `@wipcomputer/wip-license-hook`).

## 1.8.0 (2026-03-11)

# v1.8.0: Fix CC Hook duplicates, add GitHub Issues convention

## CC Hook duplicate detection fix

`wip-install` was adding duplicate PreToolUse hooks to `~/.claude/settings.json` every time it ran. After a few installs, there were 8 hooks when there should have been 2. The duplicates pointed to repo clones and `/tmp/` paths, violating the "never run tools from repo clones" rule.

The root cause: duplicate detection compared exact command strings. The same `guard.mjs` installed from different paths produced different strings, so each install added another entry.

The fix:
- Match existing hooks by tool name in the path, not exact command string
- Always prefer `~/.ldm/extensions/<tool>/guard.mjs` over source or temp paths
- If a hook for the same tool exists at a different path, update it instead of adding a duplicate

## GitHub Issues convention added to Dev Guide

We were tracking work in `ai/todos/` markdown files. Items got lost. GitHub Issues gives us tracking, cross-referencing, and visibility across agents.

Added to the public Dev Guide:
- When to use GitHub Issues vs `ai/todos/`
- Filing convention: `filed-by:<agent-id>` labels and attribution lines
- Public vs private issue routing: public issues are the front door, private issues are the workshop
- Agent ID naming convention: `[platform]-[agent]-[machine]`

Added to the private Dev Guide:
- `filed-by:cc-mini` (blue) and `filed-by:oc-lesa-mini` (purple) label details
- Org-wide deployment commands
- Incident note: Memory Crystal agent ID drift

Both labels deployed across all wipcomputer repos.

## 1.7.9 (2026-03-11)

Add GitHub Issues convention and filed-by workflow to the Dev Guide.

We've been tracking work in ai/todos/ markdown files. Items get lost. GitHub Issues gives us tracking, cross-referencing, and visibility across all agents. This release documents the full convention.

**Public Dev Guide (DEV-GUIDE-GENERAL-PUBLIC.md):**
- New "GitHub Issues" section: when to use issues vs ai/todos/, filing convention with attribution lines and filed-by labels, public vs private issue routing workflow
- Agent ID naming convention: [platform]-[agent]-[machine] format documented with examples
- Public/private issue bridge: public issues are the front door (users), private issues are the workshop (team), releases connect them

**Private Dev Guide (ai/DEV-GUIDE-FOR-WIP-ONLY-PRIVATE.md):**
- filed-by label details: cc-mini (blue), oc-lesa-mini (purple), deployed org-wide
- Commands for adding labels to new agents or repos
- Incident note: Memory Crystal agent ID drift (4 IDs instead of 2), manual merge of 141K chunks, root cause and fix tracked in memory-crystal-private#33

**Org-wide:** filed-by:cc-mini and filed-by:oc-lesa-mini labels created on all wipcomputer repos.

## 1.7.8 (2026-03-10)

# Dev Update: Smart Install + Platform Compatibility

**Date:** 2026-03-10 22:40 PST
**Author:** Claude Code (cc-mini)
**Version:** v1.7.8 (pending)
**Branches:** cc-mini/smart-install, cc-mini/platform-compat-v2

## Smart Install (wip-install)

Parker's feedback: "I want to make sure we're not going to replace stuff unless we need to. It should be smart enough to know I have this extension installed, and it's the same one."

The Universal Installer was doing blind `rm -rf` and re-copy on every run. Now it checks versions first:

- **Extensions (LDM + OpenClaw):** Reads `package.json` version from the installed extension. If it matches the source version, skip. If different, upgrade. If missing, fresh install. Dry-run shows "would upgrade v1.2.3 -> v1.2.4" vs "would deploy v1.2.4" vs "already at v1.2.4".
- **CLI:** Checks `npm list -g` for the installed version. Same version = skip.
- **MCP:** Checks if already registered at the same server path. Same path = skip.
- **CC Hooks:** Already had duplicate detection (unchanged).

No more destroying things that don't need updating.

## Platform Compatibility (SKILL.md)

Parker's feedback after testing with Grok: "Grok said 'I'll run wip-install' but it literally cannot. It's hallucinating capabilities."

First version listed platforms as "first-class / MCP-compatible / not compatible." Parker corrected: "We don't need to say 'not compatible' because Claude iOS can install stuff now. We just need to be clear about what the tool needs."

Rewrote to capability requirements:

| Interface | Requires |
|-----------|----------|
| CLI | Shell access |
| MCP Server | MCP client support |
| CC Hook | Claude Code CLI with hooks |
| OpenClaw Plugin | OpenClaw runtime |
| Skill | Ability to read this file |
| Module | Node.js import |

Key instruction to agents: "Check which capabilities you have and match them to the table. Do not claim you can run commands you cannot execute."

This is future-proof. When a platform adds MCP or shell access, the SKILL.md doesn't need updating. The agent assesses itself.

## Cross-Platform Testing Results

Three AIs read the same SKILL.md onboarding prompt:

- **Claude Code (another instance):** Read it, explained all tools correctly, offered dry-run first. Responded with "HOLY SHIT!!!" (impressed by the tooling).
- **Lesa (OpenClaw, Claude Opus 4.6):** Perfect breakdown. Every tool categorized correctly. Called out the auto-detect dev updates feature specifically. Offered dry-run first.
- **Grok (xAI):** Initially tried to roleplay as Lesa/Claude Code (read the attribution line and adopted the persona). When corrected, gave accurate breakdown. But claimed it would run `wip-install` when it cannot. This exposed the need for the Platform Compatibility section.

The SKILL.md is working. Three different AIs, three different platforms, all understood the toolbox correctly from one file.

## 1.7.7 (2026-03-10)

# Dev Update: SKILL.md as the Real Interface

**Date:** 2026-03-10 22:10 PST
**Author:** Claude Code (cc-mini)
**Version:** v1.7.4
**Branch:** cc-mini/skill-installer-details

## The Insight

Parker said it plainly: "We're not doing READMEs anymore. This is not for humans."

The human interface is the AI. The AI's interface is the SKILL.md. If the skill doesn't contain everything needed to operate, the AI guesses. And it guesses wrong.

We proved this earlier in the session. Lesa read the toolbox and miscategorized Universal Installer under "Repo Management" because the SKILL.md had no category structure (fixed in v1.7.3). But even after categories, she still couldn't explain what the tools actually do operationally, because the SKILL.md was still a half-README with links and one-liners.

## What We Researched

Parker pointed us to agentcard.sh/agent.txt as a reference. We researched three AI documentation conventions:

1. **llms.txt** (llmstxt.org) ... a directory of links. Points to docs but doesn't contain them. An AI still has to fetch and read multiple files. Good for discovery, not for operation.

2. **agent.txt / AgentCard** (agentcard.sh) ... self-contained operational manual. Everything in one file. An AI reads it and knows how to interact with the service. Closer to what we need, but designed for describing APIs/services, not developer tools.

3. **SKILL.md** (ours) ... YAML frontmatter for machine parsing, then full operational detail. Designed specifically to teach an AI how to use developer tools. Not a pointer to docs. Not a summary. The complete manual.

We took the best from each: the discoverability mindset of llms.txt, the self-contained philosophy of agent.txt, and built SKILL.md as the standard for AI-native developer tool documentation.

## What Changed in v1.7.4

The SKILL.md went from ~140 lines (descriptions + links) to ~475 lines (complete operational manual).

Every one of the 11 tools now has:
- Complete commands with all flags and options
- Step-by-step "what happens when you run it" sequences
- Exact file paths (where it reads, where it writes)
- Safety notes (what it deletes, what it overwrites, what to watch for)
- How it works across different interfaces (CC Hook, OpenClaw Plugin, MCP server)

### Specific additions worth noting:

**Universal Installer** got a full deployment table showing what each of the 6 interfaces does and where it writes. We read the install.js source code and documented that it does `rm -rf` on existing extension directories before copying. That's critical safety information an AI needs before running it.

**Release Pipeline** got all 13 steps documented (step 0: license gate through step 12: branch prune). Every flag, every file it touches, every decision point.

**Identity File Protection** got the exact list of protected files and the definition of "destructive" (replacing >50% of content). Also documented the difference between how the CC Hook and OpenClaw Plugin work.

**MCP section** got complete tool function names for all MCP-enabled tools, so an AI can add them to .mcp.json without guessing.

## The "Teach Your AI" Framing

Parker's directive on the README: the first tool (Universal Installer) says "Teaches your AI to..." explicitly. The rest infer the pattern. You don't need to say "teaches" 11 times. The frame is set once, and a reader (human or AI) carries it forward.

Universal Installer's description changed from a generic "installs tools" to: "Teaches your AI to take anything you build and make it work across every AI interface. You write code in any language. This tool turns it into a CLI, MCP Server, OpenClaw Plugin, Skill, and Claude Code Hook."

## Interface Coverage Table Iterations

We went through several iterations on the table format:

1. **Separate tables per category** ... Parker: "too hard on the eyes"
2. **Single table, bold category divider rows** ... better, but needed numbering
3. **Added numbers 1-11 in a # column** ... Parker liked it
4. **Tried moving categories into the # column, removing numbers** ... Parker: "looks worse, change it back"
5. **Final: numbers + category divider rows, no dashes in empty cells** ... clean and scannable

The lesson: don't overthink table formatting. Numbers give anchoring. Category rows give structure. Empty cells are cleaner than dashes.

## The Standard Going Forward

This is how we think SKILL.md files should be written for any tool in the toolbox:

1. YAML frontmatter with name, version, interface list
2. One-paragraph description of what the tool teaches
3. Complete command reference with all flags
4. Step-by-step operational detail (what happens when you run it)
5. File paths (reads from, writes to)
6. Safety notes (destructive operations, prerequisites)
7. Interface-specific behavior (how it works as CLI vs Hook vs MCP vs Plugin)

The SKILL.md is the source of truth. READMEs exist for humans browsing GitHub. But the AI reads the SKILL.md, and the SKILL.md must be complete.

## Release Notes Standard

We also established that release notes on GitHub should tell the story. Not just "bumped version" or a one-liner from `--notes`. The v1.7.4 release notes explain the thinking, the research, and what changed. This is how releases should read going forward.

Earlier releases (v1.7.1, v1.7.2) shipped with thin notes and we had to go back and manually update them via `gh release edit`. The tool (wip-release) uses the `--notes` flag, which encourages one-liners. For significant releases, we should write RELEASE-NOTES files on the branch and have the tool pick them up.

## Files Changed

- `SKILL.md` ... complete rewrite (140 -> 475 lines)
- `README.md` ... Interface Coverage table: numbered, category dividers, no dashes
- `ai/feedback/2026-03-10--gpt--v1.7.1-readme-review.md` ... GPT rated the README 9.6/10

## wip-release: Auto-Detect Dev Updates as Release Notes

Parker's feedback: "The release notes should be automated. I shouldn't have to keep telling you to do this."

We updated `wip-release` to auto-detect release notes from `ai/dev-updates/`. The priority order:

1. `--notes-file=path` (explicit)
2. `RELEASE-NOTES-v{ver}.md` in repo root
3. `ai/dev-updates/YYYY-MM-DD*` (today's dev update files, most recent first)
4. `--notes="one-liner"` (fallback, but dev updates win if they have more content)

This means: write dev updates as you work (which we already do). When you run `wip-release`, it finds today's dev update and uses it as the full release notes. No more thin one-liners on GitHub releases. No more "this week's sauce, come on, man."

## What's Next

- Consider making the SKILL.md standard a section in the Dev Guide
- Operational guide for agent identities (Parker mentioned needing this)

## 1.7.6 (2026-03-10)

README: onboarding prompt now does dry-run install first so users see what changes before committing

## 1.7.5 (2026-03-10)

# Dev Update: SKILL.md as the Real Interface

**Date:** 2026-03-10 22:10 PST
**Author:** Claude Code (cc-mini)
**Version:** v1.7.4
**Branch:** cc-mini/skill-installer-details

## The Insight

Parker said it plainly: "We're not doing READMEs anymore. This is not for humans."

The human interface is the AI. The AI's interface is the SKILL.md. If the skill doesn't contain everything needed to operate, the AI guesses. And it guesses wrong.

We proved this earlier in the session. Lesa read the toolbox and miscategorized Universal Installer under "Repo Management" because the SKILL.md had no category structure (fixed in v1.7.3). But even after categories, she still couldn't explain what the tools actually do operationally, because the SKILL.md was still a half-README with links and one-liners.

## What We Researched

Parker pointed us to agentcard.sh/agent.txt as a reference. We researched three AI documentation conventions:

1. **llms.txt** (llmstxt.org) ... a directory of links. Points to docs but doesn't contain them. An AI still has to fetch and read multiple files. Good for discovery, not for operation.

2. **agent.txt / AgentCard** (agentcard.sh) ... self-contained operational manual. Everything in one file. An AI reads it and knows how to interact with the service. Closer to what we need, but designed for describing APIs/services, not developer tools.

3. **SKILL.md** (ours) ... YAML frontmatter for machine parsing, then full operational detail. Designed specifically to teach an AI how to use developer tools. Not a pointer to docs. Not a summary. The complete manual.

We took the best from each: the discoverability mindset of llms.txt, the self-contained philosophy of agent.txt, and built SKILL.md as the standard for AI-native developer tool documentation.

## What Changed in v1.7.4

The SKILL.md went from ~140 lines (descriptions + links) to ~475 lines (complete operational manual).

Every one of the 11 tools now has:
- Complete commands with all flags and options
- Step-by-step "what happens when you run it" sequences
- Exact file paths (where it reads, where it writes)
- Safety notes (what it deletes, what it overwrites, what to watch for)
- How it works across different interfaces (CC Hook, OpenClaw Plugin, MCP server)

### Specific additions worth noting:

**Universal Installer** got a full deployment table showing what each of the 6 interfaces does and where it writes. We read the install.js source code and documented that it does `rm -rf` on existing extension directories before copying. That's critical safety information an AI needs before running it.

**Release Pipeline** got all 13 steps documented (step 0: license gate through step 12: branch prune). Every flag, every file it touches, every decision point.

**Identity File Protection** got the exact list of protected files and the definition of "destructive" (replacing >50% of content). Also documented the difference between how the CC Hook and OpenClaw Plugin work.

**MCP section** got complete tool function names for all MCP-enabled tools, so an AI can add them to .mcp.json without guessing.

## The "Teach Your AI" Framing

Parker's directive on the README: the first tool (Universal Installer) says "Teaches your AI to..." explicitly. The rest infer the pattern. You don't need to say "teaches" 11 times. The frame is set once, and a reader (human or AI) carries it forward.

Universal Installer's description changed from a generic "installs tools" to: "Teaches your AI to take anything you build and make it work across every AI interface. You write code in any language. This tool turns it into a CLI, MCP Server, OpenClaw Plugin, Skill, and Claude Code Hook."

## Interface Coverage Table Iterations

We went through several iterations on the table format:

1. **Separate tables per category** ... Parker: "too hard on the eyes"
2. **Single table, bold category divider rows** ... better, but needed numbering
3. **Added numbers 1-11 in a # column** ... Parker liked it
4. **Tried moving categories into the # column, removing numbers** ... Parker: "looks worse, change it back"
5. **Final: numbers + category divider rows, no dashes in empty cells** ... clean and scannable

The lesson: don't overthink table formatting. Numbers give anchoring. Category rows give structure. Empty cells are cleaner than dashes.

## The Standard Going Forward

This is how we think SKILL.md files should be written for any tool in the toolbox:

1. YAML frontmatter with name, version, interface list
2. One-paragraph description of what the tool teaches
3. Complete command reference with all flags
4. Step-by-step operational detail (what happens when you run it)
5. File paths (reads from, writes to)
6. Safety notes (destructive operations, prerequisites)
7. Interface-specific behavior (how it works as CLI vs Hook vs MCP vs Plugin)

The SKILL.md is the source of truth. READMEs exist for humans browsing GitHub. But the AI reads the SKILL.md, and the SKILL.md must be complete.

## Release Notes Standard

We also established that release notes on GitHub should tell the story. Not just "bumped version" or a one-liner from `--notes`. The v1.7.4 release notes explain the thinking, the research, and what changed. This is how releases should read going forward.

Earlier releases (v1.7.1, v1.7.2) shipped with thin notes and we had to go back and manually update them via `gh release edit`. The tool (wip-release) uses the `--notes` flag, which encourages one-liners. For significant releases, we should write RELEASE-NOTES files on the branch and have the tool pick them up.

## Files Changed

- `SKILL.md` ... complete rewrite (140 -> 475 lines)
- `README.md` ... Interface Coverage table: numbered, category dividers, no dashes
- `ai/feedback/2026-03-10--gpt--v1.7.1-readme-review.md` ... GPT rated the README 9.6/10

## wip-release: Auto-Detect Dev Updates as Release Notes

Parker's feedback: "The release notes should be automated. I shouldn't have to keep telling you to do this."

We updated `wip-release` to auto-detect release notes from `ai/dev-updates/`. The priority order:

1. `--notes-file=path` (explicit)
2. `RELEASE-NOTES-v{ver}.md` in repo root
3. `ai/dev-updates/YYYY-MM-DD*` (today's dev update files, most recent first)
4. `--notes="one-liner"` (fallback, but dev updates win if they have more content)

This means: write dev updates as you work (which we already do). When you run `wip-release`, it finds today's dev update and uses it as the full release notes. No more thin one-liners on GitHub releases. No more "this week's sauce, come on, man."

## What's Next

- Consider making the SKILL.md standard a section in the Dev Guide
- Operational guide for agent identities (Parker mentioned needing this)

## 1.7.4 (2026-03-10)

SKILL.md full operational rewrite for AI agents. Every tool now has complete commands, flags, step-by-step behavior, file paths, and safety notes. Interface Coverage table cleaned up: numbered tools, category dividers, no dashes.

## 1.7.3 (2026-03-10)

Add category structure to SKILL.md matching README. Prevents AI from miscategorizing tools.

## 1.7.2 (2026-03-10)

Reframe Universal Installer description, fix tense, update SKILL.md intro framing

## 1.7.1 (2026-03-10)

Reframe tool descriptions with teach your AI pattern, file GPT and Grok feedback on v1.7.0

## 1.7.0 (2026-03-10)

## v1.7.0: Renamed to AI DevOps Toolbox, CLA, License Enforcement, Branch Prune, README Polish

This release renames the repo, adds contributor governance, makes licensing intent unmistakable, automates branch cleanup, and tightens the README based on a second round of external feedback.

The repo is now **AI DevOps Toolbox** (`wip-ai-devops-toolbox`). The name change reflects what this actually is: not just DevOps scripts, but AI-native development infrastructure.

Includes work from PRs #53, #54.

---

### Repo Rename: AI DevOps Toolbox

**What we did:** Renamed from "DevOps Toolbox" (`wip-devops-toolbox`) to "AI DevOps Toolbox" (`wip-ai-devops-toolbox`).

**Why:** The old name undersold what this is. "DevOps Toolbox" sounds like scripts. This is an interface architecture, an agent tool ecosystem, and a workflow framework for AI-assisted development. The name should say that.

**What changed:**
- GitHub repos renamed: `wip-ai-devops-toolbox-private` and `wip-ai-devops-toolbox`
- All internal references updated: README, TECHNICAL.md, SKILL.md, package.json, cross-repo references

---

### Contributor License Agreement (CLA)

**What we did:** Added `CLA.md` at the repo root and referenced it in the README License section.

**Why:** Without a CLA, contributors who submit PRs own their code. AGPL means we can't relicense their contributions commercially. We need contributors to grant WIP Computer, Inc. the right to use their contributions under any license, including commercial. This is standard open source governance. Apache, Google, Meta, and Anthropic all use similar agreements.

**How it works:** By submitting a PR, you agree to the CLA. Contributors keep their own copyright but grant WIP Computer, Inc. a broad license. Plain-English, no lawyer needed to understand it.

**New files:**
- `CLA.md` ... the agreement itself

---

### Licensing Clarity

**What we did:** Made the licensing intent unmistakable with two new sentences.

**Why:** The dual MIT+AGPLv3 license is technically correct, but people still ask "can I use this?" The answer needed to be obvious: yes, use the tools however you want. The only thing that requires a commercial license is taking the tools themselves and reselling them.

**What changed:**
- Added "Dual-license model designed to keep tools free while preventing commercial resellers" above the license block
- Added "Using these tools to build your own software is fine. Reselling the tools themselves is what requires a commercial license" to the "Can I use this?" section
- Updated `generateReadmeBlock()` in `tools/wip-license-guard/core.mjs` so every future repo gets the same wording automatically

---

### Branch Prune Automation

**What we did:** Built automatic branch cleanup into both `post-merge-rename.sh` and `wip-release`.

**Why:** Merged branches pile up on the remote. Before this release, the private repo had 30+ stale branches. The post-merge-rename script renamed them with `--merged-YYYY-MM-DD` but never cleaned up old ones. Manually deleting branches is a waste of time. We built these tools so we don't have to keep doing things manually.

**How it works:**

`post-merge-rename.sh --prune` does three things:
1. Renames any merged branches that don't have the `--merged` suffix yet
2. For each developer prefix (`cc-mini/`, `mini/`, `lesa-mini/`, etc.), keeps the last 3 `--merged` branches and deletes the rest from the remote
3. Finds stale branches that are fully merged into main but were never renamed, and deletes them

`wip-release` now runs prune automatically as step 11 after every release. No manual cleanup needed.

Rules: never deletes `main`, never deletes the current working branch, always keeps the last 3 per developer. `--dry-run` previews what would be deleted.

**Files changed:**
- `scripts/post-merge-rename.sh` ... new `--prune` flag, stale branch detection, keep-last-3 logic
- `tools/wip-release/core.mjs` ... step 11: automatic prune after every release

---

### License Enforcement Automation

**What we did:** Made license compliance automatic across three layers: CC Hook, wip-release gate, and one-command repo setup.

**Why:** `wip-license-guard` existed but was manual. Nobody remembered to run it. The dual-license + CLA standard from this release needs to be enforced, not just documented.

**How it works:**

**CC Hook** (`tools/wip-license-guard/hook.mjs`): PreToolUse hook for Claude Code. Intercepts `git commit` and `git push` commands. Checks LICENSE file, copyright, CLA.md, and README license section. Blocks if any check fails. Same pattern as `wip-file-guard`.

**wip-release gate** (step 0): Before bumping anything, wip-release checks license compliance. If `.license-guard.json` exists and any check fails, the release aborts with a clear message. No bad releases ship.

**`--from-standard` flag**: `wip-license-guard init --from-standard` applies WIP Computer defaults without prompting. Generates `.license-guard.json`, `LICENSE` (dual MIT+AGPLv3), and `CLA.md` in one command. For new repos, this is all you need.

**Files changed:**
- `tools/wip-license-guard/hook.mjs` ... new CC Hook (PreToolUse, blocks git commit/push)
- `tools/wip-license-guard/cli.mjs` ... `--from-standard` flag, CLA.md generation, CLA check in audit
- `tools/wip-release/core.mjs` ... step 0: license compliance gate

---

### README Polish (GPT Feedback Round 2)

**What we did:** Three targeted improvements based on GPT's review of v1.6.0.

**Karpathy quote shortened.** The full two-paragraph quote was too heavy for the README. Compressed to one line: *As Andrej Karpathy said: "Apps are for people. Tools are for LLMs, and increasingly, LLMs are the ones using software."* with a source link. Same message, doesn't interrupt the flow.

**One-line "why" on every feature.** Each tool now leads with the problem it solves before describing what it does:
- "AI agents forget release steps. This makes releases one command."
- "Dependencies change licenses without telling you. This catches it."
- "AI agents overwrite identity files by accident. This stops them."
- "Repos end up everywhere. This snaps them back to where they belong."

**Feedback filed:**
- `ai/feedback/2026-03-10--gpt--v1.6.0-readme-review.md`
- `ai/feedback/2026-03-10--grok--v1.6.0-summary.md`

---

### Install

```bash
npm install -g @wipcomputer/universal-installer
wip-install wipcomputer/wip-ai-devops-toolbox
```

Or update your local clone:
```bash
git pull origin main
```

---

Built by Parker Todd Brooks, Lēsa (OpenClaw, Claude Opus 4.6), Claude Code (Claude Opus 4.6).

## 1.6.0 (2026-03-10)

## v1.6.0: README Rewrite, Dual Licensing, License Guard, Release Notes Standard

Four systems that change how DevOps Toolbox presents itself, protects its licensing, and ships releases. The README is now for humans. Licensing is enforceable. Release notes tell a story.

This release spans PRs #46 through #50 and represents a complete rethink of how we present the toolbox, how we protect its licensing, and how we communicate what each release actually means.

---

### PR #46: License Format Standard

**What we did:** Rewrote the license section across the README and private Dev Guide to use a clear, scannable format that signals both openness and commercial intent.

**Why:** The old license section just said "MIT" in a badge. That's technically correct but it doesn't tell you the full story. We moved to dual licensing (MIT + AGPLv3) and needed a format that makes the distinction immediately clear: use it freely for personal work, need a commercial license if you're bundling it into something you sell.

**What changed:**
- License section switched to a code block format for readability: MIT for all CLI tools, MCP servers, skills, and hooks. AGPLv3 for commercial redistribution, marketplace listings, or bundling into paid services.
- Added "Commercial licenses available" as a one-line signal that this is a real product, not just an open source side project.
- AGPL renamed to AGPLv3 throughout for version specificity. Grok's feedback confirmed this matters for clarity.
- Private Dev Guide (`ai/DEV-GUIDE-private.md`) updated with the licensing standard so every repo going forward follows the same format.
- Fixed "Claude Code CLI" to "Claude Code" in attribution across all files.

**Commits:** `Update license section formatting for readability`, `License section: code block with Grok-style wording`, `License: personal vs commercial distinction, add standard to dev guide`, `License: AGPL -> AGPLv3 for version specificity`

---

### PR #47: LICENSE Files Across All Tools

**What we did:** Updated the actual LICENSE file in the root and all 10 sub-tool directories to dual MIT + AGPLv3.

**Why:** PR #46 changed how we talk about the license. This PR changed the legal documents themselves. Every sub-tool had its own LICENSE file that still said plain MIT. They all needed to match the new dual-license standard, and they needed to match each other exactly.

**What changed:**
- Root `LICENSE` rewritten to dual format. Section 1: MIT (full text). Section 2: GNU Affero General Public License v3.0 (commercial and cloud use). Starts with "Dual License: MIT + AGPLv3" so GitHub's license detection picks it up correctly.
- All 10 `tools/*/LICENSE` files updated to identical dual-license text with correct copyright holder (WIP Computer, Inc.).
- Bottom line on every LICENSE: "AGPLv3 for personal use is free. Commercial licenses available."

**Commits:** `LICENSE files: dual MIT+AGPLv3 on root and all sub-tools`

---

### PR #48: wip-license-guard (New Tool)

**What we did:** Built a new tool that enforces copyright, license format, and README structure across the toolbox.

**Why:** With 10 sub-tools, each needing its own LICENSE file, and a README standard that separates human content from technical content, manual enforcement doesn't scale. We needed a tool that catches drift before it ships. The tool also enforces the README standard from the session's feedback work: no install commands in the README (those go in TECHNICAL.md), no MCP config blocks, no Quick Start sections.

**How it works:**
- Interactive first-run (`wip-license-guard init`) asks for copyright holder, license type (MIT, AGPLv3, or dual MIT+AGPL), year, and attribution. Saves config to `.license-guard.json`.
- `wip-license-guard check` audits the repo against saved config. Checks LICENSE existence, copyright match, AGPLv3 terms (if dual-license), README license section, README structure.
- `wip-license-guard check --fix` auto-repairs: generates missing LICENSE files, updates wrong copyright, creates dual-license text.
- Toolbox-aware: automatically walks every `tools/` subdirectory and checks each sub-tool's LICENSE file.
- README structure standard enforcement: warns if README contains Quick Start sections, `npm install -g` commands, MCP config blocks, or Architecture/API/Config headings that belong in TECHNICAL.md.
- All 14 checks pass on this repo.

**New files:**
- `tools/wip-license-guard/cli.mjs` (268 lines) ... CLI entry point. Commands: `init`, `check`, `check --fix`, `help`.
- `tools/wip-license-guard/core.mjs` ... `generateLicense()` produces MIT, AGPL, or dual MIT+AGPLv3 LICENSE text. `generateReadmeBlock()` produces the README license section.
- `.license-guard.json` ... config: copyright "WIP Computer, Inc.", license "MIT+AGPL", year 2026.

**Interfaces:** CLI, Module. Beta stability.

**Commits:** `Add wip-license-guard tool and .license-guard.json config`

---

### PR #49: SKILL.md v1.5.1

**What we did:** Updated the skill documentation that AI agents read when you say "read the SKILL.md."

**Why:** The SKILL.md was stuck at v1.4.0. It didn't include wip-license-guard (new in this release), didn't have the interface coverage matrix, and used incorrect tool names. When someone tells their AI to read the SKILL.md, it needs to be current and accurate. Stale skill docs mean the AI gives wrong answers about what the tools can do.

**What changed:**
- Version bumped from v1.4.0 to v1.5.1.
- Added interfaces column to tool table: CLI, Module, MCP, OpenClaw, Skill, CC Hook for every tool.
- Added wip-license-guard to the tool list.
- Fixed tool names: `deploy-public` (not `deploy-public.sh`), `post-merge-rename` (not `post-merge-rename.sh`).
- Added "Talk to Your Tools" section with concrete MCP prompts: "Scan all dependencies for license changes" calls `license_scan`. "Check if memory-crystal can go public" calls `repo_permissions_check`. Etc.
- Added license section matching the new README format.
- Updated frontmatter description and capabilities.
- Added SKILL.md staleness warning to wip-release: warns when SKILL.md version falls more than a patch behind the release version, so this can't happen again silently.

**Commits:** `SKILL.md: update to v1.5.1 with full tool table and interfaces`

---

### PR #50: README Rewrite + Release Notes Standard

**What we did:** Rewrote the entire README based on external feedback, and upgraded the release pipeline to enforce narrative release notes.

**Why:** External feedback from Grok and GPT confirmed what we suspected: the README was developer-brain. Install commands, MCP tool mappings, and Quick Start sections front and center. That's what developers write for themselves. It's not what someone landing on the repo needs to see. They want to know: what does this do for me?

The release notes problem came up during this same work. Every release was producing commit lists instead of stories. Parker had to manually rewrite the notes every time. That needed to be fixed at the tooling level.

**README changes:**

The README now follows a strict standard: tagline, "Teach Your AI to Dev" prompt block, features with stability tags, interface coverage matrix, and license. No install commands. No technical implementation details.

- **Removed Quick Start section.** Install commands belong in TECHNICAL.md, not the README. Added a guard in wip-license-guard to catch `npm install -g` commands and Quick Start headings in any README going forward.
- **Removed "Talk to Your Tools" MCP examples.** These are for AIs, not humans. Moved to SKILL.md where they belong.
- **Added Karpathy quote.** The sensor/actuator framing from Andrej Karpathy anchors the Features section. Both paragraphs, "Andrej Karpathy put it clearly:" intro, Source link. This is the future of software: not apps, tools.
- **Added Interface Coverage matrix.** Single table showing all 10 tools and their six possible interfaces. At a glance you can see what ships as CLI, Module, MCP, OpenClaw, Skill, or CC Hook.
- **Added "Can I use this?" section.** Plain-English licensing examples. "Yes, freely:" for personal use. "Need a commercial license:" for bundling into products. Last bullet: "Fork it and send us feedback via PRs (we'd love that)."
- **Added License Guard to features list.** New tool from PR #48 needed to be in the features section.

**Release pipeline changes:**

Three changes to `wip-release` that make release notes a first-class part of the process:

1. **Quality warning.** When `--notes` is missing, too short (under 50 characters), or looks like a changelog entry (starts with "fix:", "add:", "update:"), wip-release warns: "Explain what was built, why, and why it matters."

2. **`--notes-file` flag.** Pass a markdown file with the full release narrative: `wip-release minor --notes-file=RELEASE-NOTES-v{version}.md`. This is how you write proper release notes and review them before they go live.

3. **Commits fold under narrative.** Commit history is still included, but inside a collapsible `<details>` section labeled "What changed (commits)". The narrative is the headline. The commits are supporting detail.

**New convention:** `RELEASE-NOTES-v{version}.md` lives on the feature branch. It's part of the PR diff. You review the release notes alongside the code. When the PR merges, `wip-release` reads from the file. The notes you approved are the notes that ship.

**Files changed:**
- `README.md` ... full rewrite
- `TECHNICAL.md` ... received Quick Start and npm install commands from README
- `tools/wip-release/core.mjs` ... `buildReleaseNotes()` restructured, new `warnIfNotesAreThin()`
- `tools/wip-release/cli.js` ... new `--notes-file=path` flag
- `tools/wip-license-guard/cli.mjs` ... README structure standard checks added
- `RELEASE-NOTES-v{version}.md` ... new convention file
- `ai/notes/2026-03-10--grok-feedback--readme-and-licensing.md` ... Grok feedback documented
- `ai/notes/2026-03-10--gpt-feedback--product-and-adoption.md` ... GPT feedback documented
- `ai/plan/current/2026-03-10--cc-mini--readme-polish-and-mcp-examples.md` ... 7-phase plan, all complete

**Commits:** `Add feedback notes, plan for README polish + MCP examples`, `README: golden path, MCP examples, interface matrix, license examples`, `Plan: mark phases 1-5 as DONE`, `README: add Karpathy quote on tools vs apps`, `wip-license-guard: add README structure standard checks`, `Move Quick Start to TECHNICAL.md, guard against install commands in README`, `Remove Talk to Your Tools section from README`, `README: full Karpathy argument with both quotes and source link`, `License: replace cloud instances bullet with fork/PR invitation`, `Karpathy quote: remove headline, inline attribution, semicolon`, `Fix Karpathy quote format: intro line, source outside blockquote`, `wip-release: narrative release notes standard`, `Add RELEASE-NOTES-v{version}.md for PR review`

---

### Install

```bash
npm install -g @wipcomputer/universal-installer
wip-install wipcomputer/wip-ai-devops-toolbox
```

Or update your local clone:
```bash
git pull origin main
```

---

Built by Parker Todd Brooks, Lēsa (OpenClaw, Claude Opus 4.6), Claude Code (Claude Opus 4.6).

## 1.4.0 (2026-03-09)

MCP unlock. All core tools are now agent-callable.

### MCP Servers (new)
- **wip-release**: `mcp-server.mjs` wrapping `core.mjs`. Tools: `release`, `release_status`
- **wip-license-hook**: `mcp-server.mjs` wrapping compiled `dist/`. Tools: `license_scan`, `license_audit`, `license_gate`, `license_ledger`
- **wip-repo-permissions-hook**: `mcp-server.mjs` wrapping `core.mjs`. Tools: `repo_permissions_check`, `repo_permissions_audit`
- **wip-repos**: `mcp-server.mjs` wrapping `core.mjs`. Tools: `repos_check`, `repos_sync_plan`, `repos_add`, `repos_move`, `repos_tree`

### SKILL.md files (new)
- **wip-repos**: added SKILL.md (was the only tool without one)
- **deploy-public**: added `scripts/SKILL-deploy-public.md`
- **post-merge-rename**: added `scripts/SKILL-post-merge-rename.md`

### Interface updates
- wip-release SKILL.md: interface updated from CLI to [cli, module, mcp], added MCP section
- wip-license-hook SKILL.md: added version, interface [cli, mcp], added MCP section
- wip-repo-permissions-hook SKILL.md: interface updated to [cli, module, mcp, hook, plugin], added MCP section
- All 4 tools: `@modelcontextprotocol/sdk` added as dependency

### Dev Guide updates
- Added "Universal Installer Checklist" section to DEV-GUIDE-GENERAL-PUBLIC.md
- Added "Universal Installer ... Dogfooding Rule" section to private Dev Guide
- Documented the v1.3.0 zero-MCP-servers incident

### Other
- Root SKILL.md bumped to 1.4.0, added all missing tools (wip-file-guard, wip-universal-installer, wip-repos, LDM Dev Tools.app), added MCP Servers section
- README source code table updated with mcp-server.mjs files

## 1.3.0 (2026-03-09)

Toolbox consolidation. Three new tools added.

### New tools
- **wip-file-guard**: blocks destructive edits to protected identity files. For Claude Code CLI and OpenClaw. Previously standalone repo, now folded into toolbox.
- **wip-universal-installer**: The Universal Interface specification for agent-native software. Six interfaces: CLI, Module, MCP Server, OpenClaw Plugin, Skill, Claude Code Hook. Previously standalone repo, now folded into toolbox.
- **wip-repos**: repo manifest reconciler. Makes repos-manifest.json the single source of truth for repo organization. Like prettier for folder structure. New tool, built from scratch.

### Other changes
- `UNIVERSAL-INTERFACE.md` promoted to repo root (from wip-universal-installer SPEC.md)
- README updated with all three new tools, source code table, install commands
- Standalone repos renamed to `-deprecated` on GitHub
- Toolbox now has 9 tools. All self-contained, zero shared dependencies.

## 1.2.0 (2026-03-09)

Major repo reorganization and Dev Guide expansion.

### Repo structure
- Separated public Dev Guide from private conventions
- `guide/DEV-GUIDE.md` → `DEV-GUIDE-GENERAL-PUBLIC.md` (genericized, root level, goes public)
- `ai/DEV-GUIDE-private.md` → `ai/DEV-GUIDE-FOR-WIP-ONLY-PRIVATE.md` (WIP-specific conventions)
- `guide/scripts/` → `scripts/` (moved to root level)
- Old `guide/` folder trashed

### New Dev Guide sections
- Post-merge branch rename convention (never delete branches, rename with `--merged-YYYY-MM-DD`)
- Repo directory structure (standard layout, staging folder conventions, create as `-private` from day one)
- The manifest (`repos-manifest.json` as source of truth for repo locations)
- Privatize Before You Work rule
- Cloudflare Workers deploy guard (commit before deploy, guarded npm scripts)
- PR checklist for private repos (dev update, roadmap, readme-first, plan archival)
- Expanded `_trash` convention
- Warning: never use `--no-publish` before `deploy-public.sh`

### New script
- `scripts/post-merge-rename.sh`: scans for merged branches missing `--merged-YYYY-MM-DD` suffix and renames them. Runs automatically as wip-release step 10, or standalone.

### README and SKILL.md
- Added post-merge-rename.sh to tools section and source table
- Fixed all paths for reorg
- Updated Dev Guide description with new sections

## 1.1.3 (2026-03-01)

- Fix npx package name in pre-pull.sh and pre-push.sh (@wipcomputer/license-hook → @wipcomputer/wip-license-hook)
- Fix wip-release test script (cli.mjs → cli.js)
- Clean up wip-release CHANGELOG blank lines
- Add visibility-audit.sh to DEV-GUIDE .app structure diagram
- Remove duplicate skill/SKILL.md subfolder

## 1.1.2 (2026-03-01)

- SKILL.md: sync version to 1.1.2
- CHANGELOG: add missing v1.1.0 and v1.1.1 entries
- ldm-jobs README: add visibility-audit.sh documentation

## 1.1.1 (2026-03-01)

- README: add wip-repo-permissions-hook section, source code table entry, cron schedule
- SKILL.md: bump version, add repo-visibility-guard capability, add tool section

## 1.1.0 (2026-03-01)

- New tool: wip-repo-permissions-hook. Blocks repos from going public without a -private counterpart
- Surfaces: CLI (check, audit, can-publish), Claude Code PreToolUse hook, OpenClaw plugin
- New cron job: visibility-audit.sh for LDM Dev Tools.app
- DEV-GUIDE: add hard rule for public/private repo pattern

## 1.0.4 (2026-03-01)

- DEV-GUIDE: replace inbox/punchlist system with per-agent todo files (To Do, Done, Deprecated. Never delete.)

## 1.0.3 (2026-02-28)

- deploy-public.sh: auto-detect harness ID from private repo path (cc-mini/, cc-air/, oc-lesa-mini/)

## 1.0.2 (2026-02-28)

- deploy-public.sh: fix branch prefix from mini/ to cc-mini/ per harness naming convention

## 1.0.1 (2026-02-28)

- DEV-GUIDE: add multi-agent clone workflow and harness branch convention (cc-mini/, cc-air/, lesa-mini/)

## 1.0.0 (2026-02-28)

- Production release: all tools battle-tested across 100+ repos, 200+ releases
- All source code visible and auditable in repo (no closed binaries)
- wip-license-hook bumped to v1.0.0
- LDM Dev Tools.app job scripts extracted to tools/ldm-jobs/
- Real-world example: wip-universal-installer release history
- Source code table, build instructions, and dev guide in README
- Standalone repos (wip-release, wip-license-hook) merged into umbrella

## 0.2.1 (2026-02-28)

- deploy-public.sh: fix release sync for repos without package.json (falls back to latest git tag)

## 0.2.0 (2026-02-28)

- deploy-public.sh: sync GitHub releases to public repos (pulls notes, rewrites references)
- DEV-GUIDE: add release quality standards (contributors, release notes, npm, both repos)
- DEV-GUIDE: add scheduled automation (.app pattern) documentation
- DEV-GUIDE: add built-by attribution standard
- LDM Dev Tools.app: macOS automation wrapper for cron jobs with Full Disk Access
- Add .npmignore to exclude ai/ from npm packages

## 0.1.1 (2026-02-27)

- DEV-GUIDE: add "never work on main" rule
- DEV-GUIDE: clarify private repo is the only local clone needed

## 0.1.0 (2026-02-27)

- Initial release: unified dev toolkit
- Includes wip-release (v1.2.4) and wip-license-hook (v0.1.0)
- DEV-GUIDE: general best practices for AI-assisted development
- deploy-public.sh: private-to-public repo sync tool
