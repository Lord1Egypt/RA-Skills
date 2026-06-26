#!/usr/bin/env bash
# =============================================================================
# install_userlevel_restic.sh — User-level restic backup for hosts without
# system-wide service access (e.g. labvm3 / user bob).
# =============================================================================
# Installs under ~/.config/restic-home/ and ~/.config/systemd/user/.
# Requires 'loginctl enable-linger <user>' for timers to fire without login.
#
# Usage (plan only):
#   bash install_userlevel_restic.sh \
#       --repo "/mnt/offsite/backups/labvm3-home" \
#       --hostname labvm3
#
# Full apply:
#   bash install_userlevel_restic.sh \
#       --repo "/mnt/offsite/backups/labvm3-home" \
#       --hostname labvm3 \
#       --timezone "America/Los_Angeles" \
#       --mail-to sre-oncall@example.com \
#       --keep-daily 14 --keep-weekly 8 --keep-monthly 12 \
#       --apply \
#       --init-repo \
#       --enable-timers \
#       --run-initial-backup
#
# List timers:   systemctl --user list-timers 'restic-home-*'
# Manual backup: systemctl --user start restic-home-backup.service
# Install:       bash install_userlevel_restic.sh --apply [...]
# Remove:        bash install_userlevel_restic.sh --remove
# =============================================================================
set -euo pipefail

# ─── Defaults ─────────────────────────────────────────────────────────────────
USER_NAME="${USER:-$(id -un)}"
HOME_DIR="${HOME:-/home/${USER_NAME}}"
REPO=""
HOSTNAME_TAG="${HOSTNAME:-$(hostname -s)}"
TIMEZONE="America/Los_Angeles"
MAIL_TO="sre-oncall@example.com"
KEEP_DAILY=14
KEEP_WEEKLY=8
KEEP_MONTHLY=12

CONFIG_DIR="${HOME_DIR}/.config/restic-home"
LOG_DIR="${HOME_DIR}/.local/share/restic-home/logs"
BIN_DIR="${HOME_DIR}/.local/bin"
SYSTEMD_DIR="${HOME_DIR}/.config/systemd/user"

APPLY="no"
REMOVE="no"
ENABLE_TIMERS="no"
INIT_REPO="no"
RUN_INITIAL_BACKUP="no"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)           REPO="$2";          shift 2 ;;
    --hostname)       HOSTNAME_TAG="$2";  shift 2 ;;
    --timezone)       TIMEZONE="$2";      shift 2 ;;
    --mail-to)        MAIL_TO="$2";       shift 2 ;;
    --keep-daily)     KEEP_DAILY="$2";    shift 2 ;;
    --keep-weekly)    KEEP_WEEKLY="$2";   shift 2 ;;
    --keep-monthly)   KEEP_MONTHLY="$2";  shift 2 ;;
    --apply)          APPLY="yes";        shift 1 ;;
    --remove)         REMOVE="yes";       shift 1 ;;
    --enable-timers)  ENABLE_TIMERS="yes"; shift 1 ;;
    --init-repo)      INIT_REPO="yes";    shift 1 ;;
    --run-initial-backup) RUN_INITIAL_BACKUP="yes"; shift 1 ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done

# ─── Remove mode ─────────────────────────────────────────────────────────────
if [[ "$REMOVE" == "yes" ]]; then
  echo "=== Removing user-level restic timers and scripts ==="
  systemctl --user disable --now \
    restic-home-backup.timer \
    restic-home-prune.timer \
    restic-home-check.timer 2>/dev/null || true
  rm -f "${SYSTEMD_DIR}/restic-home-backup."{service,timer}
  rm -f "${SYSTEMD_DIR}/restic-home-prune."{service,timer}
  rm -f "${SYSTEMD_DIR}/restic-home-check."{service,timer}
  systemctl --user daemon-reload 2>/dev/null || true
  echo "✓ Units removed. Config files retained in ${CONFIG_DIR}"
  echo "  To fully remove: rm -rf ${CONFIG_DIR} ${LOG_DIR} ${BIN_DIR}/restic-home-*.sh"
  exit 0
fi

