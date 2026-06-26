# Guard and Repo Tools Master Plan

**Date:** 2026-04-24
**Filed by:** Codex
**Repo:** `wip-ai-devops-toolbox-private` for implementation, `wip-ldm-os-private` for this plan
**Status:** implemented for the guard/repo-tools scope. Installer follow-up for alpha deployment filed as public issue #272 and fixed in this branch.

## Why this plan exists

The guard has improved a lot since the April 5 loop, but the system still has three trust gaps:

1. The deployed guard, source guard, npm packages, and alpha tag do not agree.
2. The guard enforces correct workflow through brittle signals that agents can miss.
3. `wip-repos` reports local worktrees, trash, and staging folders as repo drift, so its signal is too noisy to act on.

This plan consolidates the existing guard bug folder plus the repo-tool findings from 2026-04-24 into one execution order.

## Current facts from 2026-04-24

- Original triage found toolbox alpha behind latest, deployed guard/source/npm drift, `wip-repos` noise from lifecycle folders, and a shared-main workflow gap.
- After PRs #386 and #387 in `wip-ai-devops-toolbox-private`, `@wipcomputer/wip-ai-devops-toolbox@alpha` is `1.9.73-alpha.3`, `@wipcomputer/wip-branch-guard` is `1.9.88`, and `@wipcomputer/wip-repos` is `1.9.69`.
- Agent-side alpha validation installed the new toolbox alpha and deployed extension files now report `wip-branch-guard 1.9.88` and `wip-repos 1.9.69`.
- `wip-branch-guard doctor` passes against the deployed guard.
- `wip-repos check` now classifies lifecycle paths and reports ignored counts separately. It still exits nonzero on the current machine because real active manifest drift remains, which is expected and actionable.
- Follow-up discovered during validation: `ldm install --alpha --yes` did not initially refresh toolbox sub-tools because the LDM OS parent-package check queried stable instead of the requested alpha tag. Public issue: https://github.com/wipcomputer/wip-ldm-os/issues/272. Private bug: `ai/product/bugs/installer/2026-04-24--codex--alpha-install-does-not-refresh-toolbox-subtools.md`.

## Consolidated Bug Inventory

### Already mostly addressed, but must stay covered

- Quoted-string false positives and compound-command false negatives from `archive/2026-03-29--cc-mini--guard-bugfix.md`.
- Main-branch write protection for `Write`, `Edit`, `NotebookEdit`, and `Bash`.
- Stash escape hatch for untracked files blocking `git pull`.
- SessionStart advisory for sessions that resume on main.
- Worktree-bootstrap allowlist.
- Onboarding-before-first-write.
- Recently-blocked-file tracking.
- External-PR creation guard.
- Canonical onboarding key across worktrees.
- Claude Code auto-memory allowlist.

These should be treated as regression coverage, not active design questions.

### Original active findings and closure

1. **Release channel drift:** closed by toolbox PRs #380, #381, #382, #386, #387 and alpha `1.9.73-alpha.3`.
2. **Guard lock imports missing:** closed by PR #380 and verified by `wip-branch-guard doctor`.
3. **Onboarding signal too narrow:** closed by PR #386 with explicit `wip-branch-guard onboard <repo>` plus retained Read/Glob tracking.
4. **Reactive error messages:** improved by PR #386 with routed shared-main and onboarding denial text.
5. **`cp` and `mv` target detection:** closed by PR #386 with destination-aware parser tests.
6. **Read-only Bash loops:** closed by PR #386 with read-only loop allow tests and write-effect deny tests.
7. **Repo bootstrap first commit:** retained as existing regression coverage.
8. **Repo manifest drift classification:** closed by PR #387 with lifecycle classes and ignored summaries.
9. **Repo mutator safety:** closed for `sync` by PR #387 with dry-run default and dirty/collision/worktree refusal.
10. **Shared `main` visibility shortcut:** closed by PR #386 with shared-main commit, merge, rebase, unsafe pull, and push protections. Clean `git pull --ff-only` remains allowed for Lēsa's local read surface after remote PR merge.

