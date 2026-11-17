# Bug: guard approvals still rely on env fallback instead of bridge or biometric approval

Date: 2026-04-29
Filed by: Codex
Area: guard
Status: Open
Implementation repo: `wip-ai-devops-toolbox-private`

## Summary

The guard now has a scoped approval path for external PR creation, but the live backend is still env-based. That was acceptable for the guard rollout because the approval interface was designed to be swappable, but the intended long-term destination is a Bridge or Kaleidoscope biometric approval backend.

This is not blocking the 2026-04-29 guard closeout. It is the active follow-up for replacing operator env vars with an approval flow that Parker can grant through the product surface.

## Current State

Implemented:

- External PR creation is denied by default for non-WIP Computer repos.
- Internal WIP Computer PR work is allowed.
- `LDM_GUARD_UPSTREAM_PR_APPROVED` can approve a specific external target or the current process.
- Approval uses the inlined approval backend interface, so future backends should be drop-in replacements.
- Bypass/approval use is audit-logged.

Still missing:

- Bridge-backed approval request flow.
- Kaleidoscope/passkey/biometric grant flow.
- Cryptographic or scoped token handoff back to the guard.
- Expiry and target scoping that do not depend on shell environment variables.

## Acceptance Criteria

1. Add a non-env approval backend implementation behind the existing approval interface.
2. Approval requests include action kind, target repo, branch context, command, session id, and expiration.
3. Parker can approve or deny from the Bridge or Kaleidoscope surface without editing shell env.
4. Approval is scoped to the exact action or target repo and expires automatically.
5. Approval and denial events are written to the guard audit log.
6. Env fallback remains available only as a documented break-glass path, or is removed after the product approval path is proven.
7. Tests cover allowed, denied, expired, wrong-target, and audit-log cases.

## Related

- `ai/product/bugs/guard/archive/2026-04-19--cc-mini--external-pr-guard.md`
- `ai/product/bugs/guard/archive/2026-04-19--cc-mini--guard-onboarding-and-blocked-file-tracking.md`
- `ai/product/bugs/guard/archive/2026-04-20--cc-mini--guard-implementation-plan.md`
- `ai/product/bugs/guard/2026-04-24--codex--guard-dev-update.md`
