#!/usr/bin/env bash
# savemaintenance — Shell entry point
# Run the full reconcile pipeline in one command.
# Usage: ./run.sh [--dry]

set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"

echo "═══════════════════════════════════════════════════"
echo "  savemaintenance — Memory System Reconcile"
echo "  $(date)"
echo "═══════════════════════════════════════════════════"
echo ""

if [ "${1:-}" = "--dry" ] || [ "${1:-}" = "-n" ]; then
    echo "▶ DRY RUN — no files will be modified"
    echo ""
    python3 "$DIR/full-reconcile.py" --dry
else
    echo "▶ Taking pre-flight snapshot..."
    python3 "$DIR/snapshot.py"
    echo ""
    
    echo "▶ Running full reconcile..."
    python3 "$DIR/full-reconcile.py"
fi

echo ""
echo "Done."
