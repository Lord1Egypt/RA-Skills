# Observe Workflow

How to start (identify the app) and how to finish (pull the layers together).

## Identify the app

Before any cloud query, resolve the target from the local deployment state.

1. Look for `.qwencloud-deploy` in the current project directory. If absent, tell the user to
   `cd` into the deployed project directory or provide the project path — do not guess resources.
   If the state file has `provisional: true` (deploy did not finish; no `outputs` / `service_name`),
   the deployment is incomplete — tell the user to finish deploying first and stop before any cloud query.
2. Parse the JSON state file. Extract:
   - `region_id`, `stack_id`, `topology`, `app_type`, `nginx_mode`, `app_port`
   - `service_name` (service name, used for service/log checks; falls back to `qwencloud-app` when missing)
   - `outputs.public_ip`, `outputs.ecs_instance_ids[]`, `outputs.security_group_id`,
     `outputs.eip_allocation_id`
   - RDS (when present): `outputs.db_instance_id`, `outputs.db_connection_address`,
     `outputs.db_port`, `outputs.db_account`, `db_engine`
   - `created_at`, `updated_at`
3. Determine topology: `single` (ECS only) or ECS + RDS (a non-null `db_instance_id`).
4. Validate region and resource IDs are non-empty. Missing critical IDs → mark the affected layer
   `unknown` with the reason.
5. If `operate_audit.jsonl` sits alongside the state file, read its last line and take
   `time` / `action` / `verification` as the "most recent operate action" context — tying this
   observation to the latest recovery. Skip if the file is absent.
6. If `app_timeline.jsonl` sits alongside the state file, read the last few lines as recent-change
   context (deploy / hotfix / past scores / operate actions) so this observation lines up with what
   most recently happened. Skip if the file is absent.

Read `.qwencloud-deploy` only. **Never** read `.qwencloud-deploy.local` (it holds passwords).
`current_artifact_urls` are signed URLs — do not print them.

| Field | Used by |
|-------|---------|
| `region_id` | every cloud query (`--region`) |
| `outputs.ecs_instance_ids` | ECS status/metrics and cost (match rows in the account bill) |
| `outputs.public_ip` | application public probe |
| `outputs.security_group_id` | security-group exposure / ingress rule check |
| `outputs.eip_allocation_id` | EIP status and bandwidth |
| `outputs.db_instance_id` | RDS checks and cost |
| `app_type` / `nginx_mode` / `app_port` | application service checks |
| `service_name` | systemd service / log file name (falls back to `qwencloud-app`) |

## Pull the layers together

Merge per-layer signals into one application-level conclusion. Identify at least these patterns:

### Verdict guardrails

- A probe only proves the entry is reachable; it is not a health verdict on its own. Every health
  verdict must also include CloudMonitor CPU/memory data points over the window, taking the
  strictest of the two — any bad signal means not `healthy`.
- Pull fresh data points on every health question and conclude from them; do not reuse a previous
  sweep's conclusion. The report's data time is the validity boundary of that conclusion.

| Pattern | Signals |
|---------|---------|
| All healthy | App reachable, ECS Running + normal metrics, RDS (if any) normal |
| ECS down / app service exited | ECS Stopped, or `<service_name>` inactive; public probe fails |
| Sustained ECS high load | CPU sustained high over the window; response time rising |
| App cannot reach RDS | App logs show DB timeout/refused/auth failure; RDS reachable but app fails to connect |
| RDS near bottleneck | Connections near limit, or space/IOPS pressure |
| Slow app from DB | Slow SQL, row-lock waits, or full-table scans correlated with rising response time |
| Partial data | Some layer `unknown` due to permission or collection limits |

Lead with the single overall conclusion, then the evidence per layer. Map the whole app to the
worst contributing state (`unavailable` > `degraded` > `unknown` > `healthy`), but still report
each layer's own state. When a fault (not merely `unknown`) is present, offer the next step:
enter fault diagnosis via `qwencloud-operate`.

When a recent operate action was read, add one line tying it in, e.g. "Last operate: 2026-09-09
restart <service_name> (recovered)", so this score lines up with the latest recovery. Never echo
passwords or full connection strings from the audit.

## Score the layers

Give each layer a score out of its weight, then sum them into the health score and grade.

| Dimension | Max (with RDS) | Max (no RDS) |
|-----------|----------------|--------------|
| Application | 35 | 45 |
| ECS | 30 | 45 |
| RDS | 25 | — |
| Availability | 10 | 10 |

Score each layer from its state and evidence: `healthy` keeps most of the weight, `degraded`
takes a partial deduction sized to the risk, `unavailable` scores near zero, and `unknown` scores
zero (state it could not be measured). No RDS → its weight moves to Application and ECS.

The Availability dimension rolls up ECS/RDS run status, recent system events, EIP status and
bandwidth, and security-group exposure. Missing backups/snapshots and security-group hardening are
risks and recommendations only, not scored.

`health_score` = sum of the layer scores; the grade follows it strictly (`>=90` A · `>=75` B ·
`>=60` C · `<60` D). Keep the one-line verdict consistent with the score — a low score never pairs
with an "all good" summary.

When a prior observe result is known (e.g. the pre-recovery score), include a "was → now" score
comparison in the report so a recovery or regression is visible in the number.

**Cost is never part of the score.** Report it separately as the actual bill (cycle, total,
per-product breakdown) plus a short utilization-based optimization note; never estimate spend.

## Append application dossier

After deriving the health score, append one JSON line (`event=observe`) to `app_timeline.jsonl`
alongside the state file. Fields: `ts` (UTC), `skill: qwencloud-observe`, `event: observe`, `summary`
(one-line verdict), merged with `score` / `grade`, plus `fault_layer` on a real fault:

```json
{"ts":"2026-08-03T16:20:00Z","skill":"qwencloud-observe","event":"observe","summary":"Checkup 87/100 (B) — app healthy; watch the RDS connection trend","score":87,"grade":"B"}
```

Write redacted read-only conclusions only; never a password or connection string.
