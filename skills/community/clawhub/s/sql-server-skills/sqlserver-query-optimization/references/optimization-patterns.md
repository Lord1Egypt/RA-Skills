# SQL Server Query Optimization Patterns

Before/after examples for the most common T-SQL anti-patterns. Each pattern includes the problem, why it's bad, and the corrected version.

---

## Pattern 1: DELETE + INSERT → MERGE

### Problem

```sql
-- ❌ BEFORE: Delete and re-insert every time, even if nothing changed
CREATE PROCEDURE usp_SaveProduct
    @ProductID INT, @Name NVARCHAR(100), @Price DECIMAL(10,2), @CategoryID INT
AS
    DELETE FROM Products WHERE ProductID = @ProductID;
    INSERT INTO Products (ProductID, Name, Price, CategoryID, UpdatedAt)
    VALUES (@ProductID, @Name, @Price, @CategoryID, GETDATE());
GO
```

**Why it's bad:**
- Forces a DELETE log record and an INSERT log record on every call
- If ProductID has a foreign key reference elsewhere, DELETE breaks those references
- Triggers fire on DELETE when nothing meaningful changed
- Auto-increment IDs in related tables may generate unnecessary rows

### Fix: MERGE

```sql
-- ✅ AFTER: MERGE handles insert vs update correctly
CREATE PROCEDURE usp_SaveProduct
    @ProductID INT, @Name NVARCHAR(100), @Price DECIMAL(10,2), @CategoryID INT
AS
    MERGE Products AS target
    USING (VALUES (@ProductID, @Name, @Price, @CategoryID))
          AS source (ProductID, Name, Price, CategoryID)
    ON target.ProductID = source.ProductID
    WHEN MATCHED THEN
        UPDATE SET
            target.Name       = source.Name,
            target.Price      = source.Price,
            target.CategoryID = source.CategoryID,
            target.UpdatedAt  = GETDATE()
    WHEN NOT MATCHED THEN
        INSERT (ProductID, Name, Price, CategoryID, CreatedAt, UpdatedAt)
        VALUES (source.ProductID, source.Name, source.Price, source.CategoryID,
                GETDATE(), GETDATE());
GO
```

---

## Pattern 2: Non-SARGable Date Functions

### Problem

```sql
-- ❌ BEFORE: Function wraps column — forces index scan
SELECT OrderID, CustomerID, TotalAmount
FROM Orders
WHERE YEAR(OrderDate) = 2024 AND MONTH(OrderDate) = 3;
```

**Why it's bad:**  
SQL Server cannot use a range seek on `OrderDate` because the index is on `OrderDate`, not `YEAR(OrderDate)`. Every row in the table is scanned and the function evaluated.

### Fix

```sql
-- ✅ AFTER: Explicit range — allows index seek
SELECT OrderID, CustomerID, TotalAmount
FROM Orders
WHERE OrderDate >= '2024-03-01' AND OrderDate < '2024-04-01';
```

---

## Pattern 3: Non-SARGable Expression on Column

### Problem

```sql
-- ❌ BEFORE: Arithmetic on the column — index unusable
SELECT OrderID, CustomerID, TotalAmount
FROM Orders
WHERE TotalAmount * 1.1 > 5000;

-- ❌ BEFORE: CONVERT wrapping a column
SELECT UserID, UserName
FROM Users
WHERE CONVERT(VARCHAR(10), CreatedDate, 120) = '2024-03-15';
```

### Fix

```sql
-- ✅ AFTER: Move math to the parameter side
SELECT OrderID, CustomerID, TotalAmount
FROM Orders
WHERE TotalAmount > 5000 / 1.1;

-- ✅ AFTER: Use explicit range
SELECT UserID, UserName
FROM Users
WHERE CreatedDate >= '2024-03-15' AND CreatedDate < '2024-03-16';
```

---

## Pattern 4: Implicit Conversion (NVARCHAR vs VARCHAR)

### Problem

