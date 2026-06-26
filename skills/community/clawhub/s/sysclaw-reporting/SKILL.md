---
name: sysclaw-reporting
description: >
  Report system issues and submit resource requests to SysClaw via the cross-agent
  communication system. Use when an agent needs to report an error, warning, or
  info-level issue for SysClaw triage, or request anything from SysClaw including
  software installation, resource access, configuration changes, service management,
  deployments, or system information. Triggers on phrases like report an issue,
  report an error, request access, need software, install package, create database,
  restart service, deploy, check status, escalate to sysclaw.
---

# SysClaw Reporting (Client)

Report issues and submit requests to SysClaw. This is the client-side skill — it covers how to communicate with SysClaw, not how SysClaw processes requests.

## Prerequisites

### 1. Install Python dependency

```bash
pip3 install psycopg2-binary
```

### 2. Set environment variables

Set these before running scripts. All scripts use a fallback chain: script-specific vars → `SYSCLAW_DB_*` → defaults.

```bash
# Shared connection settings (used by all scripts as fallback)
export SYSCLAW_DB_HOST="<your-db-host>"        # Ask your SysClaw operator
export SYSCLAW_DB_PORT="5432"
export SYSCLAW_DB_NAME="system_comm"
export SYSCLAW_DB_USER="<your-agent-role>"     # e.g., jobagent, pmagent, researcher_agent
export SYSCLAW_DB_PASSWORD="<your-db-password>"
```

You can also set per-script overrides (`ISSUE_DB_*`, `REQUEST_DB_*`) if different scripts need different credentials, but in most cases the shared `SYSCLAW_DB_*` vars are sufficient.

**Ask your SysClaw operator for the correct host address and your agent credentials.**

## Report an Issue

For errors, warnings, and problems that need attention:

```bash
scripts/report-issue.sh <source> <severity> <title> [category] [details] [source_host]
```

**Severity:** `info` | `warning` | `critical`
**Categories:** `disk` | `service` | `error` | `resource` | `network` | `config` | `other`

**Examples:**
```bash
scripts/report-issue.sh jobhunter warning "Disk usage above 80%" disk "df shows 82% on /data" srv-prod-01
scripts/report-issue.sh pmagent critical "API endpoint returning 500" service "5 consecutive failures" srv-prod-02
```

> **source_host** (6th argument, optional): Identifies which machine this report originates from. Defaults to the current hostname if omitted.

## Request Something from SysClaw

For software installs, access requests, configuration changes, and more:

```bash
scripts/request-resource.sh <source> <type> <action> <target> <justification> [urgency] [payload] [source_host]
```

**Types:** `access` | `software` | `resource` | `config` | `service` | `deployment` | `info`
**Actions:** `install` | `remove` | `create` | `modify` | `restart` | `grant` | `check` | `deploy`
**Urgency:** `low` | `normal` | `urgent` (default: `normal`)
**Payload:** Valid JSON string (optional). Validated before submission.

### Examples

```bash
scripts/request-resource.sh jobhunter software install nginx '{"version":"latest"}' normal
scripts/request-resource.sh pmagent access grant /var/data/pm '{"level":"read"}'
scripts/request-resource.sh researcher info check disk_usage
```

## What Happens Next

1. Your request is submitted and SysClaw is automatically notified
2. SysClaw assesses and processes the request (typically within 15 minutes)
3. **SysClaw executes approved actions** — you don't need to do anything after approval
4. You receive a notification with the result (e.g., "DONE: nginx installed and running")

**Verdicts:**
- `approved` + `DONE` — SysClaw completed the work, see notification for details
- `denied` — see notification for reason
- `escalated` — human operator reviewing, you'll be notified when decided

## Check Notifications

Check for responses from SysClaw:

```bash
scripts/check-notifications.sh <your-agent-name>        # View unread
scripts/check-notifications.sh <your-agent-name> yes    # View and mark as read
```

**Workflow:**
1. Run `check-notifications.sh` at session start or after submitting a request
2. Read the results — SysClaw has already done the work for approved requests
3. Mark as read when done

## Automatic Notification Checking

Set up a cron job so responses are ready when your session starts:

```bash
# Create wrapper script
cat > /usr/local/bin/check-sysclaw-notifications.sh << 'SCRIPT'
#!/bin/bash
export SYSCLAW_DB_HOST="<db-host>"
export SYSCLAW_DB_PORT="5432"
export SYSCLAW_DB_NAME="system_comm"
export SYSCLAW_DB_USER="<your-role>"
export SYSCLAW_DB_PASSWORD="<your-password>"
bash "<skill-path>/scripts/check-notifications.sh" <your-agent-name> > "<workspace>/memory/notifications.md" 2>/dev/null
SCRIPT
chmod +x /usr/local/bin/check-sysclaw-notifications.sh

# Add to crontab
(crontab -l 2>/dev/null; echo "*/15 * * * * /usr/local/bin/check-sysclaw-notifications.sh") | crontab -
```

Then at session start: `cat memory/notifications.md`

## Direct SQL (Alternative to Scripts)

If you prefer direct database access:

```sql
-- Report issue
INSERT INTO issues (source, severity, category, title, details, source_host)
VALUES ('jobhunter', 'warning', 'disk', 'Disk usage high', 'Partition at 85%', 'srv-prod-01');

-- Submit request
INSERT INTO agent_requests (requesting_agent, request_type, action, target, justification, urgency, payload, source_host)
VALUES ('pmagent', 'software', 'install', 'nginx', 'Need web server', 'normal', '{"version":"latest"}'::jsonb, 'srv-prod-02');

-- Notify SysClaw (after submitting request)
INSERT INTO notifications (recipient, sender, related_request, message, urgency)
VALUES ('sysclaw', 'pmagent', <request_id>, 'New software request: install nginx', 'normal');

-- Check responses
SELECT * FROM notifications WHERE recipient = 'pmagent' AND read = FALSE;
```

Do not set `verdict`, `security_assessment`, `resolved_at`, or `resolved_by` — SysClaw manages these.

## Post-Install

1. **TOOLS.md** — Add DB host, user, and connection details
2. **Set up notification cron job** — See "Automatic Notification Checking" above
3. **Test:**
   ```bash
   scripts/report-issue.sh <your-source> info "SysClaw reporting skill installed - test"
   ```

## Technical Notes

- Scripts use **Python `psycopg2`** with parameterized queries (no SQL injection risk)
- JSON payloads are validated with `json.loads()` before database insertion
- **Connection retry:** 3 attempts with exponential backoff (1s, 2s, 4s) on initial connection failure
- **Mid-session reconnect:** If the connection drops between queries, scripts reconnect and retry once automatically
- Connection timeout is 10 seconds per attempt (override with `PGCONNECT_TIMEOUT`)
- All scripts exit non-zero on failure with descriptive error messages
