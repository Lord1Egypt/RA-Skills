---
name: sysclaw-ops
description: >
  SysClaw operator skill for processing agent requests and managing the cross-agent
  communication system. Use when SysClaw needs to check for pending agent requests,
  review issues, process verdicts, send notifications back to agents, or manage the
  system_comm database. This is the server-side counterpart to sysclaw-reporting.
  Triggers on phrases like check agent requests, process notifications, review requests,
  pending agent requests, agent needs approval.
---

# SysClaw Ops (Server)

Server-side operations for the cross-agent communication system. This skill covers how SysClaw processes incoming requests, manages notifications, and communicates with agents.

## Required Credentials

| Credential | Purpose | Minimal Privileges |
|------------|---------|-------------------|
| `SYSCLAW_DB_HOST` | PostgreSQL host (MB-ClawTool-01) | Network access to port 5432 |
| `SYSCLAW_DB_PORT` | PostgreSQL port (5432) | — |
| `SYSCLAW_DB_NAME` | Database name (system_comm) | CONNECT privilege |
| `SYSCLAW_DB_USER` | DB role for SysClaw | See privileges below |
| `SYSCLAW_DB_PASSWORD` | DB password | — |
| Telegram bot token | For escalating urgent requests to the human operator | Configured via OpenClaw |

**Minimal DB privileges required:**
```sql
-- agent_requests table
GRANT SELECT, UPDATE (verdict, security_assessment, resolved_at, resolved_by, escalated, escalation_reason)
  ON agent_requests TO <sysclaw_role>;

-- issues table
GRANT SELECT, UPDATE (status, resolved_at, resolved_by) ON issues TO <sysclaw_role>;

-- notifications table
GRANT SELECT, INSERT, UPDATE (read) ON notifications TO <sysclaw_role>;
```

## Installation

This skill is designed for the **SysClaw operator** (an OpenClaw agent running on the server that manages infrastructure). It is not a standalone daemon.

### Components

1. **This SKILL.md** — Instructions for the SysClaw agent on processing requests
2. **OpenClaw cron job** — `sysclaw-notification-check` (see below)
3. **Telegram integration** — Via OpenClaw's session delivery to the human operator

### Cron Job Setup

The `sysclaw-notification-check` is an **OpenClaw cron job**, not a system binary. It runs as an isolated agent session within OpenClaw:

```json
{
  "name": "sysclaw-notification-check",
  "schedule": { "kind": "cron", "expr": "*/15 * * * *", "tz": "Europe/Copenhagen" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Check for new agent notifications and process requests. Use sysclaw-ops skill for workflow.",
    "timeoutSeconds": 120
  },
  "delivery": { "mode": "announce" }
}
```

Created via OpenClaw cron API. The agent session has access to SSH and DB tools — no separate binary needed.

### Telegram Integration

Escalated requests are flagged in the database by the cron job. **SysClaw checks for escalated requests** during its normal session workflow and notifies the human operator on Telegram using OpenClaw's messaging. The cron job itself does not send Telegram messages.

## Database Tables

### `agent_requests` — Requests from agents

| Column | Type | Notes |
|--------|------|-------|
| id | serial | PK |
| requesting_agent | varchar(50) | Agent name |
| request_type | varchar(30) | access, software, resource, config, service, deployment, info |
| action | varchar(30) | install, remove, create, modify, restart, grant, check, deploy |
| target | varchar(255) | What this applies to |
| justification | text | Why it's needed |
| payload | jsonb | Request-specific details |
| urgency | varchar(20) | low, normal, urgent |
| verdict | varchar(20) | pending → approved | denied | escalated |
| security_assessment | text | SysClaw writes risk analysis |
| escalated | boolean | Whether the human operator was notified |
| created_at | timestamp | |
| resolved_at | timestamp | Set by SysClaw |
| resolved_by | varchar(50) | sysclaw or the human operator |
| source_host | varchar(100) | Originating machine |

### `issues` — Issues reported by agents

| Column | Type | Notes |
|--------|------|-------|
| id | serial | PK |
| source | varchar(50) | Agent name |
| severity | varchar(20) | info, warning, critical |
| category | varchar(50) | disk, service, error, resource, network, config, other |
| title | varchar(255) | Short description |
| details | text | Extended context |
| status | varchar(20) | open → resolved |
| created_at | timestamp | |
| source_host | varchar(100) | Originating machine |

### `notifications` — Agent ↔ SysClaw communication

| Column | Type | Notes |
|--------|------|-------|
| id | serial | PK |
| recipient | varchar(50) | Agent name or 'sysclaw' |
| sender | varchar(50) | Who sent it |
| related_request | integer | FK → agent_requests(id) |
| message | text | Notification content |
| urgency | varchar(20) | low, normal, urgent |
| read | boolean | Whether recipient has processed it |
| created_at | timestamp | |

### `worklog` — SysClaw action log

| Column | Type | Notes |
|--------|------|-------|
| id | serial | PK |
| request_id | integer | FK → agent_requests(id) |
| action | varchar(50) | What was done |
| target | varchar(255) | Where it was done |
| executed_by | varchar(50) | sysclaw or agent name |
| command | text | Command or action taken |
| result | text | Outcome |
| status | varchar(20) | in_progress, completed, failed, verified |
| started_at | timestamp | |
| completed_at | timestamp | |

> **Full schema reference:** See [`references/db-schema.md`](references/db-schema.md) for detailed column constraints, indexes, role permissions, and status flows.

## Processing Workflow

