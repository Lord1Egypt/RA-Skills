#!/usr/bin/env bash
# video-fetch skill installer
# - All binaries are SHA256-verified before installation
# - ALL binaries (yt-dlp and rclone 115-fork) are installed to ~/.local/bin (user-only)
# - Does NOT install anything to /usr/local/bin or any system-wide path
# - MAY append ~/.local/bin to PATH in shell profile files (~/.bashrc, ~/.profile) if not already present
# - No credentials are collected during installation; auth is handled separately

# User-local install directory (no root/sudo required)
INSTALL_DIR="${HOME}/.local/bin"
mkdir -p "${INSTALL_DIR}"
[[ ":${PATH}:" != *":${INSTALL_DIR}:"* ]] && export PATH="${INSTALL_DIR}:${PATH}"

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ok()  { echo -e "${GREEN}[✓]${NC} $*"; }
info(){ echo -e "${YELLOW}[→]${NC} $*"; }
fail(){ echo -e "${RED}[✗]${NC} $*"; exit 1; }

echo ''
echo '══════════════════════════════════════'
echo '  video-fetch skill installer'
echo '══════════════════════════════════════'
echo ''
info "This installer will:"
info "  1. Install yt-dlp to ~/.local/bin (from github.com/yt-dlp/yt-dlp, SHA256 verified)"
info "  2. Install rclone 115-fork to ~/.local/bin (from github.com/gaoyb7/rclone-release, SHA256 verified)"
info "     All binaries install to user directory only (~/.local/bin) — no system paths modified"
info "  3. Install aria2 via system package manager"
info "  4. Install python3.12 + p115client via pip"
echo ''

# ── 1. yt-dlp ────────────────────────────────────────────────────
if command -v yt-dlp &>/dev/null; then
  ok "yt-dlp already installed ($(yt-dlp --version))"
else
  info "Installing yt-dlp ..."
  YTDLP_TMP=$(mktemp)
  curl -fsSL https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp \
    -o "${YTDLP_TMP}"
  if [[ ! -s "${YTDLP_TMP}" ]]; then
    rm -f "${YTDLP_TMP}"
    fail "yt-dlp download failed or file is empty"
  fi
  # Verify SHA256 against official checksum file (mandatory)
  YTDLP_SHA_TMP=$(mktemp)
  curl -fsSL https://github.com/yt-dlp/yt-dlp/releases/latest/download/SHA2-256SUMS \
    -o "${YTDLP_SHA_TMP}"
  if [[ ! -s "${YTDLP_SHA_TMP}" ]]; then
    rm -f "${YTDLP_TMP}" "${YTDLP_SHA_TMP}"
    fail "Cannot fetch yt-dlp checksum file — refusing to install (check network)"
  fi
  EXPECTED=$(grep ' yt-dlp$' "${YTDLP_SHA_TMP}" | awk '{print $1}')
  ACTUAL=$(sha256sum "${YTDLP_TMP}" | awk '{print $1}')
  if [[ -z "$EXPECTED" || "$EXPECTED" != "$ACTUAL" ]]; then
    rm -f "${YTDLP_TMP}" "${YTDLP_SHA_TMP}"
    fail "yt-dlp SHA256 verification failed — refusing to install"
  fi
  ok "yt-dlp SHA256 verified"
  rm -f "${YTDLP_SHA_TMP}"
  mv "${YTDLP_TMP}" "${INSTALL_DIR}/yt-dlp" && chmod +x "${INSTALL_DIR}/yt-dlp"
  ok "yt-dlp installed to ${INSTALL_DIR}/yt-dlp ($(yt-dlp --version))"
fi

# ── 2. rclone 115-fork (user directory only) ─────────────────────
# Installed to INSTALL_DIR (~/.local/bin) — does NOT touch any system path
RCLONE_INSTALL_DIR="${INSTALL_DIR}"

NEED_RCLONE=true
if [[ -f "${RCLONE_INSTALL_DIR}/rclone" ]] && "${RCLONE_INSTALL_DIR}/rclone" help backends 2>&1 | grep -q '115'; then
  ok "rclone 115-fork already installed ($(${RCLONE_INSTALL_DIR}/rclone version | head -1))"
  NEED_RCLONE=false
fi

