# GETTING STARTED: SQL Connector + SQL Memory + SQL Dreamer

**For:** Users who want to use all three skills in a standalone OpenClaw installation  
**Time Required:** 15 minutes setup + 5 minutes configuration  
**Prerequisites:** OpenClaw installed, SQL Server (cloud or local), basic CLI knowledge

---

## Overview: How These 3 Skills Work Together

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Your OpenClaw agents                                           │
│  ↓                                                              │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ SQL Memory (clawbot-sql-memory)                          │   │
│  │ ├─ Stores: facts, decisions, incidents, lessons learned │   │
│  │ ├─ Table: memory.Memories                               │   │
│  │ └─ Uses: SQL Connector to read/write                     │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ↓ (daily at 3:00 AM)                                           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ SQL Dreamer (openclaw-sql-dreamer)                       │   │
│  │ ├─ Reads: high-importance memories from SQL Memory      │   │
│  │ ├─ Runs: OpenClaw's native dreaming pipeline            │   │
│  │ ├─ Stores: dream results back to SQL                    │   │
│  │ └─ Uses: SQL Connector for all I/O                       │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ↓ (optional: publish to Confluence)                            │
│  Confluence (Dream reports)                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Foundation: SQL Connector (clawbot-sql-connector)
├─ Handles: All database communication
├─ Supports: Cloud (Azure, site4now) or local SQL Server
└─ Used by: SQL Memory and SQL Dreamer
```

**Key insight:** SQL Connector is the foundation. SQL Memory uses it. SQL Dreamer depends on both.

---

## Step 1: Install SQL Connector

The foundation — handles all database connections for the other two skills.

```bash
# Install via ClawHub
clawhub install sql-connector

# Or manually
pip install clawbot-sql-connector pymssql python-dotenv
```

### Configure SQL Connector

In your OpenClaw workspace root, create a `.env` file:

```bash
cd ~/.openclaw/workspace
# Or wherever your OpenClaw workspace is
cp .env.example .env
```

Edit `.env` and add SQL Server credentials:

**If using Cloud SQL Server (Azure, site4now, etc.):**
```env
SQL_CLOUD_SERVER=your-server.database.windows.net
SQL_CLOUD_DATABASE=your_database_name
SQL_CLOUD_USER=your_username
SQL_CLOUD_PASSWORD=your_password
SQL_DEFAULT_BACKEND=cloud
```

**If using Local SQL Server (on-prem):**
```env
SQL_LOCAL_SERVER=10.0.0.110
SQL_LOCAL_DATABASE=your_database_name
SQL_LOCAL_USER=your_username
SQL_LOCAL_PASSWORD=your_password
SQL_DEFAULT_BACKEND=local
```

### Verify Connection

```bash
python3 << 'PYTHON'
from sql_connector import get_connector

db = get_connector()
if db.ping():
    print("✅ Connected to SQL Server")
else:
    print("❌ Connection failed")
PYTHON
```

---

## Step 2: Install SQL Memory

Persistent memory for your agents. Stores everything they learn.

```bash
clawhub install sql-memory
```

### Create Database Schema

SQL Memory needs tables in your SQL Server. Create them once:

**Option A (Automatic — Recommended):**
```bash
# Find where sql-memory installed
pip show clawbot-sql-memory | grep Location
# Output example: Location: /home/username/.venv/lib/python3.10/site-packages/clawbot_sql_memory

# Go there and run setup
cd /path/from/above/clawbot_sql_memory
python3 setup_schema.py
```

**Option B (Manual — If Option A fails):**

Open your SQL Server (SSMS, Azure Data Studio, or sqlcmd) and run:

```sql
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
    created_at  DATETIME2      DEFAULT GETUTCDATE()
);
```

### Verify Setup

```bash
python3 << 'PYTHON'
from sql_memory import SQLMemory

mem = SQLMemory('cloud')  # or 'local' if using local server
mem.remember(
    category='facts',
    key='test_memory',
    content='This is a test memory',
    importance=5
)

result = mem.recall(category='facts', key='test_memory')
if result:
    print("✅ SQL Memory working")
