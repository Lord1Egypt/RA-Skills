---
name: watchdog-heartbeat
description: "Monitor service health, heartbeat freshness, stuck workflows, and trigger recovery or degraded mode. Use on: high-frequency schedule, after system startup, when a workflow stalls, when heartbeat freshness must be verified. Triggered by watchdog cron jobs or health check requests."
---

# Watchdog Heartbeat

Provide observability and recovery awareness for a resident OpenClaw system. Verify process aliveness, heartbeat freshness, and workflow integrity.

## Input

Required:
- `service_list` — list of monitored services and their expected health states
- `health_endpoints` — map of service → health check endpoint or method
- `heartbeat_records` — recent heartbeat timestamps per agent/skill
- `workflow_status_records` — current status of all active workflows
- `restart_records` — history of service restarts and recovery events

## Output Schema

```
service_health_summary: {
  service: string
  status: "healthy" | "degraded" | "down" | "unknown"
  last_check: string      # ISO-8601
  latency_ms: number | null
  error: string | null
}[]

expired_heartbeat_list: {
  agent_or_skill: string
  last_heartbeat: string  # ISO-8601
  seconds_expired: number
  severity: "warning" | "critical"
}[]

stuck_workflow_list: {
  workflow_id: string
  workflow_name: string
  stuck_since: string     # ISO-8601
  stuck_duration_min: number
  last_progress: string | null
  severity: "warning" | "critical"
}[]

recovery_recommendation: {
  action: "restart" | "notify" | "escalate" | "no_action" | "degraded_mode"
  target: string
  reason: string
}[]

degraded_mode_recommendation: {
  affected_services: string[]
  degraded_features: string[]
  estimated_recovery_time: string | null
  user_impact: string
}

watchdog_log: {
  check_id: string
  check_time: string     # ISO-8601
  services_checked: number
  heartbeats_checked: number
  workflows_checked: number
  issues_found: number
  observability_gap: string[] | null
}
```

## Rules

1. **Process alive ≠ healthy.** Check recent success, not just process existence.
2. **Expired heartbeat triggers attention.** Do not ignore stale heartbeats.
3. **Stuck workflows must be explicitly surfaced.** Don't let them disappear into silence.
4. **Silent failure is unacceptable.** If something fails and no one is notified, that's a system failure.
5. **Distinguish warning from critical.** Warning = may self-recover. Critical = requires intervention.

## Heartbeat Expiry Thresholds

| Seconds Expired | Severity |
|----------------|----------|
| < 60s | healthy |
| 60s – 300s | warning |
| > 300s | critical |

## Workflow Stuck Thresholds

| Duration | Severity |
|----------|----------|
| < 10 min | healthy (in progress) |
| 10 – 30 min | warning |
| > 30 min | critical |

## Recovery Actions

- `no_action` — within normal parameters
- `notify` — alert human, no automatic restart
- `restart` — attempt automatic restart
- `escalate` — human intervention required
- `degraded_mode` — reduce functionality, maintain partial service

## Failure Handling

If monitoring data is incomplete:
- Set `observability_gap` with missing field names
- Report `status = "unknown"` for affected services
- Do not fabricate health states
- Recommend `escalate` if critical services have observability gaps
