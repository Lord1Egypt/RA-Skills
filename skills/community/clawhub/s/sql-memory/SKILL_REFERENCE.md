# SQL Memory — Skill Reference

**Version:** 2.0 (alpha)  
**Depends on:** [clawbot-sql-connector](https://github.com/High-Falootin/clawbot-sql-connector)  
**Next tier:** [openclaw-sql-dreamer](https://github.com/High-Falootin/openclaw-sql-dreamer)

---

## The Three-Tier Memory Stack

SQL Memory is the middle tier of the OpenClaw persistent memory architecture. Understanding the full stack helps you use each skill at the right level:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│    TIER 3 — SQL Dreamer (openclaw-sql-dreamer)                         │
│    ─────────────────────────────────────────────────────────────        │
│    "Interpretation"                                                     │
│    • Reads high-importance memories nightly                             │
│    • Runs OpenClaw's native dreaming pipeline                           │
│    • Synthesizes patterns, decisions, lasting truths                    │
│    • Stores dream results back to SQL                                   │
│    • Optional: publishes to Confluence                                  │
│                                                                         │
│    TIER 2 — SQL Memory (clawbot-sql-memory)   ← THIS SKILL             │
│    ─────────────────────────────────────────────────────────────        │
│    "Meaning"                                                            │
│    • Stores facts with importance scores (1–10)                         │
│    • Provides semantic search across all stored memories                │
│    • Manages task queues for inter-agent coordination                   │
│    • Maintains immutable activity/audit logs                            │
│    • Tracks todos and agent session state                               │
│    • Hierarchical rollups: daily→weekly→monthly→yearly                  │
│                                                                         │
│    TIER 1 — SQL Connector (clawbot-sql-connector)                      │
│    ─────────────────────────────────────────────────────────────        │
│    "Transport"                                                          │
│    • Parameterized SQL execution (injection-safe, sealed by metaclass)  │
│    • Multi-backend (local, cloud, any named profile)                    │
│    • Retry + exponential backoff on transient failures                  │
│    • All query/execute/scalar primitives                                │
│                                                                         │
│    Foundation: pymssql (native TDS driver) + python-dotenv             │
│    SQL Server: 2019+ / Azure SQL / site4now                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Why this split exists:** SQL Connector handles *how* to talk to SQL Server; SQL Memory handles *what* to store and *how to find it*. SQL Dreamer handles *what it means*. Each tier is independently testable and replaceable.

---

## Data Model

All tables live in the `memory` schema. All timestamps use UTC (`GETUTCDATE()` in SQL, `datetime.now(timezone.utc)` in Python).

### memory.Memories

The primary long-term memory store. Everything your agents learn, decide, observe, or record.

| Column | Type | Default | Notes |
|--------|------|---------|-------|
| `id` | INT IDENTITY | auto | Primary key |
| `category` | NVARCHAR(100) | required | Logical group (e.g. `facts`, `decisions`, `incidents`) |
| `key` | NVARCHAR(255) | required | Unique identifier within category (upsert key) |
| `content` | NVARCHAR(MAX) | required | The memory text |
| `importance` | INT | 3 | 1–10 importance score (see scale below) |
| `tags` | NVARCHAR(500) | `''` | Comma-separated tags for filtering and search |
| `status` | NVARCHAR(50) | `'active'` | `active`, `inactive`, `rolled_up` |
| `created_at` | DATETIME2 | `GETUTCDATE()` | Insertion time (UTC) |
| `updated_at` | DATETIME2 | `GETUTCDATE()` | Last update time (UTC) |

**Upsert behavior:** `remember()` uses a SQL `MERGE` statement — if a row with the same `category` + `key` already exists and is active, it updates the content, importance, and tags. Otherwise, it inserts a new row. You never get duplicates.

**Soft delete:** `forget()` sets `status = 'inactive'` rather than deleting rows. Queries filter on `status = 'active'`. Historical data is preserved.

---

### memory.TaskQueue

Asynchronous task coordination between agents. One agent queues work; another claims and processes it.

| Column | Type | Default | Notes |
|--------|------|---------|-------|
| `id` | INT IDENTITY | auto | Primary key |
| `agent` | NVARCHAR(100) | required | Target agent name |
| `task_type` | NVARCHAR(100) | required | Task class/type (agent-defined) |
| `payload` | NVARCHAR(MAX) | `''` | JSON payload for the task |
| `priority` | INT | 5 | 1 = critical, 9 = background |
| `status` | NVARCHAR(50) | `'pending'` | `pending`, `processing`, `completed`, `failed` |
| `retries` | INT | 0 | Retry counter |
| `model_hint` | NVARCHAR(100) | `''` | Optional LLM hint for the consuming agent |
| `created_at` | DATETIME2 | `GETUTCDATE()` | Creation time (UTC) |
| `updated_at` | DATETIME2 | `GETUTCDATE()` | Last state change (UTC) |
| `claimed_at` | DATETIME2 | NULL | When an agent claimed this task |
| `completed_at` | DATETIME2 | NULL | When it completed or failed |
| `error` | NVARCHAR(MAX) | `''` | Error message on failure |

**Priority values (numeric):**

| Value | Name | Use For |
|-------|------|---------|
| 1–2 | Critical/High | Blocking work, urgent processing |
| 5 | Medium (default) | Standard agent tasks |
| 7–9 | Low/Background | Non-blocking, best-effort |

`queue_task()` also accepts string priority names: `'critical'`, `'high'`, `'medium'`, `'low'`, `'free'`.

---

### memory.ActivityLog

Immutable append-only event log. Every significant agent action should be recorded here.

| Column | Type | Default | Notes |
|--------|------|---------|-------|
| `id` | INT IDENTITY | auto | Primary key |
| `event_type` | NVARCHAR(100) | required | What happened (e.g. `task_complete`, `error`) |
| `agent` | NVARCHAR(100) | `''` | Which agent logged this |
| `description` | NVARCHAR(MAX) | `''` | Human-readable detail |
| `metadata` | NVARCHAR(MAX) | `''` | JSON or structured extra data |
| `importance` | INT | 3 | Same 1–10 scale as Memories |
| `created_at` | DATETIME2 | `GETUTCDATE()` | Immutable log time (UTC) |

**Key principle:** ActivityLog rows are never updated or deleted. This is your audit trail.

---

### memory.Sessions

Agent session state and context persistence across interactions.

| Column | Type | Default | Notes |
|--------|------|---------|-------|
| `id` | INT IDENTITY | auto | Primary key |
| `session_key` | NVARCHAR(255) | required | Unique session identifier (upsert key) |
| `agent` | NVARCHAR(100) | `''` | Agent owning this session |
| `status` | NVARCHAR(50) | `'active'` | `active`, `closed` |
| `metadata` | NVARCHAR(MAX) | `''` | JSON session context |
| `started_at` | DATETIME2 | `GETUTCDATE()` | Session start (UTC) |
| `ended_at` | DATETIME2 | NULL | Session close time |

**Use case:** Store conversation state, token counts, mid-session context, or cross-call agent state that needs to survive restarts.

---

### memory.KnowledgeIndex

Domain-specific knowledge store. Separate from agent memories — use this for trained/indexed reference material.

| Column | Type | Default | Notes |
|--------|------|---------|-------|
| `id` | INT IDENTITY | auto | Primary key |
| `domain` | NVARCHAR(100) | required | Knowledge domain (e.g. `stamps`, `legal`, `inventory`) |
| `key` | NVARCHAR(255) | required | Topic identifier (upsert key within domain) |
| `content` | NVARCHAR(MAX) | required | The knowledge content |
| `source` | NVARCHAR(255) | `''` | Origin/citation |
| `tags` | NVARCHAR(500) | `''` | Comma-separated tags |
| `created_at` | DATETIME2 | `GETUTCDATE()` | Creation time (UTC) |

**Difference from Memories:** KnowledgeIndex stores *reference material* (documents, domain facts, indexed content). Memories stores *agent experiences* (what happened, decisions made, findings). Use both.

---

### memory.Todos

Structured task tracking. Supports priorities, projects, due dates, and status tracking.

| Column | Type | Default | Notes |
|--------|------|---------|-------|
| `id` | INT IDENTITY | auto | Primary key (returned by `add_todo()`) |
| `title` | NVARCHAR(500) | required | Todo item text |
| `description` | NVARCHAR(MAX) | `''` | Extended notes |
| `priority` | INT | 3 | 1 = urgent, 5 = normal, 9 = low |
| `status` | NVARCHAR(50) | `'open'` | `open`, `done`, `cancelled`, custom |
| `tags` | NVARCHAR(500) | `''` | Comma-separated tags |
| `created_at` | DATETIME2 | `GETUTCDATE()` | Creation time (UTC) |
| `updated_at` | DATETIME2 | `GETUTCDATE()` | Last update time (UTC) |
| `closed_at` | DATETIME2 | NULL | When item was completed/closed |

---

## Importance Scale

The importance score is used across `Memories` and `ActivityLog`. It determines:
- Which memories are promoted during rollups
- Which memories SQL Dreamer reads for nightly synthesis
- How long memories survive compression cycles

| Score | Tier | Meaning | Examples |
|-------|------|---------|---------|
| 1 | Ephemeral | Discard soon | Temporary scratch notes, debug output |
| 2 | Transient | Short-lived utility | One-off lookup results |
| 3 | Routine | Default context (default value) | Task logs, status messages |
| 4 | Context | Nice-to-know | Debug traces, minor observations |
| 5 | Significant | Standard operational fact | Task completions, research notes |
| 6 | Noteworthy | Worth preserving | Patterns observed, useful references |
| 7 | Strategic | Milestone-level | Architecture decisions, system changes |
| 8 | Important | High-value | Process improvements, key findings |
| 9 | Critical | Near-permanent | Blocking issues, security decisions |
| 10 | Permanent | Never roll up | Core identity, foundational truths |

**Practical guide:**
- Agent task output → `5`
- User preference you observed → `7`
- Architectural decision → `7–8`
- Something that must never be forgotten → `9–10`
- Default (if unsure) → `3` (the default)

**SQL Dreamer threshold:** Dreamer reads memories with `importance >= 7` by default. If you want a memory to influence nightly synthesis, score it 7+.

---

## API Reference

### Factory Function

#### `get_memory(backend='local') → SQLMemory`

Singleton factory. Returns a cached `SQLMemory` instance per backend — safe to call from multiple modules.

```python
from sql_memory import get_memory

mem = get_memory('local')    # local SQL Server
mem = get_memory('cloud')    # cloud SQL Server (Azure, site4now, etc.)
```

The `backend` string maps to environment variable prefixes: `SQL_LOCAL_*` or `SQL_CLOUD_*` in your `.env`.

---

### Class: `SQLMemory`

```python
from sql_memory import SQLMemory

mem = SQLMemory('local')    # or 'cloud'
```

---

### Memory Operations

#### `remember(category, key, content, importance=3, tags='') → bool`

Store or update a memory. Upserts by `category` + `key` — safe to call repeatedly.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `category` | str | required | Logical group (`facts`, `decisions`, `incidents`, etc.) |
| `key` | str | required | Unique identifier within category |
| `content` | str | required | The memory text |
| `importance` | int | 3 | 1–10 importance score |
| `tags` | str | `''` | Comma-separated tags |

**Returns:** `True` on success, `False` on failure.

```python
# Store a decision
mem.remember(
    category='decisions',
    key='arch_db_choice',
    content='Chose SQL Server for persistence: schema flexibility + parameterized safety. Evaluated Postgres, rejected for hosting reasons.',
    importance=8,
    tags='architecture,database,decisions'
)

# Update the same entry later (importance and content updated)
mem.remember('decisions', 'arch_db_choice', 'Updated content', importance=9)
```

---

#### `recall(category, key) → Optional[str]`

Retrieve a specific memory's content by category and key.

**Returns:** Content string if found, `None` if not found or inactive.

```python
content = mem.recall('decisions', 'arch_db_choice')
if content:
    print(f"Found: {content}")
```

---

#### `recall_recent(n=10) → List[Dict]`

Return the N most recently updated active memories across all categories.

**Returns:** List of dicts with keys: `category`, `key_name`, `content`, `importance`, `tags`, `ts`.

```python
recent = mem.recall_recent(5)
for entry in recent:
    print(f"[{entry['importance']}] {entry['category']}/{entry['key_name']}: {entry['content'][:60]}")
```

---

#### `search_memories(keyword, limit=20) → List[Dict]`

Full-text LIKE search across `content`, `tags`, and `key_name`. Results ordered by importance descending, then recency.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `keyword` | str | required | Search term (case-insensitive) |
| `limit` | int | 20 | Maximum results |

**Returns:** List of dicts with keys: `category`, `key_name`, `content`, `importance`, `tags`.

```python
results = mem.search_memories('timezone', limit=5)
for r in results:
    print(f"[{r['importance']}] {r['category']}/{r['key_name']}")
```

---

#### `forget(category, key) → bool`

Soft-delete a memory (sets `status = 'inactive'`). The row is preserved in the database for historical reference; it just won't appear in queries.

```python
mem.forget('test', 'temporary_note')
```

---

### Activity Logging

#### `log_event(event_type, agent, description, metadata='', importance=3) → bool`

Append an event to the immutable activity log.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `event_type` | str | required | Event name (e.g. `task_complete`, `error`, `agent_started`) |
| `agent` | str | required | Agent that generated the event |
| `description` | str | required | Human-readable description |
| `metadata` | str | `''` | JSON or free-form extra data |
| `importance` | int | 3 | 1–10 importance score |

**Returns:** `True` on success.

```python
mem.log_event(
    event_type='research_complete',
    agent='research_agent',
    description='Processed 14 findings for ticket OB-42',
    metadata='{"ticket": "OB-42", "findings_count": 14}',
    importance=5
)
```

---

#### `get_recent_activity(since_hours=24, agent=None) → List[Dict]`

Retrieve recent activity log entries.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `since_hours` | int | 24 | Look back this many hours |
| `agent` | str | None | Filter by agent name (None = all agents) |

**Returns:** List of dicts with keys: `event_type`, `agent`, `description`, `ts`.

```python
# All activity in the last hour
recent = mem.get_recent_activity(since_hours=1)

# One agent's activity over 48 hours
agent_log = mem.get_recent_activity(since_hours=48, agent='research_agent')
```

---

### Task Queue

The task queue enables async coordination between agents. The producer queues work; the consumer claims, processes, and completes or fails it.

#### `queue_task(agent, task_type, payload='{}', priority=5) → Optional[str]`

Insert a new task into the queue.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `agent` | str | required | Target agent name |
| `task_type` | str | required | Task class string (agent-defined) |
| `payload` | str | `'{}'` | JSON payload |
| `priority` | int or str | 5 | Numeric 1–9, or `'critical'`, `'high'`, `'medium'`, `'low'`, `'free'` |

**Returns:** Task ID string if created, `None` on failure.

```python
task_id = mem.queue_task(
    agent='impl_agent',
    task_type='implementation',
    payload='{"ticket": "OB-42", "findings": "..."}',
    priority='high'   # or priority=2
)
```

---

#### `get_pending_tasks(agent, task_types, limit=10) → List[Dict]`

Fetch pending tasks for an agent, ordered by priority (low number first) then age (oldest first).

| Parameter | Type | Description |
|-----------|------|-------------|
| `agent` | str | Agent name |
| `task_types` | List[str] | Task type filter list |
| `limit` | int | Max results |

**Returns:** List of dicts with keys: `id`, `task_type`, `payload`, `priority`, `retry_count`.

```python
tasks = mem.get_pending_tasks(
    agent='impl_agent',
    task_types=['implementation', 'code_review'],
    limit=5
)
for task in tasks:
    print(f"Task {task['id']}: {task['task_type']} (priority={task['priority']})")
```

---

#### `claim_task(task_id) → bool`

Mark a task as `processing`. Call before starting work to prevent double-processing.

```python
mem.claim_task(task_id)
# ... do the work ...
```

---

#### `complete_task(task_id, result='') → bool`

Mark a task as `completed`.

```python
mem.complete_task(task_id, result='Implementation complete — see Jira comment')
```

---

#### `fail_task(task_id, error, retry_count=0, max_retries=3) → bool`

Fail a task. If `retry_count < max_retries`, the task is re-queued as `pending`. If retries are exhausted, it's marked `failed`.

```python
try:
    # ... do work ...
    mem.complete_task(task_id)
except Exception as e:
    mem.fail_task(task_id, error=str(e), retry_count=task['retry_count'])
```

---

#### `get_completed_tasks(since_hours=24, agent=None) → List[Dict]`

Retrieve recently completed or failed tasks for monitoring.

```python
done = mem.get_completed_tasks(since_hours=6, agent='impl_agent')
```

---

### Knowledge Index

Domain-specific reference material, separate from agent memories.

#### `store_knowledge(domain, topic, summary='', file_path='', tags='') → bool`

Store or update a knowledge entry. Upserts by `domain` + `topic`. Increments `training_count` on updates.

```python
mem.store_knowledge(
    domain='stamps',
    topic='inverted_jenny',
    summary='Rare 1918 misprint — airmail stamp with inverted biplane. ~100 known. Value: $500k–$2M',
    tags='rare,1918,error,biplane'
)
```

---

#### `search_knowledge(domain, keyword='') → List[Dict]`

Search knowledge within a domain.

```python
# All stamps knowledge
all_stamps = mem.search_knowledge(domain='stamps')

# Search within domain
rare = mem.search_knowledge(domain='stamps', keyword='rare')
```

---

#### `get_recent_knowledge(n=10) → List[Dict]`

Get the N most recently updated knowledge entries across all domains.

---

### Session Management

#### `get_session_context(session_id) → Optional[Dict]`

Load session context. Returns `None` if the session doesn't exist.

```python
ctx = mem.get_session_context('agent:main:telegram:direct:12345')
if ctx:
    data = ctx['context']   # deserialized dict from JSON
```

---

#### `save_session_context(session_id, context_data, channel='agent', token_count=0) → bool`

Persist session context. Upserts by `session_key`.

```python
mem.save_session_context(
    session_id='agent:main:telegram:direct:12345',
    context_data={'step': 3, 'ticket': 'OB-42', 'findings': [...]},
    channel='telegram',
    token_count=8420
)
```

---

### Todos

#### `add_todo(title, project='', priority=5, tags='', due_date=None) → Optional[int]`

Create a new todo item. Returns the new todo's integer ID.

```python
todo_id = mem.add_todo(
    title='Fix login redirect bug',
    project='TAT',
    priority=2,
    tags='bug,auth',
    due_date='2026-05-01'
)
```

---

#### `complete_todo(todo_id, status='done') → bool`

Mark a todo as done. Accepts custom status strings if needed (`'cancelled'`, `'deferred'`, etc.).

```python
mem.complete_todo(todo_id)
mem.complete_todo(todo_id, status='cancelled')
```

---

#### `update_todo(todo_id, **fields) → bool`

Update any combination of allowed fields: `title`, `project`, `priority`, `status`, `tags`, `due_date`.

```python
mem.update_todo(todo_id, priority=1, tags='bug,auth,urgent')
```

---

#### `delete_todo(todo_id) → bool`

Hard-delete a todo. Prefer `complete_todo()` when you want an audit trail.

---

### Utility

#### `ping() → bool`

Connectivity check. Delegates to the underlying SQLConnector.

```python
if not mem.ping():
    raise RuntimeError("Lost SQL connection")
```

---

#### `ensure_schema() → bool`

Create the memory schema and all tables if they don't exist. Idempotent — safe to call repeatedly.

```python
mem.ensure_schema()   # no-op if tables already exist
```

---

## Rollup System

The rollup system compresses old memories hierarchically to keep the memory store manageable over time — without losing historical context.

### The Compression Ladder

```
New memories land in:  memory.Memories (daily entries)
                           ↓ (every Sunday @ 3AM)
                       Weekly rollup entry
                           ↓ (1st of each month)
                       Monthly rollup entry
                           ↓ (January 1st)
                       Yearly rollup entry
```

### How Each Rollup Works

1. Source entries for the period are collected
2. A consolidated summary entry is created with back-references to source IDs
3. Source entries have their importance reduced
4. Sources are tagged `rolled_up` so they don't trigger re-processing
5. The rollup entry carries the highest importance of its sources

### Rollup Schedule

| Cycle | Trigger | Input | Output |
|-------|---------|-------|--------|
| Daily → Weekly | Every Sunday | Last 7 days of daily entries | 1 weekly summary |
| Weekly → Monthly | 1st of month | Last 4+ weeks of weekly entries | 1 monthly summary |
| Monthly → Yearly | January 1st | Last 12 months of monthly entries | 1 yearly summary |

### What Survives

Memories with `importance >= 9` are **never rolled up** — they're permanent. This is intentional: foundational facts and core identity should never be compressed away.

### Why This Matters for SQL Dreamer

SQL Dreamer queries `memory.Memories` for entries with `importance >= 7`. After rollups, the high-importance condensed summaries are the primary input to nightly dream synthesis. Your rollup quality directly affects dream quality.

---

## Integration With SQL Dreamer

SQL Dreamer is the third tier of the stack. It reads your memories and synthesizes patterns, decisions, and long-term insights through OpenClaw's native dreaming pipeline.

### Data Flow

```
memory.Memories (importance >= 7)
         ↓
  [pre_dream_sql_feed.py runs @ 3AM]
  Curates and formats memories for dreaming
         ↓
  OpenClaw Native Dreamer runs
  (light, REM, and deep phases)
         ↓
  [post_dream_archiver.py runs @ 4AM]
  Stores dream results back to SQL
  (dreams.DreamCorpus, DreamLight, DreamREM, DreamDeep tables)
         ↓
  Optional: confluence_dream_publisher.py
  Publishes dream reports to Confluence
```

### Setting Memories to Feed Dreams

Any memory with `importance >= 7` will be picked up by SQL Dreamer. Be intentional about what you score that high:

```python
# This WILL feed into nightly dream synthesis
mem.remember(
    category='decisions',
    key='arch_choice_cache_layer',
    content='Decided to use Redis for session cache rather than SQL. Reduces write load 60%.',
    importance=8,    # ← will feed dreams
    tags='architecture,redis,cache,performance'
)

# This WILL NOT (importance too low)
mem.remember(
    category='debug',
    key='temp_note',
    content='Remember to check port 5432 after deploy',
    importance=4,    # ← too low for dreamer
)
```

### Installing SQL Dreamer

```bash
clawhub install sql-dreamer
```

After installing, SQL Dreamer needs its own schema (`dreams.*` tables) and a `config/sql_dreamer.yml`. See the **[SQL Dreamer GETTING_STARTED.md](https://github.com/High-Falootin/openclaw-sql-dreamer/blob/main/GETTING_STARTED.md)** for full setup.

---

## Configuration Reference

SQL Memory uses the same environment variable pattern as sql-connector. Variables follow the format:
`SQL_<BACKEND>_<SETTING>` where `<BACKEND>` is your profile name in uppercase.

### Standard Profiles

```env
# ── Local SQL Server ────────────────────────────────────────────
SQL_LOCAL_SERVER=10.0.0.110
SQL_LOCAL_PORT=1433
SQL_LOCAL_DATABASE=db_99ba1f_memory4oblio
SQL_LOCAL_USER=your_username
SQL_LOCAL_PASSWORD=your_password

# ── Cloud SQL Server (Azure, site4now, etc.) ────────────────────
SQL_CLOUD_SERVER=yourserver.database.windows.net
SQL_CLOUD_PORT=1433
SQL_CLOUD_DATABASE=your_cloud_database
SQL_CLOUD_USER=your_cloud_user
SQL_CLOUD_PASSWORD=your_cloud_password

# ── Optional: default backend ───────────────────────────────────
SQL_DEFAULT_BACKEND=local
```

> **Important:** Do not use `SQL_LOCAL_DATABASE=Oblio_Memories` — that was a legacy/dead value from an early config. Use your actual database name.

### Custom Backend Profiles

You can add arbitrary named profiles by following the same pattern:

```env
# Staging environment
SQL_STAGING_SERVER=staging.database.windows.net
SQL_STAGING_PORT=1433
SQL_STAGING_DATABASE=staging_db
SQL_STAGING_USER=staging_user
SQL_STAGING_PASSWORD=staging_pass
```

Then instantiate:

```python
mem = get_memory('staging')    # reads SQL_STAGING_* from .env
```

### .env Location Discovery

The module auto-discovers `.env` by walking up to 5 directory levels from the script's location. It will find `.env` at your workspace root as long as sql-memory is installed within your workspace directory tree.

---

## Design Principles

### UTC Everywhere

All timestamps use UTC — `GETUTCDATE()` in SQL, `datetime.now(timezone.utc)` in Python. No timezone ambiguity, no daylight savings bugs, no regional behavior differences.

### Parameterized Queries Only

No string interpolation in SQL. Ever. Every query uses `%s` placeholders. The SQLConnector metaclass seals this — subclasses cannot override it. This makes SQL injection structurally impossible, not just convention-dependent.

```python
# ✅ Correct (parameterized)
db.query("SELECT * FROM memory.Memories WHERE category = %s", (category,))

# ❌ Wrong (never do this, even in scripts)
db.query(f"SELECT * FROM memory.Memories WHERE category = '{category}'")
```

### Upsert Over Insert

`remember()` and `store_knowledge()` use `MERGE` statements. You never need to check if an entry exists before storing — just call `remember()`. This makes agent code simpler and prevents accidental duplicates.

### Soft Deletes

`forget()` sets `is_active = 0` rather than deleting rows. Historical data is preserved for audit, rollup, and dreamer queries. If you need hard deletes, query the SQL directly.

### Singleton Factory

`get_memory(backend)` returns a cached `SQLMemory` instance per backend. Multiple modules can call `get_memory('local')` and share one connection — no unnecessary reconnections.

```python
# Both calls return the same instance
mem1 = get_memory('local')
mem2 = get_memory('local')
assert mem1 is mem2   # True
```

### Logging

SQL Memory writes to `logs/sql_dbo.log` with UTC timestamps. All `remember`, `forget`, `queue_task`, `claim_task`, `complete_task`, and `fail_task` calls are logged at INFO level. Errors are logged at ERROR level.

---

## Common Patterns

### Pattern 1: Agent Memory Workflow

```python
from sql_memory import get_memory

class ResearchAgent:
    def __init__(self):
        self.mem = get_memory('cloud')
    
    def run_research(self, ticket_id, findings):
        # Log start
        self.mem.log_event('research_started', 'research_agent', f'Starting {ticket_id}', importance=3)
        
        # Store key findings
        for i, finding in enumerate(findings):
            self.mem.remember(
                category='findings',
                key=f'{ticket_id}_finding_{i}',
                content=finding['content'],
                importance=finding.get('importance', 5),
                tags=f'{ticket_id},research'
            )
        
        # Queue implementation task
        task_id = self.mem.queue_task(
            agent='impl_agent',
            task_type='implementation',
            payload=f'{{"ticket": "{ticket_id}", "findings_count": {len(findings)}}}',
            priority='high'
        )
        
        # Log completion
        self.mem.log_event(
            'research_complete', 
            'research_agent', 
            f'{ticket_id}: {len(findings)} findings stored, task {task_id} queued',
            importance=5
        )
```

### Pattern 2: Task Consumer Loop

```python
from sql_memory import get_memory
import json

mem = get_memory('local')

def process_tasks():
    tasks = mem.get_pending_tasks(
        agent='impl_agent',
        task_types=['implementation'],
        limit=10
    )
    
    for task in tasks:
        mem.claim_task(task['id'])
        try:
            payload = json.loads(task['payload'])
            # ... do the work ...
            mem.complete_task(task['id'], result='Success')
        except Exception as e:
            mem.fail_task(task['id'], str(e), retry_count=task['retry_count'])
```

### Pattern 3: Knowledge Base Agent

```python
from sql_memory import get_memory

mem = get_memory('local')

# Index a knowledge domain
for item in catalog_items:
    mem.store_knowledge(
        domain='product_catalog',
        topic=item['sku'],
        summary=item['description'],
        tags=f"{item['category']},{item['brand']}"
    )

# Query it
results = mem.search_knowledge('product_catalog', keyword='vintage')
```

---

## Legacy Compatibility (v1.x → v2.0)

If you have existing code using v1.x-style methods, they still work:

| v1.x Method | v2.0 Status | Notes |
|-------------|-------------|-------|
| `SQLMemory('local')` | ✅ Works | Same constructor |
| `get_memory('local')` | ✅ Works | Same factory |
| `mem.remember(...)` | ✅ Works | Same signature |
| `mem.recall(...)` | ✅ Works | Same return type |
| `mem.execute(raw_sql)` | ⚠️ Returns bool (was string) | Legacy passthrough; prefer `mem._db.execute()` with params |
| `mem.execute_scalar(sql)` | ✅ Works | Delegates to `scalar()` |
| `mem.execute_via_file(sql)` | ✅ Works | Same as `execute()` — file workaround no longer needed |
| `mem._parse_table(raw, cols)` | ⚠️ Returns `[]` always | v2 returns `List[Dict]` directly; migrate callers |

---

## Related Skills

| Skill | Role | Install |
|-------|------|---------|
| **sql-connector** | Transport layer (required) | `clawhub install sql-connector` |
| **sql-memory** | This skill | `clawhub install sql-memory` |
| **sql-dreamer** | Synthesis layer (optional, next) | `clawhub install sql-dreamer` |

---

## Support & Resources

- **GitHub Issues:** https://github.com/VeXHarbinger/clawbot-sql-memory/issues
- **ClawHub Registry:** https://clawhub.ai/skills/sql-memory
- **sql-connector:** https://github.com/VeXHarbinger/clawbot-sql-connector
- **SQL Dreamer:** https://github.com/High-Falootin/openclaw-sql-dreamer
- **Reference implementation:** https://github.com/VeXHarbinger/oblio-heart-and-soul

---

**Last updated:** 2026-04-28  
**Version:** 2.0 (alpha — feedback period open)  
**Status:** In active production use. API stable for 30-day community feedback window.
