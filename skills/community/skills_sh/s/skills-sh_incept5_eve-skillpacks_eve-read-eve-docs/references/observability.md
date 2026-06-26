# Observability + Cost Tracking

## Use When
- You need to trace a request or job through the system using correlation IDs.
- You need to inspect execution receipts, token usage, or cost breakdowns.
- You need analytics dashboards for org health, job stats, or pipeline metrics.
- You need to configure OpenTelemetry or inspect provider/model availability.

## Load Next
- `references/cli.md` for full analytics and admin CLI syntax.
- `references/jobs.md` for job lifecycle phases and attempt details.
- `references/deploy-debug.md` for real-time log streaming and debugging.

## Ask If Missing
- Confirm the org ID for analytics queries (all analytics are org-scoped).
- Confirm the time window for usage and cost reports (default varies by endpoint).
- Confirm whether OTEL is enabled and where the collector endpoint is.

## Correlation IDs

Every request carries `x-eve-correlation-id`. If missing on inbound, the API generates a UUID and echoes it back. The ID propagates: API -> Orchestrator -> Worker -> Runner.

Standard structured log fields:

| Field | Always | When Available |
|---|---|---|
| `timestamp`, `level`, `service`, `message` | Yes | -- |
| `correlation_id`, `trace_id` | Yes | -- |
| `job_id`, `attempt_id`, `event_id` | -- | Yes |

Job execution lifecycle events are also written to `execution_logs` with correlation fields in the lifecycle `meta` object.

Embedded conversations (project-scoped chat threads) carry a normalized event
timeline (`conversation_events`, ids `cevt_*`) alongside the message stream.
Standard kinds include `user.message`, `assistant.message`, `tool.call`,
`tool.result`, `status.changed`, `progress`, `error`, and `final.result`; apps
may emit custom kinds. Each event records `job_id`, `attempt_id`,
`workflow_step`, and `source` for cross-correlation. Stream via the SSE
endpoint or tail with `eve thread events <id> --follow`. See
`agents-teams.md` and `eve-sdk.md` for the full surface.

### Event -> Trigger Visibility

Events now record why they did or did not fan out to workflows:

| Field | Meaning |
|---|---|
| `trigger_match_count` | Number of triggers that matched (0 = no match) |
| `triggers_evaluated` | Array of `{type, name, matched, reason?}` for each trigger checked |

```bash
eve event show <event-id>
#   Triggers:    matched 1 of 3 evaluated
#   Trigger Evaluations:
#     workflow:process-document - MATCHED
#     workflow:reindex          - no match (event_type mismatch)
```

`eve event list` shows a compact `MATCH` column (`1/3`). Manifest sync
(`eve project sync`) now validates trigger definitions and surfaces warnings
for unrecognized event types, invalid GitHub events, unknown system events,
and missing cron schedules — catching trigger wiring mistakes before the
first event arrives. See `events.md` for the full event + trigger surface.

For deployed app services, use environment logs and request diagnostics:

```bash
eve env logs <project> <env> <service> --follow --since 30
eve env logs <project> <env> <service> --grep req_01h...
eve env logs <project> <env> <service> --filter req_id=req_01h... --filter level=error
eve env diagnose <project> <env> --request req_01h... --window 120 --json
```

`eve env logs --filter k=v` is repeatable, ANDs filters together, and matches
JSON log fields exactly. Dotted paths such as `req.path=/api/items` read nested
JSON fields. Numeric and boolean values are coerced (`--filter status=500`
matches `{"status":500}`). Non-JSON lines fall back to `--grep` substring
semantics. `--follow` streams through the API using SSE, emits pod-change
notifications when a matching pod rolls, and combines with `--filter` for live
structured queries. `eve env diagnose --request <req_id>` integrates app-service
logs, K8s events, deploy metadata at request time, optional audit rows, and
trace pointers into one JSON payload — no more stitching four commands
together by hand.

## Execution Receipts

Receipts capture timing, token usage, and cost breakdowns per attempt. Assembled from lifecycle events plus `llm.call` usage events.

- `llm.call` events contain usage only (no content). Emitted by harnesses after each provider call.
- `eve job follow` displays live cost totals when `llm.call` events stream.

```bash
eve job receipt <job-id>              # View cost receipt for a job
eve job compare <job-id-1> <job-id-2> # Compare receipts across jobs
```

API: `GET /jobs/{job_id}/receipt`

### Receipt Fields

