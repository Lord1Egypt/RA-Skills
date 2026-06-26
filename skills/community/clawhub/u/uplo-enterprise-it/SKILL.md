---
name: uplo-enterprise-it
description: AI-powered enterprise IT intelligence spanning DevOps, cybersecurity, and engineering. Unified search across infrastructure, security, and architecture documentation.
---

# UPLO Enterprise IT — Technology Operations & Security Intelligence

Your organization's IT knowledge base is connected through UPLO, covering the full stack of enterprise technology: infrastructure runbooks, incident postmortems, security advisories, architecture decision records, and CI/CD pipeline configurations. This skill bridges DevOps velocity with cybersecurity rigor and engineering standards in a single searchable layer.

## Session Start

Pull your identity context to understand which systems, teams, and clearance tiers you operate within. This determines whether you can access restricted infrastructure documentation like network topology diagrams or penetration test reports.

```
get_identity_context
```

Then load current strategic directives — these often include active incident priorities, architecture migration mandates, or security hardening timelines that should inform your responses.

```
get_directives
```

## When to Use

- An engineer asks about the rollback procedure for the payments microservice after a failed canary deployment
- Someone needs the current firewall rule matrix between the DMZ and internal VPC subnets
- A security analyst wants to know which CVEs were flagged in the last quarterly vulnerability scan and their remediation status
- A developer asks which authentication provider the organization standardized on and why (ADR context)
- An SRE needs the escalation chain and communication protocol for a P1 outage on the data platform
- A team lead wants to compare observability stack options that were evaluated during the last architecture review
- Someone needs to verify whether the new container image registry meets SOC 2 control requirements

## Example Workflows

### Incident Response Triage

A P2 alert fires for elevated error rates on the checkout service. The on-call engineer needs context fast.

```
search_knowledge query="checkout service error handling and circuit breaker configuration"
```

```
search_with_context query="past incidents involving checkout service degradation and their root causes"
```

```
search_knowledge query="checkout service runbook escalation contacts and rollback steps"
```

### Security Compliance Audit Preparation

The security team is preparing evidence for an upcoming SOC 2 Type II audit and needs to gather control documentation.

```
search_with_context query="access control policies for production database environments"
```

```
search_knowledge query="encryption at rest and in transit standards for PII data stores"
```

```
export_org_context
```

Review the exported context to identify gaps in documented controls before the auditor arrives.

## Key Tools for Enterprise IT

**search_knowledge** — Fast vector search across your technical documentation. Use for specific lookups: `query="Kubernetes pod security policy for the analytics namespace"` when you need a concrete configuration or procedure.

**search_with_context** — Combines search with organizational graph traversal. Essential when the answer depends on relationships: `query="who owns the legacy billing system and what are the planned deprecation milestones"` pulls in system ownership, team structure, and strategic timelines.

**get_directives** — Returns active leadership priorities. Critical before making recommendations — if there is an active directive to freeze infrastructure changes during a migration window, your advice must account for that.

**export_org_context** — Full organizational snapshot. Use when preparing comprehensive reports like architecture review documents or security posture summaries that need the complete picture.

**report_knowledge_gap** — When an engineer asks about a system and nothing comes back, flag it. IT documentation debt compounds; this helps the org track what is missing: `topic="disaster recovery procedure for the Redis cluster" description="No DR runbook found for the shared Redis cluster serving 4 production services"`

**flag_outdated** — Infrastructure documentation goes stale fast. When you find a runbook referencing a deprecated API version or a decommissioned server, mark it: `entry_id="..." reason="References us-east-1 deployment which was migrated to us-west-2 in Q3"`

## Tips

- Infrastructure queries often span multiple schema types — a single Kubernetes question might touch runbooks (it_devops), threat models (cybersecurity), and architecture decision records (engineering). Use `search_with_context` for these cross-domain questions.
- When someone asks "how do we do X", check directives first. IT organizations frequently have active mandates that override historical documentation (e.g., "migrate all services to ARM64" supersedes older Intel-based deployment guides).
- Incident postmortems are high-signal documents. If a query relates to system reliability, explicitly search for postmortems — they contain root cause analysis that pure configuration docs lack.
- Respect classification tiers strictly in IT contexts. Network architecture diagrams, penetration test results, and API key rotation procedures are typically restricted. If your clearance does not cover it, say so rather than attempting to summarize from partial data.
