#!/bin/bash
# Coding Self-Improvement Activator Hook
# Triggers on UserPromptSubmit to remind about coding-specific learning capture
# Keep output minimal (~50-100 tokens) to minimize overhead

set -e

cat << 'EOF'
<coding-self-improvement-reminder>
After completing this coding task, evaluate if extractable knowledge emerged:
- Lint error or type mismatch required investigation? → BUG_PATTERNS.md
- Runtime exception with non-obvious root cause? → BUG_PATTERNS.md
- Anti-pattern or code smell discovered? → LEARNINGS.md (anti_pattern)
- Better language idiom found? → LEARNINGS.md (idiom_gap)
- Debugging breakthrough? → LEARNINGS.md (debugging_insight)
- Tooling issue blocked progress? → LEARNINGS.md (tooling_issue)

If recurring pattern (3+ occurrences): promote to lint rule or style guide.
If broadly applicable: consider skill extraction.
</coding-self-improvement-reminder>
EOF
