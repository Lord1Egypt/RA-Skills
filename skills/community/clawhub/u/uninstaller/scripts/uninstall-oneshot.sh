#!/usr/bin/env bash
# uninstall-oneshot.sh — Full OpenClaw uninstall. Run by one-shot or manually.
# Usage: uninstall-oneshot.sh [OPTIONS]
#   --notify-email EMAIL   Send email when done
#   --notify-ntfy TOPIC    Send ntfy notification when done
#   --notify-im TARGET     Push backup info to IM before uninstall (channel:target, e.g. discord:user:123456). Repeat for multiple.
#   --no-backup            Skip backup (default: openclaw backup create unless --no-backup)
#   --preserve-state       Keep ~/.openclaw for reinstall inheritance (skips backup and deletion)
#   --all-profiles         Also remove ~/.openclaw-* profile dirs (default: only STATE_DIR)
#   --dry-run              Validate only, no destructive ops (for E2E tests)

set -e

LOG_FILE="/tmp/openclaw-uninstall.log"
NOTIFY_EMAIL=""
NOTIFY_NTFY=""
declare -a NOTIFY_IM=()
NO_BACKUP=false
PRESERVE_STATE=false
ALL_PROFILES=false
DRY_RUN=false
declare -a ERRORS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --notify-email)  NOTIFY_EMAIL="$2"; shift 2 ;;
    --notify-ntfy)   NOTIFY_NTFY="$2"; shift 2 ;;
    --notify-im)     NOTIFY_IM+=("$2"); shift 2 ;;
    --no-backup)     NO_BACKUP=true; shift ;;
    --preserve-state) PRESERVE_STATE=true; shift ;;
    --all-profiles)  ALL_PROFILES=true; shift ;;
    --dry-run)       DRY_RUN=true; shift ;;
    *) shift ;;
  esac
done

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"; }

log "=== OpenClaw uninstall started ==="

STATE_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
# Expand ~ to $HOME for validation
STATE_DIR="${STATE_DIR/#\~/$HOME}"
# Resolve to canonical path when dir exists (for validation)
STATE_DIR_CANON="$STATE_DIR"
if [[ -d "$STATE_DIR" ]]; then
  STATE_DIR_CANON="$(cd -P "$STATE_DIR" 2>/dev/null && pwd)" || STATE_DIR_CANON="$STATE_DIR"
fi

