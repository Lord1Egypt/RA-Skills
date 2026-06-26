---
name: sqlserver-monitoring
description: SQL Server monitoring — SQL Agent jobs, error log, database health, blocking chains, deadlock analysis, long-running transactions, and disk space.
---

# SQL Server Monitoring

Use this skill to check SQL Server health, investigate blocking or deadlocks, monitor SQL Agent jobs, and review the error log.

---

## 1. SQL Agent Jobs

### Check Job Status

```sql
-- All jobs and their last run result
SELECT
    j.name                          AS job_name,
    j.enabled,
    CASE jh.run_status
        WHEN 0 THEN 'Failed'
        WHEN 1 THEN 'Succeeded'
        WHEN 2 THEN 'Retry'
        WHEN 3 THEN 'Cancelled'
        WHEN 4 THEN 'In Progress'
    END                             AS last_run_status,
    msdb.dbo.agent_datetime(jh.run_date, jh.run_time) AS last_run_time,
    -- Duration in HH:MM:SS
    RIGHT('0' + CAST(jh.run_duration / 10000 AS VARCHAR), 2) + ':' +
    RIGHT('0' + CAST((jh.run_duration % 10000) / 100 AS VARCHAR), 2) + ':' +
    RIGHT('0' + CAST(jh.run_duration % 100 AS VARCHAR), 2) AS duration_hhmmss,
    jh.message
FROM msdb.dbo.sysjobs j
LEFT JOIN msdb.dbo.sysjobhistory jh ON j.job_id = jh.job_id
    AND jh.instance_id = (
        SELECT MAX(instance_id) FROM msdb.dbo.sysjobhistory
        WHERE job_id = j.job_id AND step_id = 0
    )
ORDER BY last_run_time DESC;
```

### Find Failed Jobs in Last 24 Hours

```sql
SELECT
    j.name                          AS job_name,
    msdb.dbo.agent_datetime(jh.run_date, jh.run_time) AS run_time,
    jh.step_id, jh.step_name,
    jh.message
FROM msdb.dbo.sysjobs j
JOIN msdb.dbo.sysjobhistory jh ON j.job_id = jh.job_id
WHERE jh.run_status = 0   -- 0 = Failed
  AND msdb.dbo.agent_datetime(jh.run_date, jh.run_time) >= DATEADD(HOUR, -24, GETDATE())
ORDER BY run_time DESC;
```

### Currently Running Jobs

```sql
SELECT
    j.name          AS job_name,
    ja.start_execution_date,
    DATEDIFF(MINUTE, ja.start_execution_date, GETDATE()) AS running_minutes,
    ja.last_executed_step_id,
    ja.last_executed_step_date
FROM msdb.dbo.sysjobactivity ja
JOIN msdb.dbo.sysjobs j ON ja.job_id = j.job_id
WHERE ja.session_id = (SELECT MAX(session_id) FROM msdb.dbo.syssessions)
  AND ja.start_execution_date IS NOT NULL
  AND ja.stop_execution_date IS NULL;
```

---

## 2. Error Log

```sql
-- Read current SQL Server error log
-- Parameters: (log file #, log type, search str1, search str2, start, end, sort order)
EXEC xp_readerrorlog 0, 1, NULL, NULL, NULL, NULL, 'DESC';

-- Filter to errors only (severity 17+)
EXEC xp_readerrorlog 0, 1, 'Error', NULL, NULL, NULL, 'DESC';

-- Check for specific timeframe
DECLARE @start DATETIME = DATEADD(HOUR, -4, GETDATE());
DECLARE @end   DATETIME = GETDATE();
EXEC xp_readerrorlog 0, 1, NULL, NULL, @start, @end, 'DESC';

-- Check previous log file (log rotates on restart)
EXEC xp_readerrorlog 1, 1, NULL, NULL, NULL, NULL, 'DESC';

-- How many error log files exist
EXEC xp_enumerrorlogs;
```

---

## 3. Database Health

```sql
-- Status and log reuse reason for all databases
SELECT
    name,
    state_desc,             -- Should be ONLINE; SUSPECT/EMERGENCY = problem
    recovery_model_desc,
    log_reuse_wait_desc,    -- Why log space can't be reused (see below)
    is_read_only,
    is_auto_close_on,       -- Should be OFF in production
    is_auto_shrink_on,      -- Should be OFF in production
    compatibility_level     -- SQL Server version compatibility
FROM sys.databases
ORDER BY name;
```

**`log_reuse_wait_desc` values:**
| Value | Meaning | Fix |
|-------|---------|-----|
| `NOTHING` | Log can be reused — healthy | — |
| `LOG_BACKUP` | Waiting for a log backup (FULL recovery mode) | Take a transaction log backup |
| `CHECKPOINT` | Waiting for checkpoint | Run `CHECKPOINT` or wait |
| `ACTIVE_TRANSACTION` | Long-running open transaction | Find and close the transaction |
| `DATABASE_MIRRORING` | Mirroring partner is behind | Check mirroring latency |
| `REPLICATION` | Replication not read | Check distributor |
| `AVAILABILITY_REPLICA` | AG secondary is behind | Check AG health |

---

## 4. Disk Space

