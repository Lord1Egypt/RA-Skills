#!/bin/bash
# synapse-wiki ingest — Ingest a source file into the Wiki

SKILL_DIR="$HOME/.claude/skills/synapse-wiki"

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: /synapse-wiki ingest <wiki-root> <source-file>"
    echo ""
    echo "Examples:"
    echo "  /synapse-wiki ingest ~/my-wiki raw/articles/article.md"
    echo "  /synapse-wiki ingest ~/my-wiki raw/papers/paper.pdf"
    exit 1
fi

WIKI_ROOT="$1"
SOURCE_FILE="$2"

echo "Ingesting source into Synapse Wiki..."
echo "  Wiki: $WIKI_ROOT"
echo "  Source: $SOURCE_FILE"
echo ""

python3 "$SKILL_DIR/scripts/ingest.py" "$WIKI_ROOT" "$SOURCE_FILE"
