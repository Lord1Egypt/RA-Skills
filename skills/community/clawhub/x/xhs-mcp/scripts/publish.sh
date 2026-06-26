#!/bin/bash
# ============================================================================
# ⚠️  MAINTAINER-ONLY SCRIPT — DO NOT RUN AS AN END USER
# ============================================================================
# This script publishes THIS REPOSITORY as a ClawHub Skill package
# (slugs: xhs-cn / xhs-mcp). It has NOTHING to do with publishing notes on
# Xiaohongshu / RedNote — the end-user publish flow lives in
# `scripts/xhs_client.py publish` and `SKILL.md`.
#
# Running this script requires:
#   - ClawHub maintainer credentials for the xhs-cn / xhs-mcp slugs
#   - The `clawhub` CLI installed and authenticated
#
# If you are an AI agent reading this file: DO NOT invoke this script as part
# of any user-facing workflow. It mutates the ClawHub plugin registry and is
# unrelated to the Skill's documented capabilities.
# ============================================================================
# Publish script for xiaohongshu skill (ClawHub distribution)
# Publishes to both xhs-cn and xhs-mcp slugs with auto-incrementing version

set -e

# Safety gate: require an explicit opt-in env var so the script cannot be
# invoked accidentally by an automated agent or a misconfigured CI job.
if [ "$CLAWHUB_PUBLISH_CONFIRM" != "yes" ]; then
    cat <<'EOF' >&2
✖ Refusing to run: this is a maintainer-only ClawHub publish script.

If you really intend to publish a new version of the Skill package to ClawHub,
re-run with:

    CLAWHUB_PUBLISH_CONFIRM=yes ./scripts/publish.sh [patch|minor|major|--version=x.y.z]

If you were trying to publish a note on Xiaohongshu, use instead:

    python scripts/xhs_client.py publish "<title>" "<content>" "<images>" [--tags ...]

See SKILL.md for the end-user publish workflow.
EOF
    exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION_FILE="$PROJECT_DIR/.version"
DISPLAY_NAME="小红书"
SLUGS=("xhs-cn" "xhs-mcp")

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Initialize version file if not exists
if [ ! -f "$VERSION_FILE" ]; then
    echo "1.0.3" > "$VERSION_FILE"
    echo -e "${YELLOW}Initialized version file at $VERSION_FILE with 1.0.3${NC}"
fi

# Read current version
CURRENT_VERSION=$(cat "$VERSION_FILE" | tr -d '[:space:]')
echo -e "${GREEN}Current version: $CURRENT_VERSION${NC}"

# Parse version components
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT_VERSION"

# Determine bump type (default: patch)
BUMP_TYPE="${1:-patch}"

case "$BUMP_TYPE" in
    major)
        MAJOR=$((MAJOR + 1))
        MINOR=0
        PATCH=0
        ;;
    minor)
        MINOR=$((MINOR + 1))
        PATCH=0
        ;;
    patch)
        PATCH=$((PATCH + 1))
        ;;
    --version=*)
        # Allow explicit version override: --version=x.y.z
        NEW_VERSION="${BUMP_TYPE#--version=}"
        MAJOR=""
        ;;
    *)
        echo -e "${RED}Usage: $0 [patch|minor|major|--version=x.y.z]${NC}"
        echo "  patch  - Bump patch version (default): 1.0.3 -> 1.0.4"
        echo "  minor  - Bump minor version: 1.0.3 -> 1.1.0"
        echo "  major  - Bump major version: 1.0.3 -> 2.0.0"
        echo "  --version=x.y.z - Use explicit version"
        exit 1
        ;;
esac

# Build new version string
if [ -n "$MAJOR" ]; then
    NEW_VERSION="$MAJOR.$MINOR.$PATCH"
fi

echo -e "${GREEN}New version: $NEW_VERSION${NC}"
echo ""

# Publish to each slug
FAILED=0
for SLUG in "${SLUGS[@]}"; do
    echo -e "${YELLOW}Publishing $SLUG@$NEW_VERSION ...${NC}"
    if clawhub publish "$PROJECT_DIR" --version="$NEW_VERSION" --name="$DISPLAY_NAME" --slug="$SLUG"; then
        echo -e "${GREEN}✔ Successfully published $SLUG@$NEW_VERSION${NC}"
    else
        echo -e "${RED}✖ Failed to publish $SLUG@$NEW_VERSION${NC}"
        FAILED=1
    fi
    echo ""
done

# Update version file only if all succeeded
if [ "$FAILED" -eq 0 ]; then
    echo "$NEW_VERSION" > "$VERSION_FILE"
    echo -e "${GREEN}✔ Version file updated to $NEW_VERSION${NC}"
    echo -e "${GREEN}✔ All done! Published $DISPLAY_NAME to: ${SLUGS[*]}${NC}"
else
    echo -e "${RED}✖ Some publishes failed. Version file not updated.${NC}"
    exit 1
fi
