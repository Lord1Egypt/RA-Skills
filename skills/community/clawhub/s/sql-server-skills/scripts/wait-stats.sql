-- ============================================================
-- wait-stats.sql
-- Shows what SQL Server has been waiting on since last restart.
-- The dominant wait type identifies the category of your performance problem.
-- Requires: VIEW SERVER STATE permission
-- Target:   SQL Server 2016+
-- Usage:    sqlcmd -S <server> -U <user> -P <pass> -d master -i wait-stats.sql
-- ============================================================

-- Calculate total wait time (excluding benign/idle waits) for percentage calculation
;WITH WaitsCTE AS (
    SELECT
        wait_type,
        wait_time_ms,
        signal_wait_time_ms,
        waiting_tasks_count,
        wait_time_ms - signal_wait_time_ms  AS resource_wait_time_ms
    FROM sys.dm_os_wait_stats
    WHERE wait_type NOT IN (
        -- ----------------------------------------------------------------
        -- EXCLUDE: Idle / background / benign wait types
        -- These don't indicate user-facing performance problems
        -- ----------------------------------------------------------------
        'SLEEP_TASK',
        'SLEEP_DBSTARTUP', 'SLEEP_DCOMSTARTUP', 'SLEEP_MASTERDBREADY',
        'SLEEP_MASTERMDREADY', 'SLEEP_MASTERUPGRADED', 'SLEEP_MSDBSTARTUP',
        'SLEEP_SYSTEMTASK', 'SLEEP_TEMPDBSTARTUP',
        'LAZYWRITER_SLEEP',
        'LOGMGR_QUEUE',
        'ONDEMAND_TASK_QUEUE',
        'REQUEST_FOR_DEADLOCK_SEARCH',
        'RESOURCE_QUEUE',
        'SERVER_IDLE_CHECK',
        'SNI_HTTP_ACCEPT',
        'SP_SERVER_DIAGNOSTICS_SLEEP',
        'SQLTRACE_BUFFER_FLUSH',
        'SQLTRACE_INCREMENTAL_FLUSH_SLEEP',
        'SQLTRACE_WAIT_ENTRIES',
        'WAITFOR',
        'XE_DISPATCHER_WAIT',
        'XE_TIMER_EVENT',
        'CHECKPOINT_QUEUE',
        'CLR_AUTO_EVENT', 'CLR_MANUAL_EVENT',
        'DISPATCHER_QUEUE_SEMAPHORE',
        'FT_IFTS_SCHEDULER_IDLE_WAIT',
        -- Broker / Service Broker (background messaging)
        'BROKER_TO_FLUSH', 'BROKER_TASK_STOP', 'BROKER_EVENTHANDLER',
        'BROKER_TRANSMITTER', 'BROKER_IOCP',
        -- Mirroring / Availability Groups (normal AG background activity)
        'DBMIRROR_EVENTS_QUEUE', 'DBMIRROR_WORKER_QUEUE',
        'HADR_WORK_QUEUE', 'HADR_FILESTREAM_IOMGR_IOCOMPLETION',
        -- In-memory OLTP checkpoint
        'WAIT_XTP_OFFLINE_CKPT_NEW_LOG', 'WAIT_XTP_ONLINE_CKPT_NEW_LOG',
        -- Misc background
        'DIRTY_PAGE_POLL', 'DBMIRROR_SEND'
    )
      AND wait_time_ms > 0
)
SELECT TOP 30
    w.wait_type,

    -- Total time SQL Server has spent in this wait state (seconds)
    ROUND(w.wait_time_ms / 1000.0, 1)          AS wait_time_s,

    -- Resource wait = time waiting on the actual resource (disk, lock, memory)
    -- Signal wait = time waiting for a CPU scheduler slot AFTER resource became available
    -- High signal_wait_s relative to wait_time_s = CPU pressure
    ROUND(w.resource_wait_time_ms / 1000.0, 1) AS resource_wait_s,
    ROUND(w.signal_wait_time_ms / 1000.0, 1)   AS signal_wait_s,

    -- Number of tasks that waited
    w.waiting_tasks_count,

    -- Percentage of total (non-benign) wait time — focus on top items
    CAST(
        100.0 * w.wait_time_ms / SUM(w.wait_time_ms) OVER ()
    AS DECIMAL(5, 2))                           AS pct_of_total,

    -- ----------------------------------------------------------------
    -- INTERPRETATION GUIDE (inline)
    -- ----------------------------------------------------------------
    CASE
        -- I/O Bound: data pages being read from physical disk
        WHEN w.wait_type LIKE 'PAGEIOLATCH_%'
            THEN 'I/O BOUND — pages read from disk. Add RAM, faster storage, better indexes.'

        -- Lock waits: blocking between sessions
        WHEN w.wait_type LIKE 'LCK_M_%'
            THEN 'LOCKING — blocked sessions. Run blocking-analysis.sql. Review transaction isolation.'

        -- Parallelism: threads waiting on each other in parallel query
        WHEN w.wait_type IN ('CXPACKET', 'CXCONSUMER')
            THEN 'PARALLELISM — threads waiting on slowest parallel thread. Review MAXDOP setting.'

        -- CPU Pressure: threads yielding CPU (too much CPU work)
        WHEN w.wait_type = 'SOS_SCHEDULER_YIELD'
            THEN 'CPU PRESSURE — threads giving up CPU time. Tune high-CPU queries.'

        -- Transaction log writes are the bottleneck
        WHEN w.wait_type = 'WRITELOG'
            THEN 'LOG I/O — transaction log writes are slow. Move log to faster disk.'

        -- Memory pressure for query execution (sorts, hashes)
        WHEN w.wait_type = 'RESOURCE_SEMAPHORE'
            THEN 'MEMORY GRANT — queries waiting for execution memory. Fix spilling queries; check max server memory.'

        -- Client reading results slowly (app-side issue)
        WHEN w.wait_type = 'ASYNC_NETWORK_IO'
            THEN 'NETWORK/CLIENT — client reading rows slower than SQL Server sends. Reduce result set size.'

        -- TempDB page allocation contention (many sessions creating temp objects)
        WHEN w.wait_type LIKE 'PAGELATCH_%'
            THEN 'PAGE LATCH — in-memory page contention, often TempDB. Add TempDB data files (8 is common).'

        -- Always On Availability Group traffic
        WHEN w.wait_type LIKE 'HADR_%'
            THEN 'AVAILABILITY GROUPS — normal in AG environments. High values = AG latency or secondary lag.'

        -- Memory-optimized / In-Memory OLTP
        WHEN w.wait_type LIKE 'WAIT_XTP%'
            THEN 'IN-MEMORY OLTP (XTP) — checkpoint or log activity.'

        ELSE 'See: https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/sys-dm-os-wait-stats-transact-sql'
    END                                         AS interpretation

FROM WaitsCTE w
ORDER BY w.wait_time_ms DESC;

-- ============================================================
-- NEXT STEPS based on dominant wait type:
--   PAGEIOLATCH_*        → add indexes (missing-indexes.sql), add RAM
--   LCK_M_*             → run blocking-analysis.sql
--   CXPACKET            → adjust MAXDOP server config or query hint
--   SOS_SCHEDULER_YIELD → find top CPU queries in top-slow-queries.sql
--   WRITELOG            → move .ldf to dedicated fast disk
--   RESOURCE_SEMAPHORE  → check for spilling queries in active-queries.sql
-- ============================================================
