#!/usr/bin/env bash
# Install Topical hook transforms from the sibling topical skill bundle.
set -euo pipefail

SETUP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOPICAL_SKILL_DIR="${TOPICAL_SKILL_DIR:-${SETUP_DIR}/../topical}"
COPY_SCRIPT="${TOPICAL_SKILL_DIR}/scripts/copy-transforms.sh"

if [[ ! -x "${COPY_SCRIPT}" ]]; then
  echo "Expected topical skill at ${TOPICAL_SKILL_DIR} (copy-transforms.sh missing)." >&2
  echo "If installed from ClawHub, topical assets ship inside @daveangelcode/topical — set TOPICAL_SKILL_DIR." >&2
  exit 1
fi

exec "${COPY_SCRIPT}"
