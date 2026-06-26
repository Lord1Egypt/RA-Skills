# Entry Examples

Concrete examples of well-formatted operations entries with all fields.

## Learning: Process Bottleneck (Manual Deployment Approvals)

```markdown
## [LRN-20250415-001] process_bottleneck

**Logged**: 2025-04-15T10:30:00Z
**Priority**: medium
**Status**: pending
**Area**: change_management

### Summary
Deployment requires 3 manual approval steps, adding 2 hours to lead time

### Details
Production deployments require sign-off from team lead, security review, and
platform team approval. Each step involves a Slack message and manual response.
Average wait time per approval is 40 minutes. During off-hours, approvals can
take 4+ hours because approvers are unavailable. This process was designed for
quarterly releases but now blocks daily deployments.

### Impact
- **Blast Radius**: all engineering teams deploying to production
- **Duration**: 2 hours average, 4+ hours off-hours
- **Error Budget Consumed**: N/A (process issue, not incident)

### Metrics
- MTTR: N/A
- MTTD: N/A
- Frequency: 8-12 deployments per week
- Toil Hours: ~20 hours/week across all teams waiting for approvals

### Suggested Action
Replace manual approvals with automated policy gates:
1. Security review → automated SAST/DAST in CI pipeline
2. Team lead sign-off → required passing tests + code review approval
3. Platform approval → canary deployment with automated rollback on error rate spike

### Metadata
- Source: change_audit
- Environment: production
- Service: deployment-pipeline
- Tags: deployment, approval, lead-time, DORA, bottleneck
- Pattern-Key: process_bottleneck.manual_approval_chain

---
```

## Learning: Incident Pattern (Connection Pool Exhaustion)

```markdown
## [LRN-20250416-001] incident_pattern

**Logged**: 2025-04-16T09:15:00Z
**Priority**: high
**Status**: pending
**Area**: incident_management

### Summary
Database connection pool exhaustion recurring monthly during batch ETL jobs

### Details
On the 1st of each month, the full ETL job runs alongside normal API traffic.
Pool size is 50 connections. Batch ETL opens 40+ long-running connections for
data extraction, leaving fewer than 10 for API requests. API latency spikes from
50ms P99 to 3000ms+, and 503 errors begin within 5 minutes. The issue resolves
when the batch job completes (~30 minutes), but the pattern repeats monthly.

### Impact
- **Blast Radius**: all API consumers, estimated 15,000 users affected
- **Duration**: 20-30 minutes per occurrence
- **Error Budget Consumed**: ~8% of monthly error budget per occurrence

### Metrics
- MTTR: 35 minutes (once identified, wait for batch to finish)
- MTTD: 5 minutes (alert on P99 latency > 500ms)
- Frequency: monthly on the 1st
- Toil Hours: 1 hour per occurrence (paging, investigation, communication)

### Suggested Action
1. Separate connection pools: dedicated pool for batch ETL, separate for API
2. Install PgBouncer for connection multiplexing
3. Schedule full ETL during maintenance window (02:00-04:00 UTC)
4. Add connection pool utilization alert at 70% threshold

### Metadata
- Source: incident
- Environment: production
- Service: api-gateway, etl-pipeline, postgresql
- Related Alerts: db-connection-pool-high
- Tags: database, connection-pool, batch, ETL, monthly, recurring
- Pattern-Key: incident_pattern.connection_pool_exhaustion
- Recurrence-Count: 3
- First-Seen: 2025-02-01
- Last-Seen: 2025-04-01
- See Also: OPS-20250201-001, OPS-20250301-002

---
```

## Learning: Toil Accumulation (Certificate Renewals)

