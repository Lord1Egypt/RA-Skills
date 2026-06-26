#!/usr/bin/env bash
# Quick research: run a set of web searches and save raw results
# Usage: research_quick.sh "topic" [freshness: day|week|month|year]
set -euo pipefail

TOPIC="${1:?Usage: research_quick.sh TOPIC [FRESHNESS]}"
FRESHNESS="${2:-month}"
OUTDIR="/tmp/research-$(echo "$TOPIC" | tr ' ' '_' | head -c 40)"
mkdir -p "$OUTDIR"

echo "🔍 Researching: $TOPIC (freshness: $FRESHNESS)"
echo "📁 Output: $OUTDIR"

# This script is a template — actual search calls go through OpenClaw tools.
# Use this as a reference for the search pattern:
#   Query 1: broad topic
#   Query 2: topic + "latest" OR "2026"
#   Query 3: topic + "review" OR "comparison"
#   Query 4: topic + "best practices" OR "guide"

echo "Search pattern for '$TOPIC':"
echo "  1. \"$TOPIC\""
echo "  2. \"$TOPIC latest OR 2026\""
echo "  3. \"$TOPIC review OR comparison\""
echo "  4. \"$TOPIC best practices OR guide\""
echo ""
echo "Run these via web_search tool with freshness=$FRESHNESS"
