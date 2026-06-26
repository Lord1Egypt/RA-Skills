-- ============================================================
-- missing-indexes.sql
-- Queries SQL Server's missing index DMVs to find indexes that
-- would most improve query performance, with generated CREATE INDEX statements.
-- Requires: VIEW SERVER STATE permission
-- Target:   SQL Server 2016+
-- Usage:    sqlcmd -S <server> -U <user> -P <pass> -d <dbname> -i missing-indexes.sql
-- NOTE:     Run in the context of the database you want to analyze.
--           Stats reset on SQL Server service restart.
-- ============================================================

SELECT TOP 20
    -- Impact score = estimated % improvement × number of times the index would have helped
    -- Higher = more important. Not a perfect metric — use as a ranking guide.
    ROUND(
        migs.avg_user_impact * (migs.user_seeks + migs.user_scans),
        0
    )                                                           AS impact_score,

    -- Estimated average improvement if this index existed (0-100%)
    migs.avg_user_impact                                        AS estimated_improvement_pct,

    -- How many times a query needed an index seek that this index would satisfy
    migs.user_seeks,

    -- How many times a query did a scan that this index would reduce
    migs.user_scans,

    -- Database and table
    DB_NAME(mid.database_id)                                   AS database_name,
    mid.statement                                               AS table_name,

    -- Columns used in equality predicates (WHERE col = value)
    -- These become the leading key columns of the index
    mid.equality_columns,

    -- Columns used in inequality/range predicates (WHERE col > value, BETWEEN, etc.)
    -- These follow equality columns in the index key
    mid.inequality_columns,

    -- Columns that should be INCLUDEd (appear in SELECT but not WHERE)
    -- Adding these eliminates key lookups to the clustered index
    mid.included_columns,

    -- Generated CREATE INDEX statement — review and adjust name/columns before running
    -- IMPORTANT: Consolidate with similar existing indexes before creating new ones
    'CREATE NONCLUSTERED INDEX [IX_' +
        REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
            OBJECT_NAME(mid.object_id) + '_' +
            ISNULL(mid.equality_columns, '') +
            ISNULL(mid.inequality_columns, ''),
            '[', ''), ']', ''), ', ', '_'), ' ', '_'), '__', '_')
        + '] ON ' + mid.statement
        + ' ('
        + ISNULL(mid.equality_columns, '')
        + CASE
            WHEN mid.inequality_columns IS NOT NULL
                THEN CASE WHEN mid.equality_columns IS NOT NULL THEN ', ' ELSE '' END
                     + mid.inequality_columns
            ELSE ''
          END
        + ')'
        + CASE
            WHEN mid.included_columns IS NOT NULL
                THEN ' INCLUDE (' + mid.included_columns + ')'
            ELSE ''
          END
        + ' WITH (ONLINE = ON);'                               AS suggested_create_index

FROM sys.dm_db_missing_index_details mid
JOIN sys.dm_db_missing_index_groups mig
    ON mid.index_handle = mig.index_handle
JOIN sys.dm_db_missing_index_group_stats migs
    ON mig.index_group_handle = migs.group_handle

-- Filter to current database only
WHERE mid.database_id = DB_ID()

ORDER BY impact_score DESC;

-- ============================================================
-- BEFORE CREATING ANY SUGGESTED INDEX:
-- 1. Check if a similar index already exists (sys.indexes)
-- 2. Consolidate: if two suggestions share the same leading columns,
--    create ONE index that covers both (add more INCLUDEs)
-- 3. Confirm with sqlserver-indexes/SKILL.md column ordering rules:
--    equality columns → inequality columns → INCLUDE columns
-- 4. Test with SET STATISTICS IO ON before/after to measure logical reads reduction
-- 5. Monitor sys.dm_db_index_usage_stats after 1-2 weeks — confirm index is used
-- ============================================================
