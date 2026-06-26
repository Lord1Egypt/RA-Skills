# db_tool.md
Version: 1.0
Purpose: AI-readable operational skill for database tooling, integrity controls, and exec-driven helper scripts using better-sqlite3 for 
accounting-grade agents.

---

# Skill Intent

This skill defines how an agent should use SQLite tooling safely, quickly, and deterministically.

This is NOT generic database guidance.

This is:

- execution layer discipline
- tool-call reduction layer
- data integrity layer
- accounting persistence layer
- reusable script syscall layer

Primary stack:

```text
SQLite
better-sqlite3
single .db file
exec tool
scripts/ syscall layer
```

Use this skill whenever the agent:

- posts transactions
- queries ledger data
- runs aggregates
- performs reconciliation
- validates integrity
- closes periods
- mutates accounting records
- needs high-trust persistence

---

# Core Principles

Every financial mutation must satisfy:

```text
1 Valid
2 Balanced
3 Atomic
4 Idempotent
5 Audited
6 Reversible
7 Append-only
```

Never violate these.

---

# Database Initialization Standard

Always initialize database with:

```javascript
db.pragma('journal_mode = WAL')
db.pragma('foreign_keys = ON')
db.pragma('synchronous = FULL')
db.pragma('busy_timeout = 5000')
db.pragma('temp_store = MEMORY')
```

Prefer:

```text
synchronous=FULL
```

for accounting safety.

---

# Golden Posting Rule

Never post directly from user intent.

Mandatory flow:

```text
User Intent
-> Parse
-> Draft
-> Validate
-> Preview
-> Confirm
-> Commit
-> Audit Log
```

Never:

```text
User intent
-> insert rows directly
```

Forbidden.

---

# Two-Phase Posting Rule

Use staged posting.

Statuses:

```text
DRAFT
VALIDATED
POSTED
REVERSED
```

Tables:

```sql
draft_entries
posted_entries
```

Workflow:

```text
create draft
validate draft
preview draft
confirm
promote to posted
```

---

# Double Entry Enforcement

Before posting:

must verify:

```text
Total Debit = Total Credit
```

Check:

```sql
SELECT
SUM(debit),
SUM(credit)
FROM draft_lines
WHERE voucher_id=?
```

If unequal:

```text
Abort immediately
```

Hard failure.

---

# Idempotency Rule

All postings require request_id.

Schema:

```sql
request_id TEXT UNIQUE
```

Before posting:

```sql
SELECT id
FROM vouchers
WHERE request_id=?
```

If exists:

```text
Return existing voucher.
Never repost.
```

Mandatory.

---

# Append-Only Ledger Rule

Never do:

```sql
UPDATE ledger ...
DELETE ledger ...
```

Never modify historical ledger rows.

Corrections happen only through:

```text
reverse
adjust
rectify
```

using new entries.

---

# Immutable Audit Trail

Maintain:

```sql
audit_log(
 id,
 event_type,
 entity_id,
 before_json,
 after_json,
 actor,
 timestamp
)
```

Every mutation writes audit event.

Append-only.

---

# Database Constraints Rule

Push integrity into schema.

Use:

```sql
NOT NULL
CHECK(...)
UNIQUE(...)
FOREIGN KEY(...)
```

Examples:

```sql
debit REAL CHECK(debit>=0),
credit REAL CHECK(credit>=0),
voucher_no TEXT UNIQUE
```

Do not rely only on model reasoning.

Database enforces truth.

---

# Savepoint Rule

For multi-step operations use:

```sql
SAVEPOINT post_tx
...
ROLLBACK TO post_tx
```

For partial recovery.

---

# Prepared Statement Registry

Do not dynamically build SQL repeatedly.

Use statement registry.

Example:

```javascript
statements={
 insertVoucher:...,
 insertLine:...,
 trialBalance:...
}
```

Reuse prepared statements.

Faster.
Safer.

---

# Exec Script Syscall Layer

Use scripts/ as database syscall layer.

Preferred structure:

```text
scripts/
 post-voucher.js
 preview-voucher.js
 reverse-voucher.js
 rectify-entry.js
 ledger-query.js
 generate-report.js
 reconcile.js
 integrity-check.js
 close-period.js
 db-maintenance.js
 migrate-schema.js

lib/
 db.js
 validators.js
 posting-engine.js
 interpreter.js
```

Scripts should be deterministic.

One script = one accounting verb.

---

# Script Definitions

==================================================
SCRIPT
post-voucher.js
==================================================

Primary write engine.

Invocation:

```bash
node scripts/post-voucher.js payload.json
```

Must enforce Maker-Checker protocol:
Do not run directly from user intent.
Requires valid voucher type (CR, BR, JE, etc.) and source document reference.

Performs:
- idempotency check
- final balance validation
- period open check
- voucher number generation
- transaction posting
- audit logging
- commit or rollback

Workflow:
```text
BEGIN
validate
insert voucher
insert lines
update derived balances
audit log
COMMIT
```

