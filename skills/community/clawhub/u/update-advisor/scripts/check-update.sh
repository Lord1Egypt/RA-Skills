#!/usr/bin/env bash
# check-update.sh — OpenClaw update status check
# Output: structured JSON for the agent analysis layer
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARSE_SCRIPT="$SCRIPT_DIR/parse_changelog.py"
ASSEMBLE_SCRIPT="$SCRIPT_DIR/assemble_result.py"

# Use mktemp to avoid race conditions on shared /tmp paths
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

CHANGELOG_RESULT="$TMP_DIR/changelog.json"
UPDATE_STATUS="$TMP_DIR/update_status.txt"
UPDATE_STATUS_JSON="$TMP_DIR/update_status.json"
DOCTOR_OUTPUT="$TMP_DIR/doctor.txt"
DOCTOR_EXIT="$TMP_DIR/doctor_exit.txt"
RESULT_FILE="$TMP_DIR/result.json"

# ── Portable timeout wrapper ──────────────────────────────────────────────────
# macOS ships without GNU `timeout`; use gtimeout (coreutils) if available,
# otherwise fall back to a background-job approach.
run_timeout() {
  local secs=$1; shift
  if command -v gtimeout &>/dev/null; then
    gtimeout "$secs" "$@"
  elif command -v timeout &>/dev/null; then
    timeout "$secs" "$@"
  else
    # Pure-bash fallback: background job + killer
    "$@" &
    local pid=$!
    ( sleep "$secs" && kill -TERM "$pid" 2>/dev/null ) &
    local killer=$!
    wait "$pid" 2>/dev/null
    local rc=$?
    kill "$killer" 2>/dev/null
    wait "$killer" 2>/dev/null
    return $rc
  fi
}

# ── Portable realpath ─────────────────────────────────────────────────────────
# macOS readlink does not support -f; use Python as a portable fallback.
resolve_realpath() {
  python3 -c "import os, sys; print(os.path.realpath(sys.argv[1]))" "$1" 2>/dev/null \
    || readlink -f "$1" 2>/dev/null \
    || echo "$1"
}

