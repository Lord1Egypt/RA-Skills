#!/bin/bash
# Test BlueColumn recall for a specific caller
# Usage: ./scripts/test-recall.sh +12065550123

if [ -z "$1" ]; then
    echo "Usage: $0 <phone-number>"
    echo "Example: $0 +12065550123"
    exit 1
fi

PHONE="$1"

# Load API key from .env
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
if [ -f "$SCRIPT_DIR/.env" ]; then
    export $(grep -v '^#' "$SCRIPT_DIR/.env" | xargs)
fi

if [ -z "$BLUECOLUMN_API_KEY" ]; then
    echo "❌ BLUECOLUMN_API_KEY not set. Check your .env file."
    exit 1
fi

echo "🔍 Recalling BlueColumn memory for caller: $PHONE"
echo ""

curl -s -X POST "https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-recall" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -d "{\"q\": \"What do I know about caller $PHONE?\"}" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print('📝 ANSWER:')
print(data.get('answer', 'No answer')[:500])
print()
print(f'📚 Sources: {len(data.get(\"sources\", []))}')
for s in data.get('sources', [])[:3]:
    print(f'  - {s.get(\"title\", \"untitled\")} (relevance: {s.get(\"relevance\", 0)})')
print()
print(f'⚡ Tokens used: {data.get(\"tokens_used\", 0)}')
"
