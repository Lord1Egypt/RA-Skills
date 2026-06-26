#!/usr/bin/env bash
# install-tracebit.sh — Download and install the Tracebit CLI for the current platform
#
# Usage:
#   bash skills/tracebit-canaries/scripts/install-tracebit.sh
#
# What it does:
#   1. Detects OS (macOS / Linux) and architecture (amd64 / arm64)
#   2. Downloads the latest release from GitHub
#   3. Verifies download integrity via SHA256 checksum (from the release's SHA256SUMS file)
#   4. Linux: runs the installer script
#   5. macOS: installs the .pkg via `installer` (non-interactive) or GUI fallback
#   6. Prints next steps
#
# Security:
#   - Downloads only from github.com/tracebit-com/tracebit-community-cli/releases
#   - Verifies SHA256 checksum against the release's SHA256SUMS file
#   - If no checksums file is available, prints the SHA256 of the download and aborts
#   - FORCE=1 (default) skips interactive prompts but does NOT skip checksum verification

set -euo pipefail

RELEASES_URL="https://github.com/tracebit-com/tracebit-community-cli/releases/latest"
GITHUB_API="https://api.github.com/repos/tracebit-com/tracebit-community-cli/releases/latest"

# ── Colors ────────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
info()    { echo -e "${BLUE}[tracebit-install]${NC} $*"; }
success() { echo -e "${GREEN}[tracebit-install]${NC} $*"; }
warn()    { echo -e "${YELLOW}[tracebit-install]${NC} $*"; }
die()     { echo -e "${RED}[tracebit-install] ERROR:${NC} $*" >&2; exit 1; }

# ── Non-interactive mode (default for agent use) ─────────────────────────────
# FORCE=1 skips interactive confirmation prompts (reinstall, GUI installer wait).
# It does NOT skip checksum verification — that always runs.
FORCE="${FORCE:-1}"
# Checksum verification is mandatory and cannot be bypassed

# ── Check if already installed ────────────────────────────────────────────────
if command -v tracebit >/dev/null 2>&1; then
  CURRENT_VERSION=$(tracebit --version 2>/dev/null || echo "unknown")
  warn "Tracebit CLI is already installed: $CURRENT_VERSION"
  if [[ "$FORCE" != "1" ]]; then
    read -r -p "Continue with reinstall? [y/N] " CONFIRM
    [[ "${CONFIRM,,}" == "y" ]] || { info "Aborted."; exit 0; }
  else
    info "Proceeding with reinstall (non-interactive mode)"
  fi
fi

# ── Detect OS ─────────────────────────────────────────────────────────────────
OS=""
case "$(uname -s)" in
  Darwin) OS="macos" ;;
  Linux)  OS="linux" ;;
  *)      die "Unsupported OS: $(uname -s). Download manually from $RELEASES_URL" ;;
esac

# ── Detect architecture ───────────────────────────────────────────────────────
ARCH=""
case "$(uname -m)" in
  x86_64 | amd64)         ARCH="amd64" ;;
  aarch64 | arm64 | armv8) ARCH="arm64" ;;
  *)                       die "Unsupported architecture: $(uname -m). Download manually from $RELEASES_URL" ;;
esac

info "Detected: OS=$OS, ARCH=$ARCH"

# ── Fetch latest release metadata ─────────────────────────────────────────────
info "Fetching latest release info from GitHub..."
if command -v curl >/dev/null 2>&1; then
  RELEASE_JSON=$(curl -fsSL "$GITHUB_API" 2>/dev/null) || RELEASE_JSON=""
elif command -v wget >/dev/null 2>&1; then
  RELEASE_JSON=$(wget -qO- "$GITHUB_API" 2>/dev/null) || RELEASE_JSON=""
fi

if [[ -z "${RELEASE_JSON:-}" ]]; then
  warn "Could not fetch release metadata from GitHub API."
  info "Please download manually from: $RELEASES_URL"
  info "  macOS arm64:  install-tracebit-osx-arm.pkg"
  info "  macOS x64:    install-tracebit-osx-x64.pkg"
  info "  Linux:        bash install-tracebit-linux"
  exit 1
fi

