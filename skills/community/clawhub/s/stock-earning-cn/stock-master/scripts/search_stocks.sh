#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

if [ -z "$QUERY" ]; then
  echo "Error: QUERY is required"
  exit 1
fi

MARKET="${MARKET:-us}"
ENCODED_QUERY="${QUERY// /%20}"

bash "$SCRIPT_DIR/run.sh" "/api/markets/search/stocks?query=${ENCODED_QUERY}&market=${MARKET}" "GET"
