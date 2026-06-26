#!/bin/bash
# Self-Optimization Activator Hook
# Emits a compact reminder after prompt submission.

set -e

cat << 'EOF'
<self-optimization-reminder>
Before finishing, check whether this task produced durable signal:
- correction, missing fact, or new convention
- non-obvious failure or workaround
- repeated friction worth linking or promoting
- missing capability the user asked for

If yes: capture it in .learnings/ and promote stable patterns into agent guidance.
</self-optimization-reminder>
EOF
