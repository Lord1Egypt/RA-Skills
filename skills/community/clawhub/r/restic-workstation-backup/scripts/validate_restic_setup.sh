#!/usr/bin/env bash
# =============================================================================
# validate_restic_setup.sh — End-to-end validation for restic home backup
# =============================================================================
# Runs: snapshot listing, restore drill, integrity check, and three
# controlled failure drills (wrong secret / unreachable repo / bad env file).
#
# Usage:
#   sudo bash validate_restic_setup.sh [--env-file /etc/home-backup/env]
#
# Expected output: PASS/FAIL per check, exact failing commands, corrective actions.
# =============================================================================
set -uo pipefail

ENV_FILE="${1:-/etc/home-backup/env}"
DRILL_DIR="/tmp/restore-drill"
PASS=0; FAIL=0

ts() { date -u '+%Y-%m-%dT%H:%M:%SZ'; }
BOLD="\033[1m"; RED="\033[31m"; GREEN="\033[32m"; YELLOW="\033[33m"; RESET="\033[0m"

pass() { echo -e "${GREEN}[PASS]${RESET} $*"; (( PASS++ )) || true; }
fail() { echo -e "${RED}[FAIL]${RESET} $*"; (( FAIL++ )) || true; }
info() { echo -e "${YELLOW}[INFO]${RESET} $*"; }
section() { echo -e "\n${BOLD}══ $* ══${RESET}"; }

echo "restic home-backup — end-to-end validation"
echo "Timestamp : $(ts)"
echo "Env file  : ${ENV_FILE}"
echo ""

# ─── Load env ─────────────────────────────────────────────────────────────────
if ! source "${ENV_FILE}" 2>/dev/null; then
  fail "Cannot source env file: ${ENV_FILE}"
  echo "  Corrective: chmod 600 ${ENV_FILE}; verify it exists and is owned by root"
  exit 1
fi

# ─── 1. Snapshot listing ──────────────────────────────────────────────────────
section "1. Snapshot listing"
SNAP_CMD="/usr/bin/restic snapshots --group-by host"
info "Running: ${SNAP_CMD}"
if SNAP_OUT=$(${SNAP_CMD} 2>&1); then
  pass "restic snapshots succeeded"
  echo "${SNAP_OUT}"
else
  fail "restic snapshots failed"
  echo "${SNAP_OUT}"
fi

# ─── 2. Restore drill ─────────────────────────────────────────────────────────
section "2. Restore drill → ${DRILL_DIR}"
rm -rf "${DRILL_DIR}"
mkdir -p "${DRILL_DIR}"

RESTORE_CMD="/usr/bin/restic restore latest --target ${DRILL_DIR}"
info "Running: ${RESTORE_CMD}"
START_E=$(date +%s)
if RESTORE_OUT=$(${RESTORE_CMD} 2>&1); then
  END_E=$(date +%s)
  pass "Restore completed in $(( END_E - START_E ))s"
  echo "${RESTORE_OUT}" | tail -10

  # Determine restored home path
  RESTORED_HOME="${DRILL_DIR}/home/$(basename "${BACKUP_SOURCE}")"

  # Verify canonical files
  declare -A VERIFY_FILES=(
    [".ssh/config"]="${RESTORED_HOME}/.ssh/config"
    ["Documents/roadmap.md"]="${RESTORED_HOME}/Documents/roadmap.md"
    [".config/git/config"]="${RESTORED_HOME}/.config/git/config"
  )
  for label in "${!VERIFY_FILES[@]}"; do
    path="${VERIFY_FILES[$label]}"
    if [[ -f "${path}" ]]; then
      pass "  Restored: ${label}"
    else
      info "  Absent in restore: ${label}  (OK if not present in source)"
    fi
  done
else
  fail "Restore failed"
  echo "${RESTORE_OUT}"
fi

info "Cleaning up ${DRILL_DIR}..."
rm -rf "${DRILL_DIR}"
pass "Restore drill directory cleaned up"

