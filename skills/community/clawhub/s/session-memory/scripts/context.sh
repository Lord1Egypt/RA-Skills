#!/bin/bash
# Load session context: recent memories + high-importance items
# Usage: ./context.sh [--days N] [--limit N] [--json]
# Designed for session startup: shows what happened recently and what matters

DAYS=3
LIMIT=20
JSON_MODE=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --days) DAYS="$2"; shift 2 ;;
        --limit) LIMIT="$2"; shift 2 ;;
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
const days = $DAYS;
const limit = $LIMIT;

const cutoff = Date.now() - days * 24 * 60 * 60 * 1000;
const recent = [];
const important = [];

const IMPORTANCE_ORDER = { critical: 4, high: 3, normal: 2, low: 1 };

rl.on('line', line => {
    try {
        const entry = JSON.parse(line);
        // Recent entries
        if (entry.ts >= cutoff) {
            recent.push(entry);
        }
        // Always include high/critical importance regardless of age
        const imp = entry.importance || 'normal';
        if (imp === 'high' || imp === 'critical') {
            important.push(entry);
        }
    } catch (e) {}
});

rl.on('close', () => {
    // Deduplicate: merge important into recent if not already there
    const seen = new Set(recent.map(e => e.ts));
    const combined = [...recent];
    important.forEach(e => {
        if (!seen.has(e.ts)) {
            combined.push(e);
            seen.add(e.ts);
        }
    });

    // Sort by importance then recency
    combined.sort((a, b) => {
        const impA = IMPORTANCE_ORDER[a.importance || 'normal'] || 2;
        const impB = IMPORTANCE_ORDER[b.importance || 'normal'] || 2;
        if (impA !== impB) return impB - impA;
        return b.ts - a.ts;
    });

    const limited = combined.slice(0, limit);

    if (jsonMode) {
        console.log(JSON.stringify(limited, null, 2));
        return;
    }

    if (limited.length === 0) {
        console.log('No recent memories (last ' + days + ' days).');
        return;
    }

    console.log('🧠 Session Context (last ' + days + ' days + important items)\n');

    // Group by date
    const byDate = {};
    limited.forEach(m => {
        const date = new Date(m.ts).toISOString().split('T')[0];
        if (!byDate[date]) byDate[date] = [];
        byDate[date].push(m);
    });

    Object.entries(byDate).sort((a, b) => b[0].localeCompare(a[0])).forEach(([date, entries]) => {
        console.log('── ' + date + ' ──');
        entries.forEach(m => {
            const time = new Date(m.ts).toISOString().split('T')[1].slice(0, 5);
            const imp = m.importance && m.importance !== 'normal' ? ' [' + m.importance.toUpperCase() + ']' : '';
            console.log('  [' + time + '] [' + m.topic + ']' + imp + ' ' + m.content);
        });
        console.log();
    });

    console.log('Total: ' + limited.length + ' entries' + (combined.length > limit ? ' (showing ' + limit + ' of ' + combined.length + ')' : ''));
});
"
