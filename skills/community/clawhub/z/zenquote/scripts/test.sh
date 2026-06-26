#!/bin/bash
#
# ZenQuote Skill Test Suite
#

set -e

ZENQUOTE="$HOME/.openclaw/skills/zenquote/scripts/zenquote.sh"

echo "=== ZenQuote Skill Test ==="
echo ""

# Test 1: Today's quote
echo "1. Testing 'today' command..."
RESULT=$(bash "$ZENQUOTE" today)
if echo "$RESULT" | grep -q "Daily Inspiration"; then
  echo "✓ Today's quote works"
else
  echo "✗ Today's quote failed"
  exit 1
fi
echo ""

# Test 2: Random quote
echo "2. Testing 'random' command..."
RESULT=$(bash "$ZENQUOTE" random)
if echo "$RESULT" | grep -q "Daily Inspiration"; then
  echo "✓ Random quote works"
else
  echo "✗ Random quote failed"
  exit 1
fi
echo ""

# Test 3: Multiple quotes
echo "3. Testing 'quotes' command..."
RESULT=$(bash "$ZENQUOTE" quotes 3)
if echo "$RESULT" | grep -q "Inspirational Quotes"; then
  echo "✓ Multiple quotes works"
else
  echo "✗ Multiple quotes failed"
  exit 1
fi
echo ""

# Test 4: Image URL
echo "4. Testing 'image' command..."
RESULT=$(bash "$ZENQUOTE" image)
if echo "$RESULT" | grep -q "zenquotes.io/api/image"; then
  echo "✓ Image URL works"
else
  echo "✗ Image URL failed"
  exit 1
fi
echo ""

# Test 5: Help
echo "5. Testing 'help' command..."
RESULT=$(bash "$ZENQUOTE" help)
if echo "$RESULT" | grep -q "Usage:"; then
  echo "✓ Help works"
else
  echo "✗ Help failed"
  exit 1
fi
echo ""

echo "=== All Tests Passed! ==="
