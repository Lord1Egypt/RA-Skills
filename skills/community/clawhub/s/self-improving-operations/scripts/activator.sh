#!/bin/bash
# Operations Self-Improvement Activator Hook
# Triggers on UserPromptSubmit to remind about operations-specific learning capture
# Keep output minimal (~50-100 tokens) to minimize overhead

set -e

cat << 'EOF'
<operations-self-improvement-reminder>
After completing this operations task, evaluate if extractable knowledge emerged:
- Incident repeated or MTTR exceeded target? → OPERATIONS_ISSUES.md [OPS-YYYYMMDD-XXX]
- SLO/SLA breach or capacity threshold hit? → OPERATIONS_ISSUES.md
- Process bottleneck slowing deployments? → LEARNINGS.md (process_bottleneck)
- Manual step that should be automated? → LEARNINGS.md (automation_gap)
- Alert fatigue or noisy monitoring? → LEARNINGS.md (monitoring)
- Toil consuming >50% of on-call time? → LEARNINGS.md (toil_accumulation)

If recurring pattern (3+ occurrences): promote to runbook or SLO definition.
If broadly applicable: consider skill extraction.
</operations-self-improvement-reminder>
EOF
