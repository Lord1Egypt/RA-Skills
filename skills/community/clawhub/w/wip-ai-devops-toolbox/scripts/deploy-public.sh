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

PRIVATE_REPO="${1:-}"
PUBLIC_REPO="${2:-}"
DRY_RUN=false

# Parse flags
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
  esac
done

# Strip flags from positional args
ARGS=()
for arg in "$@"; do
  [[ "$arg" == --* ]] || ARGS+=("$arg")
done
PRIVATE_REPO="${ARGS[0]:-}"
PUBLIC_REPO="${ARGS[1]:-}"

if [[ -z "$PRIVATE_REPO" || -z "$PUBLIC_REPO" ]]; then
  echo "Usage: bash deploy-public.sh <private-repo-path> <public-github-repo> [--dry-run]"
  echo "Example: bash deploy-public.sh /path/to/memory-crystal wipcomputer/memory-crystal"
  echo "         bash deploy-public.sh /path/to/memory-crystal wipcomputer/memory-crystal --dry-run"
  exit 1
fi

# Resolve to absolute path so later cd's don't break when cwd changes
PRIVATE_REPO="$(cd "$PRIVATE_REPO" && pwd)"

if [[ ! -d "$PRIVATE_REPO/.git" ]]; then
  echo "Error: $PRIVATE_REPO is not a git repository"
  exit 1
fi

# ── Safety: never deploy back to the source repo ──
# Extract the private repo's GitHub org/name from its remote URL
PRIVATE_REMOTE=$(cd "$PRIVATE_REPO" && git remote get-url origin 2>/dev/null | sed 's/.*github.com[:/]\(.*\)\.git/\1/' || echo "")

if [[ -n "$PRIVATE_REMOTE" && "$PRIVATE_REMOTE" == "$PUBLIC_REPO" ]]; then
  echo "ERROR: PUBLIC_REPO ($PUBLIC_REPO) is the same as the private repo's origin ($PRIVATE_REMOTE)."
  echo "This would deploy sanitized code (no ai/) back to the source repo and destroy files."
  echo "Did you mean to target the public counterpart instead?"
  exit 1
fi

if [[ "$PUBLIC_REPO" == *"-private"* ]]; then
  echo "ERROR: PUBLIC_REPO ($PUBLIC_REPO) contains '-private'."
  echo "deploy-public.sh should only target public repos. Private repos have ai/ folders that would be destroyed."
  exit 1
fi

# Get the latest commit message from private repo
COMMIT_MSG=$(cd "$PRIVATE_REPO" && git log -1 --pretty=format:"%s")
COMMIT_HASH=$(cd "$PRIVATE_REPO" && git log -1 --pretty=format:"%h")

TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

# ── Auto-create public repo if it doesn't exist ──
REPO_EXISTS=$(gh repo view "$PUBLIC_REPO" --json name -q '.name' 2>/dev/null || echo "")
if [[ -z "$REPO_EXISTS" ]]; then
  echo "Public repo $PUBLIC_REPO does not exist. Creating..."
  DESCRIPTION=$(cd "$PRIVATE_REPO" && node -p "require('./package.json').description" 2>/dev/null || echo "")
  gh repo create "$PUBLIC_REPO" --public --description "${DESCRIPTION:-Synced from private repo}" 2>/dev/null
  echo "  + Created $PUBLIC_REPO"
  EMPTY_REPO=true
else
  EMPTY_REPO=false
  # Verify the resolved repo is actually the one we asked for (catch GitHub redirects)
  RESOLVED_NAME=$(gh repo view "$PUBLIC_REPO" --json nameWithOwner -q '.nameWithOwner' 2>/dev/null || echo "")
  if [[ -n "$RESOLVED_NAME" && "$RESOLVED_NAME" != "$PUBLIC_REPO" ]]; then
    echo "ERROR: GitHub redirected $PUBLIC_REPO to $RESOLVED_NAME."
    echo "The public repo doesn't actually exist. A repo with a similar name is redirecting."
    echo "Create the public repo first: gh repo create $PUBLIC_REPO --public"
    exit 1
  fi
fi