```sql
-- Table: Users.Username is NVARCHAR(100)
-- ❌ BEFORE: VARCHAR literal causes implicit conversion on the column
WHERE Username = 'jsmith'
```

**Why it's bad:**  
SQL Server converts every `NVARCHAR` value in the column to `VARCHAR` for comparison. Index is useless — full scan occurs. Visible as `CONVERT_IMPLICIT` in the execution plan.

### Fix

```sql
-- ✅ AFTER: Use N'' prefix for NVARCHAR columns
WHERE Username = N'jsmith'
```

---

## Pattern 5: Cursor → Set-Based

### Problem

```sql
-- ❌ BEFORE: Row-by-row cursor
DECLARE @CustomerID INT, @NewTier VARCHAR(20);
DECLARE cur CURSOR FOR
    SELECT CustomerID FROM Customers WHERE AccountBalance > 10000;
OPEN cur;
FETCH NEXT FROM cur INTO @CustomerID;
WHILE @@FETCH_STATUS = 0
BEGIN
    UPDATE Customers SET Tier = 'Gold' WHERE CustomerID = @CustomerID;
    FETCH NEXT FROM cur INTO @CustomerID;
END
CLOSE cur; DEALLOCATE cur;
```

### Fix

```sql
-- ✅ AFTER: Single set-based UPDATE
UPDATE Customers
SET Tier = 'Gold'
WHERE AccountBalance > 10000;
```

---

## Pattern 6: Cursor Aggregation → Set-Based

### Problem

```sql
-- ❌ BEFORE: Cursor to build running totals
DECLARE @RunningTotal DECIMAL(18,2) = 0;
DECLARE @Amount DECIMAL(18,2), @OrderID INT;
DECLARE @Results TABLE (OrderID INT, RunningTotal DECIMAL(18,2));
DECLARE cur CURSOR FOR SELECT OrderID, TotalAmount FROM Orders ORDER BY OrderDate;
OPEN cur;
FETCH NEXT FROM cur INTO @OrderID, @Amount;
WHILE @@FETCH_STATUS = 0
BEGIN
    SET @RunningTotal = @RunningTotal + @Amount;
    INSERT INTO @Results VALUES (@OrderID, @RunningTotal);
    FETCH NEXT FROM cur INTO @OrderID, @Amount;
END
CLOSE cur; DEALLOCATE cur;
SELECT * FROM @Results;
```

### Fix

```sql
-- ✅ AFTER: Window function
SELECT
    OrderID,
    TotalAmount,
    SUM(TotalAmount) OVER (ORDER BY OrderDate ROWS UNBOUNDED PRECEDING) AS RunningTotal
FROM Orders
ORDER BY OrderDate;
```

---

## Pattern 7: CTE vs Temp Table Decision

### Use CTE When

```sql
-- ✅ CTE: readability, used once, small result
WITH RecentOrders AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY CustomerID ORDER BY OrderDate DESC) AS rn
    FROM Orders
    WHERE OrderDate >= DATEADD(MONTH, -3, GETDATE())
)
SELECT CustomerID, OrderID, OrderDate, TotalAmount
FROM RecentOrders
WHERE rn = 1;  -- Most recent order per customer
```

### Use Temp Table When

```sql
-- ✅ Temp Table: large result, used multiple times, needs an index
SELECT
    CustomerID,
    SUM(TotalAmount)  AS TotalSpent,
    COUNT(*)          AS OrderCount,
    MAX(OrderDate)    AS LastOrderDate
INTO #CustomerStats
FROM Orders
WHERE Status = 'Completed'
GROUP BY CustomerID;

CREATE INDEX IX_Temp_CustomerID ON #CustomerStats (CustomerID);

-- Use it multiple times without re-scanning Orders
SELECT c.*, cs.TotalSpent, cs.OrderCount
FROM Customers c
JOIN #CustomerStats cs ON c.CustomerID = cs.CustomerID
WHERE cs.TotalSpent > 1000;

SELECT AVG(TotalSpent) AS AvgSpend FROM #CustomerStats;

DROP TABLE #CustomerStats;
```

