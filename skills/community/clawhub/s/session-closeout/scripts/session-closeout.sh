#!/usr/bin/env bash
set -euo pipefail

# ── Workspace root detection ─────────────────────────────
ROOT="${OPENCLAW_WORKSPACE:-$(pwd)}"
TODAY_UTC="$(date -u +%F)"
NOW_UTC="$(date -u '+%Y-%m-%d %H:%M UTC')"
MEM_DIR="$ROOT/memory"
MEM_FILE="$MEM_DIR/$TODAY_UTC.md"
MASTER_TODO_FILE="$ROOT/MASTER_TODO.md"
TODO_BUILDER="$ROOT/scripts/build-master-todo.py"
HOOKS_FILE="$ROOT/scripts/closeout-hooks.sh"

# ── Optional overrides (pipe-delimited) ──────────────────
CLOSEOUT_OUTCOMES="${CLOSEOUT_OUTCOMES:-}"
CLOSEOUT_BLOCKERS="${CLOSEOUT_BLOCKERS:-}"
CLOSEOUT_NEXT="${CLOSEOUT_NEXT:-}"

split_pipe_to_bullets() {
  local raw="$1"
  [[ -z "$raw" ]] && return 0
  IFS='|' read -r -a _parts <<< "$raw"
  for p in "${_parts[@]}"; do
    p="$(echo "$p" | sed 's/^ *//; s/ *$//')"
    [[ -n "$p" ]] && echo "  - $p"
  done
}

# ── 1) Task hygiene: refresh master TODO ─────────────────
MASTER_OK="no"
MASTER_REASON="skipped"

if [[ -f "$TODO_BUILDER" ]]; then
  TMP_LOG="$(mktemp)"
  trap 'rm -f "$TMP_LOG"' EXIT
  BEFORE_MTIME="$(stat -c %Y "$MASTER_TODO_FILE" 2>/dev/null || echo 0)"
  if python3 "$TODO_BUILDER" >"$TMP_LOG" 2>&1; then
    AFTER_MTIME="$(stat -c %Y "$MASTER_TODO_FILE" 2>/dev/null || echo 0)"
    if [[ -f "$MASTER_TODO_FILE" ]]; then
      MASTER_OK="yes"
      if [[ "$AFTER_MTIME" -gt "$BEFORE_MTIME" ]]; then
        MASTER_REASON="rewritten"
      else
        MASTER_REASON="unchanged"
      fi
    else
      MASTER_REASON="script_ok_but_file_missing"
    fi
  else
    MASTER_REASON="script_failed"
  fi
else
  MASTER_OK="yes"
  MASTER_REASON="no_builder_script"
fi

# ── 2) Repo hygiene: scan for dirty repos ────────────────
mapfile -t GIT_DIRS < <(find "$ROOT" -maxdepth 4 -type d -name .git 2>/dev/null | sed 's#/.git$##' | sort)
DIRTY=()
for repo in "${GIT_DIRS[@]}"; do
  if [[ -n "$(git -C "$repo" status --porcelain 2>/dev/null || true)" ]]; then
    DIRTY+=("$repo")
  fi
done

# ── 3) Memory hygiene: append closeout block ─────────────
mkdir -p "$MEM_DIR"
if [[ ! -f "$MEM_FILE" ]]; then
  printf '# %s\n\n' "$TODAY_UTC" > "$MEM_FILE"
fi

# Build default bullets
DEFAULT_OUTCOMES=()
DEFAULT_OUTCOMES+=("Closeout completed")
if [[ "$MASTER_OK" == "yes" && "$MASTER_REASON" != "no_builder_script" ]]; then
  DEFAULT_OUTCOMES+=("MASTER_TODO.md refreshed ($MASTER_REASON)")
