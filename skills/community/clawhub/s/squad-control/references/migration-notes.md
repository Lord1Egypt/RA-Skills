# Migration Notes (v1.1.6+ polling updates)

## What changed

- Poll script output is now a single structured envelope:
  - `POLL_RESULT:`
  - `<json>` with `pending`, `review.tasks`, `stuck.tasks`, `counts`
- Legacy section outputs (`PENDING_TASKS:`, `REVIEW_TASKS:`, `STUCK_TASKS:`) are no longer emitted.
- Poll script now includes overlap lock, retries, and timeout controls.

## Consumer update checklist

1. Update parser to look for `POLL_RESULT:` first.
2. Parse the next line as JSON.
3. Route tasks by:
   - `pending.tasks`
   - `review.tasks`
   - `stuck.tasks`
4. Keep `HEARTBEAT_OK` handling unchanged.

## Recommended backward-compatible parser strategy

- If output starts with `POLL_RESULT:`, use envelope parser.
- Else, fallback to legacy section parser (for older skill versions).

## New optional env vars

- `SC_POLL_LOCK_TTL_SEC`
- `SC_POLL_CONNECT_TIMEOUT_SEC`
- `SC_POLL_MAX_TIME_SEC`
- `SC_POLL_RETRIES`
- `SC_POLL_RETRY_DELAY_SEC`
- `SC_REVIEWER_AGENT_ID`
- `SC_DEFAULT_BRANCH`

## Testing

Run:

```bash
~/.openclaw/skills/squad-control/scripts/run-tests.sh
```
