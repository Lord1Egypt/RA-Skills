---
title: "wip-release should bump bundled sub-tool versions when content changes in a parent toolbox release"
status: open
priority: P2
owner: unassigned
reviewer: Installer CC Partner
repo: wip-ldm-os-private (bug doc only); fix lives in wip-ai-devops-toolbox-private / wip-release
created: 2026-05-14
---

## What it does

When `wip-release` cuts a new version of `wip-ai-devops-toolbox` (the bundled parent), it bumps the `package.json` version of any sub-tool whose content has changed since the last toolbox cut. Sub-tool consumers (LDM OS installer, others) can rely on the version pin to decide whether a redeploy is needed instead of falling back to content-hash comparison.

## What it fixes

2026-05-14 alpha.30 dogfood: previous `ldm install` redeployed all 12 sub-tools under `wip-ai-devops-toolbox` but six of them (`wip-branch-guard`, `wip-file-guard`, `wip-license-hook`, `wip-release`, `wip-repo-permissions-hook`, `wip-repos`) had new content WITHOUT new `package.json` version strings. The LDM OS installer caught the divergence via content-hash and redeployed correctly. But every future install will keep content-hash-redeploying these tools until upstream bumps their version pins. The catch is defensive; the upstream omission is the actual bug.

## How to dogfood

1. After a toolbox cut, run `ldm install --alpha --dry-run`.
2. The dry-run should NOT report any sub-tools as "content changed but version pinned" (a hidden category that content-hash catches today).
3. Inspect each sub-tool's `package.json`. The version field should match its on-disk content.

## Problem

`wip-release`'s toolbox-cut path doesn't walk the sub-tools directory and bump per-sub-tool versions based on a content diff. Currently it bumps the parent toolbox version and assumes sub-tools either bumped themselves or are unchanged. When neither is true, downstream consumers cannot trust the version pin.

## Fix

When `wip-release` cuts a new version of the toolbox:

1. Walk each sub-tool's directory.
2. Diff content against the last toolbox-cut snapshot.
3. For each sub-tool with content changes but no version bump, bump its `package.json` version (patch unless a major signal exists).
4. Commit the version bumps as part of the toolbox-cut PR.
5. Surface the per-sub-tool bumps in the release notes.

## Acceptance

- After a toolbox cut, no sub-tool ships content-without-version-bump.
- LDM OS installer's content-hash redeploy logic stops firing as a fallback for routine releases (it stays in place as the safety net for any future regression).
- Regression test in the wip-release repo simulates a toolbox cut with sub-tool content changes; asserts the per-sub-tool version bumps land.

## Out of scope

- Implementing the diff/bump logic in `wip-release`. This ticket scopes the requirement; the `wip-release` repo owns the implementation.
- LDM OS installer's content-hash logic. That correctly defends against this class of bug; it should stay as the safety net even after `wip-release` adds the version-bump pass.

## Cross-repo note

The bug doc lives here per the "bug docs only live in `wip-ldm-os-private/ai/product/bugs/`" rule. The actual fix lands in `wip-ai-devops-toolbox-private` and the `wip-release` tool. The fixing agent should propose the change there once the requirement is agreed.

## Related

- `2026-05-14--cc-mini--installer-bundled-parent-pin-not-updated-after-subtool-redeploy.md` (sibling; parent's own pin doesn't bump either, separate symptom of the same publish-hygiene gap).
- Surfaced by 2026-05-14 alpha.30 dogfood.
