#!/usr/bin/env bash
# storage-cleanup: Scan and clean system caches, trash, temp files, old packages, and build artifacts.
# Usage: cleanup.sh [--dry-run] [--skip-kernels] [--skip-snap] [--skip-docker] [--skip-brew] [--yes]
#
# Supports macOS and Linux. Outputs a summary of freed space.

set -euo pipefail

DRY_RUN=false
SKIP_KERNELS=false
SKIP_SNAP=false
SKIP_DOCKER=false
SKIP_BREW=false
AUTO_YES=false

OS="$(uname -s)"
IS_MAC=false
IS_LINUX=false
[[ "$OS" == "Darwin" ]] && IS_MAC=true
[[ "$OS" == "Linux" ]] && IS_LINUX=true

for arg in "$@"; do
  case "$arg" in
    --dry-run)       DRY_RUN=true ;;
    --skip-kernels)  SKIP_KERNELS=true ;;
    --skip-snap)     SKIP_SNAP=true ;;
    --skip-docker)   SKIP_DOCKER=true ;;
    --skip-brew)     SKIP_BREW=true ;;
    --yes|-y)        AUTO_YES=true ;;
    --help|-h)
      echo "Usage: cleanup.sh [--dry-run] [--skip-kernels] [--skip-snap] [--skip-docker] [--skip-brew] [--yes]"
      echo ""
      echo "Options:"
      echo "  --dry-run       Show what would be cleaned without doing it"
      echo "  --skip-kernels  Skip old kernel removal (Linux only)"
      echo "  --skip-snap     Skip disabled snap revision removal (Linux only)"
      echo "  --skip-docker   Skip Docker cleanup"
      echo "  --skip-brew     Skip Homebrew cleanup (macOS)"
      echo "  --yes, -y       Skip confirmation prompts"
      exit 0 ;;
  esac
done

# --- Helpers ---

bytes_to_human() {
  local bytes=$1
  if $IS_MAC; then
    # macOS awk handles floating point
    if (( bytes >= 1073741824 )); then
      awk "BEGIN {printf \"%.1fG\", $bytes / 1073741824}"
    elif (( bytes >= 1048576 )); then
      awk "BEGIN {printf \"%.1fM\", $bytes / 1048576}"
    elif (( bytes >= 1024 )); then
      awk "BEGIN {printf \"%.0fK\", $bytes / 1024}"
    else
      echo "${bytes}B"
    fi
  else
    if (( bytes >= 1073741824 )); then
      awk "BEGIN {printf \"%.1fG\", $bytes / 1073741824}"
    elif (( bytes >= 1048576 )); then
      awk "BEGIN {printf \"%.1fM\", $bytes / 1048576}"
    elif (( bytes >= 1024 )); then
      awk "BEGIN {printf \"%.0fK\", $bytes / 1024}"
    else
      echo "${bytes}B"
    fi
  fi
}

get_dir_bytes() {
  if $IS_MAC; then
    du -sk "$1" 2>/dev/null | awk '{print $1 * 1024}' || echo 0
  else
    du -sb "$1" 2>/dev/null | awk '{print $1}' || echo 0
  fi
}

get_avail_kb() {
  if $IS_MAC; then
    df -k / | tail -1 | awk '{print $4}'
  else
    df --output=avail / | tail -1 | tr -d ' '
  fi
}

maybe_sudo() {
  if $IS_MAC; then
    # Most macOS cleanup doesn't need sudo
    "$@"
  else
    sudo "$@"
  fi
}

section() {
  echo ""
  echo "=== $1 ==="
}

do_clean() {
  local desc="$1"
  shift
  if $DRY_RUN; then
    echo "[DRY-RUN] Would: $desc"
  else
    echo "Cleaning: $desc"
    "$@" 2>/dev/null || true
  fi
}

# Record starting disk usage
START_AVAIL=$(get_avail_kb)

# ============================================================
# 1. Trash
# ============================================================
section "Trash"
if $IS_MAC; then
  TRASH_DIR="$HOME/.Trash"
else
  TRASH_DIR="$HOME/.local/share/Trash"
fi

if [ -d "$TRASH_DIR" ] && [ "$(ls -A "$TRASH_DIR" 2>/dev/null)" ]; then
  TRASH_SIZE=$(get_dir_bytes "$TRASH_DIR")
  echo "Trash size: $(bytes_to_human $TRASH_SIZE)"
  if $IS_MAC; then
    do_clean "Empty trash" rm -rf "$HOME/.Trash/"*
  else
    do_clean "Empty trash" rm -rf "$TRASH_DIR/files/"* "$TRASH_DIR/info/"*
  fi
else
  echo "Trash is empty"
fi

