# Publish Checklist (ClawHub)

## Functional checks

- Run `python scripts/sql_easy.py tables` against one sample DB.
- Run `describe`, `lint`, `explain`, `query --summary`, `profile`.
- Verify read-only guard blocks `UPDATE/DELETE/DDL`.
- Verify `--strict-lint` blocks risky SQL.
- Verify audit logging writes one JSON line per command.

## Compatibility checks

- MySQL: `mysql://user:pass@host:3306/db`
- PostgreSQL: `postgres://user:pass@host:5432/db`
- SQLite: `sqlite:///path/to/file.db`

## Publishing notes

- Keep `SKILL.md` focused on workflow and trigger scenarios.
- Keep `agents/openai.yaml` concise and user-facing.
- Include 5-10 realistic demo commands in release notes.
- Mention explicit security default: read-only + lint + explain.
