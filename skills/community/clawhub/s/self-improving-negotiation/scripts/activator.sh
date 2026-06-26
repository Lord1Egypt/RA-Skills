#!/bin/bash
# Negotiation Self-Improvement Activator Hook
# Triggers on UserPromptSubmit to remind about negotiation learning capture.
# Reminder-only output.

set -e

cat << 'EOF'
<negotiation-self-improvement-reminder>
After completing this negotiation task, check if extractable knowledge emerged:
- Deadlock or repeated no-movement rounds? -> NEGOTIATION_ISSUES.md (framing_miss/escalation_misalignment)
- Concession made without reciprocal value? -> NEGOTIATION_ISSUES.md (concession_leak)
- BATNA unclear or missing? -> NEGOTIATION_ISSUES.md (batna_weakness)
- Objection handled poorly or recurring? -> LEARNINGS.md (objection_handling_gap)
- Anchor failed or drifted? -> LEARNINGS.md (anchor_error)
- Term ambiguity or unresolved redline? -> NEGOTIATION_ISSUES.md (agreement_risk)
- Need tooling/process support? -> FEATURE_REQUESTS.md (FEAT)

If pattern repeats 3+ times, promote to playbook, objection library, concession guardrail, BATNA checklist, or deal review template.
Safety: reminder-only. Never auto-accept terms, commit pricing, execute approvals, or finalize agreements.
</negotiation-self-improvement-reminder>
EOF
