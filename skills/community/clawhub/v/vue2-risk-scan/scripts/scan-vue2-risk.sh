#!/bin/bash

echo "================================="
echo "🔍 Vue2 Project Risk Scan"
echo "================================="

HIGH_RISK=0
MEDIUM_RISK=0

run_check() {
  OUTPUT=$(sh $1)
  echo "$OUTPUT"

  HIGH=$(echo "$OUTPUT" | grep -c "❌")
  MEDIUM=$(echo "$OUTPUT" | grep -c "⚠️")

  HIGH_RISK=$((HIGH_RISK + HIGH))
  MEDIUM_RISK=$((MEDIUM_RISK + MEDIUM))
}

echo ""
echo "📦 Dependency Check"
run_check scripts/checks/check-deps.sh

echo ""
echo "🧱 Webpack Check"
run_check scripts/checks/check-webpack.sh

echo ""
echo "🧬 Babel Check"
run_check scripts/checks/check-babel.sh

echo ""
echo "================================="
echo "📊 Summary"
echo "❌ High Risk: $HIGH_RISK"
echo "⚠️ Medium Risk: $MEDIUM_RISK"
echo "================================="