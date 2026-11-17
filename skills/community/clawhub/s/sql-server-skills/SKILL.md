---
name: sql-server-skills
description: "Comprehensive SQL Server performance diagnostics, index analysis, execution plan interpretation, query optimization, schema management, backup/restore, and monitoring using sqlcmd and T-SQL DMVs. Use when analyzing slow queries, investigating wait stats, finding missing indexes, reading execution plans, optimizing stored procedures or views, managing migrations, monitoring SQL Agent jobs, or diagnosing blocking/deadlocks on Microsoft SQL Server. Triggers on: SQL Server, MSSQL, sqlcmd, T-SQL performance, slow query, execution plan, DMV, missing index, wait stats, blocking, deadlock, stored procedure optimization, view tuning."
dependencies:
  - sqlcmd
---

# SQL Server Skills — Comprehensive Reference

This skill provides complete reference and workflows for Microsoft SQL Server diagnostics,
performance tuning, index management, execution plan analysis, and more.
It covers 7 domains via sqlcmd and T-SQL DMV queries targeting SQL Server 2016+.

---

## Overview


# SQL Server Skills

Comprehensive SQL Server skill for AI agents. Covers performance diagnostics, index analysis, execution plan interpretation, query optimization, schema management, backup/restore, and monitoring — all via `sqlcmd` and T-SQL DMVs.

---

## Requirements