## Execution Record

- `wip-ai-devops-toolbox-private` PR #386: explicit onboarding, destination-aware Bash write parsing, read-only loop handling, shared-main protections, approval list/prune, guard doctor coverage.
- `wip-ai-devops-toolbox-private` PR #387: `wip-repos check` lifecycle classification, `--all`, `--class`, JSON details, `sync --apply`, dirty/collision/worktree safety, tests.
- Toolbox alpha release: `@wipcomputer/wip-ai-devops-toolbox@1.9.73-alpha.3`.
- Published sub-tools: `@wipcomputer/wip-branch-guard@1.9.88`, `@wipcomputer/wip-repos@1.9.69`.
- LDM OS public issue #272 and this branch: fix `ldm install --alpha --yes` so parent toolbox alpha updates redeploy sub-tools and do not stamp parent versions into sub-tool registry entries.
- Local validation: deployed `~/.ldm/extensions/wip-branch-guard/guard.mjs --version` reports `1.9.88`; deployed `~/.ldm/extensions/wip-repos/cli.mjs --version` reports `1.9.69`; registry entries agree.

## Traceability: Existing Tickets to Closure Work

This 2026-04-24 plan supersedes the older master-plan documents as the current execution plan. The older tickets remain useful as repro history and acceptance-test sources. A ticket should only be marked closed after the source fix is merged, a regression test or smoke test exists, the fix is released or installed where relevant, and the ticket links back to the PR that closed it.

| Existing ticket | Current plan coverage | Closure work | Acceptance signal |
|---|---|---|---|
| `archive/2026-03-29--cc-mini--guard-bugfix.md` | Phase 2, Phase 6 | Preserve regression coverage for quoted strings, compound commands, shared-state writes, and plan-file allowlisting. | Existing guard tests pass plus new parser tests do not regress those cases. |
| `2026-04-03--cc-mini--guard-blocks-readonly-bash-loops.md` | Phase 6 | Parse loop bodies by command effect instead of denying on shell syntax. | Read-only `for` loop allows; loop containing `rm`, redirect, `tee`, or another write effect denies. |
| `2026-04-05--cc-mini--branch-guard-compaction-loop.md` | Phase 3, Phase 5 | Keep SessionStart advisory, strengthen main-branch denial routing, and make resumed sessions self-correcting. | Session resumed on `main` gets advisory before write; attempted main write includes exact worktree command and does not suggest retrying in place. |
| `2026-04-05--cc-mini--guard-master-plan.md` | Phase 1, Phase 10 | Finish release-channel and deployment repair: alpha newer than latest, sub-tool publishing, public sync, install verification. | Alpha install deploys current guard; `wip-release alpha` from a worktree refuses; source/npm/deployed versions match. |
| `2026-04-07--cc-mini--guard-open-bugs.md` | Phase 5, Phase 6 | Close first-commit/pre-commit alignment and destination-aware `cp`/`mv` behavior. | Empty repo first commit works; `cp main/file worktree/file` allows; `cp worktree/file main/file` denies. |
| `2026-04-16--cc-mini--guard-blocks-auto-memory-writes.md` | Phase 2 | Keep the Claude Code auto-memory allowlist as regression coverage, not a broad gitignored-file exception. | Writes to expected auto-memory paths are allowed; arbitrary gitignored writes are still evaluated normally. |
| `2026-04-19--cc-mini--external-pr-guard.md` | Phase 7 | Keep fork-head path easy, add durable approvals, listing, pruning, and audit logs. | External PR without fork head denies; `--head wipcomputer:<branch>` allows; durable approval allows and audits. |
| `2026-04-19--cc-mini--guard-onboarding-and-blocked-file-tracking.md` | Phase 3, Phase 5 | Add explicit onboarding, keep automatic Read/Glob tracking, preserve recently-blocked-file retry detection. | First write blocks until onboarding; same-file tool swap after denial is denied with routing text. |
| `2026-04-20--cc-mini--guard-implementation-plan.md` | Phase 0, Phase 1, Phase 2, Phase 10 | Reconcile source/deployed/npm drift, restore runtime lock behavior, add doctor and install hash verification. | `wip-branch-guard doctor` passes; source/deployed/npm versions and hashes are consistent. |
| `2026-04-20--cc-mini--guard-onboarding-canonical-key.md` | Phase 3 | Keep canonical repo key behavior across worktrees. | Onboarding in worktree A satisfies worktree B for the same repo, but not a different repo. |
| 2026-04-24 shared-`main` incident | Phase 4, Phase 5 | Prevent agents from using local shared `main` for visibility, plans, commits, fast-forwards, PR merges, or pull-side effects. | Guard blocks agent commits/merges on shared `main`; advisory says to use a worktree branch and PR; visibility is handled by branch/PR links. |
| 2026-04-24 repo-tools findings | Phase 8, Phase 9 | Classify repo lifecycle paths and make mutating repo operations dry-run-first and guard-aware. | `wip-repos check` default is actionable; `sync --apply` refuses dirty, collision, and worktree hazards. |

