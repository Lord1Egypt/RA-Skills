#!/bin/bash
# Maintain /tmp/claude/loops.json for statusline display.
# Called as PostToolUse hook for CronCreate and CronDelete.

STATE_FILE="/tmp/claude/loops.json"
mkdir -p /tmp/claude

[ ! -f "$STATE_FILE" ] && echo '[]' > "$STATE_FILE"

input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name // empty')

if [ "$tool_name" = "CronCreate" ]; then
    schedule=$(echo "$input" | jq -r '.tool_input.cron // .tool_input.schedule // .tool_input.expression // empty')
    prompt=$(echo "$input" | jq -r '.tool_input.prompt // empty')

    # Extract job ID from tool_response: try JSON first, then 8-char hex in text
    tool_response=$(echo "$input" | jq -r '.tool_response // empty')
    job_id=$(echo "$tool_response" | jq -r '.id // .job_id // empty' 2>/dev/null)
    if [ -z "$job_id" ]; then
        job_id=$(echo "$tool_response" | grep -oE '\b[0-9a-f]{8}\b' | head -1)
    fi
    if [ -z "$job_id" ]; then
        job_id=$(date +%s%N | md5 2>/dev/null || date +%s%N | md5sum | cut -c1-8)
    fi

    tmp=$(mktemp)
    jq --arg id "$job_id" --arg sched "$schedule" --arg prompt "$prompt" \
        '. + [{"id": $id, "schedule": $sched, "prompt": $prompt}]' \
        "$STATE_FILE" > "$tmp" && mv "$tmp" "$STATE_FILE"

elif [ "$tool_name" = "CronDelete" ]; then
    job_id=$(echo "$input" | jq -r '.tool_input.id // .tool_input.job_id // empty')
    if [ -n "$job_id" ]; then
        tmp=$(mktemp)
        jq --arg id "$job_id" '[.[] | select(.id != $id)]' "$STATE_FILE" > "$tmp" && mv "$tmp" "$STATE_FILE"
    fi
fi

exit 0
