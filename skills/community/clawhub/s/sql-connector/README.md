# clawbot-sql-connector

> **STABLE** — Battle-tested in production. API is stable as of v2.0.

A sealed, retry-capable SQL Server connector for OpenClaw agents. Built on **pymssql** — no `sqlcmd`, no ODBC drivers, no system tools required.

📚 **Documentation**
- **[GETTING STARTED](./GETTING_STARTED.md)** — Installation, setup, configuration, quick examples (15 min read)
- **[SKILL REFERENCE](./SKILL_REFERENCE.md)** — Full API, architecture, error handling, performance tips, advanced usage

🚀 **Getting Started (TL;DR)**
1. `pip install clawbot-sql-connector`
2. Set credentials in `.env` (cloud or local)
3. `from sql_connector import get_connector; db = get_connector(); db.ping()`
4. Use `db.query()`, `db.execute()`, `db.scalar()`

## Features

- **Multi-backend:** `local` (on-prem) and `cloud` (hosted) in one connector
- **Env-var driven default:** set `SQL_DEFAULT_BACKEND` in `.env` — no code change needed
- **Sealed transport:** `execute()` and `query()` sealed via metaclass — subclasses cannot bypass parameterized queries
- **Automatic retry:** retry 3x with exponential backoff (2s) on transient failures
- **Structured errors:** `SQLConnectionError` (transient) vs `SQLQueryError` (permanent)
- **Operations:** `execute()` (INSERT/UPDATE/DELETE), `query()` (SELECT → list of dicts), `scalar()` (single value), `ping()` (health check)
- **Production-ready:** connection pooling, timeout handling, no hardcoded credentials
- **Dependencies:** Only `pymssql` + `python-dotenv` (no ODBC, no system packages)

## Quick Start

For full setup including configuration examples, see **[GETTING STARTED](./GETTING_STARTED.md)**.

### Installation

```bash
# Via ClawHub (recommended)
clawhub install sql-connector

# Or direct pip
pip install clawbot-sql-connector pymssql python-dotenv
```

### Configure

Create `.env` in your workspace with SQL Server credentials:

**Cloud (Azure, site4now, etc.):**
```env
SQL_CLOUD_SERVER=your-server.database.windows.net
SQL_CLOUD_DATABASE=your_database
SQL_CLOUD_USER=your_user@server
SQL_CLOUD_PASSWORD=your_password
SQL_DEFAULT_BACKEND=cloud
```

**Local (on-prem):**
```env
SQL_LOCAL_SERVER=10.0.0.110
SQL_LOCAL_DATABASE=your_database
SQL_LOCAL_USER=sa
SQL_LOCAL_PASSWORD=your_password
SQL_DEFAULT_BACKEND=local
```

### Quick Example

```python
from sql_connector import get_connector, SQLConnectionError

db = get_connector()  # uses SQL_DEFAULT_BACKEND from .env

# SELECT (returns list of dicts)
rows = db.query(
    "SELECT TOP 5 id, content FROM memory.Memories WHERE category = %s",
    ('facts',)
)

# INSERT/UPDATE/DELETE (returns bool)
success = db.execute(
    "INSERT INTO memory.Memories (category, key, content) VALUES (%s, %s, %s)",
    ('facts', 'obs_001', 'Pattern discovered')
)

# Single value (COUNT, MAX, etc.)
count = db.scalar(
    "SELECT COUNT(*) FROM memory.Memories WHERE category = %s",
    ('facts',)
)

# Health check
if db.ping():
    print("✅ Database online")
```

## Design Principles

### Parameterized Queries (Always)

```python
# ❌ WRONG — SQL injection risk
db.query(f"SELECT * FROM Memories WHERE category = '{category}'")

# ✅ CORRECT — Always use %s placeholders
db.query("SELECT * FROM Memories WHERE category = %s", (category,))
```

The sealed metaclass prevents subclass override, enforcing this at the type level.

### Error Handling

```python
from sql_connector import SQLConnectionError, SQLQueryError

try:
    rows = db.query("SELECT * FROM memory.Memories")
except SQLConnectionError as e:
    # Transient failure (already retried 3x)
    print(f"Temporarily unavailable: {e}")
except SQLQueryError as e:
    # Permanent failure (syntax, permissions, etc.)
    print(f"Query error: {e}")
```

## Common Patterns

### Pattern 1: Repository Layer

