#!/bin/bash
# Conversation Self-Improvement Activator Hook
# Triggers on UserPromptSubmit to remind agent about dialogue learning capture
# Keep output minimal (~50-100 tokens) to minimize overhead

set -e

cat << 'EOF'
<conversation-self-improvement-reminder>
After completing this task, evaluate if dialogue learnings should be captured:
- Tone mismatch between agent and user? (formal vs casual, jargon vs simple)
- User had to rephrase or said "that's not what I meant"?
- Context lost mid-conversation? (asked something already answered)
- Hallucinated facts, hours, policies, or capabilities?
- User requested escalation to a human?
- Conversation abandoned due to frustration?

If yes: Log to .learnings/ using the self-improving-conversation skill format.
If a proven pattern (3+ occurrences): propose a reviewed diff for SOUL.md, AGENTS.md, or TOOLS.md; apply only after explicit user approval. Log redacted summaries only — no raw transcripts, PII, or secrets.
</conversation-self-improvement-reminder>
EOF
