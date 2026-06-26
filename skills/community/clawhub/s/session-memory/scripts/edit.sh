#!/bin/bash
# Edit or delete a memory entry by timestamp
# Usage: ./edit.sh <timestamp_ms> --content "new content"
#        ./edit.sh <timestamp_ms> --topic "new topic"
#        ./edit.sh <timestamp_ms> --importance high
#        ./edit.sh <timestamp_ms> --delete

set -e

TS="${1:?Usage: $0 <timestamp_ms> [--content text] [--topic text] [--importance level] [--delete]}"
shift

NEW_CONTENT=""
NEW_TOPIC=""
NEW_IMPORTANCE=""
DELETE=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --content) NEW_CONTENT="$2"; shift 2 ;;
        --topic) NEW_TOPIC="$2"; shift 2 ;;
        --importance) NEW_IMPORTANCE="$2"; shift 2 ;;
        --delete) DELETE=true; shift ;;
        *) shift ;;
    esac
done

MEMORY_DIR="${AGENT_MEMORY_DIR:-$HOME/.agent-memory}"

# Find the file containing this timestamp
FOUND=$(grep -r -l "\"ts\":$TS" "$MEMORY_DIR"/*/*/*.jsonl 2>/dev/null | head -1)

if [ -z "$FOUND" ]; then
    echo "Error: no memory found with timestamp $TS"
    exit 1
fi

node -e "
const fs = require('fs');
const file = process.argv[1];
const ts = parseInt(process.argv[2]);
const newContent = process.argv[3] || '';
const newTopic = process.argv[4] || '';
const newImportance = process.argv[5] || '';
const doDelete = process.argv[6] === 'true';

const lines = fs.readFileSync(file, 'utf8').trim().split('\n');
const result = [];
let found = false;

lines.forEach(line => {
    try {
        const entry = JSON.parse(line);
        if (entry.ts === ts) {
            found = true;
            if (doDelete) {
                console.log('✓ Deleted: [' + entry.topic + '] ' + entry.content.slice(0, 60));
                return; // skip this entry
            }
            if (newContent) entry.content = newContent;
            if (newTopic) entry.topic = newTopic;
            if (newImportance) entry.importance = newImportance;
            console.log('✓ Updated: [' + entry.topic + '] ' + entry.content.slice(0, 60));
        }
        result.push(JSON.stringify(entry));
    } catch (e) {
        result.push(line); // preserve unparseable lines
    }
});

if (!found) {
    console.error('Error: entry not found in file');
    process.exit(1);
}

fs.writeFileSync(file, result.join('\n') + '\n');
" "$FOUND" "$TS" "$NEW_CONTENT" "$NEW_TOPIC" "$NEW_IMPORTANCE" "$DELETE"
