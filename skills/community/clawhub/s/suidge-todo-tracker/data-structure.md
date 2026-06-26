# Data Structure

## Schema

**Location**: `memory/todo.json`

```json
{
  "items": [
    {
      "id": "todo_001",
      "description": "Follow up on project X",
      "created_at": "2026-03-21T18:00:00+08:00",
      "follow_up_time": "2026-03-22T10:00:00+08:00",
      "priority": "high",
      "status": "pending",
      "context": "User mentioned this during meeting",
      "reminded": false,
      "completed_at": null,
      "cancelled_at": null
    }
  ]
}
```

## Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique identifier (format: `todo_XXX`) |
| `description` | string | Yes | What to follow up on |
| `created_at` | ISO 8601 | Yes | When item was created |
| `follow_up_time` | ISO 8601 | Yes | When to remind user |
| `priority` | string | No | `high`, `medium`, `low` (default: `medium`) |
| `status` | string | Yes | `pending`, `completed`, `cancelled` |
| `context` | string | No | Additional context for the item |
| `reminded` | boolean | Yes | Whether user has been reminded |
| `completed_at` | ISO 8601 | No | When completed (null if pending) |
| `cancelled_at` | ISO 8601 | No | When cancelled (null if not cancelled) |

## Status Lifecycle

```
pending --(complete)--> completed --(24h)--> deleted
   |
   --(cancel)--> cancelled --(24h)--> deleted
```

## Time Format

All times must be ISO 8601 with timezone:
- Format: `YYYY-MM-DDTHH:MM:SS+HH:MM`
- Example: `2026-03-22T10:00:00+08:00`
