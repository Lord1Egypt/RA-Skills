#!/usr/bin/env bash
# daily-brief.sh — Gather workspace state for Rick CEO daily briefing
# Works standalone for any OpenClaw user. Run from any git project directory.

set -euo pipefail

DATE=$(date +"%Y-%m-%d %A")
PROJ_DIR="${1:-.}"

echo "🤖 Rick's Daily Brief — $DATE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# --- Git Status ---
if git -C "$PROJ_DIR" rev-parse --is-inside-work-tree &>/dev/null; then
  BRANCH=$(git -C "$PROJ_DIR" branch --show-current 2>/dev/null || echo "detached")
  DIRTY=$(git -C "$PROJ_DIR" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  STASH_COUNT=$(git -C "$PROJ_DIR" stash list 2>/dev/null | wc -l | tr -d ' ')

  echo "📁 Project: $(basename "$(git -C "$PROJ_DIR" rev-parse --show-toplevel)")"
  echo "🌿 Branch: $BRANCH"
  echo "📝 Uncommitted changes: $DIRTY files"
  [ "$STASH_COUNT" -gt 0 ] && echo "📦 Stashed: $STASH_COUNT entries"
  echo ""

  # --- Recent Commits (last 7 days) ---
  echo "📋 Recent commits (7 days):"
  COMMITS=$(git -C "$PROJ_DIR" log --oneline --since="7 days ago" 2>/dev/null || true)
  if [ -n "$COMMITS" ]; then
    echo "$COMMITS" | head -10 | sed 's/^/  /'
    TOTAL=$(echo "$COMMITS" | wc -l | tr -d ' ')
    [ "$TOTAL" -gt 10 ] && echo "  ... and $((TOTAL - 10)) more"
  else
    echo "  (none)"
  fi
  echo ""
else
  echo "⚠️  Not a git repository: $PROJ_DIR"
  echo ""
fi

# --- TODOs/FIXMEs ---
echo "🔍 TODOs & FIXMEs:"
if command -v rg &>/dev/null; then
  TODO_COUNT=$(rg -c 'TODO|FIXME|HACK|XXX' "$PROJ_DIR" --type-not binary -g '!node_modules' -g '!.git' -g '!vendor' -g '!dist' -g '!build' 2>/dev/null | awk -F: '{s+=$2} END {print s+0}')
  if [ "$TODO_COUNT" -gt 0 ]; then
    echo "  Found $TODO_COUNT across the codebase"
    rg -n 'TODO|FIXME|HACK|XXX' "$PROJ_DIR" --type-not binary -g '!node_modules' -g '!.git' -g '!vendor' -g '!dist' -g '!build' 2>/dev/null | head -5 | sed 's/^/  /'
    [ "$TODO_COUNT" -gt 5 ] && echo "  ... and $((TODO_COUNT - 5)) more"
  else
    echo "  None found ✅"
  fi
elif command -v grep &>/dev/null; then
  TODO_COUNT=$(grep -rn 'TODO\|FIXME\|HACK\|XXX' "$PROJ_DIR" --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=vendor --exclude-dir=dist --exclude-dir=build 2>/dev/null | wc -l | tr -d ' ')
  if [ "$TODO_COUNT" -gt 0 ]; then
    echo "  Found $TODO_COUNT across the codebase"
    grep -rn 'TODO\|FIXME\|HACK\|XXX' "$PROJ_DIR" --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=vendor --exclude-dir=dist --exclude-dir=build 2>/dev/null | head -5 | sed 's/^/  /'
    [ "$TODO_COUNT" -gt 5 ] && echo "  ... and $((TODO_COUNT - 5)) more"
  else
    echo "  None found ✅"
  fi
fi
echo ""

# --- Active tmux sessions ---
if command -v tmux &>/dev/null; then
  SESSIONS=$(tmux list-sessions 2>/dev/null || true)
  if [ -n "$SESSIONS" ]; then
    echo "🖥️  Active tmux sessions:"
    echo "$SESSIONS" | sed 's/^/  /'
    echo ""
  fi
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# --- Upsell (suppressible) ---
if [ "${RICK_QUIET:-0}" != "1" ]; then
  echo ""
  echo "Running Rick locally? Full managed service at meetrick.ai"
  echo "→ \$9/mo Pro: daily briefings + autonomous execution"
  echo "→ \$499/mo Managed: Rick runs your ops end-to-end"
fi