Rollback on failure. All writes flow through this engine.

---

# preview-voucher.js

Dry-run simulation and Audit Rule Enforcer.

Enforces:
- Completeness check
- Logic check
- Risk check
- Control check

Shows:
- proposed journal
- affected ledgers
- debit/credit totals
- warnings
- posting impact

No writes. Mandatory step before commit.

---

# reverse-voucher.js

Never edits originals.

Creates reversal entry.

Process:

- fetch original
- invert debits/credits
- post reversal
- link reversal voucher

Uses post-voucher engine internally.

---

# rectify-entry.js

Correction workflow:

```text
reverse incorrect entry
post corrected entry
```

Atomic.

Should call post-voucher engine.

---

# ledger-query.js

Universal read script.

Supports:

- account inquiry
- voucher lookup
- search
- pagination
- aggregate reads

Examples:

```bash
exec ledger-query account Cash
exec ledger-query voucher JV-101
```

Use indexed queries.

Read-only.

---

# generate-report.js

Unified reporting engine.
Produces 12 core reports:
- Trial Balance
- P&L
- Balance Sheet
- Cash Flow
- General Ledger
- AR/AP Aging
- Cash / Bank Book
- Registers (Sales/Purchase)
- Bank Reconciliation
- Audit Report

Derived dynamically from ledger.

---

# reconcile.js

Supports:

- bank reconciliation
- invoice payment matching
- unmatched detection
- duplicate detection

Rules-based matching engine.

---

# integrity-check.js

Critical safety script.

Runs:

```sql
PRAGMA integrity_check;
PRAGMA foreign_key_check;
```

Plus custom checks:

- orphan rows
- duplicate voucher numbers
- unbalanced vouchers
- broken references
- trial balance mismatch

Returns health report.

Run routinely.

---

# close-period.js

Period close engine (Monthly, Quarterly, Yearly).

Steps:
- verify books balanced
- run final reconciliations
- generate closing entries (Yearly: temp accounts to retained earnings)
- lock period

Example:
```sql
period_status='CLOSED'
```

Prevent posting into closed periods without controlled override.

---

# db-maintenance.js

Housekeeping.

Commands:

```sql
VACUUM;
ANALYZE;
PRAGMA wal_checkpoint(FULL);
```

Supports:

- backup
- optimize
- checkpoint
- maintenance

---

# migrate-schema.js

Only allowed schema change path.

Track:

```sql
schema_migrations
```

Never alter schema ad hoc.

---

# Shared Library Rules

Every script should reuse:

```text
lib/db.js
lib/validators.js
lib/posting-engine.js
```

Avoid duplicated logic.

---

# Posting Engine Internal Functions

Recommended internal functions:

```text
validateBalanced()
checkIdempotency()
generateVoucherNo()
postLines()
updateDerivedBalances()
writeAuditTrail()
```

Centralize logic.

All write scripts reuse same engine.

---

# Database Prohibitions

Agent should not issue:

```sql
DELETE FROM ledger
DROP TABLE ...
UPDATE balances ...
```

unless privileged maintenance mode.

Forbidden by default.

---

# Integrity Verification Routine

Run periodically:

```text
integrity-check
trial-balance
reconcile exceptions
backup snapshot
```

Routine order:

```text
verify
repair if needed
backup
continue
```

---

# Backup Rule

Before risky operations:

```bash
cp accounting.db accounting-backup.db
```

Prefer snapshot before:

- close
- migrations
- bulk posting
- rectification batches

---

# Materialized Summary Tables (Optional)

Optional performance layer:

```sql
account_balances
daily_totals
trial_balance_cache
```

Maintain during posting.

Improves reporting speed.

---

# Recommended Dispatcher (Optional)

Optional unified command wrapper:

```text
accounting-cli.js
```

Examples:

```bash
exec accounting-cli post ...
exec accounting-cli tb
exec accounting-cli reconcile
```

Single exec entrypoint.

Preferred for agent simplicity.

---

# Minimal Required Script Set

If creating only minimum set:

```text
post-voucher.js
preview-voucher.js
reverse-voucher.js
trial-balance.js
integrity-check.js
```

Mandatory starter pack.

---

# Agent Execution Preference Order

Always prefer:

1 preview first
2 validated post second
3 append-only corrections
4 scripted operations over ad hoc SQL
5 single write engine over many write paths

Always.

---

# Decision Rule

If operation mutates financial truth:

use script layer.

Do not improvise SQL.

If operation affects integrity:

run integrity-check.

If operation changes schema:

use migrate-schema only.

If operation corrects history:

reverse, never overwrite.

---

# Mental Model

Treat SQLite not as storage.

Treat it as:

```text
mini accounting database kernel
```

Scripts are system calls.

Agent reasons at business level.

Scripts enforce truth.

---

# Final Rule

Prefer:

```text
one database
one write path
one posting engine
many safe script verbs
```

This minimizes:

- tool calls
- hallucinated SQL
- duplicate posting
- integrity failures
- reconciliation problems

and maximizes trust.