echo "Cloning public repo $PUBLIC_REPO..."
gh repo clone "$PUBLIC_REPO" "$TMPDIR/public" -- --depth 1 2>/dev/null || {
  echo "Public repo is empty. Initializing..."
  mkdir -p "$TMPDIR/public"
  cd "$TMPDIR/public"
  git init
  git remote add origin "git@github.com:${PUBLIC_REPO}.git"
  cd - > /dev/null
  EMPTY_REPO=true
}

echo "Syncing files from private repo (excluding ai/, .git/)..."

# Remove all tracked files in public (except .git) so deleted files get removed
find "$TMPDIR/public" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +

# rsync from private, excluding ai/, .git/, worktrees, and other dev artifacts
rsync -a \
  --exclude='ai/' \
  --exclude='_trash/' \
  --exclude='.git/' \
  --exclude='.DS_Store' \
  --exclude='.wrangler/' \
  --exclude='.claude/' \
  --exclude='CLAUDE.md' \
  --exclude='.worktrees/' \
  --exclude='_worktrees/' \
  "$PRIVATE_REPO/" "$TMPDIR/public/"

cd "$TMPDIR/public"

# Rewrite package.json repository URL from private to public repo
# GitHub Packages links packages to the repo in repository.url
if [[ -f package.json ]] && grep -q "\-private" package.json 2>/dev/null; then
  sed -i '' 's|-private\.git|.git|g; s|-private"|"|g' package.json
fi

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

git add -A

# Dry-run: show what would be deployed, then stop
if $DRY_RUN; then
  echo ""
  echo "  Dry run: deploy-public.sh"
  echo "  ────────────────────────────────────"
  echo "  Source: $PRIVATE_REPO"
  echo "  Target: $PUBLIC_REPO"
  echo "  Commit: $COMMIT_MSG ($COMMIT_HASH)"
  echo ""
  echo "  Files that would change:"
  git diff --cached --stat 2>/dev/null || git diff --stat HEAD 2>/dev/null || echo "  (new files)"
  git ls-files --others --exclude-standard | head -20 | while read f; do echo "  + $f"; done
  echo ""
  echo "  Dry run complete. No changes pushed."
  exit 0
fi

git commit -m "$(cat <<COMMITEOF
$COMMIT_MSG (from $COMMIT_HASH)

Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
COMMITEOF
)"

if [[ "$EMPTY_REPO" == "true" ]]; then
  # Empty repo: push directly to main (no base branch to PR against)
  echo "Pushing initial commit to main on $PUBLIC_REPO..."
  git branch -M main
  git push -u origin main
  gh repo edit "$PUBLIC_REPO" --default-branch main 2>/dev/null || true
  PR_URL="(initial push, no PR)"
  echo "  + Initial commit pushed to main"
else
  git checkout -b "$BRANCH"

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

  # Clean up any other non-main branches on public repo
  echo "Checking for stale branches on public repo..."
  STALE_BRANCHES=$(gh api "repos/$PUBLIC_REPO/branches" --paginate --jq '.[].name' 2>/dev/null | grep -v '^main$' || true)
  if [[ -n "$STALE_BRANCHES" ]]; then
    STALE_COUNT=$(echo "$STALE_BRANCHES" | wc -l | tr -d ' ')
    echo "  Found $STALE_COUNT stale branch(es). Deleting..."
    echo "$STALE_BRANCHES" | while read -r stale; do
      gh api -X DELETE "repos/$PUBLIC_REPO/git/refs/heads/$stale" 2>/dev/null && echo "  ✓ Deleted $stale" || echo "  ! Could not delete $stale"
    done
  else
    echo "  ✓ No stale branches"
  fi

  echo "Code synced via PR: $PR_URL"
fi

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

# ── npm publish from public repo (#100) ──
# After syncing code and release, publish to npm from the public clone.
# Only if package.json exists and private !== true.

