#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
source "$SCRIPT_DIR/../../reference/config.sh"
source "$SCRIPT_DIR/../../reference/runtime.sh"

if [ -z "$SYMBOL" ]; then
  echo "Error: SYMBOL is required"
  exit 1
fi

MARKET="${MARKET:-us}"

se_request "GET" "/api/markets/stocks/${SYMBOL}/price?market=${MARKET}"
