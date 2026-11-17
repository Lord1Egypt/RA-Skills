#!/usr/bin/env bash
# session-closeout.sh — read-only end-of-session audit.
#
# Reports what the current workspace looks like at the end of a session.
# It writes nothing: no files, no directories, no commits, and it runs
# nothing it discovers in the workspace. Recording the closeout is the
# caller's job, done with the values this script prints.
set -euo pipefail

# ── Workspace root: the current directory, never an env override ──
ROOT="$(pwd -P)"
TODAY_UTC="$(date -u +%F)"
MASTER_TODO_FILE="$ROOT/MASTER_TODO.md"
PROJECTS_DIR="$ROOT/projects"

# Stale threshold: digits only, so a hostile value cannot reach arithmetic.
STALE_HOURS="${CLOSEOUT_TODO_STALE_HOURS:-24}"
[[ "$STALE_HOURS" =~ ^[0-9]+$ ]] || STALE_HOURS=24

# Project slugs to check, pipe-delimited. Each must be a plain directory
# name: no separators, no dots-only names, no leading dash.
CLOSEOUT_PROJECTS="${CLOSEOUT_PROJECTS:-}"
SLUG_PATTERN='^[A-Za-z0-9_][A-Za-z0-9._-]*$'

mtime_epoch() { # portable file mtime (GNU or BSD stat), 0 if missing
  stat -c %Y "$1" 2>/dev/null || stat -f %m "$1" 2>/dev/null || echo 0
}

epoch_day() { # epoch seconds -> YYYY-MM-DD (UTC), GNU or BSD date
  date -u -r "$1" +%F 2>/dev/null || date -u -d "@$1" +%F 2>/dev/null || echo ""
}

rel_path() { local r="${1#"$ROOT"/}"; [[ "$r" == "$1" ]] && r="."; printf '%s' "$r"; }

# ── 1) Task hygiene: MASTER_TODO.md freshness (read only) ──
NOW_EPOCH="$(date -u +%s)"
if [[ -f "$MASTER_TODO_FILE" ]]; then
  AGE_H=$(( (NOW_EPOCH - $(mtime_epoch "$MASTER_TODO_FILE")) / 3600 ))
  if (( AGE_H > STALE_HOURS )); then
    MASTER_TODO_STATUS="stale"; MASTER_TODO_DETAIL="last updated ${AGE_H}h ago"
  else
    MASTER_TODO_STATUS="fresh"; MASTER_TODO_DETAIL="updated ${AGE_H}h ago"
  fi
else
  MASTER_TODO_STATUS="missing"; MASTER_TODO_DETAIL="no MASTER_TODO.md"
fi

# ── 2) Repo hygiene: which repos have uncommitted changes ──
# `git status` in an untrusted repo can execute code the repo configures
# (fsmonitor, hooks), so both are pinned off and locks stay untouched.
GIT_DIRS=()
while IFS= read -r d; do GIT_DIRS+=("$d"); done < <(
  find "$ROOT" -maxdepth 4 -type d -name .git 2>/dev/null | sed 's#/\.git$##' | sort
)
DIRTY=()
for repo in "${GIT_DIRS[@]:-}"; do
  [[ -n "$repo" ]] || continue
  if [[ -n "$(git -C "$repo" --no-optional-locks \
                -c core.fsmonitor=false \
                -c core.hooksPath=/dev/null \
                status --porcelain 2>/dev/null || true)" ]]; then
    DIRTY+=("$repo")
  fi
done

# ── 3) Project-doc hygiene: were core docs touched today? (warn only) ──
STALE_PROJECT_DOCS=()
REJECTED_SLUGS=()
if [[ -n "$CLOSEOUT_PROJECTS" ]]; then
  IFS='|' read -r -a _slugs <<< "$CLOSEOUT_PROJECTS"
  for slug in "${_slugs[@]:-}"; do
    slug="${slug#"${slug%%[![:space:]]*}"}"; slug="${slug%"${slug##*[![:space:]]}"}"
    [[ -n "$slug" ]] || continue
    if [[ ! "$slug" =~ $SLUG_PATTERN ]] || [[ "$slug" == *".."* ]]; then
      REJECTED_SLUGS+=("$slug"); continue
    fi
    found_today="no"; any_doc="no"
    for doc in STATUS.md DECISIONS.md PROJECT.md BACKLOG.md; do
      f="$PROJECTS_DIR/$slug/$doc"
      [[ -f "$f" ]] || continue
      any_doc="yes"
      if [[ "$(epoch_day "$(mtime_epoch "$f")")" == "$TODAY_UTC" ]]; then
        found_today="yes"; break
      fi
    done
    if [[ "$any_doc" == "no" ]]; then
      STALE_PROJECT_DOCS+=("$slug (no core docs found under projects/$slug)")
    elif [[ "$found_today" == "no" ]]; then
      STALE_PROJECT_DOCS+=("$slug (no core doc updated today)")
    fi
  done
fi

# ── 4) Automation hygiene: not verifiable from here ──
AUTOMATION_STATUS="not_verified"
AUTOMATION_REASON="manual_review_required"

# ── 5) Final status ──
EXCEPTIONS=()
[[ "$MASTER_TODO_STATUS" == "missing" ]] && EXCEPTIONS+=("high|MASTER_TODO.md missing|Create or restore it")
[[ "$MASTER_TODO_STATUS" == "stale" ]]   && EXCEPTIONS+=("medium|MASTER_TODO.md $MASTER_TODO_DETAIL|Refresh it as a separate, reviewed step")
((${#DIRTY[@]} > 0)) && EXCEPTIONS+=("medium|${#DIRTY[@]} dirty repo(s)|Review git status manually")
for s in "${STALE_PROJECT_DOCS[@]:-}"; do
  [[ -n "$s" ]] && EXCEPTIONS+=("low|project docs: $s|Update STATUS/DECISIONS if the session changed them")
done
for s in "${REJECTED_SLUGS[@]:-}"; do
  [[ -n "$s" ]] && EXCEPTIONS+=("low|rejected project slug: $s|Use a plain directory name under projects/")
done

CLOSEOUT_STATUS="ok"
if [[ "$MASTER_TODO_STATUS" == "missing" ]]; then
  CLOSEOUT_STATUS="error"
elif ((${#EXCEPTIONS[@]} > 0)); then
  CLOSEOUT_STATUS="warning"
fi

# ── 6) Report (key=value for the caller) ──
echo "SESSION_CLOSEOUT_OK"
echo "CLOSEOUT_STATUS=$CLOSEOUT_STATUS"
echo "WORKSPACE_ROOT=$ROOT"
echo "MASTER_TODO_STATUS=$MASTER_TODO_STATUS"
echo "MASTER_TODO_DETAIL=$MASTER_TODO_DETAIL"
echo "DIRTY_REPO_COUNT=${#DIRTY[@]}"
echo "PROJECT_DOC_WARNINGS=${#STALE_PROJECT_DOCS[@]}"
echo "REJECTED_SLUG_COUNT=${#REJECTED_SLUGS[@]}"
echo "AUTOMATION_STATUS=$AUTOMATION_STATUS"
echo "AUTOMATION_REASON=$AUTOMATION_REASON"
echo "EXCEPTION_COUNT=${#EXCEPTIONS[@]}"
i=1
for e in "${EXCEPTIONS[@]:-}"; do
  [[ -n "$e" ]] && { echo "EXCEPTION_$i=$e"; ((i++)); }
done
if ((${#DIRTY[@]} > 0)); then
  echo "DIRTY_REPOS:"
  for d in "${DIRTY[@]}"; do echo "- $(rel_path "$d")"; done
fi
