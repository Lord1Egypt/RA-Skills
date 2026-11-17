# Operate Workflow

Identify the app before any cloud call, verify after every recovery action, and record what you
did.

## Identify the app

1. Find `.qwencloud-deploy` in the project directory. If absent, ask the user to `cd` into the
   deployed project directory or provide the path — do not guess resources.
   If the state file has `provisional: true` (deploy did not finish; no `outputs` / `service_name`),
   the deployment is incomplete — tell the user to finish deploying first and stop before diagnosis or operation.
2. Parse and extract: `region_id`, `stack_id`, `topology`, `app_type`, `nginx_mode`, `app_port`,
   `outputs.public_ip`, `outputs.ecs_instance_ids[]`, `outputs.security_group_id`,
   `outputs.eip_allocation_id`, and RDS fields
   (`outputs.db_instance_id` / `db_connection_address` / `db_port` / `db_account`, `db_engine`).
   Also `service_name` (service name, used for service/log checks; falls back to `qwencloud-app` when missing).
3. Determine topology (ECS only vs ECS + RDS).

Read `.qwencloud-deploy` only. **Never** read `.qwencloud-deploy.local` (passwords). Do not print
`current_artifact_urls` (signed URLs).

If `observe_handoff.json` (a handoff hint from `qwencloud-observe`) exists, you may read it for
`fault_layer` / `symptoms` as a starting point; it contains read-only observed evidence only, no
passwords, and is a hint rather than a conclusion.

If `app_timeline.jsonl` exists, you may read its last few lines for recent-change context (deploy /
hotfix / checkups / past operations) to line the current fault up with what most recently happened.
It holds redacted read-only information only, no passwords.

## Verify (after every recovery action)

1. **CLI/API result** — the recovery call succeeded; capture its RequestId.
2. **ECS status** — `DescribeInstances` shows `Running`.
3. **RDS status** (if present) — instance running; for pool issues, connections back to normal.
4. **App process / Nginx / ports** — read-only Cloud Assistant: `<service_name>` and `nginx` active,
   app port / 80 listening.
5. **Entry points** — `/healthz` and homepage return healthy.

Return exactly one verdict, with evidence:

- **recovered** — entry points healthy and services up.
- **partially recovered** — some layers healthy, others still failing (name which).
- **not recovered** — entry points still failing.

On **not recovered** or **partially recovered**, return the failing step, the CLI RequestId, the
current state, and a recommended next step. Do not auto-loop another write — decide the next single
action explicitly.

## Re-score (close the loop with observe)

After a **recovered** verdict, offer to re-run `qwencloud-observe` and report the health score
before → after (e.g. "D 52 → B 84"), so the user sees the recovery reflected in the score. Skip
when the user declines or observe is unavailable.

## Record (audit)

Record every recovery action (write) as a structured entry.

| Field | Value |
|-------|-------|
| `time` | action timestamp (UTC) |
| `target` | resource id (ECS/RDS) + region |
| `action` | the action performed (e.g. StartInstance, restart <service_name>, reload nginx) |
| `confirmation` | user confirmation result (confirmed / declined) |
| `request_id` | CLI RequestId of the write call |
| `verification` | recovered / partially recovered / not recovered |

Append each entry as one JSON line to `operate_audit.jsonl` in the project directory (next to
`.qwencloud-deploy`), so repeated operations leave a trail and observe can reference the most
recent action.

Also append one JSON line (`event=operate`) to `app_timeline.jsonl` alongside the state file so
deploy / hotfix / checkups / operations stay queryable in one continuous dossier. Fields: `ts` (UTC),
`skill: qwencloud-operate`, `event: operate`, `summary` (one line), merged with `target` / `action` /
`confirmation` / `request_id` / `verification`:

```json
{"ts":"2026-08-03T16:20:00Z","skill":"qwencloud-operate","event":"operate","summary":"restart <service_name>, recovered","target":"i-xxx@ap-southeast-1","action":"restart <service_name>","confirmation":"confirmed","request_id":"...","verification":"recovered"}
```

Audit records and chat output must never contain passwords, tokens, or full connection
credentials. Redact before writing. Declined confirmations are recorded too, with
`confirmation: declined` and no write performed.
