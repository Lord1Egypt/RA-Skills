---
name: uplo-customer-360
description: AI-powered customer lifecycle intelligence spanning sales, customer success, and retail. Unified search across pipeline data, account health, and customer analytics.
---

# UPLO Customer 360 — Full Lifecycle Revenue Intelligence

Your CRM holds pipeline stages. Your CS platform holds health scores. Your retail system holds transaction history. None of them talk to each other well enough to answer the question that actually matters: "What is the complete picture for this customer?" UPLO Customer 360 stitches together sales engagement history, onboarding records, support escalations, renewal signals, NPS feedback, and retail analytics into a unified knowledge layer that any revenue team member can query naturally.

## Session Start

Load your identity to establish your revenue role — AE, CSM, solutions engineer, retail operations, etc. — and the accounts you are assigned to:

```
get_identity_context
```

Pull current directives. In revenue organizations, these include quarterly targets, discount authority limits, churn reduction mandates, and promotional campaign rules:

```
get_directives
```

## Example Workflows

### Pre-Renewal Account Review

A CSM has a $480K renewal coming up in 45 days. They need the full account story before the executive business review.

```
search_with_context query="Meridian Industries account health product adoption support tickets last 6 months"
```

Check whether there were any escalations or executive complaints:

```
search_knowledge query="Meridian Industries escalation executive sponsor feedback"
```

Pull the original sales notes to understand what was promised during the initial deal:

```
search_knowledge query="Meridian Industries initial sales proposal value propositions committed deliverables"
```

Review any retail or usage analytics data:

```
search_with_context query="Meridian Industries product usage metrics feature adoption monthly active users"
```

```
log_conversation summary="Pre-renewal 360 review for Meridian Industries; compiled health metrics, escalation history, original commitments, and usage data for EBR prep" topics='["renewal","account-review","Meridian-Industries"]' tools_used='["search_with_context","search_knowledge"]'
```

### Churn Signal Investigation

The weekly health score report shows three enterprise accounts dropping below threshold simultaneously. The VP of Customer Success wants to understand if there is a common root cause.

```
search_with_context query="enterprise accounts health score decline reasons product issues Q1"
```

```
search_knowledge query="product reliability incidents outages impact customer-facing last 60 days"
```

Check if there is a directive about the product issue or a remediation plan:

```
get_directives
```

## When to Use

- Preparing for an executive business review and need the complete account history across sales, onboarding, support, and product usage
- A prospect references a competitor in a late-stage deal and you need to find how previous win/loss analyses characterized that competitor's strengths
- Investigating why a cohort of accounts is churning and whether the root cause is product, service, or pricing
- Onboarding a new AE to a territory and they need context on every strategic account including past proposals, key contacts, and competitive dynamics
- Retail operations wants to understand how online engagement correlates with in-store purchase patterns for a loyalty segment
- Building a QBR deck and need to pull NPS trends, ticket volume, and expansion revenue by account tier
- Customer success wants to identify accounts where product adoption is low despite high contract value — the "silent churn risk" pattern

## Key Tools for Customer Lifecycle

**search_with_context** — Revenue questions almost always need organizational context. "Why is this account at risk?" requires connecting support tickets, product usage data, CSM notes, and sales history. Graph traversal does this automatically. Example: `search_with_context query="Acme Corp account risk factors renewal September"`

**search_knowledge** — Fast lookup for specific customer artifacts: proposals, SOWs, meeting notes, QBR decks. Example: `search_knowledge query="Acme Corp Q3 QBR deck expansion discussion"`

**get_directives** — Revenue directives change quarterly. Discount floors, target account lists, promotional pricing, and strategic account designations all live here.

**export_org_context** — Maps the revenue organization: sales territories, CSM assignments, leadership hierarchy, key systems (CRM, CS platform, analytics tools). Useful when a customer asks "who else at your company should I be talking to?"

**report_knowledge_gap** — When you discover an account with no CSM notes, no QBR records, or missing onboarding documentation, flag it. Silent accounts are churn risks, and the gap report creates visibility.

**flag_outdated** — Pricing sheets, competitive battle cards, and product capability matrices go stale quickly. Flag outdated versions so the revenue enablement team can refresh them.

## Tips

- Account names in CRM and in ingested documents may not match exactly (abbreviations, legal entity names vs. common names). Try both the common name and the legal entity name when searching.
- Combine sales and CS queries intentionally. A CSM asking about "renewal risk" and an AE asking about "expansion opportunity" on the same account should both use `search_with_context` to get the full picture, not just their domain slice.
- NPS and CSAT scores are extracted as structured fields. You can search by score ranges in some cases: "NPS detractor accounts enterprise tier."
- Quarterly business review preparation is the single highest-value use case. Run it at least a week before the meeting so you have time to fill any gaps that `report_knowledge_gap` surfaces.