## Complete Ticket Closure Checklist

Each ticket gets closed by completing its acceptance signal, not by declaring the umbrella plan complete.

1. `archive/2026-03-29--cc-mini--guard-bugfix.md`
   - Keep tests for quoted content, compound command segmentation, plan/shared-state allowlists, and main-branch write protection.
   - Close when those tests run in the guard test suite after the parser and onboarding changes land.
2. `2026-04-03--cc-mini--guard-blocks-readonly-bash-loops.md`
   - Add effect-based loop parsing.
   - Close when read-only loops allow and write-effect loops deny.
3. `2026-04-05--cc-mini--branch-guard-compaction-loop.md`
   - Verify `Write`, `Edit`, `NotebookEdit`, and `Bash` all share main-branch protection.
   - Add SessionStart advisory and denial routing for resumed-on-main sessions.
   - Close when a resumed session on `main` is proactively routed to a worktree before writes.
4. `2026-04-05--cc-mini--guard-master-plan.md`
   - Finish alpha/latest repair, sub-tool publishing, public sync, and release refusal from worktrees.
   - Close when install alpha deploys current guard and release tooling cannot publish stale or partial tool versions.
5. `2026-04-07--cc-mini--guard-open-bugs.md`
   - Align guard and pre-commit behavior for zero-commit repos.
   - Add destination-aware `cp`/`mv` parser tests.
   - Close when empty repo first commit works and source/destination cases behave correctly.
6. `2026-04-16--cc-mini--guard-blocks-auto-memory-writes.md`
   - Keep the auto-memory write allowlist narrow.
   - Close when the deployed guard allows expected auto-memory writes and does not turn gitignored paths into a blanket bypass.
7. `2026-04-19--cc-mini--external-pr-guard.md`
   - Add durable approval lifecycle, audit logs, and clearer fork-head instructions.
   - Close when no-head external PR creation denies and fork-head or approved external PR creation allows.
8. `2026-04-19--cc-mini--guard-onboarding-and-blocked-file-tracking.md`
   - Add `wip-branch-guard onboard <repo>`.
   - Keep Read/Glob tracking and blocked-file retry detection.
   - Close when first write blocks until onboarding and retry-by-tool-swap is still denied.
9. `2026-04-20--cc-mini--guard-implementation-plan.md`
   - Reconcile deployed `1.9.85` into source, fix runtime lock imports, add doctor, and verify installed content hashes.
   - Close when source, npm, and deployed guard agree.
