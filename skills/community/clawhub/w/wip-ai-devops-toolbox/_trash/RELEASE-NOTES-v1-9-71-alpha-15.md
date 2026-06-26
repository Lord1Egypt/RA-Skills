# Release Notes: wip-ai-devops-toolbox v1.9.71-alpha.15

## Phase 3: True publish-before-commit

The release pipeline now publishes to npm BEFORE creating the git commit. Previously the order was commit -> publish -> push. If npm failed, the commit and tag were already created, requiring manual rollback.

New order: bump files -> npm publish -> (on success) commit+tag -> push. If npm publish fails, file changes are reverted with `git checkout -- .`. No commit exists. No tag exists. No remote state changed. Clean retry.

## Phase 5: Auto-publish sub-tools to npm

After the root package publishes successfully, the pipeline now scans `tools/*/package.json` and publishes each sub-tool that has a `name` field and is not `private`. If a sub-tool is already published at its current version, it's silently skipped. If a sub-tool fails to publish, the error is surfaced (Phase 7) but does not block the root release.

This means a guard fix that bumps `tools/wip-branch-guard/package.json` will auto-publish `@wipcomputer/wip-branch-guard` during the same release. No manual `npm publish` step.

## What this fixes

- Incident 3 (Apr 5): npm publish succeeded but git push failed, creating permanent state divergence
- Incident 5 (Apr 5): sub-tool packages required manual npm publish
- Incident 7 (Apr 5): sub-tool publish errors were swallowed as "non-fatal"
