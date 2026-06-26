#!/bin/bash

# Sanitize sensitive information by showing only first and last characters
# Usage: scripts/sanitize.sh "full-string" ["show-first=N,show-last=N"]

INPUT="$1"
OPTIONS="${2:-show-first=4,show-last=4}"

# Parse options
SHOW_FIRST=$(echo "$OPTIONS" | grep -oP 'show-first=\K\d+' || echo 4)
SHOW_LAST=$(echo "$OPTIONS" | grep -oP 'show-last=\K\d+' || echo 4)

# Validate input
if [ -z "$INPUT" ]; then
    echo "[empty]"
    exit 0
fi

LENGTH=${#INPUT}

# If input is too short, show more asterisks or adjust
if [ $LENGTH -le $((SHOW_FIRST + SHOW_LAST)) ]; then
    SHOW_FIRST=$((LENGTH / 2))
    SHOW_LAST=$((LENGTH - SHOW_FIRST))
fi

# Extract parts
FIRST="${INPUT:0:$SHOW_FIRST}"
LAST="${INPUT: -$SHOW_LAST}"

# Calculate asterisks count
AST_COUNT=$((LENGTH - SHOW_FIRST - SHOW_LAST))
if [ $AST_COUNT -lt 1 ]; then
    AST_COUNT=1
fi

# Generate asterisks
ASTERISKS=$(printf '%*s' "$AST_COUNT" | tr ' ' '*')

# Combine
echo "${FIRST}${ASTERISKS}${LAST}"
