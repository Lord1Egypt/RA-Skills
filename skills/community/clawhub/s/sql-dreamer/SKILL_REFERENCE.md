# SQL Skills Reference Architecture

**For:** Developers and users who want to understand how SQL Connector, SQL Memory, and SQL Dreamer work together.

---

## Quick Reference

| Skill | Purpose | Depends On | Key Files |
|-------|---------|-----------|-----------|
| **sql-connector** | Foundation: connects to SQL Server | Nothing | `.env` (credentials) |
| **sql-memory** | Persistent memory store | sql-connector | `memory.Memories` table |
| **sql-dreamer** | Automated dream synthesis | sql-connector + sql-memory | `dreams.*` tables, `config/sql_dreamer.yml` |

---

## Data Flow Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│                    Your OpenClaw Agents                        │
│                    (agents, codebase)                          │
│                                                                │
│                    Store facts/decisions in:                   │
│                                                                │
└──────────────────────┬─────────────────────────────────────────┘
                       │
                       ▼
    ┌─────────────────────────────────────┐
    │     SQL Memory API                  │
    │  from sql_memory import SQLMemory   │
    │  mem.remember(...)                  │
    │  mem.recall(...)                    │
    └──────────────┬──────────────────────┘
                   │
                   ▼
    ┌──────────────────────────────────────────┐
    │      SQL Connector                       │
    │  (handles credentials, retries, etc)     │
    └──────────────┬───────────────────────────┘
                   │
                   ▼
    ┌──────────────────────────────────────────┐
    │      SQL Server (Cloud or Local)         │
    │                                          │
    │      memory.Memories                     │
    │      memory.TaskQueue                    │
    │      memory.ActivityLog                  │
    │                                          │
    │      dreams.DreamCorpus                  │
    │      dreams.DreamLight                   │
    │      dreams.DreamREM                     │
    │      dreams.DreamDeep                    │
    │                                          │
    └──────────────────────────────────────────┘
                   ▲
                   │
    ┌──────────────┴──────────────┐
    │                             │
    │  [3:00 AM] SQL Dreamer      │
    │  pre_dream_sql_feed.py      │
    │  (queries Memories)         │
    │                             │
    │  [3:30 AM] Native Dreamer   │
    │  (runs via OpenClaw)        │
    │                             │
    │  [4:00 AM] SQL Dreamer      │
    │  post_dream_archiver.py     │
    │  (stores results)           │
    │                             │
    └─────────────────────────────┘
                   │
                   ▼ (optional)
            Confluence
         (Dream Portal)
```

---

## Dependency Chain

### Level 1: SQL Connector (Foundation)

```python
from sql_connector import get_connector

db = get_connector()  # Uses credentials from .env
# That's it. You can now query SQL Server.
```

**Requirements:**
- `.env` file with SQL Server credentials
- SQL Server running and accessible

**Provides:**
- `query()` — SELECT statements
- `execute()` — INSERT/UPDATE/DELETE
- `scalar()` — single value queries
- `ping()` — health check

---

### Level 2: SQL Memory (Depends on Level 1)

```python
from sql_memory import SQLMemory

mem = SQLMemory('cloud')  # Uses SQL Connector internally
mem.remember(
    category='facts',
    key='my_memory',
    content='Learned something',
    importance=7  # 1-10 scale
)

fact = mem.recall(category='facts', key='my_memory')
```

**Requirements:**
- SQL Connector installed and configured
- `memory.*` tables created (run setup_schema.py)

**Provides:**
- `remember()` — store a memory
- `recall()` — retrieve a memory
- `search_memories()` — full-text search
- `log_event()` — activity logging
- Task queueing for agents

**Data stored in:**
- `memory.Memories` — your facts/decisions/incidents
- `memory.TaskQueue` — agent work items
- `memory.ActivityLog` — audit trail

---

### Level 3: SQL Dreamer (Depends on Level 1 + Level 2)

```yaml
# config/sql_dreamer.yml

sql:
  backend: "cloud"  # Uses SQL Connector

corpus:
  importance_threshold: 7  # Read from memory.Memories

dreaming:
  workspace_dir: "/path/to/.openclaw/workspace"
  phases:
    light: true
    rem: true
    deep: true
```

**Requirements:**
- SQL Connector installed and configured
- SQL Memory installed with `memory.Memories` table populated
- `dreams.*` tables created (run sql/migrate.py)
- OpenClaw native dreamer installed and running

**Reads from:**
- `memory.Memories` (importance ≥ threshold)

**Writes to:**
- `dreams.DreamCorpus` (queued memories)
- `dreams.DreamLight` (light sleep candidates)
- `dreams.DreamREM` (REM sleep themes)
- `dreams.DreamDeep` (deep sleep promotions)

**Outputs to:**
- `memory/dreaming/light/YYYY-MM-DD.md`
- `memory/dreaming/rem/YYYY-MM-DD.md`
- `memory/dreaming/deep/YYYY-MM-DD.md`

---

## Configuration Map

### `.env` (SQL Connector)

Located: `~/.openclaw/workspace/.env`

```env
# For cloud SQL Server
SQL_CLOUD_SERVER=your-server.database.windows.net
SQL_CLOUD_DATABASE=your_database
SQL_CLOUD_USER=your_user@company
SQL_CLOUD_PASSWORD=xxxxx
SQL_DEFAULT_BACKEND=cloud

