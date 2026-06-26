#!/bin/bash
# Ori Accumulation Finder
# Scans trending pools to find tokens showing strong accumulation patterns
# Outputs a ranked list of opportunities

CHAIN="${1:-base}"
MIN_LIQUIDITY="${2:-50000}"  # Minimum $50k liquidity
MIN_H6_RATIO="${3:-1.5}"     # Minimum 1.5:1 buy:sell ratio in h6

echo "🎯 Ori Accumulation Finder"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "Chain: $CHAIN | Min Liquidity: \$$MIN_LIQUIDITY | Min h6 Ratio: $MIN_H6_RATIO"
echo "───────────────────────────────────────────────────────────────────────────────"
echo ""

# Fetch trending pools
POOLS=$(curl -s "https://api.geckoterminal.com/api/v2/networks/$CHAIN/trending_pools?page=1" 2>/dev/null)

if [ -z "$POOLS" ] || [ "$(echo "$POOLS" | jq -r '.data | length')" = "0" ]; then
    echo "Failed to fetch trending pools"
    exit 1
fi

echo "Scanning $(echo "$POOLS" | jq -r '.data | length') trending pools..."
echo ""

OPPORTUNITIES=""
COUNT=0

# Process each pool
echo "$POOLS" | jq -c '.data[]' | while read -r pool; do
    NAME=$(echo "$pool" | jq -r '.attributes.name // "Unknown"')
    LIQUIDITY=$(echo "$pool" | jq -r '.attributes.reserve_in_usd // 0')
    FDV=$(echo "$pool" | jq -r '.attributes.fdv_usd // 0')
    PRICE_CHANGE_H6=$(echo "$pool" | jq -r '.attributes.price_change_percentage.h6 // 0')
    PRICE_CHANGE_H24=$(echo "$pool" | jq -r '.attributes.price_change_percentage.h24 // 0')
    
    # Get transaction data
    BUYS_H6=$(echo "$pool" | jq -r '.attributes.transactions.h6.buys // 0')
    SELLS_H6=$(echo "$pool" | jq -r '.attributes.transactions.h6.sells // 0')
    BUYS_H24=$(echo "$pool" | jq -r '.attributes.transactions.h24.buys // 0')
    SELLS_H24=$(echo "$pool" | jq -r '.attributes.transactions.h24.sells // 0')
    
    # Calculate ratios
    if [ "$SELLS_H6" -gt 0 ]; then
        RATIO_H6=$(echo "scale=2; $BUYS_H6 / $SELLS_H6" | bc 2>/dev/null)
    else
        if [ "$BUYS_H6" -gt 0 ]; then
            RATIO_H6="99"
        else
            RATIO_H6="0"
        fi
    fi
    
    if [ "$SELLS_H24" -gt 0 ]; then
        RATIO_H24=$(echo "scale=2; $BUYS_H24 / $SELLS_H24" | bc 2>/dev/null)
    else
        if [ "$BUYS_H24" -gt 0 ]; then
            RATIO_H24="99"
        else
            RATIO_H24="0"
        fi
    fi
    
    # Filter criteria
    LIQ_INT=${LIQUIDITY%.*}
    LIQ_INT=${LIQ_INT:-0}
    
    # Check if meets criteria
    MEETS_LIQ=$(echo "$LIQ_INT >= $MIN_LIQUIDITY" | bc 2>/dev/null)
    MEETS_RATIO=$(echo "$RATIO_H6 >= $MIN_H6_RATIO" | bc 2>/dev/null)
    
    if [ "$MEETS_LIQ" = "1" ] && [ "$MEETS_RATIO" = "1" ]; then
        # Get token address
        TOKEN_ADDR=$(echo "$pool" | jq -r '.relationships.base_token.data.id // ""' | sed 's/.*_//')
        POOL_ADDR=$(echo "$pool" | jq -r '.attributes.address // ""')
        
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "🟢 $NAME"
        echo "   Token: $TOKEN_ADDR"
        echo "   Liquidity: \$$LIQUIDITY | FDV: \$$FDV"
        echo "   h6 Change: ${PRICE_CHANGE_H6}% | h24 Change: ${PRICE_CHANGE_H24}%"
        echo "   h6 Ratio: $RATIO_H6 ($BUYS_H6:$SELLS_H6) | h24 Ratio: $RATIO_H24 ($BUYS_H24:$SELLS_H24)"
        echo "   Pattern: ACCUMULATION ✓"
        echo ""
    fi
done

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "Scan completed at $(TZ='America/Los_Angeles' date '+%Y-%m-%d %H:%M:%S PST')"
echo ""
echo "Note: Always verify with deep-research.sh before trading"
