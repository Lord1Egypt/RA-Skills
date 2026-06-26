#!/bin/bash
# synapse-wiki init — Initialize a new Wiki knowledge base

SKILL_DIR="$HOME/.claude/skills/synapse-wiki"

if [ -z "$1" ]; then
    echo "Usage: /synapse-wiki init <wiki-root> [Topic Name]"
    echo ""
    echo "Examples:"
    echo "  /synapse-wiki init ~/my-wiki \"AI Learning Knowledge Base\""
    echo "  /synapse-wiki init ~/project-docs"
    exit 1
fi

WIKI_ROOT="$1"
TOPIC="${2:-Knowledge Base}"

echo "Initializing Synapse Wiki..."
echo "  Root: $WIKI_ROOT"
echo "  Topic: $TOPIC"
echo ""

python3 "$SKILL_DIR/scripts/scaffold.py" "$WIKI_ROOT" "$TOPIC"
