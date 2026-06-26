#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

if [ -z "$MARKET" ]; then
  echo "Error: MARKET is required"
  exit 1
fi

bash "$SCRIPT_DIR/run.sh" "/api/brokers/seed-defaults?market=${MARKET}" "POST"
