---
name: sqlserver-diagnostics
description: Identify SQL Server performance bottlenecks using DMV queries. Covers wait stats, slow queries, active requests, performance counters, and connection analysis.
---

# SQL Server Diagnostics

Use this skill when a SQL Server instance is slow, queries are timing out, or you need to identify the source of a performance problem. Start here before diving into indexes or execution plans.

---

## Recommended Workflow

```
1. Check wait stats          → scripts/wait-stats.sql
2. Find top slow queries     → scripts/top-slow-queries.sql
3. See what's running NOW    → scripts/active-queries.sql
4. Drill into a specific query → sqlserver-execution-plans/SKILL.md
5. Act on findings           → sqlserver-indexes or sqlserver-query-optimization
```

---

## 1. Wait Stats Analysis

Wait stats are the single best indicator of what SQL Server is struggling with. Every time SQL Server can't proceed, it records a wait type. High cumulative waits tell you the category of problem.

**Script:** `../scripts/wait-stats.sql`

```sql
-- Quick inline version (run from any database)
SELECT TOP 20
    wait_type,
    wait_time_ms / 1000.0                          AS wait_time_s,
    (wait_time_ms - signal_wait_time_ms) / 1000.0  AS resource_wait_s,
    signal_wait_time_ms / 1000.0                   AS signal_wait_s,
    waiting_tasks_count,
    CAST(100.0 * wait_time_ms /
         SUM(wait_time_ms) OVER () AS DECIMAL(5,2)) AS pct_of_total
FROM sys.dm_os_wait_stats
WHERE wait_type NOT IN (
    'SLEEP_TASK','BROKER_TO_FLUSH','BROKER_TASK_STOP','CLR_AUTO_EVENT',
    'CLR_MANUAL_EVENT','DISPATCHER_QUEUE_SEMAPHORE','FT_IFTS_SCHEDULER_IDLE_WAIT',
    'HADR_FILESTREAM_IOMGR_IOCOMPLETION','HADR_WORK_QUEUE','LAZYWRITER_SLEEP',
    'LOGMGR_QUEUE','ONDEMAND_TASK_QUEUE','REQUEST_FOR_DEADLOCK_SEARCH',
    'RESOURCE_QUEUE','SERVER_IDLE_CHECK','SLEEP_DBSTARTUP','SLEEP_DCOMSTARTUP',
    'SLEEP_MASTERDBREADY','SLEEP_MASTERMDREADY','SLEEP_MASTERUPGRADED',
    'SLEEP_MSDBSTARTUP','SLEEP_SYSTEMTASK','SLEEP_TEMPDBSTARTUP',
    'SNI_HTTP_ACCEPT','SP_SERVER_DIAGNOSTICS_SLEEP','SQLTRACE_BUFFER_FLUSH',
    'WAITFOR','XE_DISPATCHER_WAIT','XE_TIMER_EVENT','DBMIRROR_EVENTS_QUEUE',
    'SQLTRACE_INCREMENTAL_FLUSH_SLEEP','WAIT_XTP_OFFLINE_CKPT_NEW_LOG',
    'BROKER_EVENTHANDLER','CHECKPOINT_QUEUE','DBMIRROR_WORKER_QUEUE',
    'SQLTRACE_WAIT_ENTRIES','WAIT_XTP_ONLINE_CKPT_NEW_LOG','ASYNC_NETWORK_IO'
)
ORDER BY wait_time_ms DESC;
```

### Wait Type Interpretation Guide

| Wait Type | Meaning | Typical Fix |
|-----------|---------|-------------|
| `PAGEIOLATCH_SH` / `PAGEIOLATCH_EX` | Reading/writing data pages from disk (I/O bound) | Add RAM, faster storage, better indexes to reduce I/O |
| `LCK_M_*` | Lock waits (blocking) | Find and fix blocking queries; review transaction isolation |
| `CXPACKET` / `CXCONSUMER` | Parallelism — threads waiting on each other | Review MAXDOP setting; fix skewed parallel queries |
| `SOS_SCHEDULER_YIELD` | CPU pressure — threads giving up CPU time | Query tuning, reduce CPU-intensive operations |
| `WRITELOG` | Log writes — transaction log is a bottleneck | Move log file to faster disk; reduce transaction size |
| `RESOURCE_SEMAPHORE` | Memory grants waiting — queries need more memory | Fix memory-spilling queries; increase `max server memory` |
| `ASYNC_NETWORK_IO` | Results sent to client faster than client reads | Reduce result set sizes; check client application |
| `LATCH_EX` / `LATCH_SH` | Internal memory structure contention | Usually TempDB contention — add TempDB files |
| `PAGELATCH_*` | In-memory page contention (TempDB allocation) | Add TempDB data files (8 files is common recommendation) |
| `HADR_*` | Always On Availability Groups activity | Normal in AG environments; high values = AG lag |

**Rule of thumb:** If one wait type dominates (>30% of total), that's your problem category.

---

## 2. Top Slow Queries

Identify the queries consuming the most elapsed time, CPU, or I/O since SQL Server last restarted.

**Script:** `../scripts/top-slow-queries.sql`

