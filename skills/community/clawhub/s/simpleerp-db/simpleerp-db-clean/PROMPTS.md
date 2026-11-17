# OpenClaw prompts — SimpleERP DB

Use these as **slash-command bodies**, channel macros, or pasted instructions when the `simpleerp-db` agent workspace is bound.

**Prerequisites:** Node **18+**, `npm install` in this workspace, and network reachability to Oracle (`oracledb` thin mode; Instant Client only if required).

---

## Connection parameters (fill in each slash)

Same as [`.env.example`](.env.example) — the user supplies these on the slash line (or you use an existing workspace `.env` if already configured):

| Parameter | Example | Maps to |
|-----------|---------|---------|
| `${DB_USER}` | `your_user` | `DB_USER` |
| `${DB_PASSWORD}` | `your_password` | `DB_PASSWORD` |
| `${DB_CONNECT_STRING}` | `host:1521/SERVICE_NAME` | `DB_CONNECT_STRING` |

Use them **only** for database access in this session. **Do not** repeat `${DB_PASSWORD}` (or any secret value) in your reply, logs pasted to chat, or committed files.

---

## Credentials — all operating systems

Pick **one** approach (works on Windows, macOS, and Linux; no PowerShell-only steps):

| Priority | Method | When |
|----------|--------|------|
| 1 | Workspace **`.env`** already has `DB_*` | Local or pre-configured agent |
| 2 | **CLI flags** on `npm run sql` | Slash supplies credentials once per run |
| 3 | **`npm run sync-env`** then `npm run sql` | Persist slash credentials into `.env` for the session |
| 4 | Shell **environment variables** | Only if the host documents `export` / `$env:` for your OS |

**CLI flags (call `node` directly so flags are not stripped by npm on Windows):**

```bash
cd <simpleerp-db-workspace>
npm install
npm run check
node scripts/run-sql.mjs \
  --db-user="${DB_USER}" \
  --db-password="${DB_PASSWORD}" \
  --db-connect-string="${DB_CONNECT_STRING}" \
  -o output/last-query.json \
  "<your SELECT here>"
```

**Persist credentials to `.env` (optional):**

```bash
node scripts/sync-db-env.mjs \
  --db-user="${DB_USER}" \
  --db-password="${DB_PASSWORD}" \
  --db-connect-string="${DB_CONNECT_STRING}"
npm run sql:save -- "<your SELECT here>"
```

**npm-only (SQL in argv; flags after `npm run … --` are dropped on some platforms):** use workspace `.env`, or set `SQL_OUTPUT=output/last-query.json` in `.env`, then `npm run sql:save -- "<SELECT>"`.

---

## Slash template (run query, save + summarize)

```
/simpleerp_db query: ${QUESTION}

Connection (from .env.example):
- DB_USER = ${DB_USER}
- DB_PASSWORD = ${DB_PASSWORD}
- DB_CONNECT_STRING = ${DB_CONNECT_STRING}

Do this end-to-end without asking me to run commands manually:

1. cd to this agent workspace (OpenClaw cwd). Run `npm install` and `npm run check` if node_modules is missing.
2. Read references/table-reference.md or table-index.md as needed for correct table and column names.
3. **You** choose the read-only Oracle SQL (SELECT or WITH only) that answers ${QUESTION}. Use FETCH FIRST 50 ROWS ONLY unless a count or aggregate alone is enough.
4. Run the query (cross-platform):
   - If .env is not set: node scripts/sync-db-env.mjs --db-user="${DB_USER}" --db-password="${DB_PASSWORD}" --db-connect-string="${DB_CONNECT_STRING}"
   - Then: npm run sql:save -- "<your SELECT here>"
   - Or one shot: node scripts/run-sql.mjs --db-user=... --db-password=... --db-connect-string=... -o output/last-query.json "<your SELECT>"
5. Read output/last-query.json and reply with:
   - Plain-language answer to ${QUESTION}
   - Row count
   - The SQL you ran (no credentials)
6. Never print DB_PASSWORD, DB_USER passwords, or full .env contents in chat.
```

---

## Slash template (table lookup)

```
/simpleerp_db describe table ${TABLE}

Connection:
- DB_USER = ${DB_USER}
- DB_PASSWORD = ${DB_PASSWORD}
- DB_CONNECT_STRING = ${DB_CONNECT_STRING}

1. Open references/table-reference.md and find table ${TABLE} (exact Oracle name).
2. List columns (name + type) and note related tables from references/table-relationships.md.
3. Set credentials (node scripts/sync-db-env.mjs with --db-* if needed), then:
   npm run sql:save -- "SELECT * FROM ${TABLE} FETCH FIRST 5 ROWS ONLY"
4. Summarize sample rows; never echo DB_PASSWORD.
```

---

## Slash template (row count / health check)

```
/simpleerp_db count rows in ${TABLE}

Connection:
- DB_USER = ${DB_USER}
- DB_PASSWORD = ${DB_PASSWORD}
- DB_CONNECT_STRING = ${DB_CONNECT_STRING}

node scripts/sync-db-env.mjs --db-user="${DB_USER}" --db-password="${DB_PASSWORD}" --db-connect-string="${DB_CONNECT_STRING}"
npm run sql:save -- "SELECT COUNT(*) AS row_count FROM ${TABLE}"

Report the count from output/last-query.json. Do not print credentials.
```

---

## Shell environment variables (optional)

Only if you cannot use CLI flags or `.env`:

| OS | Example |
|----|---------|
| Linux / macOS | `export DB_USER=... DB_PASSWORD=... DB_CONNECT_STRING=...` then `npm run sql -- -o output/last-query.json "SELECT ..."` |
| PowerShell | `$env:DB_USER="..."; $env:DB_PASSWORD="..."; $env:DB_CONNECT_STRING="..."` then `npm run sql -- ...` |
| cmd.exe | `set DB_USER=...` / `set DB_PASSWORD=...` / `set DB_CONNECT_STRING=...` then `npm run sql -- ...` |

---

## Filled example

```
/simpleerp_db query: How many products do we have?

DB_USER=erp_readonly
DB_PASSWORD=***
DB_CONNECT_STRING=db.example.com:1521/ERPPRD

Run per PROMPTS.md: npm run sql with --db-* flags, COUNT on PRODUCT, output/last-query.json, summarize (no password in reply).
```

---

## Short system-style prompt

> From the simpleerp-db workspace, use `.env` or `--db-user` / `--db-password` / `--db-connect-string` from my slash parameters, run `npm run sql -- -o output/last-query.json` with your bounded SELECT, read `output/last-query.json`, and summarize. Never expose DB credentials in the reply.
