---
name: sqlserver-query-optimization
description: Fix SQL Server stored procedures, views, and T-SQL anti-patterns. Covers non-SARGable predicates, implicit conversions, cursor replacement, DELETE+INSERT anti-pattern, CTE vs temp table decisions, and query hints.
---

# SQL Server Query Optimization

Use this skill when you have a specific stored procedure, view, or T-SQL batch that needs to be rewritten or improved. This is about fixing the code — for hardware/index problems, start with `sqlserver-diagnostics` and `sqlserver-indexes`.

---

## Stored Procedure Anti-Patterns

### 1. DELETE + INSERT Per Request (Most Common)

**Problem:** A stored procedure deletes and re-inserts the same row every time it runs, even when nothing changed.

```sql
-- ❌ ANTI-PATTERN
CREATE PROCEDURE usp_UpsertUserPreference
    @UserID INT, @Key NVARCHAR(50), @Value NVARCHAR(500)
AS
    DELETE FROM UserPreferences WHERE UserID = @UserID AND PreferenceKey = @Key;
    INSERT INTO UserPreferences (UserID, PreferenceKey, PreferenceValue)
    VALUES (@UserID, @Key, @Value);
GO
```

**Problems:**
- Two DML statements = two log writes, two index operations
- Triggers fire on DELETE even when nothing really changed
- Breaks foreign keys that point to this row
- Causes unnecessary index fragmentation

**Fix — MERGE:**

```sql
-- ✅ CORRECT — MERGE (upsert)
CREATE PROCEDURE usp_UpsertUserPreference
    @UserID INT, @Key NVARCHAR(50), @Value NVARCHAR(500)
AS
    MERGE UserPreferences AS target
    USING (VALUES (@UserID, @Key, @Value)) AS source (UserID, PreferenceKey, PreferenceValue)
        ON target.UserID = source.UserID AND target.PreferenceKey = source.PreferenceKey
    WHEN MATCHED AND target.PreferenceValue != source.PreferenceValue THEN
        UPDATE SET target.PreferenceValue = source.PreferenceValue, 
                   target.UpdatedAt = GETDATE()
    WHEN NOT MATCHED THEN
        INSERT (UserID, PreferenceKey, PreferenceValue, CreatedAt)
        VALUES (source.UserID, source.PreferenceKey, source.PreferenceValue, GETDATE());
GO
```

**Alternative — staleness check:**

```sql
-- ✅ CORRECT — Only update if value actually changed
IF EXISTS (SELECT 1 FROM UserPreferences WHERE UserID = @UserID AND PreferenceKey = @Key)
BEGIN
    UPDATE UserPreferences 
    SET PreferenceValue = @Value, UpdatedAt = GETDATE()
    WHERE UserID = @UserID AND PreferenceKey = @Key
      AND PreferenceValue != @Value;  -- Skip if no change
END
ELSE
BEGIN
    INSERT INTO UserPreferences (UserID, PreferenceKey, PreferenceValue, CreatedAt)
    VALUES (@UserID, @Key, @Value, GETDATE());
END
```

---

### 2. Cursor Loops (Replace with Set-Based Operations)

```sql
-- ❌ ANTI-PATTERN — processing rows one at a time
DECLARE @OrderID INT;
DECLARE cur CURSOR FOR SELECT OrderID FROM Orders WHERE Status = 'Pending';
OPEN cur;
FETCH NEXT FROM cur INTO @OrderID;
WHILE @@FETCH_STATUS = 0
BEGIN
    EXEC usp_ProcessOrder @OrderID;
    FETCH NEXT FROM cur INTO @OrderID;
END
CLOSE cur; DEALLOCATE cur;
```

**Fix — set-based:**

```sql
-- ✅ CORRECT — process all rows at once
UPDATE Orders
SET ProcessedAt = GETDATE(), Status = 'Processing'
WHERE Status = 'Pending';
```

