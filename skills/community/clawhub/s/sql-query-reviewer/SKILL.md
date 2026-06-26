# sql-query-reviewer

## Description
Review SQL queries across any dialect for correctness, performance, and security. Finds N+1 patterns, missing indexes, injection risks, cartesian joins, and implicit type casts. Returns a structured report with severity ratings and optimized rewrites.

## Use when
- "optimize this query"
- "is this SQL safe"
- "why is my query slow"
- "check my SQL"
- "is this injection-safe"
- Any raw SQL query, ORM-generated SQL, or migration file

## Supported dialects
PostgreSQL, MySQL, SQLite, SQL Server (T-SQL), Oracle, BigQuery, Snowflake — and any ANSI SQL.

## Input
Paste the SQL query or queries. Optionally specify:
- Dialect (defaults to generic ANSI SQL)
- Approximate table sizes (helps with index advice)
- Whether this is in a hot path (e.g., called on every request)
- ORM in use (if applicable)

## Output format

```
## SQL Query Review

### Critical (fix before production)
- [Finding] — [why this causes bugs or data loss]
  ✗ Before: [problematic SQL]
  ✓ After:  [corrected SQL]

### Performance (should fix)
- [Finding] — [estimated impact]
  ✗ Before: [slow SQL]
  ✓ After:  [optimized SQL]

### Suggestions (nice to have)
- [Finding] — [explanation]

### What's correct
- [Specific patterns done right]

### Summary
[2–3 sentences: biggest risk, top fix, index recommendations if any]
```

## Review checklist

### Correctness
- `NULL` comparison using `=` instead of `IS NULL`
- `NOT IN` with a subquery that can return NULLs — always false
- `UNION` instead of `UNION ALL` when duplicates are acceptable (unnecessary dedup)
- Wrong join type: `INNER` when `LEFT` needed, or vice versa
- Cartesian join (missing `ON` clause or cross join without intent)
- Aggregate without `GROUP BY` on non-aggregated columns
- Incorrect use of `HAVING` vs `WHERE`
- Date/time arithmetic in wrong timezone

### Security
- String interpolation into query — SQL injection risk
- User-supplied value in `ORDER BY`, `LIMIT`, table/column name
- Missing parameterisation in dynamic SQL
- Overly broad `SELECT *` that exposes sensitive columns
- Missing row-level security filter

### Performance
- `SELECT *` when only specific columns needed (excess data transfer)
- Missing `WHERE` clause on large table scan
- `LIKE '%value%'` — can't use index (leading wildcard)
- Function applied to indexed column in `WHERE` — defeats index
- N+1: query inside a loop that could be a single JOIN
- Missing index on foreign key or frequently filtered column
- Subquery that re-executes per row — use CTE or JOIN instead
- `ORDER BY RAND()` or equivalent — full table scan
- Unbounded result set with no `LIMIT`

### Style
- Inconsistent case (keywords, identifiers)
- Ambiguous column reference without table alias
- Long query with no CTEs to break it into readable steps
- Magic number with no comment explaining it

## Severity definitions
- **Critical:** Correctness bug (wrong results), injection risk, or data loss — fix before production
- **Performance:** Causes slow queries, full scans, or poor scalability — fix before release
- **Suggestion:** Readability, maintainability, or defensive coding improvement

## Self-improvement instructions
After each review, note the most common finding. After 20 reviews, surface the top 3 SQL anti-patterns seen as "Most common SQL issues" at the top of the response.