| Field | Description |
|---|---|
| `duration_ms` | Wall-clock execution time |
| `input_tokens` | Total input tokens across all LLM calls |
| `output_tokens` | Total output tokens across all LLM calls |
| `total_cost` | Computed cost from rate card |
| `model` | Model used (may differ from requested if bridged) |
| `provider` | Resolved provider |

### Admin Receipt Recompute

```bash
eve admin receipts recompute                        # Recompute all
eve admin receipts recompute --since 2026-01-01     # From date
eve admin receipts recompute --project proj_xxx     # Single project
eve admin receipts recompute --dry-run              # Preview only
```

## Email Delivery Events

Outbound mail through the platform mailer is durably tracked in
`email_delivery_events`. AWS SES posts bounce/complaint/delivery notifications
via SNS to `POST /webhooks/ses-feedback`; the controller parses both
`application/json` and SNS's `text/plain` body and inserts one row per
(SNS `MessageId`, SES `eventType`, recipient) so retries do not duplicate.

Key columns: `recipient`, `event_type` (`Bounce` | `Complaint` | `Delivery` |
`Reject`), `bounce_type`, `bounce_subtype`, `diagnostic`, `ses_message_id`,
`rfc_message_id`, `raw_payload`, `received_at`. Indexed by `(recipient,
received_at DESC)` and `ses_message_id`.

Before send, the mailer pre-flights the SES account-level suppression list and
short-circuits with a loud structured error if the recipient is suppressed.
Mailer logs are JSON with `recipient`, `message-id`, and outcome.

```bash
eve admin email bounces list                                # Recent events
eve admin email bounces list --recipient user@example.com   # Lookup by address
eve admin email bounces list --event-type Bounce --limit 50 --json
```

## Analytics Dashboard

All analytics are org-scoped. Return aggregate counters, not per-item listings. Use `--json` for machine-readable output.

```bash
eve analytics summary --org org_xxx [--window 7d]
eve analytics jobs --org org_xxx [--window 7d]
eve analytics pipelines --org org_xxx [--window 7d]
eve analytics env-health --org org_xxx
```

| Endpoint | Returns |
|---|---|
| `summary` | Org-wide aggregate (jobs, pipelines, envs) |
| `jobs` | Job counters: created, completed, failed, active |
| `pipelines` | Pipeline success rates and durations |
| `env-health` | Environment snapshot: total, healthy, degraded, unknown |

`--window` accepts relative durations: `7d`, `24h`, `30d`.

## Platform Sentinel

Platform Sentinel is the platform-side environment health monitor. It is separate from org analytics:

- `eve analytics env-health --org <org_id>`: org-scoped aggregate counts only
- `eve system env-health`: cross-org detailed snapshot for `system_admin`

```bash
eve system env-health [--status critical] [--limit 100] [--json]
eve system settings sentinel.enabled --json
eve system settings sentinel.slack.integration_id --json
eve system settings sentinel.slack.channel_id --json
```

`eve system env-health` returns:

| Field | Meaning |
|---|---|
| `summary.total` | Number of tracked environments |
| `summary.healthy/degraded/critical` | Current health counts |
| `environments[].issues_json` | Active issue list (`image_pull_backoff`, `crash_loop_backoff`, `high_restarts`, `pending_too_long`) |
| `environments[].consecutive_degraded_ticks` | How many watchdog ticks the environment has stayed non-healthy |
| `environments[].actions_taken_json` | Circuit-breaker actions such as `scale_to_zero` |

Sentinel delivery behaviour:
- Outbound alerts are suppressed unless `sentinel.enabled=true`
- Slack delivery uses `sentinel.slack.integration_id` + `sentinel.slack.channel_id`
- Recovery and circuit-break alerts bypass the normal dedup window
- The watchdog can keep populating environment health rows even when Slack delivery is not configured

## Cost Tracking

Eve tracks costs through execution receipts, resource classes, per-job budgets, and an org balance ledger.

### Rate Cards

```bash
eve admin pricing seed-defaults       # Seed default rate cards (admin)
```

Rate cards map model + provider to per-token costs. The platform uses these to compute receipt costs automatically.

### Balance + Usage

```bash
eve admin balance show <org_id>                     # Current balance
eve admin balance credit <org_id> --amount 100.00   # Add credit
eve admin balance transactions <org_id>             # Transaction history

eve admin usage list --org org_xxx                   # Usage records
  [--since 2026-01-01] [--until 2026-02-01]
eve admin usage summary --org org_xxx                # Aggregated summary

eve org spend --org org_xxx                          # Org spend overview
eve project spend --project proj_xxx                 # Project spend
```

