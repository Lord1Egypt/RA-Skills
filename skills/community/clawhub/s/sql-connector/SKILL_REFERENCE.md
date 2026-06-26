# SKILL REFERENCE: SQL Connector

**For:** Developers building on SQL Connector, advanced users, agents needing production reliability  
**Scope:** Architecture, API reference, error patterns, performance optimization, advanced usage

---

## Quick Reference

| Operation | Method | Returns | Safe? |
|-----------|--------|---------|-------|
| SELECT query | `query(sql, params)` | `list[dict]` | ✅ Parameterized |
| INSERT/UPDATE/DELETE | `execute(sql, params)` | `bool` | ✅ Parameterized |
| Single value | `scalar(sql, params)` | `Any` | ✅ Parameterized |
| Health check | `ping()` | `bool` | ✅ Read-only |
| Get instance | `get_connector(backend)` | `SQLConnector` | N/A |

---

## Architecture

### Layer Model

```
┌────────────────────────────────────────┐
│  Your Code (agents, scripts)           │
│  from sql_connector import get_connector
│  db = get_connector('cloud')           │
└─────────────────┬──────────────────────┘
                  │
                  ▼
┌────────────────────────────────────────┐
│  Factory: get_connector(backend)       │
│  ├─ 'cloud' → MSSQLConnector(cloud)    │
│  └─ 'local' → MSSQLConnector(local)    │
└─────────────────┬──────────────────────┘
                  │
                  ▼
┌────────────────────────────────────────┐
│  SQLConnector (ABC + Metaclass)        │
│  _LockCoreMethods metaclass enforces   │
│  parameterized-only access             │
│                                        │
│  Public API:                           │
│  ├─ execute() — SEALED                 │
│  ├─ query() — SEALED                   │
│  ├─ scalar() — SEALED                  │
│  └─ ping()                             │
└─────────────────┬──────────────────────┘
                  │
                  ▼
┌────────────────────────────────────────┐
│  MSSQLConnector (pymssql impl)         │
│  ├─ Connection pooling                 │
│  ├─ Automatic retry (3x, 2s backoff)   │
│  └─ Structured error handling          │
└─────────────────┬──────────────────────┘
                  │
                  ▼
┌────────────────────────────────────────┐
│  pymssql (TDS 7.4 protocol)            │
│  └─ Native SQL Server driver           │
│     (no ODBC, no system packages)      │
└─────────────────┬──────────────────────┘
                  │
                  ▼
         SQL Server Database
         (Cloud or Local)
```

### Sealed Transport Pattern

The **metaclass `_LockCoreMethods`** prevents subclasses from overriding core methods:

```python
# This is BLOCKED by metaclass:
class BadConnector(MSSQLConnector):
    def query(self, sql, params=()):
        # CANNOT override - metaclass prevents it
        return super().query(sql, f"SELECT * FROM {sql}")  # ❌ Never runs
    
# ✅ This is ALLOWED - extend via composition/delegation:
class GoodRepository(MSSQLConnector):
    def get_facts(self, limit=10):
        # Cannot override query(), so we call it properly
        return self.query(
            "SELECT TOP %s * FROM memory.Memories WHERE category=%s",
            (limit, 'facts')
        )
```

**Why sealed?**
- Prevents SQL injection via subclass override
- Forces all database access through parameterized API
- No way to accidentally bypass safety

---

## Configuration Schema

### Environment Variables

All configuration comes from `.env` file (or system env vars):

```yaml
# Cloud SQL Server
SQL_CLOUD_SERVER:
  type: string
  required: true if backend=cloud
  example: "your-server.database.windows.net"
  description: Azure SQL Server hostname

SQL_CLOUD_DATABASE:
  type: string
  required: true if backend=cloud
  example: "my_database"
  description: Database name

SQL_CLOUD_USER:
  type: string
  required: true if backend=cloud
  example: "admin@your-server"
  description: Login user (may include domain)

SQL_CLOUD_PASSWORD:
  type: string
  required: true if backend=cloud
  description: Login password (store securely)

# Local SQL Server
SQL_LOCAL_SERVER:
  type: string
  required: true if backend=local
  example: "10.0.0.110"
  description: Local/on-prem SQL Server IP or hostname

SQL_LOCAL_DATABASE:
  type: string
  required: true if backend=local
  example: "db_99ba1f_memory4oblio"
  description: Database name

SQL_LOCAL_USER:
  type: string
  required: true if backend=local
  example: "oblio"
  description: Login user

SQL_LOCAL_PASSWORD:
  type: string
  required: true if backend=local
  description: Login password

# Global
SQL_DEFAULT_BACKEND:
  type: string
  required: false
  default: "cloud"
  options: ["cloud", "local"]
  description: Which backend to use when get_connector() called without argument
```

### Loading Credentials

