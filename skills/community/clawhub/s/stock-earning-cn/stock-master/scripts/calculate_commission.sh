#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

if [ -z "$BROKER_ID" ]; then
  echo "Error: BROKER_ID is required"
  exit 1
fi

if [ -z "$TRADE_TYPE" ]; then
  echo "Error: TRADE_TYPE is required (buy|sell)"
  exit 1
fi

if [ -z "$QUANTITY" ]; then
  echo "Error: QUANTITY is required"
  exit 1
fi

if [ -z "$PRICE" ]; then
  echo "Error: PRICE is required"
  exit 1
fi

JSON_DATA=$(printf '{"broker_id":%s,"trade_type":"%s","quantity":%s,"price":%s}' "$BROKER_ID" "$TRADE_TYPE" "$QUANTITY" "$PRICE")
bash "$SCRIPT_DIR/run.sh" "/api/brokers/calculate-commission" "POST" "$JSON_DATA"
