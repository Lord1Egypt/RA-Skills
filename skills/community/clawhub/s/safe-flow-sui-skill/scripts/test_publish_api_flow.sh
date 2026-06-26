#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
SKILL_CONFIG="$SCRIPT_DIR/.safeflow-config.json"
AGENT_SCRIPTS_DIR="$REPO_ROOT/agent_scripts"

DEFAULT_PUBLISH_API_BASE_URL="https://producer.safeflow.space"
DEFAULT_POLL_MS="3000"
DEFAULT_TTL_SEC="600"
DEFAULT_AMOUNT_MIST="1000000"
DEFAULT_REASON="SafeFlow skill publish-api test"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
info()    { echo -e "${BLUE}[publish-test]${NC} $*"; }
success() { echo -e "${GREEN}[publish-test]${NC} $*"; }
warn()    { echo -e "${YELLOW}[publish-test]${NC} $*"; }
error()   { echo -e "${RED}[publish-test]${NC} $*" >&2; }

is_sui_address() {
    [[ "$1" =~ ^0x[0-9a-fA-F]{64}$ ]]
}

usage() {
    cat <<'EOF'
Usage:
  ./test_publish_api_flow.sh --publish-api-base-url <url> --recipient <address> [options]

Required:
  --publish-api-base-url <url>     Publish/Producer API URL
  --recipient <address>            Recipient address for test payment

Optional:
  --agent-address <address>        Agent address override
  --wallet-id <id>                 Wallet id override
  --session-cap-id <id>            Session cap id override
  --amount-mist <n>                Amount in MIST (default: 1000000)
  --reason <text>                  Intent reason
  --order-id <text>                Merchant order id (default: skill_<timestamp>)
  --ttl-sec <n>                    Intent TTL in seconds (default: 600)
  --poll-ms <n>                    Runner poll interval ms (default: 3000)
  --api-key <key>                  Optional x-api-key for write routes
  -h, --help                       Show help
EOF
}

PUBLISH_API_BASE_URL="$DEFAULT_PUBLISH_API_BASE_URL"
RECIPIENT=""
AGENT_ADDRESS=""
WALLET_ID=""
SESSION_CAP_ID=""
AMOUNT_MIST="$DEFAULT_AMOUNT_MIST"
REASON="$DEFAULT_REASON"
ORDER_ID="skill_$(date +%s)"
TTL_SEC="$DEFAULT_TTL_SEC"
POLL_MS="$DEFAULT_POLL_MS"
API_KEY=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --publish-api-base-url) PUBLISH_API_BASE_URL="${2:-}"; shift 2 ;;
        --recipient) RECIPIENT="${2:-}"; shift 2 ;;
        --agent-address) AGENT_ADDRESS="${2:-}"; shift 2 ;;
        --wallet-id) WALLET_ID="${2:-}"; shift 2 ;;
        --session-cap-id) SESSION_CAP_ID="${2:-}"; shift 2 ;;
        --amount-mist) AMOUNT_MIST="${2:-}"; shift 2 ;;
        --reason) REASON="${2:-}"; shift 2 ;;
        --order-id) ORDER_ID="${2:-}"; shift 2 ;;
        --ttl-sec) TTL_SEC="${2:-}"; shift 2 ;;
        --poll-ms) POLL_MS="${2:-}"; shift 2 ;;
        --api-key) API_KEY="${2:-}"; shift 2 ;;
        -h|--help) usage; exit 0 ;;
        *) error "Unknown argument: $1"; usage; exit 1 ;;
    esac
done

if [[ -z "$RECIPIENT" ]]; then
    error "--recipient is required."
    usage
    exit 1
fi

if ! is_sui_address "$RECIPIENT"; then
    error "Invalid recipient: $RECIPIENT"
    exit 1
fi

if ! [[ "$AMOUNT_MIST" =~ ^[1-9][0-9]*$ ]]; then
    error "--amount-mist must be a positive integer."
    exit 1
fi

if ! [[ "$TTL_SEC" =~ ^[1-9][0-9]*$ ]]; then
    error "--ttl-sec must be a positive integer."
    exit 1
fi

if ! [[ "$POLL_MS" =~ ^[1-9][0-9]*$ ]]; then
    error "--poll-ms must be a positive integer."
    exit 1
fi

if ! command -v curl >/dev/null 2>&1; then
    error "curl not found."
    exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
    error "jq not found."
    exit 1
fi

if ! command -v npx >/dev/null 2>&1; then
    error "npx not found."
    exit 1