### Check for new notifications

```sql
SELECT * FROM notifications WHERE recipient = 'sysclaw' AND read = FALSE ORDER BY created_at ASC;
```

### Process a pending request

Agents submit requests because they **can't do it themselves**. When SysClaw approves, SysClaw executes.

> _Note: These queries show the pattern. Use parameterized queries or your agent's DB tooling — never interpolate values directly._

```sql
-- 1. Read the request
SELECT * FROM agent_requests WHERE id = <request_id>;

-- 2. Assess and update verdict
UPDATE agent_requests
SET verdict = 'approved',
    security_assessment = 'Low risk: standard package install on managed VM',
    resolved_at = NOW(),
    resolved_by = 'sysclaw'
WHERE id = <request_id>;

-- 3. Log to worklog
INSERT INTO worklog (request_id, action, target, command, status)
VALUES (<request_id>, '<action>', '<target>', '<what SysClaw will do>', 'in_progress');

-- 4. Execute the action (SSH to target, run command, verify)

-- 5. Update worklog with result
UPDATE worklog SET status = 'completed', result = '<outcome>', completed_at = NOW() WHERE id = <worklog_id>;

-- 6. Write response notification back to agent
INSERT INTO notifications (recipient, sender, related_request, message, urgency)
VALUES ('jobhunter', 'sysclaw', <request_id>, 'Request #5 DONE: cron installed and verified on MB-OpenClaw-01', 'normal');

-- 7. Mark sysclaw's notification as read
UPDATE notifications SET read = TRUE WHERE id = <notification_id>;
```

### Execution by Request Type

| Request type | Action |
|---|---|
| `info` | SSH to target, run check, write result to worklog + notification |
| `software` | SSH to target, install package, verify service running |
| `config` | SSH to target, apply config change, verify |
| `service` | SSH to target, restart/stop/start service, verify status |
| `resource` | Create DB/user/allocation if SysClaw has access; escalate infrastructure requests |
| `deployment` | SSH to target, deploy per request details, verify |
| `access` | **Escalate to human operator** — never auto-approved |

### Escalate to the human operator

For urgent requests or high-risk actions:
1. Set `verdict = 'escalated'`, `escalated = TRUE`, `escalation_reason = '<reason>'`
2. The request is now flagged for human review
3. **SysClaw checks for escalated requests** during its next session and notifies the human operator on Telegram
4. The human operator reviews and decides
5. SysClaw updates the verdict and notifies the requesting agent

> **Note:** The cron job does NOT send Telegram messages directly. It flags requests as escalated. SysClaw handles Telegram notification during its normal session workflow.
4. SysClaw updates verdict and notifies the requesting agent

### Resolve an issue

```sql
UPDATE issues SET status = 'resolved', resolved_at = NOW(), resolved_by = 'sysclaw' WHERE id = <issue_id>;
```

## Decision Guidelines

**Auto-approve (low risk):**
- Software installs on managed VMs (standard packages)
- Info/check requests (disk, service status)
- Config changes to agent's own workspace

**escalate to the human operator (high risk):**
- Access requests (SSH keys, DB credentials, new users)
- Firewall or network changes
- Production service restarts
- Anything modifying shared infrastructure
- Requests marked `urgency = 'urgent'`

The human operator and infrastructure owner. All high-risk decisions require the human operator's approval.

**Deny:**
- Requests without clear justification
- Dangerous operations (rm -rf, chmod 777)
- Conflicts with security policy

## Cron Job Behavior

The `sysclaw-notification-check` OpenClaw cron job runs every 15 minutes:
1. Checks `notifications WHERE recipient = 'sysclaw' AND read = FALSE`
2. For each notification, reads the related request
3. Assesses risk per Decision Guidelines above
4. **Low risk** → approves, executes the action, logs to worklog, notifies agent with result
5. **High risk** → flags as `verdict='escalated'` for human review
6. Marks processed notifications as read

**This is not a system cron job or binary.** It runs within the OpenClaw framework as an isolated agent session with access to SSH and DB tools.

## SysClaw Escalation Handling

SysClaw checks for escalated requests during its **heartbeat** and regular sessions:

1. Query: `SELECT * FROM agent_requests WHERE verdict = 'escalated' AND resolved_at IS NULL`
2. For each escalated request, notify the human operator on Telegram with request details
3. Wait for human operator's decision
4. Update verdict, write security_assessment, set resolved_at/resolved_by
5. Write response notification back to the requesting agent

This is configured in SysClaw's `HEARTBEAT.md` to run on every heartbeat cycle.

## Useful Queries

```sql
-- Pending requests
SELECT id, requesting_agent, request_type, action, target, urgency, created_at
FROM agent_requests WHERE verdict = 'pending' ORDER BY created_at;

-- Recent activity
SELECT * FROM agent_requests ORDER BY created_at DESC LIMIT 10;

-- Open issues
SELECT id, source, severity, title, status FROM issues WHERE status = 'open';

-- Unread notifications by recipient
SELECT recipient, COUNT(*) FROM notifications WHERE read = FALSE GROUP BY recipient;
```

## Security Considerations

- **Principle of least privilege**: DB role should only have UPDATE on specific columns, not full table access
- **Audit trail**: All verdict changes are logged via `resolved_at`, `resolved_by`, and `security_assessment`
- **Human oversight**: High-risk requests always escalate to the human operator — SysClaw never auto-approposes access/infra changes
- **No secrets in skill**: Credentials are provided via OpenClaw environment, not stored in this skill
