# Memory Crystal stops shipping `ldm-backup.sh`

## Narrative

Per the bin ownership decision in PR #717 design pass (Q3): the LDM CLI owns `ldm-backup.sh`; Memory Crystal drops its copy. With both packages now on the manifest model (memory-crystal v0.7.37 declared `crystal-capture.sh`; wip-ldm-os v0.4.83 declared `ldm-backup.sh` and four other LDM-owned files), the runtime resolves any cron target back to its declarer, install-time self-heal restores from canonical sources, and the manifest aggregator refuses to act when two declarers claim the same name. The remaining hygiene step is removing MC's duplicate so there is one source of truth on disk and in published artifacts. Closes the last item from the parent ticket on `wip-ldm-os-private` (`ai/product/bugs/installer/2026-04-28--cc-mini--ldm-bin-overwrite-wipes-crystal-capture.md`); refs #124.

This release does not affect runtime behavior on installs that already received both packages: the LDM CLI's `wipLdmOs.binFiles` is the authoritative source for `ldm-backup.sh`, and `ldm install` keeps it deployed at `~/.ldm/bin/ldm-backup.sh`. The MC-side change just stops competing for the file and removes it from MC's published artifact and `crystal init` flow.

## What changed

- **`openclaw.plugin.json`** unchanged. MC continues to declare only `crystal-capture.sh` in `binFiles`, so the runtime aggregator never saw a manifest-level conflict on `ldm-backup.sh` from this side.
- **`package.json` `files`** drops `scripts/ldm-backup.sh`. The published npm tarball no longer carries MC's copy.
- **`package.json` `scripts.build`** drops the `cp scripts/ldm-backup.sh dist/` step. The build no longer copies a duplicate into `dist/`.
- **`src/installer.ts`** Step 6 (in `runInstallOrUpdate`) replaces the `deployBackupScript()` call with a verify of `~/.ldm/bin/ldm-backup.sh`. If the file is absent, the install fails loudly with `expected ~/.ldm/bin/ldm-backup.sh (LDM CLI-owned); run "ldm install" first`.
- **`src/cli.ts`** `crystal backup setup` replaces `deployBackupScript()` with the same verify and a clear error message pointing at `ldm install`. `crystal backup` (no subcommand) updates its missing-file message from "Run crystal init first" to "Run ldm install first".
- **`deployBackupScript`** import is removed from both `installer.ts` and `cli.ts`. The function and `scripts/ldm-backup.sh` themselves stay in the repo for now (delete-restricted by the per-edit guard on this codebase) but are no longer called and no longer published.

## Why this is safe

The LDM CLI's manifest already covers `ldm-backup.sh`:

- After `wip-release patch` for wip-ldm-os v0.4.83, the LDM CLI declares ownership in `package.json#wipLdmOs.binFiles`.
- After `ldm install`, the manifest heal walk restores `~/.ldm/bin/ldm-backup.sh` from the LDM CLI's `scripts/ldm-backup.sh`.
- `crystal backup setup` is operator-invoked and now verifies-then-installs the LaunchAgent. Failure mode: clear "run ldm install first" message instead of silently double-deploying or relying on whoever ran last.
- `crystal init` similarly verifies-then-throws if the LDM CLI hasn't run.

The only behavior change visible to operators is: `crystal init` and `crystal backup setup` now expect the LDM CLI to have run first. Since `crystal init` already delegates to `ldm install` when the LDM CLI is on PATH (`installer.ts` line 633 `runLdmInstall(repoRoot)`), this is the normal flow for every existing install.

## Tests

- `npm run validate:bin-manifest` ... passes.
- `npm run build` ... passes; `dist/ldm-backup.sh` is no longer produced.
- `node scripts/test-shim-integrity.mjs` ... still 7/7 assertions pass; capture-shim diagnostics unchanged.

## What this does NOT do

- **`deployBackupScript` function** stays defined in `src/ldm.ts`. The function is dead code now (no callers in the package). A future cleanup can remove it; restricted by the per-edit guard on this PR's surface.
- **`scripts/ldm-backup.sh` file** stays in the source tree. Not in the published artifact. Removable in a future cleanup once the per-edit guard is satisfied.
- **No runtime behavior change for already-installed operators** beyond the verify-instead-of-deploy in MC's installer paths. `~/.ldm/bin/ldm-backup.sh` keeps working because the LDM CLI manifest deploys it on every `ldm install`.
