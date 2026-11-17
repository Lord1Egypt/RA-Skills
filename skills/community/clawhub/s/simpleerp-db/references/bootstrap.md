# Bootstrap — simpleerp-db

## Prerequisites

- **Node.js 18+**
- **npm**
- Oracle reachable from the host running the skill
- **Oracle Instant Client** only if `oracledb` thin mode fails (DPI-1047)

## OS-specific shell setup

Agents and users must use a shell where `node` and `npm` can run. On **Windows PowerShell**, script execution is often restricted by default.

### Windows (PowerShell) — recommended

Run once **per terminal session** before `npm install` / `npm run setup` (does not change machine-wide policy):

```powershell
Set-ExecutionPolicy RemoteSigned -Scope Process
cd path\to\simpleerp-db
npm install
Copy-Item .env.example .env
# Edit .env: DB_USER, DB_PASSWORD, DB_CONNECT_STRING, optional DB_SCHEMA
npm run setup
```

If `npm run` still fails, call Node directly (no execution-policy change needed for `.mjs`):

```powershell
node scripts/setup.mjs
node scripts/run-sql.mjs "SELECT 1 AS x FROM DUAL"
```

### Windows (cmd)

```cmd
cd path\to\simpleerp-db
npm install
copy .env.example .env
npm run setup
```

### macOS / Linux (bash, zsh)

```bash
cd path/to/simpleerp-db
npm install
cp .env.example .env
# Edit .env: DB_USER, DB_PASSWORD, DB_CONNECT_STRING, optional DB_SCHEMA
npm run setup
```

Optional: set credentials in the shell instead of `.env` (session only):

```bash
export DB_USER=your_user
export DB_PASSWORD=your_password
export DB_CONNECT_STRING=host:1521/SERVICE_NAME
npm run setup
```

Never paste real passwords into chat or commit them to tracked files.

### Troubleshooting by OS

| Symptom | Windows | macOS / Linux |
|---------|---------|----------------|
| `npm.ps1 cannot be loaded` / scripts disabled | `Set-ExecutionPolicy RemoteSigned -Scope Process` | Rare; ensure `node` / `npm` on `PATH` |
| `npm run sql -- -o …` drops flags | Use `npm run sql:save` or `node scripts/run-sql.mjs -o …` | Same |
| `oracledb` DPI-1047 | Install [Oracle Instant Client](https://node-oracledb.readthedocs.io/) | Same |
| Copy env template | `Copy-Item .env.example .env` | `cp .env.example .env` |

## First-time setup

See **OS-specific shell setup** above, then:

```bash
npm run check
npm run sql -- "SELECT 1 AS x FROM DUAL"
```

## What `npm run setup` does

1. `npm install` (if needed)
2. Verify Node, `oracledb`, and `DB_*` credentials
3. Export live DDL via `export-tables-sql.mjs` → `schema/TABLES.sql`
4. Regenerate `references/table-index.md`, `table-reference.md`, `table-relationships.md`
5. Smoke test: `SELECT 1 FROM DUAL`
6. Write `output/.setup-status.json`

## Readiness check

```bash
npm run check
```

Exits non-zero when:

- Node < 18 or `oracledb` not installed
- `output/.setup-status.json` is missing or older than `SETUP_MAX_AGE_DAYS` (default 7)

## Re-run setup

```bash
npm run setup
```

Use `--skip-export` to reuse existing `schema/TABLES.sql`:

```bash
node scripts/setup.mjs --skip-export
```

## ClawHub install

After installing from ClawHub:

1. `cd` into the skill folder
2. `npm install`
3. Copy `.env.example` → `.env` and configure `DB_*`
4. `npm run setup`

The published bundle does not include `node_modules/`, `.env`, or `schema/TABLES.sql`.
