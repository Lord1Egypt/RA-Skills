# Bug: toolbox stable promotion readiness after guard and repo-tools alpha cuts

Date: 2026-04-29
Filed by: Codex
Area: release-pipeline
Status: Open
Master plan: `2026-04-24--codex--canary-release-pipeline-master-plan.md`

## Summary

The guard/repo-tools work is validated locally, but the toolbox root package is still on an alpha train:

- `@wipcomputer/wip-ai-devops-toolbox` latest: `1.9.72`
- `@wipcomputer/wip-ai-devops-toolbox` alpha: `1.9.73-alpha.8`
- `@wipcomputer/wip-branch-guard` latest: `1.9.90`
- `@wipcomputer/wip-repos` latest: `1.9.70`

The next stable promotion needs to be intentional because it promotes the whole toolbox alpha train, not just one guard patch.

LDM OS stable promotion is tracked separately because the stale-extension installer fix lives in `@wipcomputer/wip-ldm-os`, not the toolbox root package.

## Scope

- Decide whether `1.9.73-alpha.8` is ready to become the next stable toolbox release.
- Verify the guard and repo-tools runtime versions are aligned before promotion.
- Confirm that public mirror propagation is expected and safe for this stable cut.
- Resolve or explicitly defer known sub-tool publish/version-line blockers before stable.

## Known Inputs

- Guard cp regression fixed in `wip-branch-guard` 1.9.89.
- GNU `cp -t` parser follow-up fixed in `wip-branch-guard` 1.9.90.
- Repo-tools lifecycle classification shipped in `wip-repos` 1.9.69 and npm latest now reports `1.9.70`.
- LDM installer stale-extension fix shipped in `@wipcomputer/wip-ldm-os@0.4.85-alpha.2`.
- `ai/product/bugs/installer/2026-04-28--cc-mini--installer-alignment-stable-public-propagation-pending.md` tracks one universal-installer-specific public propagation blocker.

## Acceptance Criteria

1. Stable promotion decision is recorded before `wip-release patch` or equivalent runs.
2. The stable toolbox cut includes release notes that name the guard, repo-tools, and installer validation context.
3. `deploy-public` runs as part of the stable path and the public mirror reflects the promoted docs and tools.
4. npm dist-tags are verified after release.
5. Parker dogfoods stable/latest through the install prompt unless he explicitly delegates install.

## Related

- `ai/product/bugs/guard/2026-04-24--codex--guard-dev-update.md`
- `ai/product/bugs/guard/2026-04-29--codex--guard-cp-source-regression.md`
- `ai/product/bugs/installer/2026-04-28--cc-mini--installer-alignment-stable-public-propagation-pending.md`
- `ai/product/bugs/release-pipeline/2026-04-24--codex--canary-release-pipeline-master-plan.md`
