#!/bin/bash
# Consolidate memories: group by topic, show summary with counts and date ranges
# Usage: ./consolidate.sh [--since YYYY-MM-DD] [--topic T] [--json]
# Useful for periodic review: see what topics have accumulated

SINCE=""
TOPIC_FILTER=""
JSON_MODE=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --since) SINCE="$2"; shift 2 ;;
        --topic) TOPIC_FILTER="$2"; shift 2 ;;
        --json) JSON_MODE=true; shift ;;
        *) shift ;;
    esac
done

MEMORY_DIR="${AGENT_MEMORY_DIR:-$HOME/.agent-memory}"

if [ ! -d "$MEMORY_DIR" ]; then
    echo "No memories found."
    exit 0
fi

cat "$MEMORY_DIR"/*/*/*.jsonl 2>/dev/null | \
    node -e "
const readline = require('readline');
const rl = readline.createInterface({ input: process.stdin });
const jsonMode = $JSON_MODE;
const since = '$SINCE';
const topicFilter = '$TOPIC_FILTER';

// Group by topic
const topics = {};

rl.on('line', line => {
    try {
        const entry = JSON.parse(line);
        if (since) {
            const sinceTs = new Date(since + 'T00:00:00Z').getTime();
            if (entry.ts < sinceTs) return;
        }
        if (topicFilter && entry.topic !== topicFilter) return;

        if (!topics[entry.topic]) {
            topics[entry.topic] = {
                count: 0,
                oldest: Infinity,
                newest: 0,
                importance: { low: 0, normal: 0, high: 0, critical: 0 },
                tags: {},
                recent: []
            };
        }

        const t = topics[entry.topic];
        t.count++;
        if (entry.ts < t.oldest) t.oldest = entry.ts;
        if (entry.ts > t.newest) t.newest = entry.ts;
        const imp = entry.importance || 'normal';
        t.importance[imp] = (t.importance[imp] || 0) + 1;
        (entry.tags || []).forEach(tag => { t.tags[tag] = (t.tags[tag] || 0) + 1; });
        t.recent.push(entry);
    } catch (e) {}
});

rl.on('close', () => {
    const sorted = Object.entries(topics).sort((a, b) => b[1].count - a[1].count);

    if (jsonMode) {
        const result = sorted.map(([topic, data]) => ({
            topic,
            count: data.count,
            dateRange: {
                from: new Date(data.oldest).toISOString().split('T')[0],
                to: new Date(data.newest).toISOString().split('T')[0]
            },
            importance: Object.fromEntries(Object.entries(data.importance).filter(([,v]) => v > 0)),
            topTags: Object.entries(data.tags).sort((a,b) => b[1] - a[1]).slice(0, 5).map(([t]) => t),
            recentEntries: data.recent.sort((a,b) => b.ts - a.ts).slice(0, 3).map(e => e.content)
        }));
        console.log(JSON.stringify(result, null, 2));
        return;
    }

    if (sorted.length === 0) {
        console.log('No memories found.');
        return;
    }

    console.log('🧠 Memory Consolidation\n');

    sorted.forEach(([topic, data]) => {
        const from = new Date(data.oldest).toISOString().split('T')[0];
        const to = new Date(data.newest).toISOString().split('T')[0];
        const dateRange = from === to ? from : from + ' → ' + to;
        const tags = Object.entries(data.tags).sort((a,b) => b[1] - a[1]).slice(0, 5).map(([t]) => t);

        console.log('━━ ' + topic + ' (' + data.count + ' entries, ' + dateRange + ') ━━');

        if (tags.length > 0) {
            console.log('   tags: ' + tags.join(', '));
        }

        // Show latest 3
        const latest = data.recent.sort((a,b) => b.ts - a.ts).slice(0, 3);
        latest.forEach(m => {
            const date = new Date(m.ts).toISOString().split('T')[0];
            const imp = m.importance && m.importance !== 'normal' ? ' [' + m.importance.toUpperCase() + ']' : '';
            console.log('   [' + date + ']' + imp + ' ' + m.content.slice(0, 100));
        });
        if (data.count > 3) {
            console.log('   ... and ' + (data.count - 3) + ' more');
        }
        console.log();
    });
});
"
