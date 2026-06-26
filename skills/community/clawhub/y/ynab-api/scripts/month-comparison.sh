#!/bin/bash
# Compare spending between two months
# Usage: ./month-comparison.sh [month1] [month2]  # default: current vs last month

set -e

# Load config
if [ -n "${YNAB_API_KEY:-}" ] && [ -n "${YNAB_BUDGET_ID:-}" ]; then
  API_KEY="$YNAB_API_KEY"
  BUDGET_ID="$YNAB_BUDGET_ID"
elif [ -f "${YNAB_CONFIG:-$HOME/.config/ynab/config.json}" ]; then
  API_KEY=$(jq -r .api_key "${YNAB_CONFIG:-$HOME/.config/ynab/config.json}")
  BUDGET_ID=$(jq -r '.budget_id // "last-used"' "${YNAB_CONFIG:-$HOME/.config/ynab/config.json}")
else
  echo "Error: YNAB config not found." >&2
  exit 1
fi

YNAB_API="https://api.ynab.com/v1"

if [ -z "$1" ]; then
  MONTH1=$(date -u '+%Y-%m-01')
  MONTH2=$(date -u -d "$(date -u '+%Y-%m-01') -1 month" '+%Y-%m-01')
else
  MONTH1="$1"
  MONTH2="$2"
fi

MONTH1_DATA=$(curl -s "$YNAB_API/budgets/$BUDGET_ID/months/$MONTH1" -H "Authorization: Bearer $API_KEY")
MONTH2_DATA=$(curl -s "$YNAB_API/budgets/$BUDGET_ID/months/$MONTH2" -H "Authorization: Bearer $API_KEY")

# Tag categories with source month, then merge and compare
RESULT=$(jq -n -r --argjson m1 "$MONTH1_DATA" --argjson m2 "$MONTH2_DATA" '
  # Build lookup from month2 categories by id
  ($m2.data.month.categories | map({(.id): .activity}) | add // {}) as $m2map
  |
  # Iterate month1 categories
  [ $m1.data.month.categories[]
    | select(.deleted == false and .activity < 0)
    | {
        name: .name,
        s1: (.activity / -1000),
        s2: (($m2map[.id] // 0) / -1000)
      }
  ]
  | sort_by(-.s1)
  | .[:15]
  | .[]
  | if .s2 > 0 then
      ((.s1 - .s2) / .s2 * 100) as $pct
      | (if $pct > 20 then "!!" elif $pct > 0 then "+" elif $pct < -20 then "ok" elif $pct < 0 then "-" else "=" end) as $icon
      | "\(.name): \u20ac\(.s1 | floor) (era \u20ac\(.s2 | floor)) [\($icon)] \(if $pct > 0 then "+" else "" end)\($pct | floor)%"
    else
      "\(.name): \u20ac\(.s1 | floor) (nuova spesa)"
    end
')

TOTAL_M1=$(echo "$MONTH1_DATA" | jq '[.data.month.categories[] | select(.activity < 0) | .activity] | add // 0 | . / -1000')
TOTAL_M2=$(echo "$MONTH2_DATA" | jq '[.data.month.categories[] | select(.activity < 0) | .activity] | add // 0 | . / -1000')

echo "CONFRONTO SPESE"
echo "$MONTH1 vs $MONTH2"
echo ""
echo "$RESULT"
echo ""
echo "---"
echo "TOTALE Marzo: EUR $TOTAL_M1"
echo "TOTALE Febbraio: EUR $TOTAL_M2"

if [ -n "$TOTAL_M2" ] && [ "$TOTAL_M2" != "0" ]; then
  DIFF=$(awk "BEGIN { printf \"%.2f\", $TOTAL_M1 - $TOTAL_M2 }")
  PCT=$(awk "BEGIN { printf \"%.1f\", ($TOTAL_M1 - $TOTAL_M2) / $TOTAL_M2 * 100 }")
  if awk "BEGIN { exit ($TOTAL_M1 > $TOTAL_M2) ? 0 : 1 }"; then
    echo "Differenza: +EUR $DIFF (+$PCT%)"
  else
    echo "Differenza: EUR $DIFF ($PCT%)"
  fi
fi
