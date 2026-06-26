#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENT_ADDRESS_FILE="$SCRIPT_DIR/.agent-address.txt"
OWNER_HANDOFF_FILE="$SCRIPT_DIR/.owner-handoff.json"

DEFAULT_PACKAGE_ID="0xcc76747b518ea5d07255a26141fb5e0b81fcdd0dc1cc578a83f88adc003a6191"
DEFAULT_NETWORK="testnet"
DEFAULT_PORTAL_URL="https://dash.safeflow.space"
DEFAULT_MIN_AGENT_GAS_MIST="200000000"
DEFAULT_RECOMMENDED_PREDEPOSIT_MIST="1000000000"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
info()    { echo -e "${BLUE}[handoff]${NC} $*"; }
success() { echo -e "${GREEN}[handoff]${NC} $*"; }
warn()    { echo -e "${YELLOW}[handoff]${NC} $*"; }
error()   { echo -e "${RED}[handoff]${NC} $*" >&2; }

is_sui_address() {
    [[ "$1" =~ ^0x[0-9a-fA-F]{64}$ ]]
}

usage() {
    cat <<'EOF'
Usage:
  ./bootstrap_owner_handoff.sh [options]

Options:
  --package-id <id>                 SafeFlow package id (default: shared package)
  --network <name>                  Sui env name (default: testnet)
  --portal-url <url>                Owner config portal URL placeholder
  --agent-address <address>         Reuse a specific agent address from keystore
  --min-agent-gas-mist <mist>       Suggested minimum gas for agent
  --recommended-predeposit-mist <mist>
                                    Suggested wallet predeposit amount
  --force-new-agent                 Always create a new agent address
  --no-open                         Do not open portal URL automatically
  -h, --help                        Show this help
EOF
}

PACKAGE_ID="$DEFAULT_PACKAGE_ID"
NETWORK="$DEFAULT_NETWORK"
PORTAL_URL="$DEFAULT_PORTAL_URL"
AGENT_ADDRESS=""
MIN_AGENT_GAS_MIST="$DEFAULT_MIN_AGENT_GAS_MIST"
RECOMMENDED_PREDEPOSIT_MIST="$DEFAULT_RECOMMENDED_PREDEPOSIT_MIST"
FORCE_NEW_AGENT=false
NO_OPEN=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --package-id) PACKAGE_ID="${2:-}"; shift 2 ;;
        --network) NETWORK="${2:-}"; shift 2 ;;
        --portal-url) PORTAL_URL="${2:-}"; shift 2 ;;
        --agent-address) AGENT_ADDRESS="${2:-}"; shift 2 ;;
        --min-agent-gas-mist) MIN_AGENT_GAS_MIST="${2:-}"; shift 2 ;;
        --recommended-predeposit-mist) RECOMMENDED_PREDEPOSIT_MIST="${2:-}"; shift 2 ;;
        --force-new-agent) FORCE_NEW_AGENT=true; shift ;;
        --no-open) NO_OPEN=true; shift ;;
        -h|--help) usage; exit 0 ;;
        *) error "Unknown argument: $1"; usage; exit 1 ;;
    esac
done

if ! command -v sui >/dev/null 2>&1; then
    error "sui CLI not found. Install: https://docs.sui.io/guides/developer/getting-started/sui-install"
    exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
    error "jq not found. Install with brew/apt."
    exit 1
fi

if [[ -n "$PACKAGE_ID" ]] && ! is_sui_address "$PACKAGE_ID"; then
    error "Invalid package id: $PACKAGE_ID"
    exit 1
fi

if ! [[ "$MIN_AGENT_GAS_MIST" =~ ^[0-9]+$ ]] || ! [[ "$RECOMMENDED_PREDEPOSIT_MIST" =~ ^[0-9]+$ ]]; then
    error "mist values must be integers."
    exit 1
fi

info "Switching to network: $NETWORK"
sui client switch --env "$NETWORK" >/dev/null 2>&1 || warn "Cannot switch env automatically; continuing with current env."

