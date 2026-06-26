# WHOOP Webhook Events

WHOOP supports real-time event notifications via webhooks. These are **event notifications only** — they tell you something changed, but you must call the API to get the actual data.

## Event Types

| Event | Trigger |
|---|---|
| `recovery.updated` | Recovery score created or recalculated |
| `recovery.deleted` | Recovery removed |
| `sleep.updated` | Sleep data recorded or modified |
| `sleep.deleted` | Sleep removed |
| `workout.updated` | Workout logged or edited |
| `workout.deleted` | Workout removed |

## Payload Format

```json
{
    "user_id": 12345,
    "id": "uuid-or-integer",
    "type": "recovery.updated",
    "trace_id": "unique-trace-id"
}
```

- `user_id` — WHOOP user identifier
- `id` — resource identifier (UUID for sleep/workout, integer cycle_id for recovery)
- `type` — event type string
- `trace_id` — unique ID for deduplication

## Retry Behavior

WHOOP retries failed webhook deliveries **5 times over approximately 1 hour**. After that, the event is dropped.

Recommendation: implement a daily reconciliation cron job that pulls all data for the day to catch any missed webhooks.

## Setup

1. Register your webhook URL in the WHOOP Developer Dashboard
2. URL must be HTTPS and publicly reachable
3. Must respond with 2xx status within a reasonable timeout
4. Use the `trace_id` field to deduplicate events (WHOOP may send duplicates)
