# wip-branch-guard v1.9.80

## External-PR create guard (PR 3 of the 2026-04-20 implementation plan)

The 2026-04-18 PR #89 incident: an agent ran `gh pr create --repo steipete/imsg ...` (upstream, not a WIP Computer repo) without Parker approving the intent. Nothing in the guard blocked it because `gh pr create` was a straight allow-listed command.

This release adds a targeted block on that exact shape. `gh pr create` and raw `gh api repos/<owner>/<repo>/pulls -X POST` against any owner other than `wipcomputer/` now go through the approval backend (same `approvalCheck` module Layer 3 uses). Override: `LDM_GUARD_UPSTREAM_PR_APPROVED=<owner>/<repo>` for a target-specific approval, or `=1` for a blanket run-level approval. Every approval lands in `~/.ldm/state/bypass-audit.jsonl` with kind `external-pr-create-approved`.

## Recognized shapes

- `gh pr create --repo <owner>/<repo>` (explicit flag, with or without `--head <fork>:<branch>` cross-fork)
- `gh pr create [--web] [--title ... --body ...]` (no --repo flag; origin is resolved from the cwd's git repo via `git remote get-url origin`)
- `gh api repos/<owner>/<repo>/pulls ... -X POST` (raw API form)

## Not affected

`gh pr view`, `gh pr list`, `gh pr merge`, `gh pr edit`, and `gh api repos/<owner>/<repo>/issues` all pass through. The guard is scoped to PR creation, not PR interaction. You can still merge or comment on external PRs that already exist.

## Files

- `tools/wip-branch-guard/guard.mjs`: new `parseExternalPRCreate(command, cwd)` helper (~35 lines) and a block in `main()` between the dangerous-flags check and the release-cooldown check (~45 lines). Reuses the existing `approvalCheck` and `appendAudit`.
- `tools/wip-branch-guard/test.sh`: 12 new test cases covering explicit flag, implicit origin, override variants, raw API POST, and non-target shapes that should still pass through.
- `tools/wip-branch-guard/package.json`: version 1.9.79 -> 1.9.80, description updated.

## Tests

80 passing, 0 failing, 8 main-only skipped. Up from 68.

## Closing the plan

This completes the 3-PR sequence from `wip-ldm-os-private/ai/product/bugs/guard/2026-04-20--cc-mini--guard-implementation-plan.md`:

1. v1.9.76 (PR 1) ... worktree-bootstrap allowlist
2. v1.9.77 / v1.9.78 / v1.9.79 (PR 2 + hotfix cascade) ... onboarding + blocked-file tracking + approval backend + hook matcher
3. v1.9.80 (PR 3, this release) ... external-PR guard

The approval backend's `ENV_MAP` already exposed `external-pr-create` as a kind, reserved for this PR in PR 2. No backend module changes needed.

## Related

- Triggering incident: `wip-ldm-os-private/ai/product/bugs/code/lesa/2026-04-19--cc-mini--pr-89-process-violation-postmortem.md`
- Spec: `wip-ldm-os-private/ai/product/bugs/guard/2026-04-19--cc-mini--external-pr-guard.md`
- Implementation plan: `wip-ldm-os-private/ai/product/bugs/guard/2026-04-20--cc-mini--guard-implementation-plan.md`