# ─── 3. Repository integrity check ────────────────────────────────────────────
section "3. Repository integrity check"
CHECK_CMD="/usr/bin/restic check --read-data-subset=5%"
info "Running: ${CHECK_CMD}"
START_E=$(date +%s)
if CHECK_OUT=$(${CHECK_CMD} 2>&1); then
  END_E=$(date +%s)
  pass "Repository check passed in $(( END_E - START_E ))s"
  echo "${CHECK_OUT}" | grep -E 'no errors|snapshot|pack|blobs' | head -10 || echo "${CHECK_OUT}" | head -5
else
  fail "Repository check failed"
  echo "${CHECK_OUT}"
fi

# ─── 4. Failure drills ────────────────────────────────────────────────────────
section "4. Controlled failure drills"

# — 4a. Wrong secret ————————————————————————————————————————————————————————
info "4a. Wrong-secret drill"
WRONG_CMD="env RESTIC_PASSWORD=wrong_password_drill RESTIC_PASSWORD_FILE= /usr/bin/restic snapshots"
echo "    Failing command: ${WRONG_CMD}"
if OUT_WRONG=$(${WRONG_CMD} 2>&1); then
  fail "Expected auth failure but command succeeded — investigate!"
else
  pass "Expected failure: wrong password correctly rejected"
  echo "    Output excerpt: $(echo "${OUT_WRONG}" | head -3)"
  echo "    Corrective: verify RESTIC_PASSWORD_FILE in ${ENV_FILE} points to correct file"
fi

# — 4b. Unreachable repository ——————————————————————————————————————————————
info "4b. Unreachable-repository drill"
# Use a deliberately bad SFTP host
UNREACH_CMD="env RESTIC_REPOSITORY=sftp:restic@192.0.2.1:/nonexistent RESTIC_PASSWORD_FILE=${RESTIC_PASSWORD_FILE} /usr/bin/restic snapshots --no-lock"
echo "    Failing command: ${UNREACH_CMD} (192.0.2.1 = TEST-NET, always unreachable)"
# Run with short timeout via timeout(1); restic may wait for SSH
if OUT_UNREACH=$(timeout 15 ${UNREACH_CMD} 2>&1); then
  fail "Expected network failure but command succeeded — investigate!"
else
  pass "Expected failure: unreachable repository correctly errored"
  echo "    Output excerpt: $(echo "${OUT_UNREACH}" | head -3)"
  echo "    Corrective: verify network path to repo host; check SSH known_hosts and firewall"
fi

# — 4c. Unreadable environment file ————————————————————————————————————————
info "4c. Unreadable-env-file drill"
NOREAD_ENV=$(mktemp /tmp/restic-drill-env-XXXX)
chmod 000 "${NOREAD_ENV}"
NOREAD_CMD="bash -c 'source ${NOREAD_ENV}'"
echo "    Failing command: ${NOREAD_CMD}"
if su -s /bin/bash nobody -c "source '${NOREAD_ENV}'" 2>/dev/null; then
  fail "Expected permission error but source succeeded — investigate!"
else
  pass "Expected failure: unreadable env file correctly rejected"
  echo "    Corrective: chmod 600 ${ENV_FILE} && chown root:root ${ENV_FILE}"
fi
chmod 644 "${NOREAD_ENV}" 2>/dev/null; rm -f "${NOREAD_ENV}"

# ─── Summary ──────────────────────────────────────────────────────────────────
section "Validation Summary"
TOTAL=$(( PASS + FAIL ))
echo "Total checks : ${TOTAL}"
echo -e "Passed       : ${GREEN}${PASS}${RESET}"
echo -e "Failed       : ${RED}${FAIL}${RESET}"
echo ""
if [[ ${FAIL} -eq 0 ]]; then
  echo -e "${GREEN}✓ All checks passed — backup system operational${RESET}"
  exit 0
else
  echo -e "${RED}✗ ${FAIL} check(s) failed — review output above${RESET}"
  exit 1
fi
