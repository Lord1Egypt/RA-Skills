#!/bin/bash
# Meta Self-Improvement Activator Hook
# Triggers on UserPromptSubmit to remind about infrastructure learning capture
# Keep output minimal (~50-100 tokens) to minimize overhead

set -e

cat << 'EOF'
<meta-improvement-reminder>
After completing this task, evaluate if agent infrastructure learnings emerged:
- Did any prompt file instruction cause confusion or get ignored?
- Did a hook fail to trigger or produce unexpected output?
- Was a skill missing or inadequate for the task?
- Are any rules contradicting each other across files?
- Is context being wasted on verbose or stale prompt content?
- Could memory entries be pruned or updated?

If yes: Log to .learnings/ using the self-improving-meta format.
If infrastructure fix needed: Apply directly to the affected file.
</meta-improvement-reminder>
EOF
