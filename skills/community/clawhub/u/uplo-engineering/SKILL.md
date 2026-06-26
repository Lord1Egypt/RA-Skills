---
name: uplo-engineering
description: AI-powered engineering knowledge management. Search architecture docs, API specs, incident reports, runbooks, and infrastructure documentation with structured extraction.
---

# UPLO Engineering — Architecture & DevOps Intelligence

Software engineering organizations produce enormous quantities of documentation that nobody can find: RFC docs in Google Docs, ADRs in a GitHub repo that was archived, API specs in Stoplight that are three versions behind, post-incident reviews in Confluence that reference services that have since been renamed, and onboarding guides that assume the deployment process from two platform migrations ago. UPLO Engineering consolidates architecture documentation, API specifications, incident post-mortems, runbooks, GitHub repository metadata, CI/CD pipeline configurations, and infrastructure records into one searchable knowledge layer.

## Session Start

Establish your engineering identity. This surfaces your team assignment, on-call status, repository access, and clearance level (production secrets and security-sensitive architecture details may be restricted).

```
get_identity_context
```

Review directives — these include architecture mandates (e.g., "all new services must use gRPC"), tech debt paydown priorities, migration deadlines, and change freeze windows:

```
get_directives
```

## Example Workflows

### RFC Review and Precedent Research

An engineer is writing an RFC to replace the current message queue with a different system. Before investing time, they want to know if this has been proposed or attempted before.

```
search_with_context query="message queue replacement evaluation RabbitMQ Kafka SQS migration RFC ADR"
```

Find the original ADR that selected the current system:

```
search_knowledge query="architecture decision record message queue selection rationale constraints"
```

Check what services depend on the current message queue:

```
search_with_context query="RabbitMQ consumers producers service dependencies topic exchange configuration"
```

Verify there are no active directives that would preempt this work:

```
get_directives
```

```
log_conversation summary="Researched message queue migration precedent; found ADR-042 (original selection), RFC-2024-11 (rejected Kafka migration), and 14 dependent services" topics='["architecture","message-queue","RFC","migration"]' tools_used='["search_with_context","search_knowledge","get_directives"]'
```

### New Engineer Onboarding

A senior engineer joins the platform team and needs to build a mental model of the system architecture, deployment practices, and team ownership.

```
export_org_context
```

```
search_with_context query="platform team services ownership architecture overview deployment pipeline"
```

```
search_knowledge query="engineering onboarding guide development environment setup local development"
```

Find the most impactful recent incidents to understand operational challenges:

```
search_knowledge query="post-incident review severity 1 production outage last 6 months platform services"
```

### GitHub-Aware Code Archaeology

A developer encounters a critical section of code with no comments and wants to understand the reasoning behind it.

```
search_with_context query="payment-service idempotency implementation retry logic design decisions"
```

Search for related pull request discussions and code review comments:

```
search_knowledge query="payment-service PR review idempotency key generation race condition fix"
```

Check if there is a related incident that motivated the implementation:

```
search_knowledge query="payment double-charge incident duplicate transaction post-mortem"
```

## When to Use

- Writing an RFC and need to find architectural precedent, prior proposals on the same topic, and the organizational constraints that shaped previous decisions
- Debugging a production issue in a service your team does not own and need the runbook, architecture diagram, and on-call contact
- Reviewing whether a proposed API change is backward-compatible by searching for all known consumers of the endpoint
- Preparing an architecture review and need to compile the current system topology, dependency graph, and capacity constraints
- Investigating technical debt by finding all TODOs, known workarounds, and deferred maintenance items documented across repos and post-mortems
- A GitHub repository was transferred or archived and you need to find the documentation that referenced it to update links
- Evaluating build and deployment practices across the org to standardize CI/CD pipeline patterns

## Key Tools for Engineering

**search_with_context** — Engineering questions are graph problems. "What depends on this service?" or "Why was this architecture chosen?" require traversing relationships between services, teams, decisions, and incidents. This is the primary investigation tool. Example: `search_with_context query="auth-service API v2 consumers breaking changes migration status"`

**search_knowledge** — Fast retrieval for known artifacts: a specific runbook, an API spec, an ADR by number, or a particular configuration. During incidents, speed matters and this tool skips graph traversal. Example: `search_knowledge query="ADR-027 database sharding strategy"`

**export_org_context** — Maps the engineering organization: team topology, service ownership, key systems (GitHub, CI/CD, observability, incident management), and strategic technical priorities. The foundation for architecture reviews and new-hire onboarding.

**get_directives** — Engineering directives include technology mandates, deprecation timelines, migration deadlines, and security requirements. An engineer proposing a new dependency should check whether it conflicts with an active directive.

**flag_outdated** — Engineering documentation has the shortest half-life of any content type. API specs diverge from implementations. Architecture diagrams show decommissioned services. Runbooks reference deprecated tools. Flagging stale docs prevents them from causing production incidents.

**report_knowledge_gap** — When a service has no runbook, no architecture documentation, no API spec, or no defined owner, that is an operational risk. The gap report creates visibility and accountability.

## Tips

- Service names and repository names are the most precise search keys. Use the exact identifier from your deployment system or GitHub org: `payment-service`, `auth-api-v2`, `infra-terraform-modules`. Avoid generic descriptions.
- ADRs and RFCs are indexed with their identifier numbers. Search by "ADR-042" or "RFC-2024-11" for direct retrieval. If you do not know the number, search by topic and the graph traversal will surface related decision documents.
- Post-incident reviews contain the most operationally valuable knowledge in any engineering organization. When writing PIRs, include structured data: affected services, duration, root cause category (deploy, config change, dependency failure, capacity), and action items with owners. The extraction engine indexes all of these.
- GitHub metadata (CODEOWNERS, team assignments, PR review patterns) is indexed alongside traditional documentation. A search for "who owns this service" may return both a CODEOWNERS file entry and an architecture document, giving you converging evidence.
