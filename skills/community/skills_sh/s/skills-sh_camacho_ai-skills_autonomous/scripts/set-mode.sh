#!/usr/bin/env bash
# set-mode.sh — Shared mode setter for autonomous/copilot aliases and hooks.
set -euo pipefail

requested_mode="${1:-}"

if [ "$#" -ne 1 ] || { [ "$requested_mode" != "autonomous" ] && [ "$requested_mode" != "copilot" ]; }; then
  echo "Usage: $0 <autonomous|copilot>" >&2
  exit 2
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
# shellcheck source=mode.sh
. "$script_dir/mode.sh"

if [ "$requested_mode" = "copilot" ] && [ -n "${CLAUDE_CODE_REMOTE:-}" ]; then
  echo "Cannot enter copilot mode in a remote session." >&2
  exit 1
fi

session_dir=$(_resolve_session_dir 2>/dev/null || true)

if [ -z "$session_dir" ] || [ ! -d "$session_dir" ]; then
  if [ "$requested_mode" = "autonomous" ]; then
    echo "Session dir not found; autonomous mode is assumed by default." >&2
  else
    echo "Session dir not found — bootstrap may not have run. Restart Claude Code." >&2
    exit 1
  fi
else
  now=$(date +%s)
  if [ "$requested_mode" = "copilot" ]; then
    set_mode copilot "$((now + 14400))" "$((now + 43200))"
  else
    set_mode autonomous
  fi
fi

# Audit log — .claude/.state/ is gitignored; ensure it exists before append
# so fresh checkouts (e.g., CI) don't fail the redirect under set -e.
repo_root="$(cd "$script_dir/../../../.." && pwd -P)"
main_worktree="$(git -C "$repo_root" worktree list --porcelain 2>/dev/null | head -1 | sed 's/^worktree //')"
if [ -n "$main_worktree" ]; then
  mkdir -p "$main_worktree/.claude/.state" 2>/dev/null || true
  if [ "$requested_mode" = "copilot" ]; then
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) copilot activated [pid: $PPID]" >> "$main_worktree/.claude/.state/mode-log" 2>/dev/null || true
  else
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) autonomous restored [pid: $PPID]" >> "$main_worktree/.claude/.state/mode-log" 2>/dev/null || true
  fi
fi

echo "$requested_mode"
