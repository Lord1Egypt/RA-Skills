# GETTING STARTED: SQL Memory

**For:** OpenClaw agents that need persistent, semantically-meaningful memory  
**Time Required:** 15 minutes setup + 5 minutes validation  
**Prerequisites:** OpenClaw installed, SQL Server (cloud or local), sql-connector installed

---

## ⚠️ Install sql-connector First

SQL Memory **requires** the SQL Connector skill as its transport layer. If you skip this, nothing works.

```bash
clawhub install sql-connector   # ← MUST DO THIS FIRST
clawhub install sql-memory
```

If you haven't set up sql-connector yet, start here:  
**[clawbot-sql-connector GETTING_STARTED.md](https://github.com/VeXHarbinger/clawbot-sql-connector/blob/main/GETTING_STARTED.md)**

---

## Overview: Where SQL Memory Fits

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│   Your OpenClaw Agents                                           │
│   ↓                                                              │
│   ┌───────────────────────────────────────────────────────────┐  │
│   │  SQL Memory  ← YOU ARE HERE                               │  │
│   │  ├─ remember() / recall() / search_memories()            │  │
│   │  ├─ queue_task() / claim_task() / complete_task()        │  │
│   │  ├─ log_event() / get_recent_activity()                  │  │
│   │  ├─ store_knowledge() / search_knowledge()               │  │
│   │  ├─ add_todo() / complete_todo()                         │  │
│   │  └─ Daily → Weekly → Monthly → Yearly rollups            │  │
│   └───────────────────────────────────────────────────────────┘  │
│   ↓                                                              │
│   ┌───────────────────────────────────────────────────────────┐  │
│   │  SQL Connector  (installed in Step 0 above)               │  │
│   │  └─ Handles credentials, retries, parameterized SQL      │  │
│   └───────────────────────────────────────────────────────────┘  │
│   ↓                                                              │
│   SQL Server (Cloud or Local)                                    │
│   └─ memory.Memories, TaskQueue, ActivityLog, Sessions,          │
│      KnowledgeIndex, Todos                                       │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
                          ↓ (optional, next tier)
              SQL Dreamer — interprets memories into synthesis
```

**The story:**
- **SQL Connector** moves data reliably (transport layer)
- **SQL Memory** stores meaning and context (semantic layer) ← this skill
- **SQL Dreamer** interprets memories into insight (synthesis layer)

---

## Step 1: Verify sql-connector Is Working

Before installing sql-memory, confirm your foundation is solid:

```bash
python3 -c "from sql_connector import get_connector; print('✅ OK' if get_connector().ping() else '❌ FAILED')"
```

If this fails, fix sql-connector first. Check credentials in your `.env` file.

---

## Step 2: Install SQL Memory

```bash
clawhub install sql-memory
```

Verify the import:

```bash
python3 -c "from sql_memory import get_memory; print('✅ sql-memory imported')"
```

---

## Step 3: Configure .env

SQL Memory reads the same `.env` as sql-connector. No extra variables required — the same connection profiles you configured for sql-connector work here automatically.

Your `.env` should already have entries like:

```env
# Local SQL Server
SQL_LOCAL_SERVER=10.0.0.110
SQL_LOCAL_PORT=1433
SQL_LOCAL_DATABASE=db_99ba1f_memory4oblio
SQL_LOCAL_USER=your_username
SQL_LOCAL_PASSWORD=your_password

# Cloud SQL Server (Azure, site4now, etc.)
SQL_CLOUD_SERVER=yourserver.database.windows.net
SQL_CLOUD_PORT=1433
SQL_CLOUD_DATABASE=your_cloud_database
SQL_CLOUD_USER=your_cloud_user
SQL_CLOUD_PASSWORD=your_cloud_password
```

> **Note on database name:** Use **your own database name** here. The example above uses `db_99ba1f_memory4oblio` — that's a specific instance. Your database will have whatever name you created it with in SQL Server.

> **Note on `SQL_LOCAL_DATABASE=Oblio_Memories`:** If you see this value in any old config or skill file, it's a dead/legacy value. Use your actual database name.

---

## Step 4: Create the Schema

SQL Memory needs 6 tables inside the `memory` schema. Run this once before first use:

### Option A — Automated Setup (Recommended)

```bash
# Navigate to where sql-memory installed
pip show clawbot-sql-memory | grep Location
# Example output: Location: /home/youruser/.venv/lib/python3.11/site-packages

cd /path/from/above/clawbot_sql_memory

# Create schema with default (local) profile
python3 setup_schema.py

# Or use cloud profile
python3 setup_schema.py --cloud
```

Expected output:
```
clawbot-sql-memory schema setup — profile: local

✅ Connected to SQL Server

  CREATE memory schema
  CREATE memory.Memories
  CREATE memory.TaskQueue
  CREATE memory.ActivityLog
  CREATE memory.Sessions
  CREATE memory.KnowledgeIndex
  CREATE memory.Todos

Schema setup complete.

Next step: configure your .env and run:
  python3 -c "from sql_memory import get_memory; print(get_memory('local').ping())"
```

If tables already exist, the script will print `SKIP` instead of `CREATE` — safe to re-run.

### Option B — Manual SQL

If the setup script fails or you prefer to manage schema yourself, run this in SSMS, Azure Data Studio, or `sqlcmd`:

```sql
CREATE SCHEMA memory;
GO

CREATE TABLE memory.Memories (
    id          INT IDENTITY(1,1) PRIMARY KEY,
    category    NVARCHAR(100)  NOT NULL,
    [key]       NVARCHAR(255)  NOT NULL,
    content     NVARCHAR(MAX)  NOT NULL,
    importance  INT            DEFAULT 3,
    tags        NVARCHAR(500)  DEFAULT '',
    status      NVARCHAR(50)   DEFAULT 'active',
    created_at  DATETIME2      DEFAULT GETUTCDATE(),
    updated_at  DATETIME2      DEFAULT GETUTCDATE()
);

CREATE TABLE memory.TaskQueue (
    id           INT IDENTITY(1,1) PRIMARY KEY,
    agent        NVARCHAR(100)  NOT NULL,
    task_type    NVARCHAR(100)  NOT NULL,
    payload      NVARCHAR(MAX)  DEFAULT '',
    priority     INT            DEFAULT 5,
    status       NVARCHAR(50)   DEFAULT 'pending',
    retries      INT            DEFAULT 0,
    model_hint   NVARCHAR(100)  DEFAULT '',
    created_at   DATETIME2      DEFAULT GETUTCDATE(),
    updated_at   DATETIME2      DEFAULT GETUTCDATE(),
    claimed_at   DATETIME2      NULL,
    completed_at DATETIME2      NULL,
    error        NVARCHAR(MAX)  DEFAULT ''
);

CREATE TABLE memory.ActivityLog (
    id          INT IDENTITY(1,1) PRIMARY KEY,
    event_type  NVARCHAR(100)  NOT NULL,
    agent       NVARCHAR(100)  DEFAULT '',
    description NVARCHAR(MAX)  DEFAULT '',
    metadata    NVARCHAR(MAX)  DEFAULT '',
    importance  INT            DEFAULT 3,
    created_at  DATETIME2      DEFAULT GETUTCDATE()
);

CREATE TABLE memory.Sessions (
    id          INT IDENTITY(1,1) PRIMARY KEY,
    session_key NVARCHAR(255)  NOT NULL,
    agent       NVARCHAR(100)  DEFAULT '',
    status      NVARCHAR(50)   DEFAULT 'active',
    metadata    NVARCHAR(MAX)  DEFAULT '',
    started_at  DATETIME2      DEFAULT GETUTCDATE(),
    ended_at    DATETIME2      NULL
);

CREATE TABLE memory.KnowledgeIndex (
    id         INT IDENTITY(1,1) PRIMARY KEY,
    domain     NVARCHAR(100)  NOT NULL,
    [key]      NVARCHAR(255)  NOT NULL,
    content    NVARCHAR(MAX)  NOT NULL,
    source     NVARCHAR(255)  DEFAULT '',
    tags       NVARCHAR(500)  DEFAULT '',
    created_at DATETIME2      DEFAULT GETUTCDATE()
);

CREATE TABLE memory.Todos (
    id          INT IDENTITY(1,1) PRIMARY KEY,
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

---

## Step 5: Validate — Quick Tests

Run these one by one to confirm everything is wired up correctly.

### Test 1: Connectivity

```python
from sql_memory import get_memory

mem = get_memory('local')   # or 'cloud'
result = mem.ping()
print("✅ Connected" if result else "❌ Connection failed")
```

### Test 2: Store and Retrieve a Memory

```python
from sql_memory import get_memory

mem = get_memory('local')

# Store a memory with importance=7 (strategic-level)
mem.remember(
    category='test',
    key='first_memory',
    content='sql-memory is working correctly',
    importance=7,
    tags='test,validation'
)

# Retrieve it by category + key
content = mem.recall('test', 'first_memory')
print(f"✅ Recalled: {content}" if content else "❌ Recall failed")
```

### Test 3: Search

```python
from sql_memory import get_memory

mem = get_memory('local')
results = mem.search_memories('working correctly')
print(f"✅ Found {len(results)} results" if results else "❌ Search returned nothing")
for r in results:
    print(f"  [{r['category']}] {r['key_name']}: {r['content'][:60]}")
```

### Test 4: Log an Event

```python
from sql_memory import get_memory

mem = get_memory('local')
ok = mem.log_event(
    event_type='setup_complete',
    agent='setup',
    description='sql-memory schema and connection validated',
    importance=5
)
print("✅ Event logged" if ok else "❌ Log failed")
```

### Test 5: Task Queue

```python
from sql_memory import get_memory

mem = get_memory('local')

# Queue a task
task_id = mem.queue_task(
    agent='my_agent',
    task_type='process_data',
    payload='{"source": "test"}',
    priority=5
)
print(f"✅ Task queued: {task_id}" if task_id else "❌ Queue failed")

# Fetch pending tasks
tasks = mem.get_pending_tasks(agent='my_agent', task_types=['process_data'])
print(f"  Found {len(tasks)} pending tasks")

# Complete it
if task_id:
    mem.complete_task(task_id, result='completed in test')
    print("✅ Task completed")
```

### Full Self-Test (Built In)

The module ships with a self-test runner:

```bash
python3 -m sql_memory   # runs all self-tests against 'local' backend
```

---

## What You Now Have

After completing setup, your SQL Server database has:

| Table | Purpose |
|-------|---------|
| `memory.Memories` | Persistent facts with importance scoring and search |
| `memory.TaskQueue` | Agent work items with priority + retry logic |
| `memory.ActivityLog` | Immutable audit trail for all agent actions |
| `memory.Sessions` | Agent session state and context persistence |
| `memory.KnowledgeIndex` | Domain-specific knowledge, indexed by domain + topic |
| `memory.Todos` | Structured todo/task tracking with projects and priorities |

---

## Typical Usage Pattern

Here's how a real agent integrates sql-memory:

```python
from sql_memory import get_memory

class MyAgent:
    def __init__(self):
        self.mem = get_memory('cloud')  # or 'local'
    
    def process_finding(self, key, content, importance):
        # Store it
        self.mem.remember('findings', key, content, importance=importance)
        
        # Log the event
        self.mem.log_event('finding_stored', 'my_agent', f'Stored: {key}', importance=3)
    
    def get_context(self, keyword):
        # Search across everything
        return self.mem.search_memories(keyword, limit=10)
    
    def queue_followup(self, task_type, data):
        task_id = self.mem.queue_task('downstream_agent', task_type, data, priority=3)
        return task_id
```

---

## Importance Scale — Quick Reference

When you call `remember()`, set `importance` based on how long this memory should live:

| Score | Tier | Examples |
|-------|------|---------|
| 1–2 | Ephemeral | Temporary debug notes, scratch calculations |
| 3–4 | Operational | Task logs, routine status updates |
| 5–6 | Significant | Task completions, research findings |
| 7–8 | Strategic | Architecture decisions, system changes |
| 9 | Critical | Security issues, blocking problems |
| 10 | Permanent | Core identity, values, foundational facts |

Default is `3` if you don't specify. For most agent output, use `5` or higher.

---

## Troubleshooting

### `ImportError: sql_connector.py not found`

sql-connector is not installed or not on the path.

```bash
clawhub install sql-connector   # install it
# Then verify:
python3 -c "from sql_connector import get_connector; print('OK')"
```

### Connection Fails (ping returns False)

1. Verify `.env` credentials are correct for your backend
2. Check SQL Server is running and accessible on port 1433
3. Test the connector layer directly:

```bash
python3 -c "from sql_connector import get_connector; print(get_connector('local').ping())"
```

4. For cloud SQL, verify your server hostname resolves:
```bash
ping your-server.database.windows.net
```

### `Invalid object name 'memory.Memories'`

Tables haven't been created yet. Run:

```bash
python3 setup_schema.py
# or for cloud:
python3 setup_schema.py --cloud
```

### `remember()` returns True but `recall()` returns None

This can happen if the MERGE query is matching on `category` + `key` but using a different column name than your schema uses. Verify your schema matches the expected layout by checking:

```python
from sql_connector import get_connector
db = get_connector('local')
cols = db.query("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='memory' AND TABLE_NAME='Memories'")
print([c['COLUMN_NAME'] for c in cols])
```

### Search Returns No Results

`search_memories()` does LIKE-based search (not full-text). Ensure your keyword appears in `content`, `tags`, or `key_name`. It's case-insensitive on SQL Server by default.

---

## Next Steps

You've got persistent memory running. Here's where to go next:

### 1. Read the Full Reference

**[SKILL_REFERENCE.md](./SKILL_REFERENCE.md)** — every method, every parameter, architecture deep-dive, rollup system details.

### 2. Install SQL Dreamer

SQL Dreamer reads your memories and synthesizes patterns, decisions, and long-term insights — the third tier of the stack.

```bash
clawhub install sql-dreamer
```

SQL Dreamer queries your `memory.Memories` table nightly (configurable), pulls entries with `importance >= 7`, and runs them through OpenClaw's native dreaming pipeline. The richer your memory store, the more meaningful the dream output.

### 3. Integrate With Your Agents

```python
from sql_memory import get_memory

mem = get_memory('cloud')

# Store a research finding
mem.remember('research', 'user_pref_timezone', 'User is in EST/EDT', importance=7, tags='user,prefs')

# Store a decision
mem.remember('decisions', 'arch_choice_db', 'Chose SQL Server for persistence — schema flexibility + parameterized safety', importance=8)

# Audit trail
mem.log_event('research_complete', 'research_agent', 'Processed 14 findings for ticket OB-42', importance=4)

# Pass work to next agent
mem.queue_task('impl_agent', 'implementation', '{"ticket": "OB-42"}', priority=3)
```

### 4. Explore the Rollup System

SQL Memory's rollup system compresses memory over time:
- Daily entries → rolled up weekly (every Sunday)
- Weekly → monthly (1st of each month)
- Monthly → yearly (January 1st)

This keeps your memory store manageable without losing historical context. See **[SKILL_REFERENCE.md → Rollup System](./SKILL_REFERENCE.md#rollup-system)** for details.

---

## Support & Resources

- **GitHub Issues:** https://github.com/VeXHarbinger/clawbot-sql-memory/issues
- **ClawHub Registry:** https://clawhub.ai/skills/sql-memory
- **sql-connector:** https://github.com/VeXHarbinger/clawbot-sql-connector
- **SQL Dreamer (next tier):** https://github.com/High-Falootin/openclaw-sql-dreamer

---

**Last updated:** 2026-04-28  
**Version:** 2.0 (alpha — API stable, community feedback period open)  
**Status:** Functional and in active production use.
