# clawbot-sql-memory

> ⚠️ **ALPHA — Use at your own risk.** Functional and in active use, but API may change. We'll lock the API after 30 days of community feedback. Open issues freely — this improves with use.

SQL Server-based persistent memory for OpenClaw agents. Provides semantic memory, task queuing, activity logging, todo management, and hierarchical rollups (daily → weekly → monthly → yearly).

---

## ⚠️ DEPENDENCY PRIORITY

**This skill requires `sql-connector` to be installed first.**

```
sql-connector  ←  Install this FIRST
      ↓
sql-memory     ←  You are here
      ↓
sql-dreamer    ←  Install this LAST (optional — uses memories for dream analysis)
```

```bash
# Always install in this order:
clawhub install sql-connector   # transport layer — required
clawhub install sql-memory      # this skill
clawhub install sql-dreamer     # optional — dream/analysis layer
```

If `sql-connector` is not installed, this skill will fail at import with:
`ImportError: sql_connector.py not found. Install the sql-connector skill first.`

---

## Requirements

- SQL Server 2019+ (or Azure SQL, site4now, etc.)
- [clawbot-sql-connector](https://github.com/High-Falootin/clawbot-sql-connector) — install first
- `pymssql` and `python-dotenv`

## Step 1: Create the Schema

Before installing this skill, create the required tables in your SQL Server database. You can do this one of two ways:

### Option A — Run the setup script (recommended)

```bash
python3 setup_schema.py
```

This will connect using your `.env` credentials and create all tables automatically. Run it once before first use.

### Option B — Manual SQL (paste into SSMS, Azure Data Studio, or sqlcmd)

```sql
-- Run against your target database
CREATE SCHEMA memory;
GO

CREATE TABLE memory.Memories (
    id          UNIQUEIDENTIFIER PRIMARY KEY DEFAULT newid(),
    category    NVARCHAR(100)  NOT NULL,
    key         NVARCHAR(255)  NOT NULL,
    content     NVARCHAR(MAX)  NOT NULL,
    importance  INT            DEFAULT 3,
    tags        NVARCHAR(500)  DEFAULT '',
    status      NVARCHAR(50)   DEFAULT 'active',
    created_at  DATETIME2      DEFAULT GETUTCDATE(),
    updated_at  DATETIME2      DEFAULT GETUTCDATE()
);

CREATE TABLE memory.TaskQueue (
    id          UNIQUEIDENTIFIER PRIMARY KEY DEFAULT newid(),
    agent       NVARCHAR(100)  NOT NULL,
    task_type   NVARCHAR(100)  NOT NULL,
    payload     NVARCHAR(MAX)  DEFAULT '',
    priority    INT            DEFAULT 5,
    status      NVARCHAR(50)   DEFAULT 'pending',
    retries     INT            DEFAULT 0,
    model_hint  NVARCHAR(100)  DEFAULT '',
    created_at  DATETIME2      DEFAULT GETUTCDATE(),
    updated_at  DATETIME2      DEFAULT GETUTCDATE(),
    claimed_at  DATETIME2      NULL,
    completed_at DATETIME2     NULL,
    error       NVARCHAR(MAX)  DEFAULT ''
);

CREATE TABLE memory.ActivityLog (
    id          UNIQUEIDENTIFIER PRIMARY KEY DEFAULT newid(),
    event_type  NVARCHAR(100)  NOT NULL,
    agent       NVARCHAR(100)  DEFAULT '',
    description NVARCHAR(MAX)  DEFAULT '',
    metadata    NVARCHAR(MAX)  DEFAULT '',
    importance  INT            DEFAULT 3,
    created_at  DATETIME2      DEFAULT GETUTCDATE()
);

CREATE TABLE memory.Sessions (
    id          UNIQUEIDENTIFIER PRIMARY KEY DEFAULT newid(),
    session_key NVARCHAR(255)  NOT NULL,
    agent       NVARCHAR(100)  DEFAULT '',
    status      NVARCHAR(50)   DEFAULT 'active',
    metadata    NVARCHAR(MAX)  DEFAULT '',
    started_at  DATETIME2      DEFAULT GETUTCDATE(),
    ended_at    DATETIME2      NULL
);

CREATE TABLE memory.KnowledgeIndex (
    id          UNIQUEIDENTIFIER PRIMARY KEY DEFAULT newid(),
    domain      NVARCHAR(100)  NOT NULL,
    key         NVARCHAR(255)  NOT NULL,
    content     NVARCHAR(MAX)  NOT NULL,
    source      NVARCHAR(255)  DEFAULT '',
    tags        NVARCHAR(500)  DEFAULT '',
    created_at  DATETIME2      DEFAULT GETUTCDATE()
);

CREATE TABLE memory.Todos (
    id          UNIQUEIDENTIFIER PRIMARY KEY DEFAULT newid(),
    title       NVARCHAR(500)  NOT NULL,
    description NVARCHAR(MAX)  DEFAULT '',
    priority    INT            DEFAULT 3,
    status      NVARCHAR(50)   DEFAULT 'open',
    tags        NVARCHAR(500)  DEFAULT '',
    created_at  DATETIME2      DEFAULT GETUTCDATE(),
    updated_at  DATETIME2      DEFAULT GETUTCDATE(),
    closed_at   DATETIME2      NULL
);
GO
```

## Step 2: Configure .env

Backend configuration uses a simple naming pattern. Any identifier works — not just `local` or `cloud`:

```env
# Local SQL Server
SQL_LOCAL_SERVER=10.0.0.110
SQL_LOCAL_PORT=1433
SQL_LOCAL_DATABASE=your_database_name
SQL_LOCAL_USER=your_user
SQL_LOCAL_PASSWORD=your_password

# Cloud SQL Server (Azure / site4now / etc.)
SQL_CLOUD_SERVER=yourserver.database.windows.net
SQL_CLOUD_PORT=1433
SQL_CLOUD_DATABASE=your_cloud_db
SQL_CLOUD_USER=your_cloud_user
SQL_CLOUD_PASSWORD=your_cloud_password

# Named backends — any identifier works:
# SQL_TAT_SERVER, SQL_TAT_DATABASE, etc. → get_memory('tat')
# SQL_HFTC_SERVER, SQL_HFTC_DATABASE, etc. → get_memory('hftc')
```

See [clawbot-sql-connector README](https://github.com/High-Falootin/clawbot-sql-connector#env-setup) for full backend naming docs.

## Step 3: Install

```bash
clawhub install sql-connector   # dependency — install first
clawhub install sql-memory
```

## Quick Start

```python
from sql_memory import SQLMemory, get_memory

mem = get_memory('local')   # or 'cloud', or any named backend

# Store a memory (importance 1-10: 3=routine, 7=strategic, 10=permanent)
mem.remember('facts', 'user_timezone', 'User is in EST/EDT', importance=7, tags='user,prefs')

# Recall it
entry = mem.recall('facts', 'user_timezone')
print(entry)  # → 'User is in EST/EDT'

# Search across all memories
results = mem.search_memories('timezone')

# Queue a task for an agent
task_id = mem.queue_task('my_agent', 'process_data', payload='{"source":"api"}', priority=3)

# Log an event
mem.log_event(event_type='task_started', agent='my_agent', description='Processing began')

# Todos
todo_id = mem.add_todo('Fix the login bug', priority=2, tags='bug,auth')
mem.complete_todo(todo_id)

# Connectivity check
mem.ping()  # → True
```

See [GETTING_STARTED.md](GETTING_STARTED.md) for full setup guide.
See [SKILL_REFERENCE.md](SKILL_REFERENCE.md) for complete API docs.

## API Reference

### Memory

| Method | Description |
|---|---|
| `remember(category, key, content, importance=3, tags='')` | Store or update a memory entry |
| `recall(category, key)` | Retrieve most recent active entry |
| `search_memories(query, limit=10)` | Full-text search across all memories |
| `get_recent(category, limit=10)` | Most recent entries in a category |
| `forget(category, key)` | Mark entry as inactive |

### Task Queue

| Method | Description |
|---|---|
| `queue_task(agent, task_type, payload='', priority=5, model_hint='')` | Add a task |
| `get_pending_tasks(agent=None, limit=10)` | Fetch pending tasks |
| `complete_task(task_id, result='')` | Mark task complete |
| `fail_task(task_id, error='')` | Mark task failed |

### Todos

| Method | Description |
|---|---|
| `add_todo(title, description='', priority=3, tags='')` | Create a todo |
| `complete_todo(todo_id)` | Mark complete |
| `update_todo(todo_id, **kwargs)` | Update fields |
| `delete_todo(todo_id)` | Hard delete |

### Activity Logging

| Method | Description |
|---|---|
| `log_event(event_type, agent='', description='', metadata='', importance=3)` | Write to ActivityLog |

## Memory Rollup Schedule

Hierarchical compression keeps long-term memory manageable:

```
Daily entries  → rolled up weekly   (every Sunday)
Weekly         → monthly            (1st of month)
Monthly        → yearly             (January 1st)
```

Each rollup preserves source references for traceability.

## Design Principles

- **UTC everywhere** — all timestamps use `GETUTCDATE()` in SQL, `datetime.now(timezone.utc)` in Python
- **Parameterized only** — no f-string SQL, ever; the connector layer enforces this
- **Importance scale** — 1–10: `3`=routine, `5`=significant, `7`=strategic, `10`=permanent facts

## Related

- [clawbot-sql-connector](https://github.com/High-Falootin/clawbot-sql-connector) — the transport layer this builds on (install first!)
- [openclaw-SQL-dreamer](https://github.com/High-Falootin/openclaw-SQL-dreamer) — the dream analysis layer built on top of sql-memory
- [clawhub.ai](https://clawhub.ai) — install with `clawhub install sql-memory`

## Community

Alpha software — your feedback shapes the v1 API. Open issues for broken installs, schema questions, or API suggestions.

## License

MIT
