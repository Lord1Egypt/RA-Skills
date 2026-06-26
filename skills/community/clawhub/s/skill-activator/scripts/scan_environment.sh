#!/usr/bin/env bash
# scan_environment.sh — Scan OpenClaw environment and generate activation report
# Usage: bash scripts/scan_environment.sh [workspace_dir]
#
# Scans:
#   1. Installed skills (name + description from SKILL.md frontmatter)
#   2. Channel configuration (which platforms are connected)
#   3. User identity (SOUL.md, USER.md, IDENTITY.md)
#   4. Workspace files (HEARTBEAT.md, MEMORY.md, etc.)
#
# Output: structured report to stdout

set -euo pipefail

WORKSPACE="${1:-$(pwd)}"
SKILL_DIRS=("$HOME/.agents/skills" "$HOME/git/openclaw/skills" "$WORKSPACE/skills")

echo "=== SKILL ACTIVATOR — ENVIRONMENT SCAN ==="
echo "Scan time: $(date '+%Y-%m-%d %H:%M:%S')"
echo "Workspace: $WORKSPACE"
echo ""

# --- 1. Installed Skills ---
echo "## INSTALLED SKILLS"
echo ""
skill_count=0
for dir in "${SKILL_DIRS[@]}"; do
  if [ -d "$dir" ]; then
    for skill_md in "$dir"/*/SKILL.md; do
      [ -f "$skill_md" ] || continue
      skill_dir=$(dirname "$skill_md")
      skill_name=$(basename "$skill_dir")
      # Extract description from frontmatter
      desc=$(awk '/^---$/{n++; next} n==1 && /^description:/{sub(/^description: */, ""); print; exit}' "$skill_md" 2>/dev/null || echo "N/A")
      # Truncate long descriptions
      if [ ${#desc} -gt 120 ]; then
        desc="${desc:0:117}..."
      fi
      echo "- [$skill_name] $desc"
      skill_count=$((skill_count + 1))
    done
  fi
done
echo ""
echo "Total skills installed: $skill_count"
echo ""

# --- 2. User Identity ---
echo "## USER IDENTITY"
echo ""
for f in SOUL.md USER.md IDENTITY.md; do
  fpath="$WORKSPACE/$f"
  if [ -f "$fpath" ]; then
    echo "### $f"
    head -30 "$fpath" 2>/dev/null
    echo ""
  else
    echo "### $f — NOT FOUND"
    echo ""
  fi
done

# --- 3. Channel Configuration ---
echo "## CHANNELS"
echo ""
config_dir="$HOME/.openclaw"
if [ -d "$config_dir" ]; then
  # Check for common channel configs
  for channel in feishu wecom telegram discord slack whatsapp signal; do
    if grep -rql "$channel" "$config_dir"/*.yaml "$config_dir"/*.yml "$config_dir"/*.json 2>/dev/null; then
      echo "- ✅ $channel (configured)"
    fi
  done
else
  echo "- No OpenClaw config directory found"
fi
echo ""

# --- 4. Workspace State ---
echo "## WORKSPACE STATE"
echo ""
for f in HEARTBEAT.md MEMORY.md AGENTS.md TOOLS.md; do
  fpath="$WORKSPACE/$f"
  if [ -f "$fpath" ]; then
    lines=$(wc -l < "$fpath" 2>/dev/null || echo "0")
    size=$(wc -c < "$fpath" 2>/dev/null || echo "0")
    echo "- $f: ${lines} lines, ${size} bytes"
  else
    echo "- $f: NOT FOUND"
  fi
done

# Check memory directory
if [ -d "$WORKSPACE/memory" ]; then
  mem_count=$(ls "$WORKSPACE/memory"/*.md 2>/dev/null | wc -l || echo "0")
  echo "- memory/: ${mem_count} daily files"
else
  echo "- memory/: NOT FOUND"
fi
echo ""

echo "=== SCAN COMPLETE ==="
