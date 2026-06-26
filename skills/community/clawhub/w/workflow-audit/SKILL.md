---
name: workflow-audit
description: Conduct a structured operational audit — identify friction points, map workflows, quantify waste, and produce a priority-ranked automation blueprint with ROI projections. Use when a client shares meeting transcripts, process descriptions, or operational pain points.
version: 1.0.0
author: dynoclaw
user-invocable: true
metadata: {"openclaw":{"emoji":"🔍"}}
---

# Workflow Audit — The Friction X-Ray

Transform client conversations into a structured automation blueprint with hard ROI numbers. This is the deliverable for a diagnostic engagement.

## When to Use

- Client shares a meeting transcript describing their operations
- Client describes manual processes, spreadsheet workflows, or tool-switching pain
- You're conducting a discovery call and need structured output
- Pre-sales: building the business case for a DynoClaw deployment

## Input

The user provides one or more of:
- Meeting transcript (Fathom, Otter, pasted text)
- Description of current workflows and pain points
- List of tools/systems in use
- Team size and roles involved

If insufficient context, ask targeted discovery questions:
1. "What's the ugliest spreadsheet your team updates every week?"
2. "Where is your team copy-pasting data between two screens?"
3. "What breaks when a key person goes on vacation?"
4. "If you got 50 new clients tomorrow, which department collapses first?"
5. "What does your team do on Saturday mornings that should've been done Friday?"

## Processing Steps

### Step 1 — Map the Current State

For each workflow mentioned, document:
- **Process name** (e.g., "Weekly Executive Report", "Invoice Reconciliation")
- **Trigger** — what starts this process
- **Steps** — numbered sequence of actions
- **People involved** — roles, not just names
- **Tools used** — every system touched (CRM, spreadsheet, email, ERP, etc.)
- **Frequency** — how often this runs
- **Time spent** — estimated hours per occurrence
- **Error rate** — how often it goes wrong and what the consequences are

### Step 2 — Score Each Workflow (Friction Matrix)

Rate each workflow on two dimensions:

**Volume** (1-10): How often does this run?
- 1-3: Monthly or less
- 4-6: Weekly
- 7-10: Daily or continuous

**Cost of Error** (1-10): What happens when it breaks?
- 1-3: Minor inconvenience, easy to fix
- 4-6: Delayed deliverables, client impact
- 7-10: Financial loss, compliance risk, customer churn

**Friction Score** = Volume x Cost of Error (max 100)

| Score | Category | Recommendation |
|-------|----------|----------------|
| 70-100 | High Volume, High Cost | Automate immediately — highest ROI |
| 40-69 | Medium | Strong automation candidate |
| 15-39 | Low-Medium | Automate after high-priority items |
| 1-14 | Low | Leave manual or defer indefinitely |

### Step 3 — Quantify the Waste

For each high-scoring workflow, calculate:
- **Hours/week wasted** = (time per occurrence) x (frequency)
- **Annual cost** = hours/week x 50 weeks x (blended hourly rate, default $45/hr for ops staff, $75/hr for senior staff)
- **Error cost** = (error rate) x (cost per error) x (annual occurrences)
- **Total annual waste** = labor cost + error cost

### Step 4 — Design the Automation

For each workflow scoring 40+, propose:
- **Automation approach** — which DynoClaw plugins/skills handle this
- **Data connections** — what APIs or integrations are needed
- **Human checkpoints** — where the human approves vs. where the agent acts autonomously
- **Failover plan** — what happens when the AI encounters an edge case it can't handle
- **Implementation time** — estimated hours to build and test

### Step 5 — Build the ROI Model

Create a summary table:

| Workflow | Annual Waste | Automation Cost | Annual Savings | ROI | Payback |
|----------|-------------|-----------------|----------------|-----|---------|
| Process A | $X | $Y (one-time) + $Z/mo | $W | W/Y % | N months |

**Total across all workflows:**
- Total annual waste identified
- Total automation investment (one-time + annual)
- Net annual savings
- Payback period
- 3-year cumulative savings

### Step 6 — Produce the Blueprint

Format the final output as:

```
# Operational Automation Blueprint
**Prepared for:** [Client Name]
**Date:** [Date]
**Prepared by:** ParallelScore / DynoClaw

---

## Executive Summary
[2-3 sentences: We identified X workflows consuming Y hours/week at a cost of $Z/year. We recommend automating the top N workflows, yielding $W/year in savings with a payback period of M months.]

---

## Current State Assessment
[Workflow maps from Step 1]

## Friction Matrix
[Scored table from Step 2]

## Waste Quantification
[Dollar figures from Step 3]

## Recommended Automations
[Designs from Step 4, ordered by Friction Score descending]

## Investment & ROI Summary
[Table from Step 5]

## Implementation Roadmap
| Phase | Workflows | Timeline | Investment |
|-------|-----------|----------|------------|
| Phase 1 (Quick Wins) | Top 1-2 by score | Weeks 1-2 | $X |
| Phase 2 (Core Ops) | Next 2-3 | Weeks 3-6 | $Y |
| Phase 3 (Expansion) | Remaining | Month 2-3 | $Z |

## What We Need From You
- [List of accounts, access, contacts needed]

## Next Step
Reply with "Go" to begin Phase 1, or schedule a call to discuss.
```

## Guidelines

- Always quantify in dollars, not just hours — executives respond to money
- Use conservative estimates — underpromise on savings so reality exceeds projections
- Default labor rates: $45/hr ops staff, $75/hr senior staff, $150/hr executive time
- If the client hasn't shared enough detail, ask the discovery questions — don't guess
- The blueprint should be client-ready — professional enough to present to a CFO
- Frame automation as "freeing your team for strategic work" not "replacing your team"
- Always include human checkpoints — never propose fully autonomous workflows for the first engagement
- Include a "What happens if you do nothing" section showing compounding cost of inaction
