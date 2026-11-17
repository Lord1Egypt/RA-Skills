#!/usr/bin/env bash
# Keep the existing entry point; filesystem and scan checks live in the helper.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/safe_install.py" "$@"
