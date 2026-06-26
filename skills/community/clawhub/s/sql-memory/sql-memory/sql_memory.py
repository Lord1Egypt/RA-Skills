#!/usr/bin/env python3
"""
sql_memory.py — Oblio SQL Memory Module (v2.0)
===============================================
Semantic memory layer for OpenClaw agents. All operations go through
SQLConnector v2 (pymssql, parameterised, sealed API) — no subprocess/sqlcmd.

Supports two backends:
  - 'local'  → SQL Server on DEAUS (10.0.0.110) — default
  - 'cloud'  → site4now hosted (SQL5112.site4now.net)

Backward-compatible with v1.x callers:
  - SQLMemory('local')         — works as before
  - get_memory('local')        — singleton factory preserved
  - mem.remember / recall / search / queue_task / log_event — all preserved
  - mem.execute(raw_sql)       — preserved as legacy passthrough (returns bool)
  - mem.execute_scalar(sql)    — preserved, returns Any

New in v2.0:
  - Transport: pymssql native driver (no sqlcmd subprocess)
  - UTC timestamps everywhere (datetime.now(timezone.utc))
  - Parameterised queries throughout — no string interpolation
  - execute_via_file() preserved as execute() — file-based workaround no longer needed
  - _parse_table() kept for any callers using raw output parsing (no-op path)

Usage:
    from sql_memory import SQLMemory, get_memory
    mem = get_memory('local')
    mem.remember('facts', 'sky_color', 'The sky is blue', importance=3)
    result = mem.recall('facts', 'sky_color')
"""

import os
import sys
import json
import logging
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

# ── Find and load .env ────────────────────────────────────────────────────────
import pathlib as _pathlib

def _find_env() -> Optional[str]:
    p = _pathlib.Path(os.path.abspath(__file__)).parent
    for _ in range(5):
        c = p / '.env'
        if c.exists():
            return str(c)
        p = p.parent
    return None

try:
    from dotenv import load_dotenv
    _env = _find_env()
    if _env:
        load_dotenv(_env, override=True)
except ImportError:
    _env = _find_env()
    if _env:
        with open(_env) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    os.environ[k.strip()] = v.strip().strip('"').strip("'")

# ── Import connector (handles both skill install path and infrastructure path) ─

def _import_connector():
    """Find and import SQLConnector from wherever it's installed."""
    # Try adjacent skill install first (workspace/skills/sql-connector/scripts/)
    skill_scripts_path = os.path.join(os.path.dirname(__file__), '..', '..', 'sql-connector', 'scripts')
    skill_path = os.path.join(os.path.dirname(__file__), '..', 'sql-connector')
    infra_path = os.path.join(os.path.dirname(__file__), '..', 'infrastructure')
    for p in [skill_scripts_path, skill_path, infra_path, os.path.dirname(__file__)]:
        abs_p = os.path.abspath(p)
        if os.path.exists(os.path.join(abs_p, 'sql_connector.py')):
            if abs_p not in sys.path:
                sys.path.insert(0, abs_p)
            from sql_connector import get_connector, SQLConnector
            return get_connector, SQLConnector
    raise ImportError("sql_connector.py not found. Install the sql-connector skill first.")

get_connector, SQLConnector = _import_connector()

# ── Logger ────────────────────────────────────────────────────────────────────

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

_log = logging.getLogger('sql_memory')
if not _log.handlers:
    _log.setLevel(logging.INFO)
    _fh = logging.FileHandler(os.path.join(LOG_DIR, 'sql_dbo.log'))
    _fh.setFormatter(logging.Formatter('%(asctime)s [sql_memory] %(levelname)s %(message)s'))
    _fh.formatter.converter = __import__('time').gmtime  # UTC timestamps in log file
    _log.addHandler(_fh)


# ── SQLMemory ─────────────────────────────────────────────────────────────────

