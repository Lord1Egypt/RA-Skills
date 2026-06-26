#!/usr/bin/env bash
#
# post-merge-rename.sh
# Scans for branches merged into main and renames them with --merged-YYYY-MM-DD.
# Branches already renamed (containing --merged-) are skipped.
#
# Usage:
#   bash post-merge-rename.sh                    # scan + rename all
#   bash post-merge-rename.sh <branch>           # rename a specific branch
#   bash post-merge-rename.sh --dry-run          # preview only
#   bash post-merge-rename.sh --prune            # rename + delete old merged branches (keep last 3 per developer)
#   bash post-merge-rename.sh --prune --dry-run  # preview prune
#
# Run this after merging a PR, or periodically to catch missed renames.
#
# Author: CC-mini (Opus 4.6)
# Date: 2026-03-08

set -euo pipefail

DRY_RUN=false
PRUNE=false
SPECIFIC_BRANCH=""
KEEP_COUNT=3

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
    --prune) PRUNE=true ;;
    --help|-h)
      echo "Usage: post-merge-rename.sh [<branch>] [--dry-run] [--prune]"
      echo ""
      echo "Scans for branches merged into main and renames them"
      echo "with --merged-YYYY-MM-DD suffix."
      echo ""
      echo "  --prune    After renaming, delete old --merged branches."
      echo "             Keeps the last $KEEP_COUNT per developer prefix."
      echo "             Also deletes stale branches whose PRs are merged"
      echo "             but were never renamed."
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

# ── Prune old merged branches ────────────────────────────────────────

prune_branches() {
  echo ""
  echo "Pruning old merged branches (keeping last $KEEP_COUNT per developer)..."

  # Get all remote --merged branches
  local merged_branches
  merged_branches=$(git branch -r | grep "\-\-merged\-" | sed 's|origin/||' | sed 's/^[[:space:]]*//' | sort)

  if [[ -z "$merged_branches" ]]; then
    echo "  No --merged branches found. Nothing to prune."
    return
  fi

  # Extract unique developer prefixes (everything before the first /)
  local prefixes
  prefixes=$(echo "$merged_branches" | sed 's|/.*||' | sort -u)

  for prefix in $prefixes; do
    # Get all --merged branches for this prefix, sorted by date (newest first)
    # The date is in the --merged-YYYY-MM-DD suffix
    local branches_for_prefix
    branches_for_prefix=$(echo "$merged_branches" | grep "^${prefix}/" | sort -t'-' -k$(echo "$prefix" | tr -cd '-' | wc -c | tr -d ' ' | xargs -I{} expr {} + 5) -r 2>/dev/null || echo "$merged_branches" | grep "^${prefix}/" | sort -r)

    local count=0
    while IFS= read -r branch; do
      [[ -z "$branch" ]] && continue
      count=$((count + 1))

      if [[ $count -le $KEEP_COUNT ]]; then
        echo "  ✓ KEEP $branch"
      else
        # Safety: verify branch is actually merged into main before deleting
        if ! git merge-base --is-ancestor "origin/$branch" origin/main 2>/dev/null; then
          echo "  ! SKIP $branch (NOT merged into main despite --merged suffix)"
          continue
        fi
        if $DRY_RUN; then
          echo "  [dry-run] DELETE $branch"
        else
          git push origin --delete "$branch" 2>/dev/null && echo "  ✗ DELETED $branch" || echo "  ! FAILED to delete $branch"
          git branch -d "$branch" 2>/dev/null || true
        fi
      fi
    done <<< "$branches_for_prefix"
  done

  # Also clean up stale branches: branches without --merged suffix
  # whose PRs are merged (they exist on remote but have no open PR)
  echo ""
  echo "Checking for stale unmerged-looking branches..."

  local all_remote
  all_remote=$(git branch -r | grep -v HEAD | grep -v "origin/main" | sed 's|origin/||' | sed 's/^[[:space:]]*//' | grep -v "\-\-merged\-" || true)

  local current_branch
  current_branch=$(git branch --show-current)

  for branch in $all_remote; do
    [[ -z "$branch" ]] && continue
    # Skip the current working branch
    [[ "$branch" == "$current_branch" ]] && continue

    # Check if this branch is fully merged into main
    if git merge-base --is-ancestor "origin/$branch" origin/main 2>/dev/null; then
      if $DRY_RUN; then
        echo "  [dry-run] DELETE $branch (merged but never renamed)"
      else
        git push origin --delete "$branch" 2>/dev/null && echo "  ✗ DELETED $branch (merged but never renamed)" || echo "  ! FAILED to delete $branch"
        git branch -d "$branch" 2>/dev/null || true
      fi
    fi
  done
}

if $PRUNE; then
  prune_branches
fi

echo ""
echo "Done."
