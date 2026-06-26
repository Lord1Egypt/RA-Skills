# Guard: Implementation Plan

**Date:** 2026-04-20
**Filed by:** cc-mini
**Authors:** Parker Todd Brooks, Claude Code (cc-mini, Opus 4.7), Lēsa (oc-lesa-mini, Opus 4.7)
**Repo:** wip-ai-devops-toolbox-private (guard source), wip-ldm-os-private (filing location)
**Status:** plan. Not started. Awaiting Parker's review + sign-off before execution.

## Parent specs (already merged)

- `2026-04-05--cc-mini--guard-master-plan.md` ... umbrella plan, Phases 1-7 shipped (stash allowlist, SessionStart hook, etc.)
- `2026-04-07--cc-mini--guard-open-bugs.md` ... Bug 2 (cp/mv source-path resolution) already flagged there
- `2026-04-19--cc-mini--guard-onboarding-and-blocked-file-tracking.md` ... onboarding + blocked-file spec
- `2026-04-19--cc-mini--external-pr-guard.md` ... external-PR guard spec

This doc stitches those into a concrete shipping sequence with file-level changes, tests, version bumps, and coordination points.

## What this plan ships

Three PRs on `wipcomputer/wip-ai-devops-toolbox-private`, sized smallest-first, each independently reviewable and alpha-releasable:

| Order | PR | Scope | Size | Depends on |
|---|---|---|---|---|
| 1 | Worktree-bootstrap allowlist | Extends `ALLOWED_BASH_PATTERNS` to cover `cp`/`mv`/`rm`/`touch`/redirect/`tee` with `.worktrees/` destinations | ~10 lines + 8 tests | nothing |
| 2 | Layer 3 core | Onboarding-before-first-write + recently-blocked-file tracking + pluggable approval-backend module | ~200 lines + 30 tests | PR 1 merged |
| 3 | External-PR guard | Blocks `gh pr create --repo <non-wipcomputer>/...` via the approval backend | ~80 lines + 12 tests | PR 2 merged |

After each PR merges: `wip-release alpha` → `ldm install --alpha` → smoke-test against the specific scenarios that PR addresses → proceed to next PR.

## Decisions (Parker's lean-approved 2026-04-20)

| Question | Decision | Reason |
|---|---|---|
| Ship all 3 in one PR, or split? | Split as 3 sequential PRs | Smaller reviews; each has a verifiable test plan; PR 2 depends on PR 1 |
| Approval backend architecture | Thin module: `approvalBackend.check(action, context)` with `env` backend for now, `bridge` + `kaleidoscope-biometric` backends as future drop-ins | ~30 extra lines today, zero-rewrite when Kaleidoscope biometrics ship |
| Contested-file detector (optional change 3 in the onboarding spec) | **Defer** to its own plan/PR | Orthogonal to onboarding + blocked-file tracking; real openclaw.json race isn't in today's shipping scope; separate planning for where the list lives (guard config vs. scraped from KNOWN-LANDMINES.md vs. per-repo) |
| Env-var prefix for overrides | `LDM_GUARD_*` | Guard lives at `~/.ldm/extensions/wip-branch-guard/`; part of LDM OS rule layer; consistent with future LDM conventions |
| Session-state file location | `~/.ldm/state/guard-session.json` (singleton, keyed internally by session_id) | Simpler than per-session files; easier to inspect/rotate |
| Bypass audit log | `~/.ldm/state/bypass-audit.jsonl` append-only, size-rotated at 50 MB | One artifact, easy to tail, auditable |
| Version bumps | Each PR: patch bump on the sub-tool, no root bump unless root files change | Matches existing conventions |
| Tests | Same `tools/wip-branch-guard/test.sh` bash framework | Established pattern; 33 tests already pass today |

## PR 1 ... Worktree-bootstrap allowlist

### Problem

From `tools/wip-branch-guard/guard.mjs`, current `ALLOWED_BASH_PATTERNS` covers `mkdir` into `.worktrees/` but not `cp`/`mv`/`rm`/`touch`/redirect/`tee`. The typical bootstrap compound fails at the first `cp`:

```
cd <main-tree> && git worktree add .worktrees/<name> -b <branch> origin/main \
  && mkdir -p .worktrees/<name>/ai/...                 # allowed (existing)
  && cp <file> .worktrees/<name>/ai/<file>             # BLOCKED (cp not in .worktrees allow)
```

