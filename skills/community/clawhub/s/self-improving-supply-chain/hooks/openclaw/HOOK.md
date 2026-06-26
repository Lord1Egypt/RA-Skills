---
name: self-improving-supply-chain
description: "Injects supply chain self-improvement reminder during agent bootstrap"
metadata: {"openclaw":{"emoji":"📦","events":["agent:bootstrap"]}}
---

# Self-Improving Supply Chain Hook

Injects a reminder to evaluate supply chain learnings during agent bootstrap.

## What It Does

- Fires on `agent:bootstrap` (before workspace files are injected)
- Adds a supply chain-specific reminder block to check `.learnings/` for relevant entries
- Prompts the agent to log stockouts, delivery delays, supplier failures, quality rejections, forecast misses, demand signal shifts, and capacity breaches
- Reminder-only behavior: does not place orders, execute purchases, or call external payment/commerce services

## Reminder Content

The hook injects reminders to log to the appropriate file based on what occurred:

| Trigger | Target File | Category |
|---------|-------------|----------|
| Stockout or backorder event | `SUPPLY_CHAIN_ISSUES.md` | `inventory_mismatch` |
| Delivery SLA miss or delay | `SUPPLY_CHAIN_ISSUES.md` | `logistics_delay` |
| Supplier lead time increase | `LEARNINGS.md` | `supplier_risk` |
| Quality rejection or defect | `SUPPLY_CHAIN_ISSUES.md` | `quality_deviation` |
| Forecast MAPE >15% | `LEARNINGS.md` | `forecast_error` |
| Demand spike or shift | `LEARNINGS.md` | `demand_signal_shift` |
| Warehouse capacity >90% | `SUPPLY_CHAIN_ISSUES.md` | `inventory_mismatch` |

## Configuration

No configuration needed. Enable with:

```bash
openclaw hooks enable self-improving-supply-chain
```