else:
    print("❌ Could not retrieve memory")
PYTHON
```

---

## Step 3: Install SQL Dreamer

Automated dreaming powered by SQL-backed memories.

```bash
clawhub install sql-dreamer
```

### Create Dream Schema

SQL Dreamer needs its own tables. Create them once:

```bash
# Find where sql-dreamer installed
pip show openclaw-sql-dreamer | grep Location
# Output example: Location: /home/username/.venv/lib/python3.10/site-packages/openclaw_sql_dreamer

cd /path/from/above/openclaw_sql_dreamer
python3 sql/migrate.py
```

### Configure SQL Dreamer

Create configuration file:

```bash
cd ~/.openclaw/workspace
mkdir -p config
cp /path/to/sql_dreamer/config/example.yml config/sql_dreamer.yml
```

Edit `config/sql_dreamer.yml`:

```yaml
sql:
  # Use same credentials as .env file
  backend: "cloud"  # or "local"
  # sql_connector will read from .env automatically

corpus:
  importance_threshold: 7    # Only remember items score ≥ 7 (1-10 scale)
  lookback_days: 2            # Look back 2 days for memories

dreaming:
  workspace_dir: "/home/username/.openclaw/workspace"  # YOUR WORKSPACE PATH
  phases:
    light:
      enabled: true
    rem:
      enabled: true
    deep:
      enabled: true
  archive_after_days: 7       # Delete dream files after 7 days

confluence:
  enabled: false              # Set to true to publish dreams to Confluence
  # (See section below for Confluence setup)
```

### Find Your Workspace Path

```bash
# Find your OpenClaw workspace
which openclaw
# Output: /usr/local/bin/openclaw (or similar)

openclaw status
# Output will show: repo=/home/username/.openclaw/workspace
# Use that path in the config above
```

### Verify Schema Creation

```bash
python3 << 'PYTHON'
from sql_connector import get_connector

db = get_connector()
tables = db.query("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='dreams'")
if tables:
    print("✅ Dream tables created")
    for row in tables:
        print(f"  - {row['TABLE_NAME']}")
else:
    print("❌ Dream tables not found")
PYTHON
```

---

## Step 4: Schedule Dream Cycles (Crontab)

Add these lines to your crontab to run dreams automatically:

```bash
crontab -e
```

Paste these lines (adjust times to your preference):

```cron
# Pre-dream: Curate memories from SQL (3:00 AM)
0 3 * * * /usr/bin/python3 ~/.openclaw/workspace/scripts/pre_dream_sql_feed.py >> ~/.openclaw/logs/pre_dream.log 2>&1

# Post-dream: Archive dream outputs (4:00 AM, 1 hour after native dreamer)
0 4 * * * /usr/bin/python3 ~/.openclaw/workspace/scripts/post_dream_archiver.py >> ~/.openclaw/logs/post_dream.log 2>&1

# (Optional) Confluence publisher: Publish dreams to Confluence (4:30 AM)
# 30 4 * * * /usr/bin/python3 ~/.openclaw/workspace/scripts/confluence_dream_publisher.py >> ~/.openclaw/logs/confluence.log 2>&1
```

### Find Your Python Path

```bash
which python3
# Output: /usr/bin/python3 (use this in crontab)
```

### Find Script Paths

After installing via ClawHub, scripts are installed to:

```bash
pip show openclaw-sql-dreamer | grep Location
# Location: /home/username/.venv/lib/python3.10/site-packages/openclaw_sql_dreamer

