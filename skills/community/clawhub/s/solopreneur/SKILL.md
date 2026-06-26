---
name: solopreneur
description: Solo business management with dashboard, pipeline tracking, invoicing, and weekly reviews. Use when user mentions solo business, clients, revenue, pipeline, invoices, or priorities. Produces business dashboard, tracks prospects from lead to close, drafts invoices, prioritizes actions, and runs weekly business reviews. All business data stays private and local.
---

# Solopreneur

Solo business system. Run like a company of one.

## Critical Privacy & Safety

### Data Storage (CRITICAL)
- **All business data stored locally only**: `memory/solopreneur/`
- **Client information protected** - no external sharing
- **No cloud accounting** integration
- **No payment processing** through this skill
- User controls all data retention and deletion

### Safety Boundaries
- ✅ Track business dashboard and metrics
- ✅ Manage pipeline and prospects
- ✅ Draft invoices and track payments
- ✅ Prioritize work and run weekly reviews
- ❌ **NEVER process payments**
- ❌ **NEVER file taxes**
- ❌ **NEVER replace** accountant or legal counsel

### Data Structure
Business data stored locally:
- `memory/solopreneur/dashboard.json` - Business metrics dashboard
- `memory/solopreneur/clients.json` - Client list and details
- `memory/solopreneur/pipeline.json` - Sales pipeline tracking
- `memory/solopreneur/invoices.json` - Invoice records
- `memory/solopreneur/reviews.json` - Weekly review history
- `memory/solopreneur/priorities.json` - Current priorities

## Core Workflows

### Check Dashboard
```
User: "How's my business doing?"
→ Use scripts/dashboard.py
→ Show clients, revenue YTD, pipeline, invoices outstanding, top priorities
```

### Track Pipeline
```
User: "Add new prospect to pipeline"
→ Use scripts/add_prospect.py --name "Acme Corp" --value 15000 --stage "proposal"
→ Track from lead through closed, alert if going cold
```

### Draft Invoice
```
User: "Draft invoice for the website project"
→ Use scripts/draft_invoice.py --client "XYZ Inc" --project "website" --amount 5000
→ Generate complete invoice with services, terms, due date
```

### Prioritize Work
```
User: "What should I focus on today?"
→ Use scripts/prioritize.py --time 4 --energy high
→ Review full situation, produce prioritized action list with time estimates
```

### Weekly Review
```
User: "Run my weekly business review"
→ Use scripts/weekly_review.py
→ Review revenue, pipeline, delivery, set top 3 priorities for next week
```

## Module Reference
- **Business Dashboard**: See [references/dashboard.md](references/dashboard.md)
- **Pipeline Management**: See [references/pipeline.md](references/pipeline.md)
- **Invoicing**: See [references/invoicing.md](references/invoicing.md)
- **Priority Setting**: See [references/priorities.md](references/priorities.md)
- **Weekly Reviews**: See [references/weekly-reviews.md](references/weekly-reviews.md)
- **Client Management**: See [references/clients.md](references/clients.md)

## Scripts Reference
| Script | Purpose |
|--------|---------|
| `dashboard.py` | Show business dashboard |
| `add_prospect.py` | Add prospect to pipeline |
| `draft_invoice.py` | Draft client invoice |
| `prioritize.py` | Prioritize daily work |
| `weekly_review.py` | Run weekly business review |
| `log_revenue.py` | Log revenue entry |
| `track_payment.py` | Track invoice payment |
| `set_goal.py` | Set business goals |
