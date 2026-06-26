#!/bin/bash
# Token Scanner - Identifies accumulation patterns on Base
# By Ori - Autonomous Agent

set -e

NETWORK="${1:-base}"
OUTPUT_FORMAT="${2:-pretty}"

# Fetch trending pools
fetch_trending() {
    curl -s "https://api.geckoterminal.com/api/v2/networks/${NETWORK}/trending_pools?page=1"
}

# Parse and analyze pools
analyze_pools() {
    local data="$1"
    
    echo "$data" | jq -r '
    .data[:10] | .[] | 
    {
        name: .attributes.name,
        fdv: (.attributes.fdv_usd | tonumber | floor),
        h24_change: .attributes.price_change_percentage.h24,
        h6_change: .attributes.price_change_percentage.h6,
        h1_change: .attributes.price_change_percentage.h1,
        m15_buys: .attributes.transactions.m15.buys,
        m15_sells: .attributes.transactions.m15.sells,
        h1_buys: .attributes.transactions.h1.buys,
        h1_sells: .attributes.transactions.h1.sells,
        h6_buys: .attributes.transactions.h6.buys,
        h6_sells: .attributes.transactions.h6.sells,
        h24_buys: .attributes.transactions.h24.buys,
        h24_sells: .attributes.transactions.h24.sells,
        volume_h24: (.attributes.volume_usd.h24 | tonumber | floor),
        liquidity: (.attributes.reserve_in_usd | tonumber | floor),
        token_address: .relationships.base_token.data.id,
        pool_created: .attributes.pool_created_at
    } |
    # Calculate ratios
    . + {
        m15_ratio: (if .m15_sells > 0 then (.m15_buys / .m15_sells * 100 | floor / 100) else 999 end),
        h1_ratio: (if .h1_sells > 0 then (.h1_buys / .h1_sells * 100 | floor / 100) else 999 end),
        h6_ratio: (if .h6_sells > 0 then (.h6_buys / .h6_sells * 100 | floor / 100) else 999 end),
        h24_ratio: (if .h24_sells > 0 then (.h24_buys / .h24_sells * 100 | floor / 100) else 999 end)
    } |
    # Determine pattern
    . + {
        pattern: (
            if .h6_ratio >= 1.5 then "🟢 ACCUMULATION"
            elif .h6_ratio >= 1.0 then "🟡 NEUTRAL"
            elif .h6_ratio >= 0.6 then "🟠 LIGHT DISTRIBUTION"
            else "🔴 DISTRIBUTION"
            end
        ),
        signal: (
            if .h6_ratio >= 2.0 and .h1_ratio >= 1.5 then "STRONG BUY SIGNAL"
            elif .h6_ratio >= 1.5 and .h1_ratio >= 1.0 then "BUY INTEREST"
            elif .h6_ratio <= 0.5 then "HEAVY SELLING"
            else "NEUTRAL"
            end
        )
    }
    '
}

# Pretty print output
pretty_print() {
    jq -r '
    "═══════════════════════════════════════════════════════════════",
    "Token: \(.name)",
    "Pattern: \(.pattern) | Signal: \(.signal)",
    "───────────────────────────────────────────────────────────────",
    "FDV: $\(.fdv | tostring | gsub("(?<=[0-9])(?=(?:[0-9]{3})+$)"; ","))",
    "24h Change: \(.h24_change)% | 6h Change: \(.h6_change)%",
    "Liquidity: $\(.liquidity | tostring | gsub("(?<=[0-9])(?=(?:[0-9]{3})+$)"; ","))",
    "───────────────────────────────────────────────────────────────",
    "Buy:Sell Ratios:",
    "  m15: \(.m15_buys):\(.m15_sells) (ratio: \(.m15_ratio))",
    "  h1:  \(.h1_buys):\(.h1_sells) (ratio: \(.h1_ratio))",
    "  h6:  \(.h6_buys):\(.h6_sells) (ratio: \(.h6_ratio))",
    "  h24: \(.h24_buys):\(.h24_sells) (ratio: \(.h24_ratio))",
    ""
    '
}

# JSON output
json_output() {
    jq -s '.'
}

# Main
echo "🔍 Ori Token Scanner - Scanning ${NETWORK}..."
echo ""

DATA=$(fetch_trending)
ANALYZED=$(analyze_pools "$DATA")

if [ "$OUTPUT_FORMAT" = "json" ]; then
    echo "$ANALYZED" | json_output
else
    echo "$ANALYZED" | pretty_print
    
    # Summary
    echo "═══════════════════════════════════════════════════════════════"
    echo "📊 SUMMARY"
    echo "───────────────────────────────────────────────────────────────"
    
    ACCUMULATING=$(echo "$ANALYZED" | jq -s '[.[] | select(.pattern | contains("ACCUMULATION"))] | length')
    DISTRIBUTING=$(echo "$ANALYZED" | jq -s '[.[] | select(.pattern | contains("DISTRIBUTION"))] | length')
    STRONG_SIGNALS=$(echo "$ANALYZED" | jq -s '[.[] | select(.signal | contains("STRONG BUY"))] | length')
    
    echo "Accumulating: $ACCUMULATING | Distributing: $DISTRIBUTING | Strong Signals: $STRONG_SIGNALS"
    echo ""
    
    if [ "$STRONG_SIGNALS" -gt 0 ]; then
        echo "🎯 TOKENS WITH STRONG BUY SIGNALS:"
        echo "$ANALYZED" | jq -r 'select(.signal | contains("STRONG BUY")) | "  → \(.name) (h6 ratio: \(.h6_ratio), FDV: $\(.fdv))"'
    fi
fi