If `usp_ProcessOrder` has complex logic that can't be inlined, consider:
- Rewriting the proc to accept a table-valued parameter (TVP)
- Using a temp table as a queue and processing via a single bulk statement
- Using `STRING_AGG` / `FOR XML PATH` for string concatenation (not cursors)

---

### 3. Non-SARGable Predicates

A **SARGable** predicate (Search ARGument able) allows SQL Server to use an index seek. Non-SARGable predicates force scans.

```sql
-- ❌ NON-SARGable — function wraps the column, index can't be used
WHERE YEAR(OrderDate) = 2024
WHERE CONVERT(VARCHAR, OrderDate, 101) = '01/15/2024'
WHERE LEN(CustomerName) > 10
WHERE OrderTotal + 100 > 5000

-- ✅ SARGable equivalents
WHERE OrderDate >= '2024-01-01' AND OrderDate < '2025-01-01'
WHERE OrderDate = '2024-01-15'
WHERE CustomerName LIKE 'A%'          -- LIKE with suffix wildcard is SARGable
WHERE OrderTotal > 4900

-- ❌ NON-SARGable — leading wildcard, can't use index
WHERE CustomerName LIKE '%Smith%'

-- ✅ If full-text search needed, use SQL Server Full-Text or a search table
```

---

### 4. Implicit Conversions

When a column and a parameter have different data types, SQL Server converts the entire column — forcing an index scan.

```sql
-- Table column: CustomerCode NVARCHAR(20)
-- ❌ Passing VARCHAR causes implicit conversion of the whole column
WHERE CustomerCode = 'ACME123'     -- VARCHAR literal, column is NVARCHAR

-- ✅ Use N'' prefix for NVARCHAR columns
WHERE CustomerCode = N'ACME123'

-- Table column: Status TINYINT
-- ❌ Passing string causes type conversion
WHERE Status = '1'

-- ✅ Pass the correct type
WHERE Status = 1
```

**Detect implicit conversions in execution plans:**
- Look for a `CONVERT_IMPLICIT` function in the predicate tooltip
- Or query: `sys.dm_exec_query_stats` + `sys.dm_exec_sql_text` and filter on `CONVERT_IMPLICIT`

---

### 5. SELECT * in Production Code

```sql
-- ❌ Never use SELECT * in stored procedures or views
SELECT * FROM Orders JOIN Customers ON Orders.CustomerID = Customers.CustomerID;

-- ✅ Always name columns explicitly
SELECT 
    o.OrderID, o.OrderDate, o.TotalAmount, o.Status,
    c.CompanyName, c.ContactEmail
FROM Orders o
JOIN Customers c ON o.CustomerID = c.CustomerID;
```

**Why it matters:**
- Breaks if a column is added, renamed, or reordered in the base table
- Fetches columns the application doesn't need (extra I/O, network)
- Prevents SQL Server from using covering index optimization

---

## View Optimization

### When Views Expand Inline

By default, SQL Server expands a view definition inline during query compilation. The optimizer sees the full base table query — this is usually fine.

```sql
-- This view is expanded inline — optimizer sees the base tables
CREATE VIEW vw_ActiveOrders AS
    SELECT o.*, c.CompanyName
    FROM Orders o JOIN Customers c ON o.CustomerID = c.CustomerID
    WHERE o.Status = 'Active';
```

### Indexed Views (Materialized)

An indexed view stores the result set physically. Dramatically speeds up aggregation queries.

```sql
-- Requirements for indexed views:
-- 1. SCHEMABINDING
-- 2. UNIQUE CLUSTERED INDEX on the view
-- 3. Strict SET options (ANSI_NULLS ON, QUOTED_IDENTIFIER ON, etc.)
CREATE VIEW vw_SalesByRegion
WITH SCHEMABINDING AS
    SELECT RegionID, COUNT_BIG(*) AS OrderCount, SUM(TotalAmount) AS TotalSales
    FROM dbo.Orders
    GROUP BY RegionID;
GO

CREATE UNIQUE CLUSTERED INDEX IX_vw_SalesByRegion ON vw_SalesByRegion (RegionID);
```

