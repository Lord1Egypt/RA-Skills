#!/bin/bash
# Business Self-Improvement Activator Hook
# Reminder-only output for UserPromptSubmit

set -e

cat << 'EOF'
<business-improvement-reminder>
After completing this task, evaluate if business administration findings should be captured:
- Missed SLA or delayed execution milestone?
- Overdue approval or decision gate bottleneck?
- RACI conflict or ownership ambiguity?
- KPI definition mismatch or unexplained variance?
- Budget overrun warning without mitigation owner?
- Vendor handoff failure or dependency blocked?
- Missing policy, documentation drift, or audit issue?

Reminder-only safety:
- This workflow does NOT execute approvals, spending, vendor commitments, payroll, or legal actions.
- Recommend explicit human approval for high-impact business decisions.

If yes: log to .learnings/
- Reusable learning -> LEARNINGS.md [LRN-YYYYMMDD-XXX]
- Active business issue -> BUSINESS_ISSUES.md [BUS-YYYYMMDD-XXX]
- Requested capability -> FEATURE_REQUESTS.md [FEAT-YYYYMMDD-XXX]
</business-improvement-reminder>
EOF
