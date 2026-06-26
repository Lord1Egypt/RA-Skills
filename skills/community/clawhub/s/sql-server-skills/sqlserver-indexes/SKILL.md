---
name: sqlserver-indexes
description: SQL Server index management — find missing indexes, analyze fragmentation, identify unused indexes, design covering indexes, and understand index usage stats.
---

# SQL Server Indexes

Indexes are the single biggest lever for SQL Server query performance. This skill covers finding missing indexes, maintaining existing ones, eliminating unused indexes, and designing effective covering indexes.

---

## 1. Missing Indexes

SQL Server tracks index opportunities it identified during query execution in DMVs. These are not perfect recommendations — treat them as leads.

**Script:** `../scripts/missing-indexes.sql`

```sql
-- Top missing indexes by impact score
SELECT TOP 20
    ROUND(migs.avg_user_impact * (migs.user_seeks + migs.user_scans), 0)
                                            AS impact_score,
    DB_NAME(mid.database_id)               AS database_name,
    mid.statement                          AS table_name,
    mid.equality_columns,
    mid.inequality_columns,
    mid.included_columns,
    migs.user_seeks,
    migs.user_scans,
    migs.avg_user_impact,
    'CREATE INDEX [IX_' + OBJECT_NAME(mid.object_id) + '_'
        + REPLACE(REPLACE(REPLACE(
            ISNULL(mid.equality_columns, '') + 
            ISNULL('_' + mid.inequality_columns, ''), 
            '[', ''), ']', ''), ', ', '_')
        + '] ON ' + mid.statement
        + ' (' + ISNULL(mid.equality_columns, '')
        + CASE WHEN mid.inequality_columns IS NOT NULL
               THEN CASE WHEN mid.equality_columns IS NOT NULL 
                         THEN ', ' ELSE '' END + mid.inequality_columns
               ELSE '' END + ')'
        + CASE WHEN mid.included_columns IS NOT NULL
               THEN ' INCLUDE (' + mid.included_columns + ')'
               ELSE '' END                 AS suggested_create_index
FROM sys.dm_db_missing_index_details mid
JOIN sys.dm_db_missing_index_groups mig   ON mid.index_handle = mig.index_handle
JOIN sys.dm_db_missing_index_group_stats migs ON mig.index_group_handle = migs.group_handle
WHERE mid.database_id = DB_ID()
ORDER BY impact_score DESC;
```

**Interpreting results:**
- `impact_score` = `avg_user_impact × (seeks + scans)` — higher is more important
- `equality_columns` → these become the leading key columns
- `inequality_columns` → these follow equality columns in the key (range predicates)
- `included_columns` → INCLUDE these to cover the SELECT list (no key lookup needed)
- **Don't blindly create every suggestion** — consolidate similar indexes first

**Column ordering rule:** Always put equality predicates first, then inequality predicates, then included columns. See `references/index-strategies.md`.

---

## 2. Index Fragmentation

Fragmentation degrades performance by forcing SQL Server to read more pages for the same data. Run this regularly (monthly for most workloads).

**Script:** `../scripts/index-fragmentation.sql`

```sql
SELECT
    s.name                              AS schema_name,
    o.name                              AS table_name,
    i.name                              AS index_name,
    ips.index_type_desc                 AS type_desc,
    ROUND(ips.avg_fragmentation_in_percent, 1) AS fragmentation_pct,
    ips.page_count,
    CASE
        WHEN ips.avg_fragmentation_in_percent > 30  THEN 'REBUILD'
        WHEN ips.avg_fragmentation_in_percent > 10  THEN 'REORGANIZE'
        ELSE 'SKIP'
    END                                 AS recommended_action,
    'ALTER INDEX [' + i.name + '] ON [' + s.name + '].[' + o.name + '] '
        + CASE
            WHEN ips.avg_fragmentation_in_percent > 30 THEN 'REBUILD WITH (ONLINE = ON);'
            ELSE 'REORGANIZE;'
          END                           AS maintenance_statement
FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'SAMPLED') ips
JOIN sys.indexes i   ON ips.object_id = i.object_id AND ips.index_id = i.index_id
JOIN sys.objects o   ON i.object_id = o.object_id
JOIN sys.schemas s   ON o.schema_id = s.schema_id
WHERE ips.avg_fragmentation_in_percent > 10
  AND ips.page_count > 100   -- Ignore tiny indexes (not worth maintaining)
  AND i.name IS NOT NULL
ORDER BY ips.avg_fragmentation_in_percent DESC;
```

**Decision guide:**

| Fragmentation | Action | Why |
|---------------|--------|-----|
| < 10% | Skip | Not worth the overhead |
| 10–30% | `REORGANIZE` | Online, incremental, low overhead |
| > 30% | `REBUILD` | More thorough; use `ONLINE = ON` on Enterprise Edition |

