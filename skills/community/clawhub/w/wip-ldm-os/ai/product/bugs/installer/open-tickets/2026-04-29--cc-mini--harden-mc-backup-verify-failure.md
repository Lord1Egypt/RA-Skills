---
title: Memory Crystal installer should fail loudly on backup-shim verify failure
date: 2026-04-29
status: open (parked follow-up from 2026-04-28 thread)
severity: P3
component: memory-crystal
parent-ticket: archive/2026-04-28--cc-mini--ldm-bin-overwrite-wipes-crystal-capture.md
related-prs: wipcomputer/memory-crystal-private#127 (current swallow behavior)
---

# Harden Memory Crystal backup-shim verify

## Context

PR #127 on `memory-crystal-private` replaced the duplicate `deployBackupScript()` call in `src/installer.ts` Step 6 with a verify of `~/.ldm/bin/ldm-backup.sh` (LDM CLI-owned). The verify is wrapped in a `try { ... } catch (err) { steps.push("Backup shim verify failed: ..."); }` block. On failure the install continues; only a step entry records the problem.

Parker's review note on #127:

> One small follow-up I'd file but not block on: src/installer.ts catches the missing backup shim and only records "Backup shim verify failed..." without throwing. That matches prior behavior, but if backup setup is considered critical later, this should become a stronger health failure. For now, not blocking because the backup shim is ancillary and ldm doctor/manifest owns the repair path.

## What needs to happen

When backup ownership becomes operationally critical (or when the parallel capture-shim verify in the same file is treated as a model), promote the backup-shim verify from "log and continue" to "throw and abort" at minimum. Preferably it should fail the install the same way `verifyCaptureShim()` already does at line 794-799.

Concretely, in `memory-crystal-private:src/installer.ts` Step 6, the catch block currently looks like:

```ts
} catch (err: any) {
  steps.push(`Backup shim verify failed: ${err.message}`);
}
```

Change to:

```ts
} catch (err: any) {
  steps.push(`Backup shim verify FAILED: ${err.message}`);
  throw err;
}
```

Mirroring the capture-shim block.

## Why parked, not done

`ldm doctor` and the LDM manifest already own the repair path for `~/.ldm/bin/ldm-backup.sh`: if the file goes missing, `ldm install` self-heals it, and `ldm doctor --fix` restores it on demand. So the MC install's verify is a "tell the operator early" signal, not the load-bearing recovery path. Today's behavior of logging and continuing is acceptable; it just isn't as loud as it could be.

## Acceptance criteria

- [ ] `memory-crystal-private:src/installer.ts` Step 6 throws on verify failure (no swallow).
- [ ] Test asserts `crystal init` fails loudly when `~/.ldm/bin/ldm-backup.sh` is absent.
- [ ] No regression in the capture-shim verify, which already throws.

## Why P3

Hygiene-tier. Real failure mode (capture shim missing while cron points there) is fully closed by the merged work. Backup is a daily LaunchAgent at 03:00, ancillary to capture. Promote the verify when convenient.
