#!/usr/bin/env bash
# =============================================================================
# SafeFlow Execute Payment Script
# Executes a streaming payment using the SafeFlow shared contract.
#
# Prerequisites:
#   - sui CLI installed and configured (https://docs.sui.io/references/cli)
#   - Run ./setup.sh first to create wallet and session cap
#
# Usage:
#   ./execute_payment.sh --recipient <SUI_ADDRESS> --amount <MIST>
#
# Parameters:
#   --recipient   Destination Sui address
#   --amount      Amount in MIST (1 SUI = 1,000,000,000 MIST)
#   --blob-id     Optional Walrus blob ID for audit trail (default: empty)
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/.safeflow-config.json"

# Colors
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'

info()    { echo -e "${BLUE}[SafeFlow]${NC} $*"; }
success() { echo -e "${GREEN}[SafeFlow]${NC} $*"; }
warn()    { echo -e "${YELLOW}[SafeFlow]${NC} $*"; }
error()   { echo -e "${RED}[SafeFlow]${NC} $*" >&2; }

# --------------- Parse arguments ---------------

RECIPIENT=""
AMOUNT=""
BLOB_ID=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --recipient) RECIPIENT="$2"; shift 2 ;;
        --amount)    AMOUNT="$2";    shift 2 ;;
        --blob-id)   BLOB_ID="$2";   shift 2 ;;
        *) error "Unknown argument: $1"; exit 1 ;;
    esac
done

if [[ -z "$RECIPIENT" || -z "$AMOUNT" ]]; then
    error "Missing required arguments."
    echo "Usage: ./execute_payment.sh --recipient <SUI_ADDRESS> --amount <MIST>"
    echo ""
    echo "Run ./setup.sh first if not yet configured."
    exit 1
fi

# Validate amount is a positive integer
if ! [[ "$AMOUNT" =~ ^[1-9][0-9]*$ ]]; then
    error "Invalid amount '$AMOUNT'. Must be a positive integer in MIST."
    echo "  1 SUI = 1,000,000,000 MIST"
    exit 1
fi

# --------------- Guard checks ---------------

if ! command -v sui &>/dev/null; then
    error "sui CLI not found."
    error "Install it from: https://docs.sui.io/guides/developer/getting-started/sui-install"
    exit 1
fi

if ! command -v jq &>/dev/null; then
    error "jq not found."
    error "Install it: brew install jq  (macOS) or  apt install jq  (Linux)"
    exit 1
fi

if [[ ! -f "$CONFIG_FILE" ]]; then
    error "SafeFlow not configured. Config not found: $CONFIG_FILE"
    error "Run ./setup.sh first."
    exit 1
fi

# --------------- Load config ---------------

PACKAGE_ID=$(jq -r '.packageId' "$CONFIG_FILE")
WALLET_ID=$(jq -r '.walletId' "$CONFIG_FILE")
SESSION_CAP_ID=$(jq -r '.sessionCapId' "$CONFIG_FILE")
AGENT_ADDRESS=$(jq -r '.agentAddress' "$CONFIG_FILE")
NETWORK=$(jq -r '.network' "$CONFIG_FILE")

info "Network:   $NETWORK"
info "Agent:     $AGENT_ADDRESS"
info "Wallet:    $WALLET_ID"
info "Paying $(echo "scale=4; $AMOUNT / 1000000000" | bc) SUI ($AMOUNT MIST) to $RECIPIENT..."

# --------------- Switch to agent address ---------------

sui client switch --address "$AGENT_ADDRESS" 2>/dev/null || {
    error "Failed to switch to agent address: $AGENT_ADDRESS"
    error "The agent address must be in your sui keystore."
    error "Re-run ./setup.sh --force to regenerate."
    exit 1
}

# --------------- Execute payment ---------------

RESULT=$(sui client call \
    --package "$PACKAGE_ID" \
    --module wallet \
    --function execute_payment \
    --type-args "0x2::sui::SUI" \
    --args "$WALLET_ID" "$SESSION_CAP_ID" "$AMOUNT" "$RECIPIENT" "${BLOB_ID:-}" "0x6" \
    --gas-budget 10000000 \
    --json 2>&1)

if echo "$RESULT" | jq -e '.effects.status.status == "success"' &>/dev/null; then
    DIGEST=$(echo "$RESULT" | jq -r '.digest')
    success "Payment executed successfully!"
    echo ""
    echo "  Digest:   $DIGEST"
    echo "  Explorer: https://suiscan.xyz/$NETWORK/tx/$DIGEST"
else
    error "Payment failed."
    STATUS=$(echo "$RESULT" | jq -r '.effects.status // empty' 2>/dev/null || echo "")

    # Provide actionable hints based on error patterns
    if echo "$RESULT" | grep -qi "insufficient\|balance\|coin"; then
        error "Hint: The SafeFlow wallet has insufficient SUI balance."
        error "  Fund the wallet: sui client transfer-sui --to $WALLET_ID --amount 1000000000 --gas-budget 10000000"
    elif echo "$RESULT" | grep -qi "ENotOwner\|unauthorized\|permission\|session"; then
        error "Hint: Agent is not authorized or SessionCap has expired."
        error "  Re-run: ./setup.sh --force"
    elif echo "$RESULT" | grep -qi "not found\|deleted\|object"; then
        error "Hint: Wallet or SessionCap object not found. It may have been deleted."
        error "  Re-run: ./setup.sh --force"
    elif echo "$RESULT" | grep -qi "gas\|budget"; then
        error "Hint: Insufficient gas. The agent address needs SUI for gas fees."
        CURRENT_ADDR=$(sui client active-address 2>/dev/null || echo "unknown")
        error "  Fund the agent: sui client transfer-sui --to $AGENT_ADDRESS --amount 500000000 --gas-budget 10000000"
    fi

    echo ""
    error "Full output: $RESULT"
    exit 1
fi
