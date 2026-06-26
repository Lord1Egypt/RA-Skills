#!/bin/bash
# Engineering Self-Improvement Activator Hook
# Triggers on UserPromptSubmit to remind about engineering learning capture
# Keep output minimal (~50-100 tokens) to minimize overhead

set -e

cat << 'EOF'
<engineering-self-improvement-reminder>
After completing this task, evaluate if engineering knowledge emerged:
- Architecture decision or violation discovered?
- Build or deploy failure with non-obvious root cause?
- Test gap, flaky test, or missing integration coverage?
- Performance regression (N+1 query, memory leak, slow endpoint)?
- Dependency vulnerability or breaking change encountered?
- Design flaw surfaced during implementation or review?

If yes: Log to .learnings/ using the self-improving-engineering skill format.
If recurring (3+ times): Promote to ADR, coding standard, or CI/CD runbook.
</engineering-self-improvement-reminder>
EOF