# Or for local SQL Server
SQL_LOCAL_SERVER=10.0.0.110
SQL_LOCAL_DATABASE=your_database
SQL_LOCAL_USER=oblio
SQL_LOCAL_PASSWORD=xxxxx
SQL_DEFAULT_BACKEND=local
```

### `config/sql_dreamer.yml` (SQL Dreamer)

Located: `~/.openclaw/workspace/config/sql_dreamer.yml`

```yaml
sql:
  backend: "cloud"  # Inherits from .env

corpus:
  importance_threshold: 7      # 1-10, higher = fewer but better memories
  lookback_days: 2             # How many days back to query

dreaming:
  workspace_dir: "/home/user/.openclaw/workspace"
  phases:
    light:
      enabled: true
      max_candidates: 20
    rem:
      enabled: true
    deep:
      enabled: true
  archive_after_days: 7        # Delete dream files after N days

confluence:
  enabled: false               # Set true to publish
  domain: "yourorg.atlassian.net"
  email: "your@email.com"
  api_token: "xxxxx"           # From Atlassian account settings
  space_key: "YOUR_SPACE"      # Confluence space ID
  parent_page_id: "12345"      # Parent page for Memory Palace
```

---

## Database Schema Map

### SQL Memory Tables

```sql
-- Stores your memories
CREATE TABLE memory.Memories (
    id          UNIQUEIDENTIFIER,  -- Unique ID
    category    NVARCHAR(100),     -- 'facts', 'decisions', 'incidents', 'lessons_learned'
    key         NVARCHAR(255),     -- Unique key per category
    content     NVARCHAR(MAX),     -- The actual memory text
    importance  INT,               -- 1-10 scale
    tags        NVARCHAR(500),     -- Optional tags
    status      NVARCHAR(50),      -- 'active', 'archived'
    created_at  DATETIME2,         -- When stored
    updated_at  DATETIME2          -- When last modified
);

-- Work items for agents
CREATE TABLE memory.TaskQueue (
    id          UNIQUEIDENTIFIER,
    agent       NVARCHAR(100),     -- Agent name
    task_type   NVARCHAR(100),     -- Type of work
    payload     NVARCHAR(MAX),     -- JSON data
    priority    INT,               -- 1-10, lower = sooner
    status      NVARCHAR(50),      -- 'pending', 'claimed', 'done', 'failed'
    retries     INT,               -- How many times retried
    created_at  DATETIME2,
    claimed_at  DATETIME2,
    completed_at DATETIME2,
    error       NVARCHAR(MAX)      -- Error message if failed
);

-- Activity log (audit trail)
CREATE TABLE memory.ActivityLog (
    id          UNIQUEIDENTIFIER,
    event_type  NVARCHAR(100),     -- 'memory_stored', 'task_queued', 'error'
    agent       NVARCHAR(100),
    description NVARCHAR(MAX),
    metadata    NVARCHAR(MAX),     -- JSON
    created_at  DATETIME2
);
```

### SQL Dreamer Tables

```sql
-- Memories queued for this dream cycle
CREATE TABLE dreams.DreamCorpus (
    id          UNIQUEIDENTIFIER,
    dream_date  DATE,              -- Which night
    memory_id   UNIQUEIDENTIFIER,  -- From memory.Memories
    importance  INT,               -- Inherited from memory
    source      NVARCHAR(100),     -- 'memory' or 'session'
    created_at  DATETIME2
);

-- Light sleep phase results
CREATE TABLE dreams.DreamLight (
    id          UNIQUEIDENTIFIER,
    dream_date  DATE,
    snippet     NVARCHAR(MAX),     -- The insight text
    confidence  FLOAT,             -- 0.0-1.0
    recall_count INT,              -- How many times this surfaced
    status      NVARCHAR(50),      -- 'staged', 'promoted'
    created_at  DATETIME2
);

-- REM sleep phase results
CREATE TABLE dreams.DreamREM (
    id          UNIQUEIDENTIFIER,
    dream_date  DATE,
    theme_text  NVARCHAR(MAX),     -- The theme
    frequency   INT,               -- How often this appeared
    confidence  FLOAT,
    created_at  DATETIME2
);

