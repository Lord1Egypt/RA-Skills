#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${SCHELLING_URL:-https://schellingprotocol.com}"

usage() {
  cat >&2 <<EOF
Usage: $0 [options]

Search for agents on the Schelling Protocol network.

Options:
  --freelancer             Filter to freelancer agents only
  --availability <value>   Filter by availability: available, busy, offline
  --skills <csv>           Filter by skills (comma-separated, e.g. "python,llm")
  --page <n>               Page number (default: 1)
  --limit <n>              Results per page, max 100 (default: 20)
  -h, --help               Show this help

Examples:
  $0
  $0 --freelancer
  $0 --skills "research,summarization" --availability available
  $0 --page 2 --limit 50

Environment:
  SCHELLING_URL  Override base URL (default: https://schellingprotocol.com)
EOF
  exit 0
}

PARAMS=""
PAGE="1"
LIMIT="20"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --freelancer)       PARAMS="${PARAMS}&is_freelancer=1"; shift ;;
    --availability)     PARAMS="${PARAMS}&availability=$2"; shift 2 ;;
    --skills)           PARAMS="${PARAMS}&skills=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$2" 2>/dev/null || echo "$2")"; shift 2 ;;
    --page)             PAGE="$2"; shift 2 ;;
    --limit)            LIMIT="$2"; shift 2 ;;
    -h|--help)          usage ;;
    *)                  echo "Unknown option: $1" >&2; usage ;;
  esac
done

PARAMS="${PARAMS}&page=${PAGE}&limit=${LIMIT}"
# Trim leading &
PARAMS="${PARAMS#&}"

RESPONSE=$(curl -sf \
  "${BASE_URL}/api/cards?${PARAMS}") || {
    echo "Error: Request failed." >&2
    exit 1
  }

if command -v jq &>/dev/null; then
  echo "$RESPONSE" | jq .
else
  echo "$RESPONSE"
fi
