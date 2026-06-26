#!/usr/bin/env bash
# =============================================================================
# bootstrap_restic_home.sh — Production restic home-backup installer v2.0.0
# =============================================================================
# Installs an encrypted, deduplicated, versioned restic backup workflow for a
# Linux home directory backed by a remote SSH/SFTP repository.  Ships systemd
# service+timer units, a logging/retry wrapper, retention scripts, and a
# one-time restore-audit unit.
#
# Default mode: PLAN-ONLY (prints what would happen; makes zero changes).
# Pass --apply to actually write files and configure the system.
#
# Quick usage — plan only:
#   bash bootstrap_restic_home.sh \
#       --user alice \
#       --repo "sftp:backupsvc@10.50.8.24:/srv/backups/home/devbox17"
#
# Full apply (devbox17 reference invocation):
#   sudo bash bootstrap_restic_home.sh \
#       --user alice \
#       --repo "sftp:backupsvc@10.50.8.24:/srv/backups/home/devbox17" \
#       --hostname devbox17 \
#       --timezone "America/Los_Angeles" \
#       --mail-to sre-oncall@example.com \
#       --keep-daily 14 --keep-weekly 8 --keep-monthly 12 \
#       --config-dir /etc/home-backup \
#       --log-dir /var/log/home-backup \
#       --apply \
#       --init-repo \
#       --enable-timers \
#       --run-initial-backup \
#       --archive-legacy-cron \
#       --dry-run-prune
# =============================================================================
set -euo pipefail

# ─── Defaults ─────────────────────────────────────────────────────────────────
USER_NAME=""
REPO=""
HOSTNAME_TAG="${HOSTNAME:-$(hostname -s)}"
TIMEZONE="America/Los_Angeles"
MAIL_TO="sre-oncall@example.com"
KEEP_DAILY=14
KEEP_WEEKLY=8
KEEP_MONTHLY=12
CONFIG_DIR="/etc/home-backup"
LOG_DIR="/var/log/home-backup"
APPLY="no"
ENABLE_TIMERS="no"
INIT_REPO="no"
RUN_INITIAL_BACKUP="no"
ARCHIVE_LEGACY_CRON="no"
DRY_RUN_PRUNE="no"

# ─── Parse args ───────────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --user)             USER_NAME="$2";        shift 2 ;;
    --repo)             REPO="$2";             shift 2 ;;
    --hostname)         HOSTNAME_TAG="$2";     shift 2 ;;
    --timezone)         TIMEZONE="$2";         shift 2 ;;
    --mail-to)          MAIL_TO="$2";          shift 2 ;;
    --keep-daily)       KEEP_DAILY="$2";       shift 2 ;;
    --keep-weekly)      KEEP_WEEKLY="$2";      shift 2 ;;
    --keep-monthly)     KEEP_MONTHLY="$2";     shift 2 ;;
    --config-dir)       CONFIG_DIR="$2";       shift 2 ;;
    --log-dir)          LOG_DIR="$2";          shift 2 ;;
    --apply)            APPLY="yes";           shift 1 ;;
    --enable-timers)    ENABLE_TIMERS="yes";   shift 1 ;;
    --init-repo)        INIT_REPO="yes";       shift 1 ;;
    --run-initial-backup) RUN_INITIAL_BACKUP="yes"; shift 1 ;;
    --archive-legacy-cron) ARCHIVE_LEGACY_CRON="yes"; shift 1 ;;
    --dry-run-prune)    DRY_RUN_PRUNE="yes";  shift 1 ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done

# ─── Validate required args ───────────────────────────────────────────────────
if [[ -z "$USER_NAME" || -z "$REPO" ]]; then
  echo "ERROR: --user and --repo are required." >&2
  exit 2
fi

HOME_DIR="/home/${USER_NAME}"
if [[ "$APPLY" == "yes" && ! -d "$HOME_DIR" ]]; then
  echo "ERROR: Home directory not found: $HOME_DIR" >&2
  exit 2
fi

