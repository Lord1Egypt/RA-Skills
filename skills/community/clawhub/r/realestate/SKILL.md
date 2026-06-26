---
name: realestate
description: Real estate transaction support with affordability analysis, property evaluation, and offer strategy. Use when user mentions buying a home, selling property, house hunting, mortgages, inspections, or rental agreements. Calculates true affordability, evaluates properties systematically, builds offer strategies, reviews contracts, and tracks transaction milestones. NEVER provides investment advice.
---

# Real Estate

Real estate navigation system. Buy smart, sell smart.

## Critical Privacy & Safety

### Data Storage (CRITICAL)
- **All real estate data stored locally only**: `memory/realestate/`
- **No MLS access** or listing services
- **No mortgage lender connections**
- **No document submission** through this skill
- User controls all data retention and deletion

### Safety Boundaries
- ✅ Calculate true affordability including all costs
- ✅ Evaluate properties systematically
- ✅ Build evidence-based offer strategies
- ✅ Review lease agreements
- ❌ **NEVER provide investment advice**
- ❌ **NEVER guarantee** property values
- ❌ **NEVER replace** licensed real estate agents
- ❌ **NEVER replace** real estate attorneys

### Important Note
Real estate transactions are legally complex and high-stakes. This skill provides educational support only. Always work with licensed real estate agents, mortgage professionals, and attorneys as appropriate for your jurisdiction.

### Data Structure
Real estate data stored locally:
- `memory/realestate/affordability.json` - Affordability calculations
- `memory/realestate/properties.json` - Property evaluations
- `memory/realestate/offers.json` - Offer strategies and history
- `memory/realestate/inspections.json` - Inspection findings
- `memory/realestate/contracts.json` - Contract review notes
- `memory/realestate/transactions.json` - Transaction tracking

## Core Workflows

### Calculate Affordability
```
User: "What can I actually afford?"
→ Use scripts/calculate_affordability.py --income 120000 --debts 800 --downpayment 60000
→ Calculate true monthly cost including taxes, insurance, maintenance
```

### Evaluate Property
```
User: "Evaluate this house at 123 Main St"
→ Use scripts/evaluate_property.py --address "123 Main St" --price 650000
→ Generate systematic evaluation checklist
```

### Build Offer Strategy
```
User: "Help me make an offer on the house I saw"
→ Use scripts/build_offer.py --property "PROP-123" --comps "COMP-1,COMP-2"
→ Analyze comparables, determine offer range, plan contingencies
```

### Prepare for Inspection
```
User: "What should I look for during inspection?"
→ Use scripts/prep_inspection.py --property-type "single-family" --year 1985
→ Generate inspection checklist by property type and age
```

### Review Lease
```
User: "Review this lease agreement"
→ Use scripts/review_lease.py --file "lease.pdf"
→ Identify unusual clauses, flag potential issues
```

## Module Reference
- **Affordability Analysis**: See [references/affordability.md](references/affordability.md)
- **Property Evaluation**: See [references/evaluation.md](references/evaluation.md)
- **Offer Strategy**: See [references/offers.md](references/offers.md)
- **Inspection Guide**: See [references/inspection.md](references/inspection.md)
- **Selling Strategy**: See [references/selling.md](references/selling.md)
- **Lease Review**: See [references/leases.md](references/leases.md)
- **Closing Process**: See [references/closing.md](references/closing.md)

## Scripts Reference
| Script | Purpose |
|--------|---------|
| `calculate_affordability.py` | Calculate true affordability |
| `evaluate_property.py` | Systematic property evaluation |
| `build_offer.py` | Build offer strategy |
| `prep_inspection.py` | Prepare for inspection |
| `review_lease.py` | Review lease agreements |
| `track_transaction.py` | Track transaction milestones |
| `compare_properties.py` | Compare multiple properties |
| `analyze_market.py` | Analyze local market data |