-- Deep sleep phase results
CREATE TABLE dreams.DreamDeep (
    id          UNIQUEIDENTIFIER,
    dream_date  DATE,
    snippet     NVARCHAR(MAX),     -- The promoted memory
    ranked      INT,               -- Rank by score
    promoted    BIT,               -- Was this promoted?
    created_at  DATETIME2
);
```

---

## Environment Variable Map

| Variable | Used By | Default | Required |
|----------|---------|---------|----------|
| `SQL_CLOUD_SERVER` | sql-connector | — | Only if using cloud |
| `SQL_CLOUD_DATABASE` | sql-connector | — | Only if using cloud |
| `SQL_CLOUD_USER` | sql-connector | — | Only if using cloud |
| `SQL_CLOUD_PASSWORD` | sql-connector | — | Only if using cloud |
| `SQL_LOCAL_SERVER` | sql-connector | — | Only if using local |
| `SQL_LOCAL_DATABASE` | sql-connector | — | Only if using local |
| `SQL_LOCAL_USER` | sql-connector | — | Only if using local |
| `SQL_LOCAL_PASSWORD` | sql-connector | — | Only if using local |
| `SQL_DEFAULT_BACKEND` | sql-connector | `cloud` | No (optional) |
| `CONFLUENCE_API_TOKEN` | sql-dreamer | — | Only if using Confluence |

---

## Common Patterns

### Pattern 1: Store an Agent Finding

```python
from sql_memory import SQLMemory

mem = SQLMemory('cloud')

# Your agent discovers something important
mem.remember(
    category='facts',
    key='discovered_pattern_001',
    content='Customer X always prefers Y over Z',
    importance=8,  # High importance = included in dreams
    tags='customer_behavior,shopping'
)
```

### Pattern 2: Query Memories for Your Own Use

```python
from sql_memory import SQLMemory

mem = SQLMemory('cloud')

# Get a specific memory
fact = mem.recall(category='facts', key='discovered_pattern_001')
if fact:
    print(fact['content'])

# Search for memories matching a pattern
results = mem.search_memories('customer behavior')
for memory in results:
    print(f"{memory['key']}: {memory['content'][:100]}")
```

### Pattern 3: Manual Dream Cycle

If you don't want to use crontab:

```bash
# Run pre-dream feed
python3 ~/.openclaw/workspace/scripts/pre_dream_sql_feed.py

# Native OpenClaw dreamer runs (in memory-core)
# This is automatic

# Run post-dream archiver
python3 ~/.openclaw/workspace/scripts/post_dream_archiver.py
```

### Pattern 4: Check Dream Results

```python
from sql_connector import get_connector

db = get_connector()

# Get last night's light sleep
light = db.query("""
    SELECT snippet, confidence, recall_count
    FROM dreams.DreamLight
    WHERE dream_date = CAST(GETDATE() AS DATE)
    ORDER BY confidence DESC
""")

for candidate in light:
    print(f"{candidate['snippet']} (confidence: {candidate['confidence']})")
```

---

## Troubleshooting by Layer

### Layer 1: SQL Connector Issues

**"Cannot connect to SQL Server"**
- Check `.env` credentials
- Verify SQL Server is running: `ping your-server.database.windows.net`
- Check firewall: SQL Server uses port 1433

**"Connection timeout"**
- Server might be down or unreachable
- Check network connectivity
- Try manually connecting with SQL Server Management Studio

### Layer 2: SQL Memory Issues

**"Tables not found"**
- Did you run `setup_schema.py`?
- Verify tables exist: `SELECT * FROM memory.Memories`

**"Cannot store/retrieve memories"**
- Check Layer 1: Is SQL Connector working?
- Check permissions: Does your SQL user have CREATE/SELECT/INSERT rights?

### Layer 3: SQL Dreamer Issues

**"Dreams are always empty"**
- Check `memory.Memories` table has data
- Check `importance_threshold` in config (might be too high)
- Run `pre_dream_sql_feed.py` manually and check output

**"Cron jobs not running"**
- Check crontab: `crontab -l`
- Check logs: `tail ~/.openclaw/logs/pre_dream.log`
- Run scripts manually to see errors

---

## Version Compatibility

| Component | Version | Status |
|-----------|---------|--------|
| sql-connector | 2.0+ | Stable |
| sql-memory | 0.5+ | Alpha (stable for production, API may evolve) |
| sql-dreamer | 1.0+ | Stable |
| Python | 3.9+ | Required |
| SQL Server | 2019+ | Required (Azure SQL supported) |

---

## References

- **SQL Connector API:** See `clawbot-sql-connector` README
- **SQL Memory API:** See `clawbot-sql-memory` README
- **SQL Dreamer Config:** See `openclaw-sql-dreamer` README
- **Setup Guide:** See `GETTING_STARTED.md`

---

**Last updated:** 2026-04-28
