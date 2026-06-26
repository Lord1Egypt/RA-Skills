#!/usr/bin/env bash
# shopify-tool.sh — Unified launcher for Shopify AI Toolkit scripts
# Usage: ./shopify-tool.sh <skill> <command> [args...]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

SKILL="$1"
COMMAND="$2"
shift 2

case "$SKILL" in
  admin|storefront)
    SEARCH_SCRIPT="$SCRIPT_DIR/search_docs.mjs"
    VALIDATE_SCRIPT="$SCRIPT_DIR/validate.mjs"
    ;;
  liquid)
    SEARCH_SCRIPT="$SCRIPT_DIR/liquid_search_docs.mjs"
    VALIDATE_SCRIPT="$SCRIPT_DIR/liquid_validate.mjs"
    ;;
  hydrogen)
    SEARCH_SCRIPT="$SCRIPT_DIR/hydrogen_search_docs.mjs"
    VALIDATE_SCRIPT="$SCRIPT_DIR/hydrogen_validate.mjs"
    ;;
  functions)
    SEARCH_SCRIPT="$SCRIPT_DIR/functions_search_docs.mjs"
    VALIDATE_SCRIPT="$SCRIPT_DIR/functions_validate.mjs"
    ;;
  *)
    echo "Usage: $0 <admin|storefront|liquid|hydrogen|functions> <search|validate> [args...]"
    echo ""
    echo "Skills:"
    echo "  admin         — Admin GraphQL API (products, orders, customers)"
    echo "  storefront    — Storefront GraphQL API (carts, checkout)"
    echo "  liquid         — Liquid theme templates"
    echo "  hydrogen       — Shopify Hydrogen framework"
    echo "  functions      — Shopify Functions (discounts, validators)"
    exit 1
    ;;
esac

case "$COMMAND" in
  search)
    node "$SEARCH_SCRIPT" "$@"
    ;;
  validate)
    node "$VALIDATE_SCRIPT" "$@"
    ;;
  *)
    echo "Commands: search, validate"
    exit 1
    ;;
esac
