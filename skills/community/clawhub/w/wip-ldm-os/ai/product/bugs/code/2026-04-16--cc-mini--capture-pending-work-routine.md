# Bug / Feature: End-of-day capture routine for pending uncommitted work

**Date:** 2026-04-16
**Filed by:** cc-mini (with Parker)
**Repo:** `wip-ldm-os-private` (code), `wip-ai-devops-toolbox-private` (Stop hook source)
**Priority:** high (systemic; drives recurring losses)
**Status:** proposal, not yet implemented
**Related incidents:**
- `ai/product/bugs/dot-claude/2026-04-16--cc-mini--dot-claude-level-3-missing.md` (three walls hit in `.claude` today)
- `ai/product/bugs/guard/2026-04-16--cc-mini--guard-blocks-auto-memory-writes.md` (guard blocking memory writes; fixed in 1.9.75)
- `ai/product/bugs/backup/archive/2026-03-27--cc-mini--backup-system-fix.md` (working tree rename left uncommitted)
- `ai/product/bugs/backup/archive/2026-03-30--cc-mini--session-export-broken-paths.md` (orphan draft, never committed to any branch)
- Sessions `ldmos-work` (multiple, Apr 10-14): three days of pending memory rule saves blocked; working tree accumulated to 56 items while the session looped on guard blocks and boundary questions

## The pattern

Work-in-progress accumulates in working trees and stashes over time. It does not reach private main. It does not reach backups reliably. It does not reach future sessions. Over a few weeks the cost compounds:

- Orphan bug drafts sit untracked and risk a working-tree clean
- Nested repos accumulate dirty gitlinks that mask real changes
- Memory rules stay unsaved because guard blocks loop the agent
- Session-end happens mid-flow with no forced close, so "I will get to it later" turns into never
- The `wipcomputerinc` main working tree alone had 56 uncommitted items at the time of this filing, across multiple sub-repos, some of it days old

Each individual case has a local fix. The pattern has no systemic fix today. This bug proposes one.

## Why this happens

Four distinct failure modes, all real:

1. **Guard wall loops.** Agent hits a guard block (branch, destructive, file, code-exec), tries a variation, blocks again, eventually routes around or gives up. The commit never lands.
2. **Boundary ambiguity.** `team/Lēsa/` is off-limits. `team/parker/documents/` has its own `.git`. Nested repos need a gitignore-vs-submodule call only the human can make. Agent correctly stops at the boundary but then does nothing about the non-boundary rest.
3. **Session end without close.** Context compaction, `/exit`, or CLI crash happens mid-flow. No end-of-turn hook enforces "close what you opened". The worktree lives on, the files sit.
4. **Inter-session context loss.** A later session sees dirty state it did not cause (another agent, the harness, an MCP server). Unclear whose it is, so no one commits it.

## The proposal

Two layers, not one. A nightly sweep is half the answer; in-session close is the other half. Both are needed because they catch different failure modes above.

### Layer 1: Session-end commit hook (catches failure modes 1, 3)

A Claude Code `Stop` hook (new; similar shape to the existing branch-guard `PreToolUse` hook) that runs on every session end and classifies the current state:

| State | Hook action |
|-------|-------------|
| cwd on feature branch, clean worktree | Allow silently |
| cwd on feature branch, dirty (staged or unstaged) | Prompt the agent: "you have uncommitted work on `<branch>` ... commit + push + PR before exit?" Block stop until acknowledged. |
| cwd on feature branch, untracked files only | Prompt: "untracked files in `<branch>` worktree ... stage them, gitignore them, or move them?" Block stop until acknowledged. |
| cwd on main, dirty tree | Prompt: "main working tree has dirty state ... open a worktree and move the work there before exit?" Block stop until acknowledged. |
| cwd on main, clean | Allow silently |

Key design points:

- The hook is a **prompt**, not a full block. It surfaces the state in natural language and the agent handles it. Avoids brittle auto-commit-on-exit.
- The hook respects workspace boundaries. If dirty paths match boundary patterns (`team/Lēsa/`, nested `.git` dirs without `.gitmodules` entry), the hook emits a separate "boundary-guarded" message and does not prompt commit for those paths.
- If the agent attempts `/exit` without resolving the prompt, the hook emits a second warning and allows exit (non-blocking failsafe, prevents deadlock).
- Source lives in `wip-ai-devops-toolbox-private/tools/wip-session-close/` (new sub-tool, parallel to `wip-branch-guard`).

