#!/usr/bin/env bash
# Verify file/directory paths referenced in workspace files exist
# Usage: bash scripts/audit-paths.sh
set -euo pipefail

WS="${WS:-$HOME/.openclaw/workspace}"

echo "=== Path Reference Audit ==="
echo ""

# Scan these workspace files for path references
SCAN_FILES=("AGENTS.md" "TOOLS.md" "MEMORY.md" "HEARTBEAT.md")

TOTAL=0
MISSING=0

for fname in "${SCAN_FILES[@]}"; do
  f="$WS/$fname"
  [ -f "$f" ] || continue

  # Extract paths: ~/something, skills/something, scripts/something, docs/something
  paths=$(grep -oE '(~/[a-zA-Z0-9_./-]+|skills/[a-zA-Z0-9_./-]+|scripts/[a-zA-Z0-9_./-]+|docs/[a-zA-Z0-9_./-]+)' "$f" | sort -u)

  while IFS= read -r p; do
    [ -z "$p" ] && continue

    # Resolve path
    resolved="$p"
    if [[ "$p" == "~/"* ]]; then
      resolved="${HOME}/${p:2}"
    elif [[ "$p" != /* ]]; then
      resolved="$WS/$p"
    fi

    # Strip trailing punctuation
    resolved=$(echo "$resolved" | sed 's/[),;:]*$//')

    # Skip template/placeholder paths
    if echo "$resolved" | grep -qE '(YYYY|<[^>]+>|\.\.\.|NNNN)'; then
      continue
    fi

    TOTAL=$((TOTAL + 1))
    if [ ! -e "$resolved" ]; then
      echo "  ❌ $fname → $p"
      MISSING=$((MISSING + 1))
    fi
  done <<< "$paths"
done

echo ""
echo "Checked: $TOTAL | Missing: $MISSING"
echo ""

if [ "$MISSING" -gt 0 ]; then
  echo "⚠️  $MISSING broken path reference(s)"
  exit 1
else
  echo "✅ All referenced paths exist"
  exit 0
fi
