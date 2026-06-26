#!/bin/bash
# Legacy v2 baseline preserved for reference.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
exec "$SCRIPT_DIR/query-memory.sh" "$@"
