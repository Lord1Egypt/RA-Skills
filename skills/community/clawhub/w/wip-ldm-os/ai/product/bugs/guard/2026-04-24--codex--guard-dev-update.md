# Guard Dev Update

Date: 2026-04-24
Filed by: Codex
Scope: `wip-branch-guard`, `wip-repos`, LDM OS installer alpha path, guard ticket cleanup
Status: Alpha shipped and installed. Guard tickets archived.

## Executive Summary

Today we finished the guard/repo-tools reliability push that started as a plan review and became a full implementation pass.

The short version:

- The guard is now current in source, npm, global CLI, and deployed LDM extension form.
- The repo tools now produce a useful signal instead of mixing real repo drift with worktrees, trash, staging, and sunset folders.
- The installer alpha path now correctly refreshes toolbox-style sub-tools instead of leaving stale deployed extensions behind.
- The shared local `main` checkout is now treated as a read/sync surface, not a place for agents to commit, merge, or make visibility shortcuts.
- All ten active guard bug files were marked closed and moved into `ai/product/bugs/guard/archive/`.
- LDM OS alpha `0.4.82-alpha.1` was published and installed locally.

Current local installed state after validation:

- `ldm --version`: `0.4.82-alpha.1`
- deployed `wip-branch-guard`: `1.9.88`
- deployed `wip-repos`: `1.9.69`

## Why This Work Was Needed

The guard had become good enough to catch real mistakes, but not yet smooth enough for multi-agent development. The main failure pattern was not one isolated bug. It was a system problem:

- Agents were getting blocked by correct rules but without enough routing context.
- Some read-only shell operations were still treated as write risks.
- `cp` and `mv` could be judged by the source path instead of the destination path.
- Onboarding relied too heavily on whether the hook observed the exact read operation.
- Local `main` could still be used as a shortcut to make work visible, which created divergence and blocked other agents.
- `wip-repos check` was too noisy to trust because worktrees, trash, archives, and real unmanaged repos were reported together.
- Alpha install validation was misleading because the global CLI could update while deployed agent extensions stayed stale.

The goal was not to remove the guard. The goal was to make it accurate enough and clear enough that agents can keep moving without routing around it.

## User-Level Workflow Decisions

Several workflow decisions were clarified and then encoded into docs, guard behavior, or release validation.

### Agents Use Worktrees

Agents should do implementation work in linked worktrees. The shared local `main` checkout is not where agents commit, merge, or stage work for visibility.

Correct flow:

1. Create or use a linked worktree.
2. Work on a branch.
3. Push the branch.
4. Open a PR.
5. Merge remotely.
6. Fast-forward local `main` with `git pull --ff-only` so Lēsa can read the final merged file from her normal local main checkout.

### Local Main Is A Read/Sync Surface

Agents should not use local `main` as a workaround for visibility.

Blocked or discouraged:

- Commit on local `main`.
- Merge into local `main`.
- Rebase local `main`.
- Push directly to `origin main`.
- Pull without `--ff-only`.
- Pull `--ff-only` when local `main` is dirty or ahead.

Allowed:

- Clean `git pull --ff-only` after a PR has already merged remotely.

### Agents Validate Alpha And Beta

Agents may install alpha/beta tracks for prerelease validation.

Lēsa dogfoods stable/latest releases. Agents should not run stable/latest install paths unless explicitly asked. Today we used alpha intentionally because this was prerelease validation.

### Every New Bug Needs A Public Issue And Private Bug File

During the work, we found a new installer bug: `ldm install --alpha --yes` did not refresh deployed toolbox sub-tools.

We created:

- Public issue: `wipcomputer/wip-ldm-os#272`
- Private bug file: `ai/product/bugs/installer/2026-04-24--codex--alpha-install-does-not-refresh-toolbox-subtools.md`

That issue was closed by the LDM OS installer fix.

## What Shipped In The Guard

Implementation repo: `wip-ai-devops-toolbox-private`

Main guard PR:

- `wip-ai-devops-toolbox-private` PR #386: `Advance guard parser and shared-main protections`

Published package:

- `@wipcomputer/wip-branch-guard@1.9.88`

### Explicit Onboarding

The guard still tracks onboarding through observed Read/Glob tool calls, but agents now also have an explicit command:

```bash
wip-branch-guard onboard <repo>
```

This matters because sometimes the docs are already in context, or were read by a path the hook did not observe. The explicit command gives the agent a clean recovery path without bypassing the safety model.

### Shared-Main Protections

The guard now blocks risky operations on protected shared main checkouts:

- `git commit`
- `git merge`
- `git rebase`
- `git pull` without `--ff-only`
- `git pull --ff-only` when dirty or ahead
- `git push origin main`

