---
name: sql-migration-linter
description: Lint .sql migration files for common mistakes — missing IF EXISTS guards, UPDATE/DELETE without WHERE, non-idempotent CREATE, missing transaction wrappers, reserved-word identifiers, destructive DDL, and Postgres-specific issues (CREATE INDEX locks, ADD COLUMN NOT NULL without DEFAULT). 17 rules across structure, safety, and style categories. Pure Python stdlib.
---

# SQL Migration Linter

Rule-based linter for SQL migration files. Catches mistakes that make migrations non-idempotent, destructive, or unsafe under concurrent load. Pure Python stdlib — no dependencies.

Supports dialects: `generic`, `postgres`, `mysql`, `sqlite`.

## Commands

```bash
# Lint a single file
python3 scripts/sql_migration_linter.py lint migrations/001_init.sql

# Lint a directory recursively
python3 scripts/sql_migration_linter.py lint migrations/

# Specify dialect (unlocks Postgres-specific rules)
python3 scripts/sql_migration_linter.py lint migrations/ --dialect postgres

# Filter by minimum severity
python3 scripts/sql_migration_linter.py lint migrations/ --min-severity warning

# JSON output for CI
python3 scripts/sql_migration_linter.py lint migrations/ --format json

# Compact summary
python3 scripts/sql_migration_linter.py lint migrations/ --format summary

# List all rules
python3 scripts/sql_migration_linter.py rules
```

## Rules (17 total)

### Structure
- `missing-trailing-semicolon` (error) — file does not end with `;`
- `mixed-indentation` (warning) — tabs and spaces mixed in the same line
- `trailing-whitespace` (info)
- `keyword-case-inconsistent` (info) — same keyword appears in mixed case

### DDL safety
- `drop-without-if-exists` (warning) — `DROP TABLE/INDEX/...` without `IF EXISTS`
- `destructive-drop-table` (warning) — `DROP TABLE` flagged for review
- `create-without-if-not-exists` (warning) — `CREATE TABLE/INDEX/...` without `IF NOT EXISTS`
- `create-index-locks-table` (warning, postgres) — `CREATE INDEX` without `CONCURRENTLY`
- `add-column-not-null-no-default` (error, postgres) — `ADD COLUMN ... NOT NULL` without `DEFAULT`
- `reserved-word-identifier` (warning) — identifier matches a SQL reserved word (e.g. `user`, `order`)

### DML safety
- `update-without-where` (error)
- `delete-without-where` (error)
- `truncate-is-destructive` (warning)
- `select-star` (info) — `SELECT *` in migrations
- `insert-without-conflict-handling` (info) — `INSERT` without `ON CONFLICT` / `ON DUPLICATE KEY`

### Transactions
- `missing-transaction` (warning) — 2+ DDL statements without explicit `BEGIN`/`COMMIT`
- `begin-without-commit` (error)

## Output formats

- **text** (default) — grouped by file, `line:severity: [rule] message`, with totals
- **json** — array of `{file, line, rule, severity, message}` objects
- **summary** — counts per severity + top 10 rules by frequency

## Exit codes (CI-friendly)

- `0` — clean (or only `info` below min-severity)
- `1` — warnings present, no errors
- `2` — errors present

## Examples

```bash
# Pre-commit hook — fail on any warning or error
python3 scripts/sql_migration_linter.py lint migrations/ --min-severity warning

# CI gate — fail only on errors
python3 scripts/sql_migration_linter.py lint migrations/ --min-severity error

# Postgres-specific audit
python3 scripts/sql_migration_linter.py lint migrations/ --dialect postgres --format json > report.json
```

## Why this exists

Migrations that look fine locally fail in production because:

- They aren't idempotent (re-run fails)
- They lock large tables (Postgres `CREATE INDEX`, `ADD COLUMN NOT NULL`)
- They mutate every row (`UPDATE` / `DELETE` without `WHERE`)
- They use reserved words as identifiers and break under different parsers

This linter catches those before the PR gets merged.

## Limitations

- Uses regex + statement splitting; not a full SQL parser
- No schema knowledge — cannot check FK targets, column types, etc.
- `keyword-case-inconsistent` is per-statement, not repo-wide
