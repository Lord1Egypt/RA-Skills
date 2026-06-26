#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 <keywords> [limit]" >&2
  exit 1
fi

if ! command -v mcporter >/dev/null 2>&1; then
  echo "mcporter is required but was not found in PATH" >&2
  exit 1
fi

KEYWORDS="$1"
LIMIT="${2:-10}"

mcporter call st-mcp.search_photos keywords="$KEYWORDS" limit="$LIMIT" --output json
