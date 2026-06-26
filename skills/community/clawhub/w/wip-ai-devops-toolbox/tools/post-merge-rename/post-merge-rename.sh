#!/usr/bin/env bash
#
# post-merge-rename.sh
# Scans for branches merged into main and renames them with --merged-YYYY-MM-DD.
# Branches already renamed (containing --merged-) are skipped.
# Never deletes branches. Only renames.
#
# Usage:
#   bash post-merge-rename.sh                    # scan + rename all
#   bash post-merge-rename.sh <branch>           # rename a specific branch
#   bash post-merge-rename.sh --dry-run          # preview only
#   bash post-merge-rename.sh <branch> --dry-run # preview specific branch
#
# Run this after merging a PR, or periodically to catch missed renames.
#
# Author: CC-mini (Opus 4.6)
# Date: 2026-03-08

set -euo pipefail

DRY_RUN=false
SPECIFIC_BRANCH=""

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
    --help|-h)
      echo "Usage: post-merge-rename.sh [<branch>] [--dry-run]"
      echo ""
      echo "Scans for branches merged into main and renames them"
      echo "with --merged-YYYY-MM-DD suffix. Never deletes branches."
      exit 0
      ;;
    *) SPECIFIC_BRANCH="$arg" ;;
  esac
done

# Must be in a git repo
if ! git rev-parse --is-inside-work-tree &>/dev/null; then
  echo "Error: not inside a git repo."
  exit 1
fi

# Fetch latest remote state
git fetch origin --prune 2>/dev/null || true

rename_branch() {
  local branch="$1"
  local trimmed
  trimmed=$(echo "$branch" | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')

  # Skip main
  [[ "$trimmed" == "main" || "$trimmed" == "master" ]] && return

  # Skip already renamed
  [[ "$trimmed" == *"--merged-"* ]] && return

  # Skip current branch (can't rename the checked-out branch)
  local current
  current=$(git branch --show-current)
  if [[ "$trimmed" == "$current" ]]; then
    echo "  SKIP $trimmed (currently checked out)"
    return
  fi

  # Find merge date: when this branch's tip became reachable from main
  local merge_date
  merge_date=$(git log main --format="%ai" --ancestry-path "$(git merge-base main "$trimmed" 2>/dev/null)..main" 2>/dev/null | tail -1 | cut -d' ' -f1)

  # Fallback: use the branch tip's own date
  if [[ -z "$merge_date" ]]; then
    merge_date=$(git log "$trimmed" -1 --format="%ai" 2>/dev/null | cut -d' ' -f1)
  fi

  if [[ -z "$merge_date" ]]; then
    echo "  SKIP $trimmed (could not determine merge date)"
    return
  fi

  local new_name="${trimmed}--merged-${merge_date}"

  if $DRY_RUN; then
    echo "  [dry-run] $trimmed -> $new_name"
  else
    echo "  Renaming: $trimmed -> $new_name"

    # Rename local
    git branch -m "$trimmed" "$new_name" 2>/dev/null || true

    # Push new name to remote
    git push origin "$new_name" 2>/dev/null || true

    # Remove old name from remote
    git push origin --delete "$trimmed" 2>/dev/null || true
  fi
}

if [[ -n "$SPECIFIC_BRANCH" && "$SPECIFIC_BRANCH" != "--dry-run" ]]; then
  # Rename a specific branch
  echo "Checking branch: $SPECIFIC_BRANCH"
  if git merge-base --is-ancestor "$SPECIFIC_BRANCH" main 2>/dev/null; then
    rename_branch "$SPECIFIC_BRANCH"
  else
    echo "  $SPECIFIC_BRANCH is NOT merged into main. Leaving as-is."
  fi
else
  # Scan all local branches merged into main
  echo "Scanning for merged branches..."
  merged=$(git branch --merged main | grep -v "^\*" | grep -v "main$" | grep -v "master$" | grep -v "\-\-merged\-" || true)

  if [[ -z "$merged" ]]; then
    echo "  No unrenamed merged branches found. All clean."
    exit 0
  fi

  while IFS= read -r branch; do
    rename_branch "$branch"
  done <<< "$merged"
fi

echo ""
echo "Done."