```python
from sql_connector import get_connector
import os

# 1. From .env (automatic via python-dotenv)
db = get_connector()

# 2. Verify which backend was used
print(db.backend)  # 'cloud' or 'local'
print(db.host)     # Server hostname/IP

# 3. Credentials are never exposed
print(db.user)     # Raises AttributeError (intentionally private)
```

---

## API Reference

### Factory: `get_connector(backend=None) → SQLConnector`

Get a SQL Connector instance.

**Parameters:**
- `backend` (str, optional) — `'cloud'` or `'local'`
  - If omitted: uses `SQL_DEFAULT_BACKEND` from .env (default: `'cloud'`)
  - If provided: overrides .env setting

**Returns:**
- `MSSQLConnector` instance configured for the backend

**Raises:**
- `EnvironmentError` — missing required env vars for backend

**Example:**
```python
# Use .env default
db = get_connector()

# Force cloud
db_cloud = get_connector('cloud')

# Force local
db_local = get_connector('local')
```

---

### Method: `SQLConnector.query(sql, params=())`

Execute a SELECT query, return rows as list of dicts.

**Parameters:**
- `sql` (str) — SQL SELECT statement with `%s` placeholders
- `params` (tuple) — values to substitute for `%s` placeholders

**Returns:**
- `list[dict]` — each row as a dictionary (column name → value)
- `[]` — empty list if no rows found

**Raises:**
- `SQLQueryError` — syntax error, permission denied, etc. (not retried)
- `SQLConnectionError` — connection lost (retried 3x with backoff)

**Example:**
```python
from sql_connector import get_connector

db = get_connector()

# Simple query
rows = db.query("SELECT * FROM memory.Memories WHERE category = %s", ('facts',))

# With multiple parameters
rows = db.query(
    "SELECT TOP %s id, content FROM memory.Memories WHERE category = %s AND importance >= %s",
    (10, 'facts', 7)
)

# Process results
for row in rows:
    print(f"{row['id']}: {row['content']}")
    print(row.keys())  # ['id', 'content', ...]
```

---

### Method: `SQLConnector.execute(sql, params=())`

Execute INSERT, UPDATE, or DELETE. Return success/failure.

**Parameters:**
- `sql` (str) — SQL DML statement with `%s` placeholders
- `params` (tuple) — values to substitute for `%s` placeholders

**Returns:**
- `True` — statement executed successfully
- `False` — statement had no effect (no rows matched condition)

**Raises:**
- `SQLQueryError` — syntax error, constraint violation, etc. (not retried)
- `SQLConnectionError` — connection lost (retried 3x with backoff)

**Example:**
```python
from sql_connector import get_connector

db = get_connector()

# INSERT
ok = db.execute(
    "INSERT INTO memory.Memories (category, key, content, importance) VALUES (%s, %s, %s, %s)",
    ('facts', 'discovery_001', 'Observation', 8)
)
print("Inserted" if ok else "Not inserted")

# UPDATE
ok = db.execute(
    "UPDATE memory.Memories SET importance = %s WHERE id = %s",
    (9, '123e4567-e89b-12d3-a456-426614174000')
)
print("Updated" if ok else "No rows matched")

# DELETE
ok = db.execute(
    "DELETE FROM memory.Memories WHERE status = %s AND created_at < DATEADD(day, %s, GETUTCDATE())",
    ('archived', -30)
)
print("Deleted old records" if ok else "No records to delete")
```

---

### Method: `SQLConnector.scalar(sql, params=())`

Execute query returning a single value (aggregates, counts, etc.).

**Parameters:**
- `sql` (str) — SQL query with `%s` placeholders, must return exactly 1 column, 1 row
- `params` (tuple) — values for `%s` placeholders

**Returns:**
- The single value (type depends on column: int, str, datetime, etc.)
- `None` — if query returned no rows

**Raises:**
- `SQLQueryError` — query error, multiple columns, etc. (not retried)
- `SQLConnectionError` — connection lost (retried 3x with backoff)

**Example:**
```python
from sql_connector import get_connector

db = get_connector()

# Count
count = db.scalar("SELECT COUNT(*) FROM memory.Memories WHERE category = %s", ('facts',))
print(f"Total facts: {count}")

# Max/Min
latest = db.scalar("SELECT MAX(created_at) FROM memory.Memories")
print(f"Latest memory: {latest}")

# Single lookup
content = db.scalar("SELECT content FROM memory.Memories WHERE id = %s", (123,))
if content:
    print(f"Content: {content}")
else:
    print("Not found")
```

---

### Method: `SQLConnector.ping()`

Check connectivity to SQL Server. Useful for health checks.

**Parameters:**
- None

**Returns:**
- `True` — connected and responsive
- `False` — connection failed

**Raises:**
- Nothing (catches all errors internally)