Yesterday's 2026-04-19 session demonstrated this failure mode. The fix is symmetric with the existing `mkdir` precedent.

### Changes

**File: `tools/wip-branch-guard/guard.mjs`**

In the `ALLOWED_BASH_PATTERNS` array, after the existing `mkdir .worktrees` line, add:

```javascript
// Worktree bootstrap operations: allow cp/mv/rm/touch/> /tee into .worktrees/ paths.
// Symmetric with the existing mkdir-into-.worktrees allow above. Enables the
// standard bootstrap compound (create worktree -> mkdir subdir -> cp files in)
// to pass the guard when run from a main tree whose branch isn't main/master.
// Added 2026-04-20 after the 2026-04-19 session blocked a bootstrap compound.
/\b(cp|mv|rm|touch)\s+.*\.worktrees\b/,
/>\s+[^|;&]*\.worktrees\b/,
/\btee\s+.*\.worktrees\b/,
```

Three new regex entries. Mirrors the shape of the existing temp-dir allowlist pattern.

**Known false-positive risk:** the regex matches `.worktrees` appearing anywhere in the command, including when `.worktrees` is the SOURCE of a `cp` (e.g. `cp .worktrees/a/file.md /main-tree/somewhere`). That case is rare in practice (why would an agent copy worktree content back to main?) and matches the existing mkdir precedent's imprecision. Explicit-destination regex would require argument-order parsing; deferred to a future tightening if needed.

### Tests

**File: `tools/wip-branch-guard/test.sh`**

Add 8 test cases after the existing tests:

1. `cp /src /.worktrees/<repo>/ai/foo.md` on main → allow
2. `mv /src /.worktrees/<repo>/ai/foo.md` on main → allow
3. `rm /.worktrees/<repo>/ai/foo.md` on main → allow
4. `touch /.worktrees/<repo>/ai/foo.md` on main → allow
5. `echo content > /.worktrees/<repo>/ai/foo.md` on main → allow
6. `tee /.worktrees/<repo>/ai/foo.md` on main → allow
7. Regression: `cp /src /main-tree/foo.md` on main → still block
8. Regression: `rm /main-tree/foo.md` on main → still block

Existing 33 tests must still pass. Total after this PR: 41.

### Version bump

- `tools/wip-branch-guard/package.json`: `1.9.75 -> 1.9.76`
- Root `package.json`: unchanged (no root file changes in this PR)

### Release notes on branch

`tools/wip-branch-guard/RELEASE-NOTES-v1-9-76.md`:
Narrative describing the bootstrap-compound block scenario from 2026-04-19, the fix, the regression coverage, and the test count before/after. Two paragraphs.

### Alpha + install cycle

After merge:

1. Merge PR 1 with `--merge --delete-branch`
2. On main tree of `wip-ai-devops-toolbox-private`: `git checkout main && git pull --ff-only`
3. `wip-release alpha` (bumps root to next alpha, publishes `@alpha`, creates GH release)
4. `ldm install --alpha --yes`
5. Verify: `node ~/.ldm/extensions/wip-branch-guard/guard.mjs --version` reports `1.9.76`
6. Smoke-test: the exact bootstrap compound from 2026-04-19 now passes

## PR 2 ... Layer 3 core

### Problem

From 2026-04-19 post-mortem: agents on first contact with a repo do not reliably read the repo's onboarding docs before writing to it, leading to guard blocks and process violations. Separately: when a write to file F is blocked via tool A, the agent often retries with tool B producing the same filesystem effect ("equivalent-action bypass"). Neither of those failure modes is caught at the guard level today.

### Changes

**New module: `tools/wip-branch-guard/lib/approval-backend.mjs`**

