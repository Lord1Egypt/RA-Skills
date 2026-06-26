# Structured Memory Schemas for Multi-Agent Systems

Typed inter-agent data schemas for reliable coordination in OpenClaw multi-agent fleets.
Use these schemas with `memory_sync.py --schema` to enforce data integrity.

Two backends available: file-based JSON (default) and SQLite (production).

---

## Task Assignment Schema

Used by coordinator agents to assign work to specialist agents.

```json
{
  "type": "task_assignment",
  "version": 1,
  "data": {
    "task_id": "uuid-string",
    "assigned_by": "coordinator",
    "assigned_to": "research",
    "priority": "high|normal|low",
    "title": "string",
    "description": "string",
    "context_keys": ["optional", "shared_memory_keys"],
    "deadline": "ISO-8601-timestamp|null",
    "dependencies": ["optional", "task_ids"]
  }
}
```

**Validation rules:**
- `task_id` must be a non-empty string
- `assigned_to` must be a known agent type
- `priority` must be one of: `critical | high | normal | low`
- `deadline` must be ISO 8601 or `null`

---

## Status Update Schema

Used by agents to report progress on assigned tasks.

```json
{
  "type": "status_update",
  "version": 1,
  "data": {
    "task_id": "uuid-string",
    "agent_id": "research",
    "status": "in_progress|blocked|completed|failed",
    "progress_pct": 0.0,
    "message": "human-readable status",
    "blockers": ["optional", "list_of_issues"],
    "artifacts": ["optional", "list_of_file_paths"],
    "timestamp": "ISO-8601-timestamp"
  }
}
```

**Validation rules:**
- `status` must be one of the valid enum values
- `progress_pct` must be 0.0–100.0 or -1 (unknown)
- `blockers` must be empty or omitted when `status` is `completed`

---

## Coordination Message Schema

Used for general inter-agent communication.

```json
{
  "type": "coordination_message",
  "version": 1,
  "data": {
    "message_id": "uuid-string",
    "sender": "agent-name",
    "recipient": "agent-name|*broadcast*",
    "subject": "short subject line",
    "body": "message content",
    "priority": "normal|high|critical",
    "reply_to": "message_id|null",
    "timestamp": "ISO-8601-timestamp"
  }
}
```

---

## Research Finding Schema

Used by research agents to share findings in structured format.

```json
{
  "type": "research_finding",
  "version": 1,
  "data": {
    "topic": "search-topic",
    "summary": "text-summary",
    "confidence": 0.0,
    "sources": [{"url": "string", "title": "string", "relevance": 0.0}],
    "tags": ["keyword1", "keyword2"],
    "timestamp": "ISO-8601-timestamp"
  }
}
```

**Validation rules:**
- `confidence` must be 0.0–1.0
- Each source must have a `url` field

---

## Builder Output Schema

Used by builder agents to share code or artifacts.

```json
{
  "type": "builder_output",
  "version": 1,
  "data": {
    "task_id": "uuid-string",
    "language": "python|javascript|bash|etc.",
    "files": [
      {
        "path": "relative/file/path",
        "purpose": "description of file role",
        "lines": 123
      }
    ],
    "test_results": {"passed": 0, "failed": 0, "skipped": 0},
    "dependencies": ["package1", "package2"],
    "timestamp": "ISO-8601-timestamp"
  }
}
```

---

## Audit Report Schema

Used by auditor agents to report review findings.

```json
{
  "type": "audit_report",
  "version": 1,
  "data": {
    "task_id": "uuid-string",
    "reviewed_by": "auditor",
    "verdict": "pass|pass_with_warnings|fail",
    "findings": [
      {
        "severity": "critical|high|medium|low|info",
        "category": "security|quality|compliance|style",
        "description": "text",
        "location": "file:line or reference",
        "recommendation": "text"
      }
    ],
    "overall_score": 0.0,
    "timestamp": "ISO-8601-timestamp"
  }
}
```

**Validation rules:**
- `verdict` must be one of the valid enum values
- `overall_score` must be 0.0–100.0
- `findings` entries must have a `severity` value

---

## Backend Comparison

| Feature | File (default) | SQLite (--backend sqlite) |
|---------|---------------|--------------------------|
| Dependencies | None (std lib) | None (stdlib sqlite3) |
| Concurrency | File locking (serial) | WAL mode (concurrent R/W) |
| Transactions | None (atomic replace) | ACID (full rollback) |
| Data Format | JSON file | SQLite DB (binary) |
| Max throughput | ~50 ops/sec | ~10,000 ops/sec |
| Migration | N/A | `--migrate-to-sqlite` from file |
| Space reclamation | N/A | `--compact` (VACUUM) |

**Switch to SQLite when:** running 3+ concurrent agents, expecting >100 operations/minute,
need ACID transaction guarantees, or deploying to production.

---

## Using Schemas with memory_sync.py

```bash
# Write typed data with schema validation (file backend)
python scripts/memory_sync.py --write 'coordinator:current_task:{
  "type": "task_assignment",
  "version": 1,
  "data": {
    "task_id": "t001",
    "assigned_by": "coordinator",
    "assigned_to": "research",
    "priority": "high",
    "title": "Research ClawHub trends",
    "description": "Analyze current marketplace",
    "context_keys": [],
    "deadline": null,
    "dependencies": []
  }
}' --schema task_assignment

# Read data
python scripts/memory_sync.py --read 'research:search_results'

# List available schemas
python scripts/memory_sync.py --list-schemas
```

## Migration: File → SQLite

To migrate an existing file-based shared memory to SQLite:

```bash
python scripts/memory_sync.py --migrate-to-sqlite ./shared_memory
```

This reads the current `shared_data.json`, creates `shared_memory_sqlite/shared_memory.sqlite`
with WAL mode, and copies all keys plus agent stats. After migration:

```bash
python scripts/memory_sync.py --backend sqlite --path ./shared_memory_sqlite --init
python scripts/memory_sync.py --backend sqlite --path ./shared_memory_sqlite --stats
```

To switch an existing deployment, update your config.json:
```json
{
  "sharedMemory": {
    "backend": "sqlite",
    "path": "/data/.openclaw/shared_memory_sqlite",
    "syncInterval": 5
  }
}
```

---

## Utilities

List all shared memory keys:
```bash
# All keys
python scripts/memory_sync.py --keys

# Keys for a specific agent
python scripts/memory_sync.py --keys research
```

Count keys per agent:
```bash
python scripts/memory_sync.py --count-by-agent
```

SQLite space reclamation:
```bash
python scripts/memory_sync.py --backend sqlite --compact
```

---

## Schema Versioning

Schemas use integer versions. When a schema changes:
1. Bump `version` in the data payload
2. New agents can handle both old and new versions
3. Backward-compatible changes: bump minor
4. Breaking changes: bump major