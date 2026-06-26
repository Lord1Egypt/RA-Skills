---
name: sql-memory
description: "Semantic memory layer for OpenClaw agents. Use when: (1) persisting agent memories with importance scoring, (2) hierarchical memory rollups (daily→weekly→monthly→yearly), (3) queuing tasks for agents, (4) logging activity and audit trails, (5) managing knowledge bases with semantic search. Provides remember/recall/search/queue_task/log_event APIs. Built on sql-connector for reliable parameterized SQL execution."
---

# SQL Memory Skill
> Semantic memory layer for OpenClaw agents

## Overview

Provides agent-friendly memory operations: remember, recall, search, forget, plus task queue management, knowledge indexing, activity logging, and hierarchical memory rollups. All operations go through the SQL Connector skill for reliable, parameterized SQL execution.

See `scripts/sql_memory.py` for full implementation.

## Dependencies

- **sql-connector** — provides the underlying database connection and query execution

## Quick Start

```python
from sql_memory import SQLMemory, get_memory

mem = get_memory('cloud')

# Remember something
mem.remember('facts', 'vex_timezone', 'VeX is in EST/EDT timezone', importance=7)

# Recall it
entry = mem.recall('facts', 'vex_timezone')

# Search across all memories
results = mem.search_memories('timezone')

# Queue a task
mem.queue_task('nlp_agent', 'analyze_document', '{"doc": "..."}', priority=3)

# Log an event
mem.log_event('training_complete', 'nlp_agent', 'Finished training cycle 42')

# Store knowledge
mem.store_knowledge('stamps', 'inverted_jenny', 'Rare 1918 misprint...', 'catalog')
```

## Schema

All tables live in the `memory` schema (SQL Server database):

| Table | Purpose |
|-------|---------|
| `memory.Memories` | Long-term curated memories with importance scoring |
| `memory.TaskQueue` | Task queue for agent work items |
| `memory.ActivityLog` | Event/activity logging for audit trail |
| `memory.KnowledgeIndex` | Domain-specific knowledge store |
| `memory.Sessions` | Session tracking for agents |

## Memory Rollups

Hierarchical consolidation keeps memories fresh and relevant:

```
Daily memories → Weekly rollup (Sundays 3AM)
Weekly rollups → Monthly rollup (1st of month)
Monthly → Quarterly (Jan/Apr/Jul/Oct)
Quarterly → Yearly (Jan 1st)
```

Each rollup:
1. Summarizes source entries
2. Creates a consolidated entry with back-references
3. Reduces importance of source entries
4. Tags sources as `rolled_up`

### Importance Scale

| Level | Meaning | Example |
|-------|---------|---------|
| 1-2 | Ephemeral, archive | Old workspace file |
| 3-4 | Context, nice-to-know | Debug notes |
| 5-6 | Standard operational | Task completion |
| 7-8 | Important milestone | Architecture decision |
| 9 | Critical | System design choice |
| 10 | Permanent | Core identity/values |

## API Reference

### Memory Operations

| Method | Description | Example |
|--------|-------------|---------|
| `remember(cat, key, content, importance, tags)` | Store a memory | `mem.remember('facts', 'name', 'Oblio', 7)` |
| `recall(cat, key)` | Retrieve a memory | `mem.recall('facts', 'name')` |
| `search_memories(query, limit)` | Semantic search | `mem.search_memories('timezone', limit=5)` |
| `forget(cat, key)` | Delete a memory | `mem.forget('facts', 'name')` |

### Task Queue

| Method | Description |
|--------|-------------|
| `queue_task(agent, type, payload, priority)` | Add a task |
| `claim_task(id)` | Mark task as processing |
| `complete_task(id, result)` | Mark task as completed |
| `fail_task(id, error, retries, max)` | Fail with retry logic |

### Activity Logging

| Method | Description |
|--------|-------------|
| `log_event(type, agent, detail, extra)` | Log an activity |
| `get_recent_activity(hours, agent)` | Query recent events |

## Configuration

Uses the same environment variables as sql-connector:

```
SQL_CLOUD_SERVER=sql5112.site4now.net
SQL_CLOUD_DATABASE=db_99ba1f_memory4oblio
SQL_CLOUD_USER=...
SQL_CLOUD_PASSWORD=...

SQL_LOCAL_SERVER=10.0.0.110
SQL_LOCAL_DATABASE=Oblio_Memories
SQL_LOCAL_USER=sa
SQL_LOCAL_PASSWORD=...
```

## Architecture

```
┌──────────────────┐
│   Agents         │ ← OblioAgent subclasses
├──────────────────┤
│   SQLMemory      │ ← Semantic operations (remember/recall/queue/log)
├──────────────────┤
│   SQLConnector   │ ← Generic SQL execution (retry, parameterized, logging)
├──────────────────┤
│   pymssql (TDS)  │ ← Native SQL Server driver
└──────────────────┘
```

## License

MIT

