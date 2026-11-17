---
name: test-mysql-db
description: Connect to test-environment MySQL databases for troubleshooting, data verification, schema inspection, and controlled validation queries. Use when the user asks to query or validate test/dev database data, investigate test-environment issues, check whether new Java/service code wrote expected records, inspect table structure, compare before/after data, or perform explicitly approved low-risk data correction in a test MySQL database.
---

# Test MySQL DB

Use this skill to query and validate test-environment MySQL data while keeping credentials and write operations controlled.

## Safety Rules

- Treat all database credentials as secrets. Do not write hostnames, usernames, passwords, or DSNs into skill files, repo files, chat, logs, or generated artifacts unless the user explicitly asks for a redacted template.
- Prefer read-only operations. For `INSERT`, `UPDATE`, `DELETE`, DDL, or stored procedure calls, get explicit user confirmation in the current conversation and state the target environment, database, table, predicate, expected row count, and rollback plan first.
- Never run destructive broad statements such as unconstrained `DELETE`, unconstrained `UPDATE`, `DROP`, `TRUNCATE`, or schema changes unless the user explicitly asks and the target is confirmed as a disposable test database.
- Use narrow predicates, `LIMIT`, and transactions where possible. For write validation, capture before/after query results.
- Redact passwords, tokens, personal data, payment data, and secrets in final responses.

## Connection Discovery

Find connection details from the safest available source:

1. Existing project configuration for the test/dev profile, such as Spring `application-dev.yml`, `application-test.yml`, Nacos/Apollo/local config, Docker Compose, `.env`, CI variables, or documented runbooks.
2. Environment variables already present in the shell, preferably:
   - `TEST_MYSQL_HOST`
   - `TEST_MYSQL_PORT`
   - `TEST_MYSQL_USER`
   - `TEST_MYSQL_PASSWORD`
   - `TEST_MYSQL_DATABASE`
3. A user-provided one-time value in chat, redacted after use in summaries.

If multiple test databases are plausible, identify the service/module and ask only for the missing disambiguation.

## Query Workflow

1. Clarify the business key to query: order number, request id, trace id, user id, batch id, table name, or service/module.
2. Inspect relevant code/config first when the table or database is unclear. Use `rg` to find mapper XML, repository methods, entity classes, migration files, and datasource config.
3. Build the smallest SQL that answers the question. Prefer selecting explicit columns over `SELECT *` when the table is wide or sensitive.
4. Run read-only SQL with `scripts/mysql_query.py` when Python MySQL drivers are available, or use the local `mysql` client if the environment already provides it.
5. Summarize findings with redacted values and include the exact safe SQL shape when useful.

## Write Or Validation Workflow

For new code that writes database data:

1. Read the implementation path to determine affected database, table, and expected fields.
2. Query the before state if possible.
3. Trigger or wait for the relevant test action if the user asks for end-to-end validation.
4. Query the after state with a narrow predicate.
5. Compare actual rows with the expected code behavior, including default values, enum values, timestamps, and nullable fields.

For explicit test-data fixes:

1. Draft the SQL and a rollback SQL first.
2. Ask for explicit confirmation unless the user has already given a direct command for that exact SQL and target.
3. Run inside a transaction when supported by the operation.
4. Verify affected row count and final state.

## Helper Script

Use `scripts/mysql_query.py` for repeatable CLI execution:

```bash
python scripts/mysql_query.py --sql "select 1"
python scripts/mysql_query.py --database order_deve --sql-file work/query.sql --format table
python scripts/mysql_query.py --allow-write --sql-file work/fix.sql
```

The script reads connection values from `TEST_MYSQL_*` environment variables by default. It rejects non-read SQL unless `--allow-write` is passed.

## Output Style

- For troubleshooting, lead with the conclusion and the rows or fields that prove it.
- For validation, report expected vs actual database state.
- For failed connections, report which non-secret part is missing or failed, such as host, port, network reachability, driver availability, or database name.
