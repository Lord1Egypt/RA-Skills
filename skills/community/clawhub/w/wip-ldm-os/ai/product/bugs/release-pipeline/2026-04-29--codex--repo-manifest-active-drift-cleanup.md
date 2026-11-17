# Bug: repo manifest active drift blocks release-pipeline enrollment

Date: 2026-04-29
Filed by: Codex
Area: release-pipeline
Status: Open
Master plan: `2026-04-24--codex--canary-release-pipeline-master-plan.md`
Parent phase ticket: `2026-04-27--codex--phase-0-release-enrollment-inventory.md`

## Summary

`wip-repos check` and `wip-repos release-enrollment` are now useful enough to separate lifecycle noise from real active drift. The remaining blocker is data cleanup: active repos on disk still need explicit manifest ownership, release enrollment metadata, or an intentional exclusion.

This is not a guard bug. The guard/repo-tools work made the signal actionable; this ticket owns the follow-up manifest cleanup that the guard dev update calls out as outside the guard batch.

## Current Signal

The Phase 0 release-enrollment ticket recorded the post-MVP state:

```text
Active manifest repos: 53
Enrolled:              2
Excluded:              0
Needs decision:        42
Missing on disk:       9
Unmanifested active:   21
Blockers:              30
```

That means the release pipeline cannot safely fan out shared CI or promotion gates across the repo fleet yet.

## Scope

- Reconcile active repos on disk with `repos/repos-manifest.json`.
- Decide whether each active repo is canonical, archived, generated, third-party, runtime-only, or intentionally unmanaged.
- Add release metadata or exclusion reasons for each active repo.
- Preserve lifecycle-folder classification from `wip-repos check`; do not turn trash, worktrees, or third-party clones into release-owned repos.

## Acceptance Criteria

1. `wip-repos check` has no unexplained active drift.
2. `wip-repos release-enrollment --strict --json` exits cleanly or reports only deliberately deferred release-profile decisions.
3. Every active repo is either manifest-owned or explicitly excluded with a reason.
4. Every release-owned repo has enough metadata for later CI and release-gate rollout.
5. The Phase 0 release-enrollment ticket is updated with the final before/after counts.

## Related

- `ai/product/bugs/guard/2026-04-24--codex--guard-dev-update.md`
- `ai/product/bugs/release-pipeline/2026-04-24--codex--canary-release-pipeline-master-plan.md`
- `ai/product/bugs/release-pipeline/2026-04-27--codex--phase-0-release-enrollment-inventory.md`
