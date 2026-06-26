# SQLite storage

## Location

- Default database file: `tai_alpha_output/tai_alpha.db` (next to the former JSON artifact directory).
- Override with environment variable `TAI_ALPHA_DB_PATH` (absolute or relative path).

## Schema

The canonical, idempotent DDL lives in:

- [`../../sql/schema/tai_alpha_schema_consolidated.sql`](../../sql/schema/tai_alpha_schema_consolidated.sql)

Tables:

- **`runs`** — one row per analysis run (`collect_json`, `backtest_json`, `score_json`, `ml_json` as JSON text).
- **`watchlist`** — alert targets/stops (replaces `watch.json`).

## Application bootstrap

Python code calls `tai_alpha.storage_sqlite.init_db(path)` before reads/writes. The same DDL is embedded in `tai_alpha/storage_sqlite.py` for zero-dependency bootstrap.

## Migrations

Breaking changes to columns should add a new migration file under `setup/sql/archive/` and update the consolidated schema for fresh installs.
