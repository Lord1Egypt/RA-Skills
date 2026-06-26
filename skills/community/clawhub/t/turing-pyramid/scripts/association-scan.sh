#!/usr/bin/env bash
# association-scan.sh — Contextual recall for Turing Pyramid
# Searches existing artifacts for associations with current context.
# Stateless: reads only, writes nothing, no side effects.
#
# Usage:
#   association-scan.sh --keywords "coherence memory contradictions" \
#     [--need coherence] [--max-results 3] [--recency-hours 168] \
#     [--min-score 2] [--exclude-source <source_type>]
#
# Sources: audit.log conclusions, research/threads/, research/deliberations/,
#          followups.jsonl (pending), INTERESTS.md

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
source "$SCRIPT_DIR/mindstate-utils.sh" # provides: iso_to_epoch, now_epoch, _ms_assets

# ─── Parse args ───
KEYWORDS="" NEED="" MAX_RESULTS=3 RECENCY_HOURS=168 MIN_SCORE=2 EXCLUDE_SOURCE=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --keywords)        KEYWORDS="$2"; shift 2 ;;
        --need)            NEED="$2"; shift 2 ;;
        --max-results)     MAX_RESULTS="$2"; shift 2 ;;
        --recency-hours)   RECENCY_HOURS="$2"; shift 2 ;;
        --min-score)       MIN_SCORE="$2"; shift 2 ;;
        --exclude-source)  EXCLUDE_SOURCE="$2"; shift 2 ;;
        --help|-h)
            echo "Usage: association-scan.sh --keywords '...' [--need N] [--max-results 3]"
            echo "       [--recency-hours 168] [--min-score 2] [--exclude-source <type>]"
            echo ""
            echo "Sources: audit, thread, deliberation, followup, interest"
            exit 0
            ;;
        *) shift ;;
    esac
done

[[ -z "$KEYWORDS" ]] && { echo "❌ --keywords required"; exit 1; }

# Hard cap
(( MAX_RESULTS > 5 )) && MAX_RESULTS=5

AUDIT_LOG="$(_ms_assets)/audit.log"
FOLLOWUPS_FILE="$(_ms_assets)/followups.jsonl"
INTERESTS_FILE="${WORKSPACE:-.}/INTERESTS.md"
RESEARCH_DIR="${WORKSPACE:-.}/research"

NOW_EPOCH=$(now_epoch)
CUTOFF_EPOCH=$((NOW_EPOCH - RECENCY_HOURS * 3600))

# Convert keywords to array
read -ra KW_ARRAY <<< "$KEYWORDS"

# Build grep pattern for pre-filter (ERE — use | not \|)
kw_pattern=$(printf '%s|' "${KW_ARRAY[@]}" | sed 's/|$//')

# ─── Candidate collection ───
# Each candidate: "score|source_type|age_info|need|fragment"
CANDIDATES=()

# --- Source 1: Audit log conclusions ---
if [[ -f "$AUDIT_LOG" ]] && [[ "$EXCLUDE_SOURCE" != "audit" ]]; then
    # Pre-filter: only lines containing "conclusion" AND at least one keyword
    pre_filtered=$(grep -i '"conclusion"' "$AUDIT_LOG" | grep -iE "$kw_pattern" 2>/dev/null || true)

    while IFS= read -r line; do
        [[ -z "$line" ]] && continue

        ts=$(echo "$line" | grep -oP '"timestamp":"[^"]*"' | cut -d'"' -f4)
        [[ -z "$ts" ]] && continue
        ts_epoch=$(iso_to_epoch "$ts" 2>/dev/null || echo 0)
        (( ts_epoch < CUTOFF_EPOCH )) && continue

        conclusion=$(echo "$line" | grep -oP '"conclusion":"[^"]*"' | cut -d'"' -f4)
        [[ -z "$conclusion" || "$conclusion" == "null" ]] && continue

        audit_need=$(echo "$line" | grep -oP '"need":"[^"]*"' | cut -d'"' -f4)

        # Score: keyword hits
        score=0
        for kw in "${KW_ARRAY[@]}"; do
            echo "$conclusion" | grep -qiw "$kw" && ((score += 2)) || true
        done
        (( score == 0 )) && continue

        # Need match bonus
        [[ -n "$NEED" && "$audit_need" == "$NEED" ]] && ((score += 3)) || true

        # Recency bonus (0-2), proper rounding
        hours_ago=$(( (NOW_EPOCH - ts_epoch) / 3600 ))
        recency_bonus=$(echo "scale=2; 2 * (1 - $hours_ago / $RECENCY_HOURS)" | bc -l 2>/dev/null || echo 0)
        if (( $(echo "$recency_bonus > 0" | bc -l 2>/dev/null || echo 0) )); then
            score=$(printf "%.0f" "$(echo "$score + $recency_bonus" | bc -l)")
        fi

        # Action language bonus
        echo "$conclusion" | grep -qiE '(should|need to|update|revisit|fix|demote|create|check)' && ((score += 1)) || true

        CANDIDATES+=("${score}|audit|${hours_ago}h|${audit_need}|${conclusion}")
    done <<< "$pre_filtered"
fi

