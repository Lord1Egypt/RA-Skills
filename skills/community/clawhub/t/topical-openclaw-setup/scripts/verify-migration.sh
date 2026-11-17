#!/usr/bin/env bash
set -euo pipefail

SETUP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOPICAL_SKILL_DIR="${TOPICAL_SKILL_DIR:-${SETUP_DIR}/../topical}"
VERIFY_SCRIPT="${TOPICAL_SKILL_DIR}/scripts/verify.sh"

if [[ ! -x "${VERIFY_SCRIPT}" ]]; then
  echo "Expected topical skill at ${TOPICAL_SKILL_DIR} (verify.sh missing)." >&2
  exit 1
fi

exec "${VERIFY_SCRIPT}"
