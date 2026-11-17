# Data changes

Use when a change can alter persistent records, schema compatibility, retention or access to personal data.

## Establish the real target

Identify the database/environment, owning service, affected records and active readers/writers. A disposable test database needs less process than live shared data. Before an irreversible operation, confirm the exact scope and existing authorization, and verify a usable recovery path. Code rollback does not restore deleted or overwritten data.

## Keep consumers working

For a live column rename with old and new application versions running together:

1. Add the new field without removing the old one.
2. Keep writes consistent during transition; backfill existing records in bounded, resumable batches.
3. Move readers after validating values and completeness.
4. Remove the old field only after dependent consumers and the rollback window no longer need it.

A direct rename can be appropriate in an isolated database with no old consumers. Choose based on deployment and recovery constraints, not a universal migration rule.

Review generated SQL for drops disguised as renames, table rewrites and locks. Check the database version's lock and transaction behavior. In PostgreSQL, a concurrent index build cannot run inside a transaction block and can leave an invalid index after failure; a constraint's `NOT VALID` support depends on its type. Before adopting an online-migration recipe, check those limits for the target database version. Before running a migration that rewrites or locks production tables, get the user's confirmation unless the request already covers it.

## Preserve integrity and recovery

- Represent amounts with explicit currency/unit and rounding rules; use decimal or appropriately scaled integers rather than binary floating point for exact monetary arithmetic. Keep calendar dates distinct from instants and local schedules; test timezone/DST transitions where they affect the contract.
- Use transactions for changes that must succeed together, and constraints or atomic conditional updates for concurrent writers. A check followed by a write can race.
- Make retries/backfills idempotent using a stable key or bounded partition. Track progress and test interruption followed by restart.
- Test important migrations against the actual engine with representative data. Compare values and invariants, not only row counts. Bound lock waits and workload where other clients share the database.
- For destructive work, verify the recovery artifact and restore procedure before applying it. For material data, establish acceptable data loss and restore time, then check that recovery meets them. Replication can copy corruption or deletion; it is not an independent backup.

## Minimize exposure

Use only the fields needed for the task. Keep production data out of fixtures and model prompts unless that transfer is authorized and required. Check access, processing location and retention before adding a new processor.

For deletion, trace live copies: cache, search index, exports and derived tables. Define how backups expire and how a restore avoids resurrecting deleted records. Test disappearance from the application's query paths. Follow the organization's legal/incident process for a suspected exposure; do not invent retention periods or reporting decisions.

## Sources

- [PostgreSQL ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html)
- [PostgreSQL CREATE INDEX](https://www.postgresql.org/docs/current/sql-createindex.html)
- [Google SRE: data integrity](https://sre.google/sre-book/data-integrity/)
