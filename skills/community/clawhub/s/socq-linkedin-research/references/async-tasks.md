# Asynchronous Tasks

Submitting an endpoint creates a background task. A successful submission is not a completed collection.

Use this state machine:

```text
queued -> running -> succeeded
                  -> failed
```

- MCP compact mode: call `socq_execute`, then `socq_get_task`.
- MCP typed mode: call the platform tool, then `socq_get_task`.
- CLI: add `--wait`, or run `socq task wait TASK_ID`.
- REST: submit with `POST /v1/{platform}/{resource}`, then poll `GET /v1/tasks/{task_id}`.

Request the fixed result contract by default:

- MCP polling: pass `view: "standard"`; typed tools may pass `_result_view: "standard"` and optional `_result_fields`.
- CLI: pass `--result-view standard`; use `--result-fields id,url,author.username` only when a smaller projection is useful.
- REST: poll `GET /v1/tasks/{task_id}?view=standard`; `fields` accepts at most 50 comma-separated fields or dot paths.

The standard view keeps every declared field, including nullable fields, and excludes raw and unstable extra data. Use `full` only for V1 compatibility or troubleshooting. Download task files when the complete source payload is required.

When this Skill submits a new task, include `_request_source: "skill"` in MCP execution arguments, `--request-source skill` in CLI execution commands, or `X-Socq-Source: skill-rest` in REST requests. Polling calls do not need the marker.

MCP execution returns immediately by default. `_wait_seconds` or `wait_seconds` may wait for at most 30 seconds; an unfinished call still returns the task ID. Continue polling rather than resubmitting.

When retrying a submission after a network error, reuse the same idempotency key. The same key and input return the original task; changing the input with the same key produces a conflict.
