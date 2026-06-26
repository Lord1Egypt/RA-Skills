-- ============================================================
-- index-fragmentation.sql
-- Checks index fragmentation levels and recommends REBUILD or REORGANIZE.
-- Uses SAMPLED mode for performance on large databases (avoid DETAILED).
-- Requires: VIEW DATABASE STATE permission
-- Target:   SQL Server 2016+
-- Usage:    sqlcmd -S <server> -U <user> -P <pass> -d <dbname> -i index-fragmentation.sql
-- NOTE:     Run while connected to the database you want to check.
--           On large databases, this may take a few minutes.
-- ============================================================

SELECT
    s.name                                                      AS schema_name,
    o.name                                                      AS table_name,
    i.name                                                      AS index_name,
    ips.index_type_desc                                         AS index_type,

    -- Fragmentation percentage: proportion of out-of-order pages in the index
    -- > 30%  → REBUILD  (complete reorganization, updates statistics)
    -- 10-30% → REORGANIZE (online, incremental, does NOT update statistics)
    -- < 10%  → Skip (not worth the overhead)
    ROUND(ips.avg_fragmentation_in_percent, 1)                  AS fragmentation_pct,

    -- Number of pages in the index — only indexes with > 100 pages are worth maintaining
    -- Tiny indexes fragment quickly but the overhead of fixing them exceeds the benefit
    ips.page_count,

    -- Recommended action based on fragmentation thresholds
    CASE
        WHEN ips.avg_fragmentation_in_percent > 30 THEN 'REBUILD'
        WHEN ips.avg_fragmentation_in_percent > 10 THEN 'REORGANIZE'
        ELSE 'SKIP'
    END                                                         AS recommended_action,

    -- Ready-to-run T-SQL maintenance statement
    -- ONLINE = ON keeps the table accessible during rebuild (Enterprise Edition only)
    -- If Standard Edition, remove WITH (ONLINE = ON) — table will be locked during REBUILD
    CASE
        WHEN ips.avg_fragmentation_in_percent > 30 THEN
            'ALTER INDEX [' + i.name + '] ON [' + s.name + '].[' + o.name
            + '] REBUILD WITH (ONLINE = ON, FILLFACTOR = 80);'
        WHEN ips.avg_fragmentation_in_percent > 10 THEN
            'ALTER INDEX [' + i.name + '] ON [' + s.name + '].[' + o.name
            + '] REORGANIZE;'
            + ' -- Then run: UPDATE STATISTICS [' + s.name + '].[' + o.name + '];'
        ELSE '-- No action needed'
    END                                                         AS maintenance_sql

FROM sys.dm_db_index_physical_stats(
    DB_ID(),    -- Current database
    NULL,       -- All tables
    NULL,       -- All indexes
    NULL,       -- All partitions
    'SAMPLED'   -- SAMPLED = fast approximation; DETAILED = accurate but slow
) ips
JOIN sys.indexes i
    ON ips.object_id = i.object_id AND ips.index_id = i.index_id
JOIN sys.objects o
    ON i.object_id = o.object_id
JOIN sys.schemas s
    ON o.schema_id = s.schema_id

WHERE ips.avg_fragmentation_in_percent > 10   -- Only show indexes worth acting on
  AND ips.page_count > 100                    -- Skip tiny indexes (not worth maintaining)
  AND i.name IS NOT NULL                      -- Skip heaps (no index name = heap)
  AND o.is_ms_shipped = 0                     -- Skip system objects

ORDER BY ips.avg_fragmentation_in_percent DESC;

-- ============================================================
-- POST-REORGANIZE: Statistics are NOT updated by REORGANIZE.
-- Run this after a REORGANIZE pass to keep statistics current:
--   UPDATE STATISTICS <schema>.<table>;
--
-- POST-REBUILD: Statistics ARE automatically updated by REBUILD.
--
-- FILL FACTOR = 80 on REBUILD leaves 20% free space on each page,
-- reducing immediate re-fragmentation on tables with frequent inserts.
-- Adjust based on your workload (higher churn = lower fill factor).
-- ============================================================
