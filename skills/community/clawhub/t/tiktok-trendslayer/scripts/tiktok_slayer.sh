#!/usr/bin/env bash
# tiktok_slayer.sh — TikTok Shop product + influencer analytics via EchoTik + TikTok Shop APIs
# Dependencies: curl, jq
# Required env: ECHOTIK_AUTH_HEADER, TIKTOK_SHOP_API_KEY (optional for product search)

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="${TIKTOK_SLAYER_OUTPUT:-$SKILL_DIR/output}"
mkdir -p "$OUTPUT_DIR"

CATEGORY=""
ALL=false
FORMAT="json"
REGIONS="US"
PAGE_SIZE=10
MODE="influencers"  # influencers or products or both

usage() {
  cat <<'USAGE'
Usage: tiktok_slayer.sh [options]

Data Fetching:
  --category <code>       Single category: beauty, 3c, home, fashion,
                          food, sports, baby, pet
  --all                   Analyze all 8 categories
  --region <codes>        Region(s), comma-separated: US,SG,TH,UK,...
                          Default: US  Example: --region US,SG,TH
  --page-size <n>         Results per request (default: 10, max: 10)
  --format <fmt>          Output format: json (default) or md
  --output-dir <path>     Custom output directory
  --mode <mode>           Data type: influencers (default), products, both

Other:
  -h, --help              Show this help

Environment:
  ECHOTIK_AUTH_HEADER     Required. Basic auth for EchoTik API.
                          Format: "Basic <base64(user:pass)>"
  TIKTOK_SHOP_API_KEY     Optional. TikTok Shop Partner API key for product data.
  TIKTOK_SLAYER_OUTPUT    Optional. Override output directory.

Examples:
  tiktok_slayer.sh --category beauty --region US
  tiktok_slayer.sh --category 3c --region US,SG,TH --format md --mode influencers
  tiktok_slayer.sh --category beauty --region US --mode products
  tiktok_slayer.sh --all --region US,SG,TH --format json --mode both
USAGE
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --category) CATEGORY="$2"; shift 2 ;;
    --all) ALL=true; shift ;;
    --format) FORMAT="$2"; shift 2 ;;
    --region) REGIONS="$2"; shift 2 ;;
    --page-size) PAGE_SIZE="$2"; shift 2 ;;
    --output-dir) OUTPUT_DIR="$2"; shift 2 ;;
    --mode) MODE="$2"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "Error: Unknown option: $1"; echo; usage ;;
  esac
done

# --- Validation ---

if [[ -z "${ECHOTIK_AUTH_HEADER:-}" ]]; then
  echo "Error: Missing ECHOTIK_AUTH_HEADER"
  echo "  Set: export ECHOTIK_AUTH_HEADER=\"Basic <base64_credentials>\""
  echo "  Get credentials at: https://www.echotik.com/"
  exit 1
fi

[[ "$PAGE_SIZE" =~ ^[0-9]+$ ]] && [[ "$PAGE_SIZE" -ge 1 ]] && [[ "$PAGE_SIZE" -le 10 ]] || PAGE_SIZE=10
[[ "$FORMAT" == "json" || "$FORMAT" == "md" ]] || { echo "Error: Invalid format: $FORMAT"; exit 1; }
[[ "$MODE" == "influencers" || "$MODE" == "products" || "$MODE" == "both" ]] || {
  echo "Error: Invalid mode: $MODE (use influencers/products/both)"; exit 1;
}

command -v curl &>/dev/null || { echo "Error: Missing dependency: curl"; exit 1; }
command -v jq &>/dev/null || { echo "Error: Missing dependency: jq"; exit 1; }

mkdir -p "$OUTPUT_DIR"

# --- Category helpers ---

get_category_id() {
  case "$1" in
    beauty)  echo "10001" ;; 3c)      echo "10002" ;;
    home)    echo "10003" ;; fashion) echo "10004" ;;
    food)    echo "10005" ;; sports)  echo "10006" ;;
    baby)    echo "10007" ;; pet)     echo "10008" ;;
    *) echo "" ;;
  esac
}

is_valid_category() { [[ -n "$(get_category_id "$1")" ]]; }

ALL_CATEGORIES="beauty 3c home fashion food sports baby pet"

# --- EchoTik influencer fetch ---