## Provider + Harness Discovery

```bash
eve providers list [--json]                         # Registered providers
eve providers discover <provider> [--json]          # Live model list (cached with TTL)
eve harness list [--capabilities]                   # Harness model support matrix
```

## OpenTelemetry Configuration

OTEL is enabled when `OTEL_ENABLED=true` or `OTEL_EXPORTER_OTLP_ENDPOINT` is set. Uses OTLP HTTP exporter with automatic Node.js instrumentation.

| Variable | Purpose |
|---|---|
| `OTEL_ENABLED` | `true`/`false` -- enable OTEL |
| `OTEL_DISABLED` | `true` -- hard disable (overrides OTEL_ENABLED) |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | Collector endpoint (e.g. `http://otel-collector:4318`) |

Request trace lookup requires apps to stamp `request_id` on the active span.
Use the shared helper from `@eve/shared`:

```ts
import { stampCurrentRequestId } from '@eve/shared';

stampCurrentRequestId(requestId);
```

Agents can query traces without AWS console access:

```bash
eve traces query --project proj_xxx --request-id req_01h... --json
eve traces query --project proj_xxx --trace-id 1-abcdef...
eve traces query --project proj_xxx --service api --since 5m --error
eve traces query --project proj_xxx --service api --route "POST /api/items" --since 1h --p99
```

## Real-Time Monitoring

```bash
eve job follow <id>                   # Stream harness logs + live cost totals + silence detection
eve env logs <project> <env> <service> --follow --since 30 # Stream app service logs
eve job watch <id>                    # Combined status + logs streaming
eve job runner-logs <id>              # K8s runner pod stdout/stderr
eve system status                     # Service health including agent runtime + replicas
eve system logs <service> [--tail 50] # Service logs (api, orchestrator, worker, agent-runtime, postgres)
eve system events [--limit 50]        # Recent platform events
eve agents runtime-status --org <id>  # Pod health with stale markers and active job counts
```

### Harness Heartbeat + Silence Detection

During job execution, the harness emits heartbeat lifecycle events every 30 seconds. These are used for:

- **`eve job diagnose`**: Shows `Heartbeat: 15s ago (120s into execution)` in the Latest Attempt section. Stuck detection uses heartbeat age instead of raw elapsed time — a heartbeat within 120s means "harness alive" even if there's no log output.
- **`eve job follow`**: Built-in silence timer warns at 60s and 120s of no output. If heartbeat data is available, the warning differentiates between "harness alive but quiet" and "harness may have stalled".
- **`eve job logs`**: Heartbeat events appear in the log stream (type `lifecycle_runner`) with `kind: heartbeat`, `elapsed_ms`, `harness`, and `pid`.

### Pre-Harness Startup Lifecycle

The agent-runtime emits lifecycle events for pre-harness phases:

| Phase | Event Type | What It Captures |
|-------|-----------|------------------|
| Git clone | `workspace/start` + `workspace/end` | Duration, ref, success/failure with error |
| Credential write | `secrets/start` + `secrets/end` | Duration, success (token produced?) |
| App CLI discovery | `workspace/log` | CLI name, availability |

These appear in `eve job diagnose` as part of the latency waterfall. If clone or credential provisioning fails, the error is captured in the lifecycle event.

## CLI Quick Reference

| Intent | Command |
|---|---|
| Trace a request | Check `x-eve-correlation-id` in response headers |
| Diagnose app request | `eve env diagnose <project> <env> --request <id> --json` |
| Stream app logs | `eve env logs <project> <env> <service> --follow --filter req_id=<id>` |
| Query traces | `eve traces query --project <id> --request-id <id> --json` |
| Job cost receipt | `eve job receipt <id>` |
| Compare job costs | `eve job compare <id1> <id2>` |
| Org analytics | `eve analytics summary --org <id> --window 7d` |
| Job metrics | `eve analytics jobs --org <id>` |
| Pipeline metrics | `eve analytics pipelines --org <id>` |
| Env health | `eve analytics env-health --org <id>` |
| Org balance | `eve admin balance show <org_id>` |
| Usage report | `eve admin usage summary --org <id>` |
| Recompute receipts | `eve admin receipts recompute [--dry-run]` |
| Provider models | `eve providers discover <provider>` |
| Stream job logs | `eve job follow <id>` |
| Platform events | `eve system events` |
