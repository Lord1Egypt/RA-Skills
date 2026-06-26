#!/bin/sh
set -e

# cli-state.sh — Output install state, version/update status, and API key status.
# Usage: sh scripts/cli-state.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# ── helpers ──────────────────────────────────────────────────────────
fail() { echo "Error: $1" >&2; exit 1; }

json_escape() {
  printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g; s/	/\\t/g' | tr '\n' ' '
}

json_bool() {
  echo "$1" | grep "\"$2\"" | head -1 | sed 's/.*"'"$2"'"[[:space:]]*:[[:space:]]*\([a-z]*\).*/\1/'
}

# ── argument parsing ─────────────────────────────────────────────────
while [ $# -gt 0 ]; do
  case "$1" in
    help)
      echo "Usage: sh scripts/cli-state.sh"
      echo ""
      echo "Print install state, version/update status, and API key status."
      exit 0
      ;;
    *)
      fail "unknown argument: $1"
      ;;
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

# ── cli detection: prefer skill-local install, fall back to global ───
CLI_SOURCE="none"
CLI_PATH=""

if [ -f "$LOCAL_CLI_PATH" ]; then
  CLI_PATH="$LOCAL_CLI_PATH"
  CLI_SOURCE="local"
fi

if [ -z "$CLI_PATH" ]; then
  GLOBAL_CLI_PATH="$(command -v "$CLI_FILENAME" 2>/dev/null || true)"
  if [ -n "$GLOBAL_CLI_PATH" ] && "$GLOBAL_CLI_PATH" help >/dev/null 2>&1; then
    CLI_PATH="$GLOBAL_CLI_PATH"
    CLI_SOURCE="global"
  fi
fi

if [ -n "$CLI_PATH" ]; then
  CLI_EXISTS="true"
else
  CLI_EXISTS="false"
  CLI_PATH="$LOCAL_CLI_PATH"
fi

# ── update check ────────────────────────────────────────────────────
UPDATE_NEED_UPDATE="null"
UPDATE_ERROR="null"

if [ "$CLI_EXISTS" = "true" ]; then
  chmod +x "$CLI_PATH" 2>/dev/null || true

  VERSION_OUTPUT="$("$CLI_PATH" version 2>&1)" && VERSION_EXIT=0 || VERSION_EXIT=$?

  if [ "$VERSION_EXIT" -eq 0 ]; then
    if echo "$VERSION_OUTPUT" | grep -q '"need_update"'; then
      NEED_UPDATE="$(json_bool "$VERSION_OUTPUT" "need_update")"
      case "$NEED_UPDATE" in
        true|false)
          UPDATE_NEED_UPDATE="$NEED_UPDATE"
          ;;
        *)
          UPDATE_ERROR="\"$(json_escape "$CLI_PATH version did not return valid need_update value: ${VERSION_OUTPUT:-"(empty output)"}")\""
          ;;
      esac
    else
      UPDATE_ERROR="\"$(json_escape "$CLI_PATH version did not return valid JSON: ${VERSION_OUTPUT:-"(empty output)"}")\""
    fi
  elif [ -n "$VERSION_OUTPUT" ]; then
    UPDATE_ERROR="\"$(json_escape "$VERSION_OUTPUT")\""
  else
    UPDATE_ERROR="\"$(json_escape "$CLI_PATH version failed with exit code $VERSION_EXIT.")\""
  fi
fi

# ── api key state ────────────────────────────────────────────────────
APIKEY_STATUS="error"
APIKEY_PRESENT="false"
APIKEY_ERROR="null"

if [ "$CLI_EXISTS" = "true" ]; then
  chmod +x "$CLI_PATH" 2>/dev/null || true
  APIKEY_OUTPUT="$("$CLI_PATH" apikey-get 2>&1)" && APIKEY_EXIT=0 || APIKEY_EXIT=$?

  if [ "$APIKEY_EXIT" -eq 0 ]; then
    _key="$(echo "$APIKEY_OUTPUT" | grep -o 'API Key[[:space:]]*:[[:space:]]*.*' | sed 's/API Key[[:space:]]*:[[:space:]]*//' | tr -d '[:space:]')"
    _key="$(echo "$_key" | sed "s/^['\"]//; s/['\"]$//")"

    if [ -n "$_key" ]; then
      APIKEY_STATUS="configured"
      APIKEY_PRESENT="true"
    else
      APIKEY_STATUS="error"
      APIKEY_ERROR="\"CLI apikey-get succeeded, but API key could not be parsed from output.\""
    fi
  elif echo "$APIKEY_OUTPUT" | grep -qiE '未设置 API Key|not set' || [ "$APIKEY_EXIT" -eq 2 ]; then
    APIKEY_STATUS="missing"
  else
    APIKEY_STATUS="error"
    if [ -n "$APIKEY_OUTPUT" ]; then
      APIKEY_ERROR="\"$(json_escape "$APIKEY_OUTPUT")\""
    else
      APIKEY_ERROR="\"apikey-get failed with exit code ${APIKEY_EXIT}.\""
    fi
  fi
else
  APIKEY_STATUS="error"
  APIKEY_ERROR="\"CLI not found, cannot check API key.\""
fi

# ── output JSON ──────────────────────────────────────────────────────
cat <<EOF
{
  "platform": {
    "os": "$OS",
    "arch": "$ARCH",
    "cliPath": "$CLI_PATH",
    "cliSource": "$CLI_SOURCE"
  },
  "cliExists": $CLI_EXISTS,
  "update": {
    "needUpdate": $UPDATE_NEED_UPDATE,
    "error": $UPDATE_ERROR
  },
  "apiKey": {
    "status": "$APIKEY_STATUS",
    "present": $APIKEY_PRESENT,
    "error": $APIKEY_ERROR
  }
}
EOF
