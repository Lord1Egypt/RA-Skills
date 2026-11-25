#!/usr/bin/env bash
# Space Duck listener supervision — keep BYOB receivers alive across reboots.
#
# Why this exists:
#   Containerised hosts (Docker, Hostinger, LXC) often lack systemd. The
#   common `nohup python3 telegram_listener.py &` pattern silently dies on
#   container restart. Pecks land at a dead URL, listener_state goes stale,
#   and the duck looks "connected but unresponsive" — exactly the failure
#   Sam Aldrin Bot exhibited 2026-06-12.
#
#   This script installs a user-level supervisord (no root, no apt) that
#   keeps telegram_listener.py + peck_listener.py alive with auto-restart,
#   log capture, and easy status/stop.
#
# Usage:
#   ./setup_listeners_supervised.sh                 # fresh install
#   ./setup_listeners_supervised.sh --status        # current state
#   ./setup_listeners_supervised.sh --stop          # stop all listeners
#   ./setup_listeners_supervised.sh --restart       # bounce all listeners
#   ./setup_listeners_supervised.sh --uninstall     # remove + clean up
#
# Layout:
#   ~/.space-duck/supervisor/supervisord.conf       # main config
#   ~/.space-duck/supervisor/supervisord.sock       # control socket
#   ~/.space-duck/supervisor/supervisord.log        # supervisord's own log
#   ~/.space-duck/supervisor/supervisord.pid        # supervisord PID file
#   ~/.space-duck/logs/telegram_listener.{log,err}  # listener output
#   ~/.space-duck/logs/peck_listener.{log,err}
#
# Container-restart behavior:
#   supervisord itself is not auto-started by the container — that's the
#   responsibility of your container init (CMD/ENTRYPOINT). What this gives
#   you is: once supervisord IS running, the listeners stay up.
#
#   For TRUE survive-restart, add this to your container entrypoint:
#       ~/.local/bin/supervisord -c ~/.space-duck/supervisor/supervisord.conf
#   The script prints the exact line to add at the end of a fresh install.

set -euo pipefail

SD_DIR="${HOME}/.space-duck"
SUP_DIR="${SD_DIR}/supervisor"
LOG_DIR="${SD_DIR}/logs"
SUP_CONF="${SUP_DIR}/supervisord.conf"
SUP_PID="${SUP_DIR}/supervisord.pid"
SUP_SOCK="${SUP_DIR}/supervisord.sock"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TG_LISTENER="${SCRIPT_DIR}/telegram_listener.py"
PECK_LISTENER="${SCRIPT_DIR}/peck_listener.py"
PECK_RESPONDER="${SCRIPT_DIR}/peck_responder.py"
REPLY_HOOK="${SCRIPT_DIR}/reply_with_claude.sh"
PULSE_SCRIPT="${SCRIPT_DIR}/pulse.py"

die()  { echo "✗ $*" >&2; exit 1; }
ok()   { echo "✓ $*"; }
info() { echo "→ $*"; }
warn() { echo "⚠ $*" >&2; }

# 0.8.6 — F1: kill -0 returns EPERM for a live process under another uid;
# only "no such process" means dead. Check /proc + the error text.
# Without this, this script mis-reads a live supervisord under root as
# dead and races a duplicate on port 8788 (HARDEN-071 rerun).
proc_alive() {
  local pid="$1"
  [[ -n "$pid" ]] || return 1
  if kill -0 "$pid" 2>/dev/null; then return 0; fi
  [[ -d "/proc/$pid" ]] && return 0
  kill -0 "$pid" 2>&1 | grep -qi 'not permitted' && return 0
  return 1
}

# ─────────────────────────────── action: status ───────────────────────────────
cmd_status() {
  if [[ ! -f "$SUP_PID" ]] || ! proc_alive "$(cat "$SUP_PID")"; then  # 0.8.6 — F1
    echo "supervisord: NOT RUNNING"
    echo "  Start with: $0  (without args)"
    exit 1
  fi
  echo "supervisord PID: $(cat "$SUP_PID")"
  echo ""
  ~/.local/bin/supervisorctl -c "$SUP_CONF" status 2>&1 || \
    warn "supervisorctl status failed — config or socket issue"
}

