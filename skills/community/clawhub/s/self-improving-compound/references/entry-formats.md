# Entry formats

Use the bundled `scripts/learnings.py` when possible. Durable entries are SQLite-backed in `learning/memory_tree/chunks.db`; the markdown examples below are the export format and manual fallback.

## Pattern-Key naming convention

All Pattern-Keys **must use namespaced format**: `project:key` or `domain:key`.
This prevents collisions between unrelated contexts.

| ❌ Avoid | ✅ Use instead |
|----------|---------------|
| `migration` | `db:migration` |
| `rate-limit` | `api:rate-limit` |
| `layer-cache` | `docker:layer-cache` |
| `timeout` | `network:timeout` |
| `auth` | `api:auth-flow` or `project-alpha:auth` |

## Correction entry

Stored in SQLite. Exported markdown may look like:

```markdown
### COR-YYYYMMDD-XXX (YYYY-MM-DD) [Pattern-Key: db:migration]
- **Type**: COR
- **Summary**: What I got wrong
- **Details**: Correct answer and context
- **Status**: pending
```

## Learning entry

Stored in SQLite. Exported markdown may look like:

```markdown
### LRN-YYYYMMDD-XXX (YYYY-MM-DD) [Pattern-Key: api:rate-limit]
- **Type**: LRN
- **Summary**: One-line summary of the lesson
- **Details**: What happened, what was wrong or surprising, and what is now known to be true
```

## Error entry

Stored in SQLite. Exported markdown may look like:

```markdown
### ERR-YYYYMMDD-XXX (YYYY-MM-DD) [Pattern-Key: docker:layer-cache]
- **Type**: ERR
- **Summary**: One-line description of the failure
- **Details**: Command, tool, API, or environment details
```

## Feature request entry

Stored in SQLite. Exported markdown may look like:

```markdown
### FTR-YYYYMMDD-XXX (YYYY-MM-DD) [Pattern-Key: tooling:csv-export]
- **Type**: FTR
- **Summary**: One-line summary of the request
- **Details**: Why the capability matters and a concrete starting point
```

## Status guidance

- `pending` — captured, not yet addressed
- `in_progress` — being worked on now
- `resolved` — issue fixed or lesson integrated
- `wont_fix` — intentionally not addressing it
- `promoted` — distilled into project memory
- `promoted_to_skill` — extracted into a reusable skill