# ── 1. Locate CHANGELOG.md ───────────────────────────────────────────────────
# Support npm-global, pnpm, and resolve from the openclaw binary itself.
find_changelog() {
  # Prefer the actual package root reported by OpenClaw when available.
  local status_root="${1:-}"
  if [[ -n "$status_root" && -f "$status_root/CHANGELOG.md" ]]; then
    echo "$status_root/CHANGELOG.md"
    return
  fi

  # Try npm prefix first
  local npm_prefix
  npm_prefix="$(npm config get prefix 2>/dev/null || true)"
  if [[ -n "$npm_prefix" && -f "$npm_prefix/lib/node_modules/openclaw/CHANGELOG.md" ]]; then
    echo "$npm_prefix/lib/node_modules/openclaw/CHANGELOG.md"
    return
  fi

  # Resolve from the openclaw binary itself. Walk up a few levels because
  # package managers may symlink to openclaw.mjs, bin/openclaw, or wrappers.
  local oc_bin
  oc_bin="$(which openclaw 2>/dev/null || true)"
  if [[ -n "$oc_bin" ]]; then
    local dir
    dir="$(dirname "$(resolve_realpath "$oc_bin")")"
    for _ in 1 2 3 4 5; do
      if [[ -f "$dir/CHANGELOG.md" ]]; then
        echo "$dir/CHANGELOG.md"
        return
      fi
      dir="$(dirname "$dir")"
    done
  fi

  # Try pnpm global store last (cap depth to avoid slow scans on large stores).
  # This is less precise than the active binary path, but useful for unusual setups.
  # pnpm default differs by OS: ~/Library/pnpm on macOS, ~/.local/share/pnpm on Linux
  local pnpm_home="${PNPM_HOME:-}"
  if [[ -z "$pnpm_home" ]]; then
    case "$(uname)" in
      Darwin) pnpm_home="$HOME/Library/pnpm" ;;
      *)      pnpm_home="$HOME/.local/share/pnpm" ;;
    esac
  fi
  if [[ -d "$pnpm_home" ]]; then
    local pnpm_candidate
    pnpm_candidate="$(find "$pnpm_home" -maxdepth 6 -name "CHANGELOG.md" -path "*/openclaw/*" 2>/dev/null | head -1 || true)"
    if [[ -n "$pnpm_candidate" ]]; then
      echo "$pnpm_candidate"
      return
    fi
  fi

  echo ""
}

# ── 2. Version info ──────────────────────────────────────────────────────────
# Check openclaw is findable before calling --version
if ! command -v openclaw &>/dev/null; then
  echo '{"error":"openclaw not found in PATH. Please ensure it is installed and PATH is configured correctly."}'
  exit 1
fi
CURRENT="$(openclaw --version 2>/dev/null | grep -oE '[0-9]{4}\.[0-9]+\.[0-9]+' | head -1 || true)"
if [[ -z "$CURRENT" ]]; then
  echo '{"error":"openclaw found in PATH but --version returned no recognizable version string. The installation may be broken."}'
  exit 1
fi

# Ask OpenClaw itself for update metadata when supported. This gives the active
# package root and latest version without guessing package-manager internals.
run_timeout 30 openclaw update status --json > "$UPDATE_STATUS_JSON" 2>/dev/null || true
STATUS_ROOT="$(python3 -c 'import json,sys; p=sys.argv[1];
try:
    data=json.load(open(p)); print(data.get("update",{}).get("root","") or "")
except Exception:
    print("")' "$UPDATE_STATUS_JSON")"
STATUS_LATEST="$(python3 -c 'import json,sys; p=sys.argv[1];
try:
    data=json.load(open(p)); print(data.get("availability",{}).get("latestVersion") or data.get("update",{}).get("registry",{}).get("latestVersion") or "")
except Exception:
    print("")' "$UPDATE_STATUS_JSON" | grep -oE '[0-9]{4}\.[0-9]+\.[0-9]+' | head -1 || true)"

NPM_ERR="$TMP_DIR/npm_err.txt"
LATEST="$STATUS_LATEST"
if [[ -z "$LATEST" ]]; then
  LATEST="$(run_timeout 15 npm view openclaw version 2>"$NPM_ERR" | tr -d '[:space:]' | grep -oE '[0-9]{4}\.[0-9]+\.[0-9]+' | head -1 || true)"
fi
if [[ -z "$LATEST" ]]; then
  NPM_ERR_MSG="$(head -3 "$NPM_ERR" 2>/dev/null | tr '\n' ' ' || true)"
  python3 -c "import json,sys; print(json.dumps({'error':'Could not fetch latest version from npm registry. '+sys.argv[1]+'Try again or check your network connection.'}))" "$NPM_ERR_MSG"
  exit 1
fi

HAS_UPDATE="false"
[[ "$CURRENT" != "$LATEST" ]] && HAS_UPDATE="true"

CHANGELOG_PATH="$(find_changelog "$STATUS_ROOT")"

# ── 3. Changelog delta extraction ────────────────────────────────────────────
if [[ -n "$CHANGELOG_PATH" ]]; then
  python3 "$PARSE_SCRIPT" "$CHANGELOG_PATH" "$CURRENT" "$LATEST" \
    > "$CHANGELOG_RESULT" 2>/dev/null \
    || echo '{"delta":"Failed to parse changelog.","flagged":[]}' > "$CHANGELOG_RESULT"
else
  echo '{"delta":"CHANGELOG.md not found. Install path could not be determined.","flagged":[],"changelog_not_found":true}' \
    > "$CHANGELOG_RESULT"
fi

# ── 4. openclaw update status ────────────────────────────────────────────────
run_timeout 30 openclaw update status > "$UPDATE_STATUS" 2>&1 || true

# ── 5. openclaw doctor ───────────────────────────────────────────────────────
DOCTOR_RC=0
run_timeout 30 openclaw doctor > "$DOCTOR_OUTPUT" 2>&1 || DOCTOR_RC=$?
echo "$DOCTOR_RC" > "$DOCTOR_EXIT"

# ── 6. Assemble final JSON ───────────────────────────────────────────────────
python3 "$ASSEMBLE_SCRIPT" \
  "$CURRENT" "$LATEST" "$HAS_UPDATE" \
  "$CHANGELOG_RESULT" \
  "$UPDATE_STATUS" \
  "$DOCTOR_OUTPUT" \
  "$UPDATE_STATUS_JSON" \
  "$DOCTOR_EXIT" \
  > "$RESULT_FILE"

cat "$RESULT_FILE"