if [[ -n "${VERSION:-}" ]]; then
  # Re-clone public for npm publish (the previous tmpdir might be gone)
  NPM_TMPDIR=$(mktemp -d)
  gh repo clone "$PUBLIC_REPO" "$NPM_TMPDIR/public" -- --depth 1 2>/dev/null

  if [[ -f "$NPM_TMPDIR/public/package.json" ]]; then
    IS_PRIVATE=$(cd "$NPM_TMPDIR/public" && node -p "require('./package.json').private || false" 2>/dev/null)
    echo "Publishing to npm from public repo..."
    NPM_TOKEN=$(OP_SERVICE_ACCOUNT_TOKEN=$(cat ~/.openclaw/secrets/op-sa-token) \
      op item get "npm Token" --vault "Agent Secrets" --fields label=password --reveal 2>/dev/null || echo "")
    if [[ -n "$NPM_TOKEN" ]]; then
      cd "$NPM_TMPDIR/public"

      # Publish root package (if not private)
      if [[ "$IS_PRIVATE" != "true" ]]; then
        echo "//registry.npmjs.org/:_authToken=${NPM_TOKEN}" > .npmrc
        npm publish --access public 2>/dev/null && echo "  ✓ Published root package to npm" || echo "  ✗ Root npm publish failed (non-fatal)"
        rm -f .npmrc
      else
        echo "  - Root package is private. Skipping root npm publish."
      fi

      # For toolbox repos: publish each sub-tool regardless of root private status
      if [[ -d "tools" ]]; then
        for TOOL_DIR in tools/*/; do
          if [[ -f "${TOOL_DIR}package.json" ]]; then
            TOOL_PRIVATE=$(node -p "require('./${TOOL_DIR}package.json').private || false" 2>/dev/null)
            if [[ "$TOOL_PRIVATE" != "true" ]]; then
              TOOL_NAME=$(node -p "require('./${TOOL_DIR}package.json').name" 2>/dev/null)
              echo "//registry.npmjs.org/:_authToken=${NPM_TOKEN}" > "${TOOL_DIR}.npmrc"
              (cd "$TOOL_DIR" && npm publish --access public 2>/dev/null) && echo "  ✓ Published $TOOL_NAME to npm" || echo "  ✗ npm publish failed for $TOOL_NAME (non-fatal)"
              rm -f "${TOOL_DIR}.npmrc"
            fi
          fi
        done
      fi

      # Publish to GitHub Packages from public repo (#193)
      echo "Publishing to GitHub Packages from public repo..."
      GH_TOKEN=$(gh auth token 2>/dev/null || echo "")
      if [[ -n "$GH_TOKEN" ]]; then
        cd "$NPM_TMPDIR/public"

        # Root package
        if [[ "$IS_PRIVATE" != "true" ]]; then
          echo "//npm.pkg.github.com/:_authToken=${GH_TOKEN}" > .npmrc
          npm publish --registry https://npm.pkg.github.com/ --access public 2>/dev/null && echo "  ✓ Published root to GitHub Packages" || echo "  ✗ Root GitHub Packages publish failed (non-fatal)"
          rm -f .npmrc
        fi

        # Sub-tools
        if [[ -d "tools" ]]; then
          for TOOL_DIR in tools/*/; do
            if [[ -f "${TOOL_DIR}package.json" ]]; then
              TOOL_PRIVATE=$(node -p "require('./${TOOL_DIR}package.json').private || false" 2>/dev/null)
              if [[ "$TOOL_PRIVATE" != "true" ]]; then
                TOOL_NAME=$(node -p "require('./${TOOL_DIR}package.json').name" 2>/dev/null)
                echo "//npm.pkg.github.com/:_authToken=${GH_TOKEN}" > "${TOOL_DIR}.npmrc"
                (cd "$TOOL_DIR" && npm publish --registry https://npm.pkg.github.com/ --access public 2>/dev/null) && echo "  ✓ Published $TOOL_NAME to GitHub Packages" || echo "  ✗ GitHub Packages failed for $TOOL_NAME (non-fatal)"
                rm -f "${TOOL_DIR}.npmrc"
              fi
            fi
          done
        fi

        cd - > /dev/null
      else
        echo "  ! gh auth token not found. Skipping GitHub Packages publish."
      fi

      cd - > /dev/null 2>/dev/null || true
    else
      echo "  ! npm Token not found in 1Password. Skipping npm publish."
    fi
  fi
  rm -rf "$NPM_TMPDIR"
fi

echo "Done. Public repo updated."
echo "  PR: $PR_URL"
echo "  Commit: $COMMIT_MSG (from $COMMIT_HASH)"
[[ -n "${VERSION:-}" ]] && echo "  Release: v$VERSION"
