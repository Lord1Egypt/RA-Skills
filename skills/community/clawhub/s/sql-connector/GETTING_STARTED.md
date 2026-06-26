# GETTING STARTED: SQL Connector

**For:** OpenClaw agents that need reliable SQL Server access  
**Time Required:** 10 minutes setup + 5 minutes configuration  
**Prerequisites:** OpenClaw installed, SQL Server (cloud or local), basic Python knowledge

---

## Overview: What is SQL Connector?

SQL Connector is a **sealed, retry-capable SQL Server transport** for OpenClaw agents. It handles:

- ✅ Multi-backend connections (local + cloud)
- ✅ Automatic retry on transient failures
- ✅ Parameterized queries (SQL injection safe)
- ✅ Structured error handling
- ✅ No system tools required (everything in Python)

**Why use it:**
- Your agents need SQL access without subprocess/sqlcmd
- You want **guaranteed parameterized queries** (sealed by metaclass)
- You need automatic retry and exponential backoff
- Your `.env` drives connection choice — no code change

**Who uses it:**
- SQL Memory (stores agent findings)
- SQL Dreamer (reads memories, dreams)
- Any agent querying production databases

---

## Step 1: Install SQL Connector

```bash
# Via ClawHub (recommended)
clawhub install sql-connector

# Or manually via pip
pip install clawbot-sql-connector pymssql python-dotenv
```

### Verify Installation

```bash
python3 << 'PYTHON'
from sql_connector import get_connector, SQLConnector
print("✅ SQL Connector imported successfully")
PYTHON
```

---

## Step 2: Configure Connection

Create a `.env` file in your OpenClaw workspace root with your SQL Server credentials.

### Find Your Workspace

```bash
# Locate OpenClaw workspace
openclaw status
# Look for: repo=/path/to/.openclaw/workspace
```

### Create .env File

```bash
cd ~/.openclaw/workspace
cp .env.example .env    # or create new file
```

### For Cloud SQL Server (Azure, site4now, etc.)

Edit `.env`:

```env
SQL_CLOUD_SERVER=your-server.database.windows.net
SQL_CLOUD_DATABASE=your_database_name
SQL_CLOUD_USER=your_username@yourserver
SQL_CLOUD_PASSWORD=your_password
SQL_DEFAULT_BACKEND=cloud
```

**Example (Azure):**
```env
SQL_CLOUD_SERVER=mycompany.database.windows.net
SQL_CLOUD_DATABASE=prod_memories
SQL_CLOUD_USER=admin@mycompany
SQL_CLOUD_PASSWORD=Sup3rS3cr3t!
SQL_DEFAULT_BACKEND=cloud
```

### For Local SQL Server (On-Prem / Self-Hosted)

Edit `.env`:

```env
SQL_LOCAL_SERVER=10.0.0.110
SQL_LOCAL_DATABASE=your_database_name
SQL_LOCAL_USER=your_username
SQL_LOCAL_PASSWORD=your_password
SQL_DEFAULT_BACKEND=local
```

**Example (Oblio setup):**
```env
SQL_LOCAL_SERVER=10.0.0.110
SQL_LOCAL_DATABASE=db_99ba1f_memory4oblio
SQL_LOCAL_USER=oblio
SQL_LOCAL_PASSWORD=MySecurePassword123
SQL_DEFAULT_BACKEND=local
```

### For Mixed Setup (Both Local + Cloud)

You can set **both** and switch via code:

```env
# Local (primary)
SQL_LOCAL_SERVER=10.0.0.110
SQL_LOCAL_DATABASE=db_99ba1f_memory4oblio
SQL_LOCAL_USER=oblio
SQL_LOCAL_PASSWORD=xxx

# Cloud (fallback/testing)
SQL_CLOUD_SERVER=your-server.database.windows.net
SQL_CLOUD_DATABASE=your_database
SQL_CLOUD_USER=your_user
SQL_CLOUD_PASSWORD=xxx

# Which to use by default
SQL_DEFAULT_BACKEND=local
```

---

## Step 3: Verify Connection

Test that SQL Connector can reach your SQL Server:

```bash
python3 << 'PYTHON'
from sql_connector import get_connector

# Use default backend from .env
db = get_connector()

if db.ping():
    print("✅ Connected to SQL Server")
    print(f"   Backend: {db.backend}")
    print(f"   Server: {db.host}")
else:
    print("❌ Could not connect to SQL Server")
    print("   Check your .env credentials")
PYTHON
```