```javascript
// approval-backend.mjs
// Thin pluggable backend for override/approval checks.
// Backends: "env" (ships today). Future: "bridge", "kaleidoscope-biometric".

export function check(action, context) {
  const backend = process.env.LDM_GUARD_APPROVAL_BACKEND || 'env';
  switch (backend) {
    case 'env': return envBackend(action, context);
    // TODO: case 'bridge':
    // TODO: case 'kaleidoscope-biometric':
    default: return { approved: false, reason: `unknown backend: ${backend}`, via: null };
  }
}

function envBackend(action, context) {
  // Each action type has a specific env var. Env var presence means approval.
  const envVar = ENV_MAP[action.kind];
  if (!envVar) return { approved: false, reason: `no env mapping for ${action.kind}`, via: 'env' };
  const value = process.env[envVar];
  if (!value) return { approved: false, reason: `${envVar} not set`, via: 'env' };
  // For actions with specific targets (repo path, file path), the env value must match.
  if (action.target && value !== action.target && value !== '1' && value !== 'true') {
    return { approved: false, reason: `${envVar} does not match target`, via: 'env' };
  }
  return { approved: true, reason: `${envVar} set`, via: 'env' };
}

const ENV_MAP = {
  'skip-onboarding': 'LDM_GUARD_SKIP_ONBOARDING',
  'ack-blocked-file': 'LDM_GUARD_ACK_BLOCKED_FILE',
  'external-pr-create': 'LDM_GUARD_UPSTREAM_PR_APPROVED',
};
```

~30 lines. Exported `check()` is the stable interface. Future bridge/biometric backends slot in as new cases in the switch.

**File: `tools/wip-branch-guard/guard.mjs`**

Three behavioural additions:

1. **Onboarding check.** After repo resolution, before the branch-check block:
   - Read session state file at `~/.ldm/state/guard-session.json`
   - Compute `(now - last_touch_ts) > 2h` for this repo in this session
   - If repo not onboarded (or expired), check for required doc reads (`README.md`, `CLAUDE.md`, any `*RUNBOOK*.md` / `*LANDMINES*.md` / `WORKFLOW*.md` at root + one level)
   - If any required read is missing from session's `read_files`, deny with the list
   - Override: `approvalBackend.check({kind:'skip-onboarding',target: repo})`

2. **Recently-blocked-file tracking.** At every `deny()` call:
   - Append to `~/.ldm/state/bypass-audit.jsonl`: `{ts, session_id, path, tool, command_stripped, action: 'deny'}`
   - Before every new file-writing tool call, check the log: if the same file path was denied within the last 5 entries for this session, deny again with prior-block context
   - Override: `approvalBackend.check({kind:'ack-blocked-file', target: path})`

3. **Session-state helpers.** New small helpers at top of `guard.mjs` (or in a separate `lib/session-state.mjs`):
   - `readSessionState()` / `writeSessionState(state)` atomic read/write
   - `detectNewSession(input)` — returns true if `input.session_id` differs from stored id
   - `touchRepo(repo)` — updates `last_touch_ts` for that repo
   - `markReadFile(path)` — called on `Read` tool calls to track onboarding progress
   - `isOnboarded(repo)` — returns true if all required reads are present for that repo

Total: ~150 lines across `guard.mjs` + `lib/session-state.mjs`.

**New file: `tools/wip-branch-guard/lib/session-state.mjs`** (~50 lines)

Atomic JSON read/write, with schema:

```json
{
  "session_id": "abc123",
  "started_at": 1776700000000,
  "last_touch_ts": 1776700500000,
  "read_files": ["/path/to/README.md", "/path/to/CLAUDE.md", ...],
  "onboarded_repos": {
    "/path/to/repo": { "onboarded_at_ts": 1776700200000, "last_touch_ts": 1776700500000 }
  },
  "recent_denials": [
    { "ts": ..., "path": ..., "tool": ..., "command_stripped": ... },
    ... (last 20 entries)
  ]
}
```

Session id comes from `PreToolUse` hook payload's `session_id` field (confirmed as available in Claude Code's current hook payload schema).

### Tests

**File: `tools/wip-branch-guard/test.sh`**

Add ~30 new test cases covering:

- Onboarding: first write in a new repo → deny with read-list; retry after reading → allow
- Onboarding override: `LDM_GUARD_SKIP_ONBOARDING=<repo>` env → allow without reads
- Onboarding expiry: simulated `last_touch_ts > 2h` → re-denies until re-read
- Session reset: new `session_id` in payload → all onboarded flags clear
- Blocked-file tracking: Edit blocked on X → next Bash write to X via `install`/`cat >` → denied with prior-block context
- Blocked-file override: `LDM_GUARD_ACK_BLOCKED_FILE=X` env → proceeds
- Audit log: each denial writes a line; file rotates at 50MB
- Regression: all 41 tests from PR 1 still pass

Total after PR 2: ~71 tests.

