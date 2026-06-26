```
 ____   ___  _         ____                               ____  _    _ _ _     
/ ___| / _ \| |       / ___|  ___ _ ____   _____ _ __    / ___|| | _(_) | |___ 
\___ \| | | | |   ____\___ \ / _ \ '__\ \ / / _ \ '__|___\___ \| |/ / | | / __|
 ___) | |_| | |__|_____|__) |  __/ |   \ V /  __/ | |_____|__) |   <| | | \__ \
|____/ \__\_\_____|   |____/ \___|_|    \_/ \___|_|      |____/|_|\_\_|_|_|___/
```

# sql-server-skills

**Comprehensive SQL Server skill for AI agents** — performance diagnostics, DMV queries, execution plan interpretation, index analysis, query optimization, schema management, backup/restore, and monitoring.

Built for DBAs and developers who need real answers, not syntax references.

---

## Why This Exists

See [Compared to Existing Marketplace Skills](#compared-to-existing-marketplace-skills) below.

---

## What's Included

### 7 Sub-Skills

| Sub-Skill | Description |
|-----------|-------------|
| [`sqlserver-diagnostics`](./sqlserver-diagnostics/SKILL.md) | Identify bottlenecks via DMV queries — wait stats, slow queries, active requests, performance counters |
| [`sqlserver-indexes`](./sqlserver-indexes/SKILL.md) | Missing indexes, fragmentation analysis, unused index detection, covering index design |
| [`sqlserver-execution-plans`](./sqlserver-execution-plans/SKILL.md) | Capture and read execution plans, identify bad operators, diagnose parameter sniffing |
| [`sqlserver-query-optimization`](./sqlserver-query-optimization/SKILL.md) | Fix stored procedures and views — anti-patterns, cursor replacement, CTE vs temp table |
| [`sqlserver-schema`](./sqlserver-schema/SKILL.md) | DDL patterns, data type guidance, idempotent migrations, constraints |
| [`sqlserver-backup`](./sqlserver-backup/SKILL.md) | Full/differential/log backups, restore procedures, backup history queries |
| [`sqlserver-monitoring`](./sqlserver-monitoring/SKILL.md) | SQL Agent jobs, error log, blocking chains, deadlocks, long-running transactions |

### 7 SQL Scripts

| Script | Purpose |
|--------|---------|
| [`scripts/top-slow-queries.sql`](./scripts/top-slow-queries.sql) | Top 25 queries by avg elapsed time since last restart (with avg logical reads, CPU) |
| [`scripts/wait-stats.sql`](./scripts/wait-stats.sql) | Wait stats analysis with inline interpretation guide per wait type |
| [`scripts/missing-indexes.sql`](./scripts/missing-indexes.sql) | Missing index recommendations with generated `CREATE INDEX` statements and impact scores |
| [`scripts/index-fragmentation.sql`](./scripts/index-fragmentation.sql) | Index fragmentation analysis with REBUILD vs REORGANIZE recommendations |
| [`scripts/unused-indexes.sql`](./scripts/unused-indexes.sql) | Indexes with zero reads but non-zero write cost — candidates for removal |
| [`scripts/active-queries.sql`](./scripts/active-queries.sql) | Currently running queries with wait info, blocking, and resource consumption |
| [`scripts/blocking-analysis.sql`](./scripts/blocking-analysis.sql) | Three-part blocking investigation: chains, head blockers, lock details |

### Reference Docs

- [`sqlserver-indexes/references/index-strategies.md`](./sqlserver-indexes/references/index-strategies.md) — Composite key ordering, filtered indexes, columnstore, maintenance scheduling
- [`sqlserver-execution-plans/references/plan-operators.md`](./sqlserver-execution-plans/references/plan-operators.md) — Full operator reference table with cost profiles and fix patterns
- [`sqlserver-query-optimization/references/optimization-patterns.md`](./sqlserver-query-optimization/references/optimization-patterns.md) — Before/after SQL examples for 12 major anti-patterns

---

## Requirements

- **`sqlcmd`** — [Download from Microsoft](https://learn.microsoft.com/en-us/sql/tools/sqlcmd/sqlcmd-utility)
- **SQL Server 2016+** (compatibility level 130+)
- **`VIEW SERVER STATE`** permission for most DMV queries
- **`sysadmin`** or `db_owner` for some backup/restore operations

---

## Installation

### Option 1: ClawHub (when published)

```bash
clawhub install sql-server-skills
```

### Option 2: Manual install

```bash
cd ~/.agents/skills   # or your skills directory
git clone https://github.com/vince-winkintel/sql-server-skills.git
```

Then reference in your agent's `SKILL.md` search path.

### Option 3: Claude.ai (Organization Skills)

Claude.ai requires a zip containing exactly one `SKILL.md`. Download the pre-built `claude-skill.zip` from the [latest release](https://github.com/vince-winkintel/sql-server-skills/releases/latest) and upload it in your organization's **Settings → Custom Skills**.

The zip contains a single merged `SKILL.md` combining all 7 sub-skills into one comprehensive SQL Server reference.

**Build it yourself:**

```bash
bash scripts/build-claude-skill.sh
# Output: ./claude-skill.zip
```

---

## Quick Start

```bash
# Connect and run a script
sqlcmd -S "$SQL_SERVER" -U "$SQL_USER" -P "$SQL_PASSWORD" -d master -i scripts/wait-stats.sql

# Run with CSV output to a file
sqlcmd -S "$SQL_SERVER" -U "$SQL_USER" -P "$SQL_PASSWORD" -d master \
  -i scripts/top-slow-queries.sql -o results.txt -s "," -W
```

---

## Usage Examples — Prompts That Trigger This Skill

These are the kinds of prompts that should route to this skill:

- *"SQL Server is slow, help me find the bottleneck"*
- *"What's the wait stats analysis for my SQL Server?"*
- *"Find missing indexes in my database"*
- *"Why is this T-SQL query slow? Here's the execution plan..."*
- *"Rewrite this stored procedure — it's using a cursor loop"*
- *"How do I rebuild fragmented indexes?"*
- *"Check SQL Agent job history for failed jobs"*
- *"Is there blocking on my SQL Server right now?"*
- *"Help me write an idempotent migration script"*
- *"How do I backup and restore this database?"*

---

## Compared to Existing Marketplace Skills

Before building this skill, we surveyed the existing SQL Server-related offerings in the agent skill marketplaces. Here's what we found:

| Skill | Marketplace | Coverage | Gap |
|-------|-------------|----------|-----|
| [tsql-functions](https://skills.sh/josiahsiegel/claude-plugin-marketplace/tsql-functions) | skills.sh | T-SQL function syntax reference (string, date, window, JSON functions) | Syntax only — no diagnostics, no performance analysis, no DMVs |
| [sql-server-toolkit](https://clawhub.com/skills/sql-server-toolkit) | ClawHub | Basic sqlcmd connection, one 10-line DMV query, backup/restore skeleton | Too thin — SKILL.md is ~20 lines, no real performance guidance |
| [sql-pro](https://clawhub.com/skills/sql-pro) | ClawHub | Generic SQL query optimization guidance | Not SQL Server-specific, no DMV awareness, no execution plans |
| [sql-query-optimizer](https://clawhub.com/skills/sql-query-optimizer) | ClawHub | Generic query analysis and index recommendations | Platform-agnostic, no SQL Server-specific tooling |

**None of these cover what DBAs and developers actually need day-to-day**: DMV-based diagnostics, wait stats interpretation, execution plan reading, index maintenance, blocking analysis, or stored procedure optimization patterns.

This skill fills that gap.

---

## Security

See [SECURITY.md](./SECURITY.md) for security considerations when using these scripts in production environments.

---

## License

MIT — see [LICENSE](./LICENSE)