10. `2026-04-20--cc-mini--guard-onboarding-canonical-key.md`
   - Preserve canonical repo key regression coverage.
   - Close when onboarding once works across linked worktrees for the same repo only.
11. 2026-04-24 shared-`main` incident
   - Add shared-main protection for agent commits, fast-forwards, pulls with side effects, direct merges, and local visibility shortcuts.
   - Close when agents get a proactive warning on shared `main`, writes are blocked, and the recommended path is worktree branch -> PR -> merge -> `main` fast-forward only when explicitly requested.
12. 2026-04-24 repo-tools findings
   - Add lifecycle classification and dry-run-first mutators.
   - Close when repo checks separate real active drift from worktree/trash/archive noise and mutators refuse risky paths by default.

## Desired End State

An agent can do this without Parker rescue:

1. Install the current alpha safely.
2. Verify exactly which guard, repo tools, and release tools are active.
3. Start in any repo and get proactive workflow context before the first write.
4. Read onboarding docs once per canonical repo per session.
5. Write only from a linked worktree.
6. Never use the shared local `main` checkout as a place to commit, merge, fast-forward for visibility, or stage handoff work.
7. Open internal PRs normally.
8. Open external PRs only through fork-head or durable approval.
9. Use `wip-repos check` and get a small, actionable drift report.
10. Release and deploy the fixes without manual tag repair, sub-tool publishing, or public mirror drift.

## Execution Plan

### Phase 0. Freeze and snapshot current state

Goal: stop guessing which copy is authoritative.

1. Record versions for:
   - `wip-branch-guard --version`
   - `node ~/.ldm/extensions/wip-branch-guard/guard.mjs --version`
   - source `tools/wip-branch-guard/package.json`
   - `npm view @wipcomputer/wip-ai-devops-toolbox dist-tags`
   - `npm view @wipcomputer/wip-branch-guard dist-tags`
2. Save the deployed `1.9.85` guard to a comparison artifact in the toolbox worktree.
3. Diff deployed `1.9.85` against source `1.9.84`.
4. Decide source of truth: deployed `1.9.85` wins unless the diff reveals local-only experimental code.

Deliverable: short audit note in the toolbox PR explaining exactly what source was reconciled.

### Phase 1. Repair the release channel

Goal: make alpha installable again before testing more guard changes through LDM install.

1. Fix stale npm dist-tags:
   - publish or repoint `@wipcomputer/wip-ai-devops-toolbox@alpha` so alpha is newer than latest.
   - publish `@wipcomputer/wip-branch-guard@1.9.85` or bump to `1.9.86` if source changes.
2. Ensure `wip-release alpha` refuses to publish an alpha older than latest.
3. Ensure root toolbox package and sub-tool packages are published together when sub-tool files change.
4. Run `deploy-public` as part of the release path, not as a remembered manual step.
5. Only then install alpha:
   - `npm install -g @wipcomputer/wip-ai-devops-toolbox@alpha`
   - `ldm install --alpha --yes`

Gate: alpha install must deploy the same guard version as source and npm.

### Phase 2. Fix guard runtime correctness

Goal: remove silent fail-open or fail-soft behavior.

1. Import `openSync`, `closeSync`, and `unlinkSync` in `guard.mjs`.
2. Add a direct unit/smoke test that proves the lockfile path actually executes.
3. Add a parallel-read test:
   - two hook invocations mark `README.md` and `CLAUDE.md` in the same session concurrently.
   - final session state must contain both entries.
4. Add a fail-fast self-test command:
   - `wip-branch-guard doctor`
   - checks imports, executable bit, package version, deployed version, hook matcher, state dir writability.

Gate: `bash test.sh`, `node --check guard.mjs`, and `wip-branch-guard doctor` all pass.

### Phase 3. Make onboarding explicit, not accidental

Goal: preserve safety while removing "I read it but the guard did not see it" friction.

