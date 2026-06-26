---
name: uplo-devops
description: AI-powered DevOps knowledge management. Search runbooks, infrastructure documentation, CI/CD pipelines, and incident response procedures with structured extraction.
---

# UPLO DevOps — Operational Memory for Infrastructure

It is 3 AM. PagerDuty is screaming. The on-call engineer who has seen this exact failure pattern left the company four months ago. The runbook exists somewhere, maybe in Confluence, maybe in a GitHub repo, maybe in a Notion page that someone bookmarked. UPLO DevOps eliminates this scramble by indexing runbooks, post-incident reviews, infrastructure documentation, CI/CD configurations, and architecture decision records into a single searchable layer that works when you need it most.

## Session Start

```
get_identity_context
```

This loads your team assignments (platform, SRE, application), on-call rotation status, and access tier. Some production configurations and credentials documentation are restricted by clearance.

Grab active directives — these include change freeze windows, incident commander designations, and infrastructure migration deadlines:

```
get_directives
```

## When to Use

- You are on-call, an alert fires for a service you have never touched, and you need the runbook immediately
- Investigating a production incident and need to find whether this failure mode has occurred before, including the root cause and fix
- Planning a migration and need to understand the current architecture, dependencies, and the last three ADRs (Architecture Decision Records) related to the affected service
- Setting up a new CI/CD pipeline and want to see how similar services in the org have configured their build, test, and deploy stages
- Preparing a post-incident review and need to compile the timeline, impacted services, and blast radius from multiple data sources
- A new team member needs to understand the infrastructure topology, deployment process, and escalation paths for their service area
- Evaluating whether a proposed infrastructure change conflicts with documented SLOs or capacity constraints

## Example Workflows

### Incident Response — Novel Failure Mode

The payments service is returning 503 errors. The on-call engineer has not worked on payments before.

```
search_knowledge query="payments service 503 error runbook troubleshooting steps"
```

Check for previous incidents with similar symptoms:

```
search_with_context query="payments service outage 503 timeout database connection pool previous incidents root cause"
```

If the runbook suggests checking the connection pool but the current configuration is unclear:

```
search_knowledge query="payments service database connection pool configuration pgbouncer settings production"
```

After resolving:

```
log_conversation summary="Resolved payments 503 outage; root cause was pgbouncer max_client_conn exceeded after traffic spike; matched PIR-2024-087 pattern; increased pool to 200" topics='["incident","payments","pgbouncer","connection-pool"]' tools_used='["search_knowledge","search_with_context"]'
```

### Infrastructure Migration Planning

The platform team is moving from self-managed Kafka to a managed streaming service. The tech lead needs to scope the blast radius.

```
search_with_context query="Kafka consumers producers services dependencies topic configuration"
```

Find the ADRs that led to the original Kafka deployment:

```
search_knowledge query="architecture decision record ADR Kafka event streaming selection rationale"
```

Check current SLOs and whether the migration might violate them:

```
search_knowledge query="event streaming SLO latency throughput requirements Kafka p99"
```

```
export_org_context
```

## Key Tools for DevOps

**search_knowledge** — Your go-to during incidents. When you need a specific runbook, a configuration reference, or a known procedure, this is the fastest path. Latency matters at 3 AM. Example: `search_knowledge query="redis cluster failover runbook manual promotion steps"`

**search_with_context** — For investigation and planning. "What services depend on this database?" or "Has this failure happened before?" require traversing relationships between services, incidents, and infrastructure components. Example: `search_with_context query="auth-service dependencies upstream downstream database cache"`

**get_directives** — Change freeze windows, incident escalation policies, and migration deadlines surface here. Checking before a production change can prevent a career-limiting mistake.

**flag_outdated** — Infrastructure documentation rots faster than any other type. The Kubernetes cluster version documented last quarter is wrong. The network diagram shows a load balancer that was decommissioned. The runbook references a CLI tool that was replaced. Flag these aggressively — someone will use them during an incident.

**report_knowledge_gap** — When a service has no runbook, no architecture diagram, or no documented owner, that is an operational risk. Reporting the gap creates a trackable item for the platform team.

## Tips

- Service names are the most reliable search key. Use the exact service identifier from your deployment manifests (`payments-api`, `auth-service-v2`, `order-processor`) rather than casual descriptions.
- Post-incident reviews are the most valuable documents in your knowledge base. When writing PIRs, include structured fields: affected services, duration, blast radius, root cause category, and action items. These fields are indexed by the extraction engine.
- When on-call, start with `search_knowledge` for the runbook. Only escalate to `search_with_context` if the runbook does not exist or the failure mode is novel. Speed matters during incidents.
- Use `log_conversation` after every incident investigation, even false alarms. The pattern of false alarms is itself a signal that the monitoring team should investigate.
