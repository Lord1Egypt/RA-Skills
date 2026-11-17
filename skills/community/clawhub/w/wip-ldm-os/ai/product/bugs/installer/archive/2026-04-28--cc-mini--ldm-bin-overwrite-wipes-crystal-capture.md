---
title: P0 ~/.ldm/bin/crystal-capture.sh missing while cron pointed at it (mechanism unidentified)
date: 2026-04-28
severity: P0
status: open
component: ldm-installer
also-affects: memory-crystal
reported-by: parker (forwarded from agent investigation)
---

# Post-merge mechanism correction (added 2026-04-28 11:55 PDT)

The original write-up below claimed `ldm install` (~09:00 PDT) refreshed `~/.ldm/bin` and removed `crystal-capture.sh`. **That is not supported by the code.**

`bin/ldm.js` `deployScripts()` (line 635) is **additive only**: it iterates `wip-ldm-os-private/scripts/*.sh` and copies each into `~/.ldm/bin` via `cpSync`. It never enumerates or deletes foreign files. So `ldm install` cannot have removed `crystal-capture.sh` as currently implemented.

What we know:
- `~/.ldm/bin` mtime at Apr 28 09:00 PDT and an `ldm install` ran at the same time. **Temporally correlated, not proven causal.**
- The actual delete/missing vector is unidentified.

Likeliest candidates (still to investigate):
1. A prior `crystal init` hit the silent try/catch at `memory-crystal-private/src/installer.ts:797` and reported success without writing the script.
2. A prior manual `rm`, restore from a backup that predated capture-script deployment, or some other tool that touched `~/.ldm/bin` outside `ldm install`.

**Why the action items still hold.** The real bug is the failure class, not the specific delete vector:
- Shared `~/.ldm/bin` ownership has no manifest and no self-heal.
- Memory Crystal doctor reports "cron not found" instead of "cron target missing."
- Memory Crystal install can complete "successfully" while the cron target it depends on is silently absent.

Those harden against this failure class regardless of cause. The fixes below are still correct; the hypothesis about `ldm install` is rescinded.

**Two specific items added on top of the original list:**

- [ ] Memory Crystal install must FAIL or loudly warn if `deployCaptureScript()` does not leave `~/.ldm/bin/crystal-capture.sh` executable post-install. Replace the swallow-all `try/catch` in `installer.ts:794-799` with a verify step.
- [ ] Memory Crystal doctor: if crontab references `crystal-capture.sh` and the file is missing, report **"cron target missing"** (not "cron not found") and offer or perform restore from `~/.ldm/extensions/memory-crystal/dist/crystal-capture.sh`.

Do not chase a phantom delete in `ldm install`. The bug is still serious, but the root cause is "missing ownership / self-heal / diagnostic invariant," not "installer wiped the file."

---

# P0: LDM installer wipes `~/.ldm/bin` foreign files (ORIGINAL HYPOTHESIS, partly retracted)

The section below is preserved as the original write-up. Read the correction above first; the "ldm install wiped the file" mechanism does not match the code.

## What happened

`ldm install` (run on 2026-04-28 ~09:00 PDT) refreshed `~/.ldm/bin` and removed `~/.ldm/bin/crystal-capture.sh`. The Memory Crystal cron job kept firing against that path and silently failed. The capture pipeline appeared dead until logs were inspected.

This is a cross-installer ownership bug, not a Memory Crystal bug, not user error.

## Evidence

```
~/.ldm/bin                                                  mtime Apr 28 09:00 PDT
~/.ldm/logs/install.log
  2026-04-28T16:00:46Z  ldm install started
  2026-04-28T16:01:32Z  ldm install complete

After the install, ~/.ldm/bin contained the new LDM scripts:
  ldm-summary.sh
  ldm-restore.sh
  ldm-backup.sh
  backfill-summaries.sh
  imsg

But did NOT contain:
  crystal-capture.sh

The canonical script still existed in the extension deploy:
  ~/.ldm/extensions/memory-crystal/dist/crystal-capture.sh

Cron continued to point at:
  ~/.ldm/bin/crystal-capture.sh    (now missing)
```

Manual restore of `crystal-capture.sh` from the extension dist + one capture pass succeeded (26 chunks, 132 files, 0 errors). That confirmed the database and plugin were healthy; only the bin shim was missing.

