#!/bin/bash

# Token Research Data Fetcher
# Usage: ./fetch_token_data.sh <mode> <token_address> <chain>
# Mode: shallow | deep
# Chain: ethereum | base | solana | bsc | arbitrum

set -e

# Configuration
MODE=${1:-shallow}
TOKEN_ADDRESS=${2}
CHAIN=${3:-ethereum}

# Validate inputs
if [ -z "$TOKEN_ADDRESS" ]; then
    echo "❌ Error: Token address required"
    echo "Usage: $0 <mode> <token_address> <chain>"
    echo "Example: $0 shallow 0x6982508145454ce325ddbe47a25d4ec3d2311933 ethereum"
    exit 1
fi

# Chain ID mapping
declare -A CHAIN_IDS
CHAIN_IDS["ethereum"]="1"
CHAIN_IDS["base"]="8453"
CHAIN_IDS["bsc"]="56" 
CHAIN_IDS["arbitrum"]="42161"
CHAIN_IDS["solana"]="solana"

CHAIN_ID=${CHAIN_IDS[$CHAIN]}
if [ -z "$CHAIN_ID" ]; then
    echo "❌ Unsupported chain: $CHAIN"
    echo "Supported: ethereum, base, bsc, arbitrum, solana"
    exit 1
fi

# Output directory
OUTPUT_DIR="research_$(date +%Y%m%d_%H%M%S)_${TOKEN_ADDRESS:0:8}"
mkdir -p "$OUTPUT_DIR"

echo "🔍 Starting $MODE research for $TOKEN_ADDRESS on $CHAIN"
echo "📁 Results will be saved to: $OUTPUT_DIR"

# Function to fetch with error handling
fetch_data() {
    local url="$1"
    local output_file="$2"
    local description="$3"
    
    echo "📥 Fetching $description..."
    if curl -s -f "$url" > "$output_file" 2>/dev/null; then
        echo "✅ $description saved to $output_file"
    else
        echo "❌ Failed to fetch $description"
        echo "null" > "$output_file"
    fi
}

# 1. DexScreener Data
echo -e "\n🚀 === DEXSCREENER DATA ==="
if [ "$CHAIN" = "solana" ]; then
    DEXSCREENER_URL="https://api.dexscreener.com/latest/dex/tokens/solana/$TOKEN_ADDRESS"
else
    DEXSCREENER_URL="https://api.dexscreener.com/latest/dex/tokens/$CHAIN/$TOKEN_ADDRESS"
fi

fetch_data "$DEXSCREENER_URL" "$OUTPUT_DIR/dexscreener.json" "DexScreener token data"

# 2. GoPlus Security Data
echo -e "\n🛡️ === SECURITY ANALYSIS ==="
if [ "$CHAIN" = "solana" ]; then
    GOPLUS_URL="https://api.gopluslabs.io/api/v2/token_security/$TOKEN_ADDRESS?chain_id=solana"
else
    GOPLUS_URL="https://api.gopluslabs.io/api/v1/token_security/$CHAIN_ID?contract_addresses=$TOKEN_ADDRESS"
fi

fetch_data "$GOPLUS_URL" "$OUTPUT_DIR/security.json" "GoPlus security analysis"

# 3. Token Holders (EVM only)
if [ "$CHAIN" != "solana" ]; then
    echo -e "\n👥 === HOLDER ANALYSIS ==="
    
    # Determine the correct API endpoint
    case $CHAIN in
        "ethereum")
            API_BASE="https://api.etherscan.io/api"
            ;;
        "base") 
            API_BASE="https://api.basescan.org/api"
            ;;
        "bsc")
            API_BASE="https://api.bscscan.com/api"
            ;;
        "arbitrum")
            API_BASE="https://api.arbiscan.io/api"
            ;;
    esac
    
    if [ "$MODE" = "shallow" ]; then
        HOLDERS_URL="$API_BASE?module=token&action=tokenholderlist&contractaddress=$TOKEN_ADDRESS&page=1&offset=3&sort=desc"
    else
        HOLDERS_URL="$API_BASE?module=token&action=tokenholderlist&contractaddress=$TOKEN_ADDRESS&page=1&offset=100&sort=desc"
    fi
    
    fetch_data "$HOLDERS_URL" "$OUTPUT_DIR/holders.json" "Token holders data"
    
    # Token info
    TOKEN_INFO_URL="$API_BASE?module=token&action=tokeninfo&contractaddress=$TOKEN_ADDRESS"
    fetch_data "$TOKEN_INFO_URL" "$OUTPUT_DIR/token_info.json" "Token information"
fi

# 4. Deep Research Additional Data
if [ "$MODE" = "deep" ]; then
    echo -e "\n📊 === DEEP RESEARCH DATA ==="
    
    # DexScreener search for additional pairs
    echo "🔍 Searching for additional trading pairs..."
    # Extract symbol from token data first (would need jq in practice)
    SEARCH_URL="https://api.dexscreener.com/latest/dex/search?q=$TOKEN_ADDRESS"
    fetch_data "$SEARCH_URL" "$OUTPUT_DIR/search_results.json" "Token search results"
    
    # Malicious address check
    echo "🚨 Checking for malicious address flags..."
    MAL_ADDR_URL="https://api.gopluslabs.io/api/v1/address_security/$TOKEN_ADDRESS?chain_id=$CHAIN_ID"
    fetch_data "$MAL_ADDR_URL" "$OUTPUT_DIR/malicious_check.json" "Malicious address check"
fi

# 5. Generate Summary
echo -e "\n📋 === GENERATING SUMMARY ==="
cat > "$OUTPUT_DIR/research_summary.txt" << EOF
Token Research Summary
======================
Token Address: $TOKEN_ADDRESS
Chain: $CHAIN (ID: $CHAIN_ID)
Research Mode: $MODE
Timestamp: $(date)

Files Generated:
- dexscreener.json: Price, liquidity, volume data
- security.json: GoPlus security analysis
EOF

if [ "$CHAIN" != "solana" ]; then
    cat >> "$OUTPUT_DIR/research_summary.txt" << EOF
- holders.json: Top token holders
- token_info.json: Token metadata
EOF
fi

if [ "$MODE" = "deep" ]; then
    cat >> "$OUTPUT_DIR/research_summary.txt" << EOF
- search_results.json: Additional trading pairs
- malicious_check.json: Address reputation check
EOF
fi

cat >> "$OUTPUT_DIR/research_summary.txt" << EOF

Next Steps:
1. Review JSON files for data analysis
2. Use web_search for social sentiment analysis
3. Cross-reference holder addresses with known labels
4. Compile final research report

Rate Limits:
- DexScreener: 300 req/min (pairs), 60 req/min (others)  
- GoPlus: Be respectful, no published limits
- Block explorers: 5 req/sec (free tier)

Note: This script fetches raw data. Manual analysis and 
web searches are still required for complete research.
EOF

echo -e "\n✅ === RESEARCH COMPLETE ==="
echo "📁 All data saved to: $OUTPUT_DIR/"
echo "📋 Check research_summary.txt for next steps"

# Optional: Quick data validation
echo -e "\n🔍 Quick Data Validation:"
for file in "$OUTPUT_DIR"/*.json; do
    if [ -f "$file" ] && [ -s "$file" ]; then
        if grep -q "error\|Error\|null" "$file" 2>/dev/null; then
            echo "⚠️  $(basename "$file"): May contain errors"
        else
            echo "✅ $(basename "$file"): Valid JSON data"
        fi
    else
        echo "❌ $(basename "$file"): Empty or missing"
    fi
done

echo -e "\n🎯 Research session complete! Review the data and proceed with analysis."