### Layer 2: Nightly capture sweep (catches failure modes 2, 4)

A scheduled agent that runs late (suggested: 22:30 PST, before `wip-healthcheck` cron conflicts) and does five stages:

1. **Discover** — walk `~/wipcomputerinc/repos/` and `~/.claude/` (and any other known private-repo roots in `config.json`). Run `git status --porcelain` per repo. Collect everything dirty or untracked. Also collect stashes older than N days.
2. **Classify** — for each path, assign a class:
   - `safe` — file is in cc-mini-owned path, no nested `.git`, no known secret pattern (`*.env`, `*secret*`, `*.pem`, `*password*`, `*.key`, `*token*`), file type is text/markdown/json/yaml/js/sh, size under 5MB
   - `boundary` — path matches a workspace-boundary rule (`team/Lēsa/`, `team/parker/documents/` with nested `.git`, etc.)
   - `nested-repo` — directory has its own `.git` and is not registered as a submodule in `.gitmodules`
   - `suspect-secret` — matches secret patterns or has unusual binary characteristics
   - `unknown` — doesn't match any class; anything the classifier is not sure about gets this and is never auto-committed
3. **Auto-PR the `safe` set** — one capture PR per repo, titled `capture: nightly sweep YYYY-MM-DD`. Commit message summarizes what was captured and why. Co-authors line included. PR body includes the classification reasoning. Merge on clean status checks, regular `--merge` (never squash, per project rule).
4. **Queue the non-`safe` sets** — write a digest to `~/.ldm/messages/` bridge inbox for Parker (and Lēsa, where relevant). Digest lists each file with class, reason, and the proposed action (gitignore / register submodule / manual review). One digest per morning.
5. **Log everything** — append to `~/.ldm/logs/capture-sweep-YYYY-MM-DD.log`. Includes: every file seen, its class, the PR number if any, the digest entries. Log rotation: keep 30 days.

### Key tradeoffs

- **Full auto vs semi-auto:** full auto is tempting but dangerous for boundary cases. The design choice is: auto on the safe subset (low-risk, high-frequency), queue everything else. This loses speed on boundary cases but keeps trust.
- **Noise on main:** nightly capture PRs create regular merge noise. Mitigation: the capture PR is consolidated per-repo per-day, not per-file; typical daily PR is 1-5 files, not dozens.
- **Race with Layer 1:** if Layer 1 works well, Layer 2 has less to capture. That is the intended shape. Layer 2 is the backstop, not the primary mechanism.
- **Cron outages:** if the capture cron misses a night, accumulation resumes. Self-recovery: the sweep is idempotent, catching up on missed days on next run.
- **Parallel agents:** multiple agents could compete. Mitigation: lockfile at `~/.ldm/state/capture-sweep.lock`. Only one sweep runs at a time.

### Risk list