## Why this is P0

1. **Memory looks unreliable when it's actually fine.** Crystal capture failing silently is exactly the failure mode that makes users distrust their AI's memory.
2. **Cross-installer ownership is undefined.** LDM OS owns `~/.ldm/bin` *and* deploys foreign shims into it on behalf of extensions. There is no manifest of who-put-what.
3. **Doctor was uninformative.** `crystal doctor` said "cron not found" instead of "cron target missing." That is a different diagnostic class and led to wasted time.
4. **It will reoccur.** Any future LDM install/update is the same risk for any extension that drops a shim into `~/.ldm/bin`.

## Root cause (suspected)

`ldm install` treats `~/.ldm/bin` as if it owns the entire directory and refreshes it from a known set of scripts. Foreign files placed by extension installers (Memory Crystal, others) are not preserved because the LDM installer has no record they exist.

## Required fixes

1. **Installer ownership model.** LDM installer must use a manifest-owned delete strategy instead of directory replacement. Files not in the manifest are foreign and must not be touched on update.
2. **Memory Crystal install/update** must ensure `~/.ldm/bin/crystal-capture.sh` exists whenever cron references it. If the bin shim is the cron target, the extension must own and verify it on every install.
3. **Doctor / healthcheck must distinguish "cron target missing" from "cron not found."** The error class matters.
4. **Regression test.** Run `ldm install` with Memory Crystal installed. Assert `~/.ldm/bin/crystal-capture.sh` remains executable and that the cron target resolves to a real file. Test must run before any LDM installer release.
5. **Recovery path.** On `ldm install` (or `ldm doctor`), if a cron target is missing but the corresponding extension dist script exists, restore it automatically and log the recovery.

## Suggested ownership

- Fix #1, #4, #5: LDM installer team (this repo, `bin/ldm.js` + `lib/`).
- Fix #2: Memory Crystal team (`~/wipcomputerinc/repos/ldm-os/components/memory-crystal-private/`).
- Fix #3: split. LDM doctor diagnostic + Memory Crystal doctor diagnostic.

## Related

- The separate "OpenClaw `agent:main:main` capture stale after compaction/reset" issue is mentioned in the same investigation but is a distinct bug (capture liveness, not bin shim deletion). File separately under `bugs/openclaw/` if not already tracked.

## Action items

- [x] LDM installer: switch `~/.ldm/bin` to a manifest-owned ownership model. Covered by this PR. Aggregator reads `wipLdmOs.binFiles` from the LDM CLI and `binFiles` from each registered extension's `openclaw.plugin.json`. Conflicts (two declarers claiming the same file) abort install pre-write. Note: the original "delete strategy" phrasing did not match the code (deployScripts is additive, never deletes). What was missing was ownership identity for heal/diagnose, which the manifest now provides.
- [x] Memory Crystal: add `~/.ldm/bin/crystal-capture.sh` integrity check on install + doctor. Covered by memory-crystal-private PR #123 (`verifyCaptureShim()` post-install + `checkCaptureShim()` in `crystal doctor`).
- [x] LDM doctor: explicit "cron target missing" diagnostic. Covered by this PR. `cmdDoctor()` now walks the crontab, classifies any `~/.ldm/bin/<file>` reference as ok / cron target missing / cron target not executable, and offers `--fix` restore from `~/.ldm/extensions/<plugin>/dist/<file>` for known shims.
- [x] Memory Crystal doctor: explicit "cron target missing" diagnostic. Covered by memory-crystal-private PR #123 (`checkCaptureShim()` reports cron missing / target missing / target not executable / ok).
- [x] CI: regression test `ldm install` preserves Memory Crystal cron shim. Covered by `scripts/test-ldm-install-preserves-foreign-bin.mjs`, which runs the real `bin/ldm.js install` against a temp `HOME`, pre-seeds a Memory Crystal-owned `~/.ldm/bin/crystal-capture.sh`, shims external network/crontab commands, and asserts the foreign shim survives unchanged while LDM-owned scripts still deploy.
- [x] LDM installer: auto-recover missing cron targets when extension dist script exists. Covered by this PR. After `deployScripts()`, `cmdInstallCatalog()` walks the aggregated manifest and restores any missing or non-executable file from its declared `source`. Same heal helper backs `ldm doctor --fix`. Aborts pre-write on conflict (no partial state).
