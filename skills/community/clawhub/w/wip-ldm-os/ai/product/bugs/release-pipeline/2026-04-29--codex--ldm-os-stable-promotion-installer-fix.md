# Bug: promote LDM OS stable after stale-extension installer fix

Date: 2026-04-29
Filed by: Codex
Area: release-pipeline
Status: Open
Master plan: `2026-04-24--codex--canary-release-pipeline-master-plan.md`

## Summary

The stale-extension installer bug is fixed in the alpha track, but stable machines can still hit the failure mode until the LDM OS stable package is promoted.

Current verified state:

- `@wipcomputer/wip-ldm-os` latest: `0.4.84`
- `@wipcomputer/wip-ldm-os` alpha: `0.4.85-alpha.2`
- `ldm` local validation version: `0.4.85-alpha.2`
- `wip-branch-guard` CLI/runtime validation version: `1.9.90`

The fixed alpha refreshes deployed extensions correctly. Stable/latest still points at the previous installer, so a fresh stable machine can report a current CLI while leaving `~/.ldm/extensions/<tool>/` stale.

## Why This Needs Its Own Ticket

The installer bug itself is closed in source and alpha validation. This ticket tracks the remaining operational gap: stable promotion of the fixed installer so the install-prompt path no longer repeats the mismatch.

This is separate from the toolbox stable promotion ticket because the LDM OS package has its own npm package, release cadence, and install prompt contract.

## Scope

- Promote `@wipcomputer/wip-ldm-os@0.4.85-alpha.2` or a successor containing the stale-extension fix to stable/latest.
- Preserve the stable-install ownership rule: Parker dogfoods stable/latest through the install prompt unless he explicitly delegates install.
- Verify a fresh stable install checks both the CLI package version and the deployed extension runtime version.
- Update the closed installer ticket with the stable promotion reference after release.

## Acceptance Criteria

1. `@wipcomputer/wip-ldm-os` latest resolves to a version containing the stale-extension fix.
2. The release notes explicitly mention deployed extension refresh behavior.
3. Stable install validation prints or records both versions:
   - `ldm --version`
   - the deployed runtime version under `~/.ldm/extensions/<tool>/`
4. A fresh stable install of `@wipcomputer/wip-branch-guard@1.9.90` or newer leaves CLI, package metadata, and deployed runtime aligned.
5. The installer ticket `ai/product/bugs/installer/2026-04-29--codex--ldm-install-leaves-deployed-extension-stale.md` gains a stable-promotion closeout note.
6. No agent runs Parker's stable install prompt unless explicitly delegated.

## Related

- `ai/product/bugs/installer/2026-04-29--codex--ldm-install-leaves-deployed-extension-stale.md`
- `ai/product/bugs/release-pipeline/2026-04-29--codex--toolbox-stable-promotion-readiness.md`
- `ai/product/bugs/release-pipeline/2026-04-24--codex--canary-release-pipeline-master-plan.md`