**Example:**
```python
from sql_connector import get_connector

db = get_connector()

if db.ping():
    print("✅ Database is healthy")
else:
    print("❌ Database is unavailable")
    # Stop processing, alert ops
```

---

## Error Handling

### Exception Hierarchy

```
BaseException
  └─ Exception
      └─ sql_connector.SQLConnectorError (base)
          ├─ sql_connector.SQLConnectionError
          │  └─ Transient failures: timeouts, connection lost, pool exhausted
          │  └─ Action: retry or fail gracefully
          │
          └─ sql_connector.SQLQueryError
             └─ Permanent failures: syntax, permissions, constraints
             └─ Action: log and skip (don't retry)
```

### Handling Transient Failures

```python
from sql_connector import get_connector, SQLConnectionError

db = get_connector()

try:
    rows = db.query("SELECT * FROM memory.Memories LIMIT 10")
except SQLConnectionError as e:
    # Connection issue (already retried 3x internally)
    print(f"⚠️ Database temporarily unavailable: {e}")
    print("Retrying manually...")
    
    import time
    for attempt in range(3):
        try:
            rows = db.query("SELECT * FROM memory.Memories LIMIT 10")
            print("✅ Recovered")
            break
        except SQLConnectionError:
            if attempt < 2:
                time.sleep(2 ** attempt)  # 1s, 2s, 4s exponential backoff
            else:
                print("❌ Failed after 3 attempts")
                raise
```

### Handling Query Errors

```python
from sql_connector import get_connector, SQLQueryError

db = get_connector()

try:
    # Intentionally bad query (syntax error)
    db.query("SLELECT * FROM memory.Memories")  # typo
except SQLQueryError as e:
    # Syntax error — not retried, not transient
    print(f"❌ Query error (do not retry): {e}")
    print("Fix the query syntax")
```

### Handling Missing Credentials

```python
from sql_connector import get_connector
import os

try:
    db = get_connector('cloud')
except EnvironmentError as e:
    # Missing .env vars
    print(f"❌ Missing credentials: {e}")
    print("Set SQL_CLOUD_SERVER, SQL_CLOUD_DATABASE, etc. in .env")
    raise
```

---

## Performance Tips

### 1. Connection Pooling (Built-In)

SQL Connector reuses connections automatically. No manual pooling needed:

```python
from sql_connector import get_connector

db = get_connector()

# First call: creates connection (takes ~100ms)
rows1 = db.query("SELECT COUNT(*) FROM memory.Memories")

# Second call: reuses same connection (~5ms)
rows2 = db.query("SELECT COUNT(*) FROM memory.TaskQueue")

# Connection pool is per-backend (cloud, local)
# Multiple calls reuse the same pool
```

### 2. Batch Operations

Insert multiple records in one batch rather than many individual queries:

```python
from sql_connector import get_connector

db = get_connector()

# ❌ SLOW: N queries
data = [('fact1', 'Content A'), ('fact2', 'Content B'), ('fact3', 'Content C')]
for key, content in data:
    db.execute(
        "INSERT INTO memory.Memories (category, key, content) VALUES (%s, %s, %s)",
        ('facts', key, content)
    )

# ✅ FAST: 1 query with multiple rows (SQL Server syntax)
db.execute(
    """
    INSERT INTO memory.Memories (category, key, content) VALUES
    (%s, %s, %s),
    (%s, %s, %s),
    (%s, %s, %s)
    """,
    ('facts', 'fact1', 'Content A',
     'facts', 'fact2', 'Content B',
     'facts', 'fact3', 'Content C')
)
```

### 3. Use Indexes

For frequent queries, add database indexes:

```sql
-- Add index for fast lookup by category
CREATE INDEX idx_memories_category ON memory.Memories(category);

-- Add index for date-based queries
CREATE INDEX idx_memories_created ON memory.Memories(created_at DESC);

-- Add composite index for common filters
CREATE INDEX idx_memories_cat_imp ON memory.Memories(category, importance DESC);
```

### 4. Limit Result Sets

Use `TOP N` (SQL Server syntax) to avoid loading huge datasets:

```python
from sql_connector import get_connector

db = get_connector()

# ✅ GOOD: Get only what you need
recent = db.query("SELECT TOP 100 * FROM memory.Memories ORDER BY created_at DESC")

# ❌ BAD: Load entire table
all_rows = db.query("SELECT * FROM memory.Memories")

# For pagination
page = 1
limit = 50
offset = (page - 1) * limit
rows = db.query(
    "SELECT * FROM memory.Memories ORDER BY created_at DESC "
    "OFFSET %s ROWS FETCH NEXT %s ROWS ONLY",
    (offset, limit)
)
```

### 5. Retry Strategy

Automatic retry (3x, 2s backoff) is built-in. No code needed:

