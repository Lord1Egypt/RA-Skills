#!/bin/bash
# Import memories from an exported JSON file
# Usage: ./import.sh backup.json [--dry-run]

set -e

INPUT="${1:?Usage: $0 backup.json [--dry-run]}"
DRY_RUN=false
[[ "${2:-}" == "--dry-run" ]] && DRY_RUN=true

if [ ! -f "$INPUT" ]; then
    echo "Error: file not found: $INPUT"
    exit 1
fi

MEMORY_DIR="${AGENT_MEMORY_DIR:-$HOME/.agent-memory}"

node -e "
const fs = require('fs');
const path = require('path');
const data = JSON.parse(fs.readFileSync(process.argv[1], 'utf8'));
const memDir = process.argv[2];
const dryRun = process.argv[3] === 'true';
const entries = data.entries || data;

if (!Array.isArray(entries)) {
    console.error('Error: expected entries array');
    process.exit(1);
}

let imported = 0, skipped = 0;

entries.forEach(entry => {
    if (!entry.ts || !entry.topic || !entry.content) {
        skipped++;
        return;
    }

    const d = new Date(entry.ts);
    const year = d.getUTCFullYear();
    const month = String(d.getUTCMonth() + 1).padStart(2, '0');
    const day = String(d.getUTCDate()).padStart(2, '0');
    const dir = path.join(memDir, String(year), month);
    const file = path.join(dir, day + '.jsonl');

    if (dryRun) {
        console.log('[dry-run] Would write to ' + file);
        imported++;
        return;
    }

    fs.mkdirSync(dir, { recursive: true });

    // Check for duplicate (same timestamp)
    let exists = false;
    if (fs.existsSync(file)) {
        const lines = fs.readFileSync(file, 'utf8').trim().split('\n');
        exists = lines.some(l => {
            try { return JSON.parse(l).ts === entry.ts; } catch(e) { return false; }
        });
    }

    if (exists) {
        skipped++;
        return;
    }

    fs.appendFileSync(file, JSON.stringify(entry) + '\n');
    imported++;
});

console.log('✓ Imported: ' + imported + (skipped > 0 ? ', skipped: ' + skipped : ''));
if (dryRun) console.log('  (dry run — no files written)');
" "$INPUT" "$MEMORY_DIR" "$DRY_RUN"