```python
from sql_connector import get_connector

class MemoryRepository:
    def __init__(self, backend='cloud'):
        self.db = get_connector(backend)
    
    def store_fact(self, key, content, importance=7):
        return self.db.execute(
            "INSERT INTO memory.Memories (category, key, content, importance) "
            "VALUES (%s, %s, %s, %s)",
            ('facts', key, content, importance)
        )
    
    def get_important(self, threshold=7):
        return self.db.query(
            "SELECT id, content, importance FROM memory.Memories "
            "WHERE category = %s AND importance >= %s ORDER BY importance DESC",
            ('facts', threshold)
        )

repo = MemoryRepository('local')
repo.store_fact('discovery_001', 'Pattern found', importance=9)
```

### Pattern 2: Conditional Backend

```python
from sql_connector import get_connector, SQLConnectionError

def get_db_safe():
    """Use cloud, fallback to local on error"""
    try:
        db = get_connector('cloud')
        if db.ping():
            return db
    except SQLConnectionError:
        pass
    return get_connector('local')
```

## Documentation

| Document | Purpose | Duration |
|----------|---------|----------|
| **[GETTING STARTED](./GETTING_STARTED.md)** | Installation, setup, quick examples, troubleshooting | 15 min |
| **[SKILL REFERENCE](./SKILL_REFERENCE.md)** | Complete API, architecture, error patterns, performance, advanced usage | Reference |

**Start here:** [GETTING STARTED](./GETTING_STARTED.md) (first-time users)

**Deep dive:** [SKILL REFERENCE](./SKILL_REFERENCE.md) (developers, production systems)

## Publishing & Versions

**Published to:** [clawhub.ai](https://clawhub.ai/skills/sql-connector) as `sql-connector`

**Current version:** 2.1.0 (stable, production-ready)

**Version policy:** Stable releases only. We run this in production daily and publish when thoroughly tested (30+ days stable).

**Compatibility:**
- Python 3.9+
- SQL Server 2019+ (including Azure SQL)
- pymssql 2.2.0+

---

## Custom Backend Identifiers

`local` and `cloud` are just examples. The connector supports **any identifier you define** — as long as you set matching `SQL_{IDENTIFIER}_*` env vars.

```env
# .env — define as many backends as you need

# Your primary on-prem database
SQL_LOCAL_SERVER=10.0.0.110
SQL_LOCAL_DATABASE=db_memory
SQL_LOCAL_USER=sa
SQL_LOCAL_PASSWORD=yourpassword

# A cloud/Azure database
SQL_CLOUD_SERVER=yourserver.database.windows.net
SQL_CLOUD_DATABASE=db_cloud
SQL_CLOUD_USER=admin@yourserver
SQL_CLOUD_PASSWORD=yourpassword

# A project-specific database (any name works)
SQL_TAT_SERVER=10.0.0.110
SQL_TAT_DATABASE=db_tat_operations
SQL_TAT_USER=sa
SQL_TAT_PASSWORD=yourpassword

SQL_HFTC_SERVER=10.0.0.110
SQL_HFTC_DATABASE=db_hftc_inventory
SQL_HFTC_USER=sa
SQL_HFTC_PASSWORD=yourpassword

# Set the default backend (used when no backend arg passed)
SQL_DEFAULT_BACKEND=local
```

Then use the identifier as the backend argument:

```python
from sql_connector import get_connector

db_local = get_connector()        # uses SQL_DEFAULT_BACKEND
db_tat   = get_connector('tat')   # uses SQL_TAT_* env vars
db_hftc  = get_connector('hftc')  # uses SQL_HFTC_* env vars
db_cloud = get_connector('cloud') # uses SQL_CLOUD_* env vars
```

**Pattern:** `SQL_{IDENTIFIER}_{FIELD}` where `FIELD` is one of `SERVER`, `DATABASE`, `USER`, `PASSWORD`, `PORT` (optional, defaults to 1433).

This means you can connect to as many separate databases as needed without any code changes — just add env vars and pass the identifier.

---

## API Reference

### `get_connector(backend: str = _DEFAULT_BACKEND) → SQLConnector`

Factory. Returns `MSSQLConnector` for the given backend.

### `SQLConnector.query(sql, params=()) → list[dict]`

Execute SELECT. Returns rows as list of dicts.

### `SQLConnector.execute(sql, params=()) → bool`

Execute INSERT/UPDATE/DELETE. Returns True on success.

### `SQLConnector.scalar(sql, params=()) → Any`

Execute query returning a single value.

### `SQLConnector.ping() → bool`

Connectivity check. Returns True if connected.

### `SQLConnector.from_env(profile=_DEFAULT_BACKEND) → SQLConnector`

v1.x compatibility factory.

---

## License

MIT — see LICENSE.
