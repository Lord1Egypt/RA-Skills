#!/bin/bash

# QMD LLM Query Wrapper
# Automates: LLM expansion → qmd search
#
# Usage:
#   qmd-query-llm.sh "query" [collection] [language]
#   qmd-query-llm.sh --response '{"lex":[...],"vec":[...]}' -c collection
#
# Example:
#   qmd-query-llm.sh "汽车测试流程" memory-root-main zh
#   qmd-query-llm.sh --response '{"lex":["汽车测试"],"vec":["测试流程"]}' -c memory-root-main

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Parse arguments
RESPONSE=""
COLLECTION=".openclaw"
QUERY=""
LANGUAGE="auto"
MODE="prompt"

while [[ $# -gt 0 ]]; do
  case $1 in
    --response)
      MODE="execute"
      RESPONSE="$2"
      shift 2
      ;;
    -c|--collection)
      COLLECTION="$2"
      shift 2
      ;;
    --explain)
      EXPLAIN="--json --explain"
      shift
      ;;
    -h|--help)
      echo "Usage: qmd-query-llm.sh [options]"
      echo ""
      echo "Mode 1 - Generate prompt:"
      echo "  qmd-query-llm.sh \"query\" -c collection -l language"
      echo ""
      echo "Mode 2 - Execute with LLM response:"
      echo "  qmd-query-llm.sh --response '{\"lex\":[...],\"vec\":[...]}' -c collection"
      echo ""
      echo "Options:"
      echo "  -c, --collection   QMD collection (default: .openclaw)"
      echo "  -l, --language     Language: zh, en, auto (default: auto)"
      echo "  --response         JSON response from LLM"
      echo "  --explain          Show score details"
      exit 0
      ;;
    -l|--language)
      LANGUAGE="$2"
      shift 2
      ;;
    *)
      if [ -z "$QUERY" ]; then
        QUERY="$1"
      fi
      shift
      ;;
  esac
done

if [ "$MODE" = "prompt" ]; then
  if [ -z "$QUERY" ]; then
    echo "Usage: qmd-query-llm.sh \"query\" -c collection -l language"
    echo "Example: qmd-query-llm.sh \"汽车测试流程\" memory-root-main zh"
    exit 1
  fi

  echo "🔍 QMD LLM Search"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "Query: $QUERY"
  echo "Collection: $COLLECTION"
  echo "Language: $LANGUAGE"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""

  # Generate LLM prompt
  echo "📝 LLM Prompt (send to your LLM):"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  node "$SCRIPT_DIR/expand-query.js" "$QUERY" "$LANGUAGE"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  echo "💡 After getting LLM response, run:"
  echo "   qmd-query-llm.sh --response '<json>' -c $COLLECTION"

elif [ "$MODE" = "execute" ]; then
  if [ -z "$RESPONSE" ]; then
    echo "Error: --response requires JSON argument"
    exit 1
  fi

  echo "🚀 Executing QMD search with LLM-expanded queries..."
  echo ""

  # Parse JSON and build query using jq (handles spaces in values correctly)
  QUERY_STR=$(echo "$RESPONSE" | jq -r '
    (.lex // []) | map("lex: " + .) | .[]
  ' 2>/dev/null)
  
  VEC_STR=$(echo "$RESPONSE" | jq -r '
    (.vec // []) | map("vec: " + .) | .[]
  ' 2>/dev/null)

  if [ -z "$QUERY_STR" ] && [ -z "$VEC_STR" ]; then
    echo "Error: Invalid JSON response. Expected {\"lex\":[...],\"vec\":[...]}"
    exit 1
  fi

  # Combine lex and vec queries
  if [ -n "$QUERY_STR" ] && [ -n "$VEC_STR" ]; then
    QUERY_STR="$QUERY_STR"$'\n'"$VEC_STR"
  elif [ -n "$VEC_STR" ]; then
    QUERY_STR="$VEC_STR"
  fi

  echo "📋 Expanded queries:"
  echo "$QUERY_STR" | sed 's/$/  /'
  echo ""

  # Execute qmd query
  echo "🔎 Searching..."
  echo ""
  
  if [ -n "$EXPLAIN" ]; then
    qmd query "$QUERY_STR" -c "$COLLECTION" $EXPLAIN
  else
    qmd query "$QUERY_STR" -c "$COLLECTION"
  fi
fi
