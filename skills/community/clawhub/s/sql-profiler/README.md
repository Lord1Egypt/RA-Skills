# SQL Profiler

> OpenClaw skill for profiling and optimizing SQL queries across Databricks, PostgreSQL, and Spark SQL.

## What it does

`sql-profiler` helps data engineers identify and fix performance bottlenecks in SQL queries. Paste a slow query (with or without EXPLAIN output) and get:

- Plain-English explanation of what's slow and why
- Specific rewrite suggestions with before/after examples
- Index recommendations and partitioning strategies
- Estimated performance impact of each suggestion

## Supported dialects

- **Databricks SQL** — Delta Lake, Z-ORDER, OPTIMIZE, query profiles
- **PostgreSQL** — EXPLAIN ANALYZE, index suggestions, vacuum strategies
- **Spark SQL** — physical plan analysis, broadcast hints, partition tuning
- **ANSI SQL** — generic optimization patterns

## Install

```bash
npx clawhub install sql-profiler
```

## Usage

```
/sql-profiler analyze --query "SELECT * FROM orders WHERE status = 'pending'" --dialect postgresql
/sql-profiler explain --output "<paste EXPLAIN ANALYZE output here>"
/sql-profiler rewrite --query "SELECT * FROM large_table JOIN ..." --goal "reduce scan time"
```

## Author

[Nerikko](https://clawhub.com/skills?author=Nerikko) · also see [databricks-helper](https://clawhub.com/skills/databricks-helper)
