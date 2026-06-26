#!/bin/bash
# Finance Self-Improvement Activator Hook
# Triggers on UserPromptSubmit to remind about finance-specific learning capture
# Keep output minimal (~50-100 tokens) to minimize overhead

set -e

cat << 'EOF'
<finance-self-improvement-reminder>
After completing this finance task, evaluate if extractable knowledge emerged:
- Reconciliation break requiring investigation? → FINANCE_ISSUES.md [FIN-YYYYMMDD-XXX]
- SOX control test failure or gap? → FINANCE_ISSUES.md (control_test trigger)
- Budget vs. actual variance >10%? → FINANCE_ISSUES.md (variance_analysis)
- Late close item or deadline miss? → FINANCE_ISSUES.md (close_review)
- Intercompany imbalance or JE anomaly? → FINANCE_ISSUES.md (reconciliation/audit)
- Control weakness or regulatory gap? → LEARNINGS.md (control_weakness / regulatory_gap)

ALWAYS ANONYMIZE: No real account numbers, bank details, client names, or specific figures.
If recurring pattern (3+ periods/entities): promote to close checklist or control matrix.
</finance-self-improvement-reminder>
EOF
