#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

cat >"$TMP_DIR/browser-runtime-stub.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

STATE_DIR="${RUNTIME_STUB_DIR:?}"
TARGET_URL="${RUNTIME_STUB_TARGET_URL:?}"
EXPECTED_PROFILE="${RUNTIME_STUB_EXPECTED_PROFILE:-}"

record_profile() {
  local next=""
  while [ "$#" -gt 0 ]; do
    case "$1" in
      --profile-dir)
        next="$2"
        shift 2
        ;;
      *)
        shift
        ;;
    esac
  done
  printf '%s\n' "$next" >"$STATE_DIR/profile-dir"
  if [ -n "$EXPECTED_PROFILE" ] && [ "$next" = "$EXPECTED_PROFILE" ]; then
    printf '%s\n' "mapped" >"$STATE_DIR/mode"
  else
    printf '%s\n' "fresh" >"$STATE_DIR/mode"
  fi
}

mode_value() {
  if [ -f "$STATE_DIR/mode" ]; then
    cat "$STATE_DIR/mode"
  else
    printf '%s\n' "fresh"
  fi
}

case "${1:-}" in
  verify)
    exit 1
    ;;
  status)
    cat <<OUT
runtime: stopped
mode: gui
url: $TARGET_URL
profile_dir:
run_dir: $STATE_DIR/run
cdp_port: 19222
browser_pid:
xvfb_pid:
display: :88
OUT
    ;;
  start)
    shift
    record_profile "$@"
    echo "runtime started"
    ;;
  list-targets)
    cat <<OUT
[{"id":"target-1","type":"page","url":"$TARGET_URL"}]
OUT
    ;;
  select-target)
    echo "target-1"
    ;;
  check-page)
    check=""
    while [ "$#" -gt 0 ]; do
      case "$1" in
        --check)
          check="$2"
          shift 2
          ;;
        *)
          shift
          ;;
      esac
    done
    if [ "$(mode_value)" = "mapped" ]; then
      case "$check" in
        challenge)
          echo '{"hasChallenge":false}'
          ;;
        login-wall)
          echo '{"hasLoginWall":false}'
          ;;
        page-info)
          printf '{"title":"Ready","url":"%s","bodySnippet":"authenticated"}\n' "$TARGET_URL"
          ;;
      esac
    else
      case "$check" in
        challenge)
          echo '{"hasChallenge":false}'
          ;;
        login-wall)
          echo '{"hasLoginWall":true}'
          ;;
        page-info)
          echo '{"title":"Sign in","url":"about:blank","bodySnippet":""}'
          ;;
      esac
    fi
    ;;
  *)
    echo "unexpected runtime command: $1" >&2
    exit 1
    ;;
esac
EOF

cat >"$TMP_DIR/assisted-stub.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

case "${1:-}" in
  start)
    echo '[assisted-session] noVNC URL: http://127.0.0.1:6081/vnc.html?autoconnect=1&resize=remote'
    ;;
  status)
    cat <<OUT
assisted_session: running
run_dir: /tmp/assist
runtime_run_dir: /tmp/runtime
novnc_url: http://127.0.0.1:6081/vnc.html?autoconnect=1&resize=remote
OUT
    ;;
  *)
    echo "unexpected assisted command: $1" >&2
    exit 1
    ;;
esac
EOF

chmod +x "$TMP_DIR/browser-runtime-stub.sh" "$TMP_DIR/assisted-stub.sh"
mkdir -p "$TMP_DIR/home/.agent-browser/index" "$TMP_DIR/runtime"

cat >"$TMP_DIR/home/.agent-browser/index/identity-profiles.json" <<EOF
{
  "providers": {
    "accounts.google.com": {
      "profile_dir": "$TMP_DIR/home/.agent-browser/profiles/oauth-profile",
      "source_origin": "https://x.com",
      "source_session_key": "default",
      "updated_at": "2026-03-15T03:00:00Z"
    }
  }
}
EOF