### If Connection Fails

1. **Check credentials**
   ```bash
   grep "SQL_CLOUD_SERVER\|SQL_LOCAL_SERVER" ~/.openclaw/workspace/.env
   ```

2. **Verify SQL Server is accessible**
   ```bash
   # For cloud
   ping your-server.database.windows.net

   # For local
   ping 10.0.0.110
   ```

3. **Check firewall** — SQL Server uses port 1433:
   ```bash
   # For cloud (Azure typically allows)
   # For local, check: netstat -tulpn | grep 1433
   ```

4. **Verify permissions** — test your credentials manually with a SQL client

---

## Step 4: Use SQL Connector in Your Code

### Example 1: Basic Query

```python
from sql_connector import get_connector

# Connect using default backend from .env
db = get_connector()

# SELECT query (returns list of dicts)
rows = db.query(
    "SELECT TOP 5 id, content, category FROM memory.Memories ORDER BY created_at DESC"
)

for row in rows:
    print(f"{row['category']}: {row['content'][:50]}")
```

### Example 2: Parameterized Queries (Always Use This)

```python
from sql_connector import get_connector

db = get_connector()

# Always use %s placeholders for values
category = 'facts'
limit = 10

rows = db.query(
    "SELECT TOP %s id, content FROM memory.Memories WHERE category = %s",
    (limit, category)
)

print(f"Found {len(rows)} facts")
```

**Why parameterized:**
- ✅ Safe from SQL injection
- ✅ Sealed by metaclass (subclasses cannot override)
- ✅ Database handles escaping

**❌ NEVER do this:**
```python
# WRONG — SQL injection risk!
db.query(f"SELECT * FROM memory.Memories WHERE category = '{category}'")
```

### Example 3: Connection Pooling & Retry

```python
from sql_connector import get_connector, SQLConnectionError, SQLQueryError

db = get_connector()

# Automatic retry on transient failures
try:
    rows = db.query("SELECT * FROM memory.Memories WHERE id = %s", (123,))
    print(f"✅ Got {len(rows)} rows")
    
except SQLConnectionError as e:
    # Connection issue (retried automatically 3x)
    print(f"⚠️ Connection failed after retries: {e}")
    
except SQLQueryError as e:
    # Query syntax error (not retried)
    print(f"❌ Query failed: {e}")
```

**How retry works:**
1. First attempt
2. If transient failure (timeout, connection lost) → retry after 2s
3. Second attempt
4. If still fails → retry after 2s again
5. Third attempt
6. If still fails → raise SQLConnectionError

---

## Step 5: Common Patterns

### Pattern 1: INSERT Records

```python
from sql_connector import get_connector

db = get_connector()

# Insert a single record
db.execute(
    "INSERT INTO memory.Memories (category, key, content, importance) VALUES (%s, %s, %s, %s)",
    ('facts', 'discovery_001', 'Customer prefers feature X', 8)
)

print("✅ Record inserted")
```

### Pattern 2: Update with Conditions

```python
from sql_connector import get_connector

db = get_connector()

# Update specific records
success = db.execute(
    "UPDATE memory.Memories SET importance = %s WHERE category = %s AND importance < %s",
    (9, 'facts', 5)
)

if success:
    print("✅ Updated records")
else:
    print("❌ Update failed")
```

### Pattern 3: Get Single Value (Aggregate)

```python
from sql_connector import get_connector

db = get_connector()

# Get count of pending tasks
pending_count = db.scalar(
    "SELECT COUNT(*) FROM memory.TaskQueue WHERE status = %s",
    ('pending',)
)

print(f"Pending tasks: {pending_count}")
```

### Pattern 4: Explicit Backend Selection

```python
from sql_connector import get_connector

# Force cloud instead of default
db_cloud = get_connector('cloud')

# Force local instead of default
db_local = get_connector('local')

# Compare data between backends
cloud_facts = db_cloud.query("SELECT COUNT(*) as cnt FROM memory.Memories WHERE category = %s", ('facts',))
local_facts = db_local.query("SELECT COUNT(*) as cnt FROM memory.Memories WHERE category = %s", ('facts',))

print(f"Cloud: {cloud_facts[0]['cnt']} facts")
print(f"Local: {local_facts[0]['cnt']} facts")
```

---

## Step 6: Extend via Repository Pattern

