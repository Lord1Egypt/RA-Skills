#!/usr/bin/env bash
# search-flights.sh — Search flights via Travelpayouts API with fallback
# Usage: search-flights.sh ORIGIN DEST DEPARTURE [RETURN] [CURRENCY] [LIMIT]
# Example: search-flights.sh LHR DXB 2025-12-15 2025-12-20 usd 5

set -euo pipefail

ORIGIN="${1:-}"
DEST="${2:-}"
DEPARTURE="${3:-}"
RETURN="${4:-}"
CURRENCY="${5:-usd}"
LIMIT="${6:-10}"

if [[ -z "$ORIGIN" || -z "$DEST" || -z "$DEPARTURE" ]]; then
  echo "Usage: search-flights.sh ORIGIN DEST DEPARTURE_DATE [RETURN_DATE] [CURRENCY] [LIMIT]"
  echo "Example: search-flights.sh LHR DXB 2025-12-15 2025-12-20 usd 5"
  exit 1
fi

if [[ -z "${TRAVELPAYOUTS_TOKEN:-}" ]]; then
  echo "ERROR: Set TRAVELPAYOUTS_TOKEN in your environment to enable flight search."
  exit 1
fi

for cmd in curl jq python3; do
  if ! command -v "$cmd" &>/dev/null; then
    echo "ERROR: $cmd is required but not installed."
    exit 1
  fi
done

DEP_DDMM=$(echo "$DEPARTURE" | awk -F- '{printf "%s%s", $3, $2}')
RET_DDMM=""
if [[ -n "$RETURN" ]]; then
  RET_DDMM=$(echo "$RETURN" | awk -F- '{printf "%s%s", $3, $2}')
fi

DIRECT_URL="https://api.travelpayouts.com/aviasales/v3/prices_for_dates?origin=${ORIGIN}&destination=${DEST}&departure_at=${DEPARTURE}&currency=${CURRENCY}&limit=${LIMIT}&sorting=price&token=${TRAVELPAYOUTS_TOKEN}"
if [[ -n "$RETURN" ]]; then
  DIRECT_URL+="&return_at=${RETURN}"
fi

DIRECT_RESPONSE=$(curl -sf "$DIRECT_URL" 2>/dev/null || echo '{"data":[]}')
DIRECT_COUNT=$(echo "$DIRECT_RESPONSE" | jq '.data | length' 2>/dev/null || echo "0")

SEARCH_URL="https://www.aviasales.com/search/${ORIGIN}${DEP_DDMM}${DEST}${RET_DDMM}1?marker=${TRAVELPAYOUTS_TOKEN}"

if [[ "$DIRECT_COUNT" -gt 0 ]]; then
  echo "✈️  Flights: ${ORIGIN} → ${DEST}"
  echo "📅 Departure: ${DEPARTURE}${RETURN:+ | Return: $RETURN}"
  echo "💰 Currency: ${CURRENCY^^}"
  echo "---"
  echo ""

  echo "$DIRECT_RESPONSE" | jq -r --arg token "$TRAVELPAYOUTS_TOKEN" --arg dep_ddmm "$DEP_DDMM" --arg ret_ddmm "$RET_DDMM" --arg origin "$ORIGIN" --arg dest "$DEST" '
    .data[] |
    "• \(.airline)\(if .flight_number then " " + (.flight_number|tostring) else "" end) — \(.origin // $origin) → \(.destination // $dest)" +
    "\n  Price: $\(.price)" +
    "\n  Departs: \(.departure_at // "N/A")" +
    (if .return_at then "\n  Returns: \(.return_at)" else "" end) +
    "\n  Stops: \(.transfers // 0)" +
    (if .link then
      "\n  Book: https://www.aviasales.com\(.link)&marker=\($token)"
    else
      "\n  Book: https://www.aviasales.com/search/\($origin)\($dep_ddmm)\($dest)\($ret_ddmm)1?marker=\($token)"
    end) +
    "\n"
  '

  echo "---"
  echo "Found ${DIRECT_COUNT} result(s). Prices are cached and may differ on booking site."
  exit 0
fi

CHEAP_DEPART_MONTH=$(echo "$DEPARTURE" | cut -d- -f1-2)
CHEAP_RETURN_MONTH=""
if [[ -n "$RETURN" ]]; then
  CHEAP_RETURN_MONTH=$(echo "$RETURN" | cut -d- -f1-2)
fi

CHEAP_URL="https://api.travelpayouts.com/v1/prices/cheap?origin=${ORIGIN}&destination=${DEST}&depart_date=${CHEAP_DEPART_MONTH}&currency=${CURRENCY}&token=${TRAVELPAYOUTS_TOKEN}"
if [[ -n "$CHEAP_RETURN_MONTH" ]]; then
  CHEAP_URL+="&return_date=${CHEAP_RETURN_MONTH}"
fi

CHEAP_RESPONSE=$(curl -sf "$CHEAP_URL" 2>/dev/null || echo '{"data":{}}')
CHEAP_COUNT=$(echo "$CHEAP_RESPONSE" | jq '.data | length' 2>/dev/null || echo "0")

echo "✈️  Flights: ${ORIGIN} → ${DEST}"
echo "📅 Requested: ${DEPARTURE}${RETURN:+ | Return: $RETURN}"
echo "💰 Currency: ${CURRENCY^^}"
echo "---"
echo ""

if [[ "$CHEAP_COUNT" -gt 0 ]]; then
  echo "No exact-date structured results found, but nearby cached fares are available:"
  echo ""
  echo "$CHEAP_RESPONSE" | jq -r '
    .data | to_entries[] | .value | to_entries[] | .value |
    "• " + (.airline // "Airline") + " " + ((.flight_number // "")|tostring) +
    "\n  Price: $" + ((.price // "N/A")|tostring) +
    "\n  Departs: " + (.departure_at // "N/A") +
    (if .return_at then "\n  Returns: " + .return_at else "" end) +
    "\n"
  ' | head -n $((LIMIT*5))
fi

echo "Live search:"
echo "${SEARCH_URL}"
echo ""
echo "Use the live Aviasales search link above for current bookable options when exact cached fares are unavailable."
exit 0