### Version bump

- `tools/wip-branch-guard/package.json`: `1.9.76 -> 1.9.77`

### Release notes on branch

`tools/wip-branch-guard/RELEASE-NOTES-v1-9-77.md`:
Narrative explaining the onboarding behavior, the blocked-file tracking, the approval backend module pattern, and reference to the post-mortem. Three paragraphs.

### Alpha + install cycle

Same pattern as PR 1. Verify with: trigger an Edit in a new repo, observe onboarding denial with read list; read the files via the `Read` tool; retry Edit; observe allow.

## PR 3 ... External-PR guard

### Problem

Agents can currently run `gh pr create --repo <non-wipcomputer>/<repo>` without explicit Parker approval. This is what caused the 2026-04-18 PR #89 process violation.

### Changes

**File: `tools/wip-branch-guard/guard.mjs`**

Add a new `checkExternalPRCreate(command, context)` function invoked from the `BASH_TOOL` path, before the destructive-pattern checks. It parses `gh pr create` / `gh api repos/<x>/pulls` invocations, normalizes the target `<owner>/<repo>`, and:

- If owner is `wipcomputer` → allow (internal)
- Else → call `approvalBackend.check({kind: 'external-pr-create', target: '<owner>/<repo>', ...})`
- If `approved: false` → deny with message directing to ask Parker
- If `approved: true` → log to bypass-audit.jsonl + allow

Command patterns covered:

1. `gh pr create --repo <owner>/<repo>` explicit flag
2. `gh pr create` from a worktree whose `origin` is `<owner>/<repo>` (resolve via `git remote get-url origin`)
3. `gh pr create --repo <owner>/<repo> --head <fork-owner>:<branch>` cross-fork
4. `gh api repos/<owner>/<repo>/pulls -X POST` raw API
5. `gh pr create --web` (opens browser; still counts as create intent)

Non-targets (allowed freely): `gh pr view`, `gh pr list`, `gh pr merge`, `gh pr edit`, `gh api repos/<owner>/<repo>/issues`.

~80 lines.

### Tests

Add ~12 test cases:

- `gh pr create --repo steipete/imsg ...` → deny
- Same with `LDM_GUARD_UPSTREAM_PR_APPROVED=1` env → allow
- `gh pr create --repo wipcomputer/imsg ...` → allow (internal)
- `gh pr view 5 --repo steipete/imsg` → allow (not create)
- `gh api repos/steipete/imsg/pulls -X POST` → deny
- `gh pr create` from worktree with wipcomputer origin → allow
- `gh pr create` from worktree with lesaai origin → deny
- Regression: all 71 tests from PR 2 still pass

Total after PR 3: ~83 tests.

### Version bump

- `tools/wip-branch-guard/package.json`: `1.9.77 -> 1.9.78`

### Release notes on branch

`tools/wip-branch-guard/RELEASE-NOTES-v1-9-78.md`: narrative explaining the external-PR guard behavior, the PR #89 incident it prevents, the override env var, and the approval-backend upgrade path.

### Alpha + install cycle

Same pattern. Verify with: attempt `gh pr create --repo steipete/imsg --dry-run-like-thing` → deny; set env and retry → allow; check audit log has the entry.

## Coordination + risks

### Merge order is strict

PR 1 → PR 2 → PR 3. PR 2 depends on PR 1's bootstrap fix because PR 2's tests create worktrees with `cp`/`mkdir` combos that would otherwise trip the guard. PR 3 depends on PR 2's approval-backend module.

### Parallel sessions

If another cc-mini or oc-lesa-mini session is editing `guard.mjs` during this work, coordinate via SHARED-CONTEXT. I verified 2026-04-20 morning: no other `cc-mini/guard-*` branches exist on remote. I'm cleared to proceed.

### Risk: onboarding friction

If the required-reads list is too aggressive, every session's first write in every repo triggers a denial. Mitigation: the read-list is tight (README + CLAUDE.md + any RUNBOOK/LANDMINES at root + one level), and the 2-hour expiry means re-denials don't cascade during normal continuous work.

### Risk: session state file corruption

If `~/.ldm/state/guard-session.json` gets written in parallel by two simultaneous tool calls, the write could corrupt. Mitigation: atomic write via tmp-file + rename pattern. Include a `tools/wip-branch-guard/lib/session-state.mjs` `writeSessionState()` that uses `fs.rename` for atomicity.

