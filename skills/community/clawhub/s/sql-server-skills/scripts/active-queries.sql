-- ============================================================
-- active-queries.sql
-- Shows all currently executing queries — their status, wait info,
-- resource consumption, and any blocking relationships.
-- Requires: VIEW SERVER STATE permission
-- Target:   SQL Server 2016+
-- Usage:    sqlcmd -S <server> -U <user> -P <pass> -d master -i active-queries.sql
-- Run this when: a server seems slow RIGHT NOW, to see what's happening live.
-- ============================================================

SELECT
    r.session_id,

    -- Who is running this session
    s.login_name,
    s.host_name,
    s.program_name,

    -- Current status of the request
    -- 'running'   = actively using CPU
    -- 'suspended' = waiting on a resource (see wait_type)
    -- 'runnable'  = ready to run but waiting for a CPU slot
    r.status,

    -- What the request is currently waiting on
    -- NULL = running (not waiting)
    -- PAGEIOLATCH_* = waiting on disk I/O
    -- LCK_M_*       = waiting on a lock (see blocking_session_id)
    r.wait_type,

    -- How long it has been waiting (in milliseconds)
    r.wait_time                                                 AS wait_time_ms,

    -- Resource the session is waiting for (e.g., specific lock, page address)
    r.wait_resource,

    -- CPU consumed by this request so far (milliseconds)
    r.cpu_time                                                  AS cpu_time_ms,

    -- Data pages read from buffer pool (in-memory cache)
    -- Very high value = reading lots of data = missing index candidate
    r.logical_reads,

    -- Data pages written (for DML statements)
    r.writes,

    -- Total wall-clock time since the request started (milliseconds)
    r.total_elapsed_time                                        AS elapsed_time_ms,

    -- If > 0, this session is blocked by another session (that session_id is the blocker)
    -- Use blocking-analysis.sql for full blocking chain investigation
    r.blocking_session_id,

    -- The specific T-SQL statement currently executing within the batch
    SUBSTRING(
        t.text,
        (r.statement_start_offset / 2) + 1,
        ((CASE r.statement_end_offset
            WHEN -1 THEN DATALENGTH(t.text)
            ELSE r.statement_end_offset
          END - r.statement_start_offset) / 2) + 1
    )                                                           AS current_statement,

    -- The full batch/procedure text (for context around current_statement)
    LEFT(t.text, 500)                                           AS batch_text_preview,

    -- Transaction isolation level — NOLOCK (1), RC (2), RR (3), Serializable (4)
    CASE s.transaction_isolation_level
        WHEN 0 THEN 'Unspecified'
        WHEN 1 THEN 'ReadUncommitted (NOLOCK)'
        WHEN 2 THEN 'ReadCommitted'
        WHEN 3 THEN 'RepeatableRead'
        WHEN 4 THEN 'Serializable'
        WHEN 5 THEN 'Snapshot'
    END                                                         AS isolation_level,

    -- Number of open transactions in this session (> 1 = nested transactions)
    s.open_transaction_count,

    r.plan_handle  -- Use with sys.dm_exec_query_plan() to get execution plan

FROM sys.dm_exec_requests r
JOIN sys.dm_exec_sessions s
    ON r.session_id = s.session_id
CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) t

WHERE r.session_id != @@SPID       -- Exclude this query itself
  AND s.is_user_process = 1        -- Exclude system/background sessions
  AND r.status != 'sleeping'       -- Exclude idle connections

ORDER BY r.total_elapsed_time DESC;

-- ============================================================
-- WHAT TO LOOK FOR:
--
-- blocking_session_id > 0  → Run blocking-analysis.sql to trace the chain
-- wait_type = PAGEIOLATCH_* → Heavy I/O; check missing-indexes.sql
-- wait_type = LCK_M_*      → Lock contention; run blocking-analysis.sql
-- elapsed_time_ms very high → Long-running query; get execution plan:
--   SELECT query_plan FROM sys.dm_exec_query_plan(<plan_handle>)
-- open_transaction_count > 1 → Nested transactions; verify they all commit
-- status = 'runnable' many rows → CPU pressure; too many concurrent queries
-- ============================================================
