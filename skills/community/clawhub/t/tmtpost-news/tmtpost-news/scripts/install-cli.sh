#!/bin/sh
set -e

# install-cli.sh — Download the CLI into the skill directory and verify it.
# Usage: sh scripts/install-cli.sh [--force]

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

BASE_DOWNLOAD_URL="https://pack.tmtpost.net/tmtpost-news"
DEFAULT_CHECKSUM_URL="$BASE_DOWNLOAD_URL/checksums.txt"
FORCE_INSTALL="false"

# ── helpers ──────────────────────────────────────────────────────────
fail() { echo "Error: $1" >&2; exit 1; }

json_escape() {
  printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g; s/	/\\t/g' | tr '\n' ' '
}

usage() {
  cat <<EOF
Usage: sh scripts/install-cli.sh [--force]

Download the current-platform CLI into the skill directory and verify it.
Use --force to install locally even if a global CLI is available.
EOF
}

compute_sha256() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | cut -d' ' -f1
    return 0
  fi
  if command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$1" | cut -d' ' -f1
    return 0
  fi
  return 1
}

extract_platform_path() {
  printf '%s\n' "$1" | awk -F/ '{ if (NF < 2) exit 1; print $(NF-1) "/" $NF }'
}

verify_checksum() {
  file_path="$1"
  checksum_url="$2"
  download_url="$3"

  if ! CHECKSUM_CONTENT="$(curl -fSL "$checksum_url" 2>/dev/null)"; then
    fail "failed to fetch checksums from $checksum_url"
  fi

  platform_path="$(extract_platform_path "$download_url")" || fail "failed to determine platform path from $download_url"
  EXPECTED_HASH="$(printf '%s\n' "$CHECKSUM_CONTENT" | awk -v p="$platform_path" '$2 == p { print $1; exit }')"

  if [ -z "$EXPECTED_HASH" ]; then
    fail "no matching checksum found for $platform_path in $checksum_url"
  fi

  ACTUAL_HASH="$(compute_sha256 "$file_path")" || fail "sha256sum or shasum is required for checksum verification"

  if [ "$ACTUAL_HASH" != "$EXPECTED_HASH" ]; then
    fail "checksum verification failed for $download_url
  expected: $EXPECTED_HASH
  actual:   $ACTUAL_HASH"
  fi

  echo "Checksum verification passed." >&2
}

while [ $# -gt 0 ]; do
  case "$1" in
    help|--help|-h) usage; exit 0 ;;
    --force) FORCE_INSTALL="true" ;;
    *) fail "unknown argument: $1" ;;
  esac
  shift
done

# ── platform detection ───────────────────────────────────────────────
detect_os() {
  case "$(uname -s)" in
    Darwin) echo "darwin" ;;
    Linux)  echo "linux" ;;
    *)      fail "unsupported os: $(uname -s)" ;;
  esac
}

detect_arch() {
  case "$(uname -m)" in
    arm64|aarch64) echo "arm64" ;;
    x86_64|amd64)  echo "amd64" ;;
    *)             fail "unsupported architecture: $(uname -m)" ;;
  esac
}

OS="$(detect_os)"
ARCH="$(detect_arch)"
CLI_FILENAME="tmtpost-news-cli"
LOCAL_CLI_PATH="$SKILL_DIR/$CLI_FILENAME"
DOWNLOAD_URL="$BASE_DOWNLOAD_URL/$OS-$ARCH/$CLI_FILENAME"
CLI_PATH="$LOCAL_CLI_PATH"

# ── check for global CLI first ──────────────────────────────────────
if [ "$FORCE_INSTALL" != "true" ] && [ ! -f "$LOCAL_CLI_PATH" ]; then
  GLOBAL_CLI_PATH="$(command -v "$CLI_FILENAME" 2>/dev/null || true)"
  if [ -n "$GLOBAL_CLI_PATH" ]; then
    if "$GLOBAL_CLI_PATH" help >/dev/null 2>&1; then
      RAW_VERSION_OUTPUT="$("$GLOBAL_CLI_PATH" version 2>&1)" || fail "global CLI version check failed: $RAW_VERSION_OUTPUT"
      echo "$RAW_VERSION_OUTPUT" | grep -q '"current_version"' || fail "global CLI version did not return valid JSON: $RAW_VERSION_OUTPUT"

      CURRENT_VERSION="$(echo "$RAW_VERSION_OUTPUT" | grep '"current_version"' | head -1 | sed 's/.*"current_version"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')"
      LATEST_VERSION="$(echo "$RAW_VERSION_OUTPUT" | grep '"latest_version"' | head -1 | sed 's/.*"latest_version"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')"

      [ -n "$CURRENT_VERSION" ] && CVJ="\"$CURRENT_VERSION\"" || CVJ="null"
      [ -n "$LATEST_VERSION" ] && LVJ="\"$LATEST_VERSION\"" || LVJ="null"
      RAW_ESCAPED="$(json_escape "$RAW_VERSION_OUTPUT")"

      cat <<EOF
{
  "installed": true,
  "source": "global",
  "platform": { "os": "$OS", "arch": "$ARCH", "cliPath": "$GLOBAL_CLI_PATH" },
  "downloadUrl": null,
  "currentVersion": $CVJ,
  "latestVersion": $LVJ,
  "rawVersionOutput": "$RAW_ESCAPED",
  "note": "Using globally installed CLI. No download needed."
}
EOF
      exit 0
    fi
  fi
fi

# ── download and install ────────────────────────────────────────────
TEMP_PATH="${CLI_PATH}.download.$$.$( date +%s )"

cleanup() { rm -f "$TEMP_PATH"; }
trap cleanup EXIT

echo "Downloading CLI from $DOWNLOAD_URL ..." >&2
curl -fSL -o "$TEMP_PATH" "$DOWNLOAD_URL" || fail "download failed from $DOWNLOAD_URL"

verify_checksum "$TEMP_PATH" "$DEFAULT_CHECKSUM_URL" "$DOWNLOAD_URL"

chmod +x "$TEMP_PATH"

echo "Verifying CLI ..." >&2
RAW_VERSION_OUTPUT="$("$TEMP_PATH" version 2>&1)" || fail "version check failed: $RAW_VERSION_OUTPUT"

echo "$RAW_VERSION_OUTPUT" | grep -q '"current_version"' || fail "version did not return valid JSON: $RAW_VERSION_OUTPUT"

mv -f "$TEMP_PATH" "$CLI_PATH"
chmod +x "$CLI_PATH"

# ── extract version fields ──────────────────────────────────────────
CURRENT_VERSION="$(echo "$RAW_VERSION_OUTPUT" | grep '"current_version"' | head -1 | sed 's/.*"current_version"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')"
LATEST_VERSION="$(echo "$RAW_VERSION_OUTPUT" | grep '"latest_version"' | head -1 | sed 's/.*"latest_version"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')"

[ -n "$CURRENT_VERSION" ] && CVJ="\"$CURRENT_VERSION\"" || CVJ="null"
[ -n "$LATEST_VERSION" ] && LVJ="\"$LATEST_VERSION\"" || LVJ="null"
RAW_ESCAPED="$(json_escape "$RAW_VERSION_OUTPUT")"

cat <<EOF
{
  "installed": true,
  "source": "local",
  "platform": { "os": "$OS", "arch": "$ARCH", "cliPath": "$CLI_PATH" },
  "downloadUrl": "$DOWNLOAD_URL",
  "currentVersion": $CVJ,
  "latestVersion": $LVJ,
  "rawVersionOutput": "$RAW_ESCAPED"
}
EOF
