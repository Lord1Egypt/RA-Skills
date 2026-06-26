#!/bin/bash
# workspace-audit.sh ... daily workspace health check
# Run manually or via cron. Reports issues to stdout.
# Master Plan 003, Wave 4.

set -uo pipefail
# No set -e: individual git commands may fail on broken worktrees.
# The script must continue past errors to report all issues.

HOME_DIR="${HOME:-/Users/lesa}"
WORKSPACE="${WORKSPACE_DIR:-$HOME_DIR/wipcomputerinc}"
REPOS_DIR="$WORKSPACE/repos"
LDM_DIR="$HOME_DIR/.ldm"
MANIFEST="$REPOS_DIR/repos-manifest.json"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

issues=0
clean=0

echo "Workspace Audit $(date '+%Y-%m-%d %H:%M %Z')"
echo "================================================"
echo ""

# 1. Workspace root cleanliness
echo "1. Workspace root"
ALLOWED="repos library team _trash _transfer screenshots CLAUDE.md .git .gitignore .worktrees _worktrees .DS_Store"
for item in "$WORKSPACE"/*; do
  name=$(basename "$item")
  if ! echo "$ALLOWED" | grep -qw "$name"; then
    echo -e "  ${RED}!${NC} unexpected: $name"
    issues=$((issues + 1))
  fi
done
if [ $issues -eq 0 ]; then
  echo -e "  ${GREEN}clean${NC}"
fi
echo ""

# 2. Dirty repos (uncommitted changes)
echo "2. Dirty repos"
dirty_found=false
while IFS= read -r gitdir; do
  repo=$(dirname "$gitdir")
  case "$repo" in */.worktrees/*|*/_worktrees/*|*/_trash/*) continue ;; esac
  changes=$(git -C "$repo" status --porcelain 2>/dev/null | head -1 || true)
  if [ -n "$changes" ]; then
    name=$(basename "$repo")
    count=$(git -C "$repo" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
    echo -e "  ${YELLOW}!${NC} $name: $count uncommitted file(s)"
    dirty_found=true
  fi
done < <(find "$REPOS_DIR/ldm-os" -maxdepth 3 -name ".git" -type d 2>/dev/null)
if [ "$dirty_found" = false ]; then
  echo -e "  ${GREEN}all clean${NC}"
fi
echo ""

# 3. Stale worktrees (merged branches)
echo "3. Stale worktrees"
stale_found=false
while IFS= read -r wtdir; do
  for wt in "$wtdir"/*/; do
    [ -d "$wt" ] || continue
    branch=$(git -C "$wt" branch --show-current 2>/dev/null || echo "")
    [ -z "$branch" ] && continue
    repo=$(git -C "$wt" rev-parse --git-common-dir 2>/dev/null | sed 's|/.git.*||' || true)
    [ -z "$repo" ] && continue
    merged=$(git -C "$repo" branch --merged main 2>/dev/null | grep -w "$branch" || true)
    if [ -n "$merged" ]; then
      echo -e "  ${YELLOW}!${NC} $(basename "$wt"): branch merged, can be cleaned up"
      stale_found=true
    fi
  done
done < <(find "$REPOS_DIR/ldm-os" -maxdepth 4 -name ".worktrees" -type d 2>/dev/null)
if [ "$stale_found" = false ]; then
  echo -e "  ${GREEN}none${NC}"
fi
echo ""

# 4. Secret scan
echo "4. Secret scan"
secret_count=0
patterns='(sk-ant-api[a-zA-Z0-9_-]{30,}|xai-[a-zA-Z0-9]{30,}|ghp_[a-zA-Z0-9]{30,}|tvly-[a-zA-Z0-9]{30,})'
results=$(grep -r --include="*.mjs" --include="*.js" --include="*.json" --include="*.cjs" \
  -E "$patterns" "$REPOS_DIR/ldm-os/" \
  --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=_trash --exclude-dir=.worktrees \
  2>/dev/null || true)
if [ -n "$results" ]; then
  echo -e "  ${RED}HARDCODED SECRETS FOUND:${NC}"
  echo "$results" | while read line; do
    file=$(echo "$line" | cut -d: -f1 | sed "s|$REPOS_DIR/||")
    echo -e "  ${RED}!${NC} $file"
  done
  secret_count=1
else
  echo -e "  ${GREEN}none found${NC}"
fi
echo ""

# 5. Manifest watchdog
echo "5. Manifest watchdog"
if [ -f "$MANIFEST" ]; then
  # Use wip-repos watchdog if available
  if command -v wip-repos &>/dev/null; then
    unmanifested=$(cd "$REPOS_DIR" && wip-repos watchdog --manifest "$MANIFEST" --json 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d))" 2>/dev/null || echo "?")
    if [ "$unmanifested" = "0" ]; then
      echo -e "  ${GREEN}all repos in manifest${NC}"
    else
      echo -e "  ${YELLOW}!${NC} $unmanifested repo(s) on disk but not in manifest"
      echo "    Run: cd $REPOS_DIR && wip-repos watchdog"
    fi
  else
    echo "  wip-repos not installed, skipping"
  fi
else
  echo "  no manifest found at $MANIFEST"
fi
echo ""

# 6. Compliance check
echo "6. License compliance"
if [ -f "$MANIFEST" ] && command -v wip-repos &>/dev/null; then
  failing=$(cd "$REPOS_DIR" && wip-repos compliance --manifest "$MANIFEST" --json 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(sum(1 for r in d if not r.get('clean',True)))" 2>/dev/null || echo "?")
  total=$(cd "$REPOS_DIR" && wip-repos compliance --manifest "$MANIFEST" --json 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d))" 2>/dev/null || echo "?")
  if [ "$failing" = "0" ]; then
    echo -e "  ${GREEN}$total repos passing${NC}"
  else
    echo -e "  ${YELLOW}!${NC} $failing of $total repos failing"
    echo "    Run: cd $REPOS_DIR && wip-repos compliance"
  fi
else
  echo "  skipping (no manifest or wip-repos)"
fi
echo ""

echo "================================================"
echo "Done."