```markdown
## [LRN-20250417-001] toil_accumulation

**Logged**: 2025-04-17T14:00:00Z
**Priority**: high
**Status**: pending
**Area**: on_call

### Summary
On-call engineer spending 60% of time on manual TLS certificate renewals

### Details
15 internal services use TLS certificates that expire every 90 days. Renewal
requires: SSH to host, run certbot, update certificate files, restart service,
verify TLS handshake. Each renewal takes ~45 minutes. With staggered expiration
dates, on-call handles 2-3 renewals per week. Two incidents in the past quarter
were caused by forgotten certificate renewals.

### Impact
- **Blast Radius**: on-call engineer productivity, service reliability
- **Duration**: ongoing, ~6 hours/week of on-call time
- **Error Budget Consumed**: 2 incidents from expired certs consumed ~15% of quarterly budget

### Metrics
- Frequency: 2-3 times per week
- Toil Hours: 6 hours/week, 24 hours/month

### Suggested Action
Deploy cert-manager with Let's Encrypt for automatic renewal. Estimated 2 days
of engineering effort to implement, would eliminate all manual certificate toil
and prevent expiry-related incidents.

### Metadata
- Source: on_call_handoff
- Environment: production
- Service: all internal services with TLS
- Tags: certificates, TLS, toil, automation, on-call, cert-manager
- Pattern-Key: toil_accumulation.manual_cert_renewal

---
```

## Operations Issue: SLA Breach (API Latency)

```markdown
## [OPS-20250418-001] api_latency_slo_breach

**Logged**: 2025-04-18T08:30:00Z
**Priority**: critical
**Status**: pending
**Severity**: P2
**Area**: monitoring

### Summary
API latency P99 exceeded 500ms SLO for 4 hours during peak traffic

### Timeline
| Time (UTC) | Event |
|------------|-------|
| 04:15 | P99 latency crossed 500ms threshold |
| 04:45 | Alert fired after 30-min sustained breach |
| 05:10 | On-call acknowledged, began investigation |
| 06:30 | Root cause identified: cache eviction storm after deployment |
| 07:00 | Mitigation: increased cache TTL, warmed cache manually |
| 08:15 | P99 latency returned below 300ms |

### Impact
- **Users Affected**: ~40,000 users during peak morning traffic
- **Duration**: 4 hours of SLO breach
- **SLO Impact**: consumed 35% of monthly error budget in a single event

### Root Cause
A deployment at 04:00 UTC included a cache key format change. This invalidated
all existing cache entries, causing a thundering herd to the database. The
database handled the load but response times increased from 50ms to 800ms P99.
The alert threshold was set at 30 minutes sustained, delaying notification.

### Mitigation
Increased cache TTL from 5min to 15min, manually warmed top-1000 cache keys
from database, added cache warming step to deployment pipeline.

### Prevention
- Add cache warming to deployment pipeline (pre-warm before traffic shift)
- Reduce alert threshold from 30min to 10min sustained breach
- Implement gradual cache key migration instead of invalidate-all

### Action Items
- [ ] Add cache warming to deploy pipeline (SRE team, 2025-04-25)
- [ ] Reduce SLO breach alert threshold to 10min (monitoring team, 2025-04-20)
- [ ] Implement gradual cache key migration strategy (backend team, 2025-05-01)

### Metadata
- Trigger: alert
- Environment: production
- Services Affected: api-gateway, cache-layer, postgresql
- Related Incidents: OPS-20250312-003 (similar cache issue after deploy)
- DORA Metrics Impact: change_failure_rate, mttr

---
```

## Operations Issue: Capacity Issue (Disk Space)

