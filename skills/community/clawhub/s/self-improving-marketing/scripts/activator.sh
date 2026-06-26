#!/bin/bash
# Marketing Self-Improvement Activator Hook
# Triggers on UserPromptSubmit to remind about marketing-specific learning capture
# Keep output minimal (~50-100 tokens) to minimize overhead

set -e

cat << 'EOF'
<marketing-self-improvement-reminder>
After completing this marketing task, evaluate if extractable knowledge emerged:
- CTR or conversion rate dropped significantly? → CAMPAIGN_ISSUES.md
- Email deliverability problem (bounces, spam)? → CAMPAIGN_ISSUES.md
- Messaging missed the target segment? → LEARNINGS.md (messaging_miss)
- Channel underperformed benchmarks? → LEARNINGS.md (channel_underperformance)
- Audience behavior or ICP shifted? → LEARNINGS.md (audience_drift)
- Brand guideline violated? → LEARNINGS.md (brand_inconsistency)
- UTM or attribution tracking broken? → LEARNINGS.md (attribution_gap)
- Content lost traffic or ranking? → LEARNINGS.md (content_decay)

If recurring pattern (3+ occurrences): promote to brand guidelines or channel playbook.
If broadly applicable: consider skill extraction.
</marketing-self-improvement-reminder>
EOF
