---
name: uplo-customer-success
description: AI-powered customer success knowledge management. Search account health data, onboarding records, renewal tracking, and support escalation documentation with structured extraction.
---

# UPLO Customer Success — Retention Intelligence

Every churned account tells the same story in hindsight: the signals were there, scattered across Gainsight health scores, Zendesk tickets, Slack threads, and CSM meeting notes that nobody connected in time. UPLO Customer Success consolidates these signals into structured, searchable knowledge so your team can act on patterns rather than react to surprises.

## Session Start

Establish your CSM identity. This loads your book of business, clearance level (some account financials may be restricted), and team assignments:

```
get_identity_context
```

## When to Use

- Reviewing the onboarding status of a new account — which milestones are complete, which are blocked, and who owns the blockers
- Preparing a risk assessment for the monthly CS leadership review by pulling health trends across your portfolio
- A customer champion just left and you need to find every documented relationship and handoff note for that contact
- Investigating whether a support escalation pattern (e.g., repeated SSO issues) is isolated to one account or systemic
- Building an expansion case by documenting product adoption milestones and quantified value delivered
- Checking the renewal playbook and comparing it against how the last five similar-ARR renewals were handled
- A new CSM is inheriting accounts mid-cycle and needs the full account narrative, not just the CRM fields

## Example Workflows

### Onboarding Health Check

A VP of CS wants a status report on all accounts currently in onboarding (first 90 days).

```
search_with_context query="customer onboarding status milestones blocked incomplete accounts first 90 days"
```

For a specific account that appears stuck:

```
search_knowledge query="TechFlow Inc onboarding integration API setup blockers"
```

Flag the systemic issue if integration delays are a pattern:

```
report_knowledge_gap query="onboarding integration delay patterns common blockers resolution playbook"
```

```
log_conversation summary="Onboarding health check across portfolio; identified TechFlow integration blocker and pattern of API setup delays across 3 accounts" topics='["onboarding","health-check","integration-blockers"]' tools_used='["search_with_context","search_knowledge","report_knowledge_gap"]'
```

### Champion Change Playbook

A key customer champion at a strategic account has moved to a new role. The CSM needs to execute the champion change playbook.

```
search_knowledge query="DataVault Corp primary contact stakeholder relationships decision makers"
```

```
search_with_context query="DataVault Corp engagement history executive sponsor interactions value delivered metrics"
```

Check directives for any special handling requirements on strategic accounts:

```
get_directives
```

## Key Tools for Customer Success

**search_with_context** — CS questions are relational by nature. "Is this account healthy?" requires connecting usage data, support history, CSM notes, and billing status. The graph traversal assembles these automatically. Example: `search_with_context query="Pinnacle Systems account health support tickets product usage renewal date"`

**search_knowledge** — Targeted retrieval for specific CS artifacts: onboarding checklists, success plans, meeting notes, QBR decks. Example: `search_knowledge query="Pinnacle Systems success plan Q2 goals"`

**report_knowledge_gap** — When you find an account with no success plan, no documented business outcomes, or missing stakeholder mapping, report it. These gaps are leading indicators of churn.

**flag_outdated** — Success plans, stakeholder maps, and value documentation go stale. A success plan from 18 months ago with the wrong executive sponsor listed is worse than no plan — it creates false confidence.

**propose_update** — When you discover new information during an account review (new stakeholder, updated business objective, changed renewal date), propose the update to keep the knowledge base current.

## Tips

- Health score queries work best when you specify the dimension: "product adoption health" vs. "support health" vs. "relationship health." The extraction engine often indexes these separately.
- CSM handoff is the highest-risk moment in the customer lifecycle. Use `export_org_context` combined with account-specific searches to build a comprehensive handoff document rather than relying on a 30-minute call.
- When documenting value delivered, use quantified language that the extraction engine can index: "reduced ticket volume by 34%" rather than "significantly improved support experience."
- Escalation patterns are more valuable than individual escalations. If you notice a theme across multiple accounts (e.g., "billing discrepancy" escalations spiking), use `report_knowledge_gap` to flag it as a systemic issue.