1. Keep automatic `Read` and `Glob` tracking.
2. Add explicit command:
   - `wip-branch-guard onboard <repo>`
   - prints required docs.
   - records canonical repo onboarding for the current session.
   - writes an audit entry with reason `explicit-onboard`.
3. Add a SessionStart advisory that lists required reads for the current repo and offers the exact onboard command.
4. Expand required docs carefully:
   - root `README.md`
   - root `CLAUDE.md`
   - root `*RUNBOOK*.md`, `*LANDMINES*.md`, `WORKFLOW*.md`
   - optional repo-local `.wip/onboarding.json` later, not day one.
5. Keep the two-hour TTL.
6. Keep canonical repo keys across worktrees.

Gate: the memory-crystal repro works cleanly:
first write blocks, `wip-branch-guard onboard <repo>` records onboarding, retry allows.

### Phase 4. Protect shared `main` as a coordination surface

Goal: prevent agents from blocking each other by making local `main` a read/sync surface, not a work surface.

1. Add an explicit shared-main policy:
   - no agent commits on `main`.
   - no local merge into `main` for visibility.
   - no fast-forwarding `main` after a worktree commit just so another session can see a file.
   - no `git pull` that would merge or rebase a dirty or divergent shared `main`.
   - after a PR is merged remotely, clean `git pull --ff-only` on local `main` is the expected read-sync path so Lēsa can read finished docs from her local main checkout.
   - `git pull --ff-only` on clean `main` is allowed only as an explicit read/sync action after remote merge, not as a deployment substitute and not as a way to make unmerged work visible.
2. Add PreToolUse detection for risky main operations:
   - `git commit` while current branch is `main`.
   - `git merge` while current branch is `main`.
   - `git rebase` while current branch is `main`.
   - `git pull` on `main` without `--ff-only`.
   - `git pull --ff-only` on `main` when local has unpushed commits or dirty files.
   - `git push origin main` from agent sessions unless a release-approved flow is active.
3. Add a proactive SessionStart advisory when an agent starts in a shared repo on `main`:
   - current repo and branch.
   - whether the checkout is shared root or linked worktree.
   - exact worktree creation command.
   - exact language: "Do not make visibility commits on this checkout. Use a branch/worktree and PR."
4. Add a branch handoff command:
   - `wip-branch-guard handoff-status`
   - prints branch name, PR URL if present, changed files, and readable local worktree path.
   - gives agents a safe alternative to "merge it to main so I can see it."
5. Add a `plan-visible` workflow:
   - for documents under `ai/product/bugs/**`, the guard suggests creating a PR early or sharing the worktree path.
   - if the user asks to see the plan before merge, the denial text points to the branch file and PR URL.
   - if the user asks to read the merged plan from local `main`, the next step is remote PR merge followed by clean `git pull --ff-only` in the local main checkout.
6. Allow release maintainers to update `main` only through an explicit approval:
   - `wip-branch-guard approve main-sync <repo> --ttl 15m --reason "..."`
   - approval allows clean `git pull --ff-only` or release-managed fast-forward only.
   - approval does not allow commits on `main`.
7. Add audit events for denied and approved main operations.

Gate: an attempted agent commit, merge, or visibility fast-forward on shared `main` denies with the worktree/PR alternative; after the PR is merged remotely, clean explicit `git pull --ff-only` on local `main` allows Lēsa's read copy to advance.

### Phase 5. Turn block messages into routing messages

Goal: a denial should route the agent to the next correct command.

1. Split denial types:
   - on main
   - on branch but not linked worktree
   - onboarding missing
   - recently denied same file
   - destructive command
   - external PR create
   - repo-tool mutation hazard
2. Every denial must include:
   - detected repo
   - detected branch
   - detected worktree status
   - exact next command
   - what not to retry
3. Add a "copy one file from main to worktree" message for the known `cp` source/destination failure class.
4. Keep messages short. Put full workflow below the exact fix, not before it.

Gate: snapshot tests for denial text. No wall-of-text first line.

