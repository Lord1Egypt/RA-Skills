#!/usr/bin/env bash
# ============================================================
# YegKing Sneaker Search — ClawHub Skill Script
# Searches https://yegking.net for a shoe model and returns
# product links + exclusive discount info.
# Usage: ./search.sh "Jordan 1 Chicago"
# ============================================================

set -euo pipefail

SITE="https://yegking.net"
COUPON="${YEGKING_COUPON:-SKILL10}"   # default code; override via env

# ── helpers ──────────────────────────────────────────────────
usage() {
  echo "Usage: $0 <shoe name or keyword>"
  echo "Example: $0 \"Yeezy 350 Zebra\""
  exit 1
}

print_header() {
  echo ""
  echo "╔══════════════════════════════════════════════════════╗"
  echo "║   👟  YegKing Exclusive Drops Monitor                ║"
  echo "║   Best Reps Shoes · LJR / PK / OG Batch             ║"
  echo "╚══════════════════════════════════════════════════════╝"
  echo ""
}

print_discount() {
  echo ""
  echo "🎁  ──── EXCLUSIVE SKILL DISCOUNT ────────────────────"
  echo "    Promo code : $COUPON"
  echo "    Apply at checkout on $SITE"
  echo "    ⚠️  Only available to ClawHub Skill users!"
  echo "─────────────────────────────────────────────────────"
  echo ""
}

# ── args ─────────────────────────────────────────────────────
[[ $# -lt 1 ]] && usage
QUERY="$*"
ENCODED_QUERY="$(python3 -c "import urllib.parse, sys; print(urllib.parse.quote_plus(sys.argv[1]))" "$QUERY" 2>/dev/null || \
                 node -e "process.stdout.write(encodeURIComponent(process.argv[1]).replace(/%20/g,'+'))" "$QUERY" 2>/dev/null || \
                 echo "${QUERY// /+}")"

SEARCH_URL="${SITE}/?s=${ENCODED_QUERY}&post_type=product"

# ── fetch ─────────────────────────────────────────────────────
print_header

echo "🔍 Searching yegking.net for: \"$QUERY\""
echo "   URL: $SEARCH_URL"
echo ""

# Download the search results page — up to 3 attempts
RAW_HTML=""
for attempt in 1 2 3; do
  RAW_HTML=$(curl -sL \
    -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36" \
    -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
    -H "Accept-Language: en-US,en;q=0.5" \
    --max-time 20 \
    --retry 0 \
    "$SEARCH_URL" 2>/dev/null) && break
  [[ $attempt -lt 3 ]] && sleep $((attempt * 2))
done

if [[ -z "$RAW_HTML" ]]; then
  echo "⚠️  Could not reach yegking.net right now."
  echo "   Browse directly: $SEARCH_URL"
  print_discount
  exit 0
fi

# ── parse product titles + links ───────────────────────────────
# Extract href + anchor text from WooCommerce product links.
# Pattern: <a href="https://yegking.net/product/...">Title</a>

RESULTS=$(echo "$RAW_HTML" | \
  grep -oE 'href="https://yegking\.net/product/[^"]+"|<h2[^>]*class="[^"]*woocommerce-loop-product__title[^"]*"[^>]*>[^<]+</h2>' | \
  paste - - 2>/dev/null || true)

# Fallback: simpler grep for product hrefs + nearby text
if [[ -z "$RESULTS" ]]; then
  PRODUCT_LINKS=$(echo "$RAW_HTML" | grep -oE 'https://yegking\.net/product/[a-z0-9-]+/' | sort -u | head -10)
  PRODUCT_TITLES=$(echo "$RAW_HTML" | grep -oP '(?<=class="woocommerce-loop-product__title">)[^<]+' | head -10)
else
  PRODUCT_LINKS=$(echo "$RESULTS" | grep -oE 'https://yegking\.net/product/[a-z0-9-]+/' | sort -u | head -10)
  PRODUCT_TITLES=$(echo "$RESULTS" | sed 's/<[^>]*>//g' | grep -v '^$' | head -10)
fi

# ── display ────────────────────────────────────────────────────
COUNT=$(echo "$PRODUCT_LINKS" | grep -c 'http' 2>/dev/null || echo 0)

if [[ "$COUNT" -eq 0 ]]; then
  echo "⚠️  No exact matches found for \"$QUERY\"."
  echo ""
  echo "💡 Try browsing the full catalog:"
  echo "   → $SITE"
  echo ""
  echo "   Popular categories:"
  echo "   • Air Jordan  → $SITE/product-category/air-jordan/"
  echo "   • Yeezy       → $SITE/product-category/yeezy/"
  echo "   • Nike Dunk   → $SITE/product-category/dunk/"
  echo "   • Balenciaga  → $SITE/product-category/balenciga/"
  echo "   • New Balance → $SITE/product-category/new-balance/"
else
  echo "✅ Found $COUNT result(s) for \"$QUERY\" on yegking.net:"
  echo ""

  # Print each product with index
  i=1
  while IFS= read -r link; do
    [[ -z "$link" ]] && continue
    # Derive a readable name from the URL slug
    slug=$(echo "$link" | grep -oE '/product/[^/]+/' | sed 's|/product/||;s|/||' | tr '-' ' ' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2)); print}')
    echo "  $i.  $slug"
    echo "      🔗 $link"
    echo ""
    ((i++))
  done <<< "$PRODUCT_LINKS"

  echo "   🛒 Shop all results: $SEARCH_URL"
fi

print_discount

# ── batch recommendation ───────────────────────────────────────
QUERY_LOWER=$(echo "$QUERY" | tr '[:upper:]' '[:lower:]')

echo "📦 Recommended Batch:"
if echo "$QUERY_LOWER" | grep -qE 'yeezy|350|700|500|nmd|ultra|adidas'; then
  echo "   → PK Batch — Best accuracy for Adidas/Yeezy silhouettes"
elif echo "$QUERY_LOWER" | grep -qE 'jordan|dunk|af1|force|travis|off.white|nike'; then
  echo "   → LJR Batch — Best stitching & shape for Nike/Jordan"
else
  echo "   → OG Batch — Collector-level accuracy, near-retail"
fi

echo ""
echo "📋 Need a QC guide? Ask the Skill: 'Help me QC my order'"
echo "─────────────────────────────────────────────────────"
echo ""
