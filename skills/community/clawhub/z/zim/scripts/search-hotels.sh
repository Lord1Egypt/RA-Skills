#!/usr/bin/env bash
# search-hotels.sh — Generate hotel booking deeplinks with graceful fallback
# Usage: search-hotels.sh CITY CHECKIN CHECKOUT [CURRENCY] [LIMIT]
# Example: search-hotels.sh "Dubai" 2025-12-15 2025-12-18 usd 10

set -euo pipefail

CITY="${1:-}"
CHECKIN="${2:-}"
CHECKOUT="${3:-}"
CURRENCY="${4:-usd}"
LIMIT="${5:-10}"

if [[ -z "$CITY" || -z "$CHECKIN" || -z "$CHECKOUT" ]]; then
  echo "Usage: search-hotels.sh CITY CHECKIN_DATE CHECKOUT_DATE [CURRENCY] [LIMIT]"
  echo "Example: search-hotels.sh \"Dubai\" 2025-12-15 2025-12-18 usd 10"
  exit 1
fi

if [[ -z "${TRAVELPAYOUTS_TOKEN:-}" ]]; then
  echo "ERROR: Set TRAVELPAYOUTS_TOKEN in your environment to enable affiliate-linked hotel search."
  exit 1
fi

for cmd in python3; do
  if ! command -v "$cmd" &>/dev/null; then
    echo "ERROR: $cmd is required but not installed."
    exit 1
  fi
done

CITY_ENCODED=$(python3 -c "import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1]))" "$CITY")
MARKER="${TRAVELPAYOUTS_TOKEN:-openclaw}"

HOTELLOOK_URL="https://search.hotellook.com/hotels?destination=${CITY_ENCODED}&checkIn=${CHECKIN}&checkOut=${CHECKOUT}&marker=${MARKER}&currency=${CURRENCY}"
BOOKING_URL="https://www.booking.com/searchresults.html?ss=${CITY_ENCODED}&checkin=${CHECKIN}&checkout=${CHECKOUT}&selected_currency=${CURRENCY^^}"
GOOGLE_HOTELS_URL="https://www.google.com/travel/hotels/${CITY_ENCODED}?checkin=${CHECKIN}&checkout=${CHECKOUT}&curr=${CURRENCY^^}"

NIGHTS=$(python3 -c "import sys; from datetime import datetime; d1=datetime.strptime(sys.argv[1],'%Y-%m-%d'); d2=datetime.strptime(sys.argv[2],'%Y-%m-%d'); print((d2-d1).days)" "$CHECKIN" "$CHECKOUT")

echo "🏨 Hotels in ${CITY}"
echo "📅 Check-in: ${CHECKIN} | Check-out: ${CHECKOUT} (${NIGHTS} night(s))"
echo "💰 Currency: ${CURRENCY^^}"
echo "---"
echo ""
echo "Live hotel search links:"
echo ""
echo "• Hotellook"
echo "  ${HOTELLOOK_URL}"
echo ""
echo "• Booking.com"
echo "  ${BOOKING_URL}"
echo ""
echo "• Google Hotels"
echo "  ${GOOGLE_HOTELS_URL}"
echo ""
echo "---"
echo "Use these live search links to compare availability, ratings, and current pricing."