### Phase 6. Fix Bash effect parsing

Goal: protect write targets, not read sources or syntax.

1. Replace first-path-wins logic for Bash commands with command-specific effect extraction.
2. Implement minimum parser coverage:
   - `cp`: destination path only.
   - `mv`: destination path plus source deletion risk.
   - `rm`: removed paths.
   - `mkdir`: created paths.
   - `touch`: touched paths.
   - redirects and `tee`: output paths.
   - `git -C`: repo context.
   - `cd ... &&`: repo context for following segment.
3. Split compound commands by segment, but preserve enough command structure for `for` loops.
4. For read-only loops, allow when every inner command is read-only.
5. For unknown write-shaped shell, bias to deny with a targeted message.

Gate: tests cover:
`cp main/file worktree/file` allows, `cp worktree/file main/file` denies, read-only `for` loop allows, loop with `rm` denies.

### Phase 7. Harden external PR approvals

Goal: keep normal fork contribution easy, keep upstream writes controlled.

1. Keep `--head wipcomputer:<branch>` as the preferred no-approval path.
2. Keep durable approvals for edge cases:
   - `wip-branch-guard approve external-pr-create owner/repo --ttl 30m --reason "..."`
3. Add `wip-branch-guard approvals list` and `approvals prune`.
4. Audit all allow and deny events into `~/.ldm/state/bypass-audit.jsonl`.
5. Update denial text to remove old env-var-first instructions. Env var stays as legacy fallback only.

Gate: tests for internal PR, external no-head deny, external `--head wipcomputer:<branch>` allow, durable approval allow, raw API deny.

### Phase 8. Make `wip-repos check` useful

Goal: separate real repo drift from local lifecycle clutter.

1. Add repo classes:
   - `active`
   - `worktree`
   - `trash`
   - `sort`
   - `sunsetted`
   - `archived`
   - `third-party`
   - `unknown`
2. Update `walkRepos()`:
   - detect `.git` files as worktrees, not regular repos.
   - ignore nested `.worktrees` by default.
   - ignore `_trash`, `_sort`, `_sunsetted` by default.
3. Add output modes:
   - default: actionable active drift only.
   - `--all`: everything.
   - `--class worktree`: just worktrees.
   - `--json`: machine-readable with class and reason.
4. Add manifest metadata for intentional non-active paths.

Gate: current machine's check should stop reporting 181 undifferentiated disk repos. It should produce a short active-drift list and a separate ignored summary.

### Phase 9. Make `wip-repos sync` safe enough to trust

Goal: repo tools should not become a backdoor around the guard.

1. Default `sync` to dry-run unless `--apply` is present.
2. Refuse to move:
   - dirty repos.
   - linked worktrees.
   - repos under `_trash` unless `--include-trash`.
   - paths with target already existing.
3. Before mutation, print an execution plan grouped by risk.
4. Add `--yes` only for CI or explicit scripted flows.
5. Add `wip-repos doctor`:
   - manifest path valid.
   - repo root valid.
   - no duplicate remotes.
   - no target collisions.
   - no worktrees inside paths that would be moved.

Gate: `sync --apply` on current machine refuses until dirty/collision/worktree risks are acknowledged or excluded.

### Phase 10. Wire release, install, and verification into one path

Goal: no more "fixed in source, stale in install" failures.

1. `wip-release` must refuse non-main invocations.
2. `wip-release` must fail if sub-tool files changed without a sub-tool version bump.
3. `wip-release` must publish changed sub-tools.
4. `wip-release` must run public sync or explicitly require `--skip-public-sync`.
5. `ldm install --alpha` must print:
   - source package version.
   - deployed extension version before.
   - deployed extension version after.
   - content hash changed or unchanged.
6. Add post-install smoke tests:
   - direct guard import.
   - PreToolUse allow for safe read.
   - PreToolUse deny for main write.
   - onboarding flow.
   - wip-repos check smoke.

