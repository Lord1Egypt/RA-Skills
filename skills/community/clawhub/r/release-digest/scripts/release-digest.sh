#!/usr/bin/env bash
# release-digest.sh — deterministic git-based release digest (no external API).
set -euo pipefail
repo="." since="" until="HEAD"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo) repo="$2"; shift 2;;
    --since) since="$2"; shift 2;;
    --until) until="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done
cd "$repo"
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "error: '$repo' is not a git repository" >&2; exit 2
fi
if [[ -z "$since" ]]; then
  if since="$(git describe --tags --abbrev=0 2>/dev/null)"; then :; else since="14 days ago"; fi
fi
range="$since..$until"
count="$(git rev-list --count "$range" 2>/dev/null || echo 0)"
authors="$(git log --format='%an' "$range" 2>/dev/null | sort -u | wc -l | tr -d ' ')"
printf '## Release digest\n\n'
printf -- '- Repository: `%s`\n' "$(basename "$(git rev-parse --show-toplevel)")"
printf -- '- Window: `%s` .. `%s`\n' "$since" "$until"
printf -- '- Commits: %s\n' "$count"
printf -- '- Contributors: %s\n\n' "$authors"
printf '### Commits\n\n'
git log --no-merges --reverse --format='- %s (%an) `%h`' "$range" 2>/dev/null || true
printf '\n### Files changed\n\n'
git diff --stat "$range" 2>/dev/null || true
