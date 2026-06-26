#!/bin/bash
# Daily spending report - yesterday's expenses grouped by category + monthly budget progress
# Outputs structured data to stdout. The agent should reinterpret the "ANALYSIS" section
# in its own voice/style before delivering to the user.
#
# Config: ~/.config/ynab/config.json must include "monthly_target" (e.g. 2000)

set -euo pipefail

# Load config - env vars take priority, then config file
CONFIG_FILE="${YNAB_CONFIG:-$HOME/.config/ynab/config.json}"
if [ -n "${YNAB_API_KEY:-}" ] && [ -n "${YNAB_BUDGET_ID:-}" ]; then
  API_KEY="$YNAB_API_KEY"
  BUDGET_ID="$YNAB_BUDGET_ID"
elif [ -f "$CONFIG_FILE" ]; then
  API_KEY=$(jq -r '.api_key' "$CONFIG_FILE")
  BUDGET_ID=$(jq -r '.budget_id // "last-used"' "$CONFIG_FILE")
else
  echo "Error: YNAB config not found. Set YNAB_API_KEY+YNAB_BUDGET_ID or create ~/.config/ynab/config.json" >&2
  exit 1
fi

# Monthly target from config or env
if [ -n "${YNAB_MONTHLY_TARGET:-}" ]; then
  MONTHLY_TARGET="$YNAB_MONTHLY_TARGET"
elif [ -f "$CONFIG_FILE" ]; then
  MONTHLY_TARGET=$(jq -r '.monthly_target // 0' "$CONFIG_FILE")
else
  MONTHLY_TARGET=0
fi

if [ "$MONTHLY_TARGET" = "0" ] || [ "$MONTHLY_TARGET" = "null" ]; then
  echo "Error: monthly_target not set. Add \"monthly_target\": 2000 to $CONFIG_FILE or set YNAB_MONTHLY_TARGET" >&2
  exit 1
fi

YNAB_API="https://api.ynab.com/v1"

# Date calculations
YESTERDAY=$(date -u -d "yesterday" '+%Y-%m-%d')
YESTERDAY_DISPLAY=$(date -u -d "yesterday" '+%-d %b')
TODAY=$(date -u '+%Y-%m-%d')
TODAY_DISPLAY=$(date -u '+%A %-d %b')
MONTH_START=$(date -u '+%Y-%m-01')
DAYS_IN_MONTH=$(date -u -d "$(date -u '+%Y-%m-01') +1 month -1 day" '+%-d')
DAY_OF_MONTH=$(date -u '+%-d')
DAYS_REMAINING=$((DAYS_IN_MONTH - DAY_OF_MONTH + 1))

# API call with retry
api_call() {
  local url="$1"
  local max_retries=3
  local retry_delay=2
  for i in $(seq 1 $max_retries); do
    local response
    response=$(curl -s -w "\n%{http_code}" "$url" -H "Authorization: Bearer $API_KEY")
    local http_code
    http_code=$(echo "$response" | tail -n1)
    local body
    body=$(echo "$response" | sed '$d')
    if [ "$http_code" = "200" ]; then
      echo "$body"
      return 0
    fi
    if [ "$http_code" = "429" ] || [ "$http_code" = "500" ] || [ "$http_code" = "502" ] || [ "$http_code" = "503" ]; then
      if [ "$i" -lt "$max_retries" ]; then
        sleep $retry_delay
        retry_delay=$((retry_delay * 2))
        continue
      fi
    fi
    echo "ERROR:$http_code" >&2
    return 1
  done
}

# Fetch transactions from start of month
TRANSACTIONS=$(api_call "$YNAB_API/budgets/$BUDGET_ID/transactions?since_date=$MONTH_START")
if [ $? -ne 0 ]; then
  echo "YNAB API error - could not fetch transactions"
  exit 0
fi

# Header
echo "DAILY SPENDING REPORT - $TODAY_DISPLAY"
echo ""