# ============================================================
# 2. Temp files
# ============================================================
section "Temp files"
if $IS_MAC; then
  TMPDIR_ACTUAL="${TMPDIR:-/tmp}"
  # macOS per-user tmp + /tmp
  for tmpd in "$TMPDIR_ACTUAL" /tmp /private/var/folders; do
    if [ -d "$tmpd" ]; then
      TMP_SIZE=$(get_dir_bytes "$tmpd")
      if (( TMP_SIZE > 104857600 )); then
        echo "$tmpd: $(bytes_to_human $TMP_SIZE)"
      fi
    fi
  done
  do_clean "Remove stale pip/build dirs from /tmp" bash -c '
    find /tmp -maxdepth 1 -name "pip-*" -type d -mmin +60 -exec rm -rf {} + 2>/dev/null
    find /tmp -maxdepth 1 -name "npm-*" -type d -mmin +60 -exec rm -rf {} + 2>/dev/null
  '
else
  TMP_SIZE=$(sudo du -sb /tmp 2>/dev/null | awk '{print $1}' || echo 0)
  echo "/tmp size: $(bytes_to_human $TMP_SIZE)"
  if (( TMP_SIZE > 104857600 )); then
    do_clean "Remove stale pip/build dirs from /tmp" bash -c '
      sudo find /tmp -maxdepth 1 -name "pip-*" -type d -mmin +60 -exec rm -rf {} + 2>/dev/null
      sudo find /tmp -maxdepth 1 -name "npm-*" -type d -mmin +60 -exec rm -rf {} + 2>/dev/null
      sudo find /tmp -maxdepth 1 -name "rust_*" -type d -mmin +60 -exec rm -rf {} + 2>/dev/null
    '
  fi
fi

# ============================================================
# 3. User caches
# ============================================================
section "User caches (~/.cache / ~/Library/Caches)"
if $IS_MAC; then
  CACHE_BASE="$HOME/Library/Caches"
else
  CACHE_BASE="$HOME/.cache"
fi

