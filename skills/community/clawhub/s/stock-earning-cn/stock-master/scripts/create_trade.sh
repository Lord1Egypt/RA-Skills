#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

if [ -z "$SYMBOL" ]; then
  echo "Error: SYMBOL is required"
  exit 1
fi

if [ -z "$NAME" ]; then
  echo "Error: NAME is required"
  exit 1
fi

if [ -z "$MARKET" ]; then
  echo "Error: MARKET is required"
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

if [ -z "$TRADE_DATE" ]; then
  echo "Error: TRADE_DATE is required (e.g. 2026-01-01T09:30:00+00:00)"
  exit 1
fi

COMMISSION="${COMMISSION:-0}"
NOTES="${NOTES:-recorded via stock-master}"

MARKET_LC="$(printf '%s' "$MARKET" | tr '[:upper:]' '[:lower:]')"
if [ -z "$CURRENCY" ]; then
  case "$MARKET_LC" in
    cn_a) CURRENCY="CNY" ;;
    hk) CURRENCY="HKD" ;;
    *) CURRENCY="USD" ;;
  esac
fi

ESC_NAME="${NAME//\"/\\\"}"
ESC_NOTES="${NOTES//\"/\\\"}"

JSON_DATA=$(printf '{"symbol":"%s","name":"%s","market":"%s","currency":"%s","trade_type":"%s","quantity":%s,"price":%s,"commission":%s,"notes":"%s","trade_date":"%s"}' "$SYMBOL" "$ESC_NAME" "$MARKET" "$CURRENCY" "$TRADE_TYPE" "$QUANTITY" "$PRICE" "$COMMISSION" "$ESC_NOTES" "$TRADE_DATE")
bash "$SCRIPT_DIR/run.sh" "/api/trades/" "POST" "$JSON_DATA"