```sql
-- Quick inline version
SELECT TOP 25
    qs.total_elapsed_time / qs.execution_count / 1000.0   AS avg_elapsed_ms,
    qs.total_elapsed_time / 1000.0                         AS total_elapsed_ms,
    qs.execution_count,
    qs.total_logical_reads / qs.execution_count            AS avg_logical_reads,
    qs.total_worker_time / qs.execution_count / 1000.0     AS avg_cpu_ms,
    qs.total_logical_reads                                 AS total_logical_reads,
    DB_NAME(qt.dbid)                                       AS database_name,
    SUBSTRING(qt.text, (qs.statement_start_offset/2)+1,
        ((CASE qs.statement_end_offset
            WHEN -1 THEN DATALENGTH(qt.text)
            ELSE qs.statement_end_offset
          END - qs.statement_start_offset)/2)+1)           AS query_text,
    qs.query_hash
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) qt
ORDER BY avg_elapsed_ms DESC;
```

**Key columns:**
- `avg_elapsed_ms` — wall-clock time per execution (most useful for user-facing queries)
- `avg_logical_reads` — data pages read from buffer pool (index problems show up here)
- `avg_cpu_ms` — CPU time per execution (CPU-bound queries)
- `execution_count` — high count + high avg = highest total impact

---

## 3. Currently Running Queries

See what's actively executing right now, including wait info and blocking.

**Script:** `../scripts/active-queries.sql`

```sql
-- Quick inline version
SELECT
    r.session_id,
    s.login_name,
    r.status,
    r.wait_type,
    r.wait_time / 1000.0        AS wait_time_s,
    r.cpu_time / 1000.0         AS cpu_time_s,
    r.logical_reads,
    r.total_elapsed_time / 1000.0 AS elapsed_time_s,
    r.blocking_session_id,
    SUBSTRING(t.text, (r.statement_start_offset/2)+1,
        ((CASE r.statement_end_offset
            WHEN -1 THEN DATALENGTH(t.text)
            ELSE r.statement_end_offset
          END - r.statement_start_offset)/2)+1) AS current_statement,
    s.host_name,
    s.program_name
FROM sys.dm_exec_requests r
JOIN sys.dm_exec_sessions s ON r.session_id = s.session_id
CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) t
WHERE r.session_id != @@SPID
  AND s.is_user_process = 1
ORDER BY r.total_elapsed_time DESC;
```

**What to look for:**
- `blocking_session_id > 0` → that session is being blocked (see monitoring/SKILL.md)
- `wait_type = 'PAGEIOLATCH_*'` → query doing heavy I/O right now
- `status = 'suspended'` + long `wait_time_s` → stuck on a resource

---

## 4. Performance Counters

Key performance counters via DMV (no need for PerfMon):

```sql
SELECT
    counter_name,
    instance_name,
    cntr_value
FROM sys.dm_os_performance_counters
WHERE counter_name IN (
    'Page life expectancy',        -- Buffer pool health (want > 300s, ideally > 1000s)
    'Batch Requests/sec',          -- Server load
    'SQL Compilations/sec',        -- High = lots of ad-hoc queries or plan cache pressure
    'SQL Re-Compilations/sec',     -- High = unstable plans, check sp_recompile usage
    'Page reads/sec',              -- High = I/O pressure
    'Page writes/sec',
    'Lazy writes/sec',             -- High = buffer pool too small
    'Memory Grants Pending',       -- > 0 regularly = memory pressure for query execution
    'User Connections'
)
  AND instance_name IN ('', 'SQLServer:Buffer Manager')
ORDER BY counter_name;
```

**Key thresholds:**
- **Page Life Expectancy (PLE)** < 300s: buffer pool is too small — data is cycling out before reuse
- **Memory Grants Pending** > 0: queries waiting for memory grants — potential sort/hash spills
- **Lazy Writes/sec** > 20: SQL Server is flushing dirty pages too aggressively — add RAM
- **SQL Re-Compilations/sec** high: check for `WITH RECOMPILE` stored procs or temp table schema changes

---

## 5. Connection Counts

```sql
-- Active connections by database and login
SELECT
    DB_NAME(dbid)   AS database_name,
    loginame,
    COUNT(*)        AS connection_count
FROM sys.sysprocesses
WHERE dbid > 0
GROUP BY dbid, loginame
ORDER BY connection_count DESC;

-- Total connection count
SELECT COUNT(*) AS total_connections
FROM sys.dm_exec_connections;
```

---

## 6. Memory Usage

```sql
-- Buffer pool usage by database
SELECT
    DB_NAME(database_id)     AS database_name,
    COUNT(*) * 8 / 1024.0    AS buffer_pool_mb
FROM sys.dm_os_buffer_descriptors
WHERE database_id > 4  -- exclude system databases
GROUP BY database_id
ORDER BY buffer_pool_mb DESC;

-- Total SQL Server memory usage
SELECT
    physical_memory_in_use_kb / 1024    AS memory_used_mb,
    page_fault_count
FROM sys.dm_os_process_memory;
```

---

## Diagnostic Checklist

When a performance complaint comes in:

- [ ] Run `wait-stats.sql` — what's the dominant wait type?
- [ ] Run `top-slow-queries.sql` — any obvious offenders (high avg_elapsed_ms)?
- [ ] Run `active-queries.sql` — any current blocking or long-running queries?
- [ ] Check PLE via performance counters — is the buffer pool healthy?
- [ ] Check `Memory Grants Pending` — are queries spilling to disk?
- [ ] If blocking found → go to `sqlserver-monitoring/SKILL.md`
- [ ] If slow query found → go to `sqlserver-execution-plans/SKILL.md`
- [ ] If missing indexes suggested → go to `sqlserver-indexes/SKILL.md`
