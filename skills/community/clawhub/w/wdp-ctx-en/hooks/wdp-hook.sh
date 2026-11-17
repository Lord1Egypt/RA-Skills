#!/usr/bin/env bash
# wdp session hooks (SessionStart / PreCompact)
# Usage: bash wdp-hook.sh <load|load-after-clear|load-after-compact|save-precompact>
# Behavior: emits a systemMessage reminder only when the current project already has wdp snapshots; otherwise exits silently (exit 0).
# Reminders only prompt, never auto-execute; there is no before-/clear hook (the CLI offers none), so the fallback is a reminder in the new session after the clear.
set -u

event="${1:-}"
[ -z "$event" ] && exit 0

slug="$(basename "$PWD")"

# Storage-root resolution (same as the /wdp-ctx-en skill): project-level first, user-level fallback.
# Data lives apart from skill code (data in .claude/wdp/; reinstalling the skill does not touch it).
# Only 2*.md count as snapshots (latest.md / profile.md do not).
root=""
for r in "$PWD/.claude/wdp/summaries" "$HOME/.claude/wdp/summaries"; do
  if ls "$r/$slug"/2*.md >/dev/null 2>&1; then
    root="$r"
    break
  fi
done

[ -z "$root" ] && exit 0

case "$event" in
  load)
    msg="This project has wdp work snapshots. Run /wdp-ctx-en init to load the project context (profile + latest snapshot) and resume where you left off."
    ;;
  load-after-clear)
    msg="The previous session has ended. Run /wdp-ctx-en init to load the project context and resume your work."
    ;;
  load-after-compact)
    msg="Context was just compacted. Run /wdp-ctx-en init to reload the project context and resume your work."
    ;;
  save-precompact)
    msg="Context is about to be compacted. Consider running /wdp-ctx-en sum first to save a snapshot of the current work; after compaction, /wdp-ctx-en init resumes it."
    ;;
  *)
    exit 0
    ;;
esac

printf '{"systemMessage": "%s"}\n' "$msg"
