#!/bin/bash

# ==========================================
# StockEarning 盘点修正脚本
# 用于调整持仓的股数（不影响历史成本价）
# ==========================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

POSITION_ID=$1
QUANTITY=$2
NOTES=$3

if [ -z "$POSITION_ID" ] || [ -z "$QUANTITY" ]; then
    echo "用法: ./edit_position.sh <position_id> <quantity> [notes]"
    echo "示例: ./edit_position.sh 123 1050 \"分红送转调整\""
    exit 1
fi

JSON_PAYLOAD="{\"quantity\": $QUANTITY"
if [ -n "$NOTES" ]; then
    JSON_PAYLOAD="$JSON_PAYLOAD, \"notes\": \"$NOTES\""
fi
JSON_PAYLOAD="$JSON_PAYLOAD}"

"$SCRIPT_DIR/run.sh" "/api/positions/${POSITION_ID}/edit" "PUT" "$JSON_PAYLOAD"
