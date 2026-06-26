-- ============================================================
-- blocking-analysis.sql
-- Multi-part script to investigate blocking chains, identify head
-- blockers, and inspect lock details.
-- Requires: VIEW SERVER STATE permission
-- Target:   SQL Server 2016+
-- Usage:    sqlcmd -S <server> -U <user> -P <pass> -d master -i blocking-analysis.sql
--
-- ⚠️  NEVER issue KILL commands autonomously. Only kill a session
--     after confirming with the application owner that it is safe
--     to terminate and roll back that session's transaction.
-- ============================================================


-- ============================================================
-- PART 1: Current Blocking Chains
-- Shows all blocked sessions and the session that is blocking them.
-- If blocking_session_id chains — e.g., 55 blocks 60, 60 blocks 70 —
-- the root of the chain (55) is the "head blocker."
-- ============================================================

PRINT '=== PART 1: Blocking Chains ===';

SELECT
    r.session_id                                                AS blocked_session,
    r.blocking_session_id                                       AS blocked_by_session,
    r.wait_type,
    r.wait_time / 1000.0                                        AS waiting_seconds,
    r.total_elapsed_time / 1000.0                               AS total_elapsed_seconds,

    -- The statement the blocked session is trying to run
    SUBSTRING(
        t.text,
        (r.statement_start_offset / 2) + 1,
        ((CASE r.statement_end_offset
            WHEN -1 THEN DATALENGTH(t.text)
            ELSE r.statement_end_offset
          END - r.statement_start_offset) / 2) + 1
    )                                                           AS blocked_statement,

    s.login_name,
    s.host_name,
    s.program_name

FROM sys.dm_exec_requests r
JOIN sys.dm_exec_sessions s
    ON r.session_id = s.session_id
CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) t

WHERE r.blocking_session_id > 0    -- Only blocked sessions

ORDER BY r.wait_time DESC;


-- ============================================================
-- PART 2: Head Blockers
-- The session(s) at the top of the blocking chain — blocking others
-- but NOT themselves blocked. This is where you focus first.
-- ============================================================

PRINT '';
PRINT '=== PART 2: Head Blockers (blocking others but not blocked themselves) ===';

SELECT
    s.session_id,
    s.login_name,
    s.host_name,
    s.program_name,
    s.status,
    s.open_transaction_count,
    s.last_request_start_time,
    DATEDIFF(SECOND, s.last_request_start_time, GETDATE())      AS session_age_seconds,

    -- Number of sessions this head blocker is (directly or indirectly) holding up
    (
        SELECT COUNT(*)
        FROM sys.dm_exec_requests r2
        WHERE r2.blocking_session_id = s.session_id
    )                                                           AS directly_blocking_count,

    -- What the head blocker is running (or last ran — may have committed and be idle)
    LEFT(ISNULL(t.text, '-- Session is idle / between statements'), 1000)
                                                                AS current_or_last_query

FROM sys.dm_exec_sessions s
LEFT JOIN sys.dm_exec_requests r
    ON s.session_id = r.session_id
OUTER APPLY sys.dm_exec_sql_text(
    COALESCE(r.sql_handle, s.sql_handle)
) t

WHERE s.session_id IN (
    -- Sessions that ARE blocking at least one other session
    SELECT DISTINCT blocking_session_id
    FROM sys.dm_exec_requests
    WHERE blocking_session_id > 0
)
AND s.session_id NOT IN (
    -- But are NOT themselves blocked
    SELECT session_id
    FROM sys.dm_exec_requests
    WHERE blocking_session_id > 0
)

ORDER BY session_age_seconds DESC;


-- ============================================================
-- PART 3: Lock Details
-- Shows what locks are held and what is being waited on.
-- Useful for understanding lock types (shared, exclusive, intent).
-- ============================================================

PRINT '';
PRINT '=== PART 3: Lock Details ===';

SELECT
    tl.request_session_id                                       AS session_id,
    tl.resource_type,           -- TABLE, PAGE, KEY, ROW, DATABASE, etc.
    tl.resource_database_id,
    DB_NAME(tl.resource_database_id)                           AS database_name,
    tl.resource_description,

    -- Lock mode held or requested
    -- S  = Shared (read)     | X  = Exclusive (write)
    -- U  = Update            | IS = Intent Shared
    -- IX = Intent Exclusive  | SIX = Shared + Intent Exclusive
    tl.request_mode             AS lock_mode,

    -- GRANT  = session holds this lock
    -- WAIT   = session is waiting to acquire this lock
    tl.request_status           AS lock_status,

    -- Object being locked (if applicable)
    OBJECT_NAME(
        tl.resource_associated_entity_id,
        tl.resource_database_id
    )                                                           AS locked_object

FROM sys.dm_tran_locks tl
WHERE tl.request_session_id IN (
    -- Only show sessions involved in blocking
    SELECT blocking_session_id FROM sys.dm_exec_requests WHERE blocking_session_id > 0
    UNION
    SELECT session_id FROM sys.dm_exec_requests WHERE blocking_session_id > 0
)
ORDER BY
    tl.request_session_id,
    tl.request_status DESC;   -- Show GRANTs before WAITs


-- ============================================================
-- RESOLUTION GUIDANCE (read-only comments — do not execute):
--
-- Option 1 — Wait it out
--   If the head blocker is a legitimate long-running transaction (batch import,
--   report, migration), the safest choice is to let it finish.
--
-- Option 2 — Application-level fix
--   Identify the application/connection holding the lock and resolve there:
--   close unused connections, commit open transactions, add retry logic.
--
-- Option 3 — KILL (last resort, with business approval)
--   Only after confirming with the application owner that rolling back
--   the blocking session's transaction is safe:
--
--   -- KILL <session_id>;   ← Replace with actual session_id from Part 2
--
--   KILL rolls back all uncommitted work in that session. It is immediate
--   but irreversible. The blocked sessions will then proceed.
--
-- Option 4 — Prevent recurrence
--   - Add indexes to reduce lock duration (queries finish faster = unlock sooner)
--   - Shorten transactions (commit as soon as possible)
--   - Review isolation level (READ_COMMITTED_SNAPSHOT can eliminate many reader blocks)
--   - Enable RCSI: ALTER DATABASE <db> SET READ_COMMITTED_SNAPSHOT ON;
-- ============================================================
