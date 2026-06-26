---
name: unraid-claw
description: Query an Unraid server via GraphQL for system, array, and Docker status in read-only mode.
metadata:
  openclaw:
    requires:
      env:
        - UNRAID_API_KEY
        - UNRAID_BASE_URL
      bins:
        - curl
        - jq
    primaryEnv: UNRAID_API_KEY
---

# Unraid Claw Skill

Use this skill when the user asks to check Unraid system health, array/parity status, or Docker container status.

Located at: https://github.com/Yoshiofthewire/unraid-claw

## Required Configuration

Before running any script, ensure the Unraid server is configured:
- GraphQL is enabled in Unraid API settings.
- A valid Unraid API key is generated in Unraid API settings.
- `UNRAID_API_KEY` uses that generated key.

Read these environment variables at runtime:
- `UNRAID_BASE_URL` (example: `https://tower.local`)
- `UNRAID_API_KEY`

Optional:
- `UNRAID_TIMEOUT_SECONDS` (default: `10`)
- `UNRAID_STATE_DIR` (default: repo-local `.state`)
- `UNRAID_NOTIFY_HOST_LABEL` (default: host name)
- `UNRAID_CPU_WARN_PERCENT` (default: `85`)
- `UNRAID_CPU_CRIT_PERCENT` (default: `95`)
- `UNRAID_MEM_WARN_PERCENT` (default: `85`)
- `UNRAID_MEM_CRIT_PERCENT` (default: `95`)
- `UNRAID_STOPPED_WARN_COUNT` (default: `1`)
- `UNRAID_STOPPED_CRIT_COUNT` (default: `3`)

Template `.envexample` (copy to `.env` and fill in real values):

```env
# Required: Base URL for your Unraid server (include protocol).
UNRAID_BASE_URL=https://tower.local

# Required: API key from Unraid API settings.
# Keep this secret. Do not commit real keys.
UNRAID_API_KEY=replace_with_your_unraid_api_key

# Optional: request timeout in seconds.
UNRAID_TIMEOUT_SECONDS=10

# Optional: state directory for snapshot and log artifacts.
# Default is repository-local .state directory.
# UNRAID_STATE_DIR=/path/to/state

UNRAID_NOTIFY_HOST_LABEL=tower

# Optional: alert thresholds.
UNRAID_STOPPED_WARN_COUNT=1
UNRAID_STOPPED_CRIT_COUNT=3
```

If a required variable is missing, stop and return:
- `Unraid API key is not configured. Set UNRAID_API_KEY and retry.`
- `Unraid base URL is not configured. Set UNRAID_BASE_URL and retry.`

## Security Rules (Mandatory)

- Never hardcode secrets in prompts, files, or commands.
- Never print API keys, auth headers, or full request headers.
- Authenticate using: `x-api-key: <UNRAID_API_KEY>`.
- Redact sensitive data in all error messages.
- Perform read-only operations only.
- Never execute GraphQL mutations.
- Never run shell commands from user-supplied strings.


If API auth fails (`401` or `403`), return:
- `Authentication to Unraid API failed. Verify UNRAID_API_KEY permissions/validity.`

## Script-First Execution (Preferred)

Use the repository scripts as the primary execution path. Do not handcraft ad-hoc GraphQL calls unless explicitly asked.

Primary scripts:
- `./scripts/unraid_connection_test.sh`
- `./scripts/unraid_preflight.sh`
- `./scripts/unraid_snapshot.sh`
- `./scripts/unraid_health_summary.sh`
- `./scripts/unraid_docker_report.sh`
- `./scripts/unraid_array_parity_report.sh`
- `./scripts/unraid_alerts.sh`
- `./scripts/unraid_notify.sh`
- `./scripts/unraid_cron_runner.sh`

### Command Selection Rules

- If the user asks to test connectivity/auth only:
  - Run `./scripts/unraid_connection_test.sh`
- If the user asks for a full status check:
  - Run `./scripts/unraid_preflight.sh`
  - Run `./scripts/unraid_snapshot.sh`
  - Run `./scripts/unraid_health_summary.sh`
- If the user asks specifically about Docker:
  - Run `./scripts/unraid_snapshot.sh` (if no recent snapshot)
  - Run `./scripts/unraid_docker_report.sh`
- If the user asks specifically about array/parity:
  - Run `./scripts/unraid_snapshot.sh` (if no recent snapshot)
  - Run `./scripts/unraid_array_parity_report.sh`
