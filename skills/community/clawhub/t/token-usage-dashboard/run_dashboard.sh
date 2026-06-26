#!/usr/bin/env bash
set -euo pipefail

# One-command launcher for token usage dashboard
# Usage examples:
#   ./run_dashboard.sh
#   ./run_dashboard.sh --provider claude --days 14
#   ./run_dashboard.sh --input /tmp/cost.json --no-open

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT="$ROOT_DIR/scripts/token_usage_dashboard.py"

PROVIDER="codex"
DAYS="30"
SPIKE_LOOKBACK="7"
SPIKE_MULT="2.0"
OUT_HTML="/tmp/token_usage_dashboard.html"
OUT_SUMMARY="/tmp/token_usage_summary.json"
INPUT_PATH=""
OPEN_FLAG="--open"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --provider)
      PROVIDER="$2"; shift 2 ;;
    --days)
      DAYS="$2"; shift 2 ;;
    --spike-lookback-days)
      SPIKE_LOOKBACK="$2"; shift 2 ;;
    --spike-threshold-mult)
      SPIKE_MULT="$2"; shift 2 ;;
    --output)
      OUT_HTML="$2"; shift 2 ;;
    --summary-json)
      OUT_SUMMARY="$2"; shift 2 ;;
    --input)
      INPUT_PATH="$2"; shift 2 ;;
    --no-open)
      OPEN_FLAG=""; shift ;;
    -h|--help)
      sed -n '1,40p' "$0"
      exit 0 ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1 ;;
  esac
done

CMD=(python3 "$SCRIPT" \
  --provider "$PROVIDER" \
  --days "$DAYS" \
  --spike-lookback-days "$SPIKE_LOOKBACK" \
  --spike-threshold-mult "$SPIKE_MULT" \
  --output "$OUT_HTML" \
  --summary-json "$OUT_SUMMARY")

if [[ -n "$INPUT_PATH" ]]; then
  CMD+=(--input "$INPUT_PATH")
fi

if [[ -n "$OPEN_FLAG" ]]; then
  CMD+=(--open)
fi

echo "Running: ${CMD[*]}"
"${CMD[@]}"

echo "Dashboard HTML: $OUT_HTML"
echo "Summary JSON : $OUT_SUMMARY"