# ─── Validate ─────────────────────────────────────────────────────────────────
if [[ -z "$REPO" ]]; then
  echo "ERROR: --repo is required." >&2; exit 2
fi

# ─── Plan output ──────────────────────────────────────────────────────────────
if [[ "$APPLY" != "yes" ]]; then
  cat <<EOF
╔══════════════════════════════════════════════════════════════════╗
║    USER-LEVEL RESTIC BACKUP — PLAN (no changes applied)         ║
╚══════════════════════════════════════════════════════════════════╝

User              : ${USER_NAME}
Source            : ${HOME_DIR}
Repository        : ${REPO}
Hostname tag      : ${HOSTNAME_TAG}
Timezone          : ${TIMEZONE}
Alert email       : ${MAIL_TO}

Secrets (user-private, mode 0600)
  Config dir      : ${CONFIG_DIR}/
  Env file        : ${CONFIG_DIR}/env
  Password file   : ${CONFIG_DIR}/password   (auto-generated if absent)

Exclusions        : ${CONFIG_DIR}/excludes.txt
  **/.cache  **/node_modules  **/.venv  **/.local/share/Trash
  ${HOME_DIR}/Downloads/VMs
  ${HOME_DIR}/.mozilla/firefox/*.default-release/cache2

Retention         : ${KEEP_DAILY}d / ${KEEP_WEEKLY}w / ${KEEP_MONTHLY}m

User systemd timers (require: loginctl enable-linger ${USER_NAME})
  Daily backup    : *-*-* 04:15:00 ${TIMEZONE}  + up to 10 min jitter
  Weekly prune    : Sat *-*-* 05:10:00 ${TIMEZONE}
  Monthly check   : *-*-02 06:20:00 ${TIMEZONE}

Commands
  List timers     : systemctl --user list-timers 'restic-home-*'
  Run backup now  : systemctl --user start restic-home-backup.service
  View logs       : journalctl --user -u restic-home-backup.service -n 40
  Install         : bash \$0 --repo <...> --apply --init-repo --enable-timers
  Remove          : bash \$0 --remove

To apply: re-run with --apply
EOF
  exit 0
fi

# ─── Apply ────────────────────────────────────────────────────────────────────
if ! command -v restic >/dev/null 2>&1; then
  echo "ERROR: restic not installed." >&2; exit 2
fi

echo "=== User-level restic backup install — ${USER_NAME}@${HOSTNAME_TAG} ==="

PASS_FILE="${CONFIG_DIR}/password"
ENV_FILE="${CONFIG_DIR}/env"
EXCLUDES_FILE="${CONFIG_DIR}/excludes.txt"

# ─── Secrets ──────────────────────────────────────────────────────────────────
mkdir -p "${CONFIG_DIR}"
chmod 700 "${CONFIG_DIR}"

if [[ ! -s "${PASS_FILE}" ]]; then
  if command -v openssl >/dev/null 2>&1; then
    openssl rand -base64 48 > "${PASS_FILE}"
  else
    tr -dc 'A-Za-z0-9!@#%^&*()-_=+[]{}:,.?' </dev/urandom | head -c 64 > "${PASS_FILE}"
    echo >> "${PASS_FILE}"
  fi
  chmod 600 "${PASS_FILE}"
  echo "✓ Password generated at ${PASS_FILE} (not printed)"
else
  chmod 600 "${PASS_FILE}"
  echo "✓ Existing password file retained"
fi

cat > "${ENV_FILE}" <<ENVEOF
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

cat > "${EXCLUDES_FILE}" <<'EXEOF'
**/.cache
**/node_modules
**/.venv
**/.local/share/Trash
EXEOF
cat >> "${EXCLUDES_FILE}" <<EXEOF2
${HOME_DIR}/Downloads/VMs
${HOME_DIR}/.mozilla/firefox/*.default-release/cache2
EXEOF2
echo "✓ Env, password, excludes written to ${CONFIG_DIR}"

# ─── Log dir + per-user wrapper ───────────────────────────────────────────────
mkdir -p "${LOG_DIR}" "${BIN_DIR}"

cat > "${BIN_DIR}/restic-home-log-run.sh" <<'WRAPEOF'
#!/usr/bin/env bash
set -euo pipefail
JOB_NAME="${1:?}"; shift; CMD=("$@")
[[ -z "${BACKUP_LOG_DIR:-}" ]] && source "${HOME}/.config/restic-home/env"
LOG_FILE="${BACKUP_LOG_DIR}/${JOB_NAME}.log"
LOCK_FILE="${XDG_RUNTIME_DIR:-/tmp}/restic-${JOB_NAME}.lock"
mkdir -p "${BACKUP_LOG_DIR}"
ts() { date -u '+%Y-%m-%dT%H:%M:%SZ'; }
log() { echo "[$(ts)] $*" | tee -a "${LOG_FILE}"; }
exec 9>"${LOCK_FILE}"; flock -n 9 || { log "SKIP: already running"; exit 0; }
START=$(date +%s); log "START  job=${JOB_NAME}  cmd=${CMD[*]}"
TMPOUT=$(mktemp); EXIT=0; "${CMD[@]}" >>"${TMPOUT}" 2>&1 || EXIT=$?
END=$(date +%s); cat "${TMPOUT}" >>"${LOG_FILE}"; rm -f "${TMPOUT}"
log "END    job=${JOB_NAME}  exit=${EXIT}  elapsed=$(( END - START ))s"
if [[ $EXIT -ne 0 ]] && command -v mail >/dev/null 2>&1; then
  tail -20 "${LOG_FILE}" | mail -s "ALERT: restic ${JOB_NAME} FAILED on ${BACKUP_HOSTNAME}" "${BACKUP_MAIL_TO}" 2>/dev/null || true
fi
exit ${EXIT}
WRAPEOF
chmod 755 "${BIN_DIR}/restic-home-log-run.sh"

# Backup script
cat > "${BIN_DIR}/restic-home-backup.sh" <<BKEOF
#!/usr/bin/env bash
set -euo pipefail
source "${ENV_FILE}"
exec "${BIN_DIR}/restic-home-log-run.sh" backup \
  \$(command -v restic) backup "\${BACKUP_SOURCE}" \
    --exclude-file="\${BACKUP_EXCLUDES_FILE}" \
    --tag "scheduled" --host "\${BACKUP_HOSTNAME}"
BKEOF
chmod 755 "${BIN_DIR}/restic-home-backup.sh"

# Prune script
cat > "${BIN_DIR}/restic-home-prune.sh" <<PREOF
#!/usr/bin/env bash
set -euo pipefail
source "${ENV_FILE}"
exec "${BIN_DIR}/restic-home-log-run.sh" prune \
  \$(command -v restic) forget \
    --keep-daily "\${BACKUP_KEEP_DAILY}" \
    --keep-weekly "\${BACKUP_KEEP_WEEKLY}" \
    --keep-monthly "\${BACKUP_KEEP_MONTHLY}" \
    --group-by "host,paths" --prune
PREOF
chmod 755 "${BIN_DIR}/restic-home-prune.sh"

# Check script
cat > "${BIN_DIR}/restic-home-check.sh" <<CKEOF
#!/usr/bin/env bash
set -euo pipefail
source "${ENV_FILE}"
exec "${BIN_DIR}/restic-home-log-run.sh" check \
  \$(command -v restic) check --read-data-subset=10%
CKEOF
chmod 755 "${BIN_DIR}/restic-home-check.sh"

echo "✓ Scripts written to ${BIN_DIR}"

# ─── Systemd user units ────────────────────────────────────────────────────────
mkdir -p "${SYSTEMD_DIR}"

cat > "${SYSTEMD_DIR}/restic-home-backup.service" <<USVC
[Unit]
Description=Restic home backup for ${USER_NAME}@${HOSTNAME_TAG}
After=network-online.target

[Service]
Type=oneshot
EnvironmentFile=${ENV_FILE}
ExecStart=${BIN_DIR}/restic-home-backup.sh
StandardOutput=journal
StandardError=journal
USVC

cat > "${SYSTEMD_DIR}/restic-home-backup.timer" <<UTIM
[Unit]
Description=Daily restic home backup — 04:15 ${TIMEZONE}

[Timer]
OnCalendar=*-*-* 04:15:00 ${TIMEZONE}
Persistent=true
RandomizedDelaySec=600
AccuracySec=1s
Unit=restic-home-backup.service

[Install]
WantedBy=timers.target
UTIM

cat > "${SYSTEMD_DIR}/restic-home-prune.service" <<USVC2
[Unit]
Description=Restic weekly prune for ${USER_NAME}@${HOSTNAME_TAG}

[Service]
Type=oneshot
EnvironmentFile=${ENV_FILE}
ExecStart=${BIN_DIR}/restic-home-prune.sh
StandardOutput=journal
StandardError=journal
USVC2

cat > "${SYSTEMD_DIR}/restic-home-prune.timer" <<UTIM2
[Unit]
Description=Weekly restic prune — Saturday 05:10 ${TIMEZONE}

[Timer]
OnCalendar=Sat *-*-* 05:10:00 ${TIMEZONE}
Persistent=true
RandomizedDelaySec=600
AccuracySec=1s
Unit=restic-home-prune.service

[Install]
WantedBy=timers.target
UTIM2

cat > "${SYSTEMD_DIR}/restic-home-check.service" <<USVC3
[Unit]
Description=Restic monthly check for ${USER_NAME}@${HOSTNAME_TAG}

[Service]
Type=oneshot
EnvironmentFile=${ENV_FILE}
ExecStart=${BIN_DIR}/restic-home-check.sh
StandardOutput=journal
StandardError=journal
USVC3

cat > "${SYSTEMD_DIR}/restic-home-check.timer" <<UTIM3
[Unit]
Description=Monthly restic check — 2nd of month 06:20 ${TIMEZONE}

[Timer]
OnCalendar=*-*-02 06:20:00 ${TIMEZONE}
Persistent=true
RandomizedDelaySec=600
AccuracySec=1s
Unit=restic-home-check.service

[Install]
WantedBy=timers.target
UTIM3

echo "✓ Systemd user units written to ${SYSTEMD_DIR}"
systemctl --user daemon-reload

# ─── Enable timers ────────────────────────────────────────────────────────────
if [[ "$ENABLE_TIMERS" == "yes" ]]; then
  systemctl --user enable --now \
    restic-home-backup.timer \
    restic-home-prune.timer \
    restic-home-check.timer
  echo "✓ User timers enabled"
fi

# ─── Enable linger (timers fire without active login) ─────────────────────────
if ! loginctl show-user "${USER_NAME}" 2>/dev/null | grep -q 'Linger=yes'; then
  echo "NOTICE: Linger is not enabled for ${USER_NAME}."
  echo "  Timers will NOT fire without an active login session."
  echo "  To enable (requires sudo once):"
  echo "    sudo loginctl enable-linger ${USER_NAME}"
fi

# ─── Init repo ────────────────────────────────────────────────────────────────
if [[ "$INIT_REPO" == "yes" ]]; then
  source "${ENV_FILE}"
  if restic snapshots >/dev/null 2>&1; then
    echo "✓ Repository already initialized"
  else
    restic init && echo "✓ Repository initialized"
  fi
fi

# ─── Initial backup ───────────────────────────────────────────────────────────
if [[ "$RUN_INITIAL_BACKUP" == "yes" ]]; then
  systemctl --user start restic-home-backup.service
  echo "✓ Initial backup started"
fi

cat <<SUMEOF

╔══════════════════════════════════════════════════════════════════╗
║        USER-LEVEL RESTIC BACKUP — INSTALL COMPLETE              ║
╚══════════════════════════════════════════════════════════════════╝

Useful commands:
  List timers  : systemctl --user list-timers 'restic-home-*'
  Run now      : systemctl --user start restic-home-backup.service
  View logs    : journalctl --user -u restic-home-backup.service -n 40
  Snapshots    : source ${ENV_FILE} && restic snapshots
  Remove all   : bash \$0 --remove

Remember: sudo loginctl enable-linger ${USER_NAME}  (if not already done)

SUMEOF
