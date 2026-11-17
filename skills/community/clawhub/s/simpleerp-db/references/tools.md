# Tools — simpleerp-db

Cross-platform (Windows, macOS, Linux). Paths are relative to the skill root.

## OS notes

| OS | Before `npm run` | Copy `.env.example` → `.env` |
|----|------------------|----------------------------|
| **Windows PowerShell** | `Set-ExecutionPolicy RemoteSigned -Scope Process` | `Copy-Item .env.example .env` |
| **Windows cmd** | (usually not needed) | `copy .env.example .env` |
| **macOS / Linux** | (usually not needed) | `cp .env.example .env` |

If PowerShell blocks `npm.ps1`, use `node scripts/setup.mjs` or `node scripts/run-sql.mjs` directly. Full per-OS steps: [references/bootstrap.md](references/bootstrap.md).

## Bootstrap (first use)

```bash
npm install
cp .env.example .env   # set DB_USER, DB_PASSWORD, DB_CONNECT_STRING
npm run setup
```

`npm run setup` exports live DDL, regenerates `references/*.md`, runs a smoke query, and writes `output/.setup-status.json`.

## Query pipeline

```bash
npm run check
npm run sql -- "SELECT 1 AS x FROM DUAL"
```

Save results:

```bash
npm run sql:save -- "SELECT PROD_ID, PROD_NAME FROM PRODUCT FETCH FIRST 10 ROWS ONLY"
```

On Windows, prefer `sql:save`, `.env`, or call Node directly when npm drops flags:

```bash
node scripts/run-sql.mjs -o output/my-report.json "SELECT ..."
```

### Credentials

| Method | Command |
|--------|---------|
| `.env` file | Copy `.env.example` → `.env` |
| CLI flags | `node scripts/run-sql.mjs --db-user=U --db-password=P --db-connect-string=host:1521/SVC "SELECT ..."` |
| sync-env | `node scripts/sync-db-env.mjs --db-user=U ...` |

## Environment (`.env`)

| Variable | Purpose |
|----------|---------|
| `DB_USER` | Oracle user |
| `DB_PASSWORD` | Secret — never echo in chat |
| `DB_CONNECT_STRING` | e.g. `host:1521/SERVICE_NAME` |
| `DB_SCHEMA` | Schema for DDL export (default `SIMPLEERP`) |
| `SETUP_MAX_AGE_DAYS` | Re-run setup when status file is older (default `7`) |
| `SIMPLEERP_TABLES_SQL` | Optional override path to TABLES.sql |
| `SQL_OUTPUT` | Default output file when `-o` is not passed |

## Schema commands

```bash
npm run export-schema          # live DDL → schema/TABLES.sql
npm run table-index            # regenerate references/*.md
```

## Outputs

| File | Description |
|------|-------------|
| `output/last-query.json` | Last query with `-o` or `sql:save` |
| `output/.setup-status.json` | Setup timestamp and table count |
| `schema/TABLES.sql` | Live-exported DDL (gitignored) |

## References

| File | Use |
|------|-----|
| `references/table-index.md` | Table name discovery |
| `references/table-reference.md` | Column names + types |
| `references/table-relationships.md` | Join hints |
| `references/journal-pattern.md` | `*_JNL` audit tables |
| `references/playbook.md` | Safety and credentials |
| `references/bootstrap.md` | Setup details |
