#!/bin/bash
# Agent startup recall — queries ultramemory API for relevant context.
# Usage: bash startup-recall.sh [agent_id] [optional query terms...]
# Returns compact context block for prompt injection.
# Requires memory API running on localhost:8642

AGENT_ID="${1:-kit}"
shift

# Default queries if none provided
if [ $# -eq 0 ]; then
    QUERIES='["current projects and priorities","recent decisions and changes","known issues and blockers"]'
else
    # Build JSON array from args
    QUERIES="["
    for q in "$@"; do
        QUERIES="${QUERIES}\"${q}\","
    done
    QUERIES="${QUERIES%,}]"
fi

# Hit the fast startup-context endpoint (sub-100ms with warm model)
RESPONSE=$(curl -s --max-time 5 -X POST "http://localhost:8642/api/startup-context" \
    -H "Content-Type: application/json" \
    -d "{\"agent_id\":\"${AGENT_ID}\",\"queries\":${QUERIES},\"top_k_per_query\":3}" 2>/dev/null)

if [ $? -ne 0 ] || [ -z "$RESPONSE" ]; then
    echo "# Supermemory: API unavailable"
    exit 0  # Don't fail agent startup if memory is down
fi

# Extract context field
echo "$RESPONSE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    ctx = data.get('context', '')
    count = data.get('memory_count', 0)
    if ctx and count > 0:
        print(f'# Supermemory Recall ({count} memories)')
        print(ctx)
    else:
        print('# Supermemory: no relevant memories found')
except:
    print('# Supermemory: parse error')
" 2>/dev/null
