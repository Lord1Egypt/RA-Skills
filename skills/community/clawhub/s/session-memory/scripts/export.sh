#!/bin/bash
# Export all memories to a single JSON file
# Usage: ./export.sh [-o output.json] [--since YYYY-MM-DD] [--topic T]

set -e

OUTPUT=""
SINCE=""
TOPIC_FILTER=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        -o|--output) OUTPUT="$2"; shift 2 ;;
        --since) SINCE="$2"; shift 2 ;;
        --topic) TOPIC_FILTER="$2"; shift 2 ;;
        *) shift ;;
    esac
done

MEMORY_DIR="${AGENT_MEMORY_DIR:-$HOME/.agent-memory}"

if [ ! -d "$MEMORY_DIR" ]; then
    echo "No memories to export."
    exit 0
fi

RESULT=$(cat "$MEMORY_DIR"/*/*/*.jsonl 2>/dev/null | \
    node -e "
const readline = require('readline');
const rl = readline.createInterface({ input: process.stdin });
const entries = [];
const since = '$SINCE';
const topicFilter = '$TOPIC_FILTER';

rl.on('line', line => {
    try {
        const entry = JSON.parse(line);
        if (since) {
            const sinceTs = new Date(since + 'T00:00:00Z').getTime();
            if (entry.ts < sinceTs) return;
        }
        if (topicFilter && entry.topic !== topicFilter) return;
        entries.push(entry);
    } catch (e) {}
});

rl.on('close', () => {
    entries.sort((a, b) => a.ts - b.ts);
    const output = {
        exported: new Date().toISOString(),
        count: entries.length,
        entries
    };
    console.log(JSON.stringify(output, null, 2));
});
")

if [ -n "$OUTPUT" ]; then
    echo "$RESULT" > "$OUTPUT"
    COUNT=$(echo "$RESULT" | node -e "const d=require('fs').readFileSync('/dev/stdin','utf8');console.log(JSON.parse(d).count)")
    echo "✓ Exported $COUNT memories to $OUTPUT"
else
    echo "$RESULT"
fi