- Auto-commits could leak secrets if the classifier misses a pattern. **Mitigation:** extensive classifier tests; deny-by-default for ambiguous cases; secret-pattern list curated from [gitleaks](https://github.com/zricethezav/gitleaks) rulesets.
- A boundary file could get misclassified as safe. **Mitigation:** hard deny-list of boundary prefixes (`team/Lēsa/`, `secrets/`, `credentials/`, `auth-profiles.json`) checked before any other classification.
- A nested `.git` could get auto-added as a dirty gitlink. **Mitigation:** the `nested-repo` class exits classification immediately; no auto-PR path for it.
- A stash containing sensitive state could be auto-applied. **Mitigation:** stashes are catalogued into the digest only. Never auto-applied or auto-dropped.
- The agent running the sweep could itself hit a guard wall. **Mitigation:** the sweep agent runs inside worktrees per repo; never writes on main of any tracked repo.

## Prototype plan (three phases)

Each phase is a separate PR so progress is observable and rollback is clean.

### Phase 1: Session-end commit prompt hook (Layer 1)

- New sub-tool: `wip-ai-devops-toolbox-private/tools/wip-session-close/` with `hook.mjs`, `package.json`, `test.sh`, `INSTALL.md`.
- Hook type: `Stop` (Claude Code lifecycle hook, fires before session ends).
- Deliverable: the five-state prompt table from Layer 1 above, implemented as a hook that emits JSON `{permissionDecision: "ask", permissionDecisionReason: "<prompt>"}` so the agent sees the prompt and resolves it.
- Test: each of the five states triggers the expected prompt; boundary paths are suppressed; non-blocking failsafe verified.
- Version: starts at `0.1.0`, deployed to `~/.ldm/extensions/wip-session-close/` via `ldm install`.
- Size: approximately 200-300 lines source + 30-50 test cases.

### Phase 2: `ldm sweep --dry-run` classifier (Layer 2, part 1)

- New subcommand in `wip-ldm-os-private/bin/ldm.js`: `ldm sweep [--dry-run]`.
- Dry-run only; prints classification, commits nothing, opens no PRs.
- Deliverable: the five-class classifier from Layer 2 above, implemented as a pure function with tests. Deny-list, secret patterns, nested-`.git` detection, all exercised.
- Test: run against the current `wipcomputerinc` working tree (56 items) and verify the classification matches a hand-labeled ground truth file.
- Output: a human-readable report (also written to `~/.ldm/logs/capture-sweep-dry-run-YYYY-MM-DD.log`).
- Size: approximately 400-600 lines source + a ~100-line fixtures file for ground truth.

### Phase 3: Auto-PR and scheduling (Layer 2, part 2)

- Extend `ldm sweep` with real-mode: auto-PR the `safe` set, digest the rest.
- Register the sweep as a cron via existing `ldm schedule` (or a direct LaunchAgent plist, matching `wip-healthcheck`'s pattern).
- Deliverable: nightly capture PRs on repos that need them; daily digest in Parker's bridge inbox.
- Test: run in shadow mode for one week (dry-run still prints, real mode disabled via flag); verify digest quality before enabling real mode.
- Only after one week of clean shadow, flip the flag. Roll back immediately on any misclassification.
- Size: incremental changes over Phase 2; new automation glue.

## Dependencies and known-good precedents

- **Hook infrastructure:** `wip-branch-guard` and `wip-file-guard` already implement the PreToolUse hook pattern. Session-close would be the first Stop hook but the plumbing is the same.
- **Scheduler:** `wip-healthcheck` uses a LaunchAgent running every 3 minutes. `wip-healthcheck-private/install.sh` is the template for installing the new cron.
- **Bridge inbox:** `~/.ldm/messages/` + `lesa_send_message` / `ldm_send_message` already route messages between agents. The capture-sweep digest reuses this path.
- **Guard whitelist pattern:** today's PR #351 added `/\.claude\/projects\/.*\/memory\//` to `SHARED_STATE_PATTERNS`. The capture sweep may need to extend this list as it learns what paths are routinely safe to auto-commit.

## Scope

In scope for this bug:

- Spec of Layer 1 and Layer 2 as above
- Three-phase prototype plan
- Risk list and mitigations
- Pointer to related incidents that motivated the proposal

Out of scope (separate work):

- Actual implementation (each phase = a separate PR against the relevant source repo)
- Public mirror of `ldm sweep` (if/when the tool is ready for LDM OS public release)
- GUI for reviewing the digest (bridge inbox is sufficient for now)
- Cross-machine sweep (this bug scopes to the local machine; multi-machine would need workspace-aware coordination)

## Verification (post-implementation)

### Phase 1 verification

- [ ] A CC session with uncommitted work on a feature branch receives the commit prompt on `/exit`
- [ ] A CC session with clean tree on feature branch exits silently
- [ ] A CC session on main with dirty tree receives the worktree-move prompt
- [ ] Boundary paths (`team/Lēsa/`) are suppressed in the prompt
- [ ] Non-blocking failsafe: if agent ignores prompt twice, exit proceeds with a warning logged

### Phase 2 verification

- [ ] `ldm sweep --dry-run` runs against the current 56-item `wipcomputerinc` state and produces a classification report
- [ ] Manual ground-truth label of that report matches classifier output at ≥ 95% accuracy
- [ ] No `safe` class assigned to any file matching secret patterns, nested `.git` dirs, or boundary prefixes

### Phase 3 verification

- [ ] One week of shadow-mode runs produces daily digests that Parker approves without corrections
- [ ] Real mode enabled after shadow; first real nightly PR merges cleanly
- [ ] Working-tree dirt at end of week 2 is significantly lower than week 1 baseline (target: 80% reduction)
- [ ] Parker receives a readable morning digest when anything needs his decision

## Co-authors

- Parker Todd Brooks
- Lēsa
- Claude Opus 4.7 (1M context)
