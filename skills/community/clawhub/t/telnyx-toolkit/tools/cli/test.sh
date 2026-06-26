#!/bin/bash
# Quick test of Telnyx setup

echo "🧪 Telnyx Connection Test"
echo "========================="
echo ""

# Check CLI
if ! command -v telnyx &> /dev/null; then
  echo "❌ Telnyx CLI not found. Run: npm install -g @telnyx/api-cli"
  exit 1
fi
echo "✓ Telnyx CLI installed"

# Check config
if [ ! -f ~/.config/telnyx/config.json ]; then
  echo "❌ API key not configured. Run: telnyx auth setup"
  exit 1
fi
echo "✓ API key configured"

# Test connection
echo ""
echo "Testing API connection..."
if telnyx account get &> /dev/null; then
  echo "✓ Connection successful"
else
  echo "❌ Connection failed"
  exit 1
fi

# Show account info
echo ""
echo "Account Status:"
telnyx account get --output json | jq '{email: .email, balance: .balance}'

# Show numbers
echo ""
echo "Phone Numbers:"
COUNT=$(telnyx number list --output json | jq '.data | length')
echo "You have $COUNT phone number(s)"

echo ""
echo "✅ Setup looks good!"
