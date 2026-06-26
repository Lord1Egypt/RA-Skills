# Ops playbook

## Default thresholds

Start with these defaults and keep them configurable:

- CPU high: `cpu_pct > 85` for five consecutive one-minute samples
- Memory high: `memory_pct > 85` for five consecutive one-minute samples
- Disk low: `disk_free_ratio < 0.10`
- Server error burst: `500`, `502`, or `504` count above `20` in one minute
- Suspicious IP: one IP above `200` requests per minute
- 404 scan burst: sudden 404 spike against many distinct routes in a short window
- Performance degradation: average response time above `2000 ms` over the alert window

## Alert flow

1. Detect the threshold breach.
2. Enrich it with:
   - time window
   - affected site or route
   - top IPs or URIs
   - recent error fingerprints
   - operator caveats
3. De-duplicate repeated alerts with a cooldown.
4. Send the webhook payload.
5. Record the alert as an `action_event` even when the webhook fails.

## Webhook payload shape

Keep the outgoing alert compact and readable:

```json
{
  "title": "Server-Mate alert",
  "severity": "critical",
  "kind": "server_error_burst",
  "host_id": "web-01",
  "site": "example.com",
  "summary": "502 errors crossed the threshold in the last minute.",
  "details": {
    "count": 37,
    "top_uri": "/api/pay",
    "top_ip": "203.0.113.8"
  },
  "suggested_next_step": "Check php-fpm health and upstream socket availability."
}
```

## AI diagnosis packaging

When translating an unfamiliar stack trace or error burst for the operator, send:

- the normalized category or fingerprint
- the compact message
- the top few neighboring raw lines
- the affected route, site, or upstream
- the current alert context

Ask the model for:

1. a plain-language explanation
2. the most likely root causes
3. the next three checks
4. the safest fix or rollback path
5. a confidence level

## Auto-ban policy

Keep auto-ban disabled or dry-run until the operator explicitly enables it.

Require all of the following:

- allowlist support for trusted IPs or office ranges
- evidence that the spike is abusive, not a flash crowd
- a cooldown and a per-hour action cap
- a TTL such as 24 hours
- an audit record with the exact ban or unban command

Good auto-ban candidates:

- repeated request-rate breaches from one IP
- scanner-like user-agents plus 404 spray patterns
- brute-force style hits against admin routes

## Auto-heal policy

Keep self-heal more conservative than alerting.

Require all of the following:

- repeated `502` or upstream-failure evidence
- a failing health check or equivalent secondary signal
- one restart attempt per service per cooldown window
- post-action verification
- an escalation path when the restart does not help

Prefer a sequence like:

1. Alert
2. Dry-run recommendation
3. One guarded restart of the proven failing service
4. Re-check error rate and health
5. Escalate instead of looping

## Reporting windows

- Daily report: previous calendar day
- Weekly report: current or previous ISO week, but keep the choice explicit
- Monthly report: calendar month plus a growth or peak comparison

For each report, surface only the top issues and the trend delta. Avoid dumping every counter.
