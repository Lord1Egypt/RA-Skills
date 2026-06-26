#!/bin/bash
# scan_security.sh - Check for security-related events
# Returns: 3=secure, 2=ok, 1=needs attention, 0=compromised

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_scan_helper.sh"

NEED="security"
MEMORY_DIR="$WORKSPACE/memory"
TODAY=$(date +%Y-%m-%d)
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d 2>/dev/null || date -v-1d +%Y-%m-%d 2>/dev/null)

time_sat=$(calc_time_satisfaction "$NEED")

POS_PATTERN="(backup completed|backup success|security check|passed audit|updated|patched|secured|vault intact|integrity ok|all secure|fixed to [0-9])"
NEG_PATTERN="(backup failed|security issue|compromised|breach|vulnerable|attack|unauthorized|leaked|exposed|credential.*(stolen|leaked))"
# Lines matching AUDIT_CONTEXT describe findings/fixes, not active incidents
AUDIT_CONTEXT="(audit|fixed|resolved|checked|verified|scanning|found.*→|TODO|improve scanner|should be|at most|ideally)"

pos_signals=0
neg_signals=0

# Custom scan that adds audit-context awareness on top of negation detection
scan_security_file() {
    local file="$1"
    [[ ! -f "$file" ]] && return
    
    while IFS= read -r line; do
        [[ -z "$line" || "$line" =~ ^#+ ]] && continue
        local has_pos=0 has_neg=0
        echo "$line" | grep -qiE "$POS_PATTERN" && has_pos=1
        echo "$line" | grep -qiE "$NEG_PATTERN" && has_neg=1
        if [[ $has_pos -eq 1 ]]; then
            pos_signals=$((pos_signals + 1))
        elif [[ $has_neg -eq 1 ]]; then
            # Check negation first (existing), then audit context (new)
            if line_has_negation "$line"; then
                :  # "no X leaked" → neutral
            elif echo "$line" | grep -qiE "$AUDIT_CONTEXT"; then
                :  # audit finding/fix context → neutral
            else
                neg_signals=$((neg_signals + 1))
            fi
        fi
    done < "$file"
}

scan_security_file "$MEMORY_DIR/$TODAY.md"
scan_security_file "$MEMORY_DIR/$YESTERDAY.md"

net=$((pos_signals - neg_signals))

if [[ $neg_signals -gt 0 ]]; then
    event_sat=0  # Any security issue = critical
elif [[ $pos_signals -ge 2 ]]; then
    event_sat=3
elif [[ $pos_signals -ge 1 ]]; then
    event_sat=2
else
    event_sat=$time_sat
fi

smart_satisfaction "$NEED" "$event_sat"
