---
name: sqlserver-execution-plans
description: Capture and interpret SQL Server execution plans. Identify bad operators (table scans, key lookups, hash spills), diagnose parameter sniffing, and act on row estimate discrepancies.
---

# SQL Server Execution Plans

Execution plans show exactly how SQL Server will execute (or did execute) a query. Reading them is the fastest way to diagnose why a query is slow.

---

## Capturing Plans

### Method 1: Statistics IO + Time (lightweight, always available)

```sql
SET STATISTICS IO ON;
SET STATISTICS TIME ON;
GO

-- Your query here
SELECT * FROM Orders WHERE CustomerID = 42;
GO

SET STATISTICS IO OFF;
SET STATISTICS TIME OFF;
```

**Output interpretation:**
```
Table 'Orders'. Scan count 1, logical reads 1247, physical reads 0, ...
SQL Server Execution Times: CPU time = 312 ms, elapsed time = 445 ms.
```
- **logical reads** — pages read from buffer pool (in-memory). High = too much data touched.
- **physical reads** — pages read from disk (not in buffer). High = buffer pool cold or too small.
- **CPU time** — pure computation. High = complex calculations or large in-memory sort.
- **elapsed time** — wall clock. Always >= CPU time. Gap = waiting (I/O, locks, etc.)

---

### Method 2: XML Execution Plan (estimated)

```sql
-- Estimated plan — does NOT execute the query
SET SHOWPLAN_XML ON;
GO
SELECT * FROM Orders WHERE CustomerID = 42;
GO
SET SHOWPLAN_XML OFF;
```

---

### Method 3: Actual Execution Plan

```sql
-- Actual plan — executes the query and captures real row counts
SET STATISTICS XML ON;
GO
SELECT * FROM Orders WHERE CustomerID = 42;
GO
SET STATISTICS XML OFF;
```