# ─────────────────────────────── action: stop ─────────────────────────────────
cmd_stop() {
  if [[ ! -f "$SUP_PID" ]] || ! proc_alive "$(cat "$SUP_PID")"; then  # 0.8.6 — F1
    info "supervisord not running; nothing to stop"
    exit 0
  fi
  info "Stopping supervised listeners and supervisord itself..."
  ~/.local/bin/supervisorctl -c "$SUP_CONF" stop all 2>&1 || true
  ~/.local/bin/supervisorctl -c "$SUP_CONF" shutdown 2>&1 || true
  # Give it a moment, then verify
  sleep 2
  if [[ -f "$SUP_PID" ]] && proc_alive "$(cat "$SUP_PID")"; then  # 0.8.6 — F1
    warn "supervisord still running after shutdown — sending SIGTERM"
    kill -TERM "$(cat "$SUP_PID")"
  fi
  ok "Stopped."
}

# ─────────────────────────────── action: restart ──────────────────────────────
cmd_restart() {
  if [[ ! -f "$SUP_PID" ]] || ! proc_alive "$(cat "$SUP_PID")"; then  # 0.8.6 — F1
    info "supervisord not running — performing fresh start"
    cmd_install
    exit 0
  fi
  info "Bouncing supervised listeners (supervisord itself stays up)..."
  ~/.local/bin/supervisorctl -c "$SUP_CONF" restart all
  ok "Restarted."
}

# ─────────────────────────────── action: uninstall ────────────────────────────
cmd_uninstall() {
  info "Stopping anything running..."
  cmd_stop || true
  info "Removing supervisor config + logs..."
  rm -rf "$SUP_DIR" "$LOG_DIR"
  ok "Removed ~/.space-duck/supervisor/ and ~/.space-duck/logs/"
  warn "supervisord package itself (~/.local/bin/supervisord) NOT removed — pip uninstall manually if desired."
}

# ─────────────────────────────── helper: ensure supervisord installed ─────────
ensure_supervisord() {
  if command -v supervisord >/dev/null 2>&1 || [[ -x ~/.local/bin/supervisord ]]; then
    ok "supervisord already installed"
    return
  fi
  info "Installing supervisord via pip --user..."
  # Try regular pip first, fall back to --break-system-packages for PEP 668
  if ! python3 -m pip install --user supervisor 2>/dev/null; then
    info "Retrying with --break-system-packages (PEP 668 environment)..."
    python3 -m pip install --user --break-system-packages supervisor \
      || die "supervisord install failed — install Python pip first"
  fi
  # Verify
  [[ -x ~/.local/bin/supervisord ]] || die "supervisord binary not found at ~/.local/bin/supervisord after install"
  ok "supervisord installed at ~/.local/bin/supervisord"
}

