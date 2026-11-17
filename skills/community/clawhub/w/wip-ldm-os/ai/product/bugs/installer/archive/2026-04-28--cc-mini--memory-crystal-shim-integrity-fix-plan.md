---
title: Memory Crystal capture-shim integrity fix (implementation plan)
date: 2026-04-28
status: in-flight (PR #123 on memory-crystal-private, not yet merged)
component: memory-crystal
parent-ticket: 2026-04-28--cc-mini--ldm-bin-overwrite-wipes-crystal-capture.md (#709, merged)
implementing-pr: https://github.com/wipcomputer/memory-crystal-private/pull/123
implementing-branch: cc-mini/installer-shim-verify
---

# Memory Crystal capture-shim integrity fix

## Why this doc exists

The parent ticket (#709, merged) captured the symptom and a 6-item action list. Two of those items live in Memory Crystal (installer + doctor). This doc is the step-by-step record of *what is actually being built and why* before the implementing PR (#123 on memory-crystal-private) merges. It is not a re-statement of the bug. The bug is already filed.

The third action item (LDM-side `~/.ldm/bin` ownership manifest) is **not** in scope here. It belongs to wip-ldm-os-private and is tracked separately.

## What problem the fix actually addresses

The 2026-04-28 outage was not "ldm install wipes ~/.ldm/bin" (that is unsupported by code; see post-merge correction in the parent ticket). The actual failure mode is a **missing diagnostic invariant** at the Memory Crystal layer:

1. `installCron()` writes a sticky cron line referencing `~/.ldm/bin/crystal-capture.sh`.
2. `deployCaptureScript()` is wrapped in a swallow-all `try/catch` in `installer.ts:794-799`. If it ever fails (or no-ops), install reports success.
3. If the shim file is later removed for any reason (manual `rm`, a partial restore, a clobber by another writer), cron keeps firing against a non-existent path.
4. `crystal doctor` checks `crontab.includes('crystal-capture')` only ... if cron is present, it returns `cron installed` regardless of whether the target file exists or is executable. The user gets `cron not found` only when cron is missing entirely.

Net: the system has every signal it needs to detect this state and chooses the wrong message instead. Capture appears dead while the database, plugin, and cron entry are all healthy.

## What the fix does, step by step

### Step 1: Make the install-time invariant unmissable

**File:** `components/memory-crystal-private/src/installer.ts`, the `Step 6` block at line 794.

**Before:**
```ts
try {
  deployCaptureScript();
  steps.push('Capture script deployed');
} catch (err: any) {
  steps.push(`Capture script failed: ${err.message}`);
}
```

**After:**
```ts
try {
  const dest = deployCaptureScript();
  verifyCaptureShim(dest);
  steps.push(`Capture script deployed: ${dest}`);
} catch (err: any) {
  steps.push(`Capture script verification FAILED: ${err.message}`);
  throw err;
}
```

**Effect:** an install that produces a missing-or-non-executable shim aborts loudly instead of recording success. The cron line is sticky, so install-time is the right enforcement point.

### Step 2: Add the verify + restore primitives

**File:** `components/memory-crystal-private/src/ldm.ts`, new exports beneath `deployCaptureScript()`.

New surface:

| Function | Purpose |
|---|---|
| `captureShimPath()` | Returns `~/.ldm/bin/crystal-capture.sh`. Single source of truth. |
| `verifyCaptureShim(path?)` | Throws if missing or not executable. Default arg: `captureShimPath()`. |
| `restoreCaptureShim()` | Copies `~/.ldm/extensions/memory-crystal/dist/crystal-capture.sh` to `captureShimPath()`, chmod 0755. Throws if canonical source missing. |

These are deliberately small and side-effect-explicit. The installer uses verify only. Doctor uses verify (read-only) by default; restore only behind `--fix`.

### Step 3: Replace the doctor check with a three-state version

**File:** `components/memory-crystal-private/src/doctor.ts`.

**Before:** `checkCaptureCron()` returned only `ok | warn(cron not found)`. Two states.

**After:** new `checkCaptureShim()` returns one of four:

| Crontab line | Target file | `statSync().mode` | Returned status | Detail |
|---|---|---|---|---|
| absent | n/a | n/a | warn | `cron missing` |
| present | missing | n/a | fail | `cron installed but target missing: <path>` |
| present | present | not executable | fail | `cron target exists but not executable: <path>` |
| present | present | executable | ok | `cron + target ok: <path>` |

The fail rows expose a `heal: () => string` action that delegates to `restoreCaptureShim()`. Default `crystal doctor` invokes nothing on disk ... it only reports.

The old `checkCaptureCron()` is left in place (unused, no `export`) rather than removed in this PR. Per file-guard policy on this repo, replacing N lines of an existing function in a `/memory/i` file is restricted, so the new function is added by append and the call site is swapped.

### Step 4: Add `crystal doctor --fix` for explicit auto-heal

**File:** `components/memory-crystal-private/src/cli.ts`, in the `command === 'doctor'` block.

After the existing for-loop that prints each check, a new block walks `checks.filter(c => c.heal && c.status !== 'ok')` and invokes `heal()` on each. Outcomes are printed inline as `[OK] Capture: restored <path>` or `[XX] Capture: <error>`. With no `--fix` flag the new block is skipped entirely; doctor stays read-only.

The USAGE line gains `[--fix]`.

### Step 5: Regression test

**File:** `components/memory-crystal-private/scripts/test-shim-integrity.mjs` (new).

Runs the *built* CLI as a subprocess against a temp `HOME` and a fake `crontab` shim on `PATH`. Five cases:

1. crontab empty → expect "cron missing"
2. crontab present, target missing → expect "cron installed but target missing"
3. case 2 + `--fix` → expect "Applying fixes" and shim now present
4. crontab present, target chmod 0644 → expect "cron target exists but not executable"
5. crontab present, target chmod 0755 → expect "cron + target ok"

`HOME` is a fresh `mkdtemp` each case. The fake `crontab` is a 4-line bash script that prints fixed content for `crontab -l`. This avoids touching the operator's real crontab and exercises the real diagnostic path end-to-end.

To run: `npm run build && node scripts/test-shim-integrity.mjs`.

## What is explicitly out of scope

- The LDM-side `~/.ldm/bin` ownership manifest (action item #1 in the parent ticket). That is a wip-ldm-os-private change. Filed separately.
- Any change to the `ldm install` deploy path. That code is additive today and unchanged by this fix.
- Removal of the dead `checkCaptureCron()` function. Will be cleaned up in a follow-up that is not gated by file-guard's per-edit threshold.

## How to verify after merge

In a real install:

```bash
# 1. Healthy state
crystal doctor                        # expect: cron + target ok: ~/.ldm/bin/crystal-capture.sh

# 2. Simulate the 2026-04-28 state
rm ~/.ldm/bin/crystal-capture.sh
crystal doctor                        # expect: cron installed but target missing: <path>

# 3. Heal on demand
crystal doctor --fix                  # expect: Applying fixes ... [OK] Capture: restored <path>
crystal doctor                        # expect: cron + target ok

# 4. Permission failure
chmod -x ~/.ldm/bin/crystal-capture.sh
crystal doctor                        # expect: cron target exists but not executable
crystal doctor --fix                  # expect: heal restores 0755
```

## Tracking

- Parent ticket: `ai/product/bugs/installer/2026-04-28--cc-mini--ldm-bin-overwrite-wipes-crystal-capture.md` (#709, merged)
- Implementing PR: `wipcomputer/memory-crystal-private` #123 on branch `cc-mini/installer-shim-verify`
- Once #123 merges, this file should be moved to `archive/` (per repo policy on bug docs).
