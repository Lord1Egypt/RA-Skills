#!/usr/bin/env bash
# arm-recovery-watchdog.sh — render/load/verify/cleanup external watchdog jobs
set -euo pipefail

LAUNCHCTL_BIN="${LAUNCHCTL_BIN:-launchctl}"
PLUTIL_BIN="${PLUTIL_BIN:-plutil}"
SYSTEMD_RUN_BIN="${SYSTEMD_RUN_BIN:-systemd-run}"
SYSTEMCTL_BIN="${SYSTEMCTL_BIN:-systemctl}"
BASH_BIN="${BASH_BIN:-/bin/bash}"
OPENCLAW_BIN="${OPENCLAW_BIN:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="${SKILL_DIR:-$(cd "$SCRIPT_DIR/.." && pwd)}"
WATCHDOG_SCRIPT="${WATCHDOG_SCRIPT:-$SKILL_DIR/scripts/recovery-watchdog.sh}"
STATE_DIR="${STATE_DIR:-${TMPDIR:-/tmp}/update-advisor-watchdog}"
LABEL_PREFIX="${LABEL_PREFIX:-ai.openclaw.update-recovery-watchdog}"
SYSTEMD_UNIT_PREFIX="${SYSTEMD_UNIT_PREFIX:-openclaw-update-recovery-watchdog}"
LAUNCHCTL_DOMAIN="${LAUNCHCTL_DOMAIN:-gui/$(id -u)}"
WATCHDOG_BACKEND="${WATCHDOG_BACKEND:-auto}"
OS_NAME="${OS_NAME:-$(uname -s)}"

GRACE_SECONDS="${GRACE_SECONDS:-420}"
STATUS_RETRIES="${STATUS_RETRIES:-4}"
STATUS_INTERVAL_SECONDS="${STATUS_INTERVAL_SECONDS:-20}"
RECOVERY_RETRIES="${RECOVERY_RETRIES:-2}"
RECOVERY_INTERVAL_SECONDS="${RECOVERY_INTERVAL_SECONDS:-30}"
MAX_RUNTIME_SECONDS="${MAX_RUNTIME_SECONDS:-1200}"

ACTION="${1:-}"
shift || true

usage() {
  cat <<'EOF_USAGE'
Usage:
  arm-recovery-watchdog.sh arm [--state-file PATH]
  arm-recovery-watchdog.sh cleanup [--state-file PATH]

Environment:
  WATCHDOG_BACKEND               auto|launchd|systemd (default: auto)
  OS_NAME                        Override OS detection for tests (Darwin/Linux)
  LAUNCHCTL_BIN, PLUTIL_BIN      macOS launchd backend command overrides
  SYSTEMD_RUN_BIN, SYSTEMCTL_BIN Linux systemd backend command overrides
  OPENCLAW_BIN                   OpenClaw binary path for watchdog job
  STATE_DIR                      Directory for per-run state/log/plist files
  LABEL_PREFIX                   Launchd label prefix (unique suffix is always added)
  SYSTEMD_UNIT_PREFIX            systemd unit prefix (unique suffix is always added)
  LAUNCHCTL_DOMAIN               launchctl domain target (default: gui/<uid>)
  WATCHDOG_SCRIPT                Script launched by job

  GRACE_SECONDS
  STATUS_RETRIES
  STATUS_INTERVAL_SECONDS
  RECOVERY_RETRIES
  RECOVERY_INTERVAL_SECONDS
  MAX_RUNTIME_SECONDS
EOF_USAGE
}

log() {
  printf '[arm-recovery-watchdog] %s\n' "$*" >&2
}

fatal() {
  log "error: $*"
  exit 1
}

is_positive_int() {
  [[ "$1" =~ ^[0-9]+$ ]]
}

abs_path() {
  python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$1"
}

xml_escape() {
  python3 -c 'import html,sys; print(html.escape(sys.argv[1], quote=True), end="")' "$1"
}

