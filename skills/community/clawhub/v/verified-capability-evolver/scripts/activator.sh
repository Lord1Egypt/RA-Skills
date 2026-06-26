#!/bin/bash
# Verified Capability Evolver Activator Hook
# Triggers on UserPromptSubmit to remind the agent about learning capture
# and verification gating before permanent promotion.

set -e

cat << 'EOF'
<verified-capability-evolver-reminder>
After completing this task, evaluate if extractable knowledge emerged:
- Non-obvious solution discovered through investigation?
- Workaround for unexpected behavior?
- Project-specific pattern learned?
- Error required debugging to resolve?

If yes: Log to .learnings/ using the verified capability evolver format.

If the learning may become permanent behavior:
- define a deterministic verification spec
- validate the claimed improvement
- promote only after verification returns PASS
</verified-capability-evolver-reminder>
EOF