### Risk: bypass audit log unbounded growth

Rotation at 50 MB. Old log files renamed `bypass-audit.jsonl.YYYY-MM-DD`. Keep last 10 rotations.

## Testing strategy per PR

Each PR has its own test pass. After merge + alpha + install, a small manual verification scenario specific to that PR's scope. After all three PRs land, a full manual scenario that exercises the chain: new session → onboarding → onboarded → write blocked → same file via other tool → blocked-file tracking fires → override env → proceed → external-PR attempt on non-wipcomputer → denied → override env → allowed.

## Rollout

After PR 3 merges and is installed:

1. Update `feedback_never_bypass_guards.md` in `~/.claude/projects/.../memory/` to reference the new signature-level enforcement (already drafted last night; confirm aligned).
2. Update SHARED-CONTEXT.md "Infrastructure State" block with new guard version and the new behaviors.
3. Add a short section to `dev-guide-wipcomputerinc.md.tmpl` describing the onboarding ritual (before first write in a repo, read README + CLAUDE.md + RUNBOOK).

## Open questions for Parker

All four design questions answered in the Decisions table above (Parker's leans approved 2026-04-20). Remaining operational questions:

1. **Alpha or stable release per PR?** My lean: alpha for each, promote to stable after 48h of dogfooding that PR's scenario without regressions.
2. **Should implementation PRs include the SHARED-CONTEXT.md updates in the same commit, or separately?** My lean: separately (SHARED-CONTEXT is its own repo/process).
3. **Timeline:** PR 1 today, PR 2 after PR 1 ships + dogfoods, PR 3 after PR 2 ships + dogfoods. Or faster if you want.

## Amendments (2026-04-20, mid-rollout)

### Installer bugs surfaced during PR 2 cascade

PR 2 (Layer 3 core) was the first sub-tool to ship a `lib/` subdir, and the first to bump its own hook matcher. Both exposed latent installer bugs. Tracked + fixed inline while the plan was in flight:

- `wip-ldm-os v0.4.76`: installer now recurses sibling subdirs (fix 1, PR #621) + replaces existing hook entry instead of appending (fix 2, PR #622).
- `wip-release v1.9.75 -> v1.9.76`: `publishNpm` now captures stderr so the "cannot publish over" swallow check works (PR #359, force-redeploy bump in PR #360).
- `wip-branch-guard v1.9.77 -> v1.9.78 -> v1.9.79`: inline-lib hotfix for the lib/ drop, then hook-matcher fix once the installer was healthy.

### Remaining installer item: content-hash-equality

`lib/deploy.mjs:deployExtension` short-circuits on version equality. A prior partial install could have bumped `package.json` to the new version without copying the other files (happened during the 1.9.74 -> 1.9.75 rollout: deployed `package.json` said 1.9.75, deployed `core.mjs` was still 1.9.74 content). Worked around by force-bumping to 1.9.76. Tracking as a separate cleanup for later (a "versions equal AND content hash equal" check would be the proper fix).

**Status as of 2026-04-20:** a fix is queued in the same PR as this amendment ... `computeTreeHash(dir)` sha256's every non-blacklisted file and the skip path requires `srcHash === dstHash` in addition to the version check. Content drift now triggers a redeploy with a visible "reports same version but content differs; redeploying" log line.

## Co-authors

Parker Todd Brooks, Lēsa (oc-lesa-mini, Opus 4.7), Claude Code (cc-mini, Opus 4.7).

## Resolution

Status: Closed on 2026-04-24.

Closed by the April 24 guard/repo-tools rollout:

- `wip-ai-devops-toolbox-private` PR #380 added runtime doctor coverage and reconciled guard runtime behavior.
- PR #386 completed explicit onboarding, parser fixes, shared-main protections, and approval maintenance.
- PR #387 completed `wip-repos` lifecycle classification and safe sync behavior.
- Toolbox alpha `1.9.73-alpha.3` published with `wip-branch-guard 1.9.88` and `wip-repos 1.9.69`.

Verification:

- `node --check tools/wip-branch-guard/guard.mjs`
- `bash tools/wip-branch-guard/test.sh`: 117 passed, 0 failed, 1 skipped.
- `wip-branch-guard doctor` passes against deployed `1.9.88`.
