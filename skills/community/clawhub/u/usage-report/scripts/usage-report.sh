#!/usr/bin/env bash
# Usage report - Aggregate cost/token data from OpenClaw session logs
# Reads JSONL session files and sums per-turn usage from assistant messages.

set -euo pipefail

SESSIONS_DIR="${OPENCLAW_SESSIONS_DIR:-$HOME/.openclaw/agents/main/sessions}"
FORMAT="${1:-text}"  # text or json
FILTER="${2:-all}"   # all, today, or a date like 2026-04-07

if [[ ! -d "$SESSIONS_DIR" ]]; then
    echo "Error: Sessions directory not found: $SESSIONS_DIR" >&2
    exit 1
fi

# Collect all JSONL files (skip .lock and .reset files)
files=()
for f in "$SESSIONS_DIR"/*.jsonl; do
    [[ -f "$f" ]] || continue
    [[ "$f" == *.lock ]] && continue
    [[ "$f" == *.reset.* ]] && continue
    files+=("$f")
done

if [[ ${#files[@]} -eq 0 ]]; then
    echo "No session files found in $SESSIONS_DIR" >&2
    exit 1
fi

# Build jq filter for date if needed
# Timestamps may be epoch ms (number) or ISO string — handle both
date_filter=""
if [[ "$FILTER" == "today" ]]; then
    today=$(date -u +%Y-%m-%d)
    start_epoch=$(date -u -d "$today" +%s)000
    end_epoch=$(date -u -d "$today + 1 day" +%s)000
    date_filter="| select((.message.timestamp // .timestamp) as \$ts | if (\$ts | type) == \"number\" then \$ts >= $start_epoch and \$ts < $end_epoch elif (\$ts | type) == \"string\" then \$ts | startswith(\"$today\") else false end)"
elif [[ "$FILTER" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
    start_epoch=$(date -u -d "$FILTER" +%s)000
    end_epoch=$(date -u -d "$FILTER + 1 day" +%s)000
    date_filter="| select((.message.timestamp // .timestamp) as \$ts | if (\$ts | type) == \"number\" then \$ts >= $start_epoch and \$ts < $end_epoch elif (\$ts | type) == \"string\" then \$ts | startswith(\"$FILTER\") else false end)"
fi

if [[ "$FORMAT" == "json" ]]; then
    # JSON output: per-session + total
    jq_per_session='
        [.[] | select(.type == "message" and .message.role == "assistant" and .message.usage != null) '"$date_filter"' | .message.usage] |
        if length == 0 then null
        else {
            turns: length,
            cost: (map(.cost.total) | add),
            input_tokens: (map(.input) | add),
            output_tokens: (map(.output) | add),
            cache_read_tokens: (map(.cacheRead) | add),
            cache_write_tokens: (map(.cacheWrite) | add),
            total_tokens: (map(.totalTokens) | add)
        } end
    '

    results="["
    first=true
    for f in "${files[@]}"; do
        stat=$(cat "$f" | jq -s "$jq_per_session" 2>/dev/null)
        if [[ "$stat" != "null" ]]; then
            name=$(basename "$f" .jsonl)
            entry=$(echo "$stat" | jq --arg name "$name" '. + {session: $name}')
            if $first; then first=false; else results+=","; fi
            results+="$entry"
        fi
    done
    results+="]"

    echo "$results" | jq '{
        sessions: .,
        total: {
            session_count: length,
            turns: (map(.turns) | add // 0),
            cost: (map(.cost) | add // 0),
            input_tokens: (map(.input_tokens) | add // 0),
            output_tokens: (map(.output_tokens) | add // 0),
            cache_read_tokens: (map(.cache_read_tokens) | add // 0),
            cache_write_tokens: (map(.cache_write_tokens) | add // 0),
            total_tokens: (map(.total_tokens) | add // 0)
        }
    }'
else
    # Text output
    echo "=== OpenClaw Usage Report ==="
    [[ "$FILTER" != "all" ]] && echo "Filter: $FILTER"
    echo ""

    grand_cost=0
    grand_turns=0
    grand_output=0

    for f in "${files[@]}"; do
        stat=$(cat "$f" | jq -s '
            [.[] | select(.type == "message" and .message.role == "assistant" and .message.usage != null) '"$date_filter"' | .message.usage] |
            if length == 0 then null
            else {
                turns: length,
                cost: (map(.cost.total) | add),
                output: (map(.output) | add),
                cache_read: (map(.cacheRead) | add),
                cache_write: (map(.cacheWrite) | add)
            } end
        ' 2>/dev/null)

        if [[ "$stat" != "null" ]]; then
            name=$(basename "$f" .jsonl)
            turns=$(echo "$stat" | jq -r '.turns')
            cost=$(echo "$stat" | jq -r '.cost')
            output=$(echo "$stat" | jq -r '.output')
            cache_read=$(echo "$stat" | jq -r '.cache_read')
            cost_fmt=$(printf '%.4f' "$cost")

            echo "📄 $name"
            echo "   Turns: $turns | Cost: \$$cost_fmt | Output: ${output} tokens"
            echo "   Cache: ${cache_read} read / $(echo "$stat" | jq -r '.cache_write') write"
            echo ""

            grand_cost=$(echo "$grand_cost + $cost" | bc 2>/dev/null || echo "$grand_cost")
            grand_turns=$((grand_turns + turns))
            grand_output=$((grand_output + output))
        fi
    done

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Total: $grand_turns turns | \$$(printf '%.2f' "$grand_cost") | ${grand_output} output tokens"
fi
