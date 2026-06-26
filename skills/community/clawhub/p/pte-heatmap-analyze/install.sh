#!/bin/sh
# Ptengine Heatmap — ptengine-cli installer
# Wraps the official install script with status checking.
#
# Usage:
#   sh install.sh              # Install (if needed) and show status
#   sh install.sh --check-only # Check status without installing
set -eu

# Pin upstream to an immutable commit SHA (not a tag — tags can be moved).
# Bump together with any ptengine-cli release validated against this skill,
# and update PTENGINE_CLI_SHA256 with the new install script's checksum.
PTENGINE_CLI_REF="2a25f646fc0a13e6e5159c91bf0562f6b785af72"  # v0.1.0
PTENGINE_CLI_SHA256="80e78c5668c5e9cf702c05e3c023395cd5f18f5bf5daec404d4cde9d86d6361f"

CHECK_ONLY=false
if [ "${1-}" = "--check-only" ]; then
  CHECK_ONLY=true
fi

# ---------- helpers ----------
config_file="$HOME/.config/ptengine-cli/config.yaml"

has_cli() {
  command -v ptengine-cli >/dev/null 2>&1
}

has_config() {
  [ -f "$config_file" ] && grep -q "api_key:" "$config_file" 2>/dev/null
}

# ---------- check ----------
if has_cli; then
  VERSION=$(ptengine-cli version 2>/dev/null || echo "unknown")
  echo "ptengine-cli is installed.  ($VERSION)"

  if has_config; then
    echo "Configuration found at $config_file"
    ptengine-cli config show 2>/dev/null || true
    echo ""
    echo "STATUS: READY"
    exit 0
  else
    echo ""
    echo "WARNING: ptengine-cli is installed but not configured."
    echo "Run:  ptengine-cli config set --api-key <YOUR_API_KEY> --profile-id <YOUR_PROFILE_ID>"
    echo ""
    echo "STATUS: NEEDS_CONFIG"
    exit 1
  fi
fi

# ---------- not installed ----------
if [ "$CHECK_ONLY" = true ]; then
  echo "ptengine-cli is NOT installed."
  echo ""
  echo "STATUS: NOT_INSTALLED"
  exit 1
fi

# ---------- install ----------
echo "Installing ptengine-cli via official script..."
echo ""

install_url="https://raw.githubusercontent.com/Kocoro-lab/ptengine-cli/${PTENGINE_CLI_REF}/scripts/install.sh"
tmp_script=$(mktemp -t ptengine-install.XXXXXX) || {
  echo "ERROR: failed to create temp file." >&2
  exit 1
}
trap 'rm -f "$tmp_script"' EXIT INT TERM

# 1) Download fully to a file (no pipe-to-shell).
if ! curl -fsSL --proto '=https' --tlsv1.2 -o "$tmp_script" "$install_url"; then
  echo "ERROR: failed to download installer from $install_url" >&2
  exit 1
fi

# 2) Verify SHA256 against the pinned checksum before executing.
if command -v sha256sum >/dev/null 2>&1; then
  actual=$(sha256sum "$tmp_script" | awk '{print $1}')
elif command -v shasum >/dev/null 2>&1; then
  actual=$(shasum -a 256 "$tmp_script" | awk '{print $1}')
else
  echo "ERROR: no sha256 tool available (need sha256sum or shasum)." >&2
  exit 1
fi

if [ "$actual" != "$PTENGINE_CLI_SHA256" ]; then
  echo "ERROR: checksum mismatch for install script." >&2
  echo "  expected: $PTENGINE_CLI_SHA256" >&2
  echo "  actual:   $actual" >&2
  echo "Refusing to execute. The upstream script may have changed — review and update PTENGINE_CLI_SHA256 if intentional." >&2
  exit 1
fi

# 3) Now safe to execute.
sh "$tmp_script"

echo ""

if has_cli; then
  echo "Installation successful."
  echo ""
  echo "Next step — configure your API credentials:"
  echo "  ptengine-cli config set --api-key <YOUR_API_KEY> --profile-id <YOUR_PROFILE_ID>"
  echo ""
  echo "STATUS: INSTALLED_NEEDS_CONFIG"
else
  echo "ERROR: Installation failed. ptengine-cli not found in PATH."
  echo ""
  echo "STATUS: INSTALL_FAILED"
  exit 1
fi