google_output="$(
  HOME="$TMP_DIR/home" \
  RUNTIME_STUB_DIR="$TMP_DIR/runtime" \
  RUNTIME_STUB_TARGET_URL="https://myaccount.google.com/" \
  RUNTIME_STUB_EXPECTED_PROFILE="$TMP_DIR/home/.agent-browser/profiles/oauth-profile" \
  AGENT_BROWSER_RUNTIME_HELPER="$TMP_DIR/browser-runtime-stub.sh" \
  AGENT_BROWSER_ASSISTED_HELPER="$TMP_DIR/assisted-stub.sh" \
  "$BASE_DIR/open-protected-page.sh" \
    --url 'https://myaccount.google.com/' \
    --origin 'https://myaccount.google.com' \
    --session-key default
)"
printf '%s\n' "$google_output" | grep -q '"status": "ready"'
grep -q "$TMP_DIR/home/.agent-browser/profiles/oauth-profile" "$TMP_DIR/runtime/profile-dir"

cat >"$TMP_DIR/home/.agent-browser/index/identity-profiles.json" <<EOF
{
  "providers": {
    "github.com": {
      "profile_dir": "$TMP_DIR/home/.agent-browser/profiles/github-oauth-profile",
      "source_origin": "https://clawhub.ai",
      "source_session_key": "default",
      "updated_at": "2026-03-15T03:00:00Z"
    }
  }
}
EOF

github_output="$(
  HOME="$TMP_DIR/home" \
  RUNTIME_STUB_DIR="$TMP_DIR/runtime" \
  RUNTIME_STUB_TARGET_URL="https://github.com/settings/profile" \
  RUNTIME_STUB_EXPECTED_PROFILE="$TMP_DIR/home/.agent-browser/profiles/github-oauth-profile" \
  AGENT_BROWSER_RUNTIME_HELPER="$TMP_DIR/browser-runtime-stub.sh" \
  AGENT_BROWSER_ASSISTED_HELPER="$TMP_DIR/assisted-stub.sh" \
  "$BASE_DIR/open-protected-page.sh" \
    --url 'https://github.com/settings/profile' \
    --origin 'https://github.com' \
    --session-key default
)"
printf '%s\n' "$github_output" | grep -q '"status": "ready"'
grep -q "$TMP_DIR/home/.agent-browser/profiles/github-oauth-profile" "$TMP_DIR/runtime/profile-dir"

rm -f "$TMP_DIR/home/.agent-browser/index/identity-profiles.json" "$TMP_DIR/runtime/profile-dir" "$TMP_DIR/runtime/mode"
missing_output="$(
  HOME="$TMP_DIR/home" \
  RUNTIME_STUB_DIR="$TMP_DIR/runtime" \
  RUNTIME_STUB_TARGET_URL="https://github.com/settings/profile" \
  AGENT_BROWSER_RUNTIME_HELPER="$TMP_DIR/browser-runtime-stub.sh" \
  AGENT_BROWSER_ASSISTED_HELPER="$TMP_DIR/assisted-stub.sh" \
  "$BASE_DIR/open-protected-page.sh" \
    --url 'https://github.com/settings/profile' \
    --origin 'https://github.com' \
    --session-key default
)"
printf '%s\n' "$missing_output" | grep -q '"status": "needs-user"'
printf '%s\n' "$missing_output" | grep -q '"reason": "login-wall"'

printf '{broken json\n' >"$TMP_DIR/home/.agent-browser/index/identity-profiles.json"
rm -f "$TMP_DIR/runtime/profile-dir" "$TMP_DIR/runtime/mode"
corrupt_output="$(
  HOME="$TMP_DIR/home" \
  RUNTIME_STUB_DIR="$TMP_DIR/runtime" \
  RUNTIME_STUB_TARGET_URL="https://github.com/settings/profile" \
  AGENT_BROWSER_RUNTIME_HELPER="$TMP_DIR/browser-runtime-stub.sh" \
  AGENT_BROWSER_ASSISTED_HELPER="$TMP_DIR/assisted-stub.sh" \
  "$BASE_DIR/open-protected-page.sh" \
    --url 'https://github.com/settings/profile' \
    --origin 'https://github.com' \
    --session-key default
)"
printf '%s\n' "$corrupt_output" | grep -q '"status": "needs-user"'
printf '%s\n' "$corrupt_output" | grep -q '"reason": "login-wall"'
