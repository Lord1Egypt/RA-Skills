#!/usr/bin/env bash
# ZERO Trading Skill — MCP Setup Script
# Configures the MCP server connection for zero-trading skill.
#
# Usage:
#   bash scanner/skills/zero-trading/scripts/setup.sh
#   bash scanner/skills/zero-trading/scripts/setup.sh --url https://custom.endpoint/mcp
#   bash scanner/skills/zero-trading/scripts/setup.sh --check

set -euo pipefail

ZERO_MCP_URL="${ZERO_MCP_URL:-https://api.getzero.dev/mcp}"
MCP_CONFIG_DIR="${HOME}/.config/mcp"
MCP_CONFIG_FILE="${MCP_CONFIG_DIR}/servers.json"

# Parse arguments
CHECK_ONLY=false
CUSTOM_URL=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --check)
            CHECK_ONLY=true
            shift
            ;;
        --url)
            CUSTOM_URL="$2"
            shift 2
            ;;
        --help|-h)
            echo "ZERO Trading Skill — MCP Setup"
            echo ""
            echo "Usage:"
            echo "  setup.sh              Configure MCP connection (default endpoint)"
            echo "  setup.sh --url URL    Configure with custom endpoint"
            echo "  setup.sh --check      Verify existing configuration"
            echo ""
            echo "Environment:"
            echo "  ZERO_MCP_URL          Override default MCP endpoint"
            echo ""
            echo "Default endpoint: https://api.getzero.dev/mcp"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

if [[ -n "$CUSTOM_URL" ]]; then
    ZERO_MCP_URL="$CUSTOM_URL"
fi

# Check mode — verify config exists and is valid
if $CHECK_ONLY; then
    if [[ ! -f "$MCP_CONFIG_FILE" ]]; then
        echo "no MCP config found at $MCP_CONFIG_FILE"
        echo "run: bash scanner/skills/zero-trading/scripts/setup.sh"
        exit 1
    fi

    if command -v jq &>/dev/null; then
        CONFIGURED_URL=$(jq -r '.mcpServers.zero.url // empty' "$MCP_CONFIG_FILE" 2>/dev/null)
        if [[ -z "$CONFIGURED_URL" ]]; then
            echo "zero MCP server not configured in $MCP_CONFIG_FILE"
            exit 1
        fi
        echo "zero MCP configured: $CONFIGURED_URL"

        # Quick connectivity check
        if command -v curl &>/dev/null; then
            HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$CONFIGURED_URL" 2>/dev/null || echo "000")
            if [[ "$HTTP_CODE" == "000" ]]; then
                echo "warning: cannot reach $CONFIGURED_URL"
                exit 1
            else
                echo "connectivity: ok (HTTP $HTTP_CODE)"
            fi
        fi
    else
        echo "jq not installed — cannot parse config. install jq for full validation."
        grep -q "zero" "$MCP_CONFIG_FILE" && echo "zero entry found in config" || echo "zero entry NOT found"
    fi
    exit 0
fi

# Setup mode — write or update MCP config
echo "configuring zero MCP connection..."
echo "  endpoint: $ZERO_MCP_URL"

mkdir -p "$MCP_CONFIG_DIR"

if command -v jq &>/dev/null; then
    # Use jq for proper JSON manipulation
    if [[ -f "$MCP_CONFIG_FILE" ]]; then
        # Update existing config
        TEMP=$(mktemp)
        jq --arg url "$ZERO_MCP_URL" '.mcpServers.zero = {"url": $url}' "$MCP_CONFIG_FILE" > "$TEMP"
        mv "$TEMP" "$MCP_CONFIG_FILE"
        echo "  updated existing config"
    else
        # Create new config
        jq -n --arg url "$ZERO_MCP_URL" '{"mcpServers": {"zero": {"url": $url}}}' > "$MCP_CONFIG_FILE"
        echo "  created new config"
    fi
else
    # Fallback: write config directly (no jq)
    if [[ -f "$MCP_CONFIG_FILE" ]]; then
        echo "  warning: jq not installed. cannot safely merge into existing config."
        echo "  backup existing config and overwrite? (y/n)"
        read -r REPLY
        if [[ "$REPLY" != "y" ]]; then
            echo "  aborted."
            exit 1
        fi
        cp "$MCP_CONFIG_FILE" "${MCP_CONFIG_FILE}.bak"
        echo "  backed up to ${MCP_CONFIG_FILE}.bak"
    fi

    cat > "$MCP_CONFIG_FILE" << HEREDOC
{
  "mcpServers": {
    "zero": {
      "url": "$ZERO_MCP_URL"
    }
  }
}
HEREDOC
    echo "  wrote config (no jq — clean write)"
fi

echo ""
echo "done. MCP config at: $MCP_CONFIG_FILE"
echo ""
echo "verify with: bash scanner/skills/zero-trading/scripts/setup.sh --check"
