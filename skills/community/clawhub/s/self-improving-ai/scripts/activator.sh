#!/bin/bash
# AI Self-Improvement Activator Hook
# Triggers on UserPromptSubmit to remind about AI/model learning capture
# Keep output minimal (~50-100 tokens) to minimize overhead

set -e

cat << 'EOF'
<ai-improvement-reminder>
After completing this task, evaluate if AI/model learnings emerged:
- Did the model struggle with a specific input type or modality?
- Was response quality lower than expected for the model used?
- Could a different model or configuration have performed better?
- Did latency or cost exceed expectations?
- Was context window management a problem?
- Did a prompt pattern significantly improve output?
- Were hallucinations detected in factual responses?
- Did RAG retrieval return relevant context?

If yes: Log to .learnings/ using the self-improving-ai format.
If model config change needed: Update model selection or prompt library.
</ai-improvement-reminder>
EOF