fetch_echotik_influencers() {
  local cat="$1" region="$2"
  local cat_id; cat_id=$(get_category_id "$cat")
  local ts; ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  local out_file="$OUTPUT_DIR/${cat}_${region}_$(date +%Y%m%d)_influencers.${FORMAT}"

  printf "  EchoTik [%s/%s] Influencers..." "$cat" "$region"

  local response
  response=$(curl -sf --max-time 15 \
    -X GET "https://open.echotik.live/api/v3/echotik/influencer/list?page_size=${PAGE_SIZE}&page_num=1&region=${region}" \
    -H "Authorization: ${ECHOTIK_AUTH_HEADER}" \
    -H "Content-Type: application/json" 2>/dev/null) || {
    printf " FAILED\n"; return 1;
  }

  jq empty <<<"$response" 2>/dev/null || {
    printf " FAILED (invalid JSON)\n"; return 1;
  }

  local count
  count=$(jq 'if .data then (.data | length) else 0 end' <<<"$response" 2>/dev/null) || count=0

  if [[ "$FORMAT" == "md" ]]; then
    {
      echo "# EchoTik Influencer Report"
      echo ""
      echo "**Category:** $cat | **Region:** $region | **Generated:** $ts"
      echo ""
      echo "## High-Engagement Influencers (engagement > 5%)"
      echo ""
      echo "| Nickname | Followers | Engagement | EC Score | Sales | Avg Price |"
      echo "|----------|----------|------------|----------|-------|-----------|"
      jq -r '
        .data[]? // [] |
        select((.interaction_rate // 0) > 0.05) |
        [
          (.nick_name // "N/A"),
          (.total_followers_cnt // 0 | tostring),
          ((.interaction_rate // 0) * 100 | tostring | . + "%"),
          ((.ec_score // 0) | tostring),
          (.sales // 0 | tostring),
          (.avg_30d_price // 0 | tostring)
        ] | join(" | ")
      ' <<<"$response" 2>/dev/null || echo "| (no data) | - | - | - | - | - |"
      echo ""
      echo "## Full Data ($count results)"
      echo ""
      echo '```json'
      jq '.' <<<"$response" 2>/dev/null
      echo '```'
    } > "$out_file"
  else
    jq --arg cat "$cat" --arg region "$region" --arg ts "$ts" --arg count "$count" '{
      report_meta: { category: $cat, region: $region, generated_at: $ts, result_count: ($count|tonumber), api: "echotik_influencer_list" },
      influencers: (.data // [])
    }' <<<"$response" > "$out_file" 2>/dev/null || echo "$response" > "$out_file"
  fi

  printf " OK (%d)\n" "$count"
}

# --- TikTok Shop product fetch ---

fetch_tiktokshop_products() {
  local cat="$1" region="$2"
  local cat_id; cat_id=$(get_category_id "$cat")
  local ts; ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  local out_file="$OUTPUT_DIR/${cat}_${region}_$(date +%Y%m%d)_products.${FORMAT}"

  printf "  TikTok Shop [%s/%s] Products..." "$cat" "$region"

  if [[ -z "${TIKTOK_SHOP_API_KEY:-}" ]]; then
    printf " SKIP (no API key)\n"
    {
      echo "# TikTok Shop Product Report"
      echo ""
      echo "**Category:** $cat | **Region:** $region | **Generated:** $ts"
      echo ""
      echo "## Note"
      echo "Product data unavailable because TIKTOK_SHOP_API_KEY environment variable is not set."
      echo "To enable product fetching:"
      echo "1. Log in to https://seller.tiktokglobalshop.com/"
      echo "2. Create an app in Developer Center"
      echo "3. Export: export TIKTOK_SHOP_API_KEY=\"your_app_key\""
      echo ""
    } > "$out_file"
    return 0
  fi

  # This is a placeholder for TikTok Shop API — actual endpoint may differ
  # Based on TikTok Shop Partner API docs: /api/v2/products/search
  local response
  response=$(curl -sf --max-time 15 \
    -X GET "https://api.tiktokshop.com/v2/products/search?category_id=${cat_id}&region=${region}&page_size=${PAGE_SIZE}" \
    -H "Authorization: Bearer ${TIKTOK_SHOP_API_KEY}" \
    -H "Content-Type: application/json" 2>/dev/null) || {
    printf " FAILED\n"; return 1;
  }

  jq empty <<<"$response" 2>/dev/null || {
    printf " FAILED (invalid JSON)\n"; return 1;
  }

  local count
  count=$(jq 'if .data.products then (.data.products | length) else 0 end' <<<"$response" 2>/dev/null) || count=0

  if [[ "$FORMAT" == "md" ]]; then
    {
      echo "# TikTok Shop Product Report"
      echo ""
      echo "**Category:** $cat | **Region:** $region | **Generated:** $ts"
      echo ""
      echo "## Trending Products"
      echo ""
      echo "| Product | Price | Sales Volume | GMV Growth | Image |"
      echo "|---------|-------|--------------|------------|-------|"
      jq -r '
        .data.products[]? // [] |
        [
          (.title // "N/A"),
          (.price // 0 | tostring),
          (.sales_volume // 0 | tostring),
          (.gmv_growth // "0%"),
          (.image_url // "")
        ] | join(" | ")
      ' <<<"$response" 2>/dev/null || echo "| (no data) | - | - | - | - |"
      echo ""
      echo "## Full Data ($count results)"
      echo ""
      echo '```json'
      jq '.' <<<"$response" 2>/dev/null
      echo '```'
    } > "$out_file"
  else
    jq --arg cat "$cat" --arg region "$region" --arg ts "$ts" --arg count "$count" '{
      report_meta: { category: $cat, region: $region, generated_at: $ts, result_count: ($count|tonumber), api: "tiktokshop_product_search" },
      products: (.data.products // [])
    }' <<<"$response" > "$out_file" 2>/dev/null || echo "$response" > "$out_file"
  fi

  printf " OK (%d)\n" "$count"
}

# --- Main ---

if $ALL; then categories="$ALL_CATEGORIES"; elif [[ -n "$CATEGORY" ]]; then
  if ! is_valid_category "$CATEGORY"; then echo "Error: Unknown category: $CATEGORY"; echo "  Supported: $ALL_CATEGORIES"; exit 1; fi
  categories="$CATEGORY"
else usage; fi

echo "=== TikTok Trend Slayer ==="
echo "Categories: $categories"
echo "Regions:    $REGIONS"
echo "Mode:       $MODE"
echo "Format:     $FORMAT"
echo "Output:     $OUTPUT_DIR"
echo ""

IFS=',' read -ra region_list <<< "$REGIONS"
for cat in $categories; do
  for region in "${region_list[@]}"; do
    if [[ "$MODE" == "influencers" ]]; then
      fetch_echotik_influencers "$cat" "$region" || true
    elif [[ "$MODE" == "products" ]]; then
      fetch_tiktokshop_products "$cat" "$region" || true
    elif [[ "$MODE" == "both" ]]; then
      fetch_echotik_influencers "$cat" "$region" || true
      fetch_tiktokshop_products "$cat" "$region" || true
    fi
  done
done

echo ""
echo "Done! Check $OUTPUT_DIR"
