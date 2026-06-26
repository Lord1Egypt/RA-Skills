#!/bin/bash
# Conversation Self-Improvement Error Detector Hook
# Triggers on PostToolUse for Bash to detect dialogue-related failures
# Reads CLAUDE_TOOL_OUTPUT environment variable

set -e

OUTPUT="${CLAUDE_TOOL_OUTPUT:-}"

# Patterns indicating conversation/dialogue errors
ERROR_PATTERNS=(
    "user frustration"
    "misunderstood"
    "wrong intent"
    "hallucination"
    "escalation failed"
    "context lost"
    "sentiment negative"
    "tone mismatch"
    "handoff failed"
    "intent not found"
    "intent_detection"
    "NLU error"
    "classification error"
    "confidence below threshold"
    "fallback triggered"
    "no matching intent"
    "conversation abandoned"
    "user left"
    "timeout: no response"
    "channel error"
    "webhook failed"
    "response generation failed"
    "template not found"
    "language not supported"
    "error:"
    "Error:"
    "ERROR:"
    "failed"
    "FAILED"
    "Exception"
    "Traceback"
)

contains_error=false
for pattern in "${ERROR_PATTERNS[@]}"; do
    if [[ "$OUTPUT" == *"$pattern"* ]]; then
        contains_error=true
        break
    fi
done

if [ "$contains_error" = true ]; then
    cat << 'EOF'
<dialogue-error-detected>
A conversation-related error was detected. Consider logging to .learnings/ if:
- Intent classification failed or returned wrong intent
- Response generation produced incorrect or hallucinated content
- Escalation/handoff workflow broke
- User sentiment turned negative due to agent behavior
- Context was lost in a multi-turn dialogue
- Channel integration (Slack, web, voice) encountered an error

Use the self-improving-conversation format: [DLG-YYYYMMDD-XXX] or [LRN-YYYYMMDD-XXX]
</dialogue-error-detected>
EOF
fi
