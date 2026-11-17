# Bug: toolbox shared main has dirty sub-tool version bumps

Date: 2026-04-29
Filed by: Codex
Area: release-pipeline
Status: Open
Repo: `wip-ai-devops-toolbox-private`

## Summary

The shared `main` checkout of `wip-ai-devops-toolbox-private` has local modifications in sub-tool `package.json` files that are only version bumps. They were observed while closing the guard/repo-tools work and intentionally left untouched to avoid reverting another agent's uncommitted state.

Dirty version-only package manifests are risky because they can be accidentally swept into unrelated PRs, or they may indicate incomplete release-tool behavior that bumped sub-tool versions without creating the corresponding source, changelog, and release trail.

## Current Dirty Files

Observed in the shared main checkout:

```text
tools/wip-file-guard/package.json              1.9.69 -> 1.9.70
tools/wip-license-hook/package.json            1.9.68 -> 1.9.69
tools/wip-readme-format/package.json           1.9.68 -> 1.9.69
tools/wip-repo-permissions-hook/package.json   1.9.68 -> 1.9.69
tools/wip-repos/package.json                   1.9.69 -> 1.9.70
tools/wip-universal-installer/package.json     1.9.68 -> 1.9.69
```

Registry checks showed at least some bumped versions already exist on npm, which suggests these may be release residue rather than intended new work. That should be verified before any cleanup.

## Acceptance Criteria

1. Determine whether each dirty version bump is release residue, intended pending release work, or a real local source-of-truth update.
2. If residue, clean it without reverting unrelated user work.
3. If intended, move it into a proper branch, PR, release-note, and release flow.
4. Document why the shared main checkout became dirty so the release tooling can be fixed if needed.
5. End with `wip-ai-devops-toolbox-private` shared main clean or with the remaining dirty files explicitly assigned to an active PR.

## Related

- `ai/product/bugs/release-pipeline/2026-04-24--codex--canary-release-pipeline-master-plan.md`
- `ai/product/bugs/release-pipeline/2026-04-29--codex--toolbox-stable-promotion-readiness.md`
