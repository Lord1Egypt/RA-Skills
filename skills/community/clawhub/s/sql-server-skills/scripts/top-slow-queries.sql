-- ============================================================
-- top-slow-queries.sql
-- Identifies the top 25 slowest queries since last SQL Server restart.
-- Requires: VIEW SERVER STATE permission
-- Target:   SQL Server 2016+
-- Usage:    sqlcmd -S <server> -U <user> -P <pass> -d master -i top-slow-queries.sql
-- ============================================================

SELECT TOP 25
    -- Average elapsed time (wall clock) per execution in milliseconds
    -- This is the most user-facing metric — how long callers wait
    qs.total_elapsed_time / qs.execution_count / 1000.0          AS avg_elapsed_time_ms,

    -- Total elapsed time across ALL executions since last restart
    -- High total with low avg = frequently-called moderate query (optimize first)
    qs.total_elapsed_time / 1000.0                               AS total_elapsed_time_ms,

    -- How many times this query has run since last restart
    qs.execution_count,

    -- Average number of data pages read from buffer pool (in-memory) per execution
    -- High value = query touches lots of data = missing index candidate
    qs.total_logical_reads / qs.execution_count                  AS avg_logical_reads,

    -- Average CPU time (computation only, excludes waits) per execution in ms
    -- If avg_cpu_ms ≈ avg_elapsed_ms → CPU-bound query
    -- If avg_cpu_ms << avg_elapsed_ms → waiting on I/O, locks, etc.
    qs.total_worker_time / qs.execution_count / 1000.0           AS avg_cpu_time_ms,

    -- Total logical reads across ALL executions — useful for total I/O cost ranking
    qs.total_logical_reads                                       AS total_logical_reads,

    -- Total CPU time across ALL executions in milliseconds
    qs.total_worker_time / 1000.0                                AS total_cpu_time_ms,

    -- Database that owns the plan (derived from query plan context)
    DB_NAME(qt.dbid)                                             AS database_name,

    -- The specific statement within the batch that was compiled
    -- (statement_start_offset / statement_end_offset extract just the relevant T-SQL)
    SUBSTRING(
        qt.text,
        (qs.statement_start_offset / 2) + 1,
        ((CASE qs.statement_end_offset
            WHEN -1 THEN DATALENGTH(qt.text)
            ELSE qs.statement_end_offset
          END - qs.statement_start_offset) / 2) + 1
    )                                                            AS query_text,

    -- Hash that groups semantically identical queries with different parameter values
    -- Useful for identifying the same ad-hoc query run with different parameters
    qs.query_hash,

    -- Identifies the compiled plan — use to pull plan XML:
    --   SELECT query_plan FROM sys.dm_exec_query_plan(<plan_handle>)
    qs.plan_handle,

    -- Date/time of last execution — if very old, query may no longer be relevant
    qs.last_execution_time,

    -- Minimum / maximum elapsed times — large spread indicates parameter sniffing
    qs.min_elapsed_time / 1000.0                                 AS min_elapsed_ms,
    qs.max_elapsed_time / 1000.0                                 AS max_elapsed_ms

FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) qt

-- Exclude internal/system queries
WHERE qt.dbid IS NOT NULL
  AND qt.dbid > 4   -- Skip master, msdb, model, tempdb

ORDER BY avg_elapsed_time_ms DESC;

-- ============================================================
-- NEXT STEPS:
-- 1. Focus on queries with high avg_elapsed_time_ms (slow per call)
-- 2. Also check total_elapsed_time_ms × execution_count for total impact
-- 3. For a query with high avg_logical_reads → run scripts/missing-indexes.sql
-- 4. To get the execution plan for a specific query:
--    SELECT query_plan FROM sys.dm_exec_query_plan(0x<plan_handle_value>)
-- ============================================================
