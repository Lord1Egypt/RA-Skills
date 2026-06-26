#!/bin/bash
# Ultramemory CLI wrapper. Finds venv and API key automatically.
# Usage: bash scripts/memory.sh <command> [args...]

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# Require ultramemory to be pip-installed
if ! python3 -c "import ultramemory" 2>/dev/null; then
    echo "ERROR: ultramemory not found. Install with: pip install ultramemory" >&2
    exit 1
fi

# Verify API key is set (required for LLM fact extraction during ingest)
if [[ -z "${ANTHROPIC_API_KEY:-}" && -z "${OPENAI_API_KEY:-}" ]]; then
    echo "ERROR: ANTHROPIC_API_KEY or OPENAI_API_KEY must be set for fact extraction." >&2
    echo "Search/recall work without it, but ingest requires an LLM API key." >&2
    echo "Set one in your environment: export ANTHROPIC_API_KEY=sk-ant-..." >&2
    exit 1
fi

exec python3 "$SKILL_DIR/scripts/memory.py" "$@"