**On Enterprise Edition**, SQL Server automatically uses the indexed view even when the query references the base table. On Standard Edition, use `WITH (NOEXPAND)` hint:

```sql
SELECT * FROM vw_SalesByRegion WITH (NOEXPAND) WHERE RegionID = 5;
```

---

## CTE vs Temp Table vs Table Variable

| Scenario | Use | Why |
|----------|-----|-----|
| Readability / recursive queries / used once | **CTE** | Inline, no physical storage, optimizer sees through it |
| Large result set used multiple times in same batch | **Temp Table** | Has statistics, can be indexed, persists for the session |
| Small result set (< few hundred rows) | **Table Variable** | Low overhead; no statistics (can be a problem if used in joins) |
| Need an index on intermediate results | **Temp Table** | Table variables can only have a PK constraint |
| Need statistics for optimizer accuracy | **Temp Table** | Table variables have no statistics — optimizer assumes 1 row |

```sql
-- CTE (single-use, readability)
WITH RankedOrders AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY CustomerID ORDER BY OrderDate DESC) AS rn
    FROM Orders
)
SELECT * FROM RankedOrders WHERE rn = 1;

-- Temp Table (multiple uses, large set)
SELECT OrderID, CustomerID, TotalAmount
INTO #LargeOrderSet
FROM Orders
WHERE TotalAmount > 10000;

CREATE INDEX IX_Temp_CustomerID ON #LargeOrderSet (CustomerID);  -- Can add index!

SELECT o.*, c.CompanyName FROM #LargeOrderSet o
JOIN Customers c ON o.CustomerID = c.CustomerID;

DROP TABLE #LargeOrderSet;

-- Table Variable (small set)
DECLARE @SmallSet TABLE (OrderID INT, CustomerID INT);
INSERT INTO @SmallSet SELECT TOP 10 OrderID, CustomerID FROM Orders;
```

---

## Statistics Management

```sql
-- Update statistics for a specific table (full scan = accurate, slower)
UPDATE STATISTICS dbo.Orders WITH FULLSCAN;

-- Update all statistics in the current database
EXEC sp_updatestats;

-- Check if auto-update statistics is enabled (should be ON)
SELECT name, is_auto_update_stats_on, is_auto_create_stats_on
FROM sys.databases
WHERE name = DB_NAME();

-- Check statistics for a specific table
DBCC SHOW_STATISTICS ('dbo.Orders', 'IX_Orders_CustomerID');
```

**When to run manually:**
- After a large bulk load (auto-update threshold is 20% of rows modified — can lag on large tables)
- After index creation (statistics are created automatically but may not be full scan)
- When execution plans look wrong (row estimates far off from actuals)

---

## Query Hints — When Justified

Query hints override optimizer decisions. Use sparingly — they lock in a behavior regardless of data changes.

```sql
-- NOLOCK — dirty reads (accepts uncommitted data). Use for reporting only; NEVER for financial/transactional data
SELECT * FROM Orders WITH (NOLOCK) WHERE CustomerID = 42;

-- OPTION (RECOMPILE) — recompile this statement every execution; solves parameter sniffing
SELECT * FROM Orders WHERE CustomerID = @CustomerID OPTION (RECOMPILE);

-- OPTION (OPTIMIZE FOR UNKNOWN) — use average statistics, not sniffed parameter value
SELECT * FROM Orders WHERE CustomerID = @CustomerID OPTION (OPTIMIZE FOR (@CustomerID UNKNOWN));

-- MAXDOP — limit parallelism for this query
SELECT SUM(TotalAmount) FROM Orders OPTION (MAXDOP 2);

-- FORCE ORDER — force join order as written (rarely needed; usually means missing statistics)
SELECT * FROM Orders o JOIN Customers c ON o.CustomerID = c.CustomerID OPTION (FORCE ORDER);
```

---

## Reference

- [Optimization Patterns Reference](references/optimization-patterns.md) — Before/after SQL examples for all major anti-patterns
