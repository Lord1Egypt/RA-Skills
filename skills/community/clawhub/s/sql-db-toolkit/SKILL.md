---
name: sql-db-toolkit
description: Comprehensive SQL database toolkit for querying, schema inspection, data export, and migration management. Use when the user wants to: (1) Query a database with SELECT/INSERT/UPDATE/DELETE, (2) Inspect table schemas, indexes, and foreign keys, (3) Export data to CSV/JSON, (4) Generate SQL migrations or schema diffs, (5) Run database backups and restore, (6) Analyze query performance with EXPLAIN, (7) Work with SQLite, PostgreSQL, MySQL, or any sqlalchemy-compatible database.
---

# SQL Database Toolkit

Query, inspect, export, and manage databases via conversation. Supports SQLite (no setup) and PostgreSQL/MySQL (with connection string).

## Quick Start

```bash
# SQLite - no setup needed
python3 skills/sql-db-toolkit/scripts/db_query.py --db my.db --sql "SELECT * FROM users LIMIT 5"

# PostgreSQL
python3 skills/sql-db-toolkit/scripts/db_query.py --conn "postgresql://user:pass@host:5432/db" --sql "SELECT table_name FROM information_schema.tables"
```

## Common Commands

### Query Database
```bash
python3 skills/sql-db-toolkit/scripts/db_query.py --db my.db --sql "SELECT id, name, email FROM users WHERE active = 1" --format table
```

### Inspect Schema
```bash
python3 skills/sql-db-toolkit/scripts/db_schema.py --db my.db
```

### Export to CSV
```bash
python3 skills/sql-db-toolkit/scripts/db_export.py --db my.db --sql "SELECT * FROM orders" --output orders.csv
```

### Backup Database
```bash
python3 skills/sql-db-toolkit/scripts/db_backup.py --db my.db --output backup/
```

## Scripts

| Script | Purpose |
|--------|---------|
| `db_query.py` | Execute SQL queries with formatted output (table/JSON/CSV) |
| `db_schema.py` | Inspect tables, columns, indexes, FKs, triggers |
| `db_export.py` | Export query results to CSV, JSON, or SQL dump |
| `db_backup.py` | Backup SQLite DB or dump PostgreSQL/MySQL |
| `db_migrate.py` | Compare schemas, generate migration SQL |

## Connection Strings

```python
# SQLite
sqlite:///path/to/db.sqlite

# PostgreSQL
postgresql://user:password@host:5432/database

# MySQL
mysql+pymysql://user:password@host:3306/database
```

## Options

All scripts support `--help` for full argument reference. Key shared options:

- `--db <path>` — SQLite database file path
- `--conn <url>` — SQLAlchemy connection string
- `--sql <query>` — SQL query to execute
- `--format table|json|csv` — Output format
- `--verbose` — Show execution time and row counts
