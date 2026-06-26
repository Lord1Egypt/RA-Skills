# SQL Server Plan Operators Reference

Full reference for execution plan operators — what they are, when they appear, their cost profile, and how to fix them.

---

## Data Access Operators

| Operator | Cost | When It Appears | Fix |
|----------|------|----------------|-----|
| **Table Scan** | 🔴 Very High | No usable index; heap table; small table (OK) | Add a non-clustered index with predicate columns as key |
| **Clustered Index Scan** | 🔴 High | Reading most/all rows; no selective predicate | Add a non-clustered index; check for non-SARGable predicates |
| **Clustered Index Seek** | 🟢 Low | Seeking rows by clustered index key | Ideal — no action needed |
| **Non-Clustered Index Seek** | 🟢 Low | Seeking rows by non-clustered index key | Ideal — no action needed |
| **Non-Clustered Index Scan** | 🟡 Medium | Scanning all or most of a non-clustered index | May indicate missing predicate or wrong index; check query WHERE clause |
| **Key Lookup** | 🟡 Medium (per row) | Non-clustered index seek + fetch from clustered index for non-covered columns | Add INCLUDE columns to the non-clustered index to cover SELECT list |
| **RID Lookup** | 🟡 Medium (per row) | Same as Key Lookup but on a heap (no clustered index) | Add a clustered index to the table |

---

## Join Operators

| Operator | Cost | When It Appears | Fix |
|----------|------|----------------|-----|
| **Nested Loops** | 🟢 Low (small inputs) | Outer set is small; inner set has a seek available | Good for small/selective joins; bad if outer set is large |
| **Merge Join** | 🟢 Low (sorted inputs) | Both inputs are sorted on the join key | Efficient; may indicate sorted index scan |
| **Hash Match (Join)** | 🟡 Medium–High | Large unsorted inputs; no useful index for join | Add index on join column; if memory spills occur, reduce row count or add index |

**When each join type is appropriate:**
- **Nested Loops** — Best when one side is small (< few thousand rows) and the other has an efficient seek.
- **Merge Join** — Best when both sides are large and already sorted (e.g., both have indexes on the join key).
- **Hash Match** — Last resort for large, unsorted datasets. Fine for analytics; bad for OLTP if it spills.

---

## Aggregation Operators

| Operator | Cost | When It Appears | Fix |
|----------|------|----------------|-----|
| **Stream Aggregate** | 🟢 Low | Input is sorted on GROUP BY keys | Good — efficient single-pass aggregation |
| **Hash Match (Aggregate)** | 🟡 Medium | Input is not sorted; GROUP BY on large unsorted set | Add index sorted on GROUP BY columns; watch for memory spills |

---

## Sort and Filter Operators

| Operator | Cost | When It Appears | Fix |
|----------|------|----------------|-----|
| **Sort** | 🟡 Medium–High | ORDER BY, GROUP BY, or join requiring sorted input; no supporting index | Add index matching the ORDER BY column order; or INCLUDE in sorted index |
| **Filter** | 🟡 Low–Medium | WHERE clause applied after a scan/seek | Usually indicates residual predicate after index access; check for non-SARGable conditions |
| **Top** | 🟢 Low | TOP N clause | Normal; ensure ORDER BY is satisfied by an index |

---

## Parallelism Operators (Exchange)

| Operator | Cost | When It Appears | Fix |
|----------|------|----------------|-----|
| **Distribute Streams** | ℹ️ Variable | Splits a single stream into parallel streams | Normal for parallel queries; high CXPACKET waits = thread skew |
| **Gather Streams** | ℹ️ Variable | Combines parallel streams back to single | Normal; appears at the top of parallel plans |
| **Repartition Streams** | 🟡 Medium | Re-distributes parallel streams mid-plan | Can indicate hash distribution overhead in complex parallel plans |

**CXPACKET wait + parallelism operators:**  
Threads are waiting for the slowest thread to catch up. Often caused by data skew (one partition has way more rows). Use `OPTION (MAXDOP 1)` to test if serial plan is faster.

---

## DML Operators

| Operator | Cost | When It Appears | Fix |
|----------|------|----------------|-----|
| **Clustered Index Insert** | ℹ️ Normal | INSERT into table with clustered index | Fragmentation if key is not sequential (e.g., GUID); use IDENTITY or SEQUENCE |
| **Clustered Index Update** | ℹ️ Normal | UPDATE on clustered index key | Avoid updating clustered index key columns (causes row moves) |
| **Clustered Index Delete** | ℹ️ Normal | DELETE on clustered index | Normal |
| **Table Spool** | 🟡 Medium | Intermediate result stored in TempDB; Halloween protection | Usually auto-optimized; high cost = TempDB pressure |
| **Row Count Spool** | 🟡 Medium | Optimization for EXISTS/NOT EXISTS | Generally fine |
| **Index Spool** | 🟡 Medium | Temporary index built during query execution | Missing index — SQL Server is creating one on-the-fly every execution |

**Index Spool is a red flag:** SQL Server decided it was worth building a temporary index just for this query. That's an automatic signal to add a real index.

---

## Spill Warnings

Any operator with a **yellow warning triangle** and "Spilled to TempDB" is a critical finding:

- **Sort spill** — Sort operator ran out of memory grant; spilled intermediate data to disk via TempDB
- **Hash Match spill** — Hash table didn't fit in memory grant; multiple TempDB passes required

**Spill fix process:**
1. Check the estimated vs actual rows entering the operator — large discrepancy = stale stats
2. Run `UPDATE STATISTICS tablename WITH FULLSCAN`
3. If estimates are accurate but grants are too small, query is legitimately large — optimize to reduce row counts or add indexes

---

## Reading the Plan in SSMS

- **Arrow thickness** — proportional to estimated rows flowing between operators
- **Arrow width discrepancy** — if the arrow from the operator is much wider than expected, estimates are off
- **Operator cost %** — percentage of total query cost; focus optimization on highest cost operators first
- **Tooltip** — hover any operator for: Estimated Rows, Actual Rows, Estimated CPU, Estimated I/O, Output list

**Graphical plan reads right-to-left, bottom-to-top.** The rightmost, bottom-most operators are executed first (data sources). Results flow left and up toward the SELECT/INSERT/UPDATE at the top-left.