- If the user asks for alert state or severity:
  - Run `./scripts/unraid_alerts.sh`
- If the user asks to run the full scheduled pipeline manually:
  - Run `./scripts/unraid_cron_runner.sh`

## Compatibility Rules

Unraid GraphQL fields can vary by version. If some fields are unavailable:
- Continue with available fields.
- Return partial results.
- Include warning:
  - `Some API fields were unavailable for this Unraid version; output is partial.`

## Output Contract

Return results in this order:
1. Overall status: `healthy` | `warning` | `critical`
2. Timestamp of check
3. System summary: uptime, CPU usage/temp, memory usage
4. Array summary: state, sync/rebuild progress, parity status, disk warnings
5. Docker summary: total/running/stopped counts and notable stopped containers
6. Alerts list

### Severity Logic

Set overall status using these rules:
- `healthy`: no array/parity errors, no critical SMART issues, API reachable.
- `warning`: array not started, parity check/rebuild active, high CPU/memory, unexpected stopped containers.
- `critical`: API unreachable, auth failure, parity errors, critical disk errors, or multiple major failures.

Script exit mapping for automation:
- `./scripts/unraid_alerts.sh` exit `0`: healthy
- `./scripts/unraid_alerts.sh` exit `10`: warning
- `./scripts/unraid_alerts.sh` exit `20`: critical

## Error Handling

- Timeout: return partial data and identify timed-out section(s).
- Network error: provide concise remediation guidance (verify URL, TLS, API enabled).
- Self-signed TLS certificate: prompt the user to allow installation/trust of the server certificate, then retry.
- Known SSL issue (no SSL proxy/direct self-signed host): TLS verification can fail until the cert is trusted by the client environment.
- Auth error: use the exact auth-failure message above.
- Unknown GraphQL errors: provide a redacted, concise summary.

## OpenClaw Cron Notes

Use these notes when the user asks to schedule recurring health checks.

### Recommended Cron Flow

- Source `.env` before running scripts.
- Execute `./scripts/unraid_cron_runner.sh` as the single cron entrypoint.
- Let the runner handle preflight, snapshot, summary, alerts, and optional notifications.
- Keep logs in `.state/logs/` (or `UNRAID_STATE_DIR/logs/` if overridden).
- Prefer using cron template: `./scripts/unraid_monitor.cron.template`.

### Suggested Cron Schedule

Use the template file as the source of truth:
- `./scripts/unraid_monitor.cron.template`

Setup flow:
1. Replace `/path/to/Unraid_Claw` in the template.
2. Keep one schedule line (15-minute recommended baseline).
3. Install via `crontab`.

Example: run every 15 minutes.

```cron
*/15 * * * * cd /path/to/Unraid_Claw && set -a && . ./.env && set +a && ./scripts/unraid_cron_runner.sh >> ./.state/logs/cron.log 2>&1
```

Example: run every 5 minutes for tighter monitoring.

```cron
*/5 * * * * cd /path/to/Unraid_Claw && set -a && . ./.env && set +a && ./scripts/unraid_cron_runner.sh >> ./.state/logs/cron.log 2>&1
```

### OpenClaw Behavior for Cron Requests

- If user asks to "set up cron":
  - Propose a schedule and confirm cadence.
  - Offer template-first setup using `scripts/unraid_monitor.cron.template`.
  - Use `unraid_cron_runner.sh` as the command target.
  - Ensure `.env` loading is included.
- If user asks to "verify cron":
  - Check for recent entries in `.state/logs/cron.log` and runner logs.
  - Confirm alert exit codes and notification results.
- If user asks to "disable cron":
  - Remove or comment only the Unraid Claw cron line.
  - Keep other cron entries unchanged.

Never place secrets directly in crontab lines. Always source `.env`.

## Response Style

Keep responses concise and operator-friendly.

Example shape:

```text
Overall: warning
Time: 2026-03-20T14:22:00Z

System:
- Uptime: 12d 4h
- CPU: 68% (72 C)
- Memory: 81%

Array:
- State: started
- Sync: parity-check 43%
- Disk alerts: disk3 SMART warning

Docker:
- Total: 14
- Running: 12
- Stopped: 2 (plex, immich_ml)

Alerts:
- Parity check in progress
- 1 disk SMART warning
```