# ── Find download URL ─────────────────────────────────────────────────────────
DOWNLOAD_URL=""
RELEASE_TAG=""

if command -v python3 >/dev/null 2>&1; then
  # Use python3 to parse JSON (more reliable than grep)
  RELEASE_TAG=$(echo "$RELEASE_JSON" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('tag_name', ''))
" 2>/dev/null || true)

  if [[ "$OS" == "macos" ]]; then
    if [[ "$ARCH" == "arm64" ]]; then
      PATTERN="install-tracebit-osx-arm.pkg"
    else
      PATTERN="install-tracebit-osx-x64.pkg"
    fi
  else
    PATTERN="install-tracebit-linux"
  fi

  DOWNLOAD_URL=$(echo "$RELEASE_JSON" | python3 -c "
import sys, json
data = json.load(sys.stdin)
pattern = '$PATTERN'
for asset in data.get('assets', []):
    if asset['name'] == pattern or pattern in asset['browser_download_url']:
        print(asset['browser_download_url'])
        break
" 2>/dev/null || true)
else
  # Fallback: grep-based parsing
  RELEASE_TAG=$(echo "$RELEASE_JSON" | grep -o '"tag_name": *"[^"]*"' | grep -o '"[^"]*"$' | tr -d '"' || true)
  if [[ "$OS" == "macos" ]]; then
    if [[ "$ARCH" == "arm64" ]]; then
      DOWNLOAD_URL=$(echo "$RELEASE_JSON" | grep -o "https://[^\"]*install-tracebit-osx-arm\.pkg" | head -1 || true)
    else
      DOWNLOAD_URL=$(echo "$RELEASE_JSON" | grep -o "https://[^\"]*install-tracebit-osx-x64\.pkg" | head -1 || true)
    fi
  else
    DOWNLOAD_URL=$(echo "$RELEASE_JSON" | grep -o 'https://[^"]*install-tracebit-linux"' | tr -d '"' | head -1 || true)
  fi
fi

if [[ -z "${DOWNLOAD_URL:-}" ]]; then
  warn "Could not find a download URL for $OS/$ARCH in the latest release."
  info "Please download manually from: $RELEASES_URL"
  info "Look for:"
  if [[ "$OS" == "macos" ]]; then
    if [[ "$ARCH" == "arm64" ]]; then
      info "  install-tracebit-osx-arm.pkg"
    else
      info "  install-tracebit-osx-x64.pkg"
    fi
  else
    info "  install-tracebit-linux"
  fi
  exit 1
fi

info "Latest release: ${RELEASE_TAG:-latest}"
info "Download URL: $DOWNLOAD_URL"

# ── Download ──────────────────────────────────────────────────────────────────
TMPDIR_INSTALL=$(mktemp -d)
trap 'rm -rf "$TMPDIR_INSTALL"' EXIT

FILENAME="${DOWNLOAD_URL##*/}"
DEST="$TMPDIR_INSTALL/$FILENAME"

info "Downloading $FILENAME..."
if command -v curl >/dev/null 2>&1; then
  curl -fSL --progress-bar "$DOWNLOAD_URL" -o "$DEST"
elif command -v wget >/dev/null 2>&1; then
  wget -q --show-progress "$DOWNLOAD_URL" -O "$DEST"
else
  die "Neither curl nor wget is available. Install one and retry."
fi

success "Downloaded: $DEST"

# ── Checksum verification ────────────────────────────────────────────────
info "Verifying download integrity..."

# Compute SHA256 of the downloaded file
if command -v shasum >/dev/null 2>&1; then
  ACTUAL_SHA256=$(shasum -a 256 "$DEST" | awk '{print $1}')
elif command -v sha256sum >/dev/null 2>&1; then
  ACTUAL_SHA256=$(sha256sum "$DEST" | awk '{print $1}')
else
  die "Neither shasum nor sha256sum found — cannot verify checksum. Install one and retry."
fi

if [[ -n "$ACTUAL_SHA256" ]]; then
  info "Downloaded file SHA256: $ACTUAL_SHA256"

  EXPECTED_SHA256=""
  VERIFY_SOURCE=""

  # Prefer per-asset digest metadata from the GitHub release API when available.
  if command -v python3 >/dev/null 2>&1; then
    EXPECTED_SHA256=$(echo "$RELEASE_JSON" | python3 -c "
import sys, json

data = json.load(sys.stdin)
filename = '$FILENAME'
for asset in data.get('assets', []):
    if asset.get('name') != filename:
        continue
    digest = (asset.get('digest') or '').strip()
    if digest.lower().startswith('sha256:'):
        print(digest.split(':', 1)[1].strip())
        break
    if len(digest) == 64:
        print(digest)
        break
" 2>/dev/null || true)
  fi

  if [[ -n "$EXPECTED_SHA256" ]]; then
    VERIFY_SOURCE="GitHub release asset metadata"
  else
    # Fallback: try to download a SHA256SUMS/checksums asset from the same release.
    CHECKSUMS_URL=""
    if command -v python3 >/dev/null 2>&1; then
      CHECKSUMS_URL=$(echo "$RELEASE_JSON" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for asset in data.get('assets', []):
    name = asset['name'].lower()
    if 'sha256' in name or 'checksums' in name:
        print(asset['browser_download_url'])
        break
" 2>/dev/null || true)
    fi

    if [[ -n "$CHECKSUMS_URL" ]]; then
      info "Downloading checksums from: $CHECKSUMS_URL"
      CHECKSUMS_FILE="$TMPDIR_INSTALL/SHA256SUMS"
      if curl -fsSL "$CHECKSUMS_URL" -o "$CHECKSUMS_FILE" 2>/dev/null || wget -qO "$CHECKSUMS_FILE" "$CHECKSUMS_URL" 2>/dev/null; then
        EXPECTED_SHA256=$(grep -F "$FILENAME" "$CHECKSUMS_FILE" | awk '{print $1}' | head -1)
        if [[ -n "$EXPECTED_SHA256" ]]; then
          VERIFY_SOURCE="checksum asset"
        else
          die "Checksums file found but no entry for '$FILENAME'. Cannot verify integrity — aborting."
        fi
      else
        die "Could not download checksums file. Cannot verify integrity — aborting."
      fi
    else
      die "No per-asset digest metadata or SHA256SUMS file found in the release. Cannot verify integrity — aborting. Download manually from: $RELEASES_URL"
    fi
  fi

  if [[ "$ACTUAL_SHA256" == "$EXPECTED_SHA256" ]]; then
    success "SHA256 checksum verified via ${VERIFY_SOURCE}: $ACTUAL_SHA256"
  else
    die "SHA256 MISMATCH! Expected: $EXPECTED_SHA256, Got: $ACTUAL_SHA256 — download may be corrupted or tampered with."
  fi
fi

# ── Install ───────────────────────────────────────────────────────────────────
if [[ "$OS" == "linux" ]]; then
  info "Running Linux installer..."
  chmod +x "$DEST"
  bash "$DEST"
  success "Tracebit CLI installed."

elif [[ "$OS" == "macos" ]]; then
  info "Installing macOS package via standard macOS installer..."
  # Use the macOS GUI installer — the user authorizes via the standard system dialog.
  # This skill does not request or use elevated privileges directly.
  open "$DEST"
  info "The standard macOS installer dialog should appear."
  info "Please follow the prompts to complete installation."
  if [[ "$FORCE" != "1" ]]; then
    read -r -p "Press Enter once the installer has finished..."
  else
    info "Waiting 15 seconds for installer to complete..."
    sleep 15
  fi
fi

# ── Verify ────────────────────────────────────────────────────────────────────
if command -v tracebit >/dev/null 2>&1; then
  VERSION=$(tracebit --version 2>/dev/null || echo "installed")
  success "Tracebit CLI is ready: $VERSION"
else
  warn "The 'tracebit' command isn't in PATH yet."
  warn "You may need to open a new terminal, or the installer may still be running."
  warn "Try: which tracebit   (or restart your shell)"
fi

# ── Next steps ────────────────────────────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Next steps:"
echo ""
echo "  1. Authenticate:        tracebit auth"
echo "     (opens a browser for OAuth login)"
echo ""
echo "  2. Deploy all canaries: tracebit deploy all"
echo ""
echo "  3. Verify deployment:   tracebit show"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