Gate: one command sequence gets from merged PR to installed alpha with verified deployed content.

## Suggested PR Order

1. **PR A: Reconcile guard source with deployed 1.9.85.**
   - Source/deployed diff.
   - Import missing lock functions.
   - Version bump to 1.9.86.
   - Runtime doctor.

2. **PR B: Alpha and release repair.**
   - Fix stale alpha.
   - Enforce no older alpha.
   - Publish sub-tools.
   - Public sync.

3. **PR C: Onboarding UX.**
   - `wip-branch-guard onboard`.
   - SessionStart onboarding advisory.
   - denial text routing.

4. **PR D: Shared-main protection.**
   - block agent commits, merges, risky pulls, and visibility fast-forwards on shared `main`.
   - SessionStart advisory for shared `main`.
   - `handoff-status` and plan visibility workflow.
   - `main-sync` approval for explicit clean sync only.

5. **PR E: Bash effect parser.**
   - destination-aware `cp` and `mv`.
   - read-only loop allowance.
   - parser tests.

6. **PR F: External PR approval polish.**
   - approval listing/pruning.
   - fork-head text.
   - durable approval tests.

7. **PR G: wip-repos classification.**
   - lifecycle classes.
   - ignore defaults.
   - active drift output.

8. **PR H: wip-repos safe apply.**
   - `sync --apply`.
   - dirty/collision/worktree refusal.
   - doctor command.

## Verification Matrix

| Scenario | Expected |
|---|---|
| Install alpha after PR B | alpha is newer than latest and deploys current guard |
| Direct deployed guard version | matches source package version |
| Parallel onboarding reads | both persist in session state |
| First write in new repo | blocks with required docs and exact onboard command |
| Retry after onboard | allows in linked worktree |
| Write on main | denies with exact worktree command |
| Agent `git commit` on shared `main` | denies with worktree/PR route |
| Agent `git merge` on shared `main` | denies with worktree/PR route |
| `git pull` on shared `main` without `--ff-only` | denies |
| `git pull --ff-only` on dirty or divergent shared `main` | denies and explains divergence |
| Clean local `main` after remote PR merge | `git pull --ff-only` advances Lēsa's readable checkout |
| Clean explicit `main` sync before remote PR merge | does not make unmerged work visible; use branch path or PR URL |
| User asks to see a plan before merge | guard suggests branch file path, PR URL, or handoff status instead of local main commit |
| Read-only Bash loop | allows |
| Bash loop with write | denies |
| `cp main -> worktree` | allows |
| `cp worktree -> main` | denies |
| External PR without fork head | denies |
| External PR with `--head wipcomputer:<branch>` | allows and audits |
| `wip-repos check` default | short actionable drift list |
| `wip-repos check --all` | full inventory |
| `wip-repos sync` without `--apply` | dry-run only |
| `wip-release alpha` from worktree | refuses |

## What not to do

- Do not install `@alpha` until the alpha tag is newer than latest.
- Do not hotfix only `~/.ldm/extensions` without reconciling source and npm.
- Do not broaden shared-state allowlists to all gitignored files yet.
- Do not make `wip-repos sync` mutate by default.
- Do not remove onboarding. Make it explicit and less brittle.
- Do not make local `main` visibility commits or pre-merge fast-forwards. Use worktree paths, branch pushes, PR links, or `wip-branch-guard handoff-status` before merge; after remote merge, fast-forward local `main` with `git pull --ff-only` so Lēsa can read the final doc there.

## Final State

The guard/repo-tools work in this plan is complete for the listed tickets. The remaining active work is outside the guard folder: release-pipeline hardening and any future manifest cleanup surfaced by the now-actionable `wip-repos check` output.

The local-main process rule is now explicit: agents do implementation in worktrees, merge by PR, and only fast-forward Lēsa's local `main` after the remote PR is merged so she can read the final document from her main checkout.
