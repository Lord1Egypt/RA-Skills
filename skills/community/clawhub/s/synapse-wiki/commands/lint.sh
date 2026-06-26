#!/bin/bash
# synapse-wiki lint — Run health check on the Wiki

SKILL_DIR="$HOME/.claude/skills/synapse-wiki"

if [ -z "$1" ]; then
    echo "Usage: /synapse-wiki lint <wiki-root>"
    echo ""
    echo "Examples:"
    echo "  /synapse-wiki lint ~/my-wiki"
    echo ""
    echo "Checks:"
    echo "  - Dead links ([[Target]] pointing to non-existent pages)"
    echo "  - Orphan pages (no inbound links)"
    echo "  - Missing from index (not listed in index.md)"
    echo "  - Unlinked concepts (mentioned 3+ times but no page)"
    exit 1
fi

WIKI_ROOT="$1"

echo "Running Synapse Wiki health check..."
echo "  Wiki: $WIKI_ROOT"
echo ""

python3 "$SKILL_DIR/scripts/lint_wiki.py" "$WIKI_ROOT"
