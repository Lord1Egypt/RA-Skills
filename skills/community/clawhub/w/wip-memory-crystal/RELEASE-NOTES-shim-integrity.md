# Capture-shim integrity invariant + `crystal doctor --fix`

## Summary

Two changes that close the failure mode behind the 2026-04-28 capture outage: cron at `* * * * * ~/.ldm/bin/crystal-capture.sh` continued to fire while the shim file was missing, and `crystal doctor` reported "cron not found" instead of "cron target missing." The capture pipeline appeared dead even though the database, plugin, and cron entry were all healthy.

Tracked at `wip-ldm-os-private/ai/product/bugs/installer/2026-04-28--cc-mini--ldm-bin-overwrite-wipes-crystal-capture.md` (action items 2, 3 ... Memory Crystal installer + doctor).

### 1. Installer verifies its own shim before reporting success

`src/installer.ts` previously wrapped `deployCaptureScript()` in a swallow-all `try/catch` that pushed `Capture script failed: ...` and continued. `installCron()` would then write a sticky cron line referencing a path that may not exist, with no failed install signal to the operator.

The fix: after `deployCaptureScript()` returns its destination path, the installer now calls `verifyCaptureShim(dest)` (new export from `src/ldm.ts`). Verification asserts the file exists and is executable. If either check fails, the install throws ... no silent "looks fine" path.

### 2. `crystal doctor` distinguishes three failure modes

`src/doctor.ts` `checkCaptureCron()` returned `cron not found` for every non-OK state. That covers neither "cron installed but the script the cron points at is missing" nor "the script is there but not executable." Both are real and have different fixes.

The replacement check (`checkCaptureShim()`) returns:

| State                                       | Status | Detail                                            |
|---------------------------------------------|--------|---------------------------------------------------|
| no crontab line                             | warn   | `cron missing`                                    |
| crontab line, target file missing           | fail   | `cron installed but target missing: <path>`      |
| crontab line, target present but not exec   | fail   | `cron target exists but not executable: <path>`  |
| crontab line, target present and executable | ok     | `cron + target ok: <path>`                        |

Default `crystal doctor` is detect-and-report only. No silent writes.

### 3. `crystal doctor --fix` for explicit auto-heal

When a check returns a `heal` action and the user passes `--fix`, doctor invokes the heal. For the capture shim, heal is `restoreCaptureShim()`: copies `~/.ldm/extensions/memory-crystal/dist/crystal-capture.sh` to `~/.ldm/bin/crystal-capture.sh` and chmods 0755. This is the same operation Parker performed manually to recover from the 2026-04-28 outage, behind an explicit flag.

Without `--fix`, doctor never modifies disk. The decision point is preserved.

### 4. Regression test

`scripts/test-shim-integrity.mjs` exercises the four states + heal against the built CLI in a subprocess, using a temp `HOME` and a fake `crontab` shim on `PATH`. Run from the repo root with `node scripts/test-shim-integrity.mjs` after `npm run build`. All five test cases pass before this branch ships.

## Why this matters

The 2026-04-28 outage looked like a memory-reliability problem from the user's seat. It was actually a missing diagnostic invariant: the system had every signal it needed to detect the broken state and chose the wrong message instead. With these changes:

- New installs cannot complete with a broken shim.
- `crystal doctor` names the real failure class.
- `crystal doctor --fix` restores from the canonical extension dist when safe, behind an explicit flag.

The longer-term `~/.ldm/bin` ownership manifest at the LDM OS layer is tracked separately in the parent ticket and is not part of this PR.
