#!/bin/bash
# Token Lookup - Get detailed metrics for a specific token
# By Ori - Autonomous Agent

set -e

TOKEN_ADDRESS="$1"
NETWORK="${2:-base}"

if [ -z "$TOKEN_ADDRESS" ]; then
    echo "Usage: ./token-lookup.sh <token_address> [network]"
    echo "Example: ./token-lookup.sh 0xcc4adb618253ed0d4d8a188fb901d70c54735e03 base"
    exit 1
fi

# Normalize address (remove base_ prefix if present)
TOKEN_ADDRESS=$(echo "$TOKEN_ADDRESS" | sed 's/^base_//')

echo "🔍 Looking up token: $TOKEN_ADDRESS on $NETWORK..."
echo ""

# First, try to find the pool for this token
SEARCH_URL="https://api.geckoterminal.com/api/v2/networks/${NETWORK}/tokens/${TOKEN_ADDRESS}/pools?page=1"

POOL_DATA=$(curl -s "$SEARCH_URL")

# Check if we got data
POOL_COUNT=$(echo "$POOL_DATA" | jq '.data | length')

if [ "$POOL_COUNT" = "0" ] || [ "$POOL_COUNT" = "null" ]; then
    echo "❌ No pools found for this token"
    exit 1
fi

# Analyze the top pool
echo "$POOL_DATA" | jq -r '
.data[0] |
{
    name: .attributes.name,
    price_usd: .attributes.base_token_price_usd,
    fdv: (.attributes.fdv_usd | if . then tonumber | floor else 0 end),
    market_cap: (.attributes.market_cap_usd | if . then tonumber | floor else null end),
    h24_change: .attributes.price_change_percentage.h24,
    h6_change: .attributes.price_change_percentage.h6,
    h1_change: .attributes.price_change_percentage.h1,
    m30_change: .attributes.price_change_percentage.m30,
    m15_change: .attributes.price_change_percentage.m15,
    m5_change: .attributes.price_change_percentage.m5,
    m5_buys: .attributes.transactions.m5.buys,
    m5_sells: .attributes.transactions.m5.sells,
    m15_buys: .attributes.transactions.m15.buys,
    m15_sells: .attributes.transactions.m15.sells,
    m30_buys: .attributes.transactions.m30.buys,
    m30_sells: .attributes.transactions.m30.sells,
    h1_buys: .attributes.transactions.h1.buys,
    h1_sells: .attributes.transactions.h1.sells,
    h6_buys: .attributes.transactions.h6.buys,
    h6_sells: .attributes.transactions.h6.sells,
    h24_buys: .attributes.transactions.h24.buys,
    h24_sells: .attributes.transactions.h24.sells,
    volume_h24: (.attributes.volume_usd.h24 | if . then tonumber | floor else 0 end),
    volume_h6: (.attributes.volume_usd.h6 | if . then tonumber | floor else 0 end),
    liquidity: (.attributes.reserve_in_usd | if . then tonumber | floor else 0 end),
    pool_created: .attributes.pool_created_at,
    pool_address: .attributes.address
} |
# Calculate ratios
. + {
    m5_ratio: (if .m5_sells > 0 then (.m5_buys / .m5_sells * 100 | floor / 100) else 999 end),
    m15_ratio: (if .m15_sells > 0 then (.m15_buys / .m15_sells * 100 | floor / 100) else 999 end),
    m30_ratio: (if .m30_sells > 0 then (.m30_buys / .m30_sells * 100 | floor / 100) else 999 end),
    h1_ratio: (if .h1_sells > 0 then (.h1_buys / .h1_sells * 100 | floor / 100) else 999 end),
    h6_ratio: (if .h6_sells > 0 then (.h6_buys / .h6_sells * 100 | floor / 100) else 999 end),
    h24_ratio: (if .h24_sells > 0 then (.h24_buys / .h24_sells * 100 | floor / 100) else 999 end)
} |
# Determine pattern
. + {
    pattern: (
        if .h6_ratio >= 2.0 then "🟢 STRONG ACCUMULATION"
        elif .h6_ratio >= 1.5 then "🟢 ACCUMULATION"
        elif .h6_ratio >= 1.0 then "🟡 NEUTRAL"
        elif .h6_ratio >= 0.6 then "🟠 LIGHT DISTRIBUTION"
        else "🔴 HEAVY DISTRIBUTION"
        end
    ),
    trend: (
        if .m15_ratio > .h1_ratio and .h1_ratio > .h6_ratio then "📈 IMPROVING"
        elif .m15_ratio < .h1_ratio and .h1_ratio < .h6_ratio then "📉 DETERIORATING"
        else "➡️ MIXED"
        end
    )
} |
"═══════════════════════════════════════════════════════════════════════════",
"TOKEN: \(.name)",
"═══════════════════════════════════════════════════════════════════════════",
"",
"💰 PRICE & VALUATION",
"───────────────────────────────────────────────────────────────────────────",
"Price: $\(.price_usd)",
"FDV: $\(.fdv | tostring | gsub("(?<=[0-9])(?=(?:[0-9]{3})+$)"; ","))",
"Liquidity: $\(.liquidity | tostring | gsub("(?<=[0-9])(?=(?:[0-9]{3})+$)"; ","))",
"24h Volume: $\(.volume_h24 | tostring | gsub("(?<=[0-9])(?=(?:[0-9]{3})+$)"; ","))",
"",
"📊 PRICE CHANGES",
"───────────────────────────────────────────────────────────────────────────",
"m5: \(.m5_change)% | m15: \(.m15_change)% | m30: \(.m30_change)%",
"h1: \(.h1_change)% | h6: \(.h6_change)% | h24: \(.h24_change)%",
"",
"🔄 BUY:SELL RATIOS",
"───────────────────────────────────────────────────────────────────────────",
"m5:  \(.m5_buys):\(.m5_sells) (ratio: \(.m5_ratio))",
"m15: \(.m15_buys):\(.m15_sells) (ratio: \(.m15_ratio))",
"m30: \(.m30_buys):\(.m30_sells) (ratio: \(.m30_ratio))",
"h1:  \(.h1_buys):\(.h1_sells) (ratio: \(.h1_ratio))",
"h6:  \(.h6_buys):\(.h6_sells) (ratio: \(.h6_ratio))",
"h24: \(.h24_buys):\(.h24_sells) (ratio: \(.h24_ratio))",
"",
"🎯 ANALYSIS",
"───────────────────────────────────────────────────────────────────────────",
"Pattern: \(.pattern)",
"Trend: \(.trend)",
"",
"Pool Created: \(.pool_created)",
"Pool Address: \(.pool_address)"
'
