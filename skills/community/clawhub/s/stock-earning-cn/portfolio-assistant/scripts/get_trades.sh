#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
source "$SCRIPT_DIR/../../reference/config.sh"
source "$SCRIPT_DIR/../../reference/runtime.sh"

if [ -z "$MARKET" ]; then
  echo "Error: MARKET is required"
  exit 1
fi

if [ -z "$TRADE_TYPE" ]; then
  echo "Error: TRADE_TYPE is required (buy|sell)"
  exit 1
fi

se_request "GET" "/api/trades/?market=${MARKET}&trade_type=${TRADE_TYPE}"
