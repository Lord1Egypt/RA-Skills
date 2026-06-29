#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
source "$SCRIPT_DIR/../../reference/config.sh"
source "$SCRIPT_DIR/../../reference/runtime.sh"

if [ -z "$QUERY" ]; then
  echo "Error: QUERY is required"
  exit 1
fi

MARKET="${MARKET:-us}"
ENCODED_QUERY="${QUERY// /%20}"

se_request "GET" "/api/markets/search/stocks?query=${ENCODED_QUERY}&market=${MARKET}"