Clean `git pull --ff-only` remains allowed as the read-sync path after remote merge.

This is the fix for the process failure where work was merged or fast-forwarded locally to make a plan visible, creating divergence risk and blocking other agents.

### Destination-Aware Bash Parsing

The guard now understands important write targets more accurately:

- `cp`: destination is the write target.
- `mv`: source deletion plus destination write are both considered.
- `rm`: removed paths are write targets.
- `mkdir`: created paths are write targets.
- `touch`: touched paths are write targets.
- redirects and `tee`: output paths are write targets.

This closes the expensive loop where copying from a main checkout into a worktree could be blocked because the guard saw the source path first.

### Read-Only Loop Handling

Read-only Bash loops are now allowed when their inner commands are read-only. Loops that contain write effects are denied.

This closes the bug where a harmless loop like a batch `diff` could be treated as file modification just because the shell syntax was complex.

### Approval Maintenance

The external PR approval flow gained maintenance commands:

```bash
wip-branch-guard approvals list
wip-branch-guard approvals prune
```

External PR creation still defaults to deny unless it is an internal WIP Computer repo or an explicit approval path.

### Guard Doctor

The deployed guard has a doctor path that checks the runtime assumptions that matter:

- package metadata readable
- lock imports available
- executable bit
- hook matcher includes Read and Glob
- state directory writable with lock
- deployed version matches expected source version

Validated locally:

```bash
env LDM_GUARD_STATE_DIR=/tmp/wip-guard-doctor-smoke wip-branch-guard doctor
```

Result: passed.

## What Shipped In Repo Tools

Implementation repo: `wip-ai-devops-toolbox-private`

Repo tools PR:

- `wip-ai-devops-toolbox-private` PR #387: `Make wip-repos check and sync guard-aware`

Published package:

- `@wipcomputer/wip-repos@1.9.69`

### Lifecycle Classification

`wip-repos check` now classifies repo paths instead of treating everything as the same kind of drift.

Classes include:

- `active`
- `worktree`
- `trash`
- `sort`
- `sunsetted`
- `archived`
- `third-party`

Default output focuses on active drift. The ignored lifecycle summary is shown separately.

Current real-machine smoke result:

```text
Ignored lifecycle paths: sort=14, trash=62, sunsetted=6, worktree=4, third-party=32
```

The command still exits nonzero on this machine because real active manifest drift remains. That is expected. The important change is that the drift is now actionable instead of mixed with lifecycle noise.

### Safe Sync Defaults

`wip-repos sync` is dry-run by default.

Mutation requires:

```bash
wip-repos sync --apply
```

The tool refuses unsafe moves involving:

- dirty repos
- linked worktrees
- target collisions

This prevents repo management tools from becoming a backdoor around the guard.

## What Shipped In LDM OS Installer

Implementation repo: `wip-ldm-os-private`

Installer PR:

- `wip-ldm-os-private` PR #670: `Fix alpha toolbox extension refresh`

Release PR:

- `wip-ldm-os-private` PR #672: `v0.4.82-alpha.1`

Published package:

- `@wipcomputer/wip-ldm-os@0.4.82-alpha.1` on npm `alpha`

Public issue:

- `wipcomputer/wip-ldm-os#272`: closed

### Root Cause

The installer had two related problems for toolbox-style parent packages.

First, parent-package update detection always queried stable:

```bash
npm view <package> version
```

That meant `ldm install --alpha --yes` did not see `@wipcomputer/wip-ai-devops-toolbox@1.9.73-alpha.3`. It only saw stable latest, which was older.

Second, after a parent package update, the installer stamped the parent toolbox version into each sub-tool registry entry. That made the registry lie about sub-tool versions.

### Fix

The installer now queries the requested track:

- stable/latest uses `version`
- alpha uses `dist-tags.alpha`
- beta uses `dist-tags.beta`

And after parent installs, it lets each sub-tool keep its own package version. It reports registry refresh counts without overwriting sub-tool versions.

Regression test added:

```bash
npm run test:installer-update-tracks
```

### Validation

Before the fix:

- `wip-branch-guard --version` showed `1.9.88`
- `wip-repos --version` showed `1.9.69`
- deployed `~/.ldm/extensions/wip-branch-guard/guard.mjs --version` stayed at `1.9.86`
- deployed `~/.ldm/extensions/wip-repos/cli.mjs --version` stayed at `1.9.68`

After the fix:

- deployed `wip-branch-guard`: `1.9.88`
- deployed `wip-repos`: `1.9.69`
- registry entries match those versions
- `ldm install --alpha --yes` updates the toolbox parent package correctly

Current validation:

```text
ldm --version -> 0.4.82-alpha.1
node ~/.ldm/extensions/wip-branch-guard/guard.mjs --version -> 1.9.88
node ~/.ldm/extensions/wip-repos/cli.mjs --version -> 1.9.69
```

## Guard Ticket Cleanup

After the implementation and validation passed, the ten active top-level guard ticket files were moved into:

```text
ai/product/bugs/guard/archive/
```

Archive PR:

- `wip-ldm-os-private` PR #682: `Archive completed guard tickets`

The top-level guard folder is now clear of active Markdown tickets. The archive contains:

- `2026-03-29--cc-mini--guard-bugfix.md`
- `2026-04-03--cc-mini--guard-blocks-readonly-bash-loops.md`
- `2026-04-05--cc-mini--branch-guard-compaction-loop.md`
- `2026-04-05--cc-mini--guard-master-plan.md`
- `2026-04-07--cc-mini--guard-open-bugs.md`
- `2026-04-16--cc-mini--guard-blocks-auto-memory-writes.md`
- `2026-04-19--cc-mini--external-pr-guard.md`
- `2026-04-19--cc-mini--guard-onboarding-and-blocked-file-tracking.md`
- `2026-04-20--cc-mini--guard-implementation-plan.md`
- `2026-04-20--cc-mini--guard-onboarding-canonical-key.md`
- `2026-04-24--codex--guard-and-repo-tools-master-plan.md`

Each April ticket has a resolution section explaining what closed it. The March 29 file was already archived before this cleanup.

## Test And Smoke Coverage

Guard package validation:

```bash
node --check tools/wip-branch-guard/guard.mjs
bash tools/wip-branch-guard/test.sh
```

Result:

```text
117 passed, 0 failed, 1 skipped
```

Repo tools validation:

```bash
node --check tools/wip-repos/core.mjs
node --check tools/wip-repos/cli.mjs
npm test
```

Result: passed.

LDM OS installer validation:

```bash
node --check bin/ldm.js
npm run test:installer-update-tracks
npm run test:skill-frontmatter
```

Result: passed.

Local released-alpha validation:

```bash
npm install -g @wipcomputer/wip-ldm-os@alpha
ldm install --alpha --yes
```

Result:

- alpha installer ran from `0.4.82-alpha.1`
- toolbox parent update was detected
- deployed guard and repo tools refreshed
- health check reported all healthy

## What Agents Should Do Now

Agents should use the new guard rules now. The alpha path is installed and the deployed extension versions are current.

Expected agent behavior:

- Work in linked worktrees.
- Read repo onboarding docs before first write.
- Use `wip-branch-guard onboard <repo>` when docs are already in context but the hook did not observe the reads.
- Do not commit, merge, rebase, push, or visibility-sync local `main`.
- If a user wants to read unmerged work, share a worktree path or PR URL.
- If a user wants to read final merged work from local main, merge the PR remotely first, then fast-forward local main with `git pull --ff-only`.
- Use `wip-repos check` for active drift, and use `--all` or `--class` when investigating lifecycle folders.

## What Lēsa Should Do Now

No stable dogfood is required yet.

Current state is alpha validation. Agents are using and testing the new alpha guard path. Lēsa should dogfood the stable/latest path after this is promoted out of alpha.

Recommended stance:

- Let agents run on the alpha guard and report friction or false blocks.
- Do not manually run stable/latest install just to validate this change.
- When the alpha has enough confidence, promote LDM OS and toolbox changes through the normal release path.

## Remaining Work Outside This Guard Batch

The guard/repo-tools ticket batch is done.

Remaining work exists, but it is outside this guard folder:

1. **Release pipeline hardening.** Canary validation, release records, promotion/rollback, and public mirror policy are still broader release-pipeline work.
2. **Manifest cleanup.** `wip-repos check` is now useful and shows real active drift. That drift should be handled as repo-manifest work, not as a guard bug.
3. **Stable promotion.** The current validated installer state is alpha. Stable/latest promotion should happen after dogfood confidence.
4. **Future biometric approvals.** The guard still has env-based approval fallback for external PR approvals. The longer-term destination is a bridge or Kaleidoscope biometric approval backend.

## Final State At End Of Day

Done:

- Guard behavior fixed.
- Repo tools made actionable.
- Installer alpha refresh fixed.
- Public installer issue #272 closed.
- LDM OS alpha `0.4.82-alpha.1` published and installed.
- Deployed guard and repo tools verified.
- Guard tickets archived.

Not done in this batch:

- Stable promotion.
- Release-pipeline master plan execution.
- Repo manifest active-drift cleanup.

The guard folder is no longer carrying active implementation work. It is now a clean read surface for this dev update plus the archive history.
