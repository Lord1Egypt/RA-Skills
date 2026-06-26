# Security Considerations

This document covers security best practices when deploying and using the `sql-server-skills` scripts in production SQL Server environments.

---

## Principle of Least Privilege

The scripts in this skill run as the authenticated SQL login. Grant only the minimum permissions required:

| Operation | Minimum Permission Required |
|-----------|---------------------------|
| DMV queries (wait stats, slow queries, active requests) | `VIEW SERVER STATE` |
| Missing index DMVs | `VIEW SERVER STATE` |
| Index fragmentation (`sys.dm_db_index_physical_stats`) | `VIEW DATABASE STATE` |
| Backup history (`msdb.dbo.backupset`) | `db_datareader` on `msdb` |
| SQL Agent job history | `SQLAgentReaderRole` on `msdb` |
| BACKUP DATABASE | `db_backupoperator` or `sysadmin` |
| RESTORE DATABASE | `sysadmin` (required for RESTORE) |
| ALTER INDEX (rebuild/reorganize) | `db_ddladmin` or `sysadmin` |

**Do not run these scripts as `sa` or a sysadmin login in production.** Create a dedicated monitoring login with only the permissions above.

```sql
-- Example: Create a least-privilege monitoring login
CREATE LOGIN sql_monitor WITH PASSWORD = '<strong_password>';
CREATE USER  sql_monitor FOR LOGIN sql_monitor;
GRANT VIEW SERVER STATE TO sql_monitor;
```

---

## Connection Strings — Never Store in Skill Files

Connection strings, passwords, and server names must **never** be stored inside skill files, scripts, or committed to version control.

**Bad:**
```bash
# Hardcoded in a script — never do this
sqlcmd -S prod-sql-01 -U sa -P MyPassword123 -d master -i wait-stats.sql
```

**Good — use environment variables:**
```bash
sqlcmd -S "$SQL_SERVER" -U "$SQL_USER" -P "$SQL_PASSWORD" -d master -i wait-stats.sql
```

**Good — use Windows Authentication (no password in command):**
```bash
sqlcmd -S prod-sql-01 -E -d master -i wait-stats.sql
```

Store credentials in:
- OS-level environment variables
- A secrets manager (Azure Key Vault, HashiCorp Vault, AWS Secrets Manager)
- A `.env` file that is `.gitignore`d and never committed

---

## The KILL Command

`blocking-analysis.sql` includes a commented-out `KILL` command for reference. **This script must never be executed by an AI agent autonomously.**

Rules for `KILL`:
1. Only a human DBA should issue `KILL` — never an automated process
2. Always confirm with the application owner that rolling back the session is safe
3. `KILL` rolls back all uncommitted work in the target session — this may take seconds to minutes depending on transaction size
4. Never kill system sessions (session_id ≤ 50)

---

## SQL Agent Job History

`sqlserver-monitoring/SKILL.md` queries `msdb.dbo.sysjobhistory`. Job step output messages may contain:

- SQL error text that reveals schema or data structure
- File paths from the server
- Connection strings or partial credentials (if a job step logs them)
- Business data (row counts, identifiers, error values)

Treat job history output as **potentially sensitive**. Do not log, export, or share it without reviewing the content first.

---

## Extended Events and Error Logs

`xp_readerrorlog` and deadlock graph queries from `system_health` extended events may surface:

- Failed login attempts (including attempted usernames)
- Internal error messages with object names and schema details
- IP addresses of connecting clients

These outputs should be treated as sensitive operational data.

---

## Read-Only DMV Queries

All diagnostic scripts in this skill are **read-only SELECT queries** (plus `EXEC xp_readerrorlog`). They do not modify any data.

The only scripts that modify the database are in `sqlserver-indexes/SKILL.md` (ALTER INDEX) and `sqlserver-schema/SKILL.md` (DDL). Those should be reviewed before execution.

---

## SQL Injection

These scripts use literal T-SQL — they do not accept user input as parameters. There is no SQL injection surface in the provided scripts themselves. However, if you build tooling that wraps these scripts and accepts server/database names from user input, sanitize those inputs before passing them to `sqlcmd`.