The XML result contains the full plan. Paste it into SSMS or [SentryOne Plan Explorer](https://www.sentryone.com/plan-explorer) for visual rendering.

---

### Method 4: Pull Plan from Cache

```sql
-- Find a cached plan by query text substring
SELECT TOP 5
    qs.execution_count,
    qs.total_elapsed_time / qs.execution_count / 1000.0 AS avg_elapsed_ms,
    qs.total_logical_reads / qs.execution_count          AS avg_logical_reads,
    SUBSTRING(qt.text, (qs.statement_start_offset/2)+1,
        ((CASE qs.statement_end_offset WHEN -1 THEN DATALENGTH(qt.text)
          ELSE qs.statement_end_offset END - qs.statement_start_offset)/2)+1) AS query_text,
    qp.query_plan
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle)    qt
CROSS APPLY sys.dm_exec_query_plan(qs.plan_handle) qp
WHERE qt.text LIKE '%Orders%'   -- adjust filter
ORDER BY avg_elapsed_ms DESC;
```

Click the `query_plan` result to open the graphical plan in SSMS.

---

## Key Operators — What to Look For

See `references/plan-operators.md` for the full reference table.

### 🔴 Bad: Table Scan

```
Operator: Table Scan (or Clustered Index Scan on large table)
Cost: HIGH — reads every row in the table
Fix: Add a non-clustered index with appropriate key columns
```

A table scan is acceptable only on small tables (< ~1000 rows). On large tables, it's almost always a missing index.

---

### 🔴 Bad: Key Lookup (Bookmark Lookup)

```
Operator: Key Lookup
Cost: MEDIUM–HIGH per row — two B-tree traversals per row
Fix: Add INCLUDE columns to the non-clustered index to cover the SELECT list
```

```sql
-- You have: CREATE INDEX IX_Orders_CustomerID ON Orders (CustomerID)
-- Query needs: CustomerID (seek), OrderDate, Status, TotalAmount (lookup to clustered)
-- Fix:
CREATE INDEX IX_Orders_CustomerID ON Orders (CustomerID)
INCLUDE (OrderDate, Status, TotalAmount);
```

---

### 🟡 Warning: Index Scan (non-clustered, large table)

```
Operator: Index Scan
Cost: MEDIUM — reads all or a large portion of the index leaf level
Fix: Check if a predicate is non-SARGable; verify index column order
```

---

### 🟡 Warning: Hash Match (with memory spill warning)

```
Operator: Hash Match (Join or Aggregate)
Symptom: Spill to TempDB warning icon, high memory grant
Fix: Add index to eliminate hashing; reduce row counts entering the join
```

Hash Match joins are not inherently bad — they're appropriate for large un-indexed joins. The problem is **memory spills**: when the hash table doesn't fit in the granted memory, SQL Server spills to TempDB — catastrophic for performance.

---

### 🟡 Warning: Sort (large, or causing spill)

```
Operator: Sort
Symptom: High cost percentage; spill warning
Fix: Add an index whose key order matches the ORDER BY to eliminate the sort
```

---

### 🟢 Good: Index Seek

```
Operator: Index Seek
Cost: LOW — navigates directly to relevant rows
```

This is what you want. The optimizer used the index B-tree to find exactly the rows needed.

---

### ℹ️ Parallelism (Exchange Operators)

```
Operators: Distribute Streams, Gather Streams, Repartition Streams
Context: Query is executing in parallel
Related wait: CXPACKET, CXCONSUMER
```

Parallelism is not inherently bad. Issues arise when:
- One thread finishes early and waits for others (CXPACKET skew)
- Query is too small to justify parallelism overhead
- `MAXDOP` is too high for the workload

```sql
-- Force single-threaded execution for testing
SELECT * FROM Orders WHERE CustomerID = 42
OPTION (MAXDOP 1);
```

---

## Row Estimate vs Actual Rows

One of the most important things to check: does SQL Server's estimate match reality?

**In SSMS:** Hover over any operator — "Estimated Number of Rows" vs "Actual Number of Rows"

| Discrepancy | Meaning | Fix |
|-------------|---------|-----|
| Estimate = 1, Actual = 50,000 | Severely underestimated — bad plan (wrong join strategy, missing index) | Update statistics, check for parameter sniffing |
| Estimate = 50,000, Actual = 1 | Overestimated — wasteful grants, parallel plan where serial is better | Update statistics |
| Within 2-3x | Acceptable | — |

**Update statistics:**

```sql
-- Update all statistics on a table
UPDATE STATISTICS dbo.Orders WITH FULLSCAN;

-- Update all statistics in the database
EXEC sp_updatestats;

-- Check statistics age
SELECT
    OBJECT_NAME(s.object_id) AS table_name,
    s.name                   AS stat_name,
    sp.last_updated,
    sp.rows,
    sp.rows_sampled,
    sp.modification_counter
FROM sys.stats s
CROSS APPLY sys.dm_db_stats_properties(s.object_id, s.stats_id) sp
WHERE OBJECT_NAME(s.object_id) = 'Orders'
ORDER BY sp.modification_counter DESC;
```

---

## Parameter Sniffing

SQL Server compiles a stored procedure's plan on first execution using the parameter values at that time. If those values aren't representative, all subsequent executions use a bad plan.

**Symptom:** A stored procedure is fast when run directly but slow when called from the application (or vice versa).

**Diagnose:**

```sql
-- Check the cached plan and parameters it was compiled for
SELECT
    qs.execution_count,
    qs.total_elapsed_time / qs.execution_count / 1000.0 AS avg_elapsed_ms,
    qp.query_plan
FROM sys.dm_exec_procedure_stats ps
CROSS APPLY sys.dm_exec_query_plan(ps.plan_handle) qp
JOIN sys.dm_exec_query_stats qs ON ps.plan_handle = qs.plan_handle
WHERE OBJECT_NAME(ps.object_id) = 'usp_GetOrders';
-- Look at the plan — was it compiled for a selective or non-selective parameter value?
```

**Fixes (in order of preference):**

```sql
-- Option 1: OPTIMIZE FOR UNKNOWN — use average statistics, not sniffed values
CREATE PROCEDURE usp_GetOrders @CustomerID INT
AS
    SELECT * FROM Orders WHERE CustomerID = @CustomerID
    OPTION (OPTIMIZE FOR (@CustomerID UNKNOWN));
GO

-- Option 2: OPTION (RECOMPILE) — recompile on every execution (CPU cost)
CREATE PROCEDURE usp_GetOrders @CustomerID INT
AS
    SELECT * FROM Orders WHERE CustomerID = @CustomerID
    OPTION (RECOMPILE);
GO

-- Option 3: Local variable (breaks sniffing — not always ideal)
CREATE PROCEDURE usp_GetOrders @CustomerID INT
AS
    DECLARE @LocalCustomerID INT = @CustomerID;
    SELECT * FROM Orders WHERE CustomerID = @LocalCustomerID;
GO

-- Option 4: Clear the procedure cache (nuclear, use carefully in production)
DBCC FREEPROCCACHE;
```

---

## Reference

- [Plan Operators Reference](references/plan-operators.md) — Full operator table with cost, trigger conditions, and fixes
