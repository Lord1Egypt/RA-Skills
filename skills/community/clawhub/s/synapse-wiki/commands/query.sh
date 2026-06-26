#!/bin/bash
# synapse-wiki query — Query the Wiki knowledge base

SKILL_DIR="$HOME/.claude/skills/synapse-wiki"

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: /synapse-wiki query <wiki-root> \"<query>\""
    echo ""
    echo "Examples:"
    echo "  /synapse-wiki query ~/my-wiki \"What is LLM Wiki?\""
    echo "  /synapse-wiki query ~/my-wiki \"RAG vs Wiki tradeoffs\""
    exit 1
fi

WIKI_ROOT="$1"
QUERY="$2"

echo "Querying Synapse Wiki..."
echo "  Wiki: $WIKI_ROOT"
echo "  Query: $QUERY"
echo ""

# Query is handled by LLM - this script just validates input
# The LLM will read wiki/index.md and synthesize an answer

INDEX_FILE="$WIKI_ROOT/wiki/index.md"
if [ ! -f "$INDEX_FILE" ]; then
    echo "Error: Wiki index not found at $INDEX_FILE"
    echo "Please initialize the wiki first or run ingest."
    exit 1
fi

echo "Wiki index found. LLM will synthesize answer from wiki pages."
echo ""
echo "Hint: The LLM will:"
echo "  1. Read wiki/index.md to find relevant pages"
echo "  2. Read the identified pages in full"
echo "  3. Synthesize an answer with citations"
echo "  4. Save answer to outputs/queries/"
echo "  5. Promote valuable answers to wiki/concepts/"
