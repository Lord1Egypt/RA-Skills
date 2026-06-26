#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/.safeflow-config.json"
AGENT_ADDRESS_FILE="$SCRIPT_DIR/.agent-address.txt"
ENV_FILE="$SCRIPT_DIR/.safeflow-owner.env"

DEFAULT_PACKAGE_ID="0xcc76747b518ea5d07255a26141fb5e0b81fcdd0dc1cc578a83f88adc003a6191"
DEFAULT_NETWORK="testnet"
DEFAULT_PRODUCER_BASE_URL="https://producer.safeflow.space"
DEFAULT_PUBLISH_API_URL="https://producer.safeflow.space"
DEFAULT_WALRUS_PUBLISHER="https://publisher.walrus-testnet.walrus.space"
DEFAULT_WALRUS_AGGREGATOR="https://aggregator.walrus-testnet.walrus.space"
DEFAULT_WALRUS_EPOCHS="5"
DEFAULT_WALRUS_DEGRADE="true"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
info()    { echo -e "${BLUE}[owner-config]${NC} $*"; }
success() { echo -e "${GREEN}[owner-config]${NC} $*"; }
warn()    { echo -e "${YELLOW}[owner-config]${NC} $*"; }
error()   { echo -e "${RED}[owner-config]${NC} $*" >&2; }

is_sui_address() {
    [[ "$1" =~ ^0x[0-9a-fA-F]{64}$ ]]
}

usage() {
    cat <<'EOF'
Usage:
  ./save_owner_config.sh --wallet-id <id> --session-cap-id <id> [options]

Required:
  --wallet-id <id>                 SafeFlow wallet object id from owner
  --session-cap-id <id>            SessionCap object id from owner

Options:
  --package-id <id>                SafeFlow package id (default: shared package)
  --agent-address <address>        Agent address (default: .agent-address.txt)
  --network <name>                 Sui env (default: testnet)
  --producer-api-base-url <url>    Producer/Publish API base URL
  --publish-api-base-url <url>     Publish API base URL placeholder for tests
  --walrus-publisher <url>         Walrus publisher endpoint
  --walrus-aggregator <url>        Walrus aggregator endpoint
  --walrus-epochs <n>              Walrus epochs
  --walrus-degrade <true|false>    Allow fallback blob ids on upload failure
  --sync-sql                       Sync package id to SQL after saving
  --sql-driver <sqlite|postgres>   SQL driver for sync (default: sqlite)
  --sqlite-db <path>               SQLite path for sync
  --postgres-dsn <dsn>             Postgres DSN for sync
  -h, --help                       Show help
EOF
}

WALLET_ID=""
SESSION_CAP_ID=""
PACKAGE_ID="$DEFAULT_PACKAGE_ID"
AGENT_ADDRESS=""
NETWORK="$DEFAULT_NETWORK"
PRODUCER_API_BASE_URL="$DEFAULT_PRODUCER_BASE_URL"
PUBLISH_API_BASE_URL="$DEFAULT_PUBLISH_API_URL"
WALRUS_PUBLISHER_URL="$DEFAULT_WALRUS_PUBLISHER"
WALRUS_AGGREGATOR_URL="$DEFAULT_WALRUS_AGGREGATOR"
WALRUS_EPOCHS="$DEFAULT_WALRUS_EPOCHS"
WALRUS_DEGRADE_ON_UPLOAD_FAILURE="$DEFAULT_WALRUS_DEGRADE"

SYNC_SQL=false
SQL_DRIVER="sqlite"
SQLITE_DB="$SCRIPT_DIR/.safeflow-runtime.db"
POSTGRES_DSN=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --wallet-id) WALLET_ID="${2:-}"; shift 2 ;;
        --session-cap-id) SESSION_CAP_ID="${2:-}"; shift 2 ;;
        --package-id) PACKAGE_ID="${2:-}"; shift 2 ;;
        --agent-address) AGENT_ADDRESS="${2:-}"; shift 2 ;;
        --network) NETWORK="${2:-}"; shift 2 ;;
        --producer-api-base-url) PRODUCER_API_BASE_URL="${2:-}"; shift 2 ;;
        --publish-api-base-url) PUBLISH_API_BASE_URL="${2:-}"; shift 2 ;;
        --walrus-publisher) WALRUS_PUBLISHER_URL="${2:-}"; shift 2 ;;
        --walrus-aggregator) WALRUS_AGGREGATOR_URL="${2:-}"; shift 2 ;;
        --walrus-epochs) WALRUS_EPOCHS="${2:-}"; shift 2 ;;
        --walrus-degrade) WALRUS_DEGRADE_ON_UPLOAD_FAILURE="${2:-}"; shift 2 ;;
        --sync-sql) SYNC_SQL=true; shift ;;
        --sql-driver) SQL_DRIVER="${2:-}"; shift 2 ;;
        --sqlite-db) SQLITE_DB="${2:-}"; shift 2 ;;
        --postgres-dsn) POSTGRES_DSN="${2:-}"; shift 2 ;;
        -h|--help) usage; exit 0 ;;
        *) error "Unknown argument: $1"; usage; exit 1 ;;
    esac
