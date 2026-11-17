---
name: simpleerp-db
description: >-
  Read-only Oracle SQL and live schema export for SimpleERP. Runs npm run setup
  (export DDL + regenerate references) then SELECT/WITH/EXPLAIN PLAN via
  scripts/run-sql.mjs. Use when the user asks about SimpleERP database tables,
  columns, joins, row counts, or ad-hoc SQL reports. Requires Oracle credentials.
version: 1.0.0
metadata:
  openclaw:
    skillKey: simpleerp-db
    emoji: "🗄️"
    requires:
      env:
        - DB_USER
        - DB_PASSWORD
        - DB_CONNECT_STRING
      bins:
        - node
        - npm
    primaryEnv: DB_USER
    envVars:
      - name: DB_USER
        required: true
        description: Oracle database user for read-only queries.
      - name: DB_PASSWORD
        required: true
        description: Oracle password (never echo in chat).
      - name: DB_CONNECT_STRING
        required: true
        description: "Easy Connect string, e.g. host:1521/SERVICE_NAME"
      - name: DB_SCHEMA
        required: false
        description: Schema owner for DDL export (default SIMPLEERP).
      - name: SETUP_MAX_AGE_DAYS
        required: false
        description: Re-run npm run setup when status file is older than this.
      - name: SIMPLEERP_TABLES_SQL
        required: false
        description: Override path to TABLES.sql (dev only).
    install:
      - kind: node
        package: oracledb
        bins: []
---

# SimpleERP DB

Read-only Oracle analyst for the SimpleERP schema. Query-only — no DML/DDL through this skill.

## First use (required)

Before any query or schema lookup:

```bash
npm install
cp .env.example .env   # set DB_USER, DB_PASSWORD, DB_CONNECT_STRING
npm run setup
```

The agent **must** run `npm run check` and, if setup is missing or stale, `npm run setup` before using `references/*.md` or running SQL.

If `DB_*` credentials are missing: tell the user to copy `.env.example` → `.env`. **Never** ask for `DB_PASSWORD` in chat.

**Windows (PowerShell):** run `Set-ExecutionPolicy RemoteSigned -Scope Process` in the session before `npm run` if scripts are blocked. See [references/bootstrap.md](references/bootstrap.md) for per-OS commands (`Copy-Item` vs `cp`, cmd, macOS/Linux).

## Quick commands

```bash
npm run check
npm run setup
npm run sql -- "SELECT 1 AS x FROM DUAL"
npm run sql:save -- "SELECT COUNT(*) AS c FROM PRODUCT"
npm run export-schema
npm run table-index
```

## Reference map

| Doc | Contents |
|-----|----------|
| [references/bootstrap.md](references/bootstrap.md) | Setup flow and prerequisites |
| [references/tools.md](references/tools.md) | Commands, env vars, outputs |
| [references/playbook.md](references/playbook.md) | Credentials, safety, agent rules |
| [references/table-index.md](references/table-index.md) | Table name discovery (after setup) |
| [references/table-reference.md](references/table-reference.md) | Columns and types (after setup) |
| [references/table-relationships.md](references/table-relationships.md) | Join hints (after setup) |
| [references/journal-pattern.md](references/journal-pattern.md) | `*_JNL` audit tables |

## Agent policy

- Execute `npm run setup` and `npm run sql` yourself when the task needs them.
- Read `references/table-reference.md` before writing SQL.
- Use only SELECT / WITH / EXPLAIN PLAN through `run-sql.mjs`.
- Prefer `FETCH FIRST n ROWS ONLY` when exploring large tables.

## Publish

See [PUBLISH.md](PUBLISH.md) for ClawHub upload checklist.
