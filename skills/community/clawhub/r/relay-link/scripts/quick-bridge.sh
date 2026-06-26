#!/bin/bash
# Quick Bridge script for Relay Link API with Automated Execution
# Usage: ./quick-bridge.sh <amount> <origin_chain> <dest_chain> [origin_currency] [dest_currency] [recipient_addr]

# Load Configuration from config.env (Standard location)
ENV_FILE="$HOME/.openclaw/config.env"
if [ -f "$ENV_FILE" ]; then
  export EVM_PRIVATE_KEY=$(grep "^EVM_PRIVATE_KEY=" "$ENV_FILE" | head -n 1 | cut -d'=' -f2 | tr -d '"' | tr -d "'")
  export EVM_ADDRESS=$(grep "^EVM_ADDRESS=" "$ENV_FILE" | head -n 1 | cut -d'=' -f2 | tr -d '"' | tr -d "'")
  export SOLANA_ADDRESS=$(grep "^SOLANA_ADDRESS=" "$ENV_FILE" | head -n 1 | cut -d'=' -f2 | tr -d '"' | tr -d "'")
fi

# Fallback to internal variables if not loaded (for better error messages)
USER_ADDR=${EVM_ADDRESS}
DEFAULT_RECIPIENT=${SOLANA_ADDRESS}
RPC_URL_AVAX="https://api.avax.network/ext/bc/C/rpc"

if [ -z "$USER_ADDR" ]; then echo "❌ Error: EVM_ADDRESS not found in $ENV_FILE"; exit 1; fi
if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then echo "Usage: $0 <amount> <origin_chain> <dest_chain>"; exit 1; fi

AMOUNT=$1; ORIGIN=$2; DEST=$3
ORIGIN_CURR=${4:-"0x0000000000000000000000000000000000000000"}
DEST_CURR=${5:-"0x0000000000000000000000000000000000000000"}
DEST_ADDR=${6:-$DEFAULT_RECIPIENT}

# Validate recipient for Solana
if [ -z "$DEST_ADDR" ] && [[ "$DEST" == "sol" || "$DEST" == "solana" ]]; then
  echo "❌ Error: SOLANA_ADDRESS not found in $ENV_FILE and no recipient provided."
  exit 1
fi

map_chain() {
  case $(echo "$1" | tr '[:upper:]' '[:lower:]') in
    abstract) echo 2741 ;;
    ancient8) echo 888888888 ;;
    animechain) echo 69000 ;;
    apechain|ape) echo 33139 ;;
    arbitrum|arb) echo 42161 ;;
    arbitrum-nova) echo 42170 ;;
    arena-z) echo 7897 ;;
    avalanche|avax) echo 43114 ;;
    b3) echo 8333 ;;
    base) echo 8453 ;;
    berachain|bera) echo 80094 ;;
    bitcoin|btc) echo 8253038 ;;
    blast) echo 81457 ;;
    bnb|bsc) echo 56 ;;
    bob) echo 60808 ;;
    boba) echo 288 ;;
    celo) echo 42220 ;;
    corn) echo 21000000 ;;
    cronos) echo 25 ;;
    cyber) echo 7560 ;;
    degen) echo 666666666 ;;
    doma) echo 97477 ;;
    eclipse) echo 9286185 ;;
    ethereal) echo 5064014 ;;
    ethereum|eth) echo 1 ;;
    flow) echo 747 ;;
    gnosis) echo 100 ;;
    gunz) echo 43419 ;;
    hemi) echo 43111 ;;
    hyperevm) echo 999 ;;
    hyperliquid|hl) echo 1337 ;;
    ink) echo 57073 ;;
    katana) echo 747474 ;;
    lighter) echo 3586256 ;;
    linea) echo 59144 ;;
    lisk) echo 1135 ;;
    manta) echo 169 ;;
    mantle) echo 5000 ;;
    megaeth) echo 4326 ;;
    metis) echo 1088 ;;
    mode) echo 34443 ;;
    monad) echo 143 ;;
    morph) echo 2818 ;;
    mythos) echo 42018 ;;
    optimism|op) echo 10 ;;
    perennial) echo 1424 ;;
    plasma) echo 9745 ;;
    plume) echo 98866 ;;
    polygon|poly) echo 137 ;;
    rari) echo 1380012617 ;;
    redstone) echo 690 ;;
    ronin) echo 2020 ;;
    scroll) echo 534352 ;;
    sei) echo 1329 ;;
    shape) echo 360 ;;
    solana|sol) echo 792703809 ;;
    somnia) echo 5031 ;;
    soneium) echo 1868 ;;
    sonic) echo 146 ;;
    soon) echo 9286186 ;;
    stable) echo 988 ;;
    story) echo 1514 ;;
    superposition) echo 55244 ;;
    superseed) echo 5330 ;;
    swell) echo 1923 ;;
    syndicate) echo 510003 ;;
    taiko) echo 167000 ;;
    tempo) echo 4217 ;;
    tron) echo 728126428 ;;
    unichain) echo 130 ;;
    world) echo 480 ;;
    zero) echo 543210 ;;
    zircuit) echo 48900 ;;
    zksync) echo 324 ;;
    zora) echo 7777777 ;;
    base-sepolia) echo 84532 ;;
    sepolia) echo 11155111 ;;
    tempo-testnet) echo 42431 ;;
    *) echo $1 ;;
  esac
}

