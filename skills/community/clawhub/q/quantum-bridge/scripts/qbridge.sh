#!/usr/bin/env bash
# qbridge — CLI wrapper for Quantum Bridge API
# Usage: qbridge <command> [args]
#
# Commands:
#   transpile <qasm_file>          Transpile QASM → OriginIR
#   reverse <originir_file>        Reverse OriginIR → QASM
#   validate <originir_file>       Validate OriginIR
#   consensus <agents_json_file>   Run IBC consensus
#   submit <qasm_file> [backend]   Submit to hardware (default: simulator)
#   poll <task_id>                 Poll task result
#   balance                        Check credit balance
#   backends                       List available backends
#   gates                          List supported gates

set -euo pipefail

BASE="${QUANTUM_BRIDGE_URL:-https://quantum-api.gpupulse.dev/api/v1}"
KEY="${QUANTUM_BRIDGE_KEY:-}"

if [[ -z "$KEY" ]]; then
  echo "Error: Set QUANTUM_BRIDGE_KEY env var (get one free at https://quantum-api.gpupulse.dev)" >&2
  exit 1
fi

AUTH="Authorization: Bearer $KEY"
CT="Content-Type: application/json"

cmd="${1:-help}"
shift || true

case "$cmd" in
  transpile)
    file="${1:?Usage: qbridge transpile <file.qasm>}"
    qasm=$(cat "$file")
    curl -s -X POST "$BASE/transpile" -H "$AUTH" -H "$CT" \
      -d "$(jq -n --arg q "$qasm" '{qasm: $q}')"
    ;;
  reverse)
    file="${1:?Usage: qbridge reverse <file.originir>}"
    ir=$(cat "$file")
    curl -s -X POST "$BASE/reverse" -H "$AUTH" -H "$CT" \
      -d "$(jq -n --arg o "$ir" '{originir: $o}')"
    ;;
  validate)
    file="${1:?Usage: qbridge validate <file.originir>}"
    ir=$(cat "$file")
    curl -s -X POST "$BASE/validate" -H "$AUTH" -H "$CT" \
      -d "$(jq -n --arg o "$ir" '{originir: $o}')"
    ;;
  consensus)
    file="${1:?Usage: qbridge consensus <agents.json>}"
    curl -s -X POST "$BASE/consensus" -H "$AUTH" -H "$CT" -d @"$file"
    ;;
  submit)
    file="${1:?Usage: qbridge submit <file.qasm> [simulator|wukong]}"
    backend="${2:-simulator}"
    qasm=$(cat "$file")
    curl -s -X POST "$BASE/submit" -H "$AUTH" -H "$CT" \
      -d "$(jq -n --arg q "$qasm" --arg b "$backend" '{qasm: $q, backend: $b, shots: 1000}')"
    ;;
  poll)
    task_id="${1:?Usage: qbridge poll <task_id>}"
    curl -s "$BASE/submit/$task_id" -H "$AUTH"
    ;;
  balance)
    curl -s "$BASE/balance" -H "$AUTH"
    ;;
  backends)
    curl -s "$BASE/backends" -H "$AUTH"
    ;;
  gates)
    curl -s "$BASE/gates"
    ;;
  *)
    echo "qbridge — Quantum Bridge CLI"
    echo ""
    echo "Commands:"
    echo "  transpile <file.qasm>           QASM → OriginIR (1 credit)"
    echo "  reverse <file.originir>         OriginIR → QASM (1 credit)"
    echo "  validate <file.originir>        Validate OriginIR (free)"
    echo "  consensus <agents.json>         IBC consensus (2 credits)"
    echo "  submit <file.qasm> [backend]    Run on hardware (5-10 credits)"
    echo "  poll <task_id>                  Poll task result"
    echo "  balance                         Check credits"
    echo "  backends                        List backends"
    echo "  gates                           Supported gates"
    echo ""
    echo "Set QUANTUM_BRIDGE_KEY env var first."
    ;;
esac
