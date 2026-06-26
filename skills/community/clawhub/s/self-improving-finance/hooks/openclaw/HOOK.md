---
name: self-improving-finance
description: "Injects finance self-improvement reminder during agent bootstrap"
metadata: {"openclaw":{"emoji":"💰","events":["agent:bootstrap"]}}
---

# Self-Improving Finance Hook

Injects a reminder to evaluate finance learnings during agent bootstrap.

## What It Does

- Fires on `agent:bootstrap` (before workspace files are injected)
- Adds a finance-specific reminder block to check `.learnings/` for relevant entries
- Prompts the agent to log reconciliation errors, control weaknesses, forecast variances, regulatory gaps, valuation errors, and cash flow anomalies
- Emphasizes data anonymization: never log real account numbers, bank details, or client-identifying financial data

## Reminder Content

The hook injects reminders to log to the appropriate file based on what occurred:

| Trigger | Target File | Category |
|---------|-------------|----------|
| Reconciliation break identified | `FINANCE_ISSUES.md` | reconciliation trigger |
| SOX control test failure | `FINANCE_ISSUES.md` | control_test trigger |
| Budget vs. actual variance >10% | `FINANCE_ISSUES.md` | variance_analysis trigger |
| Late close item | `FINANCE_ISSUES.md` | close_review trigger |
| Intercompany imbalance | `FINANCE_ISSUES.md` | reconciliation trigger |
| Unusual JE flagged | `FINANCE_ISSUES.md` | audit trigger |
| AR aging >90 days | `FINANCE_ISSUES.md` | aging_review trigger |
| Control weakness discovered | `LEARNINGS.md` | `control_weakness` |
| Regulatory gap found | `LEARNINGS.md` | `regulatory_gap` |
| Valuation error identified | `LEARNINGS.md` | `valuation_error` |
| Cash flow anomaly detected | `LEARNINGS.md` | `cash_flow_anomaly` |
| Forecast improvement found | `LEARNINGS.md` | `forecast_variance` |

## Configuration

No configuration needed. Enable with:

```bash
openclaw hooks enable self-improving-finance
```