# --- Source 2: Research threads ---
if [[ -d "$RESEARCH_DIR/threads" ]] && [[ "$EXCLUDE_SOURCE" != "thread" ]]; then
    while IFS= read -r filepath; do
        [[ -z "$filepath" ]] && continue

        file_epoch=$(stat -c %Y "$filepath" 2>/dev/null || echo 0)
        (( file_epoch < CUTOFF_EPOCH )) && continue

        content=$(head -20 "$filepath")

        score=0
        for kw in "${KW_ARRAY[@]}"; do
            echo "$content" | grep -qiw "$kw" && ((score += 2)) || true
        done
        (( score == 0 )) && continue

        hours_ago=$(( (NOW_EPOCH - file_epoch) / 3600 ))
        recency_bonus=$(echo "scale=2; 2 * (1 - $hours_ago / $RECENCY_HOURS)" | bc -l 2>/dev/null || echo 0)
        if (( $(echo "$recency_bonus > 0" | bc -l 2>/dev/null || echo 0) )); then
            score=$(printf "%.0f" "$(echo "$score + $recency_bonus" | bc -l)")
        fi

        # Unresolved bonus
        echo "$content" | grep -qiE '(open|unresolved|todo|question|remaining)' && ((score += 2)) || true

        fragment=$(grep -m1 -iE '(conclusion|outcome|finding|question|tension)' "$filepath" 2>/dev/null \
            || head -3 "$filepath" | tail -1)

        relpath="${filepath#${WORKSPACE:-.}/}"
        CANDIDATES+=("${score}|thread|${hours_ago}h||${relpath}: ${fragment}")
    done < <(find "$RESEARCH_DIR/threads" -name "*.md" -type f 2>/dev/null)
fi

# --- Source 3: Deliberation files ---
if [[ -d "$RESEARCH_DIR/deliberations" ]] && [[ "$EXCLUDE_SOURCE" != "deliberation" ]]; then
    while IFS= read -r filepath; do
        [[ -z "$filepath" ]] && continue
        file_epoch=$(stat -c %Y "$filepath" 2>/dev/null || echo 0)
        (( file_epoch < CUTOFF_EPOCH )) && continue

        content=$(head -30 "$filepath")

        score=0
        for kw in "${KW_ARRAY[@]}"; do
            echo "$content" | grep -qiw "$kw" && ((score += 2)) || true
        done
        (( score == 0 )) && continue

        hours_ago=$(( (NOW_EPOCH - file_epoch) / 3600 ))
        recency_bonus=$(echo "scale=2; 2 * (1 - $hours_ago / $RECENCY_HOURS)" | bc -l 2>/dev/null || echo 0)
        if (( $(echo "$recency_bonus > 0" | bc -l 2>/dev/null || echo 0) )); then
            score=$(printf "%.0f" "$(echo "$score + $recency_bonus" | bc -l)")
        fi

        fragment=$(grep -m1 -iE '(conclusion|outcome|finding)' "$filepath" 2>/dev/null \
            || head -3 "$filepath" | tail -1)

        relpath="${filepath#${WORKSPACE:-.}/}"
        CANDIDATES+=("${score}|deliberation|${hours_ago}h||${relpath}: ${fragment}")
    done < <(find "$RESEARCH_DIR/deliberations" -name "*.md" -type f 2>/dev/null)
fi

# --- Source 4: Pending followups ---
if [[ -f "$FOLLOWUPS_FILE" ]] && [[ "$EXCLUDE_SOURCE" != "followup" ]]; then
    while IFS= read -r line; do
        [[ -z "$line" ]] && continue
        status=$(echo "$line" | grep -oP '"status":"[^"]*"' | cut -d'"' -f4)
        [[ "$status" != "pending" ]] && continue

        what=$(echo "$line" | grep -oP '"what":"[^"]*"' | cut -d'"' -f4)
        fu_need=$(echo "$line" | grep -oP '"need":"[^"]*"' | cut -d'"' -f4)

        score=0
        for kw in "${KW_ARRAY[@]}"; do
            echo "$what" | grep -qiw "$kw" && ((score += 2)) || true
        done
        (( score == 0 )) && continue

        [[ -n "$NEED" && "$fu_need" == "$NEED" ]] && ((score += 3)) || true
        ((score += 2)) || true  # Unresolved bonus

        CANDIDATES+=("${score}|followup|pending|${fu_need}|${what}")
    done < "$FOLLOWUPS_FILE"
fi

# --- Source 5: INTERESTS.md ---
if [[ -f "$INTERESTS_FILE" ]] && [[ "$EXCLUDE_SOURCE" != "interest" ]]; then
    while IFS= read -r line; do
        [[ "$line" =~ ^[[:space:]]*[-*][[:space:]] ]] || continue
        clean=$(echo "$line" | sed 's/^[[:space:]]*[-*] *//')

        score=0
        for kw in "${KW_ARRAY[@]}"; do
            echo "$clean" | grep -qiw "$kw" && ((score += 2)) || true
        done
        (( score == 0 )) && continue

        CANDIDATES+=("${score}|interest|||${clean}")
    done < "$INTERESTS_FILE"
fi

# ─── Sort and output top results ───
if (( ${#CANDIDATES[@]} == 0 )); then
    echo "═══ ASSOCIATIONS (0 found) ═══"
    exit 0
fi

# Sort by score descending
SORTED=$(printf '%s\n' "${CANDIDATES[@]}" | sort -t'|' -k1 -rn)

echo "═══ ASSOCIATIONS ═══"
echo ""
count=0
while IFS='|' read -r score source age need fragment; do
    (( count >= MAX_RESULTS )) && break
    (( ${score:-0} < MIN_SCORE )) && continue

    ((count++)) || true
    need_label=""
    [[ -n "$need" && "$need" != "" ]] && need_label=", $need"
    echo "[$count] (score: $score, $source, ${age} ago${need_label})"
    echo "  ${fragment}"
    echo ""
done <<< "$SORTED"

if (( count == 0 )); then
    echo "(no associations above threshold)"
fi
echo "═══════════════════════════════"
