#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
source "$SCRIPT_DIR/../../reference/config.sh"
source "$SCRIPT_DIR/../../reference/runtime.sh"

if [ -z "$MARKET" ]; then
  echo "Error: MARKET is required"
  exit 1
fi

se_request "POST" "/api/brokers/seed-defaults?market=${MARKET}"
