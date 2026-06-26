---
name: sql-query-copilot
description: Simplify SQL querying and troubleshooting for MySQL, PostgreSQL, and SQLite. Use when users ask to inspect schema, convert natural language to SQL, debug SQL errors, run explain plans, lint risky SQL, or validate data with safe read-only execution.
---

# SQL Query Copilot

## Overview

Use this skill to turn plain-language requests into executable SQL with a predictable, low-risk workflow.
Default to read-only execution and validate every query against schema before running.

## Quick Start

Set `SQL_DSN` first (or pass `--dsn` each time).

```bash
# PowerShell
$env:SQL_DSN="mysql://user:password@127.0.0.1:3306/stock_monitor"
$env:SQL_DSN="postgres://user:password@127.0.0.1:5432/stock_monitor"
$env:SQL_DSN="sqlite:///d:/data/demo.db"

# Windows CMD
set SQL_DSN=mysql://user:password@127.0.0.1:3306/stock_monitor
set SQL_DSN=postgres://user:password@127.0.0.1:5432/stock_monitor
set SQL_DSN=sqlite:///d:/data/demo.db

# Bash / Zsh
export SQL_DSN="mysql://user:password@127.0.0.1:3306/stock_monitor"
export SQL_DSN="postgres://user:password@127.0.0.1:5432/stock_monitor"
export SQL_DSN="sqlite:///d:/data/demo.db"
```

Core commands:

```bash
python scripts/sql_easy.py tables
python scripts/sql_easy.py describe daily_kline
python scripts/sql_easy.py lint --sql "SELECT * FROM daily_kline"
python scripts/sql_easy.py explain --sql "SELECT code, close FROM daily_kline WHERE trade_date >= '2026-01-01'"
python scripts/sql_easy.py query --sql "SELECT code, close FROM daily_kline ORDER BY trade_date DESC" --limit 50
python scripts/sql_easy.py query --sql "SELECT code, close FROM daily_kline" --summary
python scripts/sql_easy.py ask --q "show symbols with old sell signals older than 20 days" --summary
python scripts/sql_easy.py profile
```

Set `OPENAI_API_KEY` (or pass `--api-key`) to use `ask`.

## v0.2 Highlights

- Multi-engine support: MySQL, PostgreSQL, SQLite.
- SQL lint engine: catches high-risk patterns before execution.
- Explain mode: quickly inspect query plan (`EXPLAIN` / `EXPLAIN QUERY PLAN`).
- Natural-language mode: `ask` generates SQL from user intent.
- Query summary: auto profile returned columns (null ratio, distinct count, min/max/avg).
- Slow query warning: highlights expensive queries using `--slow-ms`.
- Audit log: write command metadata to JSONL via `--audit-log` or `SQL_EASY_AUDIT_LOG`.

## Workflow

1. Clarify the metric and grain.
Ask for time window, dimensions, and output columns before writing SQL.

2. Discover schema first.
Run `tables`, `describe <table>`, and `profile` before any complex SQL.

3. Draft SQL in read-only mode.
Use `SELECT` or `WITH`; keep columns explicit and add time filters.

4. Execute with guardrails.
Run via `scripts/sql_easy.py query`, keep `--limit` unless full export is explicitly needed.

5. Validate results.
Cross-check row count, null ratio, and edge dates; adjust query and rerun.

## Guardrails

- Default to read-only SQL.
- Reject destructive statements (`INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `TRUNCATE`, etc.).
- Prefer explicit columns over `SELECT *` for production/report queries.
- Run `lint` before heavy or scheduled queries.
- Run `explain` before approving complex joins/window queries.
- Always quote identifiers when table/column names are uncertain.
- For business decisions, provide both SQL and a short interpretation of returned data.

## Query Patterns

Read `references/query_patterns.md` when creating:

- Top-N and ranking queries
- Time-window aggregation
- Dedup with window functions
- Funnel-style conditional counts
- Data quality checks (null/duplicate/outlier)

Read `references/chanquant_templates.md` for Chanquant-specific query templates.
