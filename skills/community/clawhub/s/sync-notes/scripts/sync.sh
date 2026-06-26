#!/usr/bin/env bash
# sync-notes — rclone-based bidirectional sync between $CLOUD_NOTES_PATH and a
# Cloudflare R2 crypt remote. All paths are derived from this script's location.
#
# Usage:
#   sync.sh setup
#   sync.sh init [--force]
#   sync.sh bisync
#   sync.sh download <glob> [--dry-run]
#   sync.sh upload <glob> [--dry-run]
#   sync.sh status

set -euo pipefail

# ---------- path resolution (relative to this script) -------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_DIR="$SKILL_DIR/config"
STATE_DIR="$SKILL_DIR/state"
LOG_DIR="$SKILL_DIR/logs"
BACKUP_DIR="$SKILL_DIR/backups"
RCLONE_CONFIG_FILE="$CONFIG_DIR/rclone.conf"
ENV_FILE="$CONFIG_DIR/.env"
FILTER_FILE="$CONFIG_DIR/filter.txt"
BISYNC_WORKDIR="$STATE_DIR/bisync"

mkdir -p "$STATE_DIR" "$LOG_DIR" "$BACKUP_DIR" "$BISYNC_WORKDIR"

# ---------- helpers -----------------------------------------------------------
log() { printf '[sync-notes] %s\n' "$*" >&2; }
die() { log "ERROR: $*"; exit 1; }

require_bin() {
  command -v "$1" >/dev/null 2>&1 || die "missing dependency: $1"
}

load_env() {
  [[ -f "$ENV_FILE" ]] || die "config missing — run: $0 setup"
  # shellcheck disable=SC1090
  set -a; source "$ENV_FILE"; set +a
  : "${RCLONE_REMOTE:?RCLONE_REMOTE not set in $ENV_FILE}"
  : "${BACKUP_KEEP:=1}"
  : "${RCLONE_EXTRA_FLAGS:=}"
}

require_local() {
  [[ -n "${CLOUD_NOTES_PATH:-}" ]] || die "CLOUD_NOTES_PATH is not set"
  [[ -d "$CLOUD_NOTES_PATH" ]]    || die "CLOUD_NOTES_PATH is not a directory: $CLOUD_NOTES_PATH"
}

require_config() {
  [[ -f "$RCLONE_CONFIG_FILE" ]] || die "rclone.conf missing — run: $0 setup"
}

rclone_run() {
  # Always pin --config to our file; never touch ~/.config/rclone.
  # Always apply filter rules when present.
  local filter_args=()
  [[ -f "$FILTER_FILE" ]] && filter_args=(--filter-from "$FILTER_FILE")
  rclone --config "$RCLONE_CONFIG_FILE" "${filter_args[@]}" $RCLONE_EXTRA_FLAGS "$@"
}

ts() { date -u +'%Y%m%dT%H%M%SZ'; }

per_run_log() {
  local name="$1"
  echo "$LOG_DIR/$(ts)-${name}.log"
}

append_master_log() {
  printf '%s [%s] %s\n' "$(date -u +'%Y-%m-%dT%H:%M:%SZ')" "$1" "$2" >> "$LOG_DIR/sync.log"
}

backup_local() {
  require_local
  local dest="$BACKUP_DIR/latest"
  if [[ -d "$dest" ]]; then
    rm -rf "$dest"
  fi
  mkdir -p "$dest"
  log "backing up $CLOUD_NOTES_PATH → $dest"
  rclone --config "$RCLONE_CONFIG_FILE" copy "$CLOUD_NOTES_PATH" "$dest" >/dev/null
}

baseline_present() {
  # rclone bisync stores listing files in --workdir keyed off the path pair.
  # A successful resync leaves .lst (not just .lst-new) files behind.
  compgen -G "$BISYNC_WORKDIR/*.lst" >/dev/null 2>&1
}

clean_failed_baseline() {
  # Wipe partial bisync state so --resync can start clean.
  rm -f "$BISYNC_WORKDIR"/*.lst-new "$BISYNC_WORKDIR"/*.lst-err 2>/dev/null || true
}

scan_conflicts() {
  # Print any files that look like bisync conflict copies, return count via stdout.
  find "$CLOUD_NOTES_PATH" -type f \( -name '*.conflict1*' -o -name '*.conflict2*' \) 2>/dev/null
}

translate_glob() {
  # Pass-through if user already supplied wildcards or a slash;
  # otherwise broaden a bare keyword to **keyword**.
  local g="$1"
  if [[ "$g" == *'*'* || "$g" == *'?'* || "$g" == *'['* || "$g" == */* ]]; then
    printf '%s' "$g"
  else
    printf '**%s**' "$g"
  fi
}

# ---------- subcommands -------------------------------------------------------
cmd_setup() {
  exec bash "$SCRIPT_DIR/setup.sh" "$@"
}

