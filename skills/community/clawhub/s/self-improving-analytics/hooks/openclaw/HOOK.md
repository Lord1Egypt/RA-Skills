---
name: self-improving-analytics
description: "Injects analytics self-improvement reminder during agent bootstrap"
metadata: {"openclaw":{"emoji":"📊","events":["agent:bootstrap"]}}
---

# Self-Improving Analytics Hook

Injects a reminder to evaluate analytics learnings during agent bootstrap.

## What It Does

- Fires on `agent:bootstrap` (before workspace files are injected)
- Adds an analytics-specific reminder block to check `.learnings/` for relevant entries
- Prompts the agent to log data quality issues, metric drift, pipeline failures, visualization problems, definition mismatches, and freshness breaches

## Reminder Content

The hook injects reminders to log to the appropriate file based on what occurred:

| Trigger | Target File | Category |
|---------|-------------|----------|
| ETL/ELT job failure | `DATA_ISSUES.md` | pipeline_failure |
| Data freshness SLA breach | `DATA_ISSUES.md` | freshness_issue |
| Metric value anomaly | `DATA_ISSUES.md` | metric_drift |
| NULL rate spike in column | `DATA_ISSUES.md` | data_quality |
| Schema change in source | `DATA_ISSUES.md` | data_quality |
| Conflicting metric definitions | `LEARNINGS.md` | definition_mismatch |
| Visualization misleading | `LEARNINGS.md` | visualization_mislead |
| Dashboard rendering error | `DATA_ISSUES.md` | rendering_error |

## Configuration

No configuration needed. Enable with:

```bash
openclaw hooks enable self-improving-analytics
```
