#!/usr/bin/env bash
# error-detector.sh — Log a non-obvious error to SQLite-backed memory.
# Usage: ./error-detector.sh <type> <detail> [pattern-key]
#   type: short error category (e.g., "Docker build failed on Apple Silicon")
#   detail: full error context
#   pattern-key: optional namespaced key (default: inferred from type)
set -euo pipefail

WORKSPACE_ROOT="${OPENCLAW_WORKSPACE:-$(pwd)}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LEARNINGS_CLI="$SCRIPT_DIR/scripts/learnings.py"

ERROR_TYPE="${1:-}"
ERROR_DETAIL="${2:-}"
PATTERN_KEY="${3:-}"

# Require at least an error type
if [ -z "$ERROR_TYPE" ]; then
    exit 0
fi

# Derive pattern key from type if not provided
if [ -z "$PATTERN_KEY" ]; then
    # Sanitize: lowercase, replace spaces with hyphens, strip non-alphanumeric
    PATTERN_KEY="tool:$(echo "$ERROR_TYPE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g' | sed 's/--*/-/g; s/^-//; s/-$//')"
fi

# Only log via SQLite CLI — no markdown fallback
if [ -f "$LEARNINGS_CLI" ]; then
    python3 "$LEARNINGS_CLI" --root "$WORKSPACE_ROOT" log-error \
        --summary "$ERROR_TYPE" \
        --details "$ERROR_DETAIL" \
        --pattern "$PATTERN_KEY" \
        >/dev/null 2>&1 || true
    echo "[error-detector] Logged error → SQLite (pattern: $PATTERN_KEY)"
fi
