# Destructive Operation Backup & Warning Notes (Rule 22 / A5)

> Companion to `SKILL.md` rule 22 and extended rule A5. Destructive operations mean: DELETE / DROP / overwrite / bulk modify / reset / large-scale status change etc. that may cause **irreversible** consequences.

## 1. Prerequisite: Explicit Authorization Required

- Destructive operations are **disabled by default**. Only allowed when `scope.destructive.allowed=true` in `AUTHORIZATION.json` AND the current target matches `scope.destructive.items` (listed item-by-item).
- A vague "you may test" does not equal permission to destroy; anything not itemized is treated as unauthorized.

## 2. Before Execution: Backup First + Advance Warning

1. **Identify resources to be touched**: data rows, files, configs, records, object-storage keys, etc.
2. **Make a recoverable backup** and record:
   - Backup method (DB export / file copy / snapshot / versioned copy)
   - Backup location (path / bucket / snapshot ID)
   - Backup time (to the second)
   - Recovery command / steps
3. **Verify backup is recoverable** (at least confirm the backup file is complete and readable; do a recovery drill in critical scenarios).
4. **Advance warning**: in the pre-test checklist and report, label "this session includes destructive ops, impact scope, irreversible risk", and confirm the authorizer is aware.
5. When `scope.destructive.backup_required=true` (default), **must not execute without backup**.

## 3. During Execution

- Proceed step by step; do not fire destructive requests in bulk within loops / retries.
- Write every destructive action immediately into the "operation log" (incl. backup-location reference, affected row / object count).
- On accidental out-of-scope touch or exceeding expectations, immediately stop per B3 and notify the authorizer.

## 4. After Execution: Restore & Verify

- After destructive ops complete, restore to original state from backup (rules 5 / 22).
- Use a "bare request" to verify restoration (rule 7).
- Write restoration result into the report; if unrestorable, mark per rule 6 and explicitly inform the authorizer.

## 5. Backup Record Template (write into report)

```
### Destructive Operation Backup Record
- Operation: <DELETE /api/orders/12345>
- Affected resource: <orders table order_id=12345>
- Backup method: <DB export>
- Backup location: </backups/2026-08-15/orders_12345.sql>
- Backup time: YYYY-MM-DD HH:MM:SS
- Recovery steps: < source /backups/.../orders_12345.sql >
- Recovery verification: <restored, bare request confirms data exists>
```
