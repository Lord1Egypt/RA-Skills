#!/usr/bin/env bash
#
# deploy-public.sh ... sync a private repo to its public counterpart
#
# Usage:
#   bash deploy-public.sh <private-repo-path> <public-github-repo>
#
# Example:
#   bash deploy-public.sh /path/to/memory-crystal wipcomputer/memory-crystal
#
# Convention:
#   - Private repo: {name}-private (where all work happens)
#   - Public repo:  {name} (deployment target, never work here directly)
#   - ai/ folder is excluded from public deploys
#   - Old ai/ in public git history is fine, just not going forward
#
# Location: wip-dev-guide-private/scripts/deploy-public.sh (one script for all repos)

set -euo pipefail

PRIVATE_REPO="$1"
PUBLIC_REPO="$2"

if [[ -z "$PRIVATE_REPO" || -z "$PUBLIC_REPO" ]]; then
  echo "Usage: bash deploy-public.sh <private-repo-path> <public-github-repo>"
  echo "Example: bash deploy-public.sh /path/to/memory-crystal wipcomputer/memory-crystal"
  exit 1
fi

if [[ ! -d "$PRIVATE_REPO/.git" ]]; then
  echo "Error: $PRIVATE_REPO is not a git repository"
  exit 1
fi

# Get the latest commit message from private repo
COMMIT_MSG=$(cd "$PRIVATE_REPO" && git log -1 --pretty=format:"%s")
COMMIT_HASH=$(cd "$PRIVATE_REPO" && git log -1 --pretty=format:"%h")

TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

echo "Cloning public repo $PUBLIC_REPO..."
gh repo clone "$PUBLIC_REPO" "$TMPDIR/public" -- --depth 1 2>/dev/null || {
  echo "Public repo is empty or doesn't exist. Initializing..."
  mkdir -p "$TMPDIR/public"
  cd "$TMPDIR/public"
  git init
  git remote add origin "git@github.com:${PUBLIC_REPO}.git"
  cd - > /dev/null
}

echo "Syncing files from private repo (excluding ai/, .git/)..."

# Remove all tracked files in public (except .git) so deleted files get removed
find "$TMPDIR/public" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +

# rsync from private, excluding ai/ and .git/
rsync -a \
  --exclude='ai/' \
  --exclude='.git/' \
  --exclude='.DS_Store' \
  --exclude='.wrangler/' \
  --exclude='.claude/' \
  --exclude='CLAUDE.md' \
  "$PRIVATE_REPO/" "$TMPDIR/public/"

cd "$TMPDIR/public"

# Check if there are changes
if git diff --quiet HEAD -- 2>/dev/null && git diff --cached --quiet HEAD -- 2>/dev/null && [[ -z "$(git ls-files --others --exclude-standard)" ]]; then
  echo "No changes to deploy."
  exit 0
fi

# Harness ID for branch prefix. Set HARNESS_ID env var, or auto-detect from private repo path.
if [[ -z "${HARNESS_ID:-}" ]]; then
  case "$PRIVATE_REPO" in
    *"Claude Code - Mini"*) HARNESS_ID="cc-mini" ;;
    *"Claude Code - MBA"*)  HARNESS_ID="cc-air" ;;
    *"Lēsa"*)               HARNESS_ID="oc-lesa-mini" ;;
    *)                       HARNESS_ID="deploy" ;;
  esac
fi
BRANCH="$HARNESS_ID/deploy-$(date +%Y%m%d-%H%M%S)"

git checkout -b "$BRANCH"
git add -A
git commit -m "$COMMIT_MSG (from $COMMIT_HASH)"

echo "Pushing branch $BRANCH to $PUBLIC_REPO..."
git push -u origin "$BRANCH"

echo "Creating PR..."
PR_URL=$(gh pr create -R "$PUBLIC_REPO" \
  --head "$BRANCH" \
  --title "$COMMIT_MSG" \
  --body "Synced from private repo (commit $COMMIT_HASH).")

echo "Merging PR..."
PR_NUMBER=$(echo "$PR_URL" | grep -o '[0-9]*$')
gh pr merge "$PR_NUMBER" -R "$PUBLIC_REPO" --merge --delete-branch

echo "Code synced via PR: $PR_URL"

# ── Sync release to public repo ──
# If the private repo has a version tag, create a matching release on the public repo.
# Pulls full release notes from the private repo and rewrites any private repo references.

# Try package.json first, fall back to latest git tag
VERSION=$(cd "$PRIVATE_REPO" && node -p "require('./package.json').version" 2>/dev/null || echo "")
if [[ -z "$VERSION" ]]; then
  # No package.json. Use the latest version tag (v*) in the repo
  TAG=$(cd "$PRIVATE_REPO" && git tag -l 'v*' --sort=-version:refname 2>/dev/null | head -1 || echo "")
  if [[ -n "$TAG" ]]; then
    VERSION="${TAG#v}"
  fi
fi
if [[ -n "$VERSION" ]]; then
  TAG="v$VERSION"
  EXISTING=$(gh release view "$TAG" -R "$PUBLIC_REPO" --json tagName 2>/dev/null || echo "")
  if [[ -z "$EXISTING" ]]; then
    # Get the private repo's GitHub path (e.g., wipcomputer/memory-crystal-private)
    PRIVATE_GH=$(cd "$PRIVATE_REPO" && git remote get-url origin | sed 's/.*github.com[:/]\(.*\)\.git/\1/')

    # Pull full release notes from private repo
    NOTES=$(gh release view "$TAG" -R "$PRIVATE_GH" --json body -q '.body' 2>/dev/null || echo "")

    if [[ -z "$NOTES" || "$NOTES" == "null" ]]; then
      NOTES="Release $TAG"
    else
      # Rewrite private repo references to public repo
      NOTES=$(echo "$NOTES" | sed "s|$PRIVATE_GH|$PUBLIC_REPO|g")
    fi

    echo "Creating release $TAG on $PUBLIC_REPO..."
    gh release create "$TAG" -R "$PUBLIC_REPO" --title "$TAG" --notes "$NOTES" 2>/dev/null && echo "  ✓ Release $TAG created on $PUBLIC_REPO" || echo "  ✗ Release creation failed (non-fatal)"
  else
    # Update existing release notes (in case they were incomplete)
    PRIVATE_GH=$(cd "$PRIVATE_REPO" && git remote get-url origin | sed 's/.*github.com[:/]\(.*\)\.git/\1/')
    NOTES=$(gh release view "$TAG" -R "$PRIVATE_GH" --json body -q '.body' 2>/dev/null || echo "")
    if [[ -n "$NOTES" && "$NOTES" != "null" ]]; then
      NOTES=$(echo "$NOTES" | sed "s|$PRIVATE_GH|$PUBLIC_REPO|g")
      gh release edit "$TAG" -R "$PUBLIC_REPO" --notes "$NOTES" 2>/dev/null && echo "  ✓ Release $TAG notes updated on $PUBLIC_REPO" || true
    fi
    echo "  Release $TAG exists on $PUBLIC_REPO (notes synced)"
  fi
fi

echo "Done. Public repo updated."
echo "  PR: $PR_URL"
echo "  Commit: $COMMIT_MSG (from $COMMIT_HASH)"
[[ -n "${VERSION:-}" ]] && echo "  Release: v$VERSION"