# Yesterday's expenses grouped by category with payees
YESTERDAY_DATA=$(echo "$TRANSACTIONS" | jq -r --arg date "$YESTERDAY" '
  .data.transactions[]
  | select(.date == $date and .amount < 0 and .deleted == false and .transfer_account_id == null and .category_name != "Tasse")
  | if .category_name == "Split" then
      .subtransactions[] | select(.amount < 0)
    else . end
  | {
      category: (.category_name // "Uncategorized"),
      amount: (.amount / -1000),
      payee: (.payee_name // .memo // "")
    }
')

if [ -z "$YESTERDAY_DATA" ] || [ "$YESTERDAY_DATA" = "" ]; then
  echo "YESTERDAY ($YESTERDAY_DISPLAY)"
  echo "No expenses."
  echo ""
else
  echo "YESTERDAY ($YESTERDAY_DISPLAY)"

  # Group by category: sum amounts and collect payees
  echo "$YESTERDAY_DATA" | jq -s '
    group_by(.category)
    | map({
        category: .[0].category,
        total: (map(.amount) | add),
        payees: [.[] | .payee | select(. != "")] | unique,
        count: length
      })
    | sort_by(-.total)
    | .[]
    | . as $cat
    | $cat.category + ": EUR " + ($cat.total * 100 | round / 100 | tostring)
      + " ("
      + (if ($cat.payees | length) == 0 then
           ($cat.count | tostring) + " transactions"
         elif ($cat.payees | length) <= 3 then
           ($cat.payees | join(", "))
         else
           ($cat.payees[:3] | join(", ")) + "..."
         end)
      + ")"
  ' -r | while IFS= read -r line; do
    echo "- $line"
  done

  # Yesterday total
  YESTERDAY_TOTAL=$(echo "$YESTERDAY_DATA" | jq -s 'map(.amount) | add | . * 100 | round / 100')
  echo "---"
  echo "Day total: EUR $YESTERDAY_TOTAL"
  echo ""
fi

# Monthly progress
MONTH_SPENT=$(echo "$TRANSACTIONS" | jq --arg start "$MONTH_START" '
  [.data.transactions[]
    | select(.date >= $start and .amount < 0 and .deleted == false and .transfer_account_id == null and .category_name != "Tasse")
    | if .category_name == "Split" then
        .subtransactions[] | select(.amount < 0) | .amount
      else .amount end
  ] | map(. / -1000) | add // 0
  | . * 100 | round / 100
')

PERCENT=$(echo "$MONTH_SPENT $MONTHLY_TARGET" | awk '{printf "%.0f", ($1/$2)*100}')
MONTH_PERCENT=$(echo "$DAY_OF_MONTH $DAYS_IN_MONTH" | awk '{printf "%.0f", ($1/$2)*100}')
DAILY_BUDGET=$(echo "$MONTH_SPENT $MONTHLY_TARGET $DAYS_REMAINING" | awk '{printf "%.2f", ($2-$1)/$3}')

# Progress bar (20 chars)
FILLED=$((PERCENT / 5))
if [ "$FILLED" -gt 20 ]; then FILLED=20; fi
EMPTY=$((20 - FILLED))
BAR=$(printf '%0.s█' $(seq 1 $FILLED 2>/dev/null) || true)
BAR="${BAR}$(printf '%0.s░' $(seq 1 $EMPTY 2>/dev/null) || true)"

echo "MONTHLY PROGRESS ($DAY_OF_MONTH/$DAYS_IN_MONTH days)"
echo "- Spent so far: EUR $MONTH_SPENT / EUR $MONTHLY_TARGET = ${PERCENT}%"
echo "  $BAR"
echo "- Daily budget remaining: EUR $DAILY_BUDGET/day ($DAYS_REMAINING days left)"
echo ""

# Top categories this month
echo "TOP CATEGORIES THIS MONTH"
echo "$TRANSACTIONS" | jq -r --arg start "$MONTH_START" '
  [.data.transactions[]
    | select(.date >= $start and .amount < 0 and .deleted == false and .transfer_account_id == null and .category_name != "Tasse")
    | if .category_name == "Split" then
        .subtransactions[] | select(.amount < 0)
        | {category: (.category_name // "Uncategorized"), amount: (.amount / -1000)}
      else
        {category: (.category_name // "Uncategorized"), amount: (.amount / -1000)}
      end
  ]
  | group_by(.category)
  | map({category: .[0].category, total: (map(.amount) | add | . * 100 | round / 100)})
  | sort_by(-.total)
  | .[:5]
  | .[] | "- \(.category): EUR \(.total)"
' 2>/dev/null
echo ""

# Analysis data for the agent to reinterpret in its own style
echo "ANALYSIS DATA (reinterpret in your own style for the user)"
echo "- Budget used: ${PERCENT}% with ${MONTH_PERCENT}% of month elapsed"
if [ "$PERCENT" -le "$MONTH_PERCENT" ]; then
  echo "- Status: ON TRACK (spending pace is below or at expected rate)"
elif [ "$PERCENT" -le $((MONTH_PERCENT + 10)) ]; then
  echo "- Status: SLIGHTLY OVER PACE (spending is a bit ahead, worth monitoring)"
else
  echo "- Status: OVER PACE (spending significantly ahead of expected rate, needs attention)"
fi
echo "- Daily budget to stay on target: EUR $DAILY_BUDGET"
echo "- Month spent: EUR $MONTH_SPENT of EUR $MONTHLY_TARGET"
