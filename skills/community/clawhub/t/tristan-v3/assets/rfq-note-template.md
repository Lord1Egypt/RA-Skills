---
rfq_id: "{{rfq_id}}"
status: intake
client: "{{client}}"
contact_name: "{{contact_name}}"
contact_email: "{{contact_email}}"
source: "{{source}}"
due_date: "{{due_date}}"
value_estimate: 0
created: "{{created_date}}"
last_updated: "{{created_date}}"
---

# RFQ {{rfq_id}} — {{client}}

## Summary
[NEEDS INPUT: one or two lines describing what is being quoted]

## Line Items

| Item | Qty | Unit | Target Unit Cost | Notes |
|---|---|---|---|---|
|  |  |  |  |  |

## Pricing
_Populated by `scripts/pricing_model.py`. This is the cost-plus baseline — the cost floor every other pricing method is compared against._

- Subtotal: [NEEDS INPUT]
- Margin applied: [NEEDS INPUT]
- Total quote value: [NEEDS INPUT]

## Pricing Strategy Comparison
_Populated by `scripts/pricing_strategies.py report`. Optional — use for competitive, value-based, target-costing, escalation, or TCO comparisons. Long-term/capital RFQs should include escalation and/or TCO._

[NEEDS INPUT: run `pricing_strategies.py report` with the appropriate strategy]

## Supplier Quotes
_Populated by `scripts/compare_quotes.py`._

| Supplier | Quoted Price | Lead Time | Cert Status | Rank |
|---|---|---|---|---|
|  |  |  |  |  |

## Timeline

- Received: {{created_date}}
- Due: {{due_date}}

## Status Log

- {{created_date}} — Intake created via {{source}}.
