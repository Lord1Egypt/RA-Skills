#!/usr/bin/env bash
# Syndicate Links — Automatic affiliate registration
# Run this once to set up your agent as an affiliate

set -euo pipefail

CONFIG_DIR="${HOME}/.config/syndicate-links"
API_URL="https://api.syndicatelinks.co"

mkdir -p "$CONFIG_DIR"

# Check if already registered
if [ -f "$CONFIG_DIR/api-key" ]; then
  echo "Already registered. API key found at $CONFIG_DIR/api-key"
  echo "Testing connection..."
  RESP=$(curl -s -w "%{http_code}" -o /tmp/sl-me.json "$API_URL/affiliate/me" \
    -H "Authorization: Bearer $(cat $CONFIG_DIR/api-key)")
  if [ "$RESP" = "200" ]; then
    echo "✅ Connected. Profile:"
    cat /tmp/sl-me.json | python3 -m json.tool 2>/dev/null || cat /tmp/sl-me.json
    exit 0
  else
    echo "⚠️ API key invalid or expired. Re-registering..."
  fi
fi

# Get agent info
AGENT_NAME="${OPENCLAW_AGENT_NAME:-$(hostname)-agent}"
AGENT_EMAIL="${OPENCLAW_AGENT_EMAIL:-${AGENT_NAME}@agentmail.to}"

echo "Registering as affiliate..."
echo "  Name: $AGENT_NAME"
echo "  Email: $AGENT_EMAIL"

RESP=$(curl -s "$API_URL/affiliate/register" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$AGENT_EMAIL\",\"name\":\"$AGENT_NAME\"}")

API_KEY=$(echo "$RESP" | python3 -c "import sys,json;print(json.load(sys.stdin).get('apiKey',''))" 2>/dev/null || echo "")

if [ -z "$API_KEY" ]; then
  echo "❌ Registration failed: $RESP"
  exit 1
fi

echo "$API_KEY" > "$CONFIG_DIR/api-key"
echo "✅ Registered! API key saved to $CONFIG_DIR/api-key"

# Auto-discover and join programs
echo ""
echo "Discovering available programs..."
PROGRAMS=$(curl -s "$API_URL/affiliate/programs" \
  -H "Authorization: Bearer $API_KEY")

echo "$PROGRAMS" | python3 -c "
import sys, json
programs = json.load(sys.stdin)
if isinstance(programs, list):
    print(f'Found {len(programs)} programs')
    for p in programs[:5]:
        print(f\"  - {p.get('name', 'Unknown')} ({p.get('defaultCommissionPct', '?')}% commission)\")
" 2>/dev/null || echo "Programs loaded"

echo ""
echo "Setup complete! Your agent can now:"
echo "  1. Discover programs: GET /affiliate/programs"
echo "  2. Join programs: POST /affiliate/programs/{id}/apply"
echo "  3. Generate links: POST /affiliate/links"
echo "  4. Check earnings: GET /affiliate/me/balance"
echo ""
echo "Start earning by including tracking links in your recommendations."