if $NEED_RCLONE; then
  info "Installing rclone 115-fork to ${RCLONE_INSTALL_DIR}/rclone ..."
  info "Source: https://github.com/gaoyb7/rclone-release (115 Pan support fork)"
  ARCH=$(uname -m)
  case $ARCH in
    x86_64)  RCLONE_FILE="rclone_v1_20250119_Linux_x86_64.tar.gz" ;;
    aarch64) RCLONE_FILE="rclone_v1_20250119_Linux_arm64.tar.gz" ;;
    armv7*)  RCLONE_FILE="rclone_v1_20250119_Linux_armv7.tar.gz" ;;
    armv6*)  RCLONE_FILE="rclone_v1_20250119_Linux_armv6.tar.gz" ;;
    *)       fail "Unsupported architecture: $ARCH" ;;
  esac

  # SHA256 values verified from gaoyb7/rclone-release v1_20250119
  declare -A RCLONE_SHA256=(
    [rclone_v1_20250119_Linux_x86_64.tar.gz]="88419bdc269da9e8a9c02617de3afcc83197288164131bb3eec16c6e6fb88bba"
    [rclone_v1_20250119_Linux_arm64.tar.gz]="b348552be45ec74da1a9924b836ec02964203d07da8fbb7add10a953fda45839"
    [rclone_v1_20250119_Linux_armv7.tar.gz]="d41c849093c5362989755e606d156f6d6a30a0a17f853a8c411abb16878d0700"
    [rclone_v1_20250119_Linux_armv6.tar.gz]="bd07fd47e26bd8ce20d0963bfa4daa671bcc81413b1149168fd7ceffc6c970be"
  )

  RCLONE_TMP=$(mktemp -d)
  curl -fsSL "https://github.com/gaoyb7/rclone-release/releases/download/v1_20250119/${RCLONE_FILE}" \
    -o "${RCLONE_TMP}/rclone.tar.gz"

  if [[ ! -s "${RCLONE_TMP}/rclone.tar.gz" ]]; then
    rm -rf "${RCLONE_TMP}"
    fail "rclone download failed or file is empty"
  fi

  # SHA256 verification (mandatory for all architectures)
  EXPECTED_SHA="${RCLONE_SHA256[$RCLONE_FILE]:-}"
  if [[ -z "$EXPECTED_SHA" ]]; then
    rm -rf "${RCLONE_TMP}"
    fail "No pinned SHA256 for architecture $ARCH — refusing to install"
  fi
  ACTUAL_SHA=$(sha256sum "${RCLONE_TMP}/rclone.tar.gz" | awk '{print $1}')
  if [[ "$EXPECTED_SHA" != "$ACTUAL_SHA" ]]; then
    rm -rf "${RCLONE_TMP}"
    fail "rclone SHA256 verification failed — refusing to install (expected: ${EXPECTED_SHA}, got: ${ACTUAL_SHA})"
  fi
  ok "rclone SHA256 verified"

  tar xzf "${RCLONE_TMP}/rclone.tar.gz" -C "${RCLONE_TMP}/"
  RCLONE_BIN=$(find "${RCLONE_TMP}" -type f -name 'rclone' | head -1)
  [[ -z "$RCLONE_BIN" ]] && fail "Failed to extract rclone binary"
  mv "$RCLONE_BIN" "${RCLONE_INSTALL_DIR}/rclone" && chmod +x "${RCLONE_INSTALL_DIR}/rclone"
  rm -rf "${RCLONE_TMP}"
  ok "rclone 115-fork installed to ${RCLONE_INSTALL_DIR}/rclone"

  # Add to shell profile if not already present
  PROFILE_LINE="export PATH=\"\${HOME}/.local/bin:\${PATH}\""
  for PROFILE in "${HOME}/.bashrc" "${HOME}/.bash_profile" "${HOME}/.profile"; do
    if [[ -f "$PROFILE" ]] && ! grep -q '\.local/bin' "$PROFILE"; then
      echo "" >> "$PROFILE"
      echo "# Added by video-fetch installer" >> "$PROFILE"
      echo "$PROFILE_LINE" >> "$PROFILE"
      info "Added ~/.local/bin to PATH in $PROFILE"
      break
    fi
  done
fi

# ── 3. aria2 ─────────────────────────────────────────────────────
if command -v aria2c &>/dev/null; then
  ok "aria2 already installed"
else
  info "Installing aria2 ..."
  if command -v yum &>/dev/null; then
    yum install -y aria2 &>/dev/null
  elif command -v apt-get &>/dev/null; then
    apt-get install -y aria2 &>/dev/null
  else
    fail "Cannot install aria2 — please install it manually and re-run"
  fi
  ok "aria2 installed"
fi

# ── 4. Python 3.12 + p115client ──────────────────────────────────
if python3.12 -c 'import p115client' &>/dev/null 2>&1; then
  ok "p115client already installed"
else
  info "Installing Python 3.12 + p115client ..."
  if ! command -v python3.12 &>/dev/null; then
    if command -v yum &>/dev/null; then
      yum install -y python3.12 &>/dev/null
    elif command -v apt-get &>/dev/null; then
      apt-get install -y python3.12 &>/dev/null
    else
      fail "Cannot install Python 3.12 — please install it manually and re-run"
    fi
  fi
  python3.12 -m ensurepip 2>/dev/null || true
  python3.12 -m pip install -q p115client
  ok "p115client installed"
fi

# ── 5. 115 Pan auth ──────────────────────────────────────────────
echo ''
echo '══════════════════════════════════════'
ok "All dependencies installed"
echo '══════════════════════════════════════'
echo ''

RCLONE_CMD="${RCLONE_INSTALL_DIR}/rclone"
if "${RCLONE_CMD}" listremotes 2>/dev/null | grep -q '115drive'; then
  ok "115 Pan already authorized — skipping login"
else
  info "Starting 115 Pan authorization (TV mode QR scan — does not affect phone/browser sessions)..."
  echo ''
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd)"
  export PATH="${INSTALL_DIR}:${PATH}"
  python3.12 "${SCRIPT_DIR}/115_qrlogin.py"
fi

echo ''
echo '══════════════════════════════════════'
echo '  Installation complete!'
echo ''
echo '  # Offline download via magnet'
echo '  python3.12 scripts/115_offline.py "magnet:?xt=..."'
echo ''
echo '  # Check download tasks'
echo '  python3.12 scripts/115_offline.py --list'
echo ''
echo '  # Download video URL and upload'
echo '  VIDEOFETCH_REMOTE=115drive:云下载 bash scripts/video_fetch.sh <url>'
echo ''
echo "  Note: rclone installed to ${RCLONE_INSTALL_DIR}/rclone"
echo "  Add to PATH permanently: export PATH=\"\${HOME}/.local/bin:\${PATH}\""
echo '══════════════════════════════════════'
echo ''
