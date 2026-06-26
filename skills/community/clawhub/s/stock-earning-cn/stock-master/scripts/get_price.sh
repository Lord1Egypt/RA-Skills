#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

if [ -z "$SYMBOL" ]; then
  echo "Error: SYMBOL is required"
  exit 1
fi

MARKET="${MARKET:-us}"

bash "$SCRIPT_DIR/run.sh" "/api/markets/stocks/${SYMBOL}/price?market=${MARKET}" "GET"
