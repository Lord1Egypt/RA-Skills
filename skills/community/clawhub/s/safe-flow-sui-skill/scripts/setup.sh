#!/usr/bin/env bash
# =============================================================================
# SafeFlow Setup Script
# Sets up a SafeFlow wallet and session cap using the official shared contract.
#
# Prerequisites:
#   - sui CLI installed and configured (https://docs.sui.io/references/cli)
#   - Active Sui address with gas funds (or testnet faucet access)
#
# Usage:
#   ./setup.sh [--force]
#
# Options:
#   --force   Recreate wallet and session cap even if config already exists
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/.safeflow-config.json"
AGENT_ADDRESS_FILE="$SCRIPT_DIR/.agent-address.txt"

# =============================================================================
# TODO: Fill in after deployment
# =============================================================================
SAFEFLOW_PACKAGE_ID="0xcc76747b518ea5d07255a26141fb5e0b81fcdd0dc1cc578a83f88adc003a6191"
SAFEFLOW_NETWORK="testnet"
# =============================================================================

SUI_COIN_TYPE="0x2::sui::SUI"

# Colors
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'

info()    { echo -e "${BLUE}[Setup]${NC} $*"; }
success() { echo -e "${GREEN}[Setup]${NC} $*"; }
warn()    { echo -e "${YELLOW}[Setup]${NC} $*"; }
error()   { echo -e "${RED}[Setup]${NC} $*" >&2; }

# --------------- Guard checks ---------------

if [[ "$SAFEFLOW_PACKAGE_ID" == *"TODO"* ]]; then
    error "SafeFlow Package ID is not configured yet."
    error "Edit setup.sh and fill in SAFEFLOW_PACKAGE_ID."
    exit 1
fi

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

FORCE=false
for arg in "$@"; do
    [[ "$arg" == "--force" ]] && FORCE=true
done

# --------------- Show existing config ---------------

if [[ -f "$CONFIG_FILE" ]] && [[ "$FORCE" == false ]]; then
    info "SafeFlow is already configured. Use --force to reconfigure."
    echo ""
    cat "$CONFIG_FILE" | jq .
    exit 0
fi

# --------------- Switch network ---------------

info "Switching to $SAFEFLOW_NETWORK..."
sui client switch --env "$SAFEFLOW_NETWORK" 2>/dev/null || true

# --------------- Get active address ---------------

info "Step 1: Get active address"
USER_ADDRESS=$(sui client active-address 2>/dev/null | tr -d '[:space:]')
if [[ -z "$USER_ADDRESS" ]]; then
    error "No active Sui address found."
    error "Create one with: sui client new-address ed25519"
    exit 1
fi
info "User address: $USER_ADDRESS"

# --------------- Check / fund balance ---------------

info "Step 2: Check balance"
BALANCE_RAW=$(sui client gas --json 2>/dev/null | jq '[.[].mistBalance] | add // 0')
info "Current balance: $(echo "scale=4; $BALANCE_RAW / 1000000000" | bc) SUI ($BALANCE_RAW MIST)"

MIN_BALANCE=500000000  # 0.5 SUI

if [[ "$BALANCE_RAW" -lt "$MIN_BALANCE" ]]; then
    if [[ "$SAFEFLOW_NETWORK" == "testnet" ]]; then
        info "Balance low, requesting from faucet..."
        sui client faucet --address "$USER_ADDRESS" || {
            warn "Faucet command failed. Trying HTTP faucet..."
            curl -sf -X POST https://faucet.testnet.sui.io/v1/gas \
                -H 'Content-Type: application/json' \
                -d "{\"FixedAmountRequest\":{\"recipient\":\"$USER_ADDRESS\"}}" > /dev/null || {
                error "Faucet request failed."
                error "Please fund manually: https://faucet.sui.io/?address=$USER_ADDRESS"
                exit 1
            }
        }
        info "Waiting for faucet confirmation..."
        sleep 5
        BALANCE_RAW=$(sui client gas --json 2>/dev/null | jq '[.[].mistBalance] | add // 0')
        if [[ "$BALANCE_RAW" -lt "$MIN_BALANCE" ]]; then
            error "Still insufficient balance after faucet."
            error "Please fund manually: https://faucet.sui.io/?address=$USER_ADDRESS"
            exit 1
        fi
        info "New balance: $(echo "scale=4; $BALANCE_RAW / 1000000000" | bc) SUI"
    else
        error "Insufficient balance ($BALANCE_RAW MIST). Please fund the wallet:"
        error "  $USER_ADDRESS"
        exit 1
    fi
