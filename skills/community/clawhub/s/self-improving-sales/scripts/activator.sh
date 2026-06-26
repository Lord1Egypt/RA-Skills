#!/bin/bash
# Sales Self-Improvement Activator Hook
# Triggers on UserPromptSubmit to remind about sales-specific learning capture
# Keep output minimal (~50-100 tokens) to minimize overhead

set -e

cat << 'EOF'
<sales-self-improvement-reminder>
After completing this sales task, evaluate if extractable knowledge emerged:
- Deal stuck or slipping past stage threshold? → DEAL_ISSUES.md (pipeline_leak)
- Objection you couldn't handle or heard before? → LEARNINGS.md (objection_pattern)
- Pricing mistake or unapproved discount? → DEAL_ISSUES.md (pricing_error)
- Forecast miss or deal push? → DEAL_ISSUES.md (forecast_miss)
- Lost deal to competitor or new competitive intel? → LEARNINGS.md (competitor_shift)
- Deal taking longer than expected to close? → LEARNINGS.md (deal_velocity_drop)

If recurring pattern (3+ deals): promote to battle card, objection script, or pricing playbook.
If broadly applicable: consider skill extraction (MEDDIC checklist, competitive framework).
</sales-self-improvement-reminder>
EOF
