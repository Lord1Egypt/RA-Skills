#!/bin/bash
# record_outcome.sh wrapper - passes --lang from environment or first arg
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "${SCRIPT_DIR}/record_outcome.py" "$@"
