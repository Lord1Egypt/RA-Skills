# Runbook — wedding-flight

> Execution log schema for debugging and auditing.

---

## Log Entry Schema

```json
{
  "timestamp": "2026-04-14T10:30:00Z",
  "skill": "wedding-flight",
  "playbook": "A",
  "trigger_phrase": "honeymoon flight",
  "params": {
    "origin": "Shanghai",
    "destination": "Maldives",
    "dep_date_start": "2026-05-01",
    "dep_date_end": "2026-05-31",
    "journey_type": "1",
    "sort_type": "2"
  },
  "cli_command": "flyai search-flight --origin 'Shanghai' --destination 'Maldives' --dep-date-start 2026-05-01 --dep-date-end 2026-05-31 --journey-type 1 --sort-type 2",
  "result_count": 5,
  "status": "success",
  "error": null,
  "retry_count": 0,
  "duration_ms": 2300
}
```

## Status Values

| Status | Meaning |
|--------|---------|
| `success` | CLI returned results |
| `no_results` | CLI returned empty list |
| `cli_error` | CLI execution failed |
| `timeout` | CLI did not respond in time |
| `fallback` | Used fallback playbook |

## Retention

- Logs are for debugging only, not shown to users
- No persistent storage required
- Discard after session ends
