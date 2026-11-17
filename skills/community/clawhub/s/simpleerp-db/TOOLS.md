# TOOLS.md - SimpleERP DB

Cross-platform (Windows, macOS, Linux). All paths are relative to the workspace root unless absolute.

## Query pipeline

```bash
npm install
npm run check
npm run sql -- "SELECT 1 AS x FROM DUAL"
```

With saved output (slash macros and reports):

```bash
npm run sql:save -- "SELECT PROD_ID, PROD_NAME FROM PRODUCT FETCH FIRST 10 ROWS ONLY"
```

`npm run sql:save` embeds `-o output/last-query.json` in the script (reliable on Windows). For other output paths, call Node directly:

```bash
node scripts/run-sql.mjs -o output/my-report.json "SELECT ..."
```

Note: on Windows, `npm run sql -- -o …` and `npm run sql -- --db-user=…` often **do not** reach the script (npm drops flags after `--`). Use `sql:save`, `.env`, `SQL_OUTPUT` in `.env`, or `node scripts/run-sql.mjs …` directly.

### Credentials (pick one)

| Method | Command |
|--------|---------|
| **`.env` file** | Copy `.env.example` → `.env`; `run-sql.mjs` loads it automatically |
| **CLI flags** | `node scripts/run-sql.mjs --db-user=U --db-password=P --db-connect-string=host:1521/SVC "SELECT ..."` |
| **sync-env** | `node scripts/sync-db-env.mjs --db-user=U ...` then `npm run sql:save -- "SELECT ..."` |
| **Shell env** | Set `DB_USER`, `DB_PASSWORD`, `DB_CONNECT_STRING` (syntax varies by OS; see `PROMPTS.md`) |

Stdin (one statement):

```bash
echo "SELECT COUNT(*) AS c FROM USER_TABLES" | npm run sql -- -o output/last-query.json
```

## Environment (`.env`)

Copy **`.env.example`** → **`.env`**:

| Variable | Purpose |
|----------|---------|
| `DB_USER` | Oracle user |
| `DB_PASSWORD` | **Secret** — never echo in chat |
| `DB_CONNECT_STRING` | e.g. `host:1521/SERVICE_NAME` |

Optional:

| Variable | Purpose |
|----------|---------|
| `SIMPLEERP_TABLES_SQL` | Absolute path to `TABLES.sql` for `gen-table-index` |
| `SQL_OUTPUT` | Default output file for `run-sql.mjs` when `-o` is not passed |

Use forward slashes or native paths in `SIMPLEERP_TABLES_SQL` (e.g. `C:/data/TABLES.sql` on Windows).

## Allowed SQL

Only **`SELECT`**, **`WITH … SELECT`**, and **`EXPLAIN PLAN FOR …`**. All else is rejected.

## Schema regeneration

```bash
npm run table-index
# or
node scripts/gen-table-index.mjs --tables-sql /path/to/TABLES.sql
```

Updates `references/table-index.md`, `table-reference.md`, `table-relationships.md`.

## Outputs (under `output/`)

| File | Description |
|------|-------------|
| `output/last-query.json` | JSON rows from the last `npm run sql` with `-o` or `SQL_OUTPUT` |

Query stdout is always JSON rows; stderr may show `(0 rows)` or `Wrote <path>`.

## References (read before writing SQL)

| File | Use |
|------|-----|
| `references/table-index.md` | Table name discovery |
| `references/table-reference.md` | Column names + types |
| `references/table-relationships.md` | Join hints |
| `references/journal-pattern.md` | `*_JNL` audit tables |

Full rules: **`PLAYBOOK.md`**. Slash templates: **`PROMPTS.md`**.