---

## Pattern 8: SELECT * → Explicit Columns

### Problem

```sql
-- ❌ BEFORE
CREATE VIEW vw_OrderSummary AS
    SELECT o.*, c.*
    FROM Orders o JOIN Customers c ON o.CustomerID = c.CustomerID;
```

### Fix

```sql
-- ✅ AFTER
CREATE VIEW vw_OrderSummary AS
    SELECT
        o.OrderID, o.OrderDate, o.TotalAmount, o.Status,
        c.CustomerID, c.CompanyName, c.ContactEmail, c.Region
    FROM Orders o
    JOIN Customers c ON o.CustomerID = c.CustomerID;
```

---

## Pattern 9: LIKE '%value%' — Full-Text Alternative

```sql
-- ❌ Leading wildcard — full index scan, cannot seek
WHERE ProductName LIKE '%widget%'

-- ✅ Option 1: Trailing wildcard only — index seek possible
WHERE ProductName LIKE 'widget%'

-- ✅ Option 2: Full-text search (SQL Server Full-Text feature)
WHERE CONTAINS(ProductName, '"widget"')

-- ✅ Option 3: Computed persisted column for common search patterns
ALTER TABLE Products ADD SearchName AS LOWER(ProductName) PERSISTED;
CREATE INDEX IX_Products_SearchName ON Products (SearchName);
WHERE SearchName LIKE 'widget%'
```

---

## Pattern 10: NOLOCK Anti-Pattern

```sql
-- ❌ Used indiscriminately — can return uncommitted, rolled-back, or duplicate/missing rows
SELECT SUM(TotalAmount) FROM Orders WITH (NOLOCK);  -- Financial total — WRONG

-- ✅ Acceptable: Non-critical dashboard count where minor drift is tolerable
SELECT COUNT(*) FROM AuditLog WITH (NOLOCK);

-- ✅ Better alternative: READ_COMMITTED_SNAPSHOT isolation (RCSI)
-- Enable once per database — eliminates most lock contention without dirty reads:
ALTER DATABASE MyDatabase SET READ_COMMITTED_SNAPSHOT ON;
-- Then use normal queries without NOLOCK hints — readers don't block writers
```

---

## Pattern 11: N+1 Queries in a Loop

```sql
-- ❌ BEFORE: Application calls this proc once per order (N+1 pattern)
CREATE PROCEDURE usp_GetOrderDetails @OrderID INT
AS
    SELECT * FROM Orders WHERE OrderID = @OrderID;
    SELECT * FROM OrderItems WHERE OrderID = @OrderID;
    SELECT * FROM Customers WHERE CustomerID = 
        (SELECT CustomerID FROM Orders WHERE OrderID = @OrderID);
GO

-- ✅ AFTER: Single proc with all data in one call, joined
CREATE PROCEDURE usp_GetOrderDetails @OrderID INT
AS
    SELECT
        o.OrderID, o.OrderDate, o.TotalAmount, o.Status,
        c.CompanyName, c.ContactEmail,
        oi.ProductID, oi.Quantity, oi.UnitPrice, oi.LineTotal
    FROM Orders o
    JOIN Customers c   ON o.CustomerID = c.CustomerID
    JOIN OrderItems oi ON o.OrderID = oi.OrderID
    WHERE o.OrderID = @OrderID;
GO
```

---

## Pattern 12: Unnecessary Scalar UDF in WHERE Clause

```sql
-- ❌ BEFORE: Scalar UDF prevents parallelism and is called row-by-row
WHERE dbo.fn_GetCustomerTier(CustomerID) = 'Gold'

-- ✅ AFTER: Inline table-valued function or inlined logic
WHERE CustomerID IN (
    SELECT CustomerID FROM Customers WHERE Tier = 'Gold'
)

-- Or: Convert scalar UDF to inline TVF (SQL Server 2019+: scalar UDF inlining may help)
-- Check: SELECT * FROM sys.sql_modules WHERE uses_native_compilation = 0 AND ...
```
