#!/bin/bash
set -euo pipefail

# Prepare manual reminder templates without modifying system schedulers.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
RUNTIME_DIR="${SKILL_ROOT}/runtime"
MANUAL_FILE="${RUNTIME_DIR}/manual-reminders.txt"

mkdir -p "${RUNTIME_DIR}"

cat > "${MANUAL_FILE}" <<EOF
# x-engagement manual reminder templates
#
# This file is informational only.
# It does not modify crontab, launchd, or any other scheduler.
#
# Recommended manual routines:
#
# 1. Daily hotspot review
#    Run manually when needed:
#    cd "${SKILL_ROOT}" && ./scripts/check-cron.sh
#
# 2. Memory cleanup preview
#    cd "${SKILL_ROOT}" && ./scripts/cleanup-memory.sh
#
# 3. Memory cleanup apply
#    cd "${SKILL_ROOT}" && ./scripts/cleanup-memory.sh --apply
#
# If you later decide to create OS-level reminders, do it manually after review.
EOF

echo "=== x-engagement reminder setup ==="
echo "No persistent tasks were installed."
echo "Created manual reminder template:"
echo "  ${MANUAL_FILE}"
echo ""
echo "Review and run the listed commands manually."
