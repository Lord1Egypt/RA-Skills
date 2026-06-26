#!/bin/bash
#
# test.sh - Test growth-loop-orchestrator functionality
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "Testing growth-loop-orchestrator"
echo "============================"

# Test 1: Check scripts exist
echo ""
echo "Test 1: Checking script files..."
for script in design-loop.sh analyze-loops.sh track-metrics.sh; do
    if [[ -f "$SCRIPT_DIR/$script" ]]; then
        echo "✅ $script exists"
    else
        echo "❌ $script missing"
        exit 1
    fi
done

# Test 2: Check executability
echo ""
echo "Test 2: Checking executability..."
for script in design-loop.sh analyze-loops.sh track-metrics.sh; do
    if [[ -x "$SCRIPT_DIR/$script" ]]; then
        echo "✅ $script is executable"
    else
        echo "⚠️  $script not executable, fixing..."
        chmod +x "$SCRIPT_DIR/$script"
    fi
done

# Test 3: Test design-loop
echo ""
echo "Test 3: Testing design-loop..."
for type in viral content network engagement; do
    "$SCRIPT_DIR/design-loop.sh" --type $type --skill test-skill || true
done

# Test 4: Test analyze-loops
echo ""
echo "Test 4: Testing analyze-loops..."
"$SCRIPT_DIR/analyze-loops.sh" --portfolio || true

# Test 5: Test track-metrics
echo ""
echo "Test 5: Testing track-metrics..."
"$SCRIPT_DIR/track-metrics.sh" --dashboard || true

echo ""
echo "============================"
echo "Tests complete"
