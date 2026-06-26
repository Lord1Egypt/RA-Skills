#!/bin/bash
# Memory statistics
# Usage: ./stats.sh [--json]

MEMORY_DIR="${AGENT_MEMORY_DIR:-$HOME/.agent-memory}"
JSON_MODE=false
[[ "${1:-}" == "--json" ]] && JSON_MODE=true

if [ ! -d "$MEMORY_DIR" ]; then
    echo "No memories found."
    exit 0
fi

cat "$MEMORY_DIR"/*/*/*.jsonl 2>/dev/null | \
    node -e "
const readline = require('readline');
const rl = readline.createInterface({ input: process.stdin });
const jsonMode = $JSON_MODE;

let total = 0;
let oldest = Infinity, newest = 0;
const topics = {};
const importance = { low: 0, normal: 0, high: 0, critical: 0 };
const monthly = {};
let totalSize = 0;

rl.on('line', line => {
    try {
        const entry = JSON.parse(line);
        total++;
        totalSize += line.length;
        if (entry.ts < oldest) oldest = entry.ts;
        if (entry.ts > newest) newest = entry.ts;
        topics[entry.topic] = (topics[entry.topic] || 0) + 1;
        const imp = entry.importance || 'normal';
        importance[imp] = (importance[imp] || 0) + 1;
        const month = new Date(entry.ts).toISOString().slice(0, 7);
        monthly[month] = (monthly[month] || 0) + 1;
    } catch (e) {}
});

rl.on('close', () => {
    if (total === 0) {
        console.log('No memories found.');
        return;
    }

    const sortedTopics = Object.entries(topics).sort((a, b) => b[1] - a[1]);
    const days = Math.max(1, Math.ceil((newest - oldest) / (1000 * 60 * 60 * 24)));
    const avgPerDay = (total / days).toFixed(1);

    if (jsonMode) {
        console.log(JSON.stringify({
            total, days, avgPerDay: +avgPerDay,
            oldest: new Date(oldest).toISOString().split('T')[0],
            newest: new Date(newest).toISOString().split('T')[0],
            sizeKB: +(totalSize / 1024).toFixed(1),
            topics: Object.fromEntries(sortedTopics),
            importance,
            monthly
        }, null, 2));
        return;
    }

    console.log('🧠 Memory Statistics\n');
    console.log('  Total entries:  ' + total);
    console.log('  Date range:     ' + new Date(oldest).toISOString().split('T')[0] + ' → ' + new Date(newest).toISOString().split('T')[0]);
    console.log('  Span:           ' + days + ' days (' + avgPerDay + '/day avg)');
    console.log('  Storage:        ' + (totalSize / 1024).toFixed(1) + ' KB');
    console.log();
    console.log('  Topics (' + sortedTopics.length + '):');
    sortedTopics.slice(0, 10).forEach(([t, c]) => {
        console.log('    ' + t + ': ' + c);
    });
    if (sortedTopics.length > 10) console.log('    ... and ' + (sortedTopics.length - 10) + ' more');
    console.log();
    console.log('  Importance:');
    Object.entries(importance).filter(([,v]) => v > 0).forEach(([k, v]) => {
        console.log('    ' + k + ': ' + v);
    });
});
"
