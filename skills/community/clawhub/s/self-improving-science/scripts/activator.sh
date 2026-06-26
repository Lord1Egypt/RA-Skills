#!/bin/bash
# Self-Improving Science Activator Hook
# Triggers on UserPromptSubmit to remind about experiment learning capture
# Keep output minimal (~60-120 tokens) to minimize overhead

set -e

cat << 'EOF'
<science-improvement-reminder>
After completing this task, evaluate if extractable research knowledge emerged:
- Data quality issue or leakage discovered?
- Statistical test assumption violated?
- Methodology flaw found in experiment design?
- Model failed to reproduce across seeds or environments?
- Hypothesis needs revision based on results?
- Training error (NaN loss, OOM, convergence failure)?

If yes: Log to .learnings/ using the self-improving-science format.
  - Data/reproducibility issues → EXPERIMENT_ISSUES.md
  - Methodology/statistical insights → LEARNINGS.md
  - Missing ML tooling → FEATURE_REQUESTS.md

If high-value (recurring, broadly applicable): Promote to experiment checklist, model card, or methodology standard.
</science-improvement-reminder>
EOF