done

if ! command -v jq >/dev/null 2>&1; then
    error "jq not found."
    exit 1
fi

if [[ -z "$WALLET_ID" || -z "$SESSION_CAP_ID" ]]; then
    error "--wallet-id and --session-cap-id are required."
    usage
    exit 1
fi

if ! is_sui_address "$WALLET_ID"; then
    error "Invalid wallet id: $WALLET_ID"
    exit 1
fi

if ! is_sui_address "$SESSION_CAP_ID"; then
    error "Invalid session cap id: $SESSION_CAP_ID"
    exit 1
fi

if ! is_sui_address "$PACKAGE_ID"; then
    error "Invalid package id: $PACKAGE_ID"
    exit 1
fi

if [[ -z "$AGENT_ADDRESS" ]]; then
    if [[ -f "$AGENT_ADDRESS_FILE" ]]; then
        AGENT_ADDRESS="$(tr -d '[:space:]' < "$AGENT_ADDRESS_FILE")"
    elif [[ -f "$CONFIG_FILE" ]]; then
        AGENT_ADDRESS="$(jq -r '.agentAddress // empty' "$CONFIG_FILE")"
    fi
fi

if ! is_sui_address "$AGENT_ADDRESS"; then
    error "Missing valid agent address. Provide --agent-address or run bootstrap_owner_handoff.sh first."
    exit 1
fi

USER_ADDRESS=""
if command -v sui >/dev/null 2>&1; then
    USER_ADDRESS="$(sui client active-address 2>/dev/null | tr -d '[:space:]' || true)"
fi
if ! is_sui_address "$USER_ADDRESS"; then
    USER_ADDRESS=""
fi

cat > "$CONFIG_FILE" <<EOF
{
  "packageId": "$PACKAGE_ID",
  "walletId": "$WALLET_ID",
  "sessionCapId": "$SESSION_CAP_ID",
  "agentAddress": "$AGENT_ADDRESS",
  "userAddress": "$USER_ADDRESS",
  "network": "$NETWORK"
}
EOF

cat > "$ENV_FILE" <<EOF
# Generated by save_owner_config.sh
PACKAGE_ID=$PACKAGE_ID
WALLET_ID=$WALLET_ID
SESSION_CAP_ID=$SESSION_CAP_ID
AGENT_ADDRESS=$AGENT_ADDRESS
NETWORK=$NETWORK

PRODUCER_API_BASE_URL=$PRODUCER_API_BASE_URL
PUBLISH_API_BASE_URL=$PUBLISH_API_BASE_URL

WALRUS_PUBLISHER_URL=$WALRUS_PUBLISHER_URL
WALRUS_AGGREGATOR_URL=$WALRUS_AGGREGATOR_URL
WALRUS_EPOCHS=$WALRUS_EPOCHS
WALRUS_DEGRADE_ON_UPLOAD_FAILURE=$WALRUS_DEGRADE_ON_UPLOAD_FAILURE
EOF

success "SafeFlow owner-provided config saved."
echo "  Config file: $CONFIG_FILE"
echo "  Env file:    $ENV_FILE"
echo "  Package ID:  $PACKAGE_ID"
echo "  Wallet ID:   $WALLET_ID"
echo "  SessionCap:  $SESSION_CAP_ID"
echo "  Agent:       $AGENT_ADDRESS"
echo ""
echo "Next:"
echo "  ./execute_payment.sh --recipient <RECIPIENT_ADDRESS> --amount 1000000"
echo "  ./test_publish_api_flow.sh --publish-api-base-url <API_URL> --recipient <RECIPIENT_ADDRESS>"

if [[ "$SYNC_SQL" == true ]]; then
    info "Syncing package id to SQL..."
    "$SCRIPT_DIR/sync_package_id_to_sql.sh" \
        --package-id "$PACKAGE_ID" \
        --driver "$SQL_DRIVER" \
        --sqlite-db "$SQLITE_DB" \
        --postgres-dsn "$POSTGRES_DSN"
fi