fi

# --------------- Get or create agent address ---------------

info "Step 3: Agent address"
if [[ -f "$AGENT_ADDRESS_FILE" ]] && [[ "$FORCE" == false ]]; then
    AGENT_ADDRESS=$(cat "$AGENT_ADDRESS_FILE" | tr -d '[:space:]')
    info "Using existing agent address: $AGENT_ADDRESS"
else
    # Create a new dedicated address for the agent
    AGENT_ADDRESS_RAW=$(sui client new-address ed25519 --json 2>/dev/null)
    AGENT_ADDRESS=$(echo "$AGENT_ADDRESS_RAW" | jq -r '.address')
    echo "$AGENT_ADDRESS" > "$AGENT_ADDRESS_FILE"
    info "Created new agent address: $AGENT_ADDRESS"
    info "Agent key saved to keystore by sui CLI."
fi

# --------------- Create SafeFlow Wallet ---------------

info "Step 4: Creating SafeFlow Wallet..."
WALLET_OUTPUT=$(sui client call \
    --package "$SAFEFLOW_PACKAGE_ID" \
    --module wallet \
    --function create_wallet \
    --type-args "$SUI_COIN_TYPE" \
    --gas-budget 10000000 \
    --json 2>&1)

if echo "$WALLET_OUTPUT" | jq -e '.effects.status.status == "success"' &>/dev/null; then
    WALLET_ID=$(echo "$WALLET_OUTPUT" | jq -r '
        .events[]
        | select(.type | contains("WalletCreated"))
        | .parsedJson.wallet_id
    ')
    success "Wallet created: $WALLET_ID"
else
    error "Failed to create wallet."
    error "$WALLET_OUTPUT"
    exit 1
fi

# --------------- Create SessionCap ---------------

info "Step 5: Creating SessionCap for agent..."

# 30 days from now in milliseconds
EXPIRES_AT_MS=$(( ($(date +%s) + 30 * 24 * 3600) * 1000 ))
MAX_SPEND_PER_SEC=1000000000   # 1 SUI/sec
MAX_SPEND_TOTAL=10000000000    # 10 SUI total

SESSION_OUTPUT=$(sui client call \
    --package "$SAFEFLOW_PACKAGE_ID" \
    --module wallet \
    --function create_session_cap \
    --type-args "$SUI_COIN_TYPE" \
    --args "$WALLET_ID" "$AGENT_ADDRESS" "$MAX_SPEND_PER_SEC" "$MAX_SPEND_TOTAL" "$EXPIRES_AT_MS" "0x6" \
    --gas-budget 10000000 \
    --json 2>&1)

if echo "$SESSION_OUTPUT" | jq -e '.effects.status.status == "success"' &>/dev/null; then
    SESSION_CAP_ID=$(echo "$SESSION_OUTPUT" | jq -r '
        .events[]
        | select(.type | contains("SessionCapCreated"))
        | .parsedJson.cap_id
    ')
    success "SessionCap created: $SESSION_CAP_ID"
else
    error "Failed to create SessionCap."
    error "$SESSION_OUTPUT"
    exit 1
fi

# --------------- Save config ---------------

cat > "$CONFIG_FILE" <<EOF
{
  "packageId": "$SAFEFLOW_PACKAGE_ID",
  "walletId": "$WALLET_ID",
  "sessionCapId": "$SESSION_CAP_ID",
  "agentAddress": "$AGENT_ADDRESS",
  "userAddress": "$USER_ADDRESS",
  "network": "$SAFEFLOW_NETWORK"
}
EOF

echo ""
success "Setup complete!"
echo ""
echo "  Package ID:    $SAFEFLOW_PACKAGE_ID"
echo "  Wallet ID:     $WALLET_ID"
echo "  SessionCap ID: $SESSION_CAP_ID"
echo "  Agent Address: $AGENT_ADDRESS"
echo "  User Address:  $USER_ADDRESS"
echo ""
info "Next: deposit SUI into your SafeFlow wallet to fund payments:"
echo "  sui client transfer-sui --to $WALLET_ID --amount 1000000000 --gas-budget 10000000"
echo ""
info "Then make payments with:"
echo "  ./execute_payment.sh --recipient <addr> --amount <mist>"
