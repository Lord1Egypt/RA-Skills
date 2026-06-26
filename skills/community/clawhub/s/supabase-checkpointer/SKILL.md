---
name: supabase-checkpointer
description: Durable LangGraph checkpointing via Supabase REST API (PostgREST) — no direct Postgres connection needed. Use when deploying LangGraph graphs to ephemeral platforms (Railway, Fly, Cloud Run) where in-memory state is lost on redeploy, and you need interrupt/resume to survive process death. Works with any Supabase project using the existing service role key.
---

# Supabase REST Checkpointer for LangGraph

## Problem

LangGraph's `MemorySaver` stores state in-process. Ephemeral deployments (Railway, Fly, etc.) kill processes on redeploy, losing all interrupted graph state. `PostgresSaver` needs a direct Postgres connection string, which may not be available.

## Solution

A `BaseCheckpointSaver` implementation that stores checkpoints via Supabase's PostgREST API using the existing Supabase client. No direct Postgres connection needed.

## Setup

### 1. Create Tables

Run `scripts/create_tables.sql` in Supabase (via SQL editor or `exec_sql` RPC):

```sql
CREATE TABLE langgraph_checkpoints (
    thread_id TEXT NOT NULL,
    checkpoint_ns TEXT NOT NULL DEFAULT '',
    checkpoint_id TEXT NOT NULL,
    parent_checkpoint_id TEXT,
    type TEXT,
    checkpoint JSONB NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT now(),
    PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id)
);

CREATE TABLE langgraph_writes (
    thread_id TEXT NOT NULL,
    checkpoint_ns TEXT NOT NULL DEFAULT '',
    checkpoint_id TEXT NOT NULL,
    task_id TEXT NOT NULL,
    idx INTEGER NOT NULL,
    channel TEXT NOT NULL,
    type TEXT,
    blob JSONB,
    PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id, task_id, idx)
);
```

### 2. Use the Checkpointer

```python
from supabase import create_client
from supabase_checkpointer import SupabaseCheckpointer

client = create_client(url, key)
checkpointer = SupabaseCheckpointer(client)
graph = builder.compile(checkpointer=checkpointer)
```

### 3. Fallback Chain (recommended)

```python
def _create_checkpointer():
    # 1. Try Supabase (durable across redeploys)
    try:
        from supabase_checkpointer import SupabaseCheckpointer
        client = get_supabase_client()
        if client:
            return SupabaseCheckpointer(client)
    except Exception:
        pass

    # 2. Try SQLite (survives process restarts within same deploy)
    try:
        from langgraph.checkpoint.sqlite import SqliteSaver
        import sqlite3
        return SqliteSaver(sqlite3.connect("checkpoints.db", check_same_thread=False))
    except Exception:
        pass

    # 3. Fallback: in-memory (lost on restart)
    from langgraph.checkpoint.memory import MemorySaver
    return MemorySaver()
```

## Implementation

The full implementation is in `scripts/supabase_checkpointer.py`. It implements all required `BaseCheckpointSaver` methods:

- `put()` — Upsert checkpoint to `langgraph_checkpoints`
- `put_writes()` — Upsert pending writes to `langgraph_writes`
- `get_tuple()` — Fetch latest checkpoint + pending writes for a thread
- `list()` — Iterate checkpoints for a thread (time-travel)

All data serialized as JSONB. Uses `json.dumps(obj, default=str)` for non-serializable types.

## Key Details

- **Thread isolation:** Each graph run uses a unique `thread_id` in the config
- **Checkpoint ordering:** Uses `created_at DESC` for latest checkpoint lookup
- **Write deduplication:** Composite primary key prevents duplicate writes
- **Error tolerance:** All operations wrapped in try/except — logs errors but doesn't crash the graph
- **No async required:** Uses synchronous Supabase client (PostgREST over HTTP)
