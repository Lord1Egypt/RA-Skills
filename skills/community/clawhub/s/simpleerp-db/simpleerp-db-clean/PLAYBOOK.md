# SimpleERP Oracle database — playbook

Read-only Oracle SQL against the SimpleERP schema. Everything you need for queries lives under this workspace except **Oracle Instant Client** (or your platform’s equivalent for `oracledb`).

## Scope: queries only

`scripts/run-sql.mjs` accepts **only**:

- `SELECT …`
- `WITH …` (CTE leading with `WITH`)
- `EXPLAIN PLAN …`

It **rejects** `INSERT`, `UPDATE`, `DELETE`, `MERGE`, DDL, and PL/SQL blocks. For changes, use **SQLcl**, **SQL\*Plus**, or another DBA tool.

| Use another path | Use this workspace |
|------------------|-------------------|
| Application CRUD, workflows | Ad hoc **SELECT**s, reports, joins for analysis |
| Mutations | **Never** via `run-sql.mjs` |
| Deep audit history | **`SELECT`** on `*_JNL` tables (see [journal-pattern.md](references/journal-pattern.md)) |

**Trust:** Effective access is whatever the Oracle user (`DB_USER`) is granted. This skill does not implement application-level permission models.

## Credentials

Credential handling is strictly non-interactive:

1. Read credentials from **`process.env`** (includes **`<workspace>/.env`** when present).
2. If any of `DB_USER`, `DB_PASSWORD`, or `DB_CONNECT_STRING` is missing, **fail with a clear error and stop**.
3. Do **not** prompt for secrets and do **not** scrape disk for credentials.

Copy [.env.example](.env.example) → `.env` in this folder for local runs. Never commit `.env` or passwords into tracked files.

Secret safety rules:

- Treat `.env` files and `DB_*` environment variable values as **secrets**.
- **Never print, quote, summarize, or confirm actual secret values** from `.env`, shell env, logs, or command output.
- If asked to "show the `.env` file", provide only a sanitized template from [.env.example](.env.example) with placeholders.
- If you must reference configured credentials, only state whether each required key is present/missing; do not reveal contents.

**`CONNECT_STRING`:** Oracle Easy Connect form, e.g. `host:1521/SERVICE_NAME`.

## Schema reference

1. **[references/table-index.md](references/table-index.md)** — Fast map of table names (~188 base + ~155 `*_JNL` in a typical export). Groups are **name-prefix heuristics**, not guaranteed business modules.
2. **[references/table-reference.md](references/table-reference.md)** — Exact column names and Oracle data types per table (use this first when writing SQL).
3. **[references/table-relationships.md](references/table-relationships.md)** — Connected-table map (`*_ID` links, curated business chains).
4. **[references/journal-pattern.md](references/journal-pattern.md)** — `*_JNL` usage guidance and sample queries.
5. **Column-level DDL** — Source of truth remains **`TABLES.sql`** (`--  DDL for Table TABLE_NAME`).

Typical export schema: **`SIMPLEERP`**. Use unqualified table names by default (for example `PRODUCT`) unless you explicitly need a schema prefix.

### Regenerating references

```bash
node scripts/gen-table-index.mjs
```

- **`--tables-sql <path>`** — Input DDL file (required if the default path does not exist).
- **`SIMPLEERP_TABLES_SQL`** — Optional env var: absolute path to `TABLES.sql`.
- **Default input path** when neither is set: three levels above the workspace, then `simpleerp-api/db/TABLES.sql` (monorepo convenience). **Standalone copies** should set **`SIMPLEERP_TABLES_SQL`** or pass **`--tables-sql`**.
- **`--out`**, **`--detail-out`**, **`--rel-out`** — Override generated markdown paths under `references/`.

## Running queries (`run-sql.mjs`)

**Prerequisites:** Node **18+**, **`npm install`** in this workspace (`npm run check`), Oracle client libraries only if thin mode cannot connect.

- **Credentials:** `<workspace>/.env`, shell `DB_*` env vars, or **`--db-user` / `--db-password` / `--db-connect-string`** CLI flags (preferred for headless agents on any OS).
- **Output:** JSON array on stdout; **`-o output/last-query.json`**, **`--out=`**, or env **`SQL_OUTPUT`** (see `TOOLS.md`).
- **SQL in argv:** entire query is joined from remaining args; prefer stdin for complex SQL.
- **Binds:** The script does **not** expose bind variables; only trusted literals.

### If `oracledb` fails to load

Run **`npm install`** in the workspace. **DPI-1047** / missing client: install **Oracle Instant Client** per [node-oracledb](https://node-oracledb.readthedocs.io/).

## Safety

- Prefer **`FETCH FIRST n ROWS ONLY`** (12c+) or `WHERE` limits; avoid unbounded exports on large tables.
- Do not concatenate untrusted input into SQL strings.

## Agent execution

When the user’s task needs a DB read or schema regeneration, **execute the commands yourself** in this workspace—do not only tell the user what to run, and **do not ask** whether it is OK to run `run-sql.mjs` or `gen-table-index.mjs` when the task clearly needs them.

- **Automatic runs:** If `DB_*` credentials are available, run `npm run sql -- "<QUERY>"` immediately. Run `npm run table-index` when regenerating references. Ensure `npm install` once if modules are missing.
- **Credentials missing:** Do not prompt for passwords. Let the script fail; tell the user only that `DB_*` must be set (see `.env.example`), without asking them to paste secrets into chat.
- **Scope:** Use **only** `SELECT` / `WITH` / `EXPLAIN PLAN` through this script.
