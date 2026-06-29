#!/usr/bin/env bash
# archive-session.sh — Move a session jsonl out of an active project key
#                     to ~/.claude/projects/.bak/<project-key>_<uuid>.jsonl
#
# Naming convention matches the existing ~/.claude/projects/.bak/ layout
# (flat: <project-key>_<uuid>.jsonl). See claude-session/archive.md.
#
# Usage: archive-session.sh <session-uuid> [--dry-run]
#        archive-session.sh --dry-run <session-uuid>   # --dry-run accepted in any positional slot
#
# Environment:
#   CLAUDE_SESSION_ID  UUID of the currently active Claude Code session.
#                      When set, this script aborts if its target equals
#                      this UUID — preventing archive of a live session
#                      whose JSONL the harness may still rewrite.
#                      The SessionStart inject hook
#                      (~/.claude/hooks/session-id-inject.sh) sets this;
#                      install it via `/session install`.
#                      UNSET → the current-session safety check is
#                      bypassed and a WARN is emitted; the caller must
#                      independently confirm the target is not live.
#
# Exit codes:
#   0   success / dry-run preview
#   1   I/O or precondition error (source missing, dest exists, live session, ...)
#   2   post-move verification mismatch
#   64  CLI usage error (missing/unknown/extra args)

set -euo pipefail

SESSION_ID=""
DRY_RUN=0

usage() {
  echo "Usage: $(basename "$0") <session-uuid> [--dry-run]" >&2
}

for arg in "$@"; do
  case "$arg" in
    --dry-run)
      DRY_RUN=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --*)
      echo "ERROR: unknown flag: $arg" >&2
      usage
      exit 64
      ;;
    *)
      if [[ -n "$SESSION_ID" ]]; then
        echo "ERROR: unexpected extra positional arg: $arg (session-uuid already set to '$SESSION_ID')" >&2
        usage
        exit 64
      fi
      SESSION_ID="$arg"
      ;;
  esac
done

if [[ -z "$SESSION_ID" ]]; then
  usage
  exit 64
fi

# Locate the source file
SRC=$(find "$HOME/.claude/projects" -maxdepth 2 -name "${SESSION_ID}.jsonl" -type f 2>/dev/null | head -1)
if [[ -z "$SRC" ]]; then
  echo "ERROR: session not found anywhere under ~/.claude/projects: $SESSION_ID" >&2
  exit 1
fi

PROJECT_KEY=$(basename "$(dirname "$SRC")")
DST_DIR="$HOME/.claude/projects/.bak"
DST="$DST_DIR/${PROJECT_KEY}_${SESSION_ID}.jsonl"

# Safety checks
if [[ ! -s "$SRC" ]]; then
  echo "ERROR: source is empty (use /session purge instead): $SRC" >&2
  exit 1
fi

if [[ -e "$DST" ]]; then
  echo "ERROR: destination already exists: $DST" >&2
  echo "       Manual resolution required." >&2
  exit 1
fi

# Detect if this is the currently active session via the SessionStart inject hook env.
# When CLAUDE_SESSION_ID is unset, the safety check is bypassed — emit a warning so
# the caller knows they must independently confirm the target is not the live session.
# (See the "Environment" block in this script's header for details.)
if [[ -z "${CLAUDE_SESSION_ID:-}" ]]; then
  echo "WARN: CLAUDE_SESSION_ID is unset — current-session safety check bypassed." >&2
  echo "      Install the SessionStart inject hook via '/session install', or verify" >&2
  echo "      that $SESSION_ID is not the currently active session before proceeding." >&2
elif [[ "${CLAUDE_SESSION_ID}" == "$SESSION_ID" ]]; then
  echo "ERROR: $SESSION_ID is the currently active session — refusing to archive." >&2
  echo "       Close the session in Claude Code first, then re-run." >&2
  exit 1
fi

# Report
SIZE=$(wc -c < "$SRC" | tr -d ' ')
LINES=$(wc -l < "$SRC" | tr -d ' ')
echo "Will archive:"
echo "  FROM: $SRC"
echo "  TO:   $DST"
echo "  SIZE: $SIZE bytes, $LINES lines"
echo "  PROJ: $PROJECT_KEY"

if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "(dry-run — no changes made)"
  exit 0
fi

# Execute
mkdir -p "$DST_DIR"
mv "$SRC" "$DST"

# Verify
if [[ -f "$DST" && ! -f "$SRC" ]]; then
  echo "OK: archived"
else
  echo "FAIL: post-move verification mismatch" >&2
  exit 2
fi

# Append to ledger
LEDGER="$HOME/.claude/projects/.bak/INDEX.md"
if [[ ! -f "$LEDGER" ]]; then
  cat > "$LEDGER" <<'EOF'
# Claude Code Session Archive Index

Each entry: `- YYYY-MM-DD <project-key>_<uuid> — <custom-title or empty>`

EOF
fi

# Pick up a custom-title if the session had one
TITLE=""
if command -v jq >/dev/null 2>&1; then
  TITLE=$(jq -r 'select(.type=="custom-title") | .customTitle // empty' "$DST" 2>/dev/null | head -1 || true)
fi
echo "- $(date +%Y-%m-%d) ${PROJECT_KEY}_${SESSION_ID} — ${TITLE:-(no custom-title)}" >> "$LEDGER"

echo "Ledger updated: $LEDGER"