cmd_init() {
  require_bin rclone; require_config; load_env; require_local
  local force=0
  [[ "${1:-}" == "--force" ]] && force=1
  if baseline_present && [[ $force -eq 0 ]]; then
    die "bisync baseline already exists in $BISYNC_WORKDIR — pass --force to recreate"
  fi
  clean_failed_baseline
  backup_local
  local logf; logf="$(per_run_log init)"
  log "establishing bisync baseline (--resync) → $logf"
  rclone_run bisync "$CLOUD_NOTES_PATH" "${RCLONE_REMOTE}:" \
    --workdir "$BISYNC_WORKDIR" \
    --resync \
    --create-empty-src-dirs \
    --modify-window 1s \
    --log-file "$logf" \
    --log-level INFO
  append_master_log INIT "ok"
  log "baseline created"
}

cmd_bisync() {
  require_bin rclone; require_config; load_env; require_local
  baseline_present || die "no bisync baseline — run: $0 init"
  backup_local
  local logf; logf="$(per_run_log bisync)"
  log "bidirectional sync → $logf"
  if ! rclone_run bisync "$CLOUD_NOTES_PATH" "${RCLONE_REMOTE}:" \
        --workdir "$BISYNC_WORKDIR" \
        --create-empty-src-dirs \
        --modify-window 1s \
        --conflict-resolve none \
        --conflict-loser pathname \
        --conflict-suffix conflict1,conflict2 \
        --log-file "$logf" \
        --log-level INFO; then
    append_master_log BISYNC "rclone returned non-zero — see $logf"
  else
    append_master_log BISYNC "ok"
  fi
  local conflicts; conflicts="$(scan_conflicts || true)"
  if [[ -n "$conflicts" ]]; then
    log "CONFLICTS detected — review before next sync:"
    printf '%s\n' "$conflicts" | sed 's/^/  /' >&2
    exit 2
  fi
  log "bisync complete"
}

cmd_download() {
  require_bin rclone; require_config; load_env; require_local
  [[ $# -ge 1 ]] || die "usage: $0 download <glob> [--dry-run]"
  local raw="$1"; shift || true
  local glob; glob="$(translate_glob "$raw")"
  local dry=()
  [[ "${1:-}" == "--dry-run" ]] && dry=(--dry-run)
  backup_local
  local logf; logf="$(per_run_log download)"
  log "download '$glob' → $CLOUD_NOTES_PATH (log: $logf)"
  rclone_run copy "${RCLONE_REMOTE}:" "$CLOUD_NOTES_PATH" \
    --include "$glob" \
    --create-empty-src-dirs \
    --log-file "$logf" --log-level INFO \
    "${dry[@]}"
  append_master_log DOWNLOAD "glob='$glob' dry=${#dry[@]}"
}

cmd_upload() {
  require_bin rclone; require_config; load_env; require_local
  [[ $# -ge 1 ]] || die "usage: $0 upload <glob> [--dry-run]"
  local raw="$1"; shift || true
  local glob; glob="$(translate_glob "$raw")"
  local dry=()
  [[ "${1:-}" == "--dry-run" ]] && dry=(--dry-run)
  local logf; logf="$(per_run_log upload)"
  log "upload '$glob' → ${RCLONE_REMOTE}: (log: $logf)"
  rclone_run copy "$CLOUD_NOTES_PATH" "${RCLONE_REMOTE}:" \
    --include "$glob" \
    --create-empty-src-dirs \
    --log-file "$logf" --log-level INFO \
    "${dry[@]}"
  append_master_log UPLOAD "glob='$glob' dry=${#dry[@]}"
}

cmd_status() {
  echo "skill dir : $SKILL_DIR"
  echo "config    : $RCLONE_CONFIG_FILE $( [[ -f $RCLONE_CONFIG_FILE ]] && echo OK || echo MISSING )"
  echo "env       : $ENV_FILE $( [[ -f $ENV_FILE ]] && echo OK || echo MISSING )"
  echo "filter    : $FILTER_FILE $( [[ -f $FILTER_FILE ]] && echo OK || echo MISSING )"
  echo "local     : ${CLOUD_NOTES_PATH:-<unset>}"
  echo "baseline  : $( baseline_present && echo present || echo absent )"
  echo "backup    : $( [[ -d $BACKUP_DIR/latest ]] && echo present || echo none )"
  if [[ -n "${CLOUD_NOTES_PATH:-}" && -d "${CLOUD_NOTES_PATH:-}" ]]; then
    local c; c="$(scan_conflicts || true)"
    if [[ -n "$c" ]]; then
      echo "conflicts :"
      printf '%s\n' "$c" | sed 's/^/  /'
    else
      echo "conflicts : none"
    fi
  fi
  if [[ -f "$LOG_DIR/sync.log" ]]; then
    echo "last log  :"
    tail -n 5 "$LOG_DIR/sync.log" | sed 's/^/  /'
  fi
}

# ---------- dispatcher --------------------------------------------------------
main() {
  local sub="${1:-bisync}"; shift || true
  case "$sub" in
    setup)    cmd_setup    "$@" ;;
    init)     cmd_init     "$@" ;;
    bisync|"") cmd_bisync  "$@" ;;
    download|pull|get) cmd_download "$@" ;;
    upload|push|put)   cmd_upload   "$@" ;;
    status)   cmd_status   "$@" ;;
    -h|--help|help)
      sed -n '2,16p' "$0"
      ;;
    *)
      die "unknown subcommand: $sub (try: setup | init | bisync | download | upload | status)"
      ;;
  esac
}

main "$@"
