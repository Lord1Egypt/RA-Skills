-- ============================================================
-- unused-indexes.sql
-- Finds non-clustered indexes that are never read but still cost
-- write overhead on every INSERT, UPDATE, and DELETE.
-- These are candidates for removal to improve write performance.
-- Requires: VIEW DATABASE STATE permission
-- Target:   SQL Server 2016+
-- Usage:    sqlcmd -S <server> -U <user> -P <pass> -d <dbname> -i unused-indexes.sql
--
-- ⚠️  IMPORTANT: Usage stats reset when SQL Server restarts.
--     Only use this analysis after the server has been running for
--     a representative period (ideally 30+ days including monthly batch jobs).
-- ============================================================

SELECT
    s.name                                                      AS schema_name,
    o.name                                                      AS table_name,
    i.name                                                      AS index_name,
    i.type_desc                                                 AS index_type,

    -- All three read operations are zero — this index is never helping any query
    ius.user_seeks,     -- Seeks = direct navigation to rows by index key
    ius.user_scans,     -- Scans = partial or full index traversal
    ius.user_lookups,   -- Lookups = index + bookmark lookup to base table

    -- But every write to the table pays a maintenance cost for this index
    -- High user_updates with zero reads = pure overhead
    ius.user_updates    AS write_operations_on_index,

    -- Estimated write cost per day (rough approximation for prioritization)
    -- Higher = more urgently worth dropping
    ius.user_updates    AS total_write_overhead_since_restart,

    -- When the index was last used for any read (NULL = never used since restart)
    ius.last_user_seek,
    ius.last_user_scan,
    ius.last_user_lookup,

    -- Check if this is a unique constraint (drop behavior differs)
    i.is_unique_constraint,
    i.is_unique,

    -- Number of columns in this index key
    (SELECT COUNT(*) FROM sys.index_columns ic
     WHERE ic.object_id = i.object_id AND ic.index_id = i.index_id
       AND ic.is_included_column = 0)                          AS key_column_count,

    -- Safe to copy and un-comment after verifying the index is truly unused:
    '-- DROP INDEX [' + i.name + '] ON [' + s.name + '].[' + o.name + '];'
                                                                AS drop_statement_commented_for_safety

FROM sys.dm_db_index_usage_stats ius
JOIN sys.indexes i
    ON ius.object_id = i.object_id AND ius.index_id = i.index_id
JOIN sys.objects o
    ON i.object_id = o.object_id
JOIN sys.schemas s
    ON o.schema_id = s.schema_id

WHERE ius.database_id = DB_ID()
  AND ius.user_seeks   = 0      -- Never used for a seek
  AND ius.user_scans   = 0      -- Never used for a scan
  AND ius.user_lookups = 0      -- Never used for a lookup
  AND ius.user_updates > 0      -- But has been written to (not zero traffic)
  AND i.type_desc != 'CLUSTERED'        -- Never drop the clustered index this way
  AND i.is_primary_key = 0              -- Never drop primary key indexes
  AND i.is_unique_constraint = 0        -- Be cautious with unique constraints
  AND o.is_ms_shipped = 0               -- Skip system objects

ORDER BY ius.user_updates DESC;   -- Sort by write cost (highest overhead first)

-- ============================================================
-- BEFORE DROPPING ANY INDEX:
--
-- 1. Verify stats aren't stale: Check OBJECT_NAME + SQL Server uptime.
--    SELECT sqlserver_start_time FROM sys.dm_os_sys_info;
--    If uptime is short (< 30 days), these stats may not be representative.
--
-- 2. Check for batch jobs: Some indexes are only used by monthly/quarterly
--    reports. Absence from stats doesn't mean absence of use.
--
-- 3. Check query hints: Some queries may explicitly hint this index:
--    SELECT * FROM sys.sql_modules WHERE definition LIKE '%IX_YourIndexName%'
--
-- 4. Disable before dropping (can re-enable if something breaks):
--    ALTER INDEX [IX_Name] ON [schema].[table] DISABLE;
--    -- Monitor for 1-2 weeks before:
--    DROP INDEX [IX_Name] ON [schema].[table];
--
-- 5. Script the index first (in case you need to recreate it):
--    Use SSMS: right-click index → Script Index As → CREATE To
-- ============================================================
