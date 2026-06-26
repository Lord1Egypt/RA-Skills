---
name: sqlserver-backup
description: SQL Server backup and restore operations — full, differential, and log backups, RESTORE with NORECOVERY/RECOVERY, RESTORE VERIFYONLY, backup history queries, and recovery model guidance.
---

# SQL Server Backup & Restore

Use this skill for database backup strategies, restore procedures, and verifying backup integrity.

---

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

-- Change recovery model
ALTER DATABASE MyDatabase SET RECOVERY FULL;
ALTER DATABASE MyDatabase SET RECOVERY SIMPLE;
```

⚠️ **Switching to FULL recovery model:** You must take a full backup immediately after switching — until you do, the log cannot be backed up and will grow unbounded.

---

## BACKUP DATABASE

### Full Backup

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

Verify a backup file is readable without performing the restore:

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
- Use `WITH CHECKSUM` — detects media corruption at backup time, not restore time
