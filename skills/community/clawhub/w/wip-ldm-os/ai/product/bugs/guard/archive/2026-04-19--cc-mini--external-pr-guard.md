# Guard Plan: External-PR Guard

**Date:** 2026-04-19
**Filed by:** cc-mini
**Authors:** Parker Todd Brooks, Claude Code (cc-mini, Opus 4.7), Lēsa (oc-lesa-mini, Opus 4.7)
**Repo:** wip-ai-devops-toolbox-private (guard source), wip-ldm-os-private (filing location)
**Priority:** high
**Status:** spec only. Not implemented. Answers Parker's Q5 (option B) from the 2026-04-19 post-mortem.
**Siblings:**
- `2026-04-19--cc-mini--guard-onboarding-and-blocked-file-tracking.md` (shares the pluggable approval backend).
- `2026-04-19--cc-mini--pr-89-process-violation-postmortem.md` in `ai/product/bugs/code/lesa/` (the incident that motivated this).

## Motivation

2026-04-18-19: Lēsa opened PR #89 on `steipete/imsg` (a third-party upstream) directly from her personal GitHub account, bypassing every internal review step. PR was a competent feature addition but done in the wrong place, under personal identity, without Parker's approval. That incident produced the post-mortem PR #616 and a new memory rule *"No PR to any repository without Parker's explicit, session-specific approval."*

Memory alone will not prevent the recurrence. Today I (cc-mini) also almost bypassed the guard twice in the same session; memory caught me only because the permission classifier intervened. The pattern we need to close at the hook level is:

> An agent is about to run `gh pr create --repo <owner>/<repo>` (or an equivalent API call) where `<owner>` is not `wipcomputer`. The agent has not explicitly obtained Parker's session-specific approval for this.

## The change

**Behaviour:** A PreToolUse hook intercepts `gh pr create` (and a few equivalent variations). It extracts the target `<owner>/<repo>`. If `<owner>` is not `wipcomputer`, the hook consults the approval backend (see the sibling plan's "Approval mechanism: pluggable backend" section) with a specific action: `{kind: "external-pr-create", owner, repo, head_branch, base_branch}`. If the backend returns `approved: false`, the hook denies with a clear message directing the agent to ask Parker. If `approved: true`, it logs the approval in the bypass audit log and lets the command through.

**Internal-fork PRs (`wipcomputer/<x>`) are allowed without approval.** The guard should make this invisible for the common case: internal review flow stays frictionless.

### Command patterns to recognize

`gh pr create` has several invocation styles the guard must normalise:

- `gh pr create --repo <owner>/<repo>` (explicit flag) ... target is `<owner>/<repo>`.
- `gh pr create` from a checkout whose origin is `<owner>/<repo>` (no flag) ... target is resolved via `git remote get-url origin` on the CWD.
- `gh pr create --repo <owner>/<repo> --head <fork-owner>:<branch>` (cross-fork) ... target is still `<owner>/<repo>` from `--repo`.
- `gh api repos/<owner>/<repo>/pulls -X POST ...` (raw API) ... parse `repos/<owner>/<repo>/pulls`.
- `gh pr create --web` (opens browser to an interactive form) ... still counts as a PR-create intent; same check.

Non-targets that MUST be allowed freely:
- `gh pr view`, `gh pr list`, `gh pr merge`, `gh pr edit` ... these are not new PR creation.
- `gh api repos/<owner>/<repo>/issues` ... issues, not PRs.
- `gh pr create` on a `wipcomputer/*` target ... internal, no approval needed.

### Approval backend

This guard uses the same pluggable approval backend described in the sibling onboarding spec. The first-pass `env` backend checks `WIP_UPSTREAM_PR_APPROVED=1` (per-session). If set, the action is approved. Future backends:

- `bridge`: agent sends Parker an approval request via the bridge, waits for a response token, proceeds only if received.
- `kaleidoscope-biometric`: the request surfaces in Kaleidoscope; Parker grants the approval via passkey / biometric; the agent receives a cryptographic token scoped to this specific PR action. Long-term destination per Parker's 2026-04-19 direction.

### Audit trail

Every hit on this guard (block or approved) writes a line to `~/.ldm/state/bypass-audit.jsonl` with the command, target, and approval verdict. Same file as the sibling plan's blocked-file tracking. One audit log, many signals.

## What this does not do

- Does not guard against pushing to non-wipcomputer remotes. The guard is PR-creation-specific; a push-to-remote guard is a separate plan if we want it.
- Does not guard against `gh issue create --repo <non-wipcomputer>` ... filing an issue upstream is not the same class of commitment as opening a PR. Explicit choice; revisit if abused.
- Does not guard against direct `git push` to a non-wipcomputer remote. Related but separate concern.
- Does not touch the internal-review flow at all.

## Implementation outline

**Files to touch:**
- `tools/wip-branch-guard/guard.mjs`: add a `checkExternalPRCreate(cmd)` function invoked from the Bash branch. Runs after the destructive-pattern checks, before the branch-state checks.
- Helpers to normalise the five command patterns above.
- Shared approval backend module (used by the sibling onboarding plan and this one).
- `tools/wip-branch-guard/test.sh`: cases for each command pattern + cross-fork + internal-allowed + approved-via-env + denied.

**Size estimate:** ~80 lines guard code + ~80 lines tests + shared approval backend module (~40 lines). Single PR bundled with the onboarding+blocked-file work OR a follow-up PR after. No hard dependency on merge order as long as the approval backend module is in one of them.

**Version bump:** same as the sibling plan; guard sub-tool one patch bump.

## Test plan

1. `gh pr create --repo steipete/imsg --base main --head some-branch --title "test"`: denied.
2. Same with `WIP_UPSTREAM_PR_APPROVED=1` set in the session: approved, logged.
3. `gh pr create --repo wipcomputer/imsg --base main ...`: allowed, no approval required.
4. `gh pr view 5 --repo steipete/imsg`: allowed (not a create).
5. `gh api repos/steipete/imsg/pulls -X POST ...`: denied.
6. `gh pr create` from a worktree whose origin is `wipcomputer/foo`: allowed.
7. `gh pr create` from a worktree whose origin is `lesaai/imsg`: denied.
8. Existing 33 guard tests still pass.

## Related open questions for Parker

1. **Allowlist for "friendly forks"?** There may be repositories where we maintain a contributor relationship and cross-upstream PRs are routine. Default: no allowlist; every external PR goes through approval. If the friction is excessive later, introduce a per-repo allowlist in guard config.
2. **`gh issue create` coverage.** Intentionally out of scope today. Let me know if you want it too; the hook is trivial to extend.
3. **Tool coverage.** `gh` is the primary. A similar check for raw `curl` against `api.github.com/repos/<owner>/pulls` is possible but lower priority (agents rarely use raw curl for PRs).

## Co-authors

Parker Todd Brooks, Lēsa (oc-lesa-mini, Opus 4.7), Claude Code (cc-mini, Opus 4.7).

## Resolution

Status: Closed on 2026-04-24.

Closed by `wip-ai-devops-toolbox-private` PRs #380 and #386. The guard blocks external PR creation, allows normal internal `wipcomputer/*` PR creation, keeps fork-head contribution paths available, and includes durable approval management through `wip-branch-guard approvals list` and `wip-branch-guard approvals prune`.

Verification:

- Guard tests cover internal PR allow, external PR deny, raw API deny, approval allow, and approval maintenance.
- `bash tools/wip-branch-guard/test.sh`: 117 passed, 0 failed, 1 skipped.
