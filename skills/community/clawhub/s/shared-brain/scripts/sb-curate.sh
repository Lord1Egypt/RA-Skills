#!/usr/bin/env bash
# sb-curate.sh — Merge queue into shared-brain.md (run by heartbeat)
# Usage: sb-curate.sh [--dry-run]

set -euo pipefail

# Portable sed -i (macOS requires empty string arg, GNU sed does not)
if sed --version 2>&1 | grep -q GNU 2>/dev/null; then
  _SED_I() { sed -i "$@"; }
else
  _SED_I() { sed -i "" "$@"; }
fi

_CLAWD="${SB_WORKSPACE:-$HOME/clawd}"
BRAIN="${SB_BRAIN:-$_CLAWD/memory/shared-brain.md}"
QUEUE="${SB_QUEUE:-$_CLAWD/memory/shared-brain-queue.md}"
ARCHIVE_DIR="${SB_ARCHIVE_DIR:-$_CLAWD/memory}"
MAX_BYTES=8192
DRY_RUN=0

[ "${1:-}" = "--dry-run" ] && DRY_RUN=1

# No queue or empty queue → nothing to do
if [ ! -f "$QUEUE" ] || [ ! -s "$QUEUE" ]; then
  echo "Queue empty — nothing to curate."
  exit 0
fi

CONFLICTS=()
MERGED=0

# Init brain if missing
if [ ! -f "$BRAIN" ]; then
  mkdir -p "$(dirname "$BRAIN")"
  cat > "$BRAIN" << 'EOF'
# Shared Brain
> Canonical ground truth for all agents. Curated by heartbeat. Do not edit manually.

## [INFRA]

## [PROJECTS]

## [DECISIONS]

## [CAMPAIGNS]

## [SECURITY]
EOF
fi

# Parse queue entries
while IFS= read -r line; do
  # Format: [YYYY-MM-DD HH:MM UTC] [SECTION] [agent] key = value
  if [[ "$line" =~ ^\[([0-9]{4}-[0-9]{2}-[0-9]{2}\ [0-9]{2}:[0-9]{2}\ UTC)\]\ \[([A-Z]+)\]\ \[([^\]]+)\]\ (.+=.+)$ ]]; then
    TS="${BASH_REMATCH[1]}"
    SECTION="${BASH_REMATCH[2]}"
    AGENT="${BASH_REMATCH[3]}"
    FACT="${BASH_REMATCH[4]}"
    KEY="${FACT%% = *}"
    NEW_VAL="${FACT#* = }"

    MERGED=$((MERGED + 1))

    # Conflict detection: same key, different value already in brain
    existing_line=$(grep -E "^\[$KEY\] =" "$BRAIN" 2>/dev/null || true)
    if [ -n "$existing_line" ]; then
      existing_val="${existing_line#*= }"
      existing_val="${existing_val%% <!--*}"
      existing_val="${existing_val# }"
      if [ "$existing_val" != "$NEW_VAL" ]; then
        CONFLICTS+=("CONFLICT [$SECTION] $KEY: was '$existing_val' → now '$NEW_VAL' (by $AGENT at $TS)")
      fi
    fi

    if [ $DRY_RUN -eq 0 ]; then
      ENTRY="[$KEY] = $NEW_VAL  <!-- $TS by $AGENT -->"
      if grep -q "^\[$KEY\] =" "$BRAIN" 2>/dev/null; then
        # Replace existing key line
        _SED_I "s|^\[$KEY\] =.*|$ENTRY|" "$BRAIN"
      else
        # Append under the correct section header
        _SED_I "/^## \[$SECTION\]/a $ENTRY" "$BRAIN"
      fi
    fi
  fi
done < "$QUEUE"

# Report conflicts
if [ ${#CONFLICTS[@]} -gt 0 ]; then
  echo "⚠️  CONFLICTS DETECTED — escalate to TARS:"
  for c in "${CONFLICTS[@]}"; do echo "  $c"; done
fi

# Archive if over size limit
if [ $DRY_RUN -eq 0 ] && [ "$(wc -c < "$BRAIN")" -gt $MAX_BYTES ]; then
  ARCHIVE="$ARCHIVE_DIR/shared-brain-archive-$(date -u '+%Y-%m').md"
  echo "Brain > ${MAX_BYTES}B — archiving oldest section to $ARCHIVE"
  python3 - "$BRAIN" "$ARCHIVE" << 'PYEOF'
import sys, re
brain_path, archive_path = sys.argv[1], sys.argv[2]
with open(brain_path) as f:
    content = f.read()
sections = re.split(r'(^## \[.*?\]$)', content, flags=re.MULTILINE)
for i in range(1, len(sections)-1, 2):
    header, body = sections[i], sections[i+1]
    if body.strip():
        with open(archive_path, 'a') as af:
            af.write(f"# Archived {header}\n{body}\n")
        sections[i+1] = "\n"
        with open(brain_path, 'w') as bf:
            bf.write(''.join(sections))
        print(f"Archived section: {header}")
        break
PYEOF
fi

# Clear queue and report
if [ $DRY_RUN -eq 0 ]; then
  > "$QUEUE"
  echo "✓ Curated $MERGED facts. Queue cleared."
else
  echo "[dry-run] Would merge $MERGED facts."
fi