```sql
-- Data and log file sizes and free space
SELECT
    DB_NAME(mf.database_id)                             AS database_name,
    mf.name                                             AS logical_name,
    mf.physical_name,
    mf.type_desc,
    mf.size * 8 / 1024                                  AS allocated_mb,
    (mf.size * 8 / 1024) -
        (FILEPROPERTY(mf.name, 'SpaceUsed') * 8 / 1024) AS free_mb,
    FILEPROPERTY(mf.name, 'SpaceUsed') * 8 / 1024      AS used_mb,
    CASE mf.is_percent_growth
        WHEN 1 THEN CAST(mf.growth AS VARCHAR) + '%'
        ELSE CAST(mf.growth * 8 / 1024 AS VARCHAR) + ' MB'
    END                                                 AS auto_growth
FROM sys.master_files mf
ORDER BY database_name, mf.type_desc;
```

---

## 5. Blocking Analysis

**Script:** `../scripts/blocking-analysis.sql`

### Quick Blocking Check

```sql
-- Sessions that are blocked and what's blocking them
SELECT
    r.session_id,
    r.blocking_session_id,
    r.wait_type,
    r.wait_time / 1000.0        AS wait_time_s,
    r.total_elapsed_time / 1000.0 AS elapsed_s,
    SUBSTRING(t.text, (r.statement_start_offset/2)+1,
        ((CASE r.statement_end_offset WHEN -1 THEN DATALENGTH(t.text)
          ELSE r.statement_end_offset END - r.statement_start_offset)/2)+1) AS blocked_query,
    s.login_name,
    s.host_name
FROM sys.dm_exec_requests r
JOIN sys.dm_exec_sessions s ON r.session_id = s.session_id
CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) t
WHERE r.blocking_session_id > 0
ORDER BY r.wait_time DESC;
```

### Find the Head Blocker

```sql
-- The session blocking all others (head of the chain)
SELECT
    s.session_id,
    s.login_name,
    s.host_name,
    s.program_name,
    s.status,
    t.text AS current_or_last_query
FROM sys.dm_exec_sessions s
LEFT JOIN sys.dm_exec_requests r  ON s.session_id = r.session_id
OUTER APPLY sys.dm_exec_sql_text(COALESCE(r.sql_handle, s.sql_handle)) t
WHERE s.session_id IN (
    -- Sessions that ARE blocking someone but are NOT themselves blocked
    SELECT DISTINCT blocking_session_id
    FROM sys.dm_exec_requests
    WHERE blocking_session_id > 0
)
AND s.session_id NOT IN (
    SELECT session_id FROM sys.dm_exec_requests WHERE blocking_session_id > 0
);
```

⚠️ **Using KILL:**
```sql
-- KILL should only be used after business confirmation that the blocking transaction
-- can be safely terminated. Killing a session rolls back all open transactions.
-- Never execute KILL autonomously.
-- KILL 57;  -- Replace 57 with actual session_id
```

---

## 6. Deadlock Detection

### Read from System Health Session

SQL Server captures deadlock graphs automatically in the `system_health` extended events session.

```sql
-- Read deadlock events from system_health ring buffer
SELECT
    xdr.value('@timestamp', 'DATETIME2')       AS deadlock_time,
    xdr.query('.')                              AS deadlock_graph_xml
FROM (
    SELECT CAST(target_data AS XML) AS target_data
    FROM sys.dm_xe_session_targets t
    JOIN sys.dm_xe_sessions s ON t.event_session_address = s.address
    WHERE s.name = 'system_health'
      AND t.target_name = 'ring_buffer'
) AS data
CROSS APPLY target_data.nodes('//RingBufferTarget/event[@name="xml_deadlock_report"]') AS xdt(xdr)
ORDER BY deadlock_time DESC;
```

Click the `deadlock_graph_xml` result in SSMS to view the graphical deadlock graph.

### Read Deadlock Graph

In the deadlock graph:
- **Ovals** = transactions/processes
- **Rectangles** = resources (locks)
- **Arrows** = "this process owns this lock" and "this process is waiting for this lock"
- The process marked with the **X** was chosen as the deadlock victim (killed by SQL Server)

**Common deadlock patterns:**
1. **Update order deadlock** — Two sessions update the same two tables in different order. Fix: standardize update order.
2. **Reader-writer deadlock** — Reader holds shared lock, writer needs exclusive. Fix: add indexes to reduce scan time; use RCSI.
3. **Foreign key deadlock** — Parent-child insert/delete in different order. Fix: index foreign key columns on child table.

---

## 7. Long-Running Transactions

```sql
-- Transactions open longer than 5 minutes
SELECT
    s.session_id,
    s.login_name,
    s.host_name,
    at.transaction_begin_time,
    DATEDIFF(MINUTE, at.transaction_begin_time, GETDATE()) AS open_minutes,
    at.transaction_type,
    at.transaction_state,
    t.text AS last_query
FROM sys.dm_tran_active_transactions at
JOIN sys.dm_tran_session_transactions st ON at.transaction_id = st.transaction_id
JOIN sys.dm_exec_sessions s ON st.session_id = s.session_id
LEFT JOIN sys.dm_exec_requests r ON s.session_id = r.session_id
OUTER APPLY sys.dm_exec_sql_text(COALESCE(r.sql_handle, s.sql_handle)) t
WHERE DATEDIFF(MINUTE, at.transaction_begin_time, GETDATE()) > 5
ORDER BY open_minutes DESC;
```

**Long-running transactions cause:**
- Log space not being reused (`log_reuse_wait_desc = ACTIVE_TRANSACTION`)
- Version store bloat in TempDB (if RCSI is enabled)
- Blocking other sessions

Fix: investigate whether the transaction is in an application that forgot to commit, or whether a stored procedure is running longer than expected.
