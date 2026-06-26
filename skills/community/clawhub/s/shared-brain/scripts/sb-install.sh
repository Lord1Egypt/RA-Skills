#!/usr/bin/env bash
# sb-install.sh — One-time setup for a workspace
# Patches all agents/*/AGENTS.md with shared-brain read at startup
# Adds curation step to HEARTBEAT.md
#
# Usage: sb-install.sh [--dry-run]
#   --dry-run   Show what would be changed without modifying any files

set -euo pipefail

# Portable sed -i (macOS requires empty string arg, GNU sed does not)
if sed --version 2>&1 | grep -q GNU 2>/dev/null; then
  _SED_I() { sed -i "$@"; }
else
  _SED_I() { sed -i "" "$@"; }
fi

DRY_RUN=0
[ "${1:-}" = "--dry-run" ] && DRY_RUN=1

CLAWD="${SB_WORKSPACE:-$HOME/clawd}"
BRAIN="$CLAWD/memory/shared-brain.md"
QUEUE="$CLAWD/memory/shared-brain-queue.md"
AGENTS_DIR="$CLAWD/agents"
HEARTBEAT="$CLAWD/HEARTBEAT.md"
SKILL_DEST="$CLAWD/skills/shared-brain/scripts"

echo "=== Shared Brain Install ==="
echo "    Workspace: $CLAWD"
[ $DRY_RUN -eq 1 ] && echo "    [DRY RUN — no files will be modified]"

# 1. Create brain and queue files
if [ ! -f "$BRAIN" ]; then
  if [ $DRY_RUN -eq 1 ]; then
    echo "[dry-run] Would create: $BRAIN"
  else
    mkdir -p "$(dirname "$BRAIN")"
    cat > "$BRAIN" << 'EOF'
# Shared Brain
> Canonical ground truth for all agents. Curated by heartbeat every ≤10 min.
> Written by: sb-write.sh | Curated by: sb-curate.sh | Do not edit manually.
> Sections: [INFRA] [PROJECTS] [DECISIONS] [CAMPAIGNS] [SECURITY]

## [INFRA]

## [PROJECTS]

## [DECISIONS]

## [CAMPAIGNS]

## [SECURITY]
EOF
    echo "✓ Created $BRAIN"
  fi
else
  echo "  $BRAIN already exists — skipped"
fi

if [ $DRY_RUN -eq 0 ]; then
  touch "$QUEUE"
  echo "✓ Queue ready: $QUEUE"
else
  echo "[dry-run] Would create queue: $QUEUE"
fi

# 2. Patch each agent's AGENTS.md
READ_LINE="- **SHARED BRAIN:** \`cat $BRAIN\` (read relevant sections at startup)"
PATCHED=0
SKIPPED=0

for agents_md in "$AGENTS_DIR"/*/AGENTS.md; do
  [ -f "$agents_md" ] || continue
  if grep -q "shared-brain.md" "$agents_md" 2>/dev/null; then
    echo "  $(dirname "$agents_md" | xargs basename) — already patched"
    SKIPPED=$((SKIPPED+1))
    continue
  fi
  if [ $DRY_RUN -eq 1 ]; then
    echo "[dry-run] Would patch: $agents_md"
  else
    if grep -qE "^## (Init|Iniciali)" "$agents_md"; then
      _SED_I "/^## \(Init\|Iniciali\)/a $READ_LINE" "$agents_md"
    else
      sed -i "0,/^##/{/^##/a $READ_LINE
}" "$agents_md"
    fi
    echo "  ✓ Patched: $agents_md"
  fi
  PATCHED=$((PATCHED+1))
done

echo "✓ Agents: $PATCHED to patch, $SKIPPED already done"

# 3. Add curation step to HEARTBEAT.md
if [ -f "$HEARTBEAT" ] && ! grep -q "sb-curate.sh" "$HEARTBEAT"; then
  if [ $DRY_RUN -eq 1 ]; then
    echo "[dry-run] Would patch: $HEARTBEAT"
  else
    cat >> "$HEARTBEAT" << HEREDOC

## Shared Brain Curation (every heartbeat)
\`\`\`bash
$SKILL_DEST/sb-curate.sh
\`\`\`
- Merges shared-brain-queue.md → shared-brain.md
- Reports conflicts for resolution
- Archives if brain > 8KB
HEREDOC
    echo "✓ Patched HEARTBEAT.md"
  fi
else
  echo "  HEARTBEAT.md already patched or not found"
fi

# 4. Copy scripts to workspace
if [ $DRY_RUN -eq 1 ]; then
  echo "[dry-run] Would copy scripts to: $SKILL_DEST"
else
  mkdir -p "$SKILL_DEST"
  cp "$(dirname "$0")"/*.sh "$SKILL_DEST/"
  chmod +x "$SKILL_DEST"/*.sh
  echo "✓ Scripts installed to $SKILL_DEST"
fi

echo ""
if [ $DRY_RUN -eq 1 ]; then
  echo "=== Dry run complete. Run without --dry-run to apply changes. ==="
else
  echo "=== Done. All agents will read shared-brain.md on next startup. ==="
  echo "    Write facts:  $SKILL_DEST/sb-write.sh SECTION \"key = value\""
  echo "    Curate now:   $SKILL_DEST/sb-curate.sh"
fi
