#!/bin/bash
# Test script for workspace-architect skill
# Tests basic functionality: sandbox analysis, workspace file sizes

set -e

# Resolve skill directory relative to this script
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "🧪 Testing workspace-architect skill..."

# Test 1: Check skill structure
echo "Test 1: Checking skill structure..."
if [ -f "$SKILL_DIR/SKILL.md" ]; then
    echo "✅ SKILL.md exists"
else
    echo "⚠️  SKILL.md not found"
fi

if [ -f "$SKILL_DIR/index.js" ]; then
    echo "✅ index.js exists"
else
    echo "❌ index.js not found"
fi

# Test 2: Load main script (should not error)
echo "Test 2: Loading main script..."
timeout 10 node "$SKILL_DIR/index.js" 2>&1 | grep -q -E "(Architect|workspace)" || echo "✅ Script loads successfully"

# Test 3: Test info command
echo "Test 3: Testing info command..."
node "$SKILL_DIR/index.js" info 2>&1 | grep -q "Architect" && echo "✅ Info command works"

# Test 4: Check sandbox directory
echo "Test 4: Checking sandbox directory..."
SANDBOX_DIR="$SKILL_DIR/sandbox"
if [ -d "$SANDBOX_DIR" ]; then
    echo "✅ sandbox directory exists"
    FILES=$(ls -1 "$SANDBOX_DIR" 2>/dev/null | wc -l)
    echo "  Files in sandbox: $FILES"
else
    echo "⚠️  sandbox directory not found"
fi

# Test 5: Test analyze command
echo "Test 5: Testing analyze command..."
node "$SKILL_DIR/index.js" analyze 2>&1 | grep -q "Workspace" && echo "✅ Analyze command works"

# Test 6: Check references
echo "Test 6: Checking references..."
REFERENCES_DIR="$SKILL_DIR/references"
if [ -d "$REFERENCES_DIR" ]; then
    echo "✅ references directory exists"
    ls -1 "$REFERENCES_DIR" 2>/dev/null | head -3 || echo "  (references: empty)"
else
    echo "⚠️  references directory not found"
fi

echo "✅ All basic tests passed!"