OWNER_ADDRESS="$(sui client active-address 2>/dev/null | tr -d '[:space:]')"
if ! is_sui_address "$OWNER_ADDRESS"; then
    error "No active Sui address found. Run: sui client new-address ed25519"
    exit 1
fi

if [[ -n "$AGENT_ADDRESS" ]]; then
    if ! is_sui_address "$AGENT_ADDRESS"; then
        error "Invalid --agent-address: $AGENT_ADDRESS"
        exit 1
    fi
    info "Using provided agent address: $AGENT_ADDRESS"
elif [[ -f "$AGENT_ADDRESS_FILE" && "$FORCE_NEW_AGENT" == false ]]; then
    AGENT_ADDRESS="$(tr -d '[:space:]' < "$AGENT_ADDRESS_FILE")"
    if ! is_sui_address "$AGENT_ADDRESS"; then
        error "Corrupt $AGENT_ADDRESS_FILE. Use --force-new-agent."
        exit 1
    fi
    info "Using existing agent address: $AGENT_ADDRESS"
else
    info "Creating new agent address in local sui keystore..."
    NEW_ADDRESS_JSON="$(sui client new-address ed25519 --json)"
    AGENT_ADDRESS="$(echo "$NEW_ADDRESS_JSON" | jq -r '.address')"
    if ! is_sui_address "$AGENT_ADDRESS"; then
        error "Failed to parse new agent address."
        exit 1
    fi
    info "Created agent address: $AGENT_ADDRESS"
fi

echo "$AGENT_ADDRESS" > "$AGENT_ADDRESS_FILE"

cat > "$OWNER_HANDOFF_FILE" <<EOF
{
  "network": "$NETWORK",
  "packageId": "$PACKAGE_ID",
  "ownerAddress": "$OWNER_ADDRESS",
  "agentAddress": "$AGENT_ADDRESS",
  "portalUrl": "$PORTAL_URL",
  "minAgentGasMist": $MIN_AGENT_GAS_MIST,
  "recommendedPredepositMist": $RECOMMENDED_PREDEPOSIT_MIST,
  "createdAtMs": $(($(date +%s) * 1000))
}
EOF

success "Owner handoff context created."
echo "  File:          $OWNER_HANDOFF_FILE"
echo "  Package ID:    $PACKAGE_ID"
echo "  Owner Address: $OWNER_ADDRESS"
echo "  Agent Address: $AGENT_ADDRESS"
echo ""
echo "Ask owner to complete these actions:"
echo "1) Transfer gas to agent:"
echo "   sui client transfer-sui --to $AGENT_ADDRESS --amount $MIN_AGENT_GAS_MIST --gas-budget 5000000"
echo "2) Open portal and configure SafeFlow wallet/session cap:"
echo "   $PORTAL_URL"
echo "   - Suggested predeposit into SafeFlow wallet: $RECOMMENDED_PREDEPOSIT_MIST MIST"
echo "3) Return with walletId and sessionCapId."
echo "4) Run:"
echo "   ./save_owner_config.sh --wallet-id <WALLET_ID> --session-cap-id <SESSION_CAP_ID> --package-id $PACKAGE_ID"

if [[ "$NO_OPEN" == false ]]; then
    if [[ "$PORTAL_URL" == *"PLACEHOLDER"* ]]; then
        warn "Portal URL still placeholder; skip auto-open."
    elif command -v open >/dev/null 2>&1; then
        info "Opening portal with macOS open..."
        open "$PORTAL_URL" >/dev/null 2>&1 || warn "Failed to open portal URL."
    elif command -v xdg-open >/dev/null 2>&1; then
        info "Opening portal with xdg-open..."
        xdg-open "$PORTAL_URL" >/dev/null 2>&1 || warn "Failed to open portal URL."
    else
        warn "No open/xdg-open command found. Open URL manually: $PORTAL_URL"
    fi
fi
