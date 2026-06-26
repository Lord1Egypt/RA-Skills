# Database Schema Reference

## Server

- **Database:** system_comm
- **Authentication:** TCP with password (scram-sha-256)

## Table: issues

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | serial | PK | Auto-increment |
| source | varchar(50) | NOT NULL | Agent name |
| severity | varchar(20) | NOT NULL, default 'info' | `info` \| `warning` \| `critical` |
| category | varchar(50) | nullable | `disk` \| `service` \| `error` \| `resource` \| `network` \| `config` \| `other` |
| title | varchar(255) | NOT NULL | Short description |
| details | text | nullable | Extended context, error output |
| status | varchar(20) | default 'open' | SysClaw manages: `open` → `resolved` |
| resolved_at | timestamp | nullable | Set by SysClaw |
| resolved_by | varchar(50) | nullable | `sysclaw` or `virus` |
| created_at | timestamp | default CURRENT_TIMESTAMP | |
| updated_at | timestamp | default CURRENT_TIMESTAMP | |
| source_host | varchar(100) | nullable | Hostname/IP of the originating machine |

**Indexes:** severity, source, status, source_host

**Agent permissions:** INSERT + SELECT only. Do not UPDATE status — SysClaw owns this.

## Table: agent_requests

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | serial | PK | Auto-increment |
| requesting_agent | varchar(50) | NOT NULL | Agent name |
| request_type | varchar(30) | NOT NULL | See valid types below |
| action | varchar(30) | NOT NULL | `install` \| `remove` \| `create` \| `modify` \| `restart` \| `grant` \| `check` \| `deploy` |
| target | varchar(255) | NOT NULL | What this request applies to |
| justification | text | NOT NULL | **Required.** Why this is needed |
| payload | jsonb | nullable | Request-specific details |
| urgency | varchar(20) | NOT NULL, default 'normal' | `low` \| `normal` \| `urgent` |
| verdict | varchar(20) | NOT NULL, default 'pending' | SysClaw manages: `pending` → `approved` \| `denied` \| `escalated` |
| security_assessment | text | nullable | SysClaw writes risk analysis |
| escalated | boolean | NOT NULL, default false | Whether Virus was notified |
| escalation_reason | text | nullable | Why it was escalated |
| created_at | timestamp | default CURRENT_TIMESTAMP | |
| resolved_at | timestamp | nullable | Set by SysClaw |
| resolved_by | varchar(50) | nullable | `sysclaw` or `virus` |
| updated_at | timestamp | default CURRENT_TIMESTAMP | |
| source_host | varchar(100) | nullable | Hostname/IP of the originating machine |

**Indexes:** verdict, requesting_agent, request_type, created_at, source_host

### Valid Request Types

| Type | Use For |
|------|---------|
| `access` | Directory/file access, SSH, DB credentials, network access |
| `software` | Install, update, remove packages |
| `resource` | New database, DB user, disk space, CPU/RAM |
| `config` | Edit config files, cron jobs, firewall rules, env vars |
| `service` | Start, stop, restart services |
| `deployment` | Deploy code, rollback, update running services |
| `info` | Server status, resource usage, health checks |

**Agent permissions:** INSERT + SELECT only. Do not UPDATE verdict, security_assessment, or any column after creation. SysClaw manages all status transitions.

## Table: notifications

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | serial | PK | Auto-increment |
| recipient | varchar(50) | NOT NULL | Agent name or 'sysclaw' |
| sender | varchar(50) | NOT NULL | Who sent the notification |
| related_request | integer | FK → agent_requests(id) | Optional link to request |
| message | text | NOT NULL | Notification content |
| urgency | varchar(20) | default 'normal' | `low` \| `normal` \| `urgent` |
| read | boolean | default FALSE | Whether recipient has read it |
| created_at | timestamp | default CURRENT_TIMESTAMP | |

**Indexes:** (recipient, read), (created_at)

**Agent permissions:** INSERT, SELECT, UPDATE (read column only). Agents INSERT to notify SysClaw or respond to requests. Agents UPDATE read=TRUE on their own notifications after processing.

## Table: worklog

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | serial | PK | Auto-increment |
| request_id | integer | FK → agent_requests(id) | Related request |
| action | varchar(50) | NOT NULL | What was done |
| target | varchar(255) | NOT NULL | Where it was done |
| executed_by | varchar(50) | NOT NULL, default 'sysclaw' | Who executed |
| command | text | nullable | Command or action taken |
| result | text | nullable | Outcome |
| status | varchar(20) | NOT NULL, default 'in_progress' | `in_progress` \| `completed` \| `failed` \| `verified` |
| started_at | timestamp | default CURRENT_TIMESTAMP | |
| completed_at | timestamp | nullable | |

**Indexes:** (request_id), (status)

**Agent permissions:** SELECT only. SysClaw writes all worklog entries.

## Roles

| Role | issues | agent_requests | notifications | worklog |
|------|--------|----------------|---------------|---------|
| jobagent | INSERT, SELECT | INSERT, SELECT | INSERT, SELECT, UPDATE (read) | SELECT |
| pmagent | INSERT, SELECT | INSERT, SELECT | INSERT, SELECT, UPDATE (read) | SELECT |
| researcher_agent | INSERT, SELECT | INSERT, SELECT | INSERT, SELECT, UPDATE (read) | SELECT |
| system_agent | INSERT, SELECT | INSERT, SELECT | INSERT, SELECT, UPDATE (read) | SELECT |
| issue_reporter | INSERT, SELECT | INSERT, SELECT | INSERT, SELECT, UPDATE (read) | SELECT |
| postgres | ALL | ALL | ALL | ALL |

> **Note:** INSERT requires USAGE on sequences. If you get `permission denied for sequence`, ask your SysClaw operator.

## Status Flows

```
issues:          open → resolved
agent_requests:  pending → approved | denied | escalated → (resolved by human operator if escalated)
```
```
