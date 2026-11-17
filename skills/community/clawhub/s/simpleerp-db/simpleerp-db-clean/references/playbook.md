# Playbook — simpleerp-db

Read-only Oracle SQL against the SimpleERP schema.

## Scope: queries only

`scripts/run-sql.mjs` accepts **only**:

- `SELECT …`
- `WITH …` (CTE leading with `WITH`)
- `EXPLAIN PLAN …`

It **rejects** `INSERT`, `UPDATE`, `DELETE`, `MERGE`, DDL, and PL/SQL blocks.

| Use another path | Use this skill |
|------------------|----------------|
| Application CRUD | Ad hoc SELECTs and reports |
| Mutations | Never via `run-sql.mjs` |
| Audit history | SELECT on `*_JNL` tables |

## Credentials

1. Read from `process.env` (includes `.env` when present).
2. If any `DB_*` is missing, fail with a clear error.
3. Do **not** prompt for secrets in chat.

Secret safety:

- Never print, quote, or confirm `DB_PASSWORD` or full `.env` contents.
- If asked to show `.env`, provide only `.env.example` with placeholders.
- State only whether each required key is present or missing.

## Schema reference

1. [table-index.md](table-index.md) — table names by heuristic group
2. [table-reference.md](table-reference.md) — columns and types
3. [table-relationships.md](table-relationships.md) — join hints
4. [journal-pattern.md](journal-pattern.md) — `*_JNL` usage

Regenerate after schema changes: `npm run setup` or `npm run table-index`.

Do not trust `references/*.md` older than the last `npm run setup` (see `output/.setup-status.json`).

## Safety

- Prefer `FETCH FIRST n ROWS ONLY` when exploring.
- Do not concatenate untrusted input into SQL strings.

## Agent execution

When a task needs a DB read:

1. On **Windows PowerShell**, run `Set-ExecutionPolicy RemoteSigned -Scope Process` if `npm` scripts are blocked (session only).
2. Run `npm run check`; if setup is missing or stale, run `npm run setup`.
3. Look up tables in `references/` before writing SQL.
4. Run `npm run sql` or `npm run sql:save` — do not only tell the user what to run.
5. If credentials are missing, report which `DB_*` keys are absent; do not ask for passwords in chat.

Per-OS copy/setup commands: [bootstrap.md](bootstrap.md).
