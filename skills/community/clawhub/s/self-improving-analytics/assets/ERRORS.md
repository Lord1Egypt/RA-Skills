# Data Issues Log

Pipeline failures, data quality problems, metric anomalies, visualization errors, and schema drift captured during analytics work.

**Triggers**: etl_failure | freshness_breach | metric_anomaly | null_spike | schema_drift | definition_conflict | rendering_error
**Areas**: ingestion | transformation | modeling | reporting | visualization | governance | data_catalog

## Status Definitions

| Status | Meaning |
|--------|---------|
| `pending` | Not yet addressed |
| `in_progress` | Actively being investigated |
| `resolved` | Issue fixed, root cause documented |
| `wont_fix` | Decided not to address (reason in Resolution) |
| `promoted` | Elevated to pipeline runbook, data dictionary, or dashboard standard |
| `promoted_to_skill` | Extracted as a reusable skill |

---
