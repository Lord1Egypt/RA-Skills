#!/usr/bin/env bash
# ThoughtProof CLI Wrapper — delegates to pot-cli
# MIT-licensed thin wrapper. Pipeline logic lives in pot-cli (BSL).
#
# Commands:
#   tp verify <question>     → pot ask <question>
#   tp deep <question>       → pot deep <question>
#   tp list                  → pot list
#   tp show <n>              → pot show <n>
#   tp config                → pot config

set -euo pipefail

POT_CLI="pot"

if ! command -v "$POT_CLI" &>/dev/null; then
  echo "Error: pot-cli not found. Install with: npm install -g pot-cli"
  exit 1
fi

ACTION="${1:-help}"
shift || true

case "$ACTION" in
  verify|ask)
    $POT_CLI ask "$@"
    ;;
  deep)
    $POT_CLI deep "$@"
    ;;
  list|status)
    $POT_CLI list "$@"
    ;;
  show)
    $POT_CLI show "$@"
    ;;
  config)
    $POT_CLI config
    ;;
  help|--help|-h)
    cat <<EOF
ThoughtProof — Epistemic Verification Protocol

Usage:
  tp verify <question>         Run full verification pipeline
  tp verify --context last     Chain from previous block
  tp verify --tier light|deep  Set verification depth
  tp deep <question>           Deep multi-run with rotated roles
  tp list                      Show block history
  tp show <n>                  Show a specific block
  tp config                    Show current configuration
  tp help                      Show this help

Examples:
  tp verify "Should we use microservices for our MVP?"
  tp verify --context last "What about scaling?"
  tp deep "Is this investment thesis sound?"

More info: https://thoughtproof.ai
EOF
    ;;
  *)
    echo "Unknown command: $ACTION"
    echo "Run 'tp help' for usage."
    exit 1
    ;;
esac
