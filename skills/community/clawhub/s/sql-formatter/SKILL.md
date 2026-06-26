---
name: sql-formatter
description: Format, minify, and lint SQL queries from the command line. Formats SQL with proper indentation and keyword casing, minifies by removing whitespace and comments, and lints for common anti-patterns (SELECT *, inconsistent casing, missing semicolons, trailing whitespace). No external dependencies — pure Python. Use when formatting SQL queries, cleaning up SQL files, minifying SQL for production, or checking SQL quality.
---

# SQL Formatter

Format, minify, and lint SQL with zero dependencies.

## Commands

All commands use `scripts/sql_format.py`.

### Format SQL

```bash
python3 scripts/sql_format.py format --sql "SELECT id, name FROM users WHERE active = true"
python3 scripts/sql_format.py format --input query.sql
python3 scripts/sql_format.py format --input query.sql --output formatted.sql
python3 scripts/sql_format.py format --input query.sql --indent 4 --lowercase
echo "SELECT * FROM t" | python3 scripts/sql_format.py format --input -
```

Adds line breaks before major clauses (SELECT, FROM, WHERE, JOIN, ORDER BY, etc.), indents AND/OR/ON, and uppercases keywords by default.

### Minify SQL

```bash
python3 scripts/sql_format.py minify --sql "SELECT  id,  name  FROM  users  -- comment"
python3 scripts/sql_format.py minify --input query.sql
```

Strips comments, collapses whitespace, removes unnecessary spaces around parentheses and commas.

### Lint SQL

```bash
python3 scripts/sql_format.py lint --input query.sql
python3 scripts/sql_format.py lint --sql "SELECT * FROM users WHERE 1=1" --json
```

Checks for: SELECT *, multiple spaces, tabs, != vs <>, double commas, WHERE 1=1, long lines (>120 chars), trailing whitespace, missing semicolons, inconsistent keyword casing.

## Supported SQL

Handles SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, DROP, WITH (CTEs), JOINs (all types), subqueries, string literals, double-quoted identifiers, single-line and multi-line comments.
