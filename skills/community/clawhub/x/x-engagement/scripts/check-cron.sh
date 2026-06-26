#!/bin/bash
set -euo pipefail

# Report local x-engagement runtime state without touching system schedulers.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
RUNTIME_DIR="${SKILL_ROOT}/runtime"
MANUAL_FILE="${RUNTIME_DIR}/manual-reminders.txt"
MEMORY_DIR="${HOME}/memory/daily/hotspots"

echo "=== x-engagement runtime status ==="
echo ""

if [ -f "${MANUAL_FILE}" ]; then
  echo "✓ Manual reminder template: ${MANUAL_FILE}"
else
  echo "✗ Manual reminder template: missing"
fi

if [ -d "${MEMORY_DIR}" ]; then
  echo "✓ Memory directory: ${MEMORY_DIR}"
else
  echo "✗ Memory directory: ${MEMORY_DIR} (missing)"
fi

echo ""
echo "Scheduled automation is disabled by default."
echo "Run maintenance scripts manually after review."