# ─────────────────────────────── action: install (default) ────────────────────
cmd_install() {
  info "Setting up supervised Space Duck listeners under $SD_DIR"

  # Prereqs
  [[ -f "$TG_LISTENER" ]] || die "telegram_listener.py missing at $TG_LISTENER — run from the skill's scripts/ dir"
  [[ -f "$PECK_LISTENER" ]] || die "peck_listener.py missing at $PECK_LISTENER — run from the skill's scripts/ dir"
  [[ -f "$PECK_RESPONDER" ]] || die "peck_responder.py missing at $PECK_RESPONDER — required for auto-reply (v0.4.7)"
  [[ -f "$REPLY_HOOK" ]] || die "reply_with_claude.sh missing at $REPLY_HOOK — required for plain-DM auto-reply (v0.4.16)"
  [[ -f "${SD_DIR}/config.json" ]] || die "no ~/.space-duck/config.json — pair this agent first via 'python3 pair.py'"
  command -v python3 >/dev/null || die "python3 not in PATH"

  # v0.4.7 — brain-runtime check. peck_responder.py invokes `claude` CLI to
  # compose auto-replies. Without it, the responder will fire but log
  # "claude CLI not found" and not actually reply. Warn loudly here so the
  # operator knows what they're missing.
  if ! command -v claude >/dev/null 2>&1; then
    warn "claude CLI not on PATH — auto-reply will be DISABLED."
    warn "  peck_responder.py will receive pecks but cannot compose replies."
    warn "  Install: https://docs.claude.com/claude-code/install — then re-run this script."
    warn "  Continuing install; everything else still works (listening, owner-approval, file sync)."
  else
    ok "claude CLI present at $(command -v claude) — auto-reply enabled"
  fi

  ensure_supervisord

  # Layout
  mkdir -p "$SUP_DIR" "$LOG_DIR"
  chmod 700 "$SUP_DIR"

  # If something is already running under our PID file, refuse to overwrite
  if [[ -f "$SUP_PID" ]] && proc_alive "$(cat "$SUP_PID")"; then  # 0.8.6 — F1
    warn "supervisord already running (PID $(cat "$SUP_PID")) — use --restart to bounce, or --status to inspect"
    exit 0
  fi
  # [HARDEN-071] The pidfile guard alone races: two same-second invocations
  # (e.g. heal path + manual start) each see no pidfile and both launch a
  # daemon on the same conf/socket (field incident: dual supervisord PIDs
  # 519/521, listener crash-loop on :8788). Also catch pidfile-less daemons.
  local other_sup
  other_sup="$(pgrep -f "supervisord.*${SUP_CONF}" 2>/dev/null || true)"
  if [[ -n "$other_sup" ]]; then
    warn "A supervisord using $SUP_CONF is already running (PID(s): $other_sup) but the pidfile is missing/stale."
    die "Refusing to start a second daemon. Kill it first (kill -TERM $other_sup) or use --restart."
  fi
  # Stale PID file? Clean up.
  rm -f "$SUP_PID" "$SUP_SOCK"

  # Detect any pre-existing nohup listeners — warn the operator (we won't kill them)
  local pre_existing
  pre_existing="$(pgrep -fa 'telegram_listener\.py\|peck_listener\.py' 2>/dev/null | grep -v supervisord || true)"
  if [[ -n "$pre_existing" ]]; then
    # [HARDEN-071] duplicates restart-loop on 'Address already in use'
    # and flood the .err logs — abort instead of spawning alongside.
    warn "Found existing listener processes — installing supervisord alongside WILL create duplicates:"
    echo "$pre_existing" | sed 's/^/    /'
    warn "Stop them first: pkill -f 'telegram_listener.py|peck_listener.py'"
    if [[ "${SPACEDUCK_ALLOW_DUP_LISTENERS:-}" == "1" ]]; then
      warn "SPACEDUCK_ALLOW_DUP_LISTENERS=1 set — continuing anyway."
    else
      die "Aborting to avoid duplicate listeners (set SPACEDUCK_ALLOW_DUP_LISTENERS=1 to override)."
    fi
  fi

  # Write supervisord config
  info "Writing $SUP_CONF"
  cat > "$SUP_CONF" <<EOF
; Space Duck listener supervisor — v0.4.0 (2026-06-13)
; Edit by running setup_listeners_supervised.sh again, not by hand.

[unix_http_server]
file=${SUP_SOCK}
chmod=0700

[supervisord]
pidfile=${SUP_PID}
logfile=${SUP_DIR}/supervisord.log
loglevel=info
nodaemon=false
minfds=1024
minprocs=200

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=unix://${SUP_SOCK}

[program:telegram_listener]
; v0.4.16 — wire reply_with_claude.sh via --on-message so verified plain DMs
; actually get a reply. Before this, the listener accepted + owner-approved
; inbound DMs but had no hook to compose an answer — root cause of the
; "duck looks connected but never replies to DMs" failure. We do NOT pass
; --auto-reply: reply_with_claude.sh forks a detached worker and sends its
; own threaded reply via tg_send, so --auto-reply would double-send and the
; hook-timeout would race the brain. The hook owns its own dispatch.
command=python3 ${TG_LISTENER} --owner-approval --on-message "bash ${REPLY_HOOK}"
directory=${SD_DIR}
autostart=true
autorestart=true
startsecs=3
startretries=20
stdout_logfile=${LOG_DIR}/telegram_listener.log
stdout_logfile_maxbytes=10MB
stdout_logfile_backups=3
stderr_logfile=${LOG_DIR}/telegram_listener.err
stderr_logfile_maxbytes=10MB
stderr_logfile_backups=3
environment=HOME="${HOME}",PATH="${PATH}"

[program:peck_listener]
; v0.4.7 — wire peck_responder.py via --on-peck so inbound pecks auto-reply
; by default. Closes the "pushed but silent inbox" gap diagnosed
; 2026-06-16 03:45 KL. peck_responder.py server-side-checks the connection's
; auto_respond permission before composing, so MC owner-toggle gates apply.
; The --allow-shell-hook flag is required for the on-peck handler to run.
command=python3 ${PECK_LISTENER} --poll --interval 3 --allow-shell-hook --on-peck "python3 ${PECK_RESPONDER}"
directory=${SD_DIR}
autostart=true
autorestart=true
startsecs=3
startretries=20
stdout_logfile=${LOG_DIR}/peck_listener.log
stdout_logfile_maxbytes=10MB
stdout_logfile_backups=3
stderr_logfile=${LOG_DIR}/peck_listener.err
stderr_logfile_maxbytes=10MB
stderr_logfile_backups=3
environment=HOME="${HOME}",PATH="${PATH}"

; v0.4.7 — capability-declaring pulse. Pulses every 4 min so MC + senders
; see this duck's actual posture (auto_respond_peck, owner_approval_marker,
; etc) within one window of any state change. Cheap call, single HTTPS.
[program:capability_pulse]
command=/bin/sh -c "while true; do python3 ${PULSE_SCRIPT} >/dev/null 2>&1 || true; sleep 240; done"
directory=${SD_DIR}
autostart=true
autorestart=true
startsecs=3
startretries=10
stdout_logfile=${LOG_DIR}/capability_pulse.log
stdout_logfile_maxbytes=2MB
stdout_logfile_backups=2
stderr_logfile=${LOG_DIR}/capability_pulse.err
stderr_logfile_maxbytes=2MB
stderr_logfile_backups=2
environment=HOME="${HOME}",PATH="${PATH}"