# ─── Derived paths ────────────────────────────────────────────────────────────
PASS_FILE="${CONFIG_DIR}/password"
ENV_FILE="${CONFIG_DIR}/env"
EXCLUDES_FILE="${CONFIG_DIR}/excludes.txt"
LOCK_DIR="/var/lock"

# ─── PLAN-ONLY output ─────────────────────────────────────────────────────────
plan_banner() {
  cat <<EOF
╔══════════════════════════════════════════════════════════════════╗
║        RESTIC HOME BACKUP — PLAN (no changes applied)           ║
╚══════════════════════════════════════════════════════════════════╝

Backup contract
  User              : ${USER_NAME}
  Source            : ${HOME_DIR}
  Repository        : ${REPO}
  Hostname tag      : ${HOSTNAME_TAG}
  Timezone          : ${TIMEZONE}
  Alert email       : ${MAIL_TO}

Secrets
  Config directory  : ${CONFIG_DIR}  (mode 0700, owner root)
  Environment file  : ${ENV_FILE}    (mode 0600)
  Password file     : ${PASS_FILE}   (mode 0600, auto-generated if absent)
  ⚠  Password is never printed to stdout, stderr, or logs.

Exclusions  (${EXCLUDES_FILE})
  **/.cache
  **/node_modules
  **/.venv
  **/.local/share/Trash
  /home/${USER_NAME}/Downloads/VMs
  /home/${USER_NAME}/.mozilla/firefox/*.default-release/cache2

Retention policy
  Daily   : ${KEEP_DAILY}  copies
  Weekly  : ${KEEP_WEEKLY}  copies
  Monthly : ${KEEP_MONTHLY} copies

Scheduled jobs  (systemd timers, Persistent=true catches up after reboot)
  Daily backup      : *-*-* 04:15:00 ${TIMEZONE}  + up to 10 min random delay
  Weekly prune      : Sat *-*-* 05:10:00 ${TIMEZONE}  + random delay
  Monthly check     : *-*-02 06:20:00 ${TIMEZONE}  + random delay
  ✓ All times are outside the 01:00–03:00 DST transition window.
  ✓ Overlap prevention: flock(1) + systemd Type=oneshot

Retry logic
  Transient errors  : One delayed retry 20 minutes later (systemd-run)
  Auth/perm errors  : No retry; immediate failure + alert
  Retry guard file  : /run/restic-home-backup-retry-pending
    (deleted on success; prevents retry loops)

One-time restore audit
  Fires at          : 2026-04-17 17:00:00 ${TIMEZONE}
  Unit              : restic-home-audit.{service,timer}
  Inspect           : systemctl list-timers restic-home-audit.timer
  Cancel            : systemctl disable --now restic-home-audit.timer

Files that would be written
  ${ENV_FILE}
  ${PASS_FILE}
  ${EXCLUDES_FILE}
  /usr/local/bin/restic-home-backup.sh
  /usr/local/bin/restic-home-prune.sh
  /usr/local/bin/restic-home-check.sh
  /usr/local/bin/restic-home-audit-drill.sh
  /usr/local/bin/restic-home-log-run.sh
  /etc/systemd/system/restic-home-backup.{service,timer}
  /etc/systemd/system/restic-home-prune.{service,timer}
  /etc/systemd/system/restic-home-check.{service,timer}
  /etc/systemd/system/restic-home-audit.{service,timer}
  ${LOG_DIR}/   (log directory, mode 0750)

Legacy cron archival  (--archive-legacy-cron)
  Saves current root crontab to: ${CONFIG_DIR}/legacy-crontab-YYYYMMDD.txt
  Removes entry matching: /usr/local/bin/home-backup

Prune dry-run         (--dry-run-prune)
  Runs: restic forget --dry-run ... and reports without deleting.
  During this engagement NO snapshots will be removed.

To apply, re-run with: --apply
Add: --init-repo --enable-timers --run-initial-backup --archive-legacy-cron

EOF
}

if [[ "$APPLY" != "yes" ]]; then
  plan_banner
  exit 0
fi

# ─── Apply guard: must run as root ────────────────────────────────────────────
if [[ "$(id -u)" != "0" ]]; then
  echo "ERROR: --apply requires root." >&2
  exit 2
fi

if ! command -v restic >/dev/null 2>&1; then
  echo "ERROR: restic is not installed. Run: sudo apt install -y restic" >&2
  exit 2
fi

echo "=== restic home backup bootstrap — APPLY MODE ==="
echo "User: ${USER_NAME}  Repo: ${REPO}  Host: ${HOSTNAME_TAG}"
echo ""

# ─── 1. Config directory + secrets ───────────────────────────────────────────
echo "[1/9] Secrets and config directory..."
install -d -m 0700 -o root -g root "${CONFIG_DIR}"

# Password: generate if absent or empty (never print)
if [[ ! -s "${PASS_FILE}" ]]; then
  echo "      Generating new random password → ${PASS_FILE}"
  if command -v openssl >/dev/null 2>&1; then
    openssl rand -base64 48 > "${PASS_FILE}"
  else
    tr -dc 'A-Za-z0-9!@#%^&*()-_=+[]{}:,.?' </dev/urandom | head -c 64 > "${PASS_FILE}"
    echo >> "${PASS_FILE}"
  fi
  chmod 600 "${PASS_FILE}"
  chown root:root "${PASS_FILE}"
  echo "      ✓ Password generated (not printed). Path: ${PASS_FILE}"
else
  chmod 600 "${PASS_FILE}"
  chown root:root "${PASS_FILE}"
  echo "      ✓ Existing password file retained."
fi

# Env file
cat > "${ENV_FILE}" <<ENVEOF
# restic home-backup environment — root-only, sourced by scripts and systemd
# Do NOT add comments with secret values here.
RESTIC_REPOSITORY=${REPO}
RESTIC_PASSWORD_FILE=${PASS_FILE}
BACKUP_SOURCE=${HOME_DIR}
BACKUP_HOSTNAME=${HOSTNAME_TAG}
BACKUP_EXCLUDES_FILE=${EXCLUDES_FILE}
BACKUP_LOG_DIR=${LOG_DIR}
BACKUP_MAIL_TO=${MAIL_TO}
BACKUP_KEEP_DAILY=${KEEP_DAILY}
BACKUP_KEEP_WEEKLY=${KEEP_WEEKLY}
BACKUP_KEEP_MONTHLY=${KEEP_MONTHLY}
ENVEOF
chmod 600 "${ENV_FILE}"
chown root:root "${ENV_FILE}"
echo "      ✓ ${ENV_FILE}"

# Excludes
cat > "${EXCLUDES_FILE}" <<'EXEOF'
**/.cache
**/node_modules
**/.venv
**/.local/share/Trash
EXEOF
# Append user-specific path exclusions
cat >> "${EXCLUDES_FILE}" <<EXEOF2
/home/${USER_NAME}/Downloads/VMs
/home/${USER_NAME}/.mozilla/firefox/*.default-release/cache2
EXEOF2
chmod 644 "${EXCLUDES_FILE}"
echo "      ✓ ${EXCLUDES_FILE}"

# ─── 2. Log directory ─────────────────────────────────────────────────────────
echo "[2/9] Log directory..."
install -d -m 0750 -o root -g adm "${LOG_DIR}" 2>/dev/null || install -d -m 0750 -o root "${LOG_DIR}"
echo "      ✓ ${LOG_DIR}"

# ─── 3. Logging/retry wrapper ─────────────────────────────────────────────────
echo "[3/9] Logging + retry wrapper..."
cat > /usr/local/bin/restic-home-log-run.sh <<'WRAPEOF'
#!/usr/bin/env bash
# restic-home-log-run.sh — Structured logging + retry wrapper for restic jobs.
# Usage: restic-home-log-run.sh <job-name> <command> [args...]
# Env:   BACKUP_LOG_DIR  BACKUP_MAIL_TO
set -euo pipefail

JOB_NAME="${1:?Usage: restic-home-log-run.sh <job-name> <command> [args...]}"
shift
CMD=("$@")

# Source env if not already loaded by systemd EnvironmentFile
[[ -z "${BACKUP_LOG_DIR:-}" ]] && source /etc/home-backup/env

LOG_FILE="${BACKUP_LOG_DIR}/${JOB_NAME}.log"
RETRY_MARKER="/run/restic-home-backup-retry-pending"
LOCK_FILE="/var/lock/restic-${JOB_NAME}.lock"

mkdir -p "${BACKUP_LOG_DIR}"

ts() { date -u '+%Y-%m-%dT%H:%M:%SZ'; }

logline() { echo "[$(ts)] $*" | tee -a "${LOG_FILE}"; }

# Acquire exclusive lock — exit 0 (not error) if another instance is running
exec 9>"${LOCK_FILE}"
if ! flock -n 9; then
  logline "SKIP: another ${JOB_NAME} instance already running (lock held: ${LOCK_FILE})"
  exit 0
fi

START_EPOCH=$(date +%s)
logline "START  job=${JOB_NAME}  cmd=${CMD[*]}"

# Run and capture output+exit code
TMPOUT=$(mktemp)
EXIT_CODE=0
"${CMD[@]}" >> "${TMPOUT}" 2>&1 || EXIT_CODE=$?

END_EPOCH=$(date +%s)
ELAPSED=$(( END_EPOCH - START_EPOCH ))

# Append captured output to log
cat "${TMPOUT}" >> "${LOG_FILE}"

logline "END    job=${JOB_NAME}  exit=${EXIT_CODE}  elapsed=${ELAPSED}s"

# ─── Success path ─────────────────────────────────────────────────────────────
if [[ ${EXIT_CODE} -eq 0 ]]; then
  rm -f "${RETRY_MARKER}"
  rm -f "${TMPOUT}"
  exit 0
fi

# ─── Failure classification ───────────────────────────────────────────────────
OUTPUT=$(cat "${TMPOUT}")
rm -f "${TMPOUT}"

# Auth/key errors — never retry
if echo "${OUTPUT}" | grep -qiE 'wrong password|no key found|incorrect password'; then
  logline "ERROR_CLASS=auth_failure  RETRY=no  Corrective: verify RESTIC_PASSWORD_FILE"
  send_alert() {
    local subj="ALERT: restic ${JOB_NAME} AUTH FAILURE on ${BACKUP_HOSTNAME}"
    local body="Job: ${JOB_NAME}\nHost: ${BACKUP_HOSTNAME}\nTime: $(ts)\nError: wrong password / no key\nAction: Check ${ENV_FILE} and password file."
    if command -v mail >/dev/null 2>&1 && [[ -n "${BACKUP_MAIL_TO:-}" ]]; then
      printf '%b' "$body" | mail -s "$subj" "${BACKUP_MAIL_TO}" 2>/dev/null || true
    fi
  }
  send_alert
  exit ${EXIT_CODE}
fi

# Permission errors on config files — never retry
if echo "${OUTPUT}" | grep -qiE 'permission denied.*env|cannot open.*password|cannot read.*env'; then
  logline "ERROR_CLASS=perm_failure  RETRY=no  Corrective: chmod 600 ${ENV_FILE} ${PASS_FILE}"
  exit ${EXIT_CODE}
fi

# Transient/network errors — one retry in 20 minutes
if echo "${OUTPUT}" | grep -qiE 'connection refused|no route to host|connection timed out|dial tcp|unable to connect|ssh: connect|network is unreachable|i/o timeout|broken pipe|EOF'; then
  if [[ -f "${RETRY_MARKER}" ]]; then
    logline "ERROR_CLASS=transient  RETRY=no  (already retried once)  Corrective: check network to repo"
    rm -f "${RETRY_MARKER}"
  else
    touch "${RETRY_MARKER}"
    logline "ERROR_CLASS=transient  RETRY=scheduled_in_20min  marker=${RETRY_MARKER}"
    # Queue one-shot retry via systemd-run (not loopable — marker prevents second retry)
    systemd-run --on-active=1200 \
      --description="restic-home-backup one-time retry after transient failure" \
      --unit="restic-home-backup-retry" \
      /usr/local/bin/restic-home-log-run.sh backup \
        /usr/bin/restic backup \
          "${BACKUP_SOURCE}" \
          --exclude-file="${BACKUP_EXCLUDES_FILE}" \
          --tag "retry" \
          2>/dev/null || logline "WARN: systemd-run for retry failed — retry not scheduled"
    logline "RETRY_UNIT=restic-home-backup-retry.service  inspect: systemctl status restic-home-backup-retry.service"
  fi
fi

# Generic failure — alert
if command -v mail >/dev/null 2>&1 && [[ -n "${BACKUP_MAIL_TO:-}" ]]; then
  {
    echo "Job: ${JOB_NAME}"
    echo "Host: ${BACKUP_HOSTNAME:-${HOSTNAME}}"
    echo "Time: $(ts)"
    echo "Exit: ${EXIT_CODE}"
    echo "Elapsed: ${ELAPSED}s"
    echo "---"
    tail -40 "${LOG_FILE}"
  } | mail -s "ALERT: restic ${JOB_NAME} FAILED on ${BACKUP_HOSTNAME:-${HOSTNAME}}" \
      "${BACKUP_MAIL_TO}" 2>/dev/null || true
fi

exit ${EXIT_CODE}
WRAPEOF
chmod 755 /usr/local/bin/restic-home-log-run.sh
echo "      ✓ /usr/local/bin/restic-home-log-run.sh"

# ─── 4. Backup / prune / check / audit scripts ────────────────────────────────
echo "[4/9] Operational scripts..."

cat > /usr/local/bin/restic-home-backup.sh <<'BKEOF'
#!/usr/bin/env bash
# Entrypoint for the daily backup job (called by systemd or directly).
set -euo pipefail
source /etc/home-backup/env
exec /usr/local/bin/restic-home-log-run.sh backup \
  /usr/bin/restic backup "${BACKUP_SOURCE}" \
    --exclude-file="${BACKUP_EXCLUDES_FILE}" \
    --tag "scheduled" \
    --host "${BACKUP_HOSTNAME}"
BKEOF
chmod 755 /usr/local/bin/restic-home-backup.sh

cat > /usr/local/bin/restic-home-prune.sh <<'PREOF'
#!/usr/bin/env bash
# Weekly retention/prune job.
# Pass --dry-run to preview without deleting (used during initial engagement).
set -euo pipefail
source /etc/home-backup/env
DRY=""
[[ "${1:-}" == "--dry-run" ]] && DRY="--dry-run"
exec /usr/local/bin/restic-home-log-run.sh prune \
  /usr/bin/restic forget ${DRY} \
    --keep-daily  "${BACKUP_KEEP_DAILY}" \
    --keep-weekly "${BACKUP_KEEP_WEEKLY}" \
    --keep-monthly "${BACKUP_KEEP_MONTHLY}" \
    --group-by "host,paths" \
    --prune
PREOF
chmod 755 /usr/local/bin/restic-home-prune.sh

cat > /usr/local/bin/restic-home-check.sh <<'CKEOF'
#!/usr/bin/env bash
# Monthly repository integrity check.
set -euo pipefail
source /etc/home-backup/env
exec /usr/local/bin/restic-home-log-run.sh check \
  /usr/bin/restic check --read-data-subset=10%
CKEOF
chmod 755 /usr/local/bin/restic-home-check.sh

cat > /usr/local/bin/restic-home-audit-drill.sh <<AUEOF
#!/usr/bin/env bash
# One-time restore audit drill — fires 2026-04-17 17:00 America/Los_Angeles.
# Restores three canonical files and verifies their existence.
set -euo pipefail
source /etc/home-backup/env

DRILL_DIR="/tmp/restore-drill"
RESTORE_LOG="${BACKUP_LOG_DIR}/audit-drill.log"
ts() { date -u '+%Y-%m-%dT%H:%M:%SZ'; }

log() { echo "[\$(ts)] \$*" | tee -a "\${RESTORE_LOG}"; }

log "=== RESTORE AUDIT DRILL START ==="
log "Host: ${HOSTNAME_TAG}  Repo: \${RESTIC_REPOSITORY}"

rm -rf "\${DRILL_DIR}"
mkdir -p "\${DRILL_DIR}"

log "Restoring latest snapshot to \${DRILL_DIR}..."
/usr/bin/restic restore latest --target "\${DRILL_DIR}" 2>&1 | tee -a "\${RESTORE_LOG}"

VERIFY_FILES=(
  ".ssh/config"
  "Documents/roadmap.md"
  ".config/git/config"
)
PASS_COUNT=0
FAIL_COUNT=0

for rel in "\${VERIFY_FILES[@]}"; do
  FULL="\${DRILL_DIR}/home/${USER_NAME}/\${rel}"
  if [[ -f "\${FULL}" ]]; then
    log "  PRESENT : \${rel}"
    (( PASS_COUNT++ )) || true
  else
    log "  ABSENT  : \${rel}  (may not exist in source — not a failure if source also absent)"
    (( FAIL_COUNT++ )) || true
  fi
done

log "Verification: \${PASS_COUNT} present, \${FAIL_COUNT} absent (absent = file not in source)"
log "Cleaning up \${DRILL_DIR}..."
rm -rf "\${DRILL_DIR}"
log "=== RESTORE AUDIT DRILL COMPLETE ==="

# Alert
if command -v mail >/dev/null 2>&1 && [[ -n "\${BACKUP_MAIL_TO:-}" ]]; then
  tail -30 "\${RESTORE_LOG}" | mail -s "Restore Audit Drill: ${HOSTNAME_TAG} — \${PASS_COUNT} verified, \${FAIL_COUNT} absent" "\${BACKUP_MAIL_TO}" 2>/dev/null || true
fi
AUEOF
chmod 755 /usr/local/bin/restic-home-audit-drill.sh

echo "      ✓ restic-home-backup.sh"
echo "      ✓ restic-home-prune.sh"
echo "      ✓ restic-home-check.sh"
echo "      ✓ restic-home-audit-drill.sh"
echo "      ✓ restic-home-log-run.sh"

# ─── 5. systemd service + timer units ────────────────────────────────────────
echo "[5/9] systemd units..."

# --- backup.service ---
cat > /etc/systemd/system/restic-home-backup.service <<SVCEOF
[Unit]
Description=Restic encrypted home backup for ${USER_NAME}@${HOSTNAME_TAG}
Documentation=file://${CONFIG_DIR}/runbook.md
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
EnvironmentFile=${ENV_FILE}
ExecStart=/usr/local/bin/restic-home-backup.sh
# Prevent second instance from starting if one is already running
# (flock inside the script also protects this)
StandardOutput=journal+console
StandardError=journal+console
SyslogIdentifier=restic-home-backup
# Resource limits
CPUWeight=50
IOWeight=50
SVCEOF

# --- backup.timer ---
cat > /etc/systemd/system/restic-home-backup.timer <<TIMEOF
[Unit]
Description=Daily restic home backup — 04:15 ${TIMEZONE}
Documentation=file://${CONFIG_DIR}/runbook.md

[Timer]
# 04:15 local time — well outside 01:00–03:00 DST window
OnCalendar=*-*-* 04:15:00 ${TIMEZONE}
# Catch up missed runs after reboot
Persistent=true
# Up to 10 minutes of random jitter
RandomizedDelaySec=600
AccuracySec=1s
Unit=restic-home-backup.service

[Install]
WantedBy=timers.target
TIMEOF

# --- prune.service ---
cat > /etc/systemd/system/restic-home-prune.service <<SVCEOF2
[Unit]
Description=Restic retention prune for ${USER_NAME}@${HOSTNAME_TAG}
Documentation=file://${CONFIG_DIR}/runbook.md
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
EnvironmentFile=${ENV_FILE}
ExecStart=/usr/local/bin/restic-home-prune.sh
StandardOutput=journal+console
StandardError=journal+console
SyslogIdentifier=restic-home-prune
CPUWeight=50
IOWeight=50
SVCEOF2

# --- prune.timer ---
cat > /etc/systemd/system/restic-home-prune.timer <<TIMEOF2
[Unit]
Description=Weekly restic prune — Saturday 05:10 ${TIMEZONE}
Documentation=file://${CONFIG_DIR}/runbook.md

[Timer]
OnCalendar=Sat *-*-* 05:10:00 ${TIMEZONE}
Persistent=true
RandomizedDelaySec=600
AccuracySec=1s
Unit=restic-home-prune.service

[Install]
WantedBy=timers.target
TIMEOF2

# --- check.service ---
cat > /etc/systemd/system/restic-home-check.service <<SVCEOF3
[Unit]
Description=Restic monthly integrity check for ${USER_NAME}@${HOSTNAME_TAG}
Documentation=file://${CONFIG_DIR}/runbook.md
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
EnvironmentFile=${ENV_FILE}
ExecStart=/usr/local/bin/restic-home-check.sh
StandardOutput=journal+console
StandardError=journal+console
SyslogIdentifier=restic-home-check
CPUWeight=30
IOWeight=30
SVCEOF3

# --- check.timer ---
cat > /etc/systemd/system/restic-home-check.timer <<TIMEOF3
[Unit]
Description=Monthly restic integrity check — 2nd of month 06:20 ${TIMEZONE}
Documentation=file://${CONFIG_DIR}/runbook.md

[Timer]
OnCalendar=*-*-02 06:20:00 ${TIMEZONE}
Persistent=true
RandomizedDelaySec=600
AccuracySec=1s
Unit=restic-home-check.service

[Install]
WantedBy=timers.target
TIMEOF3

# --- audit.service (one-time restore drill) ---
cat > /etc/systemd/system/restic-home-audit.service <<SVCEOF4
[Unit]
Description=Restic one-time restore audit drill for ${USER_NAME}@${HOSTNAME_TAG}
Documentation=file://${CONFIG_DIR}/runbook.md

[Service]
Type=oneshot
EnvironmentFile=${ENV_FILE}
ExecStart=/usr/local/bin/restic-home-audit-drill.sh
StandardOutput=journal+console
StandardError=journal+console
SyslogIdentifier=restic-home-audit
# Disable after running once (timer has RemainAfterElapse=no)
SVCEOF4

# --- audit.timer (one-shot, 2026-04-17 17:00 LA) ---
cat > /etc/systemd/system/restic-home-audit.timer <<TIMEOF4
[Unit]
Description=One-time restore audit drill 2026-04-17 17:00 ${TIMEZONE}
Documentation=file://${CONFIG_DIR}/runbook.md

[Timer]
OnCalendar=2026-04-17 17:00:00 ${TIMEZONE}
# One-shot — do not persist / catch up
Persistent=false
RemainAfterElapse=no
Unit=restic-home-audit.service

[Install]
WantedBy=timers.target
TIMEOF4

echo "      ✓ restic-home-backup.{service,timer}"
echo "      ✓ restic-home-prune.{service,timer}"
echo "      ✓ restic-home-check.{service,timer}"
echo "      ✓ restic-home-audit.{service,timer}"

systemctl daemon-reload
echo "      ✓ daemon-reload"

# ─── 6. Archive legacy cron ──────────────────────────────────────────────────
echo "[6/9] Legacy cron archival..."
if [[ "$ARCHIVE_LEGACY_CRON" == "yes" ]]; then
  ARCHIVE_FILE="${CONFIG_DIR}/legacy-crontab-$(date +%Y%m%d-%H%M%S).txt"
  if crontab -l >/dev/null 2>&1; then
    crontab -l > "${ARCHIVE_FILE}" 2>/dev/null || true
    chmod 600 "${ARCHIVE_FILE}"
    echo "      ✓ Archived root crontab → ${ARCHIVE_FILE}"
    # Remove the legacy home-backup entry
    CLEANED=$(crontab -l 2>/dev/null | grep -v '/usr/local/bin/home-backup' || true)
    echo "${CLEANED}" | crontab -
    echo "      ✓ Removed legacy '/usr/local/bin/home-backup' entry"
  else
    echo "      ✓ No existing root crontab found — nothing to archive"
  fi
else
  echo "      (skipped — pass --archive-legacy-cron to enable)"
fi

# ─── 7. Enable timers ─────────────────────────────────────────────────────────
echo "[7/9] Enabling systemd timers..."
if [[ "$ENABLE_TIMERS" == "yes" ]]; then
  systemctl enable --now \
    restic-home-backup.timer \
    restic-home-prune.timer \
    restic-home-check.timer \
    restic-home-audit.timer
  echo "      ✓ All four timers enabled and started"
  systemctl list-timers 'restic-home-*' --no-pager 2>/dev/null || true
else
  echo "      (skipped — pass --enable-timers to enable)"
fi

# ─── 8. Init repository ───────────────────────────────────────────────────────
echo "[8/9] Repository initialization..."
if [[ "$INIT_REPO" == "yes" ]]; then
  source "${ENV_FILE}"
  if /usr/bin/restic snapshots >/dev/null 2>&1; then
    echo "      ✓ Repository already initialized — skipping init"
  else
    echo "      Initializing repository at ${RESTIC_REPOSITORY}..."
    /usr/bin/restic init 2>&1
    echo "      ✓ Repository initialized"
  fi
else
  echo "      (skipped — pass --init-repo to enable)"
fi

# ─── 9. Initial backup + optional dry-run prune ──────────────────────────────
echo "[9/9] Initial backup..."
if [[ "$RUN_INITIAL_BACKUP" == "yes" ]]; then
  echo "      Running first backup (this may take several minutes)..."
  systemctl start restic-home-backup.service
  echo "      ✓ Initial backup job started via systemd"
  # Wait for completion
  sleep 2
  systemctl is-active restic-home-backup.service 2>/dev/null || true
  journalctl -u restic-home-backup.service -n 20 --no-pager 2>/dev/null || true
else
  echo "      (skipped — pass --run-initial-backup to enable)"
fi

if [[ "$DRY_RUN_PRUNE" == "yes" ]]; then
  echo ""
  echo "=== DRY-RUN PRUNE (no snapshots removed) ==="
  source "${ENV_FILE}"
  /usr/bin/restic forget --dry-run \
    --keep-daily  "${BACKUP_KEEP_DAILY}" \
    --keep-weekly "${BACKUP_KEEP_WEEKLY}" \
    --keep-monthly "${BACKUP_KEEP_MONTHLY}" \
    --group-by "host,paths" 2>&1 || true
  echo "=== END DRY-RUN PRUNE ==="
fi

# ─── Summary ──────────────────────────────────────────────────────────────────
cat <<SUMEOF

╔══════════════════════════════════════════════════════════════════╗
║              RESTIC HOME BACKUP — APPLY COMPLETE                ║
╚══════════════════════════════════════════════════════════════════╝

Config            : ${CONFIG_DIR}
Env file          : ${ENV_FILE}
Password file     : ${PASS_FILE}  (root-only, never printed)
Excludes          : ${EXCLUDES_FILE}
Logs              : ${LOG_DIR}/

Scripts written to /usr/local/bin/:
  restic-home-backup.sh   restic-home-prune.sh
  restic-home-check.sh    restic-home-audit-drill.sh
  restic-home-log-run.sh

Systemd units in /etc/systemd/system/:
  restic-home-backup.{service,timer}   → daily    04:15 ${TIMEZONE}
  restic-home-prune.{service,timer}    → Saturday 05:10 ${TIMEZONE}
  restic-home-check.{service,timer}    → 2nd/mo   06:20 ${TIMEZONE}
  restic-home-audit.{service,timer}    → one-shot 2026-04-17 17:00 ${TIMEZONE}

Timers enabled    : ${ENABLE_TIMERS}
Repo initialized  : ${INIT_REPO}
Initial backup    : ${RUN_INITIAL_BACKUP}
Legacy cron saved : ${ARCHIVE_LEGACY_CRON}
Dry-run prune     : ${DRY_RUN_PRUNE}

Restore audit timer:
  Inspect  : systemctl list-timers restic-home-audit.timer
  Cancel   : systemctl disable --now restic-home-audit.timer
  Re-run   : systemctl start restic-home-audit.service

Verify setup:
  source ${ENV_FILE} && /usr/bin/restic snapshots
  journalctl -u restic-home-backup.service -n 40 --no-pager
  systemctl list-timers 'restic-home-*' --no-pager

SUMEOF
