---
name: warehouse-ui
description: Universal database IDE CLI — query PostgreSQL, MySQL, SQLite, BigQuery, MongoDB with cost projection
version: 0.10.0
homepage: https://github.com/olegnazarov23/warehouse-ui
metadata: {"openclaw": {"emoji": "db", "requires": {"bins": ["warehouse-ui"]}, "primaryEnv": "DATABASE_URL", "os": ["darwin", "linux", "win32"], "install": [{"kind": "github-release", "repo": "olegnazarov23/warehouse-ui", "bins": ["warehouse-ui"], "label": "Download from GitHub Releases"}]}}
---

# Warehouse UI — Database Query Tool

Use this skill to connect to databases, explore schemas, run queries, estimate costs, and generate SQL from natural language.

## Installation

Download from GitHub Releases: https://github.com/olegnazarov23/warehouse-ui/releases

- **macOS**: Download the DMG, drag to Applications, then add to PATH:
  `ln -s /Applications/warehouse-ui.app/Contents/MacOS/warehouse-ui /usr/local/bin/warehouse-ui`
- **Windows**: Run the installer EXE, it adds to PATH automatically

## Supported Databases

- PostgreSQL
- MySQL
- SQLite
- BigQuery (with cost projection)
- MongoDB

## Connect to a Database

Before running queries, establish a connection:

```bash
# From a connection URL
warehouse-ui connect --url "postgres://user:pass@localhost:5432/mydb"

# With explicit parameters
warehouse-ui connect --type postgres --host localhost:5432 --database mydb --user admin --password secret

# SQLite (local file)
warehouse-ui connect --type sqlite --database /path/to/data.db

# BigQuery (service account)
warehouse-ui connect --type bigquery --database my-gcp-project --option sa_json_path=/path/to/sa.json

# MySQL
warehouse-ui connect --url "mysql://user:pass@localhost:3306/mydb"
```

## Check Connection Status

```bash
warehouse-ui status
```

## Explore Schema

```bash
# List all databases
warehouse-ui schema list-databases

# List tables in a database
warehouse-ui schema list-tables --database mydb

# Describe a table (columns, types, nullability)
warehouse-ui schema describe users --database mydb
```

## Run Queries

```bash
# SQL as argument
warehouse-ui query "SELECT * FROM users LIMIT 10"

# With explicit limit
warehouse-ui query --sql "SELECT count(*) FROM orders WHERE created_at > '2024-01-01'" --limit 1000

# From a SQL file
warehouse-ui query --file path/to/report.sql
```

Output is JSON with columns, rows, row count, duration, and (for BigQuery) bytes processed and cost.

## Cost Estimation (Dry Run)

Check query cost before executing — especially useful for BigQuery:

```bash
warehouse-ui dry-run "SELECT * FROM big_dataset.events WHERE date > '2024-01-01'"
```

Returns: estimated bytes, estimated cost (USD), statement type, referenced tables, and warnings.

## AI-Powered Queries

Generate SQL from natural language using a configured AI provider (set OPENAI_API_KEY or ANTHROPIC_API_KEY):

```bash
# Generate SQL only
warehouse-ui ai "show me the top 10 customers by total revenue"

# Generate and execute
warehouse-ui ai "find all orders from last week that were cancelled" --execute
```

## List Saved Connections

```bash
warehouse-ui connections
```

## Query History

```bash
warehouse-ui history --limit 10
warehouse-ui history --search "SELECT"
```

## Disconnect

```bash
warehouse-ui disconnect
```

## Output Format

All commands output JSON to stdout by default. Add `--format table` for human-readable output. Errors are JSON on stderr with exit code 1.

## Environment Variables

- `DATABASE_URL` — Auto-connect without explicit `connect` step (supports postgres://, mysql://, sqlite://, mongodb://)
- `OPENAI_API_KEY` — Required for `ai` command with OpenAI
- `ANTHROPIC_API_KEY` — Required for `ai` command with Anthropic

## Tips

- Set `DATABASE_URL` to skip the `connect` step entirely
- Use `schema describe <table>` to understand table structure before querying
- Use `dry-run` on BigQuery to check costs before executing expensive queries
- Use `--limit` to control result size for large tables
- Use `connections` to see databases already configured in the desktop app