EOF
  # 0.8.11 [VER-0811] — the [program:version_check] block was REMOVED here.
  # It ran version_check_daemon.sh on a 6h loop while telegram_listener.py
  # also checks daily from the pulse thread: two nudgers, two sources of
  # truth (clawhub inspect vs /beak/skill/latest). Invisible only while the
  # listener path 401'd; fixing that contract in 0.8.11 would have made every
  # supervised box double-nudge. Do not re-add.
  chmod 600 "$SUP_CONF"
  ok "Config written"

  # Start it
  info "Starting supervisord..."
  ~/.local/bin/supervisord -c "$SUP_CONF"
  sleep 3

  # Verify
  if [[ ! -f "$SUP_PID" ]] || ! proc_alive "$(cat "$SUP_PID")"; then  # 0.8.6 — F1
    die "supervisord failed to start — check $SUP_DIR/supervisord.log"
  fi
  ok "supervisord running (PID $(cat "$SUP_PID"))"
  echo ""
  echo "─── Listener status ───"
  ~/.local/bin/supervisorctl -c "$SUP_CONF" status

  echo ""
  echo "─── How to manage ───"
  echo "  Status:    $0 --status"
  echo "  Restart:   $0 --restart"
  echo "  Stop:      $0 --stop"
  echo "  Logs:      tail -f $LOG_DIR/{telegram_listener,peck_listener}.{log,err}"
  echo ""
  echo "─── Container-restart persistence ───"
  echo "If you are inside a Docker/LXC/Hostinger container with no systemd, supervisord"
  echo "will NOT auto-restart on container reboot. Add this to your container entrypoint"
  echo "(or to your shell rc) so supervisord comes back up after each restart:"
  echo ""
  echo "    ~/.local/bin/supervisord -c ${SUP_CONF}"
  echo ""
}

# ─────────────────────────────── dispatch ─────────────────────────────────────
case "${1:-install}" in
  --status|status)       cmd_status ;;
  --stop|stop)           cmd_stop ;;
  --restart|restart)     cmd_restart ;;
  --uninstall|uninstall) cmd_uninstall ;;
  --help|-h)
    sed -n '2,40p' "$0" | sed 's/^# \?//'
    exit 0 ;;
  install|"")            cmd_install ;;
  *) die "unknown command: $1 (try --help)" ;;
esac