ORIGIN_ID=$(map_chain "$ORIGIN")
DEST_ID=$(map_chain "$DEST")

# Currency mapping for native tokens
if [ "$DEST_ID" == "792703809" ] && [ "$DEST_CURR" == "0x0000000000000000000000000000000000000000" ]; then
  DEST_CURR="11111111111111111111111111111111"
fi

clear
echo "╔════════════════════════════════════════════════════════╗"
echo "║          🔀 BRIDGE TRANSACTION REQUEST               ║"
echo "╠════════════════════════════════════════════════════════╣"
echo "║ From: $USER_ADDR ║"
echo "║ To:   $DEST_ADDR ║"
echo "║ Route: $ORIGIN ($ORIGIN_ID) → $DEST ($DEST_ID)           ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "⏳ Getting quote from Relay..."

CONVERTED_AMOUNT=$(echo "$AMOUNT * 10^18" | bc | cut -d'.' -f1)

QUOTE=$(curl -s -X POST "https://api.relay.link/quote/v2" \
     -H "Content-Type: application/json" \
     -d "{
       \"user\": \"$USER_ADDR\",
       \"originChainId\": $ORIGIN_ID,
       \"destinationChainId\": $DEST_ID,
       \"originCurrency\": \"$ORIGIN_CURR\",
       \"destinationCurrency\": \"$DEST_CURR\",
       \"recipient\": \"$DEST_ADDR\",
       \"amount\": \"$CONVERTED_AMOUNT\",
       \"tradeType\": \"EXACT_INPUT\"
     }")

if [ "$(echo "$QUOTE" | jq -r '.message')" != "null" ] && [ "$(echo "$QUOTE" | jq -r '.message')" != "" ]; then
    echo "❌ Error getting quote: $(echo "$QUOTE" | jq -r '.message')"
    exit 1
fi

echo "✅ Quote received!"
echo ""
echo "┌────────────────────────────────────────────┐"
echo "│ 📊 QUOTE DETAILS"
echo "├────────────────────────────────────────────┤"
RECEIVE_AMOUNT=$(echo "$QUOTE" | jq -r '.details.currencyOut.amountFormatted')
RECEIVE_SYMBOL=$(echo "$QUOTE" | jq -r '.details.currencyOut.currency.symbol')
echo "│ You Send:    $AMOUNT $(echo "$ORIGIN" | tr '[:lower:]' '[:upper:]')                      │"
echo "│ You Receive: $RECEIVE_AMOUNT $RECEIVE_SYMBOL              │"
echo "│ Est. Time:   ~1 min                        │"
echo "└────────────────────────────────────────────┘"

if [ -z "$EVM_PRIVATE_KEY" ]; then
    echo "❌ EVM_PRIVATE_KEY not found in $ENV_FILE. Showing raw steps for manual execution:"
    echo "$QUOTE" | jq '.steps'
    exit 0
fi

read -p "Do you want to sign and send this transaction now? (yes/no): " CONFIRM

if [ "$CONFIRM" == "yes" ]; then
    echo "🚀 Sending transaction..."
    TX_TO=$(echo "$QUOTE" | jq -r '.steps[0].items[0].data.to')
    TX_VALUE=$(echo "$QUOTE" | jq -r '.steps[0].items[0].data.value')
    TX_DATA=$(echo "$QUOTE" | jq -r '.steps[0].items[0].data.data')
    
    # Use environment variable for private key instead of CLI arg for security
    export ETH_PRIVATE_KEY="$EVM_PRIVATE_KEY"
    RESULT=$(cast send "$TX_TO" "$TX_DATA" --value "$TX_VALUE" --rpc-url "$RPC_URL_AVAX" 2>&1)
    
    if [[ $RESULT == *"transactionHash"* ]]; then
        TX_HASH=$(echo "$RESULT" | grep "transactionHash" | awk '{print $2}')
        echo "✅ Transaction Sent!"
        echo "🔗 Hash: $TX_HASH"
        echo ""
        echo "Tracking status in 10 seconds..."
        sleep 10
        "$(dirname "$0")/get-status.sh" "$TX_HASH" "$ORIGIN_ID"
    else
        echo "❌ Execution Failed:"
        echo "$RESULT"
    fi
else
    echo "Cancelled."
fi
