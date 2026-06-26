#!/bin/bash
# Update script for Thetanuts OpenClaw Skill
# Fetches manifest and updates skill files if newer version available
#
# Usage: bash scripts/update.sh
#
# Environment variables (optional):
#   REFRESH_WDK_DEPS=1  - Refresh dependencies from lockfile (npm ci)
#   UPGRADE_WDK_DEPS=1  - Upgrade dependency versions (npm update)
#   RESTART_WDK_RUNTIME=1 - Best-effort restart of runtime process
#   UPDATE_SOURCE_URL   - Override manifest URL

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get script directory (skill base directory)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

# Update source URL (can be overridden via env var)
UPDATE_SOURCE_URL="${UPDATE_SOURCE_URL:-https://raw.githubusercontent.com/goheesheng/thetanuts-openclaw/main/manifest.json}"

echo "🥜 Thetanuts OpenClaw - Update Check"
echo "===================================="
echo ""

# Get current version from SKILL.md frontmatter or manifest.json
get_local_version() {
    if [ -f "$BASE_DIR/manifest.json" ]; then
        # Try to get version from manifest.json
        VERSION=$(grep -o '"version"[[:space:]]*:[[:space:]]*"[^"]*"' "$BASE_DIR/manifest.json" | head -1 | cut -d'"' -f4)
        if [ -n "$VERSION" ]; then
            echo "$VERSION"
            return
        fi
    fi

    # Fallback: try SKILL.md metadata (not reliable)
    echo "0.0.0"
}

# Fetch remote manifest
fetch_manifest() {
    local url="$1"
    local tmp_file=$(mktemp)

    if command -v curl &> /dev/null; then
        if curl -s -f --connect-timeout 10 "$url" -o "$tmp_file" 2>/dev/null; then
            echo "$tmp_file"
            return 0
        fi
    elif command -v wget &> /dev/null; then
        if wget -q --timeout=10 "$url" -O "$tmp_file" 2>/dev/null; then
            echo "$tmp_file"
            return 0
        fi
    fi

    rm -f "$tmp_file"
    return 1
}

# Compare versions (returns 0 if remote > local)
version_gt() {
    local remote="$1"
    local local_ver="$2"

    # Simple comparison using sort -V
    if [ "$(printf '%s\n' "$local_ver" "$remote" | sort -V | tail -n1)" = "$remote" ] && [ "$remote" != "$local_ver" ]; then
        return 0
    fi
    return 1
}

# Main update logic
LOCAL_VERSION=$(get_local_version)
echo "Current version: $LOCAL_VERSION"
echo "Checking for updates..."
echo ""

# Fetch remote manifest
MANIFEST_FILE=$(fetch_manifest "$UPDATE_SOURCE_URL") || {
    echo -e "${YELLOW}⚠ Could not reach update server${NC}"
    echo "  URL: $UPDATE_SOURCE_URL"
    echo "  Check your network connection or try again later."
    echo ""

    # Still allow dependency operations even if manifest fetch fails
    if [ -n "$REFRESH_WDK_DEPS" ] || [ -n "$UPGRADE_WDK_DEPS" ]; then
        echo "Proceeding with dependency operations..."
    else
        exit 0
    fi
}

if [ -n "$MANIFEST_FILE" ] && [ -f "$MANIFEST_FILE" ]; then
    # Parse remote version
    REMOTE_VERSION=$(grep -o '"version"[[:space:]]*:[[:space:]]*"[^"]*"' "$MANIFEST_FILE" | head -1 | cut -d'"' -f4)

    if [ -z "$REMOTE_VERSION" ]; then
        echo -e "${YELLOW}⚠ Could not parse version from remote manifest${NC}"
        rm -f "$MANIFEST_FILE"
    else
        echo "Remote version: $REMOTE_VERSION"

        if version_gt "$REMOTE_VERSION" "$LOCAL_VERSION"; then
            echo -e "${GREEN}New version available!${NC}"
            echo ""

            # Get update URL from manifest
            UPDATE_SCRIPT_URL=$(grep -o '"updateUrl"[[:space:]]*:[[:space:]]*"[^"]*"' "$MANIFEST_FILE" | head -1 | cut -d'"' -f4)

            if [ -n "$UPDATE_SCRIPT_URL" ]; then
                echo "Fetching update script..."

                UPDATE_SCRIPT=$(mktemp)
                if curl -s -f "$UPDATE_SCRIPT_URL" -o "$UPDATE_SCRIPT" 2>/dev/null || \
                   wget -q "$UPDATE_SCRIPT_URL" -O "$UPDATE_SCRIPT" 2>/dev/null; then

                    echo "Running update..."
                    echo ""

                    # CRITICAL: Never modify .env
                    export PROTECT_ENV=1
                    export BASE_DIR="$BASE_DIR"

                    bash "$UPDATE_SCRIPT"

                    rm -f "$UPDATE_SCRIPT"
                    echo -e "${GREEN}✅ Update complete!${NC}"
                else
                    echo -e "${RED}❌ Failed to fetch update script${NC}"
                    rm -f "$UPDATE_SCRIPT"
                fi
            else
                echo -e "${YELLOW}⚠ No updateUrl in manifest - manual update required${NC}"
            fi
        else
            echo -e "${GREEN}✓ Already up to date${NC}"
        fi
    fi

    rm -f "$MANIFEST_FILE"
fi

# Handle dependency operations
WDK_MCP_DIR="$HOME/.openclaw/wdk-mcp"

if [ -n "$REFRESH_WDK_DEPS" ]; then
    echo ""
    echo "Refreshing dependencies (npm ci)..."
    if [ -d "$WDK_MCP_DIR" ]; then
        cd "$WDK_MCP_DIR"
        npm ci --silent 2>&1 | tail -3
        echo -e "${GREEN}✓ Dependencies refreshed${NC}"
    else
        echo -e "${YELLOW}⚠ WDK MCP directory not found. Run onboard.sh first.${NC}"
    fi
fi

if [ -n "$UPGRADE_WDK_DEPS" ]; then
    echo ""
    echo "Upgrading dependencies (npm update)..."
    if [ -d "$WDK_MCP_DIR" ]; then
        cd "$WDK_MCP_DIR"
        npm update --silent 2>&1 | tail -3
        echo -e "${GREEN}✓ Dependencies upgraded${NC}"
    else
        echo -e "${YELLOW}⚠ WDK MCP directory not found. Run onboard.sh first.${NC}"
    fi
fi

if [ -n "$RESTART_WDK_RUNTIME" ]; then
    echo ""
    echo "Attempting to restart WDK runtime..."
    # Best-effort restart - look for running node process with server.js
    pkill -f "wdk-mcp/server.js" 2>/dev/null && echo -e "${GREEN}✓ Runtime process terminated${NC}" || true
    echo -e "${YELLOW}⚠ Runtime restart is best-effort. Start manually if needed.${NC}"
fi

echo ""
echo "===================================="
echo -e "${GREEN}Done.${NC}"
echo ""
echo -e "${YELLOW}Note: Wallet secrets (.env, WDK_SEED) are NEVER modified by updates.${NC}"