resolve_openclaw_bin() {
  local candidate resolved
  candidate="${OPENCLAW_BIN:-openclaw}"

  if [[ "$candidate" == */* ]]; then
    [[ -x "$candidate" ]] || fatal "openclaw binary not executable: $candidate"
    OPENCLAW_BIN="$(abs_path "$candidate")"
    return 0
  fi

  resolved="$(command -v "$candidate" 2>/dev/null || true)"
  [[ -n "$resolved" ]] || fatal "openclaw binary not found: $candidate"
  [[ -x "$resolved" ]] || fatal "openclaw binary not executable: $resolved"
  OPENCLAW_BIN="$(abs_path "$resolved")"
}

watchdog_path_env() {
  local bin_dir
  bin_dir="$(dirname "$OPENCLAW_BIN")"
  printf '%s:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin' "$bin_dir"
}

write_kv() {
  local path="$1" k="$2" v="$3"
  printf '%s=%s\n' "$k" "$v" >> "$path"
}

read_state_value() {
  local path="$1" key="$2"
  awk -F= -v k="$key" '$1==k{print substr($0, index($0,"=")+1); exit}' "$path"
}

latest_state_file() {
  find "$STATE_DIR" -type f -name '*.state' -print 2>/dev/null | sort | tail -n 1
}

select_backend() {
  case "$WATCHDOG_BACKEND" in
    launchd|systemd) printf '%s\n' "$WATCHDOG_BACKEND" ;;
    auto)
      case "$OS_NAME" in
        Darwin) printf 'launchd\n' ;;
        Linux) printf 'systemd\n' ;;
        *) fatal "unsupported OS for recovery watchdog arming: $OS_NAME" ;;
      esac
      ;;
    *) fatal "unknown WATCHDOG_BACKEND: $WATCHDOG_BACKEND" ;;
  esac
}

systemd_unit_name() {
  local run_id="$1" prefix
  prefix="$(printf '%s' "$SYSTEMD_UNIT_PREFIX" | tr -cs 'A-Za-z0-9_.@-' '-')"
  printf '%s-%s.service' "${prefix%-}" "$run_id"
}

ensure_common_prereqs() {
  command -v python3 >/dev/null 2>&1 || fatal "python3 binary not found"
  [[ -f "$WATCHDOG_SCRIPT" ]] || fatal "watchdog script missing: $WATCHDOG_SCRIPT"
  [[ -x "$BASH_BIN" ]] || fatal "bash binary not executable: $BASH_BIN"
  resolve_openclaw_bin

  for n in \
    "$GRACE_SECONDS" \
    "$STATUS_RETRIES" \
    "$STATUS_INTERVAL_SECONDS" \
    "$RECOVERY_RETRIES" \
    "$RECOVERY_INTERVAL_SECONDS" \
    "$MAX_RUNTIME_SECONDS"; do
    is_positive_int "$n" || fatal "numeric value required, got: $n"
  done
}

ensure_backend_prereqs() {
  local backend="$1"
  case "$backend" in
    launchd)
      command -v "$LAUNCHCTL_BIN" >/dev/null 2>&1 || fatal "launchctl binary not found: $LAUNCHCTL_BIN"
      command -v "$PLUTIL_BIN" >/dev/null 2>&1 || fatal "plutil binary not found: $PLUTIL_BIN"
      ;;
    systemd)
      command -v "$SYSTEMD_RUN_BIN" >/dev/null 2>&1 || fatal "systemd-run binary not found: $SYSTEMD_RUN_BIN"
      command -v "$SYSTEMCTL_BIN" >/dev/null 2>&1 || fatal "systemctl binary not found: $SYSTEMCTL_BIN"
      ;;
    *) fatal "unsupported backend: $backend" ;;
  esac
}

render_launchd_plist() {
  local label="$1" plist="$2" watchdog_log="$3" stdout_log="$4" stderr_log="$5"

  local label_esc bash_esc script_esc wl_esc so_esc se_esc openclaw_esc path_esc
  label_esc="$(xml_escape "$label")"
  bash_esc="$(xml_escape "$BASH_BIN")"
  script_esc="$(xml_escape "$WATCHDOG_SCRIPT")"
  wl_esc="$(xml_escape "$watchdog_log")"
  so_esc="$(xml_escape "$stdout_log")"
  se_esc="$(xml_escape "$stderr_log")"
  openclaw_esc="$(xml_escape "$OPENCLAW_BIN")"
  path_esc="$(xml_escape "$(watchdog_path_env)")"

  cat > "$plist" <<EOF_PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>$label_esc</string>
    <key>EnvironmentVariables</key>
    <dict>
      <key>OPENCLAW_BIN</key>
      <string>$openclaw_esc</string>
      <key>PATH</key>
      <string>$path_esc</string>
    </dict>
    <key>ProgramArguments</key>
    <array>
      <string>$bash_esc</string>
      <string>$script_esc</string>
      <string>--log-file</string>
      <string>$wl_esc</string>
      <string>--grace-seconds</string>
      <string>$GRACE_SECONDS</string>
      <string>--status-retries</string>
      <string>$STATUS_RETRIES</string>
      <string>--status-interval-seconds</string>
      <string>$STATUS_INTERVAL_SECONDS</string>
      <string>--recovery-retries</string>
      <string>$RECOVERY_RETRIES</string>
      <string>--recovery-interval-seconds</string>
      <string>$RECOVERY_INTERVAL_SECONDS</string>
      <string>--max-runtime-seconds</string>
      <string>$MAX_RUNTIME_SECONDS</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
    <key>StandardOutPath</key>
    <string>$so_esc</string>
    <key>StandardErrorPath</key>
    <string>$se_esc</string>
  </dict>
</plist>
EOF_PLIST
}

launchd_print_verify() {
  local domain="$1" label="$2"
  "$LAUNCHCTL_BIN" print "$domain/$label" >/dev/null 2>&1
}

arm_launchd() {
  local label="$1" plist="$2" watchdog_log="$3" stdout_log="$4" stderr_log="$5"

  render_launchd_plist "$label" "$plist" "$watchdog_log" "$stdout_log" "$stderr_log"
  "$PLUTIL_BIN" -lint "$plist" >/dev/null

  if ! "$LAUNCHCTL_BIN" bootstrap "$LAUNCHCTL_DOMAIN" "$plist" >/dev/null 2>&1; then
    rm -f "$plist"
    fatal "failed to bootstrap launchd job"
  fi

  if ! launchd_print_verify "$LAUNCHCTL_DOMAIN" "$label"; then
    "$LAUNCHCTL_BIN" bootout "$LAUNCHCTL_DOMAIN/$label" >/dev/null 2>&1 || true
    rm -f "$plist"
    fatal "arming verification failed (launchctl print)"
  fi
}

arm_systemd() {
  local unit="$1" watchdog_log="$2"
  local path_env
  path_env="$(watchdog_path_env)"

  if ! "$SYSTEMD_RUN_BIN" \
    --user \
    --unit "$unit" \
    --description "OpenClaw update recovery watchdog" \
    --setenv "OPENCLAW_BIN=$OPENCLAW_BIN" \
    --setenv "PATH=$path_env" \
    "$BASH_BIN" "$WATCHDOG_SCRIPT" \
      --log-file "$watchdog_log" \
      --grace-seconds "$GRACE_SECONDS" \
      --status-retries "$STATUS_RETRIES" \
      --status-interval-seconds "$STATUS_INTERVAL_SECONDS" \
      --recovery-retries "$RECOVERY_RETRIES" \
      --recovery-interval-seconds "$RECOVERY_INTERVAL_SECONDS" \
      --max-runtime-seconds "$MAX_RUNTIME_SECONDS" >/dev/null 2>&1; then
    fatal "failed to start systemd user watchdog unit"
  fi

  if ! "$SYSTEMCTL_BIN" --user show "$unit" >/dev/null 2>&1; then
    "$SYSTEMCTL_BIN" --user stop "$unit" >/dev/null 2>&1 || true
    "$SYSTEMCTL_BIN" --user reset-failed "$unit" >/dev/null 2>&1 || true
    fatal "arming verification failed (systemctl --user show)"
  fi
}

arm_watchdog() {
  local state_file_override=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --state-file) state_file_override="$2"; shift 2 ;;
      --help|-h) usage; exit 0 ;;
      *) fatal "unknown arm argument: $1" ;;
    esac
  done

  local backend run_id label unit plist watchdog_log stdout_log stderr_log state_file
  backend="$(select_backend)"
  ensure_common_prereqs
  ensure_backend_prereqs "$backend"
  mkdir -p "$STATE_DIR"

  run_id="$(date +%Y%m%dT%H%M%S)-$$-$RANDOM"
  label="$LABEL_PREFIX.$run_id"
  unit="$(systemd_unit_name "$run_id")"

  plist="$STATE_DIR/$label.plist"
  watchdog_log="$STATE_DIR/$label.watchdog.log"
  stdout_log="$STATE_DIR/$label.stdout.log"
  stderr_log="$STATE_DIR/$label.stderr.log"
  state_file="${state_file_override:-$STATE_DIR/$label.state}"
  mkdir -p "$(dirname "$state_file")"

  case "$backend" in
    launchd) arm_launchd "$label" "$plist" "$watchdog_log" "$stdout_log" "$stderr_log" ;;
    systemd) arm_systemd "$unit" "$watchdog_log" ;;
    *) fatal "unsupported backend: $backend" ;;
  esac

  : > "$state_file"
  write_kv "$state_file" "backend" "$backend"
  write_kv "$state_file" "label" "$label"
  write_kv "$state_file" "unit" "$unit"
  write_kv "$state_file" "domain" "$LAUNCHCTL_DOMAIN"
  write_kv "$state_file" "plist" "$plist"
  write_kv "$state_file" "watchdog_log" "$watchdog_log"
  write_kv "$state_file" "stdout_log" "$stdout_log"
  write_kv "$state_file" "stderr_log" "$stderr_log"
  write_kv "$state_file" "launchctl_bin" "$LAUNCHCTL_BIN"
  write_kv "$state_file" "systemctl_bin" "$SYSTEMCTL_BIN"
  write_kv "$state_file" "openclaw_bin" "$OPENCLAW_BIN"

  printf 'armed=1\nbackend=%s\nlabel=%s\nunit=%s\nstate_file=%s\nplist=%s\nwatchdog_log=%s\n' \
    "$backend" "$label" "$unit" "$state_file" "$plist" "$watchdog_log"
}

cleanup_watchdog() {
  local state_file=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --state-file) state_file="$2"; shift 2 ;;
      --help|-h) usage; exit 0 ;;
      *) fatal "unknown cleanup argument: $1" ;;
    esac
  done

  mkdir -p "$STATE_DIR"
  if [[ -z "$state_file" ]]; then
    state_file="$(latest_state_file || true)"
  fi

  if [[ -z "$state_file" || ! -f "$state_file" ]]; then
    log "no watchdog state file found; nothing to cleanup"
    return 0
  fi

  local backend label unit domain plist watchdog_log stdout_log stderr_log stored_launchctl stored_systemctl
  backend="$(read_state_value "$state_file" backend)"
  label="$(read_state_value "$state_file" label)"
  unit="$(read_state_value "$state_file" unit)"
  domain="$(read_state_value "$state_file" domain)"
  plist="$(read_state_value "$state_file" plist)"
  watchdog_log="$(read_state_value "$state_file" watchdog_log)"
  stdout_log="$(read_state_value "$state_file" stdout_log)"
  stderr_log="$(read_state_value "$state_file" stderr_log)"
  stored_launchctl="$(read_state_value "$state_file" launchctl_bin)"
  stored_systemctl="$(read_state_value "$state_file" systemctl_bin)"
  [[ -n "$stored_launchctl" ]] && LAUNCHCTL_BIN="$stored_launchctl"
  [[ -n "$stored_systemctl" ]] && SYSTEMCTL_BIN="$stored_systemctl"

  case "$backend" in
    launchd|"")
      if [[ -n "$domain" && -n "$label" ]]; then
        "$LAUNCHCTL_BIN" bootout "$domain/$label" >/dev/null 2>&1 || true
      fi
      ;;
    systemd)
      if [[ -n "$unit" ]]; then
        "$SYSTEMCTL_BIN" --user stop "$unit" >/dev/null 2>&1 || true
        "$SYSTEMCTL_BIN" --user reset-failed "$unit" >/dev/null 2>&1 || true
      fi
      ;;
    *)
      fatal "unknown backend in state file: $backend"
      ;;
  esac

  rm -f "$plist" "$state_file" "$stdout_log" "$stderr_log" "$watchdog_log"
  printf 'cleaned=1\nbackend=%s\nlabel=%s\nunit=%s\n' "$backend" "$label" "$unit"
}

case "$ACTION" in
  arm) arm_watchdog "$@" ;;
  cleanup) cleanup_watchdog "$@" ;;
  --help|-h|"") usage; exit 0 ;;
  *) fatal "unknown action: $ACTION" ;;
esac
