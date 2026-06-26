#!/bin/bash
# Search flight tickets via voyager MCP API
# Usage: search-flights.sh <depCountry> <arrCountry> <isBusiness> <depCity> <arrCity> <currency> <depDate> <subQuery>

set -e

# Parameters
DEP_COUNTRY="$1"
ARR_COUNTRY="$2"
IS_BUSINESS="$3"
DEP_CITY="$4"
ARR_CITY="$5"
CURRENCY="$6"
DEP_DATE="$7"
SUB_QUERY="$8"

# Make API call
curl --silent --location --request POST \
  'https://ivguserprod.alipay.com/ivgavatarcn/api/v1/voyager/mcp/RECALL_flight' \
  --header 'Content-Type: application/json' \
  --data @- <<EOF
{"depCountry":"${DEP_COUNTRY}","arrCountry":"${ARR_COUNTRY}","isBusiness":${IS_BUSINESS},"arrCity":"${ARR_CITY}","depCity":"${DEP_CITY}","currency":"${CURRENCY}","depDate":"${DEP_DATE}","subQuery":"${SUB_QUERY}"}
EOF
