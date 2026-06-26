#!/usr/bin/env bash
# anchor — re-anchor persona from IDENTITY.md / SOUL.md
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="${WORKSPACE_ROOT:-$HOME/.openclaw/workspace}"

ID_FILE="$WORKSPACE_ROOT/IDENTITY.md"
SOUL_FILE="$WORKSPACE_ROOT/SOUL.md"

if [ ! -f "$ID_FILE" ]; then
    echo "No IDENTITY.md found at workspace root."
    echo "Run: soulmatic configure"
    exit 1
fi

# Check for anchors
if grep -qi "mbti\|zodiac\|enneagram" "$ID_FILE"; then
    ANCHORS=$(grep -i "mbti\|zodiac\|enneagram" "$ID_FILE" | head -3 | tr '\n' ' ')
    echo "Anchored — $ANCHORS"
else
    echo "Identity active (identity file present, no Triple Anchor set)"
fi

# SOUL.md if present
if [ -f "$SOUL_FILE" ]; then
    echo "SOUL.md loaded"
fi

echo "Identity re-anchored."