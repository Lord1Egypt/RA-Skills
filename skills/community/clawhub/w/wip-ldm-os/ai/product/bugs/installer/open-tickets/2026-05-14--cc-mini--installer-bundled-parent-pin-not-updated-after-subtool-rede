---
title: "Installer redeploys bundled sub-tools but doesn't bump the parent's registry version pin"
status: open
priority: P2
owner: unassigned
reviewer: Installer CC Partner
repo: wip-ldm-os-private
created: 2026-05-14
---

## What it does

When `ldm install` redeploys a bundled parent (e.g., `wip-ai-devops-toolbox`) and its sub-tools, it bumps the parent's `installed.version` field in the registry to match the redeployed content. Subsequent dry-runs no longer report the parent as "update available" when the on-disk content is already current.

## What it fixes

2026-05-14 alpha.30 dogfood: previous `ldm install` redeployed all 12 sub-tools under `wip-ai-devops-toolbox` (`wip-release`, `wip-license-hook`, etc.) to their 1.9.73-alpha.12 content. The on-disk files matched the new version. But the registry entry for `wip-ai-devops-toolbox` itself still showed `installed.version: "1.9.69"`. Every subsequent `ldm install --alpha --dry-run` then reported the toolbox as needing a 1.9.69 → 1.9.73-alpha.12 update, even though there was nothing actually pending. The user can't tell from dry-run output whether the install is real or a phantom.

## How to dogfood

1. Install a bundled parent package via `ldm install --alpha` (e.g., a toolbox version bump).
2. Run `ldm install --alpha --dry-run` immediately after.
3. The dry-run should report no pending changes for the parent. Today it incorrectly reports the parent as still needing the version bump.

## Problem

The redeploy path in `bin/ldm.js` writes new sub-tool content but doesn't update the parent's `installed.version` in `registry.json`. Two install passes are required: the first deploys content, the second updates the version pin. The second pass is wasted work and confuses the user about whether a real update is pending.

## Fix

When `ldm install` finishes redeploying a parent + sub-tools, update the parent's registry entry's `installed.version` to match the version it just deployed. Atomic with the content deploy: either both succeed or neither does. Surface "Bumped `wip-ai-devops-toolbox` 1.9.69 → 1.9.73-alpha.12" in the install summary.

## Acceptance

- After `ldm install --alpha` on a bundled parent, the registry's `installed.version` for that parent matches the deployed content's `package.json` version.
- Immediate `ldm install --alpha --dry-run` reports no pending changes for the just-installed parent.
- Regression test simulates the toolbox redeploy; asserts the registry pin bumps; asserts dry-run reports no pending update.

## Out of scope

- The bundled sub-tools' own version pins (those are separate registry entries; this ticket is about the parent).
- The 2026-05-13 source-types refactor's `bundled` updateSource type. This bug exists in current install code; the fix applies to whatever bundling implementation is current and survives Phase 2's `bundled` type when it lands.

## Related

- `2026-05-13--cc-mini--installer-source-bundled.md` (Phase 2 source-bundled; once it ships, this fix may move to the new bundled-extension handler).
- Surfaced by 2026-05-14 alpha.30 dogfood.