class SQLMemory:
    """
    Unified SQL memory interface for Oblio agents.
    Wraps SQLConnector — all queries are parameterised, no string interpolation.

    Args:
        backend: 'local' (default) or 'cloud'
    """

    def __init__(self, backend: str = 'local') -> None:
        self.backend = backend
        self._db = get_connector(backend)
        _log.info(f"SQLMemory v2.0 initialized (backend={backend})")

    # ── Low-level passthrough (v1.x compatibility) ────────────────────────────

    def execute(self, query: str, timeout: int = 30) -> bool:
        """
        Legacy passthrough for raw SQL. Returns bool (v2) instead of stdout string (v1).
        Callers that checked 'error' in result.lower() should switch to checking False.
        NOTE: Raw SQL here bypasses parameterisation — migrate to mem.* methods for new code.
        """
        return self._db.execute(query)

    def execute_scalar(self, query: str) -> Optional[Any]:
        """Execute query and return first value. Parameterised via scalar()."""
        return self._db.scalar(query)

    def execute_via_file(self, query: str, timeout: int = 30) -> bool:
        """v1.x large-payload workaround — now just delegates to execute() since pymssql has no arg-length limit."""
        return self._db.execute(query)

    def execute_rows(self, query: str) -> List[str]:
        """Execute query and return rows as list of strings (v1.x compat)."""
        rows = self._db.query(query)
        return [str(list(r.values())) for r in rows]

    def ping(self) -> bool:
        return self._db.ping()

    # ── Memory Operations ─────────────────────────────────────────────────────

    def remember(self, category: str, key: str, content: str,
                 importance: int = 3, tags: str = '') -> bool:
        """
        Store or update a memory. Upserts by category + key_name.
        importance: 1-10 (10 = permanent)
        """
        now = datetime.now(timezone.utc)
        ok = self._db.execute("""
            MERGE memory.Memories AS target
            USING (SELECT %s AS category, %s AS key_name) AS source
              ON target.category = source.category
             AND target.key_name = source.key_name
             AND target.is_active = 1
            WHEN MATCHED THEN
              UPDATE SET content=%s, importance=%s, tags=%s, updated_at=%s
            WHEN NOT MATCHED THEN
              INSERT (category, key_name, content, importance, tags, source, is_active, created_at, updated_at)
              VALUES (%s, %s, %s, %s, %s, 'sql_memory', 1, %s, %s);
        """, (category, key, content, importance, tags, now,
              category, key, content, importance, tags, now, now))
        _log.info(f"remember({category}/{key}) → {'ok' if ok else 'failed'}")
        return ok

    def recall(self, category: str, key: str) -> Optional[str]:
        """Retrieve a specific memory's content. Returns content string or None."""
        rows = self._db.query(
            "SELECT content FROM memory.Memories WHERE category=%s AND key_name=%s AND is_active=1",
            (category, key)
        )
        return rows[0]['content'] if rows else None

    def recall_recent(self, n: int = 10) -> List[Dict[str, Any]]:
        """Return the N most recently updated memories across all categories."""
        return self._db.query("""
            SELECT TOP (%s) category, key_name, content, importance, tags,
                   CONVERT(varchar, ISNULL(updated_at, created_at), 120) AS ts
            FROM memory.Memories WHERE is_active=1
            ORDER BY ISNULL(updated_at, created_at) DESC
        """, (n,))

    def search_memories(self, keyword: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Full-text search across content, tags, and key_name."""
        like = f'%{keyword}%'
        return self._db.query("""
            SELECT TOP (%s) category, key_name, content, importance, tags
            FROM memory.Memories
            WHERE is_active=1
              AND (content LIKE %s OR tags LIKE %s OR key_name LIKE %s)
            ORDER BY importance DESC, ISNULL(updated_at, created_at) DESC
        """, (limit, like, like, like))

    def forget(self, category: str, key: str) -> bool:
        """Soft-delete a memory (set is_active=0)."""
        ok = self._db.execute(
            "UPDATE memory.Memories SET is_active=0 WHERE category=%s AND key_name=%s",
            (category, key)
        )
        _log.info(f"forget({category}/{key})")
        return ok

    # ── Activity Log ──────────────────────────────────────────────────────────

    def log_event(self, event_type: str, agent: str, description: str,
                  metadata: str = '', importance: int = 3) -> bool:
        """Write an event to the activity log (logged_at set by DB default)."""
        return self._db.execute("""
            INSERT INTO memory.ActivityLog (event_type, agent, description, metadata, importance)
            VALUES (%s, %s, %s, %s, %s)
        """, (event_type, agent, description, metadata, importance))

    def get_recent_activity(self, since_hours: int = 24,
                            agent: Optional[str] = None) -> List[Dict]:
        """Get recent activity log entries."""
        col = 'logged_at'   # actual column name on cloud schema
        if agent:
            return self._db.query(f"""
                SELECT event_type, agent, description,
                       CONVERT(varchar, {col}, 120) AS ts
                FROM memory.ActivityLog
                WHERE {col} >= DATEADD(HOUR, -%s, GETUTCDATE())
                  AND agent=%s
                ORDER BY {col} DESC
            """, (since_hours, agent))
        return self._db.query(f"""
            SELECT event_type, agent, description,
                   CONVERT(varchar, {col}, 120) AS ts
            FROM memory.ActivityLog
            WHERE {col} >= DATEADD(HOUR, -%s, GETUTCDATE())
            ORDER BY {col} DESC
        """, (since_hours,))

    # ── Task Queue ────────────────────────────────────────────────────────────

    def queue_task(self, agent: str, task_type: str, payload: str = '{}',
                   priority: Any = 5) -> Optional[str]:
        """Insert a new task. Priority can be int or string name."""
        _pmap = {'critical': 1, 'high': 2, 'medium': 5, 'low': 7, 'free': 9}
        if isinstance(priority, str):
            priority = _pmap.get(priority.lower(), 5)
        priority = int(priority)
        now = datetime.now(timezone.utc)
        ok = self._db.execute("""
            INSERT INTO memory.TaskQueue (agent, task_type, payload, priority, status, created_at)
            VALUES (%s, %s, %s, %s, 'pending', %s)
        """, (agent, task_type, payload, priority, now))
        if not ok:
            return None
        tid = self._db.scalar("""
            SELECT TOP 1 id FROM memory.TaskQueue
            WHERE agent=%s AND task_type=%s AND status='pending'
            ORDER BY created_at DESC
        """, (agent, task_type))
        _log.info(f"queue_task({agent}/{task_type}) → id={tid}")
        return str(tid) if tid else None

    def get_pending_tasks(self, agent: str, task_types: List[str],
                          limit: int = 10) -> List[Dict]:
        """Fetch pending tasks for an agent, ordered by priority then age."""
        if not task_types:
            return []
        placeholders = ','.join(['%s'] * len(task_types))
        return self._db.query(f"""
            SELECT TOP (%s) id, task_type, payload, priority, retry_count
            FROM memory.TaskQueue
            WHERE agent=%s AND task_type IN ({placeholders}) AND status='pending'
            ORDER BY priority ASC, created_at ASC
        """, (limit, agent, *task_types))

    def claim_task(self, task_id: Any) -> bool:
        """Mark a task as processing."""
        return self._db.execute("""
            UPDATE memory.TaskQueue
            SET status='processing', started_at=%s
            WHERE id=%s
        """, (datetime.now(timezone.utc), int(task_id)))

    def complete_task(self, task_id: Any, result: str = '') -> bool:
        """Mark a task as completed."""
        ok = self._db.execute("""
            UPDATE memory.TaskQueue
            SET status='completed', completed_at=%s, error_log=%s
            WHERE id=%s
        """, (datetime.now(timezone.utc), result[:500], int(task_id)))
        _log.info(f"complete_task({task_id})")
        return ok

    def fail_task(self, task_id: Any, error: str, retry_count: int = 0,
                  max_retries: int = 3) -> bool:
        """Fail or re-queue a task based on retry count."""
        new_status = 'pending' if retry_count < max_retries else 'failed'
        ok = self._db.execute("""
            UPDATE memory.TaskQueue
            SET status=%s, retry_count=retry_count+1, error_log=%s
            WHERE id=%s
        """, (new_status, error[:800], int(task_id)))
        _log.info(f"fail_task({task_id}) → {new_status}")
        return ok

    def get_completed_tasks(self, since_hours: int = 24,
                            agent: Optional[str] = None) -> List[Dict]:
        """Get recently completed or failed tasks."""
        if agent:
            return self._db.query("""
                SELECT id, agent, task_type, status,
                       CONVERT(varchar, completed_at, 120) AS ts
                FROM memory.TaskQueue
                WHERE status IN ('completed','failed')
                  AND completed_at >= DATEADD(HOUR, -%s, GETUTCDATE())
                  AND agent=%s
                ORDER BY completed_at DESC
            """, (since_hours, agent))
        return self._db.query("""
            SELECT id, agent, task_type, status,
                   CONVERT(varchar, completed_at, 120) AS ts
            FROM memory.TaskQueue
            WHERE status IN ('completed','failed')
              AND completed_at >= DATEADD(HOUR, -%s, GETUTCDATE())
            ORDER BY completed_at DESC
        """, (since_hours,))

    # ── Knowledge Index ───────────────────────────────────────────────────────

    def store_knowledge(self, domain: str, topic: str, summary: str = '',
                        file_path: str = '', tags: str = '') -> bool:
        """Store or update a knowledge entry. Upserts by domain + topic."""
        now = datetime.now(timezone.utc)
        return self._db.execute("""
            MERGE memory.KnowledgeIndex AS target
            USING (SELECT %s AS domain, %s AS topic) AS source
              ON target.domain = source.domain AND target.topic = source.topic
            WHEN MATCHED THEN
              UPDATE SET summary=%s, file_path=%s,
                         last_trained=%s, training_count=ISNULL(training_count,0)+1
            WHEN NOT MATCHED THEN
              INSERT (domain, topic, summary, file_path, last_trained, training_count, created_at)
              VALUES (%s, %s, %s, %s, %s, 1, %s);
        """, (domain, topic, summary, file_path, now,
              domain, topic, summary, file_path, now, now))

    def search_knowledge(self, domain: str, keyword: str = '') -> List[Dict]:
        """Search knowledge entries by domain and optional keyword."""
        if keyword:
            like = f'%{keyword}%'
            return self._db.query("""
                SELECT domain, topic, summary, file_path, training_count,
                       CONVERT(varchar, last_trained, 120) AS ts
                FROM memory.KnowledgeIndex
                WHERE domain=%s AND (topic LIKE %s OR summary LIKE %s)
                ORDER BY last_trained DESC
            """, (domain, like, like))
        return self._db.query("""
            SELECT domain, topic, summary, file_path, training_count,
                   CONVERT(varchar, last_trained, 120) AS ts
            FROM memory.KnowledgeIndex
            WHERE domain=%s ORDER BY last_trained DESC
        """, (domain,))

    def get_recent_knowledge(self, n: int = 10) -> List[Dict]:
        """Get the N most recently updated knowledge entries."""
        return self._db.query("""
            SELECT TOP (%s) domain, topic, summary,
                   CONVERT(varchar, last_trained, 120) AS ts
            FROM memory.KnowledgeIndex ORDER BY last_trained DESC
        """, (n,))

    # ── Sessions ──────────────────────────────────────────────────────────────

    def get_session_context(self, session_id: str) -> Optional[Dict]:
        """Load session context from the database."""
        rows = self._db.query(
            "SELECT session_key, channel, summary, token_count FROM memory.Sessions WHERE session_key=%s",
            (session_id,)
        )
        if not rows:
            return None
        row = rows[0]
        try:
            row['context'] = json.loads(row.get('summary') or '{}')
        except (json.JSONDecodeError, TypeError):
            row['context'] = {}
        return row

    def save_session_context(self, session_id: str, context_data: Dict,
                             channel: str = 'agent', token_count: int = 0) -> bool:
        """Persist session context as JSON in memory.Sessions."""
        ctx_json = json.dumps(context_data, default=str)
        now = datetime.now(timezone.utc)
        return self._db.execute("""
            MERGE memory.Sessions AS target
            USING (SELECT %s AS session_key) AS source
              ON target.session_key = source.session_key
            WHEN MATCHED THEN
              UPDATE SET summary=%s, token_count=%s, ended_at=%s
            WHEN NOT MATCHED THEN
              INSERT (session_key, channel, summary, token_count, started_at)
              VALUES (%s, %s, %s, %s, %s);
        """, (session_id, ctx_json, token_count, now,
              session_id, channel, ctx_json, token_count, now))

    # ── Todos ─────────────────────────────────────────────────────────────────

    def add_todo(self, title: str, project: str = '', priority: int = 5,
                 tags: str = '', due_date=None) -> Optional[int]:
        """Insert a new todo item. Returns the new todo id."""
        now = datetime.now(timezone.utc)
        return self._db.scalar("""
            INSERT INTO memory.Todos (title, project, priority, status, tags, due_date, created_at)
            OUTPUT INSERTED.id
            VALUES (%s, %s, %s, 'open', %s, %s, %s)
        """, (title, project, priority, tags, due_date, now))

    def complete_todo(self, todo_id: int, status: str = 'done') -> bool:
        """Mark a todo as done/completed."""
        now = datetime.now(timezone.utc)
        return self._db.execute("""
            UPDATE memory.Todos SET status=%s, completed_at=%s WHERE id=%s
        """, (status, now, todo_id))

    def update_todo(self, todo_id: int, **fields) -> bool:
        """Update arbitrary todo fields. Allowed: title, project, priority, status, tags, due_date."""
        allowed = {'title', 'project', 'priority', 'status', 'tags', 'due_date'}
        updates = {k: v for k, v in fields.items() if k in allowed}
        if not updates:
            return False
        set_clause = ', '.join(f'{k}=%s' for k in updates)
        params = list(updates.values()) + [todo_id]
        return self._db.execute(
            f'UPDATE memory.Todos SET {set_clause} WHERE id=%s', params
        )

    def delete_todo(self, todo_id: int) -> bool:
        """Hard-delete a todo. Prefer complete_todo() for audit trail."""
        return self._db.execute('DELETE FROM memory.Todos WHERE id=%s', (todo_id,))

    # ── Utility ───────────────────────────────────────────────────────────────

    def _parse_table(self, raw_output: str, columns: List[str]) -> List[Dict]:
        """
        v1.x compat stub. v2 query() returns list[dict] directly.
        Kept so any code that calls _parse_table on raw output still runs.
        Returns empty list — callers should migrate to query().
        """
        _log.debug("_parse_table() called — migrate caller to use query() directly")
        return []

    def ensure_schema(self) -> bool:
        """Create memory schema + core tables if they don't exist."""
        self._db.execute("IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name='memory') EXEC('CREATE SCHEMA memory')")
        tables = {
            'Memories': """CREATE TABLE memory.Memories (
                id BIGINT IDENTITY(1,1) PRIMARY KEY, category NVARCHAR(100) NOT NULL,
                key_name NVARCHAR(255), content NVARCHAR(MAX) NOT NULL,
                importance TINYINT DEFAULT 3, tags NVARCHAR(500), source NVARCHAR(255),
                created_at DATETIME2 DEFAULT GETUTCDATE(), updated_at DATETIME2 DEFAULT GETUTCDATE(),
                expires_at DATETIME2, is_active BIT DEFAULT 1)""",
            'Sessions': """CREATE TABLE memory.Sessions (
                id BIGINT IDENTITY(1,1) PRIMARY KEY, session_key NVARCHAR(255),
                channel NVARCHAR(100), started_at DATETIME2 DEFAULT GETUTCDATE(),
                ended_at DATETIME2, summary NVARCHAR(MAX), token_count INT DEFAULT 0)""",
            'TaskQueue': """CREATE TABLE memory.TaskQueue (
                id BIGINT IDENTITY(1,1) PRIMARY KEY, agent NVARCHAR(100) NOT NULL,
                task_type NVARCHAR(100) NOT NULL, payload NVARCHAR(MAX),
                priority TINYINT DEFAULT 5, status NVARCHAR(50) DEFAULT 'pending',
                created_at DATETIME2 DEFAULT GETUTCDATE(), started_at DATETIME2,
                completed_at DATETIME2, error_log NVARCHAR(MAX), retry_count TINYINT DEFAULT 0)""",
            'KnowledgeIndex': """CREATE TABLE memory.KnowledgeIndex (
                id BIGINT IDENTITY(1,1) PRIMARY KEY, domain NVARCHAR(100) NOT NULL,
                topic NVARCHAR(255) NOT NULL, file_path NVARCHAR(1000),
                summary NVARCHAR(MAX), last_trained DATETIME2, training_count INT DEFAULT 0,
                created_at DATETIME2 DEFAULT GETUTCDATE())""",
            'ActivityLog': """CREATE TABLE memory.ActivityLog (
                id BIGINT IDENTITY(1,1) PRIMARY KEY, event_type NVARCHAR(100) NOT NULL,
                agent NVARCHAR(100), description NVARCHAR(MAX), metadata NVARCHAR(MAX),
                importance TINYINT DEFAULT 3, created_at DATETIME2 DEFAULT GETUTCDATE())""",
        }
        for name, ddl in tables.items():
            self._db.execute(f"""
                IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES
                               WHERE TABLE_SCHEMA='memory' AND TABLE_NAME='{name}')
                BEGIN {ddl} END
            """)
            _log.info(f"ensure_schema: {name} OK")
        return True


# ── Module-level factory (singleton) ─────────────────────────────────────────

_instances: Dict[str, SQLMemory] = {}

def get_memory(backend: str = 'local') -> SQLMemory:
    """Get or create a SQLMemory instance. Singleton per backend."""
    if backend not in _instances:
        _instances[backend] = SQLMemory(backend)
    return _instances[backend]


# ── Self-test ─────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("sql_memory v2.0 — self-test")
    passed = failed = 0

    def t(name, fn):
        global passed, failed
        try:
            r = fn()
            print(f"  ✅ {name}: {r!r:.60}" if r is not None else f"  ✅ {name}: ok")
            passed += 1
        except Exception as e:
            print(f"  ❌ {name}: {e}")
            failed += 1

    mem = get_memory('local')
    t("ping", mem.ping)
    t("remember", lambda: mem.remember('test', '_v2_test', 'v2 self-test', importance=1, tags='test'))
    t("recall", lambda: mem.recall('test', '_v2_test'))
    t("search", lambda: mem.search_memories('v2 self-test'))
    t("log_event", lambda: mem.log_event('selftest', 'sql_memory', 'v2 test'))
    t("queue_task", lambda: mem.queue_task('test_agent', '_v2_task', '{}', priority=1))
    t("forget", lambda: mem.forget('test', '_v2_test'))

    print(f"\n{passed} passed, {failed} failed")
    import sys; sys.exit(1 if failed else 0)
