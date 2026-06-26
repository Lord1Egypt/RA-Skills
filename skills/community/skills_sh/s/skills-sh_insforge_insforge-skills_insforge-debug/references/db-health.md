# DB health

Postgres system views (`pg_stat_*`, `pg_locks`, `pg_class`) exposed as named checks. The primary primitive for **current database state** — connection pool, query performance, lock contention, storage, index efficacy.

## Command

```bash
npx @insforge/cli diagnose db [--check <checks>]
```

`--check` accepts comma-separated names. Default `all`. Run no-arg first when triaging unknown DB issues.

## Checks

| Check | Underlying view | What it tells you |
|-------|-----------------|-------------------|
| `connections` | `pg_stat_activity` | Active vs idle vs idle-in-transaction count; how close to pool limit |
| `slow-queries` | `pg_stat_statements` | Queries by total/mean exec time; which queries dominate load |
| `bloat` | `pg_class`, `pg_stats` | Table/index dead-row bloat (vacuum lag, write-heavy tables) |
| `size` | `pg_class` size functions | Table and index disk footprint |
| `index-usage` | `pg_stat_user_indexes` | Indexes that are never scanned (unused) vs heavy hitters |
| `locks` | `pg_locks` + `pg_stat_activity` | Lock contention, blocking queries, deadlock candidates |
| `cache-hit` | `pg_statio_*` | Buffer cache hit ratio (low = working set exceeds RAM) |

## How to read

| Reading | Likely problem | Next step |
|---------|---------------|-----------|
| `connections` near pool limit + many idle-in-transaction | Connection leak in client code | Find client missing `release()` or transaction not committing |
| `slow-queries` top entry called frequently | Missing index or bad plan | Check `index-usage` for that table; consider migration |
| `bloat` high on actively-written table | Vacuum not keeping up | Schedule vacuum tighter or rewrite query pattern |
| `index-usage` shows unused indexes | Wasted write cost | Drop unused indexes (after confirming they're truly unused) |
| `locks` with blocker/blocked pairs | Long transactions or deadlocks | Kill blocking PID after investigation, fix the lock-holding query |
| `cache-hit` < 0.99 | Working set exceeds RAM | Tune queries to reduce buffer churn, or scale |

## Boundaries

- **Current snapshot, not history.** `pg_stat_*` resets on Postgres restart; numbers are cumulative since last reset, not a time series.
- **Doesn't show query text inline.** `slow-queries` shows hashed query templates — get the actual SQL from [logs](logs.md) (`postgres.logs`) or `pg_stat_statements.query` directly via `db query`.
- **Doesn't evaluate RLS.** For "which policy is making this query slow," use [policies](policies.md).

## Example

User reports: "this one query is slow — `SELECT * FROM orders WHERE user_id = ... ORDER BY created_at DESC`".

```bash
# 1. Confirm it's in the slow-query log and check index usage on the table
npx @insforge/cli diagnose db --check slow-queries,index-usage

# 2. Verify no lock contention from a concurrent writer
npx @insforge/cli diagnose db --check locks

# 3. Cross-reference postgres.logs for the actual query plan / errors
npx @insforge/cli logs postgres.logs --limit 100
```

## Frequently paired with

- [logs](logs.md) — `postgres.logs` has the query text, plans, and error context behind `slow-queries`/`locks` aggregates
- [policies](policies.md) — when slow queries are RLS-gated, the policy may be adding hidden joins
- [metrics](metrics.md) — DB pressure usually shows as EC2 CPU/memory pressure; cross-reference timestamps
- [advisor](advisor.md) — performance category often pre-flags the same issues `slow-queries` / `index-usage` would surface
