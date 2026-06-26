---
name: uplo-operations
description: AI-powered operations knowledge management. Search process documentation, capacity plans, resource allocation data, and KPI dashboards with structured extraction.
---

# UPLO Operations

Operations is the connective tissue of any organization — the processes, playbooks, capacity models, and performance metrics that keep everything running. This skill connects your AI assistant to UPLO's structured extraction of operational knowledge: SOPs, runbooks, capacity plans, incident postmortems, vendor SLAs, and the KPI data that tells you whether things are actually working.

## Session Start

Load your ops context to understand your role, team scope, and current operational priorities:

```
use_mcp_tool: get_identity_context
```

Then pull the latest on anything that might need immediate attention:

```
use_mcp_tool: search_knowledge query="active incidents open action items SLA breaches capacity warnings"
use_mcp_tool: get_directives
```

Directives for operations teams typically cover efficiency targets, cost reduction mandates, and service level commitments — knowing these frames every decision you make.

## When to Use

- A process just broke and you need the runbook — fast. What are the exact steps for failover?
- Calculating whether you have enough capacity (people, systems, physical space) for a projected demand increase next quarter
- Pulling the vendor SLA terms for a service that's been underperforming so you can initiate a formal review
- Building a business case for process automation by finding where manual steps create the most bottlenecks
- Preparing for an operational review meeting with executive leadership — need KPI trends, not just snapshots
- Investigating why cycle time increased on a key process and what changed in the last 60 days
- Onboarding a new operations manager who needs to understand the full process landscape

## Example Workflows

### Incident Response and Postmortem

Something went wrong and you need to contain it, then learn from it.

```
use_mcp_tool: search_knowledge query="runbook incident response procedure for payment processing failures"
use_mcp_tool: search_knowledge query="previous incidents payment processing root cause analysis postmortem"
use_mcp_tool: search_with_context query="payment processing system dependencies upstream downstream SLA obligations"
```

The first search gets you the immediate playbook. The second surfaces prior incidents so you can check whether this is a recurring pattern. The context search maps system dependencies so you understand blast radius.

### Quarterly Capacity Planning

You need to model whether current resources can handle projected Q3 volume.

```
use_mcp_tool: search_knowledge query="capacity utilization rates by team department Q1 Q2 actual vs planned"
use_mcp_tool: search_knowledge query="demand forecast projections Q3 volume transaction throughput"
use_mcp_tool: search_knowledge query="hiring plan headcount approved positions open requisitions operations"
use_mcp_tool: export_org_context
```

The org context export gives you the current organizational structure overlaid with capacity data, making it clear where you have headroom and where you're already running hot.

## Key Tools for Operations

**search_knowledge** — Your primary tool for finding SOPs, runbooks, KPI data, and process documentation. Operations data is often spread across wikis, shared drives, and ticketing systems — UPLO consolidates it into searchable structured records. Example: `"order fulfillment process cycle time SLA target vs actual last 6 months"`

**search_with_context** — Operations is all about dependencies. A process change in one area cascades through others. This tool follows those connections. Example: `"upstream dependencies for the monthly close process including data feeds handoffs and approval gates"`

**export_org_context** — Generates a snapshot of your operational structure: teams, systems, processes, and their interconnections. Use it to brief new team members or to give leadership a helicopter view of operational health.

**flag_outdated** — Stale runbooks are dangerous. If you encounter a procedure that references a decommissioned system, an old vendor, or a changed approval chain, flag it immediately. Example: flag a disaster recovery plan that still references the on-prem data center you migrated off of 18 months ago.

**propose_update** — After a process improvement, push the updated procedure back into the knowledge base. Don't let the documentation drift from reality. Example: update the customer onboarding SOP to reflect the new automated verification step.

## Tips

- Operations documents tend to use internal jargon and acronyms heavily. Search using both the acronym and the full name: `"MTTR mean time to repair"` or `"NPS net promoter score customer operations"` — this catches documents regardless of which form they used.
- When you find conflicting SOPs (two different procedures for the same process), don't just pick one. Use `flag_outdated` on the stale version AND `report_knowledge_gap` to note the conflict so the process owner can reconcile them.
- Time-series KPI data is most useful when you search with specific date ranges rather than asking for "the latest" — this lets you build trend lines and spot degradation patterns.
- After any significant operational change (new vendor, process redesign, system migration), use `log_conversation` to document the rationale and expected outcomes. This creates an audit trail that's invaluable when someone later asks "why did we change this?"
