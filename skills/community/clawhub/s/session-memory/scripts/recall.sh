#!/bin/bash
# Search memories with multi-keyword support and relevance scoring
# Usage: ./recall.sh "query" [--json] [--limit N] [--topic T] [--importance I] [--since YYYY-MM-DD]

set -e

QUERY=""
JSON_MODE=false
LIMIT=10
TOPIC_FILTER=""
IMPORTANCE_FILTER=""
SINCE=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --json) JSON_MODE=true; shift ;;
        --limit) LIMIT="$2"; shift 2 ;;
        --topic) TOPIC_FILTER="$2"; shift 2 ;;
        --importance) IMPORTANCE_FILTER="$2"; shift 2 ;;
        --since) SINCE="$2"; shift 2 ;;
        *) QUERY="$1"; shift ;;
    esac
done

if [ -z "$QUERY" ]; then
    echo "Usage: $0 \"query\" [--json] [--limit N] [--topic T] [--importance I] [--since YYYY-MM-DD]"
    exit 1
fi

MEMORY_DIR="${AGENT_MEMORY_DIR:-$HOME/.agent-memory}"

if [ ! -d "$MEMORY_DIR" ]; then
    echo "No memories found. Start saving with ./save.sh"
    exit 0
fi

# Search through all jsonl files
grep -r -i -h "$QUERY" "$MEMORY_DIR"/*/*/*.jsonl 2>/dev/null | \
    node -e "
const readline = require('readline');
const rl = readline.createInterface({ input: process.stdin });
const results = [];
const jsonMode = $JSON_MODE;
const limit = $LIMIT;
const topicFilter = '$TOPIC_FILTER';
const importanceFilter = '$IMPORTANCE_FILTER';
const since = '$SINCE';
const queryWords = process.argv[1].toLowerCase().split(/\s+/);

const IMPORTANCE_WEIGHT = { critical: 4, high: 3, normal: 2, low: 1 };

rl.on('line', line => {
    try {
        const entry = JSON.parse(line);
        const text = (entry.content + ' ' + entry.topic + ' ' + (entry.tags || []).join(' ')).toLowerCase();

        // Check all query words match (AND logic)
        const matchCount = queryWords.filter(w => text.includes(w)).length;
        if (matchCount === 0) return;

        // Apply filters
        if (topicFilter && entry.topic !== topicFilter) return;
        if (importanceFilter && (entry.importance || 'normal') !== importanceFilter) return;
        if (since) {
            const sinceTs = new Date(since + 'T00:00:00Z').getTime();
            if (entry.ts < sinceTs) return;
        }

        // Relevance score: word matches + importance + recency
        const matchRatio = matchCount / queryWords.length;
        const importanceScore = IMPORTANCE_WEIGHT[entry.importance || 'normal'] || 2;
        const recencyDays = (Date.now() - entry.ts) / (1000 * 60 * 60 * 24);
        const recencyScore = Math.max(0, 1 - recencyDays / 365);

        entry._score = matchRatio * 10 + importanceScore + recencyScore * 2;
        results.push(entry);
    } catch (e) {}
});

rl.on('close', () => {
    results.sort((a, b) => b._score - a._score);
    const limited = results.slice(0, limit);

    if (jsonMode) {
        const clean = limited.map(({_score, ...rest}) => ({...rest, relevance: +_score.toFixed(2)}));
        console.log(JSON.stringify(clean, null, 2));
        return;
    }

    if (limited.length === 0) {
        console.log('No memories found for: ' + process.argv[1]);
        return;
    }

    console.log('Found ' + results.length + ' memories' + (results.length > limit ? ' (showing top ' + limit + ')' : '') + ':\n');
    limited.forEach(m => {
        const date = new Date(m.ts).toISOString().split('T')[0];
        const imp = m.importance && m.importance !== 'normal' ? ' [' + m.importance.toUpperCase() + ']' : '';
        console.log('[' + date + '] [' + m.topic + ']' + imp + ' ' + m.content);
        if (m.tags?.length) console.log('         tags: ' + m.tags.join(', '));
        console.log();
    });

    if (results.length > limit) {
        console.log('... and ' + (results.length - limit) + ' more (use --limit to see more)');
    }
});
" "$QUERY"
