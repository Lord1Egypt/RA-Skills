#!/bin/bash
# Analytics Self-Improvement Activator Hook
# Triggers on UserPromptSubmit to remind about analytics-specific learning capture
# Keep output minimal (~50-100 tokens) to minimize overhead

set -e

cat << 'EOF'
<analytics-self-improvement-reminder>
After completing this analytics task, evaluate if extractable knowledge emerged:
- Pipeline failure with non-obvious root cause? → DATA_ISSUES.md [DAT-YYYYMMDD-XXX]
- Data freshness SLA breached? → DATA_ISSUES.md (freshness_issue)
- Metric value anomaly or drift detected? → LEARNINGS.md (metric_drift)
- NULL rate spike or data quality degradation? → DATA_ISSUES.md (data_quality)
- Conflicting metric definitions across teams? → LEARNINGS.md (definition_mismatch)
- Misleading visualization discovered? → LEARNINGS.md (visualization_mislead)
- Schema change broke downstream? → DATA_ISSUES.md (schema_drift)

If recurring pattern (3+ occurrences): promote to data dictionary or pipeline runbook.
If broadly applicable: consider skill extraction.
</analytics-self-improvement-reminder>
EOF