# Scripts are in: /path/from/above/scripts/
```

---

## Step 5: Verify Everything Works

### Test 1: Can SQL Connector connect?

```bash
python3 << 'PYTHON'
from sql_connector import get_connector
db = get_connector()
print("✅ SQL Connector OK" if db.ping() else "❌ SQL Connector FAILED")
PYTHON
```

### Test 2: Can SQL Memory store/retrieve?

```bash
python3 << 'PYTHON'
from sql_memory import SQLMemory
mem = SQLMemory('cloud')
mem.remember(category='test', key='verify', content='Works!', importance=7)
result = mem.recall(category='test', key='verify')
print("✅ SQL Memory OK" if result else "❌ SQL Memory FAILED")
PYTHON
```

### Test 3: Can SQL Dreamer see the tables?

```bash
python3 << 'PYTHON'
from sql_connector import get_connector
db = get_connector()
tables = db.query("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA IN ('memory', 'dreams')")
print(f"✅ Found {len(tables)} tables:" if tables else "❌ No tables found")
for row in tables:
    print(f"  - {row['TABLE_NAME']}")
PYTHON
```

---

## What Happens on First Run?

After setup, here's what to expect:

**Day 1:** 
- You have empty SQL Memory (no memories yet)
- First dream cycle runs but finds nothing to dream about
- Dream output files are created but mostly empty
- ✅ This is normal

**Days 2-7:**
- Your agents store memories in SQL Memory
- Each night, dreams include those memories
- Dream quality improves as memory grows
- ✅ This is expected

**After 1 week:**
- Dreams should show patterns (themes, lasting truths)
- First synthetic memories promoted to long-term storage
- System is working as designed
- ✅ This is success

---

## Troubleshooting

### "Connection refused" or "Cannot connect to SQL Server"

**Check:**
1. SQL Server is running and accessible
2. `.env` credentials are correct
3. Firewall allows connection on port 1433 (SQL Server default)
4. Network can reach the server

```bash
# Test connection manually
python3 -c "from sql_connector import get_connector; get_connector().ping()" && echo "OK" || echo "FAILED"
```

### "Table not found" or "Schema not found"

**Check:**
1. Did you run `setup_schema.py` for SQL Memory?
2. Did you run `python3 sql/migrate.py` for SQL Dreamer?
3. Do the tables exist in your SQL Server?

```bash
# List all tables
python3 << 'PYTHON'
from sql_connector import get_connector
db = get_connector()
tables = db.query("SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES ORDER BY TABLE_SCHEMA, TABLE_NAME")
for row in tables:
    print(f"{row['TABLE_SCHEMA']}.{row['TABLE_NAME']}")
PYTHON
```

### "Script not found" in crontab

**Check:**
1. Find the actual script path: `pip show openclaw-sql-dreamer | grep Location`
2. Update crontab with full path: `/full/path/to/scripts/pre_dream_sql_feed.py`

### Dreams are always empty

**Expected if:**
- First run (no memories in SQL Memory yet)
- Memory importance is too high (raise threshold in config)

**Check:**
1. Do you have memories in SQL Memory? Query: `SELECT COUNT(*) FROM memory.Memories`
2. Are their importance scores ≥ 7? Check `importance` column
3. Lower threshold in `sql_dreamer.yml`: `importance_threshold: 5`

### Logs show errors

Check log files:

```bash
tail -50 ~/.openclaw/logs/pre_dream.log
tail -50 ~/.openclaw/logs/post_dream.log
```

---

## Next Steps

1. **Read individual skill READMEs** for advanced configuration
   - clawbot-sql-connector: Advanced retry logic, multi-tenant setup
   - clawbot-sql-memory: Semantic search, rollups, activity logging
   - openclaw-sql-dreamer: Confluence publishing, custom synthesizers

2. **Integrate with your agents** — use SQL Memory to store agent findings
   ```python
   from sql_memory import SQLMemory
   mem = SQLMemory('cloud')
   mem.remember(category='findings', key='research_123', content='...', importance=8)
   ```

3. **Set up Confluence publishing** (optional) — share dreams with team
   - See openclaw-sql-dreamer README → Confluence Integration

---

## Support

- **SQL Connector Issues:** https://github.com/VeXHarbinger/clawbot-sql-connector/issues
- **SQL Memory Issues:** https://github.com/VeXHarbinger/clawbot-sql-memory/issues
- **SQL Dreamer Issues:** https://github.com/High-Falootin/openclaw-sql-dreamer/issues

---

**Last updated:** 2026-04-28  
**Version:** 1.0 (stable for production use)
