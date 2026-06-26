# Unraid Monitor Skill for OpenClaw

This repository contains an OpenClaw skill that checks Unraid health through the Unraid GraphQL API.

## What this does

- Checks system status
- Checks array and parity status
- Lists Docker container status
- Provides a read-only connection test harness
- Captures periodic snapshots for reporting and alerting

## Project files

- Skill definition: SKILL.md
- Skill planning/spec notes: PROMPT.md
- Connection test harness: scripts/unraid_connection_test.sh
- Script helper library: scripts/unraid_common.sh
- Preflight checks: scripts/unraid_preflight.sh
- Snapshot capture: scripts/unraid_snapshot.sh
- Health summary report: scripts/unraid_health_summary.sh
- Docker-focused report: scripts/unraid_docker_report.sh
- Array/parity report: scripts/unraid_array_parity_report.sh
- Alert evaluator: scripts/unraid_alerts.sh
- Notification sender: scripts/unraid_notify.sh
- Cron orchestrator: scripts/unraid_cron_runner.sh
- Cron template: scripts/unraid_monitor.cron.template
- Environment template: .envexample
- Git ignore rules for secrets: .gitignore

## Prerequisites

- Unraid API with GraphQL enabled on your server
- An Unraid API key generated from Unraid API settings
- curl installed
- jq installed

## Unraid server setup

1. In Unraid, open API settings and enable GraphQL.
2. Generate a new Unraid API key.
3. Copy the key into your local `.env` as `UNRAID_API_KEY`.

Known SSL note:
- If you are not using an SSL proxy and your Unraid host uses a self-signed certificate, TLS verification may fail until that cert is trusted on the machine running these scripts.

Linux cert trust example (Debian/Ubuntu):
1. Export the server certificate:
   `openssl s_client -showcerts -connect <UNRAID_HOST>:443 </dev/null 2>/dev/null | openssl x509 -outform PEM > unraid-selfsigned.crt`
2. Install it into the system trust store:
   `sudo cp unraid-selfsigned.crt /usr/local/share/ca-certificates/unraid-selfsigned.crt`
3. Refresh trust store:
   `sudo update-ca-certificates`
4. Re-run connection test:
   `./scripts/unraid_connection_test.sh`

If your distro uses a different trust mechanism, follow the distro-specific CA trust workflow.

## Setup

1. Create your local environment file:
   cp .envexample .env

2. Edit .env and set your values:
   UNRAID_BASE_URL=https://tower.local
   UNRAID_API_KEY=your_real_api_key
   UNRAID_CSRF_TOKEN=your_csrf_token_if_required   # optional
   UNRAID_SESSION_COOKIE=your_cookie_if_required   # optional
   UNRAID_TIMEOUT_SECONDS=10

3. Load environment variables into your shell:
   set -a
   source .env
   set +a

## Test connection

Run the harness:

./scripts/unraid_connection_test.sh

Expected outcomes:
- PASS means endpoint is reachable and auth succeeded.
- FAIL includes a sanitized reason and exit code.

Common fail cases:
- Missing UNRAID_BASE_URL or UNRAID_API_KEY
- Invalid API key (401/403)
- Invalid CSRF token (use direct Unraid URL, or set UNRAID_CSRF_TOKEN + UNRAID_SESSION_COOKIE for login-gated proxies)
- TLS or network routing issues (including self-signed cert trust failures on non-proxy setups)

## Using with OpenClaw

The skill behavior is defined in SKILL.md.

OpenClaw should use this skill when asked to:
- Check Unraid health
- Check array or parity status
- List Docker containers
- Troubleshoot Unraid API connectivity

For connectivity troubleshooting, OpenClaw should run:

./scripts/unraid_connection_test.sh

before broader status queries.

## Monitoring scripts

Recommended run sequence:

1. Validate environment and connectivity:

   ./scripts/unraid_preflight.sh

2. Capture latest snapshot:

   ./scripts/unraid_snapshot.sh

3. View reports:

   ./scripts/unraid_health_summary.sh
   ./scripts/unraid_docker_report.sh
   ./scripts/unraid_array_parity_report.sh

4. Evaluate alerts:

   ./scripts/unraid_alerts.sh
   echo $?   # 0 healthy, 10 warning, 20 critical

5. Send notification manually:

   ./scripts/unraid_notify.sh WARNING "Unraid status warning"

6. Run full scheduled pipeline:

   ./scripts/unraid_cron_runner.sh

## Cron template

Use the provided cron template to schedule recurring checks:

- Template file: `scripts/unraid_monitor.cron.template`

Install workflow:

1. Edit the template and replace `/path/to/Unraid_Claw` with your real path.
2. Keep only one schedule line (15m recommended, or 5m for tighter monitoring).
3. Install the line into your crontab:

   crontab -l > /tmp/current.cron 2>/dev/null || true
   cat /tmp/current.cron scripts/unraid_monitor.cron.template | crontab -

Verify cron output:

- `tail -n 50 .state/logs/cron.log`
- `tail -n 50 .state/logs/runner_$(date -u +%Y%m%d).log`

Optional JSON output:

- ./scripts/unraid_health_summary.sh --json
- ./scripts/unraid_docker_report.sh --json
- ./scripts/unraid_array_parity_report.sh --json
- ./scripts/unraid_alerts.sh --json

Default state artifacts:

- Latest snapshot: .state/latest_snapshot.json
- Archived snapshots: .state/snapshots/
- Logs: .state/logs/

Set UNRAID_STATE_DIR to move those artifacts elsewhere.

## Alert defaults

Default thresholds are tuned for safe early warnings and can be adjusted in .env:

- CPU warning/critical: 85% / 95%
- Memory warning/critical: 85% / 95%
- Stopped container warning/critical count: 1 / 3

## Security notes

- Never commit real credentials.
- Keep API keys only in environment variables.
- Do not print tokens or authorization headers in logs.
- This project is read-only against the API and does not run mutations.


## References

- OpenClaw skills docs: https://docs.openclaw.ai/tools/creating-skills
- Unraid API docs: https://docs.unraid.net/API/
