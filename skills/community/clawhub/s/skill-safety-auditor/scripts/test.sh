#!/bin/bash
#
# test.sh - Test skill-safety-auditor functionality
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "Testing skill-safety-auditor"
echo "============================"

# Test 1: Check scripts exist
echo ""
echo "Test 1: Checking script files..."
for script in audit-skill.sh quick-scan.sh list-audits.sh; do
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
for script in audit-skill.sh quick-scan.sh list-audits.sh; do
    if [[ -x "$SCRIPT_DIR/$script" ]]; then
        echo "✅ $script is executable"
    else
        echo "⚠️  $script not executable, fixing..."
        chmod +x "$SCRIPT_DIR/$script"
    fi
done

# Test 3: Test quick-scan on itself
echo ""
echo "Test 3: Running quick-scan on self..."
"$SCRIPT_DIR/quick-scan.sh" "$SKILL_DIR" || true

# Test 4: Test audit with verbose
echo ""
echo "Test 4: Running audit with verbose..."
"$SCRIPT_DIR/audit-skill.sh" "$SKILL_DIR" --verbose || true

echo ""
echo "============================"
echo "Tests complete"
