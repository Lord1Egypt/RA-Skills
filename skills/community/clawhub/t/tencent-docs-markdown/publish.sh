#!/bin/bash
# ============================================================
# Auto version bump & publish script for 腾讯文档Markdown
# Usage:
#   ./publish.sh              # auto bump patch version (e.g. 1.0.3 -> 1.0.4)
#   ./publish.sh patch        # same as above
#   ./publish.sh minor        # bump minor version (e.g. 1.0.3 -> 1.1.0)
#   ./publish.sh major        # bump major version (e.g. 1.0.3 -> 2.0.0)
#   ./publish.sh 2.1.0        # set a specific version
# ============================================================

set -e

# ---- Configuration ----
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
PACKAGE_JSON="$PROJECT_DIR/package.json"
SKILL_NAME="腾讯文档Markdown"

# ---- Color helpers ----
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

info()  { echo -e "${CYAN}[INFO]${NC}  $1"; }
ok()    { echo -e "${GREEN}[OK]${NC}    $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# ---- Pre-flight checks ----
if [ ! -f "$PACKAGE_JSON" ]; then
  error "package.json not found at $PACKAGE_JSON"
fi

if ! command -v clawhub &> /dev/null; then
  error "'clawhub' command not found. Please install it first."
fi

# ---- Read current version ----
CURRENT_VERSION=$(grep -o '"version": *"[^"]*"' "$PACKAGE_JSON" | head -1 | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+')

if [ -z "$CURRENT_VERSION" ]; then
  error "Could not parse current version from package.json"
fi

info "Current version: ${YELLOW}$CURRENT_VERSION${NC}"

# ---- Parse version parts ----
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT_VERSION"

# ---- Determine new version ----
BUMP_TYPE="${1:-patch}"

case "$BUMP_TYPE" in
  patch)
    PATCH=$((PATCH + 1))
    NEW_VERSION="$MAJOR.$MINOR.$PATCH"
    ;;
  minor)
    MINOR=$((MINOR + 1))
    PATCH=0
    NEW_VERSION="$MAJOR.$MINOR.$PATCH"
    ;;
  major)
    MAJOR=$((MAJOR + 1))
    MINOR=0
    PATCH=0
    NEW_VERSION="$MAJOR.$MINOR.$PATCH"
    ;;
  *)
    # Treat as explicit version string (validate format)
    if echo "$BUMP_TYPE" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+$'; then
      NEW_VERSION="$BUMP_TYPE"
    else
      error "Invalid argument: '$BUMP_TYPE'. Use patch|minor|major or a semver string (e.g. 2.1.0)"
    fi
    ;;
esac

info "New version:     ${GREEN}$NEW_VERSION${NC}"

# ---- Confirm ----
echo ""
read -p "$(echo -e "${YELLOW}Publish ${SKILL_NAME} v${NEW_VERSION}? [y/N]: ${NC}")" CONFIRM
if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
  warn "Aborted."
  exit 0
fi

# ---- Update version in package.json ----
if [[ "$OSTYPE" == "darwin"* ]]; then
  # macOS sed requires '' for in-place editing
  sed -i '' "s/\"version\": *\"$CURRENT_VERSION\"/\"version\": \"$NEW_VERSION\"/" "$PACKAGE_JSON"
else
  sed -i "s/\"version\": *\"$CURRENT_VERSION\"/\"version\": \"$NEW_VERSION\"/" "$PACKAGE_JSON"
fi

ok "Updated package.json version to $NEW_VERSION"

# ---- Git commit (optional) ----
if command -v git &> /dev/null && [ -d "$PROJECT_DIR/.git" ]; then
  info "Committing version bump..."
  cd "$PROJECT_DIR"
  git add package.json
  git commit -m "chore: bump version to $NEW_VERSION" 2>/dev/null || warn "Nothing to commit (version may already be staged)"
  ok "Git commit done"
else
  warn "Not a git repo or git not available, skipping commit"
fi

# ---- Publish ----
info "Publishing ${SKILL_NAME} v${NEW_VERSION}..."
echo ""

clawhub publish "$PROJECT_DIR" --version "$NEW_VERSION" --name "$SKILL_NAME"

PUBLISH_EXIT=$?

echo ""
if [ $PUBLISH_EXIT -eq 0 ]; then
  ok "🎉 Successfully published ${SKILL_NAME} v${NEW_VERSION}!"
else
  error "Publish failed with exit code $PUBLISH_EXIT"
fi
