#!/bin/bash
# HR Self-Improvement Activator Hook
# Triggers on UserPromptSubmit to remind about HR-specific learning capture
# Keep output minimal (~50-100 tokens) to minimize overhead

set -e

cat << 'EOF'
<hr-self-improvement-reminder>
After completing this HR task, evaluate if extractable knowledge emerged:
- Compliance finding or regulatory risk? → HR_PROCESS_ISSUES.md [HRP-YYYYMMDD-XXX]
- Policy gap or outdated handbook section? → LEARNINGS.md (policy_gap)
- Candidate experience issue or pipeline drop-off? → LEARNINGS.md (candidate_experience)
- New hire friction or onboarding delay? → LEARNINGS.md (onboarding_friction)
- Retention signal or exit interview theme? → LEARNINGS.md (retention_signal)
- Benefits or payroll process error? → HR_PROCESS_ISSUES.md (process_inefficiency)

NEVER log PII (names, SSNs, salaries, medical info). Always anonymize.
If recurring pattern (3+ occurrences): promote to policy doc or compliance calendar.
</hr-self-improvement-reminder>
EOF
