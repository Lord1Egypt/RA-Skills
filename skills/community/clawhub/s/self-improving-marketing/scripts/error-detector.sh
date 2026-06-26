#!/bin/bash
# Marketing Self-Improvement Error Detector Hook
# Triggers on PostToolUse for Bash to detect campaign issues, deliverability problems, and tracking errors
# Reads CLAUDE_TOOL_OUTPUT environment variable

set -e

OUTPUT="${CLAUDE_TOOL_OUTPUT:-}"

ERROR_PATTERNS=(
    "bounce rate"
    "unsubscribe"
    "deliverability"
    "CTR"
    "conversion"
    "impression"
    "CPL"
    "CPA"
    "ROAS"
    "brand"
    "off-brand"
    "spam"
    "spam score"
    "open rate"
    "click rate"
    "unattributed"
    "utm"
    "UTM"
    "attribution"
    "organic traffic"
    "ranking drop"
    "content decay"
    "audience drift"
    "engagement rate"
    "reach decline"
    "frequency cap"
    "ad fatigue"
    "quality score"
    "relevance score"
    "domain reputation"
    "blacklist"
    "blocklist"
    "SPF"
    "DKIM"
    "DMARC"
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
<marketing-issue-detected>
A marketing issue was detected in command output. Consider logging to .learnings/ if:
- Campaign performance dropped below benchmarks → CAMPAIGN_ISSUES.md [CMP-YYYYMMDD-XXX]
- Email deliverability problem (bounce, spam, reputation) → CAMPAIGN_ISSUES.md with deliverability trigger
- Attribution or tracking broken (UTM, redirect, cross-domain) → LEARNINGS.md with attribution_gap category
- Brand or messaging inconsistency found → LEARNINGS.md with brand_inconsistency category
- Content lost organic traffic or ranking → LEARNINGS.md with content_decay category

Include before/after metrics, channel, and area tag.
</marketing-issue-detected>
EOF
fi