# --- Path safety: never delete outside $HOME or system paths ---
validate_state_dir() {
  local dir="$1"
  [[ -z "$dir" ]] && return 1
  case "$dir" in
    "$HOME") return 1 ;;   # Never delete $HOME itself
    "$HOME"/*) ;;
    *) log "SAFETY: Rejecting STATE_DIR outside HOME: $dir"; return 1 ;;
  esac
  case "$(basename "$dir")" in
    .openclaw|.openclaw-*) return 0 ;;
    *) log "SAFETY: Rejecting non-OpenClaw path: $dir"; return 1 ;;
  esac
}

if ! validate_state_dir "$STATE_DIR_CANON"; then
  log "FATAL: Invalid OPENCLAW_STATE_DIR. Use default ~/.openclaw or a path under \$HOME matching .openclaw*"
  exit 1
fi

if [[ "$DRY_RUN" == "true" ]]; then
  if [[ "$PRESERVE_STATE" == "true" ]]; then
    log "DRY_RUN: Would preserve STATE_DIR=$STATE_DIR (validation passed)"
  else
    log "DRY_RUN: Would remove STATE_DIR=$STATE_DIR (validation passed)"
  fi
  exit 0
fi

# 0. Backup via openclaw backup create (unless --no-backup or --preserve-state)
BACKUP_ARCHIVE=""
if [[ "$PRESERVE_STATE" != "true" ]] && [[ "$NO_BACKUP" != "true" ]] && [[ -d "$STATE_DIR" ]]; then
  BACKUP_DIR="$HOME/.openclaw-backup-$(date '+%Y%m%d-%H%M%S')"
  mkdir -p "$BACKUP_DIR" || { log "ERROR: Failed to create backup dir"; ERRORS+=("backup-dir"); }
  if [[ ${#ERRORS[@]} -eq 0 ]]; then
    if command -v openclaw &>/dev/null; then
      log "Creating backup via openclaw backup create..."
      if openclaw backup create --output "$BACKUP_DIR" --no-include-workspace 2>/dev/null; then
        BACKUP_ARCHIVE=$(ls -t "$BACKUP_DIR"/*.tar.gz 2>/dev/null | head -1)
        [[ -n "$BACKUP_ARCHIVE" ]] && log "Backup complete: $BACKUP_ARCHIVE" || log "Backup created but archive path not found"
      else
        log "openclaw backup create failed; falling back to manual copy"
        cp -r "$STATE_DIR/skills" "$BACKUP_DIR/" 2>/dev/null || true
        cp -r "$STATE_DIR/sessions" "$BACKUP_DIR/" 2>/dev/null || true
        [[ -f "$STATE_DIR/openclaw.json" ]] && cp "$STATE_DIR/openclaw.json" "$BACKUP_DIR/" 2>/dev/null || true
        [[ -d "$STATE_DIR/credentials" ]] && cp -r "$STATE_DIR/credentials" "$BACKUP_DIR/" 2>/dev/null || true
        log "Backup complete (manual): $BACKUP_DIR"
      fi
    else
      log "openclaw not found; manual backup only"
      cp -r "$STATE_DIR/skills" "$BACKUP_DIR/" 2>/dev/null || true
      cp -r "$STATE_DIR/sessions" "$BACKUP_DIR/" 2>/dev/null || true
      [[ -f "$STATE_DIR/openclaw.json" ]] && cp "$STATE_DIR/openclaw.json" "$BACKUP_DIR/" 2>/dev/null || true
      [[ -d "$STATE_DIR/credentials" ]] && cp -r "$STATE_DIR/credentials" "$BACKUP_DIR/" 2>/dev/null || true
      log "Backup complete (manual): $BACKUP_DIR"
    fi
  fi
fi

# 0b. Push backup info to IM channels (before stopping gateway; requires gateway running)
if [[ ${#NOTIFY_IM[@]} -gt 0 ]] && command -v openclaw &>/dev/null; then
  if [[ "$PRESERVE_STATE" == "true" ]]; then
    BACKUP_MSG="OpenClaw uninstall: state preserved at $STATE_DIR (--preserve-state)"
  elif [[ -n "$BACKUP_ARCHIVE" ]] || [[ -n "$BACKUP_DIR" ]]; then
    BACKUP_MSG="OpenClaw uninstall backup: ${BACKUP_ARCHIVE:-$BACKUP_DIR}"
  else
    BACKUP_MSG="OpenClaw uninstall: no backup (--no-backup or backup failed)"
  fi
  for target in "${NOTIFY_IM[@]}"; do
    [[ -z "$target" ]] && continue
    channel="${target%%:*}"
    rest="${target#*:}"
    [[ "$channel" == "$target" ]] && continue
    log "Pushing backup info to $target..."
    if openclaw message send --channel "$channel" --target "$rest" --message "$BACKUP_MSG" 2>/dev/null; then
      log "Notified IM: $target"
    else
      log "WARNING: Failed to notify IM $target (gateway may be stopped)"
    fi
  done
fi

# 1. Stop gateway (if CLI available)
if command -v openclaw &>/dev/null; then
  log "Stopping gateway..."
  openclaw gateway stop 2>/dev/null || true
  log "Uninstalling gateway service..."
  openclaw gateway uninstall 2>/dev/null || true
fi

# 2. Manual service removal (if CLI gone or as backup)
case "$(uname -s)" in
  Darwin)
    launchctl bootout "gui/$UID/ai.openclaw.gateway" 2>/dev/null || true
    rm -f ~/Library/LaunchAgents/ai.openclaw.gateway.plist
    for f in ~/Library/LaunchAgents/com.openclaw.*.plist; do
      [[ -f "$f" ]] && rm -f "$f"
    done
    ;;
  Linux)
    systemctl --user disable --now openclaw-gateway.service 2>/dev/null || true
    rm -f ~/.config/systemd/user/openclaw-gateway.service
    systemctl --user daemon-reload 2>/dev/null || true
    ;;
esac

# 3. Delete state dir (validated above; skip when --preserve-state)
if [[ "$PRESERVE_STATE" == "true" ]]; then
  if [[ -d "$STATE_DIR" ]]; then
    log "State preserved at $STATE_DIR for reinstall inheritance"
  fi
elif [[ -d "$STATE_DIR" ]]; then
  log "Removing state dir: $STATE_DIR"
  rm -rf "$STATE_DIR" || { log "ERROR: Failed to remove $STATE_DIR"; ERRORS+=("state-dir"); }
fi

# 4. Delete profile dirs (only when --all-profiles; exclude .openclaw-backup-*)
if [[ "$ALL_PROFILES" == "true" ]]; then
  for d in "$HOME"/.openclaw-*; do
    [[ -d "$d" ]] || continue
    [[ "$d" == *"/.openclaw-backup-"* ]] && continue
    # Safety: only remove paths under HOME that look like OpenClaw profile dirs
    case "$(basename "$d")" in
      .openclaw-backup-*) continue ;;
      .openclaw-*)
        log "Removing profile dir: $d"
        rm -rf "$d" || { log "ERROR: Failed to remove $d"; ERRORS+=("profile:$d"); }
        ;;
      *) log "SKIP: Ignoring non-profile dir $d" ;;
    esac
  done
else
  log "Skipping profile dirs (use --all-profiles to remove ~/.openclaw-*)"
fi

# 5. Remove CLI
for pm in npm pnpm bun; do
  if command -v "$pm" &>/dev/null; then
    if "$pm" list -g openclaw --depth=0 &>/dev/null 2>&1; then
      log "Removing npm package: $pm remove -g openclaw"
      "$pm" remove -g openclaw 2>/dev/null || { log "WARNING: $pm remove -g openclaw failed"; ERRORS+=("cli"); }
      break
    fi
  fi
done

# 6. macOS app
if [[ "$(uname -s)" == "Darwin" ]] && [[ -d "/Applications/OpenClaw.app" ]]; then
  log "Removing macOS app"
  rm -rf /Applications/OpenClaw.app || { log "ERROR: Failed to remove /Applications/OpenClaw.app"; ERRORS+=("macos-app"); }
fi

# Final report
if [[ ${#ERRORS[@]} -gt 0 ]]; then
  log "=== Uninstall completed with errors ==="
  log "Failed steps: ${ERRORS[*]}"
  log "Check $LOG_FILE for details. You may need to remove some items manually."
else
  log "=== Uninstall complete ==="
fi

# Notify
if [[ -n "$NOTIFY_EMAIL" ]]; then
  if command -v mail &>/dev/null; then
    echo "OpenClaw uninstalled. Details: $LOG_FILE" | mail -s "OpenClaw Uninstall Complete" "$NOTIFY_EMAIL" 2>/dev/null || log "Email send failed (mail unavailable)"
  else
    log "Email notification skipped (mail command unavailable)"
  fi
fi

if [[ -n "$NOTIFY_NTFY" ]]; then
  if command -v curl &>/dev/null; then
    curl -s -d "OpenClaw uninstalled" "https://ntfy.sh/$NOTIFY_NTFY" &>/dev/null || log "ntfy send failed"
  else
    log "ntfy notification skipped (curl unavailable)"
  fi
fi

[[ ${#ERRORS[@]} -gt 0 ]] && exit 1
exit 0