**Notes:**
- `REBUILD` updates statistics automatically; `REORGANIZE` does not (run `UPDATE STATISTICS` separately)
- `ONLINE = ON` requires Enterprise Edition — table stays accessible during rebuild
- Use `SAMPLED` mode (not `DETAILED`) for DMV query — much faster on large tables

---

## 3. Unused Indexes

Indexes that are never read but still incur write overhead on every INSERT/UPDATE/DELETE. These are pure waste.

**Script:** `../scripts/unused-indexes.sql`

```sql
SELECT
    s.name                  AS schema_name,
    o.name                  AS table_name,
    i.name                  AS index_name,
    i.type_desc,
    ius.user_seeks,
    ius.user_scans,
    ius.user_lookups,
    ius.user_updates,       -- Write cost — every DML pays this price
    ius.last_user_seek,
    ius.last_user_scan,
    ius.last_user_lookup,
    -- Commented out for safety — review before executing
    '-- DROP INDEX [' + i.name + '] ON [' + s.name + '].[' + o.name + '];'
                            AS drop_statement
FROM sys.dm_db_index_usage_stats ius
JOIN sys.indexes i  ON ius.object_id = i.object_id AND ius.index_id = i.index_id
JOIN sys.objects o  ON i.object_id = o.object_id
JOIN sys.schemas s  ON o.schema_id = s.schema_id
WHERE ius.database_id = DB_ID()
  AND ius.user_seeks   = 0
  AND ius.user_scans   = 0
  AND ius.user_lookups = 0
  AND ius.user_updates > 0
  AND i.type_desc != 'CLUSTERED'   -- Never drop the clustered index this way
  AND o.is_ms_shipped = 0
ORDER BY ius.user_updates DESC;
```

⚠️ **Important caveats:**
- Usage stats **reset on SQL Server service restart** — don't use this query after a recent restart
- An index may be used by infrequent batch jobs — verify against monthly patterns before dropping
- Some indexes exist for constraint enforcement (UNIQUE) — check `i.is_unique_constraint`
- Test dropping in dev/staging first

---

## 4. Index Usage Stats

Understand how an index is actually being used:

```sql
SELECT
    s.name                  AS schema_name,
    o.name                  AS table_name,
    i.name                  AS index_name,
    i.type_desc,
    ius.user_seeks,         -- Index seeks (best — specific rows via key)
    ius.user_scans,         -- Full or range scans (usually worse)
    ius.user_lookups,       -- Key lookups (seek + bookmark lookup — consider covering)
    ius.user_updates,       -- Write overhead
    ius.last_user_seek,
    ius.last_user_scan
FROM sys.dm_db_index_usage_stats ius
JOIN sys.indexes i  ON ius.object_id = i.object_id AND ius.index_id = i.index_id
JOIN sys.objects o  ON i.object_id = o.object_id
JOIN sys.schemas s  ON o.schema_id = s.schema_id
WHERE ius.database_id = DB_ID()
  AND o.is_ms_shipped = 0
ORDER BY ius.user_seeks + ius.user_scans + ius.user_lookups DESC;
```

**Seeks vs Scans vs Lookups:**
- **Seeks** — Best. SQL Server navigated directly to specific rows via the B-tree key.
- **Scans** — SQL Server read the whole index (or a large range). May indicate missing predicate or wrong index.
- **Lookups** — SQL Server found a row in the non-clustered index but had to go back to the clustered index for additional columns. Fix with a covering index.

---

## 5. Covering Indexes

A covering index satisfies a query entirely from the index — no lookup to the base table needed.

**Problem pattern (Key Lookup):**

```sql
-- Table: Orders (OrderID PK, CustomerID, OrderDate, Status, TotalAmount, Notes)
-- Query:
SELECT OrderDate, Status, TotalAmount
FROM Orders
WHERE CustomerID = 42;

-- If you have: CREATE INDEX IX_Orders_CustomerID ON Orders (CustomerID)
-- SQL Server seeks to CustomerID = 42 but then does a KEY LOOKUP for OrderDate, Status, TotalAmount
```

**Fix — covering index:**

```sql
CREATE INDEX IX_Orders_CustomerID_Covering
ON Orders (CustomerID)
INCLUDE (OrderDate, Status, TotalAmount);
-- CustomerID is the key (searchable); OrderDate/Status/TotalAmount are carried along
-- No key lookup needed
```

**Key vs INCLUDE columns:**
- **Key columns** — used in WHERE, JOIN, ORDER BY. Added to the B-tree structure.
- **INCLUDE columns** — only carried in the leaf level. Can be any data type. Not searchable. Used to satisfy SELECT list.

See `references/index-strategies.md` for detailed design patterns.

---

## Reference

- [Index Strategies Reference](references/index-strategies.md) — Composite key ordering, filtered indexes, columnstore, maintenance scheduling
- Scripts: `../scripts/missing-indexes.sql`, `../scripts/index-fragmentation.sql`, `../scripts/unused-indexes.sql`
