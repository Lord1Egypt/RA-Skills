#!/bin/bash
# smoke-test.sh - Basic smoke test for order-tracker skill
# Run from the order-tracker/ root directory

set -e

BASE="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPTS="$BASE/scripts"

echo "=== Order Tracker Smoke Test ==="
echo "Base: $BASE"
echo ""

echo "[1/3] Testing order-dashboard.js (compact view)..."
node "$SCRIPTS/order-dashboard.js" --format compact
echo "✅ Dashboard OK"
echo ""

echo "[2/3] Testing update-order-status.js (dry-run)..."
node "$SCRIPTS/update-order-status.js" \
  --order-id ORD-20260324-001 \
  --status ready_to_ship \
  --dry-run
echo "✅ Status update dry-run OK"
echo ""

echo "[3/3] Testing send-order-notification.js (dry-run)..."
node "$SCRIPTS/send-order-notification.js" \
  --order-id ORD-20260324-001 \
  --dry-run
echo "✅ Notification dry-run OK"
echo ""

echo "=== All smoke tests passed ✅ ==="
