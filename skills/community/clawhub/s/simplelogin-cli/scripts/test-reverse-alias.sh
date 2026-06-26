#!/bin/bash
# Test SimpleLogin reverse alias creation
# Usage: test-reverse-alias.sh <alias_email> <contact_email>

set -e

ALIAS_EMAIL="$1"
CONTACT_EMAIL="$2"
API_KEY="${SIMPLELOGIN_API_KEY:-}"

if [ -z "$API_KEY" ]; then
    API_KEY=$(jq -r '.password // .api_key // empty' "$HOME/.openclaw/secrets/simplelogin.json" 2>/dev/null)
fi

if [ -z "$API_KEY" ]; then
    echo "❌ Error: SIMPLELOGIN_API_KEY not set"
    exit 1
fi

if [ -z "$ALIAS_EMAIL" ] || [ -z "$CONTACT_EMAIL" ]; then
    echo "Usage: test-reverse-alias.sh <alias_email> <contact_email>"
    echo "Example: test-reverse-alias.sh nordvpm@aleeas.com support@nordvpn.com"
    exit 1
fi

echo "🔍 Finding alias ID for: $ALIAS_EMAIL"

# Get alias ID
ALIAS_ID=$(curl -s "https://app.simplelogin.io/api/aliases?page_id=0" \
  -H "Authentication: $API_KEY" | jq -r ".aliases[] | select(.email==\"$ALIAS_EMAIL\") | .id")

if [ -z "$ALIAS_ID" ] || [ "$ALIAS_ID" = "null" ]; then
    echo "❌ Alias not found: $ALIAS_EMAIL"
    echo "Hint: Rate limiting may occur. Wait 60s and retry."
    exit 1
fi

echo "✅ Found alias ID: $ALIAS_ID"

# Create contact (which returns reverse_alias)
echo "📧 Creating contact: $CONTACT_EMAIL"
RESPONSE=$(curl -s -X POST "https://app.simplelogin.io/api/aliases/$ALIAS_ID/contacts" \
  -H "Authentication: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"contact\": \"$CONTACT_EMAIL\"}")

echo "📥 API Response:"
echo "$RESPONSE" | jq '.'

# Extract reverse_alias
REVERSE_ALIAS=$(echo "$RESPONSE" | jq -r '.reverse_alias // empty')

if [ -n "$REVERSE_ALIAS" ]; then
    echo -e "\n✅ SUCCESS! Reverse alias: $REVERSE_ALIAS"
    echo "📮 Send emails to this address and they'll forward through $ALIAS_EMAIL to your mailbox"
    echo "$REVERSE_ALIAS" | tr -d '\n' | pbcopy 2>/dev/null && echo "📋 Copied to clipboard!" || true
else
    echo -e "\n❌ Failed to get reverse_alias"
    echo "Response: $RESPONSE"
    exit 1
fi