if [ -d "$CACHE_BASE" ]; then
  CACHE_SIZE=$(get_dir_bytes "$CACHE_BASE")
  echo "Total cache: $(bytes_to_human $CACHE_SIZE)"
  echo "Breakdown (top 10):"
  du -sh "$CACHE_BASE"/*/ 2>/dev/null | sort -rh | head -10

  # Safe caches to always clean (cross-platform names)
  SAFE_CACHES=(
    "go-build"
    "pip"
    "pnpm"
    "node"
    "thumbnails"
    "mesa_shader_cache"
    "mesa_shader_cache_db"
    "yarn"
    "typescript"
    "node-gyp"
  )

  for name in "${SAFE_CACHES[@]}"; do
    cache_dir="$CACHE_BASE/$name"
    if [ -d "$cache_dir" ]; then
      size=$(get_dir_bytes "$cache_dir")
      if (( size > 1048576 )); then
        do_clean "Clear $name cache ($(bytes_to_human $size))" rm -rf "$cache_dir"
      fi
    fi
  done

  # Larger conditional caches
  CONDITIONAL_CACHES=(
    "JetBrains"
    "whisper"
    "google-chrome"
    "Google"
    "ms-playwright"
    "Homebrew"
    "com.apple.DeveloperTools"
    "com.apple.dt.Xcode"
    "com.spotify.client"
    "Firefox"
  )

  for name in "${CONDITIONAL_CACHES[@]}"; do
    cache_dir="$CACHE_BASE/$name"
    if [ -d "$cache_dir" ]; then
      size=$(get_dir_bytes "$cache_dir")
      if (( size > 104857600 )); then
        echo "Large cache: $name ($(bytes_to_human $size))"
        do_clean "Clear $name cache" rm -rf "$cache_dir"
      fi
    fi
  done
fi

# pip cache purge
if command -v pip &>/dev/null; then
  do_clean "Purge pip cache" pip cache purge
fi

# go clean
if command -v go &>/dev/null; then
  do_clean "Clean Go build cache" go clean -cache
fi

# ============================================================
# 4. macOS-specific caches
# ============================================================
if $IS_MAC; then
  section "macOS caches"

  # Derived Data (Xcode)
  DERIVED="$HOME/Library/Developer/Xcode/DerivedData"
  if [ -d "$DERIVED" ]; then
    size=$(get_dir_bytes "$DERIVED")
    if (( size > 104857600 )); then
      echo "Xcode DerivedData: $(bytes_to_human $size)"
      do_clean "Clear Xcode DerivedData" rm -rf "$DERIVED"/*
    fi
  fi

  # Xcode Archives (old builds)
  ARCHIVES="$HOME/Library/Developer/Xcode/Archives"
  if [ -d "$ARCHIVES" ]; then
    size=$(get_dir_bytes "$ARCHIVES")
    if (( size > 104857600 )); then
      echo "Xcode Archives: $(bytes_to_human $size)"
      do_clean "Clear Xcode Archives" rm -rf "$ARCHIVES"/*
    fi
  fi

  # iOS Device Support
  DEVICE_SUPPORT="$HOME/Library/Developer/Xcode/iOS DeviceSupport"
  if [ -d "$DEVICE_SUPPORT" ]; then
    size=$(get_dir_bytes "$DEVICE_SUPPORT")
    if (( size > 524288000 )); then
      echo "iOS DeviceSupport: $(bytes_to_human $size)"
      do_clean "Clear iOS DeviceSupport" rm -rf "$DEVICE_SUPPORT"/*
    fi
  fi

  # CoreSimulator (old simulator data)
  SIMULATORS="$HOME/Library/Developer/CoreSimulator/Caches"
  if [ -d "$SIMULATORS" ]; then
    size=$(get_dir_bytes "$SIMULATORS")
    if (( size > 104857600 )); then
      echo "CoreSimulator Caches: $(bytes_to_human $size)"
      do_clean "Clear CoreSimulator caches" rm -rf "$SIMULATORS"/*
    fi
  fi

  # Apple logs
  APPLE_LOGS="$HOME/Library/Logs"
  if [ -d "$APPLE_LOGS" ]; then
    size=$(get_dir_bytes "$APPLE_LOGS")
    if (( size > 104857600 )); then
      echo "User logs: $(bytes_to_human $size)"
      do_clean "Clear old user logs" find "$APPLE_LOGS" -name "*.log" -mtime +30 -delete
    fi
  fi
fi

# ============================================================
# 5. Package manager cleanup
# ============================================================

# --- Apt (Linux/Debian) ---
if $IS_LINUX && command -v apt &>/dev/null; then
  section "Apt cache"
  APT_SIZE=$(sudo du -sb /var/cache/apt 2>/dev/null | awk '{print $1}' || echo 0)
  echo "Apt cache: $(bytes_to_human $APT_SIZE)"
  do_clean "Clean apt cache" sudo apt clean -y
fi

# --- Homebrew (macOS or Linux) ---
if ! $SKIP_BREW && command -v brew &>/dev/null; then
  section "Homebrew"
  do_clean "Cleanup Homebrew (remove old versions, clear cache)" brew cleanup --prune=7 -s
fi

# ============================================================
# 6. Journal logs (Linux only)
# ============================================================
if $IS_LINUX && command -v journalctl &>/dev/null; then
  section "Journal logs"
  journalctl --disk-usage 2>/dev/null || true
  do_clean "Vacuum journals to 200M" sudo journalctl --vacuum-size=200M
fi

# ============================================================
# 7. Snap cleanup (Linux only)
# ============================================================
if $IS_LINUX && ! $SKIP_SNAP && command -v snap &>/dev/null; then
  section "Snap: disabled revisions"
  DISABLED=$(snap list --all 2>/dev/null | awk '/disabled/{print $1, $3}')
  if [ -n "$DISABLED" ]; then
    echo "Disabled snap revisions found:"
    echo "$DISABLED"
    if ! $DRY_RUN; then
      echo "$DISABLED" | while read -r snapname revision; do
        echo "Removing $snapname revision $revision..."
        sudo snap remove "$snapname" --revision="$revision" 2>&1 || true
      done
    else
      echo "[DRY-RUN] Would remove all disabled snap revisions"
    fi
  else
    echo "No disabled snap revisions"
  fi
fi

# ============================================================
# 8. Docker cleanup
# ============================================================
if ! $SKIP_DOCKER && command -v docker &>/dev/null; then
  section "Docker"
  docker system df 2>/dev/null || true
  do_clean "Prune dangling Docker images and build cache" docker system prune -f
fi

# ============================================================
# 9. Old kernels (Linux only)
# ============================================================
if $IS_LINUX && ! $SKIP_KERNELS; then
  section "Old kernels"
  CURRENT=$(uname -r)
  echo "Running kernel: $CURRENT"
  OLD_KERNELS=$(dpkg -l 'linux-image-*' 2>/dev/null | grep '^ii' | awk '{print $2}' | grep -v "$CURRENT" | grep -v 'generic$' | grep 'linux-image-[0-9]') || true
  if [ -n "$OLD_KERNELS" ]; then
    echo "Old kernels found:"
    echo "$OLD_KERNELS"
    if ! $DRY_RUN; then
      echo "$OLD_KERNELS" | xargs sudo apt purge -y 2>&1 || true
      sudo apt autoremove -y 2>&1 || true
    else
      echo "[DRY-RUN] Would purge old kernels"
    fi
  else
    echo "No old kernels to remove"
  fi
fi

# ============================================================
# Summary
# ============================================================
section "Summary"
END_AVAIL=$(get_avail_kb)
FREED_KB=$((END_AVAIL - START_AVAIL))
if (( FREED_KB > 0 )); then
  FREED_BYTES=$((FREED_KB * 1024))
  echo "Freed: $(bytes_to_human $FREED_BYTES)"
else
  echo "Freed: minimal (most targets were already clean)"
fi

if $IS_MAC; then
  df -h / | tail -1 | awk '{printf "Disk: %s used of %s (%s available)\n", $3, $2, $4}'
else
  df -h / | tail -1 | awk '{printf "Disk: %s used of %s (%s free, %s)\n", $3, $2, $4, $5}'
fi

if $DRY_RUN; then
  echo ""
  echo "This was a dry run. Re-run without --dry-run to actually clean."
fi
