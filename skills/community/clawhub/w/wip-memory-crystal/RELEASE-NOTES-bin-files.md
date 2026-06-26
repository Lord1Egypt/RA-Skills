# Memory Crystal declares `binFiles` for the LDM bin manifest

## Narrative

On 2026-04-28 a capture outage exposed the failure mode at the heart of this release: cron lines in `~/.ldm/bin/` are sticky, but the files they reference can disappear, and nothing in either Memory Crystal's or the LDM CLI's diagnostic surface said who owned what. PR #123 closed the install-time invariant and `crystal doctor --fix` recovery on the Memory Crystal side. The parent ticket on `wip-ldm-os-private` (`ai/product/bugs/installer/2026-04-28--cc-mini--ldm-bin-overwrite-wipes-crystal-capture.md`) then called for a shared ownership model so the LDM CLI could heal extension shims without hardcoded knowledge.

This release contributes Memory Crystal's half of that contract: an explicit `binFiles` declaration in `openclaw.plugin.json` naming `crystal-capture.sh`, plus a prepublish validator that prevents a broken declaration from ever reaching npm. After this lands and the operator runs `ldm install` (with LDM CLI v0.4.83+), `ldm doctor` resolves Memory Crystal as the explicit owner of `crystal-capture.sh`, and the LDM CLI can self-heal a missing or non-executable shim from Memory Crystal's extension dist without any LDM-side hardcoded mapping. Closes #124.

## What changed

- `openclaw.plugin.json` now declares `binFiles` with one entry: `crystal-capture.sh` from `dist/crystal-capture.sh`. This lets the LDM CLI's bin-ownership manifest aggregate Crystal's shim and self-heal it during `ldm install` or `ldm doctor --fix`. Previously the LDM CLI fell back to a hard-coded match for this file; now ownership is explicit and symmetric with every other declarer.
- `scripts/validate-bin-manifest.mjs` (new) runs from `prepublishOnly` after `npm run build`. Asserts each declared `source` exists in the published artifact, no internal duplicates, `name` is a basename. A broken declaration cannot reach npm. Layer 1 of the release-blocker design.
- `package.json` `prepublishOnly` chains `validate:bin-manifest` after the existing build step.

## Why

Closes the Memory Crystal half of the LDM bin-ownership manifest follow-up tracked in `wipcomputer/wip-ldm-os-private:ai/product/bugs/installer/2026-04-28--cc-mini--ldm-bin-overwrite-wipes-crystal-capture.md`. With this declaration:

- `ldm doctor` resolves `crystal-capture.sh` as `declarer = memory-crystal` instead of `owner unknown`.
- `ldm install` can self-heal a missing or non-executable `~/.ldm/bin/crystal-capture.sh` from `~/.ldm/extensions/memory-crystal/dist/crystal-capture.sh` without any LDM-side hardcode.
- A future broken declaration (missing source, internal duplicate, non-basename name) is caught at publish time, not at install time on the operator's machine.

## What this does NOT do

- **`ldm-backup.sh` collision cleanup.** Memory Crystal still ships and deploys its own copy of `ldm-backup.sh`. Per the agreed ownership in the design pass (LDM CLI keeps it, MC drops its copy), that cleanup lands as a separate small PR. This PR is intentionally scoped to the binFiles declaration so review is small. If MC declared `ldm-backup.sh` here it would conflict at the manifest level with the LDM CLI's declaration; we are avoiding that until the cleanup PR runs.
- **Layer 2 cross-package CI gate.** That is a workflow on `wip-ldm-os-private` and is independent of MC.
