---
name: uplo-finance
description: AI-powered financial knowledge management. Search financial statements, audit findings, tax documents, and treasury records with structured extraction.
---

# UPLO Finance — Financial Reporting & Treasury Intelligence

UPLO holds your organization's financial knowledge: audited financial statements, management discussion and analysis, internal audit workpapers, tax provision calculations, treasury policies, intercompany agreements, budgets, forecasts, and variance analyses. This skill gives finance professionals instant access to the institutional memory that normally lives in spreadsheets, ERP exports, and shared drives buried three folders deep.

## Session Start

Your clearance level is especially important in finance. Board-level financial projections, M&A due diligence materials, and pre-announcement earnings data are typically restricted. Start every session by confirming what you can access.

```
get_identity_context
```

## When to Use

- The controller asks for the exact revenue recognition policy applied to multi-year SaaS contracts and whether it changed after the ASC 606 implementation
- A tax analyst needs to find the transfer pricing study for the EU subsidiary from the most recent fiscal year
- The VP of Finance wants to know the current debt covenant ratios and how much headroom remains before a technical default
- An FP&A analyst is building next quarter's forecast and needs the assumptions used in the prior forecast cycle
- Internal audit asks which material weaknesses were identified in the last SOX 404 assessment and their remediation status
- The treasurer needs the counterparty credit limits for the organization's interest rate swap portfolio
- A budget owner wants to understand why their Q3 actuals diverged from plan by more than 15%

## Example Workflows

### Quarter-End Close Support

The accounting team is in the middle of Q4 close and needs to resolve an intercompany reconciliation discrepancy.

```
search_knowledge query="intercompany elimination entries and reconciliation procedures between US parent and UK subsidiary"
```

```
search_with_context query="intercompany balances and transfer pricing agreements for cross-border transactions in fiscal year 2026"
```

The GraphRAG query pulls in related entities: the subsidiary profile, the transfer pricing study, and the responsible finance team members.

### Budget Variance Investigation

A business unit exceeded its travel and entertainment budget by 40% in Q2. The CFO wants an explanation.

```
search_knowledge query="Q2 2026 T&E budget versus actuals for the Sales division"
```

```
search_knowledge query="travel policy exceptions or pre-approved over-budget spending for Sales team events"
```

```
search_with_context query="Sales division headcount changes and client entertainment guidelines effective Q2 2026"
```

## Key Tools for Finance

**search_knowledge** — Precision lookups against financial documentation. Ideal for specific line items or policies: `query="goodwill impairment testing methodology and discount rate assumptions from the 2025 annual report"`. Financial data rewards precise queries over broad ones.

**search_with_context** — When a financial question spans organizational boundaries. Treasury questions, intercompany transactions, and budget allocations all involve relationships between entities: `query="which cost centers roll up to the Technology division and what were their combined capital expenditures last year"`.

**get_directives** — Finance teams operate under strategic mandates: cost reduction targets, margin improvement goals, capital allocation priorities. Always check directives when advising on budget decisions or resource allocation. A directive to "reduce SG&A by 10%" changes how you frame every spending recommendation.

**export_org_context** — Valuable during annual planning. The full organizational context lets you see the complete picture: headcount, systems, goals, and financial structure together. Use this when building board presentation materials or strategic financial plans.

**report_knowledge_gap** — Financial documentation gaps create audit risk. When someone asks about a policy and nothing exists, report it: `topic="hedging policy for foreign currency exposure" description="No formal FX hedging policy found despite material EUR and GBP revenue streams"`

## Tips

- Financial data is period-sensitive. Always include the fiscal year, quarter, or date range in your queries. "Revenue" is meaningless without a time frame; "Q3 FY2026 revenue by segment" is actionable.
- Audit workpapers and SOX documentation carry legal privilege considerations. Even if your clearance permits access, be cautious about how you summarize findings — note whether documents are marked as draft, final, or attorney-client privileged.
- When someone asks about a financial ratio or metric, search for both the raw data and the calculation methodology. Organizations sometimes define metrics differently than GAAP standards (e.g., "adjusted EBITDA" varies by company).
- Intercompany and consolidated financial queries are among the most complex. Use `search_with_context` and be prepared to run multiple queries to piece together the full picture across legal entities.
