#!/bin/bash
# Support Self-Improvement Activator Hook
# Triggers on UserPromptSubmit to remind about support-specific learning capture
# Keep output minimal (~50-100 tokens) to minimize overhead

set -e

cat << 'EOF'
<support-self-improvement-reminder>
After completing this support task, evaluate if extractable knowledge emerged:
- Ticket took longer than SLA target? → TICKET_ISSUES.md (sla_breach)
- Initial diagnosis turned out wrong? → TICKET_ISSUES.md (misdiagnosis)
- Customer reopened a resolved ticket? → TICKET_ISSUES.md (ticket_reopen)
- Same issue from multiple customers? → TICKET_ISSUES.md (repeat_ticket)
- KB search found no relevant article? → LEARNINGS.md (knowledge_gap)
- Escalation went to wrong team? → LEARNINGS.md (escalation_gap)
- Customer expressed churn intent? → LEARNINGS.md (customer_churn_signal)

If recurring pattern (3+ occurrences): promote to KB article or escalation rule.
If broadly applicable: consider skill extraction.
</support-self-improvement-reminder>
EOF
