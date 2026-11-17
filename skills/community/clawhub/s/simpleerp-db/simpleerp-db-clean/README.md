# SimpleERP DB skill (clean / not yet set up)

This package has **no** credentials, `node_modules`, live DDL, or generated table docs yet.

## First-time setup

**Windows (PowerShell):**

```powershell
Set-ExecutionPolicy RemoteSigned -Scope Process
cd path\to\simpleerp-db-clean
npm install
Copy-Item .env.example .env
# Edit .env: DB_USER, DB_PASSWORD, DB_CONNECT_STRING (optional DB_SCHEMA)
npm run setup
```

**macOS / Linux:**

```bash
cd path/to/simpleerp-db-clean
npm install
cp .env.example .env
# Edit .env
npm run setup
```

`npm run setup` exports Oracle DDL → `schema/TABLES.sql`, regenerates `references/table-*.md`, smoke-tests SQL, and writes `output/.setup-status.json`.

## Not included (by design)

- `.env` (secrets)
- `node_modules/`
- `schema/TABLES.sql`
- `output/.setup-status.json` / query results
- Populated `references/table-index.md`, `table-reference.md`, `table-relationships.md` (stubs until setup)

See [references/bootstrap.md](references/bootstrap.md) and [SKILL.md](SKILL.md).