```
Attempt 1: Immediate
  └─ Fails with transient error
Attempt 2: After 2 seconds
  └─ Fails with transient error
Attempt 3: After 2 seconds
  └─ Succeeds ✅
  
Total time: ~4-5 seconds, but guaranteed eventual success
```

To add custom retry on top:

```python
import time
from sql_connector import get_connector, SQLConnectionError

db = get_connector()

def query_with_fallback(sql, params):
    """Query with fallback to local if cloud fails"""
    try:
        return db.query(sql, params)
    except SQLConnectionError:
        print("Cloud failed, trying local...")
        db_local = get_connector('local')
        return db_local.query(sql, params)

# Use it
rows = query_with_fallback("SELECT * FROM memory.Memories", ())
```

---

## Advanced Usage

### 1. Custom Repository Layer

Build domain-specific query logic:

```python
from sql_connector import get_connector, SQLQueryError

class MemoryRepository:
    def __init__(self, backend='cloud'):
        self.db = get_connector(backend)
    
    def store_finding(self, category, key, content, importance=5, tags=''):
        """Store a finding with validation"""
        if not key or len(key) > 255:
            raise ValueError(f"Invalid key: {key}")
        
        return self.db.execute(
            "INSERT INTO memory.Memories (category, key, content, importance, tags) "
            "VALUES (%s, %s, %s, %s, %s)",
            (category, key, content, importance, tags)
        )
    
    def get_by_importance(self, category, min_importance=7):
        """Get high-importance memories"""
        return self.db.query(
            "SELECT id, key, content, importance FROM memory.Memories "
            "WHERE category = %s AND importance >= %s "
            "ORDER BY importance DESC",
            (category, min_importance)
        )
    
    def search(self, query_text):
        """Full-text search (SQL Server CONTAINS syntax)"""
        try:
            return self.db.query(
                "SELECT id, key, content FROM memory.Memories "
                "WHERE CONTAINS(content, %s)",
                (f'"{query_text}"',)
            )
        except SQLQueryError as e:
            # Full-text index may not exist
            print(f"Full-text search not available: {e}")
            return []

# Use it
repo = MemoryRepository('local')
repo.store_finding('findings', 'obs_001', 'Pattern X observed', importance=9)
important = repo.get_by_importance('findings', min_importance=8)
```

### 2. Switching Backends Dynamically

Compare or migrate between cloud and local:

```python
from sql_connector import get_connector

db_cloud = get_connector('cloud')
db_local = get_connector('local')

# Get counts from both
cloud_count = db_cloud.scalar("SELECT COUNT(*) FROM memory.Memories")
local_count = db_local.scalar("SELECT COUNT(*) FROM memory.Memories")

print(f"Cloud: {cloud_count} records")
print(f"Local: {local_count} records")

# Copy from cloud to local
if cloud_count > local_count:
    print("Syncing cloud → local...")
    missing = db_cloud.query(
        "SELECT id, category, key, content, importance FROM memory.Memories "
        "WHERE created_at > (SELECT MAX(created_at) FROM memory.Memories @db_local)"
    )
    for row in missing:
        db_local.execute(
            "INSERT INTO memory.Memories (id, category, key, content, importance) "
            "VALUES (%s, %s, %s, %s, %s)",
            (row['id'], row['category'], row['key'], row['content'], row['importance'])
        )
```

### 3. Monitoring & Observability

Log query performance:

```python
import time
from sql_connector import get_connector

db = get_connector()

def logged_query(name, sql, params):
    """Execute query and log timing"""
    start = time.time()
    try:
        result = db.query(sql, params)
        duration = time.time() - start
        print(f"✅ {name}: {len(result)} rows in {duration:.2f}s")
        return result
    except Exception as e:
        duration = time.time() - start
        print(f"❌ {name}: {type(e).__name__} after {duration:.2f}s")
        raise

# Use it
rows = logged_query("fetch_facts", "SELECT * FROM memory.Memories WHERE category=%s", ('facts',))
```

---

## Troubleshooting

| Problem | Diagnosis | Solution |
|---------|-----------|----------|
| "Cannot connect" | Check firewall, server running | See Troubleshooting in GETTING_STARTED.md |
| "Table not found" | Schema/permission issue | Verify table exists, check permissions |
| "Too many open connections" | Connection pool exhausted | Limit concurrent queries, increase timeout |
| "Query is slow" | Missing index or bad query | Add index, optimize WHERE clause |
| "Parameterization error" | Wrong number of %s vs params | Count placeholders: `%s` = params count |

---

## References

- **GETTING_STARTED.md** — Installation, setup, quick examples
- **GitHub:** https://github.com/VeXHarbinger/clawbot-sql-connector
- **ClawHub:** https://clawhub.ai/skills/sql-connector
- **pymssql docs:** https://pymssql.readthedocs.io/

---

**Last updated:** 2026-04-28  
**Version:** 2.1 (stable)  
**Status:** Production-ready, heavily tested
