#!/bin/bash
# Ori Small-Cap Opportunity Scanner
# Finds accumulating tokens with FDV < $5M (suitable for small capital)
# Scans multiple pages to find hidden gems

CHAIN="${1:-base}"
MAX_FDV="${2:-5000000}"       # Max $5M FDV
MIN_LIQUIDITY="${3:-10000}"   # Min $10k liquidity (lower than main scanner)
MIN_BUY_RATIO="${4:-1.3}"     # Min 1.3:1 buy:sell ratio in h6
PAGES="${5:-3}"               # Number of pages to scan

echo "🔍 Ori Small-Cap Scanner"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "Chain: $CHAIN | Max FDV: \$$MAX_FDV | Min Liquidity: \$$MIN_LIQUIDITY"
echo "Min Buy Ratio: $MIN_BUY_RATIO | Pages: $PAGES"
echo "───────────────────────────────────────────────────────────────────────────────"
echo ""

OPPORTUNITIES=()
TOTAL_SCANNED=0

for ((page=1; page<=PAGES; page++)); do
    echo "📡 Scanning page $page..."
    
    POOLS=$(curl -s "https://api.geckoterminal.com/api/v2/networks/$CHAIN/trending_pools?page=$page" 2>/dev/null)
    
    if [ -z "$POOLS" ] || [ "$(echo "$POOLS" | jq -r '.data | length')" = "0" ]; then
        echo "   No more pools on page $page"
        break
    fi
    
    POOL_COUNT=$(echo "$POOLS" | jq -r '.data | length')
    TOTAL_SCANNED=$((TOTAL_SCANNED + POOL_COUNT))
    
    # Process each pool
    while IFS= read -r pool; do
        NAME=$(echo "$pool" | jq -r '.attributes.name // "Unknown"')
        LIQUIDITY=$(echo "$pool" | jq -r '.attributes.reserve_in_usd // 0')
        FDV=$(echo "$pool" | jq -r '.attributes.fdv_usd // 0')
        PRICE_CHANGE_M15=$(echo "$pool" | jq -r '.attributes.price_change_percentage.m15 // 0')
        PRICE_CHANGE_H1=$(echo "$pool" | jq -r '.attributes.price_change_percentage.h1 // 0')
        PRICE_CHANGE_H6=$(echo "$pool" | jq -r '.attributes.price_change_percentage.h6 // 0')
        PRICE_CHANGE_H24=$(echo "$pool" | jq -r '.attributes.price_change_percentage.h24 // 0')
        VOLUME_H24=$(echo "$pool" | jq -r '.attributes.volume_usd.h24 // 0')
        CREATED=$(echo "$pool" | jq -r '.attributes.pool_created_at // ""')
        
        # Get transaction data
        BUYS_M15=$(echo "$pool" | jq -r '.attributes.transactions.m15.buys // 0')
        SELLS_M15=$(echo "$pool" | jq -r '.attributes.transactions.m15.sells // 0')
        BUYS_H1=$(echo "$pool" | jq -r '.attributes.transactions.h1.buys // 0')
        SELLS_H1=$(echo "$pool" | jq -r '.attributes.transactions.h1.sells // 0')
        BUYS_H6=$(echo "$pool" | jq -r '.attributes.transactions.h6.buys // 0')
        SELLS_H6=$(echo "$pool" | jq -r '.attributes.transactions.h6.sells // 0')
        
        # Calculate ratios (handle division by zero)
        if [ "$SELLS_M15" -gt 0 ] 2>/dev/null; then
            RATIO_M15=$(echo "scale=2; $BUYS_M15 / $SELLS_M15" | bc 2>/dev/null || echo "0")
        else
            RATIO_M15="0"
        fi
        
        if [ "$SELLS_H1" -gt 0 ] 2>/dev/null; then
            RATIO_H1=$(echo "scale=2; $BUYS_H1 / $SELLS_H1" | bc 2>/dev/null || echo "0")
        else
            RATIO_H1="0"
        fi
        
        if [ "$SELLS_H6" -gt 0 ] 2>/dev/null; then
            RATIO_H6=$(echo "scale=2; $BUYS_H6 / $SELLS_H6" | bc 2>/dev/null || echo "0")
        else
            RATIO_H6="0"
        fi
        
        # Convert to integers for comparison
        LIQ_INT=$(printf "%.0f" "$LIQUIDITY" 2>/dev/null || echo "0")
        FDV_INT=$(printf "%.0f" "$FDV" 2>/dev/null || echo "0")
        
        # Filter criteria:
        # 1. FDV under max (small cap)
        # 2. Liquidity above min
        # 3. Buy ratio meets threshold in at least h6
        
        if [ "$FDV_INT" -gt 0 ] && [ "$FDV_INT" -le "$MAX_FDV" ] && \
           [ "$LIQ_INT" -ge "$MIN_LIQUIDITY" ] && \
           [ "$(echo "$RATIO_H6 >= $MIN_BUY_RATIO" | bc 2>/dev/null)" = "1" ]; then
            
            TOKEN_ADDR=$(echo "$pool" | jq -r '.relationships.base_token.data.id // ""' | sed 's/.*_//')
            SYMBOL=$(echo "$NAME" | cut -d'/' -f1 | xargs)
            
            # Calculate a score (higher = better opportunity)
            # Score = ratio * (1 + positive_momentum)
            MOMENTUM=0
            [ "$(echo "$PRICE_CHANGE_H1 > 0" | bc 2>/dev/null)" = "1" ] && MOMENTUM=$((MOMENTUM + 1))
            [ "$(echo "$PRICE_CHANGE_H6 > 0" | bc 2>/dev/null)" = "1" ] && MOMENTUM=$((MOMENTUM + 1))
            
            SCORE=$(echo "scale=2; $RATIO_H6 * (1 + $MOMENTUM * 0.25)" | bc 2>/dev/null || echo "$RATIO_H6")
            
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "🟢 $NAME (Score: $SCORE)"
            echo "   Token: $TOKEN_ADDR"
            echo "   FDV: \$$(printf "%'.0f" $FDV_INT) | Liquidity: \$$(printf "%'.0f" $LIQ_INT)"
            echo "   Volume 24h: \$$(printf "%'.0f" ${VOLUME_H24%.*})"
            echo ""
            echo "   📈 Price Changes:"
            echo "      m15: ${PRICE_CHANGE_M15}% | h1: ${PRICE_CHANGE_H1}% | h6: ${PRICE_CHANGE_H6}% | h24: ${PRICE_CHANGE_H24}%"
            echo ""
            echo "   📊 Buy:Sell Ratios:"
            echo "      m15: $RATIO_M15 ($BUYS_M15:$SELLS_M15)"
            echo "      h1:  $RATIO_H1 ($BUYS_H1:$SELLS_H1)"
            echo "      h6:  $RATIO_H6 ($BUYS_H6:$SELLS_H6)"
            echo ""
            echo "   ⏰ Created: $CREATED"
            echo "   🔗 https://dexscreener.com/$CHAIN/$TOKEN_ADDR"
        fi
        
    done < <(echo "$POOLS" | jq -c '.data[]')
    
    # Rate limiting
    sleep 0.5
done

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "Scanned $TOTAL_SCANNED pools across $PAGES pages"
echo "Completed at $(TZ='America/Los_Angeles' date '+%Y-%m-%d %H:%M:%S PST')"
echo ""
echo "💡 Tip: Run deep-research.sh <token> before trading"
