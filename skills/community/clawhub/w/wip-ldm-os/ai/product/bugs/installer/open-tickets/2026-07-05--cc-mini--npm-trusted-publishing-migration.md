---
title: "Migrate npm publishing to Trusted Publishing (OIDC); retire hand-minted bypass-2FA tokens"
status: open
priority: P2
owner: unassigned
reviewer: Installer CC Partner
repo: wip-ldm-os-private (cross-repo: fix spans wip-ai-devops-toolbox-private wip-release + per-repo CI)
created: 2026-07-05
---

## What happened

The 2026-07-05 alpha release train (CC speedup batch) was blocked for hours by npm token rot: the previous granular write token had expired (npm caps write tokens at 90 days), the replacement was created without Bypass 2FA (403 on publish), and the service account initially could not see the vault item. npm's own UI warns that Bypass 2FA tokens are a security risk and recommends Trusted Publishing for automation.

Current interim state: a 90-day bypass-2FA granular token scoped to @wipcomputer, stored as 1Password item `npm-token` (Agent Secrets vault), consumed by wip-release 1.9.80's resolution chain (ambient npm auth, then configurable op item). This works but expires 2026-10 and carries the bypass-2FA risk npm warns about.

## Fix

Adopt npm Trusted Publishing (OIDC between npmjs.com and GitHub Actions):

1. Per published package (@wipcomputer/wip-ldm-os, @wipcomputer/memory-crystal, @wipcomputer/wip-ai-devops-toolbox and its sub-tools, others as published): configure a trusted publisher on npmjs.com pointing at a release workflow in the source repo.
2. Split wip-release: local half keeps version bump, CHANGELOG, SKILL.md sync, commit, tag (everything that needs the working tree); the `npm publish` step moves to a GitHub Actions workflow triggered by the tag push, authenticated via OIDC, no token anywhere.
3. wip-release gains a `--publish-via-ci` mode (or detects the workflow's existence) and reports the Actions run URL instead of publishing directly. Local direct publish stays available as a fallback while any token exists.
4. Retire the npm-token item when all packages are migrated; document the rotation-free flow in library/documentation/how-releases-work.md.

## Tension to resolve in design review

Local-first principle vs CI dependency: publishing would depend on GitHub Actions availability. Mitigation: npm publish already depends on npmjs.com being reachable, and the local tag/commit half stays fully local; only the push-to-registry step rides CI. Parker adjudicates.

## Acceptance

- A release of one pilot package (suggest memory-crystal) publishes to npm via tag-push workflow with zero tokens on the machine or in 1Password.
- wip-release local half completes without npm credentials and prints the CI run URL.
- how-releases-work.md updated; 90-day rotation instructions deleted.

## Related

- wip-ai-devops-toolbox-private PR #423 (wip-release 1.9.80 configurable token resolution: the interim fix)
- `2026-05-14--cc-mini--wip-release-bundled-subtool-version-bump.md` (same wip-release surface)
