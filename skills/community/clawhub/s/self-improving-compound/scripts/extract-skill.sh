#!/usr/bin/env bash
# extract-skill.sh - Extract a reusable skill from learning records
# Adapted from tristanmanchester + pskoett best practices

set -euo pipefail

SKILL_NAME="${1:-}"
WORKSPACE_ROOT="${2:-$HOME/.openclaw/workspace}"
SOURCE_QUERY="${3:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LEARNINGS_CLI="$SCRIPT_DIR/learnings.py"

if [ -z "$SKILL_NAME" ]; then
    echo "Usage: extract-skill.sh <skill-name> [workspace-root]"
    echo "Example: extract-skill.sh docker-build-fixes"
    exit 1
fi

if [[ ! "$SKILL_NAME" =~ ^[a-z0-9][a-z0-9-]{0,63}$ ]]; then
    echo "ERROR: skill-name must be a slug: lowercase letters, numbers, and hyphens only" >&2
    exit 1
fi

WORKSPACE_ROOT="$(mkdir -p "$WORKSPACE_ROOT" && cd "$WORKSPACE_ROOT" && pwd)"
SKILLS_ROOT="$WORKSPACE_ROOT/skills"
SKILL_DIR="$SKILLS_ROOT/$SKILL_NAME"
mkdir -p "$SKILL_DIR"

sanitize_inline() {
    printf '%s' "$1" | tr '\r\n' '  ' | sed 's/[[:space:]][[:space:]]*/ /g; s/^ //; s/ $//'
}

SOURCE_NOTE="No source query provided."
WHEN_TO_USE="[Fill from the source learning.]"
CORE_RULES="[Fill from the source learning.]"

if [ -n "$SOURCE_QUERY" ] && [ -f "$LEARNINGS_CLI" ]; then
    SEARCH_JSON="$(python3 "$LEARNINGS_CLI" --root "$WORKSPACE_ROOT" search "$SOURCE_QUERY" --format json --limit 1 2>/dev/null || true)"
    EXTRACTED="$(printf '%s' "$SEARCH_JSON" | python3 -c '
import json, sys
try:
    data = json.load(sys.stdin)
except Exception:
    data = []
if data:
    first = data[0]
    print(first.get("id", "unknown"))
    print(first.get("summary", ""))
else:
    print("")
    print("")
' 2>/dev/null || true)"
    SOURCE_ID="$(printf '%s\n' "$EXTRACTED" | sed -n '1p')"
    SOURCE_SUMMARY="$(printf '%s\n' "$EXTRACTED" | sed -n '2p')"
    if [ -n "$SOURCE_ID" ]; then
        SOURCE_NOTE="Source learning: $SOURCE_ID ($SOURCE_QUERY)"
        WHEN_TO_USE="$(sanitize_inline "$SOURCE_SUMMARY")"
        CORE_RULES="- Start from the verified source learning: $(sanitize_inline "$SOURCE_SUMMARY")"
    fi
fi

cat > "$SKILL_DIR/SKILL.md" << EOF
---
name: $SKILL_NAME
description: >-
  Extracted from SQLite-backed learning records. Use when this reusable pattern recurs: $WHEN_TO_USE
metadata:
  source: "learning/extract"
  extracted_at: "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
---

# $SKILL_NAME

## When to Use

$WHEN_TO_USE

## Core Rules

$CORE_RULES

## Quick Reference

| Situation | Action |
|-----------|--------|

## References

- $SOURCE_NOTE
EOF

echo "[extract] Skill scaffold created: $SKILL_DIR/SKILL.md"
echo "[extract] Next steps:"
echo "  1. Edit $SKILL_DIR/SKILL.md to tighten trigger conditions and rules"
echo "  2. Add scripts/ or references/ if needed"
echo "  3. Test before installing: clawhub install $SKILL_NAME --dir /tmp/test"
