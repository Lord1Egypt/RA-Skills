# Package ID SQL Sync

Use this when AI/runtime looks up active SafeFlow package id from SQL instead of hardcoded env.

## SQLite (Default)

```bash
cd .claude/skills/safe-flow-sui-skill/scripts
./sync_package_id_to_sql.sh --driver sqlite
```

Default DB path:

- `.claude/skills/safe-flow-sui-skill/scripts/.safeflow-runtime.db`

Default table schema:

- table: `safeflow_runtime_config`
- columns: `config_key`, `config_value`, `updated_at`
- key used: `package_id`

## Postgres

```bash
./sync_package_id_to_sql.sh \
  --driver postgres \
  --postgres-dsn "postgres://user:pass@localhost:5432/dbname?sslmode=disable"
```

## Custom Table/Key

```bash
./sync_package_id_to_sql.sh \
  --driver sqlite \
  --table ai_runtime_config \
  --key safeflow_package_id
```

The script validates table/key identifier formats to avoid unsafe SQL interpolation.
