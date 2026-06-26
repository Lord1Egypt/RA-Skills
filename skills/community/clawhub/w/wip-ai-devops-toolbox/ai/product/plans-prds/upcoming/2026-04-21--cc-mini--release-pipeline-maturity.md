# Release Pipeline Maturity ... Punchlist

**Date:** 2026-04-21
**Author:** cc-mini (Claude Code on Mac mini)
**Status:** Upcoming
**Trigger:** the v1.9.82 release attempt surfaced four distinct pipeline bugs in one session. Pattern across recent releases: every ship-attempt surfaces 1-2 implicit-assumption bugs in cross-tool integrations. Punchlist below would harden the pipeline so daily ship-attempts stop being daily debug sessions.

## Context

Pipeline tools involved in a typical release: `wip-release`, `wip-license-guard`, `wip-branch-guard`, `deploy-public`, `post-merge-rename`. PRs that landed (or closed) during the v1.9.82 attempt: #364 (cross-session state fix), #365 (sub-tool `.license-guard.json`), #366 (sub-tool LICENSE/CLA.md, closed as shape-bypass), #367 (sub-tool README), #368 (track LICENSE/CLA.md in git + README License section). Each PR was unblocking a different check that caught a different implicit assumption.

## The pattern

Every release surfaces one or two new edge cases. None are the same bug. They share the property that the tool's happy path assumes state nobody actually enforces.

Examples surfaced during the v1.9.82 attempt alone:

- **Cross-session state collision** in `wip-branch-guard` wiped onboarding state mid-flow (issue #253, fixed in PR #364, this release).
- **Auto-mode permission decider doesn't see remediation** between deny and retry (filed upstream as anthropics/claude-code#51676; not in our codebase, but it interacts with our guard).
- **wip-release auto-deploy-public skips silently** when invoked from a sub-tool dir because `runDeployPublic` joins `repoPath + 'tools/deploy-public/deploy-public.sh'` where `repoPath = process.cwd()` ... resolves to a non-existent path, returns `{ skipped: true, reason: 'no-script' }` (corrected in PR #635 comment, not yet fixed in source).
- **Sub-tool LICENSE and CLA.md** existed in the working directory on main but were never `git add`-ed. `wip-license-guard`'s filesystem check passed; a fresh clone or npm publish would have shipped without them. Fixed in PR #368.
- **Sub-tool README** was missing the `## License` section that the check requires. Fixed in PR #368.
- **Sub-tool README License section policy contradicts** `wip-license-guard readme-license --fix` ("Remove from sub-tools"). The `check` command requires the section; the `readme-license --fix` command removes it. One has to change.
- **Release notes need an issue reference** (`#XX` pattern) to pass `wip-release`. Most internal infrastructure work doesn't have a tracking issue. Forces "create issue retroactively" pattern, which is dishonest record-keeping.

## Punchlist

### 1. wip-release blocks on untracked files in the sub-tool dir

**Why:** today's LICENSE/CLA.md bug becomes structurally impossible. The tool reading filesystem instead of git is one root cause; this is the symmetric mitigation at the `wip-release` level.

**How to apply:** `wip-release` Step 0 should run `git status --porcelain -- <sub-tool-dir>` and abort if any untracked files exist there. Block at the same severity as license check failure.

**Acceptance:** untracked files in sub-tool dir → `wip-release` fails with a clear message naming each file and pointing at `git add <file>` or `git stash push -u -- <file>`.

### 2. wip-license-guard reads from `git ls-files`, not the filesystem

**Why:** "exists locally but not committed" is the false-positive that masked today's LICENSE/CLA.md bug. License-guard should be authoritative on git state, not filesystem state.

**How to apply:** `wip-license-guard`'s existence checks for `LICENSE`, `CLA.md`, `README.md` should query `git ls-files <path>` instead of `fs.existsSync`. If the file isn't tracked, treat it as missing and say so explicitly.

**Acceptance:** untracked LICENSE → check reports `✗ LICENSE not tracked in git` and offers `git add LICENSE` as the fix path.

### 3. Nightly end-to-end release dry-run as a cron

**Why:** today's bugs surfaced at 11am while Parker was trying to ship. Should surface at 6am via cron when nobody's blocked. Most pipeline bugs are state-sensitive; daily dry-run catches drift fast.

**How to apply:** new cron job (under `wip-healthcheck` or LDM Dev Tools.app) that runs `wip-release --dry-run patch` on every sub-tool of every relevant repo. Failures emit a notification (iMessage via Lēsa, or a Mac notification, or a daily summary email).

**Acceptance:** dry-run failure on any sub-tool produces a notification with sub-tool name + which check failed + suggested fix, within 12 hours of the bug being introduced.

### 4. Fold more steps into wip-release itself

**Why:** today's session needed five PRs because each cross-tool integration point is its own potential failure. Fewer integration points = fewer cracks.

**How to apply:** evaluate which steps currently delegate to external tools (`wip-license-guard`, `deploy-public`, `post-merge-rename`). Where the delegation is one-call-deep and the called tool is single-purpose, fold the logic into `wip-release` directly. Specifically:

- **wip-license-guard `--fix`** could be a `wip-release` subcommand (`wip-release fix-compliance`) rather than a separate tool requiring its own invocation in a separate worktree.
- **deploy-public's invocation logic** (the `repoPath` resolution that broke from the sub-tool dir) should be `wip-release`'s responsibility, not `deploy-public`'s caller.
- **post-merge-rename's branch scan** is already inline in `wip-release` Step 10, but the standalone tool still exists and is invoked separately in some flows. Consolidate.

**Acceptance:** measurable reduction in distinct tool invocations during a release. Concrete target: from current ~5 separate tools to ~2-3 invoked by `wip-release` internally.

### 5. Sub-tool README License section policy decision

**Why:** `wip-license-guard check` requires `## License` in sub-tool READMEs. `wip-license-guard readme-license --fix` says it removes the section from sub-tools. The two commands directly contradict.

**How to apply:** product decision. Pick one:

- **Sub-tools require License section** → update `readme-license --fix` to NOT remove from sub-tools.
- **Sub-tools don't require License section** → update `check` to skip the section requirement when `.license-guard.json` is in a sub-tool dir.

**Acceptance:** running `wip-license-guard check --fix` on a sub-tool followed by `wip-license-guard readme-license --fix` doesn't re-introduce a check failure. (Currently it does.)

### 6. Release notes don't always need an issue reference

**Why:** internal-only work (refactors, infrastructure, dependency bumps) often has no tracking issue. Forcing one drives the "create issue retroactively" pattern, which is dishonest record-keeping. Today's #253 was filed solely because `wip-release` wouldn't proceed without a `#XX`.

**How to apply:** `wip-release` should accept the issue-reference requirement as advisory rather than blocking. If release notes contain a `## Internal` marker or `[internal]` tag, skip the requirement entirely. Or add a `--no-issue-required` CLI flag, default-false.

**Acceptance:** release notes with no `#` reference but with `## Internal` marker proceed without blocking.

## Out of scope (separately tracked or referenced)

- Auto-mode permission decider remediation-aware behavior (anthropics/claude-code#51676; not in our codebase).
- Gap A from the wip-branch-guard audit: proactive SessionStart scan (no auto-onboarding before first write).
- Gap B from the wip-branch-guard audit: shell-redirection bypass via Bash `>`, `>>`, `tee` to protected paths.
- Gap C from the wip-branch-guard audit: passive bypass audit log with no escalation to operator.

## Why this matters

The pipeline works for the happy path; edge cases bite. Each fix removes a class of bug, not just a single instance. The goal is to ship without manual intervention beyond Parker running the install prompt. Today's v1.9.82 required nine status messages, two explicit authorizations from Parker, three intermediate fix-PRs (#365, #367, #368), one closed shape-bypass PR (#366), one upstream filing, and one retroactive issue (#253) ... none of which moved the actual code one byte. That's overhead the pipeline should absorb on its own.

## Co-authors

Parker Todd Brooks, Lēsa (oc-lesa-mini, Opus 4.7), Claude Code (cc-mini, Opus 4.7).