fi
if ((${#DIRTY[@]} == 0)); then
  DEFAULT_OUTCOMES+=("All repos clean")
else
  DEFAULT_OUTCOMES+=("${#DIRTY[@]} dirty repo(s) found")
fi

DEFAULT_BLOCKERS=()
if ((${#DIRTY[@]} > 0)); then
  DEFAULT_BLOCKERS+=("${#DIRTY[@]} dirty repo(s) need manual review")
fi
if [[ "$MASTER_OK" != "yes" ]]; then
  DEFAULT_BLOCKERS+=("MASTER_TODO refresh failed: $MASTER_REASON")
fi
if ((${#DEFAULT_BLOCKERS[@]} == 0)); then
  DEFAULT_BLOCKERS+=("None")
fi

DEFAULT_NEXT=()
if ((${#DIRTY[@]} > 0)); then
  DEFAULT_NEXT+=("Resolve dirty repo(s) before next work block")
fi
DEFAULT_NEXT+=("Resume from highest-priority item in MASTER_TODO.md")

{
  echo "## Session Closeout — $NOW_UTC"
  echo "- Status: ok"
  echo "- MASTER_TODO: $MASTER_OK ($MASTER_REASON)"
  if ((${#DIRTY[@]} == 0)); then
    echo "- Dirty repos: none"
  else
    echo "- Dirty repos: ${#DIRTY[@]}"
    for d in "${DIRTY[@]}"; do
      rel="${d#$ROOT/}"
      [[ "$rel" == "$d" ]] && rel="."  # workspace root is the repo
      echo "  - $rel"
    done
  fi
  echo "- Key outcomes:"
  if [[ -n "$CLOSEOUT_OUTCOMES" ]]; then
    split_pipe_to_bullets "$CLOSEOUT_OUTCOMES"
  else
    for b in "${DEFAULT_OUTCOMES[@]}"; do echo "  - $b"; done
  fi
  echo "- Blockers:"
  if [[ -n "$CLOSEOUT_BLOCKERS" ]]; then
    split_pipe_to_bullets "$CLOSEOUT_BLOCKERS"
  else
    for b in "${DEFAULT_BLOCKERS[@]}"; do echo "  - $b"; done
  fi
  echo "- Next session starts with:"
  if [[ -n "$CLOSEOUT_NEXT" ]]; then
    split_pipe_to_bullets "$CLOSEOUT_NEXT"
  else
    for b in "${DEFAULT_NEXT[@]}"; do echo "  - $b"; done
  fi
  echo
} >> "$MEM_FILE"

# ── 4) Automation hygiene ────────────────────────────────
AUTOMATION_STATUS="not_verified"
AUTOMATION_REASON="manual_review_required"

# ── 5) Optional hooks ────────────────────────────────────
HOOKS_STATUS="none"
if [[ -f "$HOOKS_FILE" ]]; then
  # shellcheck source=/dev/null
  source "$HOOKS_FILE" && HOOKS_STATUS="ok" || HOOKS_STATUS="failed"
fi

# ── 6) Collect exceptions ────────────────────────────────
EXCEPTIONS=()
if [[ "$MASTER_OK" != "yes" ]]; then
  EXCEPTIONS+=("high|MASTER_TODO refresh failed|Check build-master-todo.py")
fi
if ((${#DIRTY[@]} > 0)); then
  EXCEPTIONS+=("medium|${#DIRTY[@]} dirty repo(s)|Review git status manually")
fi

CLOSEOUT_STATUS="ok"
if [[ "$MASTER_OK" != "yes" ]]; then
  CLOSEOUT_STATUS="error"
elif ((${#EXCEPTIONS[@]} > 0)); then
  CLOSEOUT_STATUS="warning"
fi

# ── 7) Print summary ─────────────────────────────────────
echo "SESSION_CLOSEOUT_OK"
echo "CLOSEOUT_STATUS=$CLOSEOUT_STATUS"
echo "MASTER_TODO_REFRESH=$MASTER_OK"
echo "MASTER_REASON=$MASTER_REASON"
echo "DIRTY_REPO_COUNT=${#DIRTY[@]}"
echo "AUTOMATION_STATUS=$AUTOMATION_STATUS"
echo "HOOKS_STATUS=$HOOKS_STATUS"
echo "EXCEPTION_COUNT=${#EXCEPTIONS[@]}"
i=1
for e in "${EXCEPTIONS[@]}"; do
  echo "EXCEPTION_$i=$e"
  ((i++))
done
if ((${#DIRTY[@]} > 0)); then
  echo "DIRTY_REPOS:"
  for d in "${DIRTY[@]}"; do
    rel="${d#$ROOT/}"
    [[ "$rel" == "$d" ]] && rel="."  # workspace root is the repo
    echo "- $rel"
  done
fi
