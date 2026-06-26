#!/usr/bin/env bash
# search-cars.sh — Generate car rental search links across providers
# Usage: search-cars.sh LOCATION PICKUP_DATE RETURN_DATE
# Example: search-cars.sh "Dubai Airport" 2025-12-15 2025-12-18
#
# Note: No single free car rental API exists with full search.
# This script generates deeplinks to major car rental comparison sites
# so users can compare prices across providers.

set -euo pipefail

# --- Args ---
LOCATION="${1:-}"
PICKUP="${2:-}"
RETURN="${3:-}"

if [[ -z "$LOCATION" || -z "$PICKUP" || -z "$RETURN" ]]; then
  echo "Usage: search-cars.sh LOCATION PICKUP_DATE RETURN_DATE"
  echo "Example: search-cars.sh \"Dubai Airport\" 2025-12-15 2025-12-18"
  exit 1
fi

if [[ -z "${TRAVELPAYOUTS_TOKEN:-}" ]]; then
  echo "WARNING: TRAVELPAYOUTS_TOKEN is not set. Affiliate commissions will not be tracked."
fi

# --- URL-encode location ---
if command -v python3 &>/dev/null; then
  LOC_ENCODED=$(python3 -c "import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1]))" "$LOCATION")
else
  LOC_ENCODED=$(echo "$LOCATION" | sed 's/ /+/g')
fi

# --- Parse dates ---
PU_YEAR=$(echo "$PICKUP" | cut -d- -f1)
PU_MONTH=$(echo "$PICKUP" | cut -d- -f2)
PU_DAY=$(echo "$PICKUP" | cut -d- -f3)
DO_YEAR=$(echo "$RETURN" | cut -d- -f1)
DO_MONTH=$(echo "$RETURN" | cut -d- -f2)
DO_DAY=$(echo "$RETURN" | cut -d- -f3)

# --- Calculate rental days ---
if command -v python3 &>/dev/null; then
  DAYS=$(python3 -c "
import sys
from datetime import datetime
d1 = datetime.strptime(sys.argv[1], '%Y-%m-%d')
d2 = datetime.strptime(sys.argv[2], '%Y-%m-%d')
print((d2-d1).days)
" "$PICKUP" "$RETURN")
else
  DAYS="?"
fi

# --- Affiliate marker ---
MARKER="${TRAVELPAYOUTS_TOKEN:-openclaw}"

# --- Build deeplinks ---
KAYAK_URL="https://www.kayak.com/cars/${LOC_ENCODED}/${PICKUP}/${RETURN}?a=${MARKER}"
DISCOVER_URL="https://www.discovercars.com/?location=${LOC_ENCODED}&pickup_date=${PICKUP}&return_date=${RETURN}&marker=${MARKER}"
RENTALCARS_URL="https://www.rentalcars.com/search?location=${LOC_ENCODED}&driversAge=30&puDay=${PU_DAY}&puMonth=${PU_MONTH}&puYear=${PU_YEAR}&doDay=${DO_DAY}&doMonth=${DO_MONTH}&doYear=${DO_YEAR}"
ECONOMYBOOKINGS_URL="https://www.economybookings.com/search?location=${LOC_ENCODED}&pick_up_date=${PICKUP}&drop_off_date=${RETURN}&marker=${MARKER}"

# --- Output ---
echo "🚗 Car Rentals: ${LOCATION}"
echo "📅 Pickup: ${PICKUP} | Return: ${RETURN} (${DAYS} days)"
echo "---"
echo ""
echo "Compare prices across these providers:"
echo ""
echo "• Kayak — Compares 100+ agencies"
echo "  ${KAYAK_URL}"
echo ""
echo "• Discover Cars — Best price guarantee"
echo "  ${DISCOVER_URL}"
echo ""
echo "• Rentalcars.com — Largest selection"
echo "  ${RENTALCARS_URL}"
echo ""
echo "• Economy Bookings — Budget-friendly"
echo "  ${ECONOMYBOOKINGS_URL}"
echo ""
echo "---"
echo "Tip: Compare across all providers for the best deal."
echo "Prices vary significantly between aggregators."