Create domain-specific query layers:

```python
from sql_connector import get_connector

class MemoryRepository:
    def __init__(self, backend='cloud'):
        self.db = get_connector(backend)
    
    def get_important_facts(self, threshold=7):
        """Get facts with importance >= threshold"""
        return self.db.query(
            "SELECT id, content, importance, created_at FROM memory.Memories "
            "WHERE category = %s AND importance >= %s "
            "ORDER BY importance DESC",
            ('facts', threshold)
        )
    
    def store_finding(self, key, content, importance, tags=''):
        """Store a new finding"""
        return self.db.execute(
            "INSERT INTO memory.Memories (category, key, content, importance, tags) "
            "VALUES (%s, %s, %s, %s, %s)",
            ('findings', key, content, importance, tags)
        )
    
    def mark_archived(self, memory_id):
        """Archive a memory"""
        return self.db.execute(
            "UPDATE memory.Memories SET status = %s WHERE id = %s",
            ('archived', memory_id)
        )

# Use it
repo = MemoryRepository('local')
important = repo.get_important_facts(threshold=8)
repo.store_finding('obs_001', 'Pattern discovered', 9, 'analytics')
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'pymssql'"

**Install missing dependency:**
```bash
pip install pymssql
```

### "Connection refused" or "Cannot connect to SQL Server"

**Check:**
1. SQL Server is running: `ping your-server`
2. Port 1433 is accessible: `telnet your-server 1433`
3. `.env` credentials are correct: `grep SQL_ ~/.openclaw/workspace/.env`
4. Network allows connection (firewall, VPN)

**Test manually:**
```bash
python3 << 'PYTHON'
import pymssql
try:
    conn = pymssql.connect(
        server='your-server',
        user='your_user',
        password='your_password',
        database='your_db'
    )
    print("✅ Direct connection works")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")
PYTHON
```

### "Table or view not found"

**Check:**
1. Table exists in SQL Server: `SELECT * FROM INFORMATION_SCHEMA.TABLES`
2. Spelling is correct (SQL is case-sensitive for names on Linux)
3. You have SELECT permission on the table
4. Schema name is correct (usually `dbo` or `memory`)

**Debug query:**
```python
from sql_connector import get_connector
db = get_connector()

# List all tables
tables = db.query("SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES ORDER BY TABLE_SCHEMA, TABLE_NAME")
for row in tables:
    print(f"{row['TABLE_SCHEMA']}.{row['TABLE_NAME']}")
```

### ".env file not found" or "Credentials missing"

**Check:**
1. `.env` exists: `ls ~/.openclaw/workspace/.env`
2. Variables are set: `grep SQL_DEFAULT_BACKEND ~/.openclaw/workspace/.env`
3. No syntax errors in `.env` (should be `KEY=value` lines)

### Connection works, but queries are slow

**Optimization:**
1. Add indexes on frequently queried columns
2. Use `TOP N` for large result sets
3. Check query plan: `SET STATISTICS IO ON` (in SQL Server)
4. Consider connection pooling (built into SQL Connector)

---

## What's Next?

1. **Read [SKILL_REFERENCE.md](./SKILL_REFERENCE.md)** — detailed API reference, architecture, advanced usage

2. **Use SQL Memory** — build on top of SQL Connector
   ```python
   from sql_memory import SQLMemory
   mem = SQLMemory('cloud')
   mem.remember(category='facts', key='obs_001', content='...', importance=8)
   ```

3. **Integrate with agents** — agents can now access SQL databases
   ```python
   def agent_task(self):
       db = get_connector()
       findings = db.query("SELECT * FROM my_table")
       # Process findings
   ```

4. **Set up error handling** — catch and log failures gracefully
   ```python
   from sql_connector import SQLConnectionError, SQLQueryError
   try:
       db.query(...)
   except SQLConnectionError:
       # Log and retry
   except SQLQueryError:
       # Log and skip
   ```

---

## Support & Resources

- **GitHub Issues:** https://github.com/VeXHarbinger/clawbot-sql-connector/issues
- **ClawHub Registry:** https://clawhub.ai/skills/sql-connector
- **Full API Reference:** [SKILL_REFERENCE.md](./SKILL_REFERENCE.md)

---

**Last updated:** 2026-04-28  
**Version:** 2.1 (stable, production-ready)  
**Status:** Battle-tested. Used in production daily.