```markdown
## [OPS-20250419-001] disk_space_critical

**Logged**: 2025-04-19T16:00:00Z
**Priority**: high
**Status**: pending
**Severity**: P2
**Area**: capacity_planning

### Summary
Disk usage hit 95% on primary database server, no alert configured below 90%

### Timeline
| Time (UTC) | Event |
|------------|-------|
| 14:30 | Application errors begin: "no space left on device" in WAL writes |
| 14:35 | On-call paged by application error alert (not disk alert) |
| 14:50 | Identified disk at 95%, WAL archiving backed up |
| 15:10 | Cleared old WAL files, freed 20% disk space |
| 15:20 | Database recovered, application errors stopped |

### Impact
- **Users Affected**: all write operations failed for 50 minutes
- **Duration**: 50 minutes of write degradation
- **SLO Impact**: consumed 12% of monthly error budget

### Root Cause
Disk usage alert was configured at 90% threshold only. Storage grew 18% in the
last month due to new audit logging feature, but capacity review missed the
projection. WAL archival was delayed, accumulating on primary disk.

### Mitigation
Cleared old WAL files, configured WAL archival to S3 with 1-hour max retention
on local disk, expanded volume by 50%.

### Prevention
- Add tiered disk alerts: 70% (warning), 80% (high), 90% (critical)
- Monthly capacity review including storage growth rate
- Auto-expansion policy for database volumes

### Metadata
- Trigger: monitoring
- Environment: production
- Services Affected: postgresql-primary
- DORA Metrics Impact: mttr

---
```

## Feature Request: Automated Runbook Execution

```markdown
## [FEAT-20250420-001] automated_runbook_execution

**Logged**: 2025-04-20T11:00:00Z
**Priority**: high
**Status**: pending
**Area**: automation

### Requested Capability
Automated execution of runbook steps for known incident types, triggered by
alert conditions matching incident patterns logged in OPERATIONS_ISSUES.md.

### User Context
On-call engineers follow the same runbook steps for 60% of P3/P4 incidents. These
steps are well-documented, deterministic, and safe to automate. Manual execution
adds 15-30 minutes to MTTR and requires on-call to be alert and responsive.
Automating known remediation would reduce MTTR for common incidents from 30 minutes
to under 5 minutes.

### Complexity Estimate
complex

### Suggested Implementation
1. Define runbook steps as executable scripts with pre/post-condition checks
2. Map alert conditions to runbook IDs in monitoring configuration
3. Build orchestrator that: receives alert → matches to runbook → executes steps
   → verifies post-conditions → pages human only if automation fails
4. Start with lowest-risk runbooks (restart service, clear cache, scale up replicas)
5. Track automation success rate and false-positive rate

### Metadata
- Frequency: recurring
- Related Features: PagerDuty automation, Rundeck, Ansible AWX

---
```

## Learning: Promoted to Runbook

```markdown
## [LRN-20250410-003] incident_pattern

**Logged**: 2025-04-10T11:00:00Z
**Priority**: high
**Status**: promoted
**Promoted**: runbook (RUNBOOK-db-connection-pool.md)
**Area**: incident_management

### Summary
Database connection pool exhaustion response procedure

### Details
After 3 occurrences of connection pool exhaustion (OPS-20250201-001,
OPS-20250301-002, OPS-20250401-001), the incident response steps were distilled
into a formal runbook with detection criteria, immediate response steps, and
verification commands.

### Metadata
- Source: incident
- Service: postgresql, api-gateway
- Tags: database, connection-pool, runbook, incident-response
- See Also: OPS-20250201-001, OPS-20250301-002, OPS-20250401-001

---
```

## Learning: Promoted to Skill

```markdown
## [LRN-20250412-001] incident_pattern

**Logged**: 2025-04-12T15:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/incident-response-checklist
**Area**: incident_management

### Summary
Systematic incident response checklist applicable across all service incidents

### Details
After reviewing 20+ incidents over 6 months, extracted a common incident response
checklist that applies regardless of the specific failure mode. Covers detection,
triage, communication, mitigation, recovery, and postmortem phases. Each phase
has specific actions, verification steps, and escalation criteria.

### Metadata
- Source: postmortem
- Service: all production services
- Tags: incident-response, checklist, SRE, postmortem
- See Also: OPS-20250201-001, OPS-20250315-002, OPS-20250401-001, LRN-20250410-003

---
```