- **`sqlcmd`** — [Microsoft Download](https://learn.microsoft.com/en-us/sql/tools/sqlcmd/sqlcmd-utility)
- **SQL Server 2016+** — All DMV queries target compatibility level 130+
- **Permissions** — `VIEW SERVER STATE` for most DMV queries; operation-specific least privilege and exact-target DBA review for changes

---

## Quick Connect

Prefer integrated authentication (`-E`) with an operator-configured identity. For SQL
authentication, sqlcmd reads an already securely provisioned `SQLCMDPASSWORD` directly;
never expand it into arguments. Never ask for, print, or persist passwords. Do not
create password files, use shell tracing, or dump the environment. If no secure
authentication is available, stop and let the operator configure it outside the agent.

Choose exactly one authentication setup in the same Bash session as the workflows.
The choice is explicit: a missing SQL password never falls back to another identity.

```bash
# Integrated authentication: operator-configured identity
SQL_AUTH=(-E)
```

```bash
# SQL Authentication: SQLCMDPASSWORD must already be exported securely
[ -n "${SQLCMDPASSWORD:-}" ] || { echo 'SQLCMDPASSWORD not provisioned or empty' >&2; exit 1; }
SQL_AUTH=(-U "$SQL_USER")
```

```bash
# Connect to the selected database using the chosen authentication
sqlcmd -S "$SQL_SERVER" "${SQL_AUTH[@]:?Select authentication first}" -d "$SQL_DATABASE"

# Run a diagnostic script
sqlcmd -S "$SQL_SERVER" "${SQL_AUTH[@]:?Select authentication first}" -d master -i scripts/top-slow-queries.sql

# Run with output to file
sqlcmd -S "$SQL_SERVER" "${SQL_AUTH[@]:?Select authentication first}" -d master -i scripts/wait-stats.sql -o results.txt -s "," -W
```

SQL authentication requires a nonempty, exported `SQLCMDPASSWORD` provisioned outside
this agent session. If it is absent or empty, stop; never type a password into a prompt.
Re-run the presence check before SQL-auth workflows if the environment has changed.

### Compatibility

The old `SQL_PASSWORD` credential name is replaced by `SQLCMDPASSWORD`. Operators must
update secure environment provisioning outside the agent; the old variable is not read
or copied. This is a breaking credential-name change. Integrated authentication needs
no SQL password. The examples below reuse the chosen `SQL_AUTH` Bash array for either
mode; do not switch identities silently.

---

## Skill Organization

| Sub-Skill | Path | Use When |
|-----------|------|----------|
| **Diagnostics** | `sqlserver-diagnostics/SKILL.md` | Server is slow — find the bottleneck (wait stats, slow queries, active requests) |
| **Indexes** | `sqlserver-indexes/SKILL.md` | Find missing indexes, fix fragmentation, drop unused indexes |
| **Execution Plans** | `sqlserver-execution-plans/SKILL.md` | Read and interpret query execution plans, spot bad operators |
| **Query Optimization** | `sqlserver-query-optimization/SKILL.md` | Fix stored procedures, views, anti-patterns, parameter sniffing |
| **Schema** | `sqlserver-schema/SKILL.md` | CREATE/ALTER TABLE, migrations, constraints, data types |
| **Backup/Restore** | `sqlserver-backup/SKILL.md` | BACKUP DATABASE, RESTORE, check backup history |
| **Monitoring** | `sqlserver-monitoring/SKILL.md` | SQL Agent jobs, error log, blocking, deadlocks, long-running transactions |

---

## Decision Tree — What Are You Trying To Do?

```
Is the server slow or a query timing out?
├── I don't know WHERE the bottleneck is → sqlserver-diagnostics
│   └── Start with wait-stats.sql, then top-slow-queries.sql
│
├── I have a specific slow query → sqlserver-execution-plans
│   └── Capture the plan, identify bad operators
│
├── I suspect missing or broken indexes → sqlserver-indexes
│   └── Run missing-indexes.sql + index-fragmentation.sql
│
└── I want to rewrite/fix bad T-SQL code → sqlserver-query-optimization
    └── Check anti-patterns: cursors, non-SARGable, DELETE+INSERT loops

Is there a blocking/locking issue?
└── sqlserver-monitoring (blocking-analysis.sql)

Do I need to change the schema?
└── sqlserver-schema

Do I need to backup or restore a database?
└── sqlserver-backup

Do I need to check SQL Agent jobs or the error log?
└── sqlserver-monitoring
```

---

## Common Workflows

### Workflow 1: Server Is Slow — Start Here

```bash
# Step 1: What is SQL Server waiting on?
sqlcmd -S "$SQL_SERVER" "${SQL_AUTH[@]:?Select authentication first}" -d master -i scripts/wait-stats.sql

# Step 2: Which queries are consuming the most resources?
sqlcmd -S "$SQL_SERVER" "${SQL_AUTH[@]:?Select authentication first}" -d master -i scripts/top-slow-queries.sql

# Step 3: What's running right now?
sqlcmd -S "$SQL_SERVER" "${SQL_AUTH[@]:?Select authentication first}" -d master -i scripts/active-queries.sql
```

Then read `sqlserver-diagnostics/SKILL.md` to interpret results.

---

### Workflow 2: Optimize a Specific Query

```sql
-- Step 1: Capture I/O and time stats
SET STATISTICS IO ON;
SET STATISTICS TIME ON;
GO
-- paste your query here
GO

-- Step 2: Get XML execution plan
SET STATISTICS XML ON;
GO
-- paste your query here
GO
SET STATISTICS XML OFF;
```

Then read `sqlserver-execution-plans/SKILL.md` to interpret the plan.

---

### Workflow 3: Monthly Index Maintenance

```bash
# Find missing indexes (sorted by impact score)
sqlcmd -S "$SQL_SERVER" "${SQL_AUTH[@]:?Select authentication first}" -d "$SQL_DATABASE" -i scripts/missing-indexes.sql -b -y 0 -w 65535 || exit $?

# Check fragmentation
sqlcmd -S "$SQL_SERVER" "${SQL_AUTH[@]:?Select authentication first}" -d "$SQL_DATABASE" -i scripts/index-fragmentation.sql

# Find unused indexes costing write overhead
sqlcmd -S "$SQL_SERVER" "${SQL_AUTH[@]:?Select authentication first}" -d "$SQL_DATABASE" -i scripts/unused-indexes.sql
```

The missing-index XML aggregation cannot represent XML 1.0-invalid identifier
characters (for example U+0001). Check the `-b` exit status: on any error, discard
the entire report, including partial output, and stop for DBA investigation.

Missing-index proposals retain `nvarchar(max)` for long column lists. Use `-y 0`
to remove sqlcmd's default 256-character limit; `-w 65535` reduces line wrapping.
Do not combine `-W` with `-y` or `-Y`. Unlimited display increases output cost;
very long rows can still wrap. Inspect complete values in a suitable client and
never execute a saved report as SQL. See [sqlcmd output options](https://learn.microsoft.com/en-us/sql/tools/sqlcmd/sqlcmd-utility#format-options).

See `sqlserver-indexes/SKILL.md` for interpretation and the rebuild/reorganize decision.

---

### Workflow 4: Investigate Blocking

```bash
# Run blocking analysis
sqlcmd -S "$SQL_SERVER" "${SQL_AUTH[@]:?Select authentication first}" -d master -i scripts/blocking-analysis.sql
```

See `sqlserver-monitoring/SKILL.md` for deadlock investigation and KILL guidance.

Only a human DBA issues KILL; agents and automated processes never do.
A human DBA must obtain exact-target and application-owner approval, review rollback
safety, and recheck identity because session IDs can be reused.

```sql
-- Human DBA preflight only: replace NULL with the reviewed session ID.
-- Confirm sys.dm_exec_sessions.is_user_process = 1; no row means stop.
-- Recheck identity immediately before acting; this snapshot is not authorization.
DECLARE @review_session_id smallint = NULL;
SELECT session_id, is_user_process, login_name, host_name, program_name,
       login_time, open_transaction_count
FROM sys.dm_exec_sessions
WHERE session_id = @review_session_id
  AND is_user_process = 1;
```

---

## Sub-Skill Quick Reference

- **`sqlserver-diagnostics/SKILL.md`** — DMV-based bottleneck analysis (most important starting point)
- **`sqlserver-indexes/SKILL.md`** — Full index lifecycle: find, fix, maintain, drop
- **`sqlserver-execution-plans/SKILL.md`** — Read plans, spot table scans, fix key lookups
- **`sqlserver-query-optimization/SKILL.md`** — Stored proc rewrites, anti-patterns, hints
- **`sqlserver-schema/SKILL.md`** — DDL patterns, migrations, data type guidance
- **`sqlserver-backup/SKILL.md`** — Backup/restore commands and history queries
- **`sqlserver-monitoring/SKILL.md`** — Jobs, error log, blocking, deadlocks

---

## sqlserver backup


# SQL Server Backup & Restore

Use this skill for database backup strategies, restore procedures, and verifying backup integrity.

---

Before any backup, restore or recovery-model change, require exact-target DBA review
of the server, database, backup set and destination paths. Use least privilege and
SQL Server service-account filesystem permissions scoped to the intended location.
Backups contain sensitive data: restrict access and protect them according to the
operator's encryption and retention policy. Test in staging with a recovery plan,
capacity checks and an approved maintenance window; never run these changes autonomously.

## Recovery Models

Choose the right recovery model before designing your backup strategy.

| Model | Log Truncation | Point-in-Time Recovery | Log Growth Risk | Use When |
|-------|---------------|----------------------|-----------------|----------|
| **SIMPLE** | Auto at checkpoint | ❌ No | Low | Dev, test, non-critical data |
| **FULL** | On log backup | ✅ Yes | High (must take log backups) | Production — minimizes data loss |
| **BULK_LOGGED** | On log backup | Partial | Medium | Bulk load periods (then switch back to FULL) |

```sql
-- Check current recovery model
SELECT name, recovery_model_desc, log_reuse_wait_desc
FROM sys.databases
WHERE name = DB_NAME();

-- DBA approval required: SIMPLE breaks the log backup chain and point-in-time recovery.
-- These are alternative choices, not a sequence to execute.
-- Change recovery model
ALTER DATABASE MyDatabase SET RECOVERY FULL;
ALTER DATABASE MyDatabase SET RECOVERY SIMPLE;
```

⚠️ **Switching from SIMPLE to FULL:** Take a full or differential data backup to start the log backup chain, then schedule log backups and monitor space. Switching to SIMPLE loses log-chain continuity; assess RPO and recovery requirements first.

---

## BACKUP DATABASE

### Full Backup

Confirm destination capacity, access and retention; do not overwrite required backup
media. An ordinary full backup changes the differential base. For an ad hoc full
backup, consider `COPY_ONLY` to preserve the scheduled differential base. Check I/O
impact and protect backup files; do not add INIT/FORMAT to bypass media safeguards.

```sql
-- Full backup to disk
BACKUP DATABASE MyDatabase
TO DISK = 'D:\Backups\MyDatabase_Full_20240315.bak'
WITH
    COMPRESSION,              -- Recommended — reduces size significantly
    CHECKSUM,                 -- Verify backup integrity during write
    STATS = 10,               -- Progress reporting every 10%
    NAME = 'MyDatabase Full Backup 2024-03-15';
GO

-- Full backup with timestamp in filename (useful for scripted backups)
DECLARE @BackupPath NVARCHAR(500) =
    'D:\Backups\MyDatabase_Full_' + FORMAT(GETDATE(), 'yyyyMMdd_HHmmss') + '.bak';
BACKUP DATABASE MyDatabase TO DISK = @BackupPath WITH COMPRESSION, CHECKSUM;
```

### Differential Backup

A differential backup captures only changes since the last full backup. Faster than full; faster to restore than many log backups.

```sql
BACKUP DATABASE MyDatabase
TO DISK = 'D:\Backups\MyDatabase_Diff_20240315.bak'
WITH DIFFERENTIAL, COMPRESSION, CHECKSUM, STATS = 10;
```

### Transaction Log Backup

Must be taken regularly in FULL recovery mode to prevent log growth and enable point-in-time recovery.

```sql
BACKUP LOG MyDatabase
TO DISK = 'D:\Backups\MyDatabase_Log_20240315_1200.trn'
WITH COMPRESSION, CHECKSUM, STATS = 10;
```

---

## RESTORE DATABASE

**STOP: restore can replace data and interrupt applications.** Require exact-target
DBA review, service-owner approval and a tested recovery plan. Prefer restoring to a
new staging database and new files first. Inspect HEADERONLY and FILELISTONLY,
verify the full/differential/log chain and recovery point, and confirm every MOVE
path avoids existing files. Determine whether a tail-log backup is needed and possible
to preserve recent work before restoring. Do not add REPLACE to bypass safety checks.
NORECOVERY keeps the database unavailable for further restores; RECOVERY ends that
restore sequence. Confirm client cutover, dependencies, capacity and outage timing.

### Restore from Full Backup Only

```sql
-- Restore to original location
RESTORE DATABASE MyDatabase
FROM DISK = 'D:\Backups\MyDatabase_Full_20240315.bak'
WITH
    RECOVERY,    -- Bring database online after this restore
    STATS = 10;

-- Restore to different location (new database)
RESTORE DATABASE MyDatabase_Restored
FROM DISK = 'D:\Backups\MyDatabase_Full_20240315.bak'
WITH
    MOVE 'MyDatabase'      TO 'E:\Data\MyDatabase_Restored.mdf',
    MOVE 'MyDatabase_log'  TO 'F:\Logs\MyDatabase_Restored_log.ldf',
    RECOVERY, STATS = 10;
```

### Restore Full + Differential + Log Backups

```sql
-- Step 1: Restore full backup (NORECOVERY = keep restoring)
RESTORE DATABASE MyDatabase
FROM DISK = 'D:\Backups\MyDatabase_Full_20240315.bak'
WITH NORECOVERY, STATS = 10;

-- Step 2: Apply differential backup (NORECOVERY)
RESTORE DATABASE MyDatabase
FROM DISK = 'D:\Backups\MyDatabase_Diff_20240315.bak'
WITH NORECOVERY, STATS = 10;

-- Step 3: Apply transaction log backups in order (NORECOVERY until last one)
RESTORE LOG MyDatabase
FROM DISK = 'D:\Backups\MyDatabase_Log_20240315_0800.trn'
WITH NORECOVERY;

RESTORE LOG MyDatabase
FROM DISK = 'D:\Backups\MyDatabase_Log_20240315_0900.trn'
WITH NORECOVERY;

-- Step 4: Final log backup — WITH RECOVERY brings database online
RESTORE LOG MyDatabase
FROM DISK = 'D:\Backups\MyDatabase_Log_20240315_1000.trn'
WITH RECOVERY;
```

### Point-in-Time Restore

```sql
-- Restore to specific point in time (requires FULL recovery model)
RESTORE LOG MyDatabase
FROM DISK = 'D:\Backups\MyDatabase_Log_20240315_1200.trn'
WITH
    RECOVERY,
    STOPAT = '2024-03-15 11:45:00';
```

---

## RESTORE VERIFYONLY

Check backup readability without performing a restore. `RESTORE VERIFYONLY` does not replace a test restore or validate the full logical data structure. Rehearse restoration and application validation in isolation:

```sql
RESTORE VERIFYONLY
FROM DISK = 'D:\Backups\MyDatabase_Full_20240315.bak'
WITH CHECKSUM;

-- Also check backup header
RESTORE HEADERONLY FROM DISK = 'D:\Backups\MyDatabase_Full_20240315.bak';

-- List files in a backup (for MOVE statements)
RESTORE FILELISTONLY FROM DISK = 'D:\Backups\MyDatabase_Full_20240315.bak';
```

---

## Check Backup History

```sql
-- Recent backups for a database
SELECT TOP 20
    bs.database_name,
    bs.backup_start_date,
    bs.backup_finish_date,
    DATEDIFF(SECOND, bs.backup_start_date, bs.backup_finish_date) AS duration_seconds,
    bs.backup_size / 1048576.0                                     AS backup_size_mb,
    bs.compressed_backup_size / 1048576.0                          AS compressed_mb,
    CASE bs.type
        WHEN 'D' THEN 'Full'
        WHEN 'I' THEN 'Differential'
        WHEN 'L' THEN 'Log'
    END                                                            AS backup_type,
    bmf.physical_device_name                                       AS backup_file
FROM msdb.dbo.backupset bs
JOIN msdb.dbo.backupmediafamily bmf ON bs.media_set_id = bmf.media_set_id
WHERE bs.database_name = 'MyDatabase'
ORDER BY bs.backup_finish_date DESC;

-- Check when last full backup was taken for all databases
SELECT
    database_name,
    MAX(backup_finish_date) AS last_full_backup,
    DATEDIFF(HOUR, MAX(backup_finish_date), GETDATE()) AS hours_since_backup
FROM msdb.dbo.backupset
WHERE type = 'D'  -- D = Full
GROUP BY database_name
ORDER BY last_full_backup ASC;
```

---

## Backup Strategy Recommendations

| Database Size | RPO | Recommended Strategy |
|---------------|-----|---------------------|
| < 50 GB | Hours | Nightly full + 4-hourly log backups |
| 50–500 GB | 1 hour | Nightly full + daily differential + hourly log |
| > 500 GB | 15 min | Weekly full + nightly differential + 15-min log |

**Always:**
- Store backups on a separate disk/server from the database
- Test restores periodically (at least monthly) — an untested backup is not a backup
- Use `WITH COMPRESSION` — typically 60-80% size reduction
- Use `WITH CHECKSUM` — validates available checksums; use restore checks and test restores too

---

## sqlserver diagnostics


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

---

## sqlserver execution plans


# SQL Server Execution Plans

Execution plans show exactly how SQL Server will execute (or did execute) a query. Reading them is the fastest way to diagnose why a query is slow.

---

## Capturing Plans

### Method 1: Statistics IO + Time (lightweight, always available)

```sql
SET STATISTICS IO ON;
SET STATISTICS TIME ON;
GO

-- Your query here
SELECT * FROM Orders WHERE CustomerID = 42;
GO

SET STATISTICS IO OFF;
SET STATISTICS TIME OFF;
```

**Output interpretation:**
```
Table 'Orders'. Scan count 1, logical reads 1247, physical reads 0, ...
SQL Server Execution Times: CPU time = 312 ms, elapsed time = 445 ms.
```
- **logical reads** — pages read from buffer pool (in-memory). High = too much data touched.
- **physical reads** — pages read from disk (not in buffer). High = buffer pool cold or too small.
- **CPU time** — pure computation. High = complex calculations or large in-memory sort.
- **elapsed time** — wall clock. Always >= CPU time. Gap = waiting (I/O, locks, etc.)

---

### Method 2: XML Execution Plan (estimated)

```sql
-- Estimated plan — does NOT execute the query
SET SHOWPLAN_XML ON;
GO
SELECT * FROM Orders WHERE CustomerID = 42;
GO
SET SHOWPLAN_XML OFF;
```

---

### Method 3: Actual Execution Plan

```sql
-- Actual plan — executes the query and captures real row counts
SET STATISTICS XML ON;
GO
SELECT * FROM Orders WHERE CustomerID = 42;
GO
SET STATISTICS XML OFF;
```

The XML result contains the full plan. Paste it into SSMS or [SentryOne Plan Explorer](https://www.sentryone.com/plan-explorer) for visual rendering.

---

### Method 4: Pull Plan from Cache

```sql
-- Find a cached plan by query text substring
SELECT TOP 5
    qs.execution_count,
    qs.total_elapsed_time / qs.execution_count / 1000.0 AS avg_elapsed_ms,
    qs.total_logical_reads / qs.execution_count          AS avg_logical_reads,
    SUBSTRING(qt.text, (qs.statement_start_offset/2)+1,
        ((CASE qs.statement_end_offset WHEN -1 THEN DATALENGTH(qt.text)
          ELSE qs.statement_end_offset END - qs.statement_start_offset)/2)+1) AS query_text,
    qp.query_plan
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle)    qt
CROSS APPLY sys.dm_exec_query_plan(qs.plan_handle) qp
WHERE qt.text LIKE '%Orders%'   -- adjust filter
ORDER BY avg_elapsed_ms DESC;
```

Click the `query_plan` result to open the graphical plan in SSMS.

---

## Key Operators — What to Look For

See `references/plan-operators.md` for the full reference table.

### 🔴 Bad: Table Scan

```
Operator: Table Scan (or Clustered Index Scan on large table)
Cost: HIGH — reads every row in the table
Fix: Add a non-clustered index with appropriate key columns
```

A table scan is acceptable only on small tables (< ~1000 rows). On large tables, it's almost always a missing index.

---

### 🔴 Bad: Key Lookup (Bookmark Lookup)

```
Operator: Key Lookup
Cost: MEDIUM–HIGH per row — two B-tree traversals per row
Fix: Add INCLUDE columns to the non-clustered index to cover the SELECT list
```

```sql
-- You have: CREATE INDEX IX_Orders_CustomerID ON Orders (CustomerID)
-- Query needs: CustomerID (seek), OrderDate, Status, TotalAmount (lookup to clustered)
-- Fix:
CREATE INDEX IX_Orders_CustomerID ON Orders (CustomerID)
INCLUDE (OrderDate, Status, TotalAmount);
```

---

### 🟡 Warning: Index Scan (non-clustered, large table)

```
Operator: Index Scan
Cost: MEDIUM — reads all or a large portion of the index leaf level
Fix: Check if a predicate is non-SARGable; verify index column order
```

---

### 🟡 Warning: Hash Match (with memory spill warning)

```
Operator: Hash Match (Join or Aggregate)
Symptom: Spill to TempDB warning icon, high memory grant
Fix: Add index to eliminate hashing; reduce row counts entering the join
```

Hash Match joins are not inherently bad — they're appropriate for large un-indexed joins. The problem is **memory spills**: when the hash table doesn't fit in the granted memory, SQL Server spills to TempDB — catastrophic for performance.

---

### 🟡 Warning: Sort (large, or causing spill)

```
Operator: Sort
Symptom: High cost percentage; spill warning
Fix: Add an index whose key order matches the ORDER BY to eliminate the sort
```

---

### 🟢 Good: Index Seek

```
Operator: Index Seek
Cost: LOW — navigates directly to relevant rows
```

This is what you want. The optimizer used the index B-tree to find exactly the rows needed.

---

### ℹ️ Parallelism (Exchange Operators)

```
Operators: Distribute Streams, Gather Streams, Repartition Streams
Context: Query is executing in parallel
Related wait: CXPACKET, CXCONSUMER
```

Parallelism is not inherently bad. Issues arise when:
- One thread finishes early and waits for others (CXPACKET skew)
- Query is too small to justify parallelism overhead
- `MAXDOP` is too high for the workload

```sql
-- Force single-threaded execution for testing
SELECT * FROM Orders WHERE CustomerID = 42
OPTION (MAXDOP 1);
```

---

## Row Estimate vs Actual Rows

One of the most important things to check: does SQL Server's estimate match reality?

**In SSMS:** Hover over any operator — "Estimated Number of Rows" vs "Actual Number of Rows"

| Discrepancy | Meaning | Fix |
|-------------|---------|-----|
| Estimate = 1, Actual = 50,000 | Severely underestimated — bad plan (wrong join strategy, missing index) | Inspect statistics under the review gates below; check for parameter sniffing |
| Estimate = 50,000, Actual = 1 | Overestimated — wasteful grants, parallel plan where serial is better | Inspect statistics under the review gates below |
| Within 2-3x | Acceptable | — |

**Update statistics:**

Require **exact-target DBA approval** of the database, schema, table and statistic
before any update. Prefer a reviewed named statistic (or explicitly reviewed table
scope); confirm the database context and require **ALTER on the target table**.
Monitoring permission alone does not authorize changes. Inspect statistics age and
sampling first; estimate errors alone do not justify FULLSCAN.

Review workload impact: FULLSCAN reads all rows, consumes I/O/CPU and can use tempdb;
statistics updates can trigger recompilation and change cardinality estimates and
execution plans. Rehearse on representative data in staging, schedule a maintenance window,
capture statistics/histogram and query-performance baselines, and agree on monitoring,
stop criteria and a DBA-owned recovery plan before execution. These examples
cannot automatically undo statistic/histogram changes or restore the plan cache and
previous plans. There is no universal rollback; investigate regressions and use a
separately reviewed, workload-specific recovery action rather than clearing cache.
On errors or regressions, stop further maintenance and consult the DBA.

```sql
-- Review-only example: replace with the approved statistic name and confirm context.
-- FULLSCAN is optional and needs its own workload justification.
-- UPDATE STATISTICS dbo.Orders [ReviewedStatisticName] WITH FULLSCAN;
```

`sp_updatestats` is database-wide maintenance, **not a default** troubleshooting step.
It requires separate DBA approval of the entire database scope and the same staging,
workload, maintenance and recovery gates above. On SQL Server, the caller must be
the database owner (dbo) or a member of the sysadmin fixed server role;
db_owner membership alone is not sufficient. Do not escalate a monitoring account
to run it. It can affect many statistics and cause recompilation across the database.

```sql
-- Reference only, after the separate database-wide approval:
-- EXEC sys.sp_updatestats;

-- Read-only inspection in the confirmed database; review metadata visibility.
SELECT
    OBJECT_NAME(s.object_id) AS table_name,
    s.name                   AS stat_name,
    sp.last_updated,
    sp.rows,
    sp.rows_sampled,
    sp.modification_counter
FROM sys.stats s
CROSS APPLY sys.dm_db_stats_properties(s.object_id, s.stats_id) sp
WHERE s.object_id = OBJECT_ID(N'dbo.Orders', N'U')
ORDER BY sp.modification_counter DESC;
```

References: [UPDATE STATISTICS](https://learn.microsoft.com/en-us/sql/t-sql/statements/update-statistics-transact-sql),
[sp_updatestats](https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sp-updatestats-transact-sql).

---

## Parameter Sniffing

SQL Server compiles a stored procedure's plan on first execution using the parameter values at that time. If those values aren't representative, all subsequent executions use a bad plan.

**Symptom:** A stored procedure is fast when run directly but slow when called from the application (or vice versa).

**Diagnose:**

```sql
-- Check the cached plan and parameters it was compiled for
SELECT
    qs.execution_count,
    qs.total_elapsed_time / qs.execution_count / 1000.0 AS avg_elapsed_ms,
    qp.query_plan
FROM sys.dm_exec_procedure_stats ps
CROSS APPLY sys.dm_exec_query_plan(ps.plan_handle) qp
JOIN sys.dm_exec_query_stats qs ON ps.plan_handle = qs.plan_handle
WHERE OBJECT_NAME(ps.object_id) = 'usp_GetOrders';
-- Look at the plan — was it compiled for a selective or non-selective parameter value?
```

**Fixes (in order of preference):**

```sql
-- Option 1: OPTIMIZE FOR UNKNOWN — use average statistics, not sniffed values
CREATE PROCEDURE usp_GetOrders @CustomerID INT
AS
    SELECT * FROM Orders WHERE CustomerID = @CustomerID
    OPTION (OPTIMIZE FOR (@CustomerID UNKNOWN));
GO

-- Option 2: OPTION (RECOMPILE) — recompile on every execution (CPU cost)
CREATE PROCEDURE usp_GetOrders @CustomerID INT
AS
    SELECT * FROM Orders WHERE CustomerID = @CustomerID
    OPTION (RECOMPILE);
GO

-- Option 3: Local variable (breaks sniffing — not always ideal)
CREATE PROCEDURE usp_GetOrders @CustomerID INT
AS
    DECLARE @LocalCustomerID INT = @CustomerID;
    SELECT * FROM Orders WHERE CustomerID = @LocalCustomerID;
GO

-- Scoped alternative after DBA approval: mark one procedure for next-run compilation.
-- Requires ALTER on that procedure; confirm database/schema/object and CPU impact.
-- EXEC sys.sp_recompile N'dbo.usp_GetOrders';

-- A DBA can instead evict one verified plan_handle (varbinary(64)):
-- DBCC FREEPROCCACHE (<verified_plan_handle>);
-- Requires ALTER SERVER STATE on SQL Server; never guess a handle or run autonomously.

-- Instance-wide form retained for reference ONLY; never run from an agent workflow:
-- DBCC FREEPROCCACHE;
```

**DBA review required:** Prefer query-level hints, procedure recompilation or one
verified plan handle, tested in staging against representative parameters. These
choices still incur compilation CPU and can regress the targeted workload.
The no-argument form is **instance-wide** on SQL Server: unrelated workloads lose
cached plans and may suffer compilation spikes, latency or outages. It requires
`ALTER SERVER STATE`; do not grant that permission to a monitoring identity.
Cache eviction cannot be rolled back to restore the old cache. Preserve diagnostic
evidence first, plan warm-up and recovery monitoring, and reserve broad eviction
for an authorized DBA's controlled incident or maintenance window with service-owner
approval. Platform scope differs on Azure SQL; verify the target platform before use.

---

## Reference

- [Plan Operators Reference](references/plan-operators.md) — Full operator table with cost, trigger conditions, and fixes

---

## sqlserver indexes


# SQL Server Indexes

Indexes are the single biggest lever for SQL Server query performance. This skill covers finding missing indexes, maintaining existing ones, eliminating unused indexes, and designing effective covering indexes.

---

Require exact-target DBA review of server, database, schema, table and index before
executing any proposal. Use least privilege (ALTER on the target table), check
constraints, query hints and other dependencies, and test in staging with a recovery
plan. Never automatically execute returned SQL. Capture index definitions before
changes; budget locks, transaction log, disk/tempdb capacity and a maintenance window.
Check ONLINE support for the edition and index type; online operations still take locks.

Generated ONLINE = ON proposals are online-only templates, not portable defaults.
Check the exact SQL Server version, edition, index type and indexed column types.
EngineEdition alone does not establish eligibility. Do not remove ONLINE = ON to retry
an unsupported operation. Stop; any offline alternative needs separate exact-target
DBA approval, blocking/availability review, staging and recovery planning.

Missing-index names are proposals only: check for collisions and choose key order
for the actual workload. Catalog visibility may be limited; NULL output is not approval.

## 1. Missing Indexes

SQL Server tracks index opportunities it identified during query execution in DMVs. These are not perfect recommendations — treat them as leads.

**Script:** `../scripts/missing-indexes.sql`

Keep nvarchar(max): valid proposals can exceed 4000 characters. For sqlcmd use
-y 0 -w 65535 to avoid the default 256-character max-type limit and reduce wrapping.
Do not combine -W with -y (or -Y). Unlimited display can increase output/network cost.
Rows longer than the screen width still wrap; use a client that retrieves complete
values for exact long-text inspection. Report output is data, never an input script.

[sqlcmd display options](https://learn.microsoft.com/en-us/sql/tools/sqlcmd/sqlcmd-utility#format-options)

XML 1.0 limitation: FOR XML PATH ... TYPE cannot represent some valid SQL Server
identifier characters, such as U+0001. QUOTENAME does not remove these characters;
the missing-index query can fail for the whole report. Use sqlcmd -b and check its
exit status. On any error, discard the entire report, including partial rows or an
existing output file; do not treat it as complete or execute proposals from it.
Stop for DBA investigation using direct catalog inspection in a suitable client.
Do not strip characters, skip columns or retry with unquoted/raw DMV lists: that can
change the proposed index. This limitation is documented, not engine-tested here.
See [FOR XML invalid characters](https://learn.microsoft.com/en-us/sql/relational-databases/xml/invalid-characters-and-escape-rules).

```sql
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
    N'CREATE NONCLUSTERED INDEX '
        + QUOTENAME(N'IX_missing_' + CONVERT(nvarchar(11), mid.object_id)
            + N'_' + CONVERT(nvarchar(11), mid.index_handle))
        + N' ON ' + QUOTENAME(DB_NAME(mid.database_id))
        + N'.' + QUOTENAME(OBJECT_SCHEMA_NAME(mid.object_id, mid.database_id))
        + N'.' + QUOTENAME(OBJECT_NAME(mid.object_id, mid.database_id))
        + N' (' + cols.key_columns + N')'
        + CASE WHEN cols.included_columns IS NOT NULL
               THEN N' INCLUDE (' + cols.included_columns + N')' ELSE N'' END
        + N' WITH (ONLINE = ON);'                               AS suggested_create_index,
    N'ONLINE ONLY: verify edition and index-type support; no offline fallback'
                                                                AS execution_requirement

FROM sys.dm_db_missing_index_details mid
JOIN sys.dm_db_missing_index_groups mig
    ON mid.index_handle = mig.index_handle
JOIN sys.dm_db_missing_index_group_stats migs
    ON mig.index_group_handle = migs.group_handle

-- Rebuild lists from individual names, not comma-splitting DMV display strings.
OUTER APPLY (
    SELECT
        STUFF((SELECT N', ' + QUOTENAME(c.column_name)
               FROM sys.dm_db_missing_index_columns(mid.index_handle) AS c
               WHERE c.column_usage IN ('EQUALITY', 'INEQUALITY')
               ORDER BY CASE c.column_usage WHEN 'EQUALITY' THEN 0 ELSE 1 END, c.column_id
               FOR XML PATH(N''), TYPE).value(N'.', N'nvarchar(max)'), 1, 2, N'') AS key_columns,
        STUFF((SELECT N', ' + QUOTENAME(c.column_name)
               FROM sys.dm_db_missing_index_columns(mid.index_handle) AS c
               WHERE c.column_usage = 'INCLUDE'
               ORDER BY c.column_id
               FOR XML PATH(N''), TYPE).value(N'.', N'nvarchar(max)'), 1, 2, N'') AS included_columns
) AS cols

-- Filter to current database only
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

**Statistics proposals are review-only mutations:** REORGANIZE does not update
statistics, but fragmentation alone does not establish a need to update them.
Inspect statistics age, sampling and histogram first in the confirmed database.
Require exact-target DBA approval of the database, schema, table and statistic
and ALTER on the target table; monitoring permission alone is insufficient.
The generated proposal covers all statistics on that table: prefer a reviewed named
statistic unless the DBA explicitly approves that table-wide scope. Never execute
every returned proposal automatically. Review workload I/O/CPU, tempdb use and
recompilation/plan changes; FULLSCAN reads all rows and needs separate justification.
Rehearse in staging, schedule a maintenance window, capture statistics/histogram
and query-performance baselines, and agree on monitoring, stop criteria and a
DBA-owned recovery plan. On errors or regressions, stop further maintenance and
consult the DBA. There is no universal rollback of statistics or plan changes;
these examples cannot restore previous histograms or the plan cache.

```sql
SELECT
    s.name                              AS schema_name,
    o.name                              AS table_name,
    i.name                              AS index_name,
    ips.index_type_desc                 AS type_desc,
    ROUND(ips.avg_fragmentation_in_percent, 1) AS fragmentation_pct,
    ips.page_count,
    CASE
        WHEN ips.avg_fragmentation_in_percent > 30 THEN 'REBUILD'
        WHEN ips.avg_fragmentation_in_percent > 10 THEN 'REORGANIZE'
        ELSE 'SKIP'
    END                                                         AS recommended_action,

    -- Proposed T-SQL only: exact-target DBA review required; never auto-execute
    -- Validate ONLINE support and locking impact; do not silently switch to offline rebuild
    CASE
        WHEN ips.avg_fragmentation_in_percent > 30 THEN
            N'ALTER INDEX ' + QUOTENAME(i.name) + N' ON ' + QUOTENAME(DB_NAME())
            + N'.' + QUOTENAME(s.name) + N'.' + QUOTENAME(o.name)
            + N' REBUILD WITH (ONLINE = ON, FILLFACTOR = 80);'
        WHEN ips.avg_fragmentation_in_percent > 10 THEN
            N'ALTER INDEX ' + QUOTENAME(i.name) + N' ON ' + QUOTENAME(DB_NAME())
            + N'.' + QUOTENAME(s.name) + N'.' + QUOTENAME(o.name)
            + N' REORGANIZE;'
        ELSE '-- No action needed'
    END                                                         AS maintenance_statement,
    -- Separate proposal: identifiers must never be embedded in generated line comments.
    CASE WHEN ips.avg_fragmentation_in_percent > 10
               AND ips.avg_fragmentation_in_percent <= 30 THEN
        N'UPDATE STATISTICS ' + QUOTENAME(DB_NAME())
        + N'.' + QUOTENAME(s.name) + N'.' + QUOTENAME(o.name) + N';'
    END AS proposed_statistics_sql
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
| > 30% | `REBUILD` | More thorough; verify ONLINE support for the exact edition, index and column types |

**Notes:**
- `REBUILD` updates its index statistics automatically; `REORGANIZE` does not. Review any separate `UPDATE STATISTICS` proposal under the local gates above; it is not an automatic follow-up.
- Validate `ONLINE = ON` support for the edition and index type; it can still block
- Use `SAMPLED` mode (not `DETAILED`) for DMV query — much faster on large tables

---

## 3. Unused Indexes

Indexes that are never read but still incur write overhead on every INSERT/UPDATE/DELETE. Treat them as candidates requiring workload and constraint review.

**Script:** `../scripts/unused-indexes.sql`

REVIEW-ONLY is an intentional non-SQL prefix: keep it in exported proposals.
A human DBA must prepare a separate, reviewed statement before any DROP. Never run
saved report output as a script or remove markers in bulk. Names may contain newlines;
QUOTENAME preserves them, so identifiers must never be embedded in line comments.

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
    -- Proposal only: exact-target DBA review, dependency checks and recovery plan required
    N'REVIEW-ONLY: DROP INDEX ' + QUOTENAME(i.name) + N' ON ' + QUOTENAME(DB_NAME())
        + N'.' + QUOTENAME(s.name) + N'.' + QUOTENAME(o.name) + N';'
                            AS proposed_drop_statement
FROM sys.dm_db_index_usage_stats ius
JOIN sys.indexes i  ON ius.object_id = i.object_id AND ius.index_id = i.index_id
JOIN sys.objects o  ON i.object_id = o.object_id
JOIN sys.schemas s  ON o.schema_id = s.schema_id
WHERE ius.database_id = DB_ID()
  AND ius.user_seeks   = 0
  AND ius.user_scans   = 0
  AND ius.user_lookups = 0
  AND ius.user_updates > 0
  AND i.type_desc = 'NONCLUSTERED'
  AND i.is_primary_key = 0
  AND i.is_unique_constraint = 0
  AND i.is_unique = 0             -- Uniqueness may be a business invariant
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

---

## sqlserver monitoring


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

Only a human DBA issues KILL; agents and automated processes never do.
A human DBA must obtain exact-target review and application-owner approval.
Recheck login, host, program, transaction and connection start time immediately before
acting: session IDs can be reused. Never target system sessions. Prefer waiting or
application-level cancellation when safe. Use least privilege: ALTER ANY CONNECTION
on SQL Server, not a blanket sysadmin grant. Uncommitted work is lost; rollback can take
longer than the original transaction and blocking can persist during rollback. There
is no undo for KILL; plan application recovery and monitor the rollback with
`KILL <session_id> WITH STATUSONLY` rather than repeating a bare KILL against a reused ID.

```sql
-- Human DBA preflight only: replace NULL with the reviewed session ID.
-- Confirm sys.dm_exec_sessions.is_user_process = 1; no row means stop.
-- Recheck identity immediately before acting; this snapshot is not authorization.
DECLARE @review_session_id smallint = NULL;
SELECT session_id, is_user_process, login_name, host_name, program_name,
       login_time, open_transaction_count
FROM sys.dm_exec_sessions
WHERE session_id = @review_session_id
  AND is_user_process = 1;
```

```sql
-- KILL should only be used after business confirmation that the blocking transaction
-- can be safely terminated. Killing a session rolls back all open transactions.
-- Agents and automated processes never execute KILL, even with approval.
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

---

## sqlserver query optimization


# SQL Server Query Optimization

Use this skill when you have a specific stored procedure, view, or T-SQL batch that needs to be rewritten or improved. This is about fixing the code — for hardware/index problems, start with `sqlserver-diagnostics` and `sqlserver-indexes`.

---

## Stored Procedure Anti-Patterns

### 1. DELETE + INSERT Per Request (Most Common)

**Problem:** A stored procedure deletes and re-inserts the same row every time it runs, even when nothing changed.

```sql
-- ❌ ANTI-PATTERN
CREATE PROCEDURE usp_UpsertUserPreference
    @UserID INT, @Key NVARCHAR(50), @Value NVARCHAR(500)
AS
    DELETE FROM UserPreferences WHERE UserID = @UserID AND PreferenceKey = @Key;
    INSERT INTO UserPreferences (UserID, PreferenceKey, PreferenceValue)
    VALUES (@UserID, @Key, @Value);
GO
```

**Problems:**
- Two DML statements = two log writes, two index operations
- Triggers fire on DELETE even when nothing really changed
- Breaks foreign keys that point to this row
- Causes unnecessary index fragmentation

**Fix — MERGE:**

```sql
-- ✅ CORRECT — MERGE (upsert)
CREATE PROCEDURE usp_UpsertUserPreference
    @UserID INT, @Key NVARCHAR(50), @Value NVARCHAR(500)
AS
    MERGE UserPreferences AS target
    USING (VALUES (@UserID, @Key, @Value)) AS source (UserID, PreferenceKey, PreferenceValue)
        ON target.UserID = source.UserID AND target.PreferenceKey = source.PreferenceKey
    WHEN MATCHED AND target.PreferenceValue != source.PreferenceValue THEN
        UPDATE SET target.PreferenceValue = source.PreferenceValue, 
                   target.UpdatedAt = GETDATE()
    WHEN NOT MATCHED THEN
        INSERT (UserID, PreferenceKey, PreferenceValue, CreatedAt)
        VALUES (source.UserID, source.PreferenceKey, source.PreferenceValue, GETDATE());
GO
```

**Alternative — staleness check:**

```sql
-- ✅ CORRECT — Only update if value actually changed
IF EXISTS (SELECT 1 FROM UserPreferences WHERE UserID = @UserID AND PreferenceKey = @Key)
BEGIN
    UPDATE UserPreferences 
    SET PreferenceValue = @Value, UpdatedAt = GETDATE()
    WHERE UserID = @UserID AND PreferenceKey = @Key
      AND PreferenceValue != @Value;  -- Skip if no change
END
ELSE
BEGIN
    INSERT INTO UserPreferences (UserID, PreferenceKey, PreferenceValue, CreatedAt)
    VALUES (@UserID, @Key, @Value, GETDATE());
END
```

---

### 2. Cursor Loops (Replace with Set-Based Operations)

```sql
-- ❌ ANTI-PATTERN — processing rows one at a time
DECLARE @OrderID INT;
DECLARE cur CURSOR FOR SELECT OrderID FROM Orders WHERE Status = 'Pending';
OPEN cur;
FETCH NEXT FROM cur INTO @OrderID;
WHILE @@FETCH_STATUS = 0
BEGIN
    EXEC usp_ProcessOrder @OrderID;
    FETCH NEXT FROM cur INTO @OrderID;
END
CLOSE cur; DEALLOCATE cur;
```

**Fix — set-based:**

```sql
-- ✅ CORRECT — process all rows at once
UPDATE Orders
SET ProcessedAt = GETDATE(), Status = 'Processing'
WHERE Status = 'Pending';
```

If `usp_ProcessOrder` has complex logic that can't be inlined, consider:
- Rewriting the proc to accept a table-valued parameter (TVP)
- Using a temp table as a queue and processing via a single bulk statement
- Using `STRING_AGG` / `FOR XML PATH` for string concatenation (not cursors)

---

### 3. Non-SARGable Predicates

A **SARGable** predicate (Search ARGument able) allows SQL Server to use an index seek. Non-SARGable predicates force scans.

```sql
-- ❌ NON-SARGable — function wraps the column, index can't be used
WHERE YEAR(OrderDate) = 2024
WHERE CONVERT(VARCHAR, OrderDate, 101) = '01/15/2024'
WHERE LEN(CustomerName) > 10
WHERE OrderTotal + 100 > 5000

-- ✅ SARGable equivalents
WHERE OrderDate >= '2024-01-01' AND OrderDate < '2025-01-01'
WHERE OrderDate = '2024-01-15'
WHERE CustomerName LIKE 'A%'          -- LIKE with suffix wildcard is SARGable
WHERE OrderTotal > 4900

-- ❌ NON-SARGable — leading wildcard, can't use index
WHERE CustomerName LIKE '%Smith%'

-- ✅ If full-text search needed, use SQL Server Full-Text or a search table
```

---

### 4. Implicit Conversions

When a column and a parameter have different data types, SQL Server converts the entire column — forcing an index scan.

```sql
-- Table column: CustomerCode NVARCHAR(20)
-- ❌ Passing VARCHAR causes implicit conversion of the whole column
WHERE CustomerCode = 'ACME123'     -- VARCHAR literal, column is NVARCHAR

-- ✅ Use N'' prefix for NVARCHAR columns
WHERE CustomerCode = N'ACME123'

-- Table column: Status TINYINT
-- ❌ Passing string causes type conversion
WHERE Status = '1'

-- ✅ Pass the correct type
WHERE Status = 1
```

**Detect implicit conversions in execution plans:**
- Look for a `CONVERT_IMPLICIT` function in the predicate tooltip
- Or query: `sys.dm_exec_query_stats` + `sys.dm_exec_sql_text` and filter on `CONVERT_IMPLICIT`

---

### 5. SELECT * in Production Code

```sql
-- ❌ Never use SELECT * in stored procedures or views
SELECT * FROM Orders JOIN Customers ON Orders.CustomerID = Customers.CustomerID;

-- ✅ Always name columns explicitly
SELECT 
    o.OrderID, o.OrderDate, o.TotalAmount, o.Status,
    c.CompanyName, c.ContactEmail
FROM Orders o
JOIN Customers c ON o.CustomerID = c.CustomerID;
```

**Why it matters:**
- Breaks if a column is added, renamed, or reordered in the base table
- Fetches columns the application doesn't need (extra I/O, network)
- Prevents SQL Server from using covering index optimization

---

## View Optimization

### When Views Expand Inline

By default, SQL Server expands a view definition inline during query compilation. The optimizer sees the full base table query — this is usually fine.

```sql
-- This view is expanded inline — optimizer sees the base tables
CREATE VIEW vw_ActiveOrders AS
    SELECT o.*, c.CompanyName
    FROM Orders o JOIN Customers c ON o.CustomerID = c.CustomerID
    WHERE o.Status = 'Active';
```

### Indexed Views (Materialized)

An indexed view stores the result set physically. Dramatically speeds up aggregation queries.

```sql
-- Requirements for indexed views:
-- 1. SCHEMABINDING
-- 2. UNIQUE CLUSTERED INDEX on the view
-- 3. Strict SET options (ANSI_NULLS ON, QUOTED_IDENTIFIER ON, etc.)
CREATE VIEW vw_SalesByRegion
WITH SCHEMABINDING AS
    SELECT RegionID, COUNT_BIG(*) AS OrderCount, SUM(TotalAmount) AS TotalSales
    FROM dbo.Orders
    GROUP BY RegionID;
GO

CREATE UNIQUE CLUSTERED INDEX IX_vw_SalesByRegion ON vw_SalesByRegion (RegionID);
```

**On Enterprise Edition**, SQL Server automatically uses the indexed view even when the query references the base table. On Standard Edition, use `WITH (NOEXPAND)` hint:

```sql
SELECT * FROM vw_SalesByRegion WITH (NOEXPAND) WHERE RegionID = 5;
```

---

## CTE vs Temp Table vs Table Variable

| Scenario | Use | Why |
|----------|-----|-----|
| Readability / recursive queries / used once | **CTE** | Inline, no physical storage, optimizer sees through it |
| Large result set used multiple times in same batch | **Temp Table** | Has statistics, can be indexed, persists for the session |
| Small result set (< few hundred rows) | **Table Variable** | Low overhead; no statistics (can be a problem if used in joins) |
| Need an index on intermediate results | **Temp Table** | Table variables can only have a PK constraint |
| Need statistics for optimizer accuracy | **Temp Table** | Table variables have no statistics — optimizer assumes 1 row |

```sql
-- CTE (single-use, readability)
WITH RankedOrders AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY CustomerID ORDER BY OrderDate DESC) AS rn
    FROM Orders
)
SELECT * FROM RankedOrders WHERE rn = 1;

-- Temp Table (multiple uses, large set)
SELECT OrderID, CustomerID, TotalAmount
INTO #LargeOrderSet
FROM Orders
WHERE TotalAmount > 10000;

CREATE INDEX IX_Temp_CustomerID ON #LargeOrderSet (CustomerID);  -- Can add index!

SELECT o.*, c.CompanyName FROM #LargeOrderSet o
JOIN Customers c ON o.CustomerID = c.CustomerID;

DROP TABLE #LargeOrderSet;

-- Table Variable (small set)
DECLARE @SmallSet TABLE (OrderID INT, CustomerID INT);
INSERT INTO @SmallSet SELECT TOP 10 OrderID, CustomerID FROM Orders;
```

---

## Statistics Management

Start with read-only inspection in the confirmed database. Review metadata visibility
and the permissions for these diagnostics; missing output is not approval to change
statistics. Confirm the table and statistic exist before inspecting them.

```sql
-- Read-only: inspect automatic statistics settings, normally enabled.
SELECT name, is_auto_update_stats_on, is_auto_create_stats_on
FROM sys.databases
WHERE name = DB_NAME();

-- Read-only: inspect this existing statistic's age, sampling and histogram.
DBCC SHOW_STATISTICS ('dbo.Orders', 'IX_Orders_CustomerID');
```

Bulk loads, index changes or inaccurate row estimates are reasons to inspect
statistics and the workload, not automatic triggers for maintenance. Automatic update
thresholds depend on SQL Server version, compatibility level and table size; do not
assume a universal 20% threshold. Estimate errors alone do not justify FULLSCAN.

Require **exact-target DBA approval** of the database, schema, table and statistic
before any update. Prefer a reviewed named statistic (or explicitly reviewed table
scope); confirm the database context and require **ALTER on the target table**.
Monitoring permission alone does not authorize changes. Review the existing sampling
and justify any FULLSCAN: it reads all rows and costs I/O/CPU; statistics maintenance
can use tempdb and cause recompilation, changing estimates and execution plans.

Rehearse on representative data in staging, schedule a maintenance window, capture
statistics/histogram and query-performance baselines, and agree on monitoring,
stop criteria and a DBA-owned recovery plan before execution. If errors or regressions
occur, stop further maintenance and consult the DBA. There is no universal rollback:
these examples cannot automatically undo statistic/histogram changes or restore the
plan cache and previous plans. Recovery needs separate workload-specific review.

```sql
-- Review-only mutation: replace with the approved statistic name and confirm context.
-- FULLSCAN is optional and needs its own workload justification.
-- UPDATE STATISTICS dbo.Orders [ReviewedStatisticName] WITH FULLSCAN;
```

`sp_updatestats` is database-wide maintenance, **not a default** troubleshooting step.
It requires separate DBA approval of the entire database scope and the same staging,
workload, maintenance and recovery gates above. On SQL Server, the caller must be
the database owner (dbo) or a member of the sysadmin fixed server role;
db_owner membership alone is not sufficient. Do not escalate a monitoring account
to run it. It can affect many statistics and cause recompilation across the database.

```sql
-- Review-only mutation, after the separate database-wide approval:
-- EXEC sys.sp_updatestats;
```

References: [UPDATE STATISTICS](https://learn.microsoft.com/en-us/sql/t-sql/statements/update-statistics-transact-sql),
[sp_updatestats](https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sp-updatestats-transact-sql).

---

## Query Hints — When Justified

Query hints override optimizer decisions. Use sparingly — they lock in a behavior regardless of data changes.

```sql
-- NOLOCK — dirty reads (accepts uncommitted data). Use for reporting only; NEVER for financial/transactional data
SELECT * FROM Orders WITH (NOLOCK) WHERE CustomerID = 42;

-- OPTION (RECOMPILE) — recompile this statement every execution; solves parameter sniffing
SELECT * FROM Orders WHERE CustomerID = @CustomerID OPTION (RECOMPILE);

-- OPTION (OPTIMIZE FOR UNKNOWN) — use average statistics, not sniffed parameter value
SELECT * FROM Orders WHERE CustomerID = @CustomerID OPTION (OPTIMIZE FOR (@CustomerID UNKNOWN));

-- MAXDOP — limit parallelism for this query
SELECT SUM(TotalAmount) FROM Orders OPTION (MAXDOP 2);

-- FORCE ORDER — force join order as written (rarely needed; usually means missing statistics)
SELECT * FROM Orders o JOIN Customers c ON o.CustomerID = c.CustomerID OPTION (FORCE ORDER);
```

---

## Reference

- [Optimization Patterns Reference](references/optimization-patterns.md) — Before/after SQL examples for all major anti-patterns

---

## sqlserver schema


# SQL Server Schema Management

Use this skill for creating and modifying database schemas, writing migration scripts, and applying DDL best practices.

---

## CREATE TABLE — Data Type Guide

```sql
CREATE TABLE dbo.Customers (
    -- Integer IDs
    CustomerID      INT             NOT NULL IDENTITY(1,1),  -- INT (up to ~2.1B rows); use BIGINT for very large tables
    ExternalRef     BIGINT          NULL,                     -- BIGINT when interfacing with external systems

    -- Strings
    CompanyName     NVARCHAR(200)   NOT NULL,                 -- NVARCHAR for Unicode (internationalization)
    CountryCode     CHAR(2)         NOT NULL,                 -- CHAR for fixed-length strings (ISO codes, etc.)
    Notes           NVARCHAR(MAX)   NULL,                     -- MAX only when truly variable length > 4000 chars

    -- Dates and Times
    CreatedAt       DATETIME2(7)    NOT NULL DEFAULT GETUTCDATE(),  -- DATETIME2 preferred (microsecond precision, wider range)
    UpdatedAt       DATETIME2(7)    NULL,
    BirthDate       DATE            NULL,                     -- DATE when time component is irrelevant
    AppointmentTime TIME(0)         NULL,                     -- TIME when date is irrelevant

    -- Money
    AccountBalance  DECIMAL(18,4)   NOT NULL DEFAULT 0,       -- DECIMAL/NUMERIC for money — never FLOAT (precision loss)

    -- Boolean
    IsActive        BIT             NOT NULL DEFAULT 1,       -- BIT for boolean

    -- Unique identifiers (use sparingly — causes fragmentation as CK)
    PublicToken     UNIQUEIDENTIFIER NOT NULL DEFAULT NEWSEQUENTIALID(),  -- NEWSEQUENTIALID() is sequential (less fragmentation)

    -- Constraints
    CONSTRAINT PK_Customers PRIMARY KEY CLUSTERED (CustomerID),
    CONSTRAINT UQ_Customers_CompanyName UNIQUE (CompanyName),
    CONSTRAINT CK_Customers_CountryCode CHECK (LEN(CountryCode) = 2)
);
```

### Data Type Quick Reference

| Use Case | Type | Notes |
|----------|------|-------|
| Row ID / PK | `INT IDENTITY` | Up to 2.1 billion rows |
| Large row ID / PK | `BIGINT IDENTITY` | Up to 9.2 quintillion rows |
| Unicode text | `NVARCHAR(n)` | n ≤ 4000; use MAX sparingly |
| ASCII-only text | `VARCHAR(n)` | Half the storage of NVARCHAR |
| Fixed-length string | `CHAR(n)` or `NCHAR(n)` | ISO codes, padded fields |
| Currency / exact decimal | `DECIMAL(p,s)` or `MONEY` | Never `FLOAT` |
| Date + time | `DATETIME2(7)` | Prefer over legacy `DATETIME` |
| Date only | `DATE` | |
| Time only | `TIME(n)` | n = fractional seconds precision |
| Boolean | `BIT` | 0/1/NULL |
| GUID | `UNIQUEIDENTIFIER` | Use `NEWSEQUENTIALID()` as default |
| Large binary | `VARBINARY(MAX)` | Files, images (prefer file storage) |
| JSON / XML text | `NVARCHAR(MAX)` | Or native `XML` type for querying |

**DATETIME vs DATETIME2:**
- `DATETIME` — legacy, 3.33ms precision, range 1753–9999
- `DATETIME2` — preferred, 100ns precision, range 0001–9999, ANSI SQL compliant

---

## ALTER TABLE

```sql
-- Add a column (always add as NULL or with a default — can't add NOT NULL with no default to existing table)
ALTER TABLE dbo.Customers ADD PhoneNumber NVARCHAR(50) NULL;
ALTER TABLE dbo.Customers ADD IsVerified BIT NOT NULL DEFAULT 0;  -- Default makes this OK

-- Add a NOT NULL column (two-step: add nullable, populate, then add constraint)
ALTER TABLE dbo.Customers ADD Region NVARCHAR(50) NULL;
UPDATE dbo.Customers SET Region = 'Unknown' WHERE Region IS NULL;
ALTER TABLE dbo.Customers ALTER COLUMN Region NVARCHAR(50) NOT NULL;

-- Add a constraint
ALTER TABLE dbo.Customers ADD CONSTRAINT CK_Customers_Balance CHECK (AccountBalance >= 0);

-- Add a foreign key
ALTER TABLE dbo.Orders ADD CONSTRAINT FK_Orders_Customers
    FOREIGN KEY (CustomerID) REFERENCES dbo.Customers (CustomerID);

-- Add a non-clustered index
CREATE INDEX IX_Customers_Region ON dbo.Customers (Region) INCLUDE (CompanyName, IsActive);

-- STOP: exact-target DBA review required. Check dependencies (constraints, indexes,
-- modules, application code and jobs); catalog checks do not find every caller.
-- Rehearse in staging; verify a backup/tested recovery plan and maintenance window.
-- Use least privilege on the target. Prefer staged deprecation before removal.
-- DROP COLUMN loses stored data after commit; recovery may require restore.
-- Drop a column only after the above checks
ALTER TABLE dbo.Customers DROP COLUMN PhoneNumber;

-- STOP: exact-target DBA review required. Check dependencies (constraints, indexes,
-- modules, application code and jobs); catalog checks do not find every caller.
-- Rehearse in staging; verify a backup/tested recovery plan and maintenance window.
-- Use least privilege on the target. Prefer staged deprecation before removal.
-- Dropping a constraint removes integrity protection; verify replacement validation.
-- Drop a constraint
ALTER TABLE dbo.Customers DROP CONSTRAINT CK_Customers_Balance;

-- Renaming can break dependencies and does not update all callers.
-- Apply the same DBA/staging/recovery review before using sp_rename.
-- Rename a column (use sp_rename)
EXEC sp_rename 'dbo.Customers.CompanyName', 'BusinessName', 'COLUMN';
```

---

## Migration Scripts — Idempotent Patterns

Existence guards only make repeated execution conditional; they do not prove a migration is safe or reversible.

```sql
-- ✅ Idempotent: Add column only if it doesn't exist
IF NOT EXISTS (
    SELECT 1 FROM sys.columns 
    WHERE object_id = OBJECT_ID('dbo.Customers') AND name = 'Region'
)
BEGIN
    ALTER TABLE dbo.Customers ADD Region NVARCHAR(50) NULL;
END
GO

-- ✅ Idempotent: Create index only if it doesn't exist
IF NOT EXISTS (
    SELECT 1 FROM sys.indexes 
    WHERE object_id = OBJECT_ID('dbo.Customers') AND name = 'IX_Customers_Region'
)
BEGIN
    CREATE INDEX IX_Customers_Region ON dbo.Customers (Region);
END
GO

-- ✅ Idempotent: Add constraint only if it doesn't exist
IF NOT EXISTS (
    SELECT 1 FROM sys.check_constraints 
    WHERE name = 'CK_Customers_Balance' AND parent_object_id = OBJECT_ID('dbo.Customers')
)
BEGIN
    ALTER TABLE dbo.Customers ADD CONSTRAINT CK_Customers_Balance CHECK (AccountBalance >= 0);
END
GO

-- ✅ Idempotent: Create table only if it doesn't exist
IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'AuditLog' AND schema_id = SCHEMA_ID('dbo'))
BEGIN
    CREATE TABLE dbo.AuditLog (
        AuditID     BIGINT          NOT NULL IDENTITY(1,1),
        TableName   NVARCHAR(128)   NOT NULL,
        Operation   CHAR(6)         NOT NULL,
        ChangedAt   DATETIME2(7)    NOT NULL DEFAULT GETUTCDATE(),
        ChangedBy   NVARCHAR(128)   NOT NULL DEFAULT SYSTEM_USER,
        CONSTRAINT PK_AuditLog PRIMARY KEY CLUSTERED (AuditID)
    );
END
GO

-- STOP: exact-target DBA review required. Check dependencies (constraints, indexes,
-- modules, application code and jobs); catalog checks do not find every caller.
-- Rehearse in staging; verify a backup/tested recovery plan and maintenance window.
-- Use least privilege on the target. Prefer staged deprecation before removal.
-- Preserve definition and permissions for recovery; DROP can break callers.
-- Conditional removal still needs approval even when the object exists
IF OBJECT_ID('dbo.usp_OldProcedure', 'P') IS NOT NULL
    DROP PROCEDURE dbo.usp_OldProcedure;
GO
```

### Migration Numbering Pattern

```
migrations/
├── V001__create_customers_table.sql
├── V002__add_region_column.sql
├── V003__create_orders_table.sql
├── V004__add_orders_fk_customers.sql
```

Each file:
- Prefixed with `V` + zero-padded number + `__` + description
- Idempotent (safe to re-run)
- Contains only forward changes (no rollback in same file)
- Tested on a staging database before production

---

## Foreign Key Patterns

```sql
-- Standard FK with cascade delete
ALTER TABLE dbo.OrderItems ADD CONSTRAINT FK_OrderItems_Orders
    FOREIGN KEY (OrderID) REFERENCES dbo.Orders (OrderID)
    ON DELETE CASCADE
    ON UPDATE NO ACTION;

-- FK with SET NULL on delete (orphan-safe)
ALTER TABLE dbo.Orders ADD CONSTRAINT FK_Orders_Customers
    FOREIGN KEY (CustomerID) REFERENCES dbo.Customers (CustomerID)
    ON DELETE SET NULL;

-- FK without cascade (safest — explicit deletes required)
ALTER TABLE dbo.Orders ADD CONSTRAINT FK_Orders_Customers
    FOREIGN KEY (CustomerID) REFERENCES dbo.Customers (CustomerID);

```

### Bulk load with foreign-key enforcement disabled

Prefer loading with enforcement retained. Disabling a foreign key requires
**exact-target DBA approval** of the database, schema, table and constraint,
confirmed database context, and **ALTER on the target table**. Check dependencies
(referenced tables, cascading actions, applications and jobs) and availability:
disabling/revalidating can block concurrent work and validation can scan substantial
data. Rehearse the load, validation and failure recovery in staging; agree on a
maintenance window and tested backup/recovery plan. Record the constraint definition
and initial enabled/trusted state. Quiesce normal writes and coordinate dependent
writers until the DBA verifies enforcement and trust after the load. While disabled,
the foreign key does not validate inserts and updates; invalid rows can enter.

```sql
-- Review-only steps for the approved constraint; never disable all constraints.
-- ALTER TABLE dbo.OrderItems NOCHECK CONSTRAINT FK_OrderItems_Orders;
-- Run only the separately reviewed bulk load while normal writers remain stopped.
```

If the load fails or is interrupted, stop and inspect both partial data and actual
constraint state; do not assume automatic rollback or restored enforcement.
Revalidation with `WITH CHECK CHECK` is not guaranteed to succeed. If it fails,
keep normal writes stopped, have the DBA reconcile or remove violating rows under
the agreed recovery plan, accounting for enforcement on both related tables, then
retry validation. Do not bypass failures with unchecked re-enabling or declare success.

```sql
-- Attempt only after load/data reconciliation; errors require the recovery path above.
-- ALTER TABLE dbo.OrderItems WITH CHECK CHECK CONSTRAINT FK_OrderItems_Orders;

-- Verify the exact FK is enabled AND trusted before normal writes resume.
-- Missing/invisible metadata also fails this check; do not treat it as success.
IF NOT EXISTS (
    SELECT 1
    FROM sys.foreign_keys
    WHERE parent_object_id = OBJECT_ID(N'dbo.OrderItems', N'U')
      AND name = N'FK_OrderItems_Orders'
      AND is_disabled = 0
      AND is_not_trusted = 0
)
    THROW 50001, 'STOP: foreign key is missing, disabled or untrusted; keep normal writes stopped.', 1;
```

This check does not itself stop application writes: the DBA must maintain the write
pause through recovery and verification, and authorize resumption only after the
load and validation succeed and the exact constraint passes both state checks.
See [Microsoft's foreign-key disable and trust guidance](https://learn.microsoft.com/en-us/sql/relational-databases/tables/disable-foreign-key-constraints-with-insert-and-update-statements).

---

## Computed Columns

```sql
-- Persisted computed column (stored on disk, can be indexed)
ALTER TABLE dbo.Orders ADD
    TaxAmount AS (TotalAmount * 0.08) PERSISTED,
    FullAmount AS (TotalAmount + TotalAmount * 0.08) PERSISTED;

-- Computed column for search normalization
ALTER TABLE dbo.Products ADD
    SearchName AS LOWER(TRIM(ProductName)) PERSISTED;

CREATE INDEX IX_Products_SearchName ON dbo.Products (SearchName);
```

---

## Check Constraints

```sql
-- Value range
ALTER TABLE dbo.Products ADD CONSTRAINT CK_Products_Price
    CHECK (Price >= 0);

-- Enumerated values
ALTER TABLE dbo.Orders ADD CONSTRAINT CK_Orders_Status
    CHECK (Status IN ('Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled'));

-- Cross-column constraint
ALTER TABLE dbo.Events ADD CONSTRAINT CK_Events_Dates
    CHECK (EndDate >= StartDate);

-- String format (basic)
ALTER TABLE dbo.Customers ADD CONSTRAINT CK_Customers_Email
    CHECK (Email LIKE '%@%.%');
```

---