fi

if [[ ! -d "$AGENT_SCRIPTS_DIR" ]]; then
    error "agent_scripts directory not found: $AGENT_SCRIPTS_DIR"
    exit 1
fi

if [[ -f "$SKILL_CONFIG" ]]; then
    [[ -z "$AGENT_ADDRESS" ]] && AGENT_ADDRESS="$(jq -r '.agentAddress // empty' "$SKILL_CONFIG")"
    [[ -z "$WALLET_ID" ]] && WALLET_ID="$(jq -r '.walletId // empty' "$SKILL_CONFIG")"
    [[ -z "$SESSION_CAP_ID" ]] && SESSION_CAP_ID="$(jq -r '.sessionCapId // empty' "$SKILL_CONFIG")"
fi

if ! is_sui_address "$AGENT_ADDRESS" || ! is_sui_address "$WALLET_ID" || ! is_sui_address "$SESSION_CAP_ID"; then
    error "Need valid agentAddress/walletId/sessionCapId. Run save_owner_config.sh first or pass explicit args."
    exit 1
fi

BASE="${PUBLISH_API_BASE_URL%/}"

info "Checking Publish API health..."
curl -fsS "$BASE/health" | jq .

if [[ -n "$API_KEY" ]]; then
    CREATE_OUTPUT="$(
        cd "$AGENT_SCRIPTS_DIR"
        PRODUCER_API_BASE_URL="$BASE" PRODUCER_API_KEY="$API_KEY" \
        npx tsx create_intent.ts \
            --agent-address "$AGENT_ADDRESS" \
            --wallet-id "$WALLET_ID" \
            --session-cap-id "$SESSION_CAP_ID" \
            --recipient "$RECIPIENT" \
            --amount-mist "$AMOUNT_MIST" \
            --reason "$REASON" \
            --ttl-sec "$TTL_SEC" \
            --order-id "$ORDER_ID"
    )"
else
    CREATE_OUTPUT="$(
        cd "$AGENT_SCRIPTS_DIR"
        PRODUCER_API_BASE_URL="$BASE" \
        npx tsx create_intent.ts \
            --agent-address "$AGENT_ADDRESS" \
            --wallet-id "$WALLET_ID" \
            --session-cap-id "$SESSION_CAP_ID" \
            --recipient "$RECIPIENT" \
            --amount-mist "$AMOUNT_MIST" \
            --reason "$REASON" \
            --ttl-sec "$TTL_SEC" \
            --order-id "$ORDER_ID"
    )"
fi

INTENT_ID="$(echo "$CREATE_OUTPUT" | jq -r '.intent.intentId // empty')"
if [[ -z "$INTENT_ID" ]]; then
    error "Failed to parse intentId from create_intent.ts output."
    echo "$CREATE_OUTPUT"
    exit 1
fi

success "Intent created: $INTENT_ID"
echo "$CREATE_OUTPUT" | jq .

info "Running one-shot consumer (e2e_runner.ts --once)..."
if [[ -n "$API_KEY" ]]; then
    (
        cd "$AGENT_SCRIPTS_DIR"
        PRODUCER_API_BASE_URL="$BASE" PRODUCER_API_KEY="$API_KEY" \
        npx tsx e2e_runner.ts --once --poll-ms "$POLL_MS"
    )
else
    (
        cd "$AGENT_SCRIPTS_DIR"
        PRODUCER_API_BASE_URL="$BASE" \
        npx tsx e2e_runner.ts --once --poll-ms "$POLL_MS"
    )
fi

FINAL_JSON="$(curl -fsS "$BASE/v1/intents/$INTENT_ID")"
FINAL_STATUS="$(echo "$FINAL_JSON" | jq -r '.intent.status // empty')"
TX_DIGEST="$(echo "$FINAL_JSON" | jq -r '.intent.txDigest // empty')"
WALRUS_BLOB_ID="$(echo "$FINAL_JSON" | jq -r '.intent.walrusBlobId // empty')"

success "Publish API test flow complete."
echo "  Intent ID:      $INTENT_ID"
echo "  Final status:   $FINAL_STATUS"
echo "  Tx digest:      $TX_DIGEST"
echo "  Walrus blob id: $WALRUS_BLOB_ID"

if [[ "$WALRUS_BLOB_ID" == fallback:* ]]; then
    warn "Walrus upload degraded to fallback blob id. Check WALRUS_* env and endpoint connectivity."
fi

echo ""
echo "$FINAL_JSON" | jq .
