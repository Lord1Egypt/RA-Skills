#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

cat >"$TMP_DIR/browser-runtime-stub.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

MODE="${RUNTIME_STUB_MODE:-ready}"
STATE_FILE="${RUNTIME_STUB_STATE_FILE:-}"
LOG_FILE="${RUNTIME_STUB_LOG_FILE:-}"
if [ -n "$LOG_FILE" ]; then
  printf '%s\n' "$*" >>"$LOG_FILE"
fi

mode_value() {
  if { [ "$MODE" = "recover-mismatch" ] || [ "$MODE" = "recover-wrong-login" ]; } && [ -n "$STATE_FILE" ] && [ -f "$STATE_FILE" ]; then
    cat "$STATE_FILE"
    return 0
  fi
  printf '%s\n' "$MODE"
}

case "${1:-}" in
  verify)
    exit 1
    ;;
  status)
    if [ "$MODE" = "verify-fails-running" ] || { { [ "$MODE" = "recover-mismatch" ] || [ "$MODE" = "recover-wrong-login" ]; } && [ "$(mode_value)" != "stopped" ]; }; then
      cat <<OUT
runtime: running
mode: gui
url: https://foxcode.rjj.cc/api-keys
profile_dir: /tmp/profile
run_dir: /tmp/run
cdp_port: 19222
browser_pid: 12345
xvfb_pid: 67890
display: :88
OUT
    else
      cat <<OUT
runtime: stopped
mode: gui
url: https://foxcode.rjj.cc/api-keys
profile_dir: /tmp/profile
run_dir: /tmp/run
cdp_port: 19222
browser_pid:
xvfb_pid:
display: :88
OUT
    fi
    ;;
  start)
    if [ "$MODE" = "verify-fails-running" ]; then
      echo "[browser-runtime] ERROR: browser runtime already running; use stop or status first" >&2
      exit 1
    fi
    if { [ "$MODE" = "recover-mismatch" ] || [ "$MODE" = "recover-wrong-login" ]; } && [ -n "$STATE_FILE" ]; then
      printf '%s\n' "recovered" >"$STATE_FILE"
    fi
    echo "runtime started"
    ;;
  stop)
    if { [ "$MODE" = "recover-mismatch" ] || [ "$MODE" = "recover-wrong-login" ]; } && [ -n "$STATE_FILE" ]; then
      printf '%s\n' "stopped" >"$STATE_FILE"
    fi
    echo "runtime stopped"
    ;;
  list-targets)
    if [ "$MODE" = "recover-mismatch" ] && [ "$(mode_value)" = "recovered" ]; then
      echo '[{"id":"page-foxcode","type":"page","url":"https://foxcode.rjj.cc/api-keys"}]'
    else
      echo '[{"id":"page-foxcode","type":"page","url":"https://foxcode.rjj.cc/api-keys"}]'
    fi
    ;;
  select-target)
    echo "page-foxcode"
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
      case "$(mode_value):$check" in
        ready:challenge|login-wall:challenge)
          echo '{"hasChallenge":false}'
          ;;
        transient-login:challenge)
          echo '{"hasChallenge":false}'
          ;;
        recover-mismatch:challenge)
          echo '{"hasChallenge":false}'
          ;;
        recover-wrong-login:challenge)
          echo '{"hasChallenge":false}'
          ;;
        ready:login-wall)
          echo '{"hasLoginWall":false}'
          ;;
        login-wall:login-wall)
          echo '{"hasLoginWall":true}'
          ;;
        transient-login:login-wall)
          if [ -n "$STATE_FILE" ]; then
            count=0
            if [ -f "$STATE_FILE" ]; then
              count="$(cat "$STATE_FILE")"
            fi
            count=$((count + 1))
            printf '%s\n' "$count" >"$STATE_FILE"
            if [ "$count" -ge 2 ]; then
              echo '{"hasLoginWall":true}'
            else
              echo '{"hasLoginWall":false}'
            fi
          else
            echo '{"hasLoginWall":false}'
          fi
          ;;
        recover-mismatch:login-wall)
          echo '{"hasLoginWall":false}'
          ;;
        recover-wrong-login:login-wall)
          if [ "$(mode_value)" = "recovered" ]; then
            echo '{"hasLoginWall":false}'
          else
            echo '{"hasLoginWall":true}'
          fi
          ;;
        *:page-info)
        if [ "$MODE" = "transient-login" ] && [ -n "$STATE_FILE" ] && [ -f "$STATE_FILE" ] && [ "$(cat "$STATE_FILE")" -lt 2 ]; then
          echo '{"title":"","url":"about:blank","bodySnippet":""}'
        elif [ "$(mode_value)" = "wrong-page" ] || [ "$(mode_value)" = "recover-mismatch" ]; then
          echo '{"title":"Google Account","url":"https://myaccount.google.com/","bodySnippet":"signed in"}'
        elif [ "$(mode_value)" = "same-origin-wrong-page" ]; then
          echo '{"title":"Foxcode Settings","url":"https://foxcode.rjj.cc/settings","bodySnippet":"settings"}'
        elif [ "$(mode_value)" = "recover-wrong-login" ]; then
          if [ -n "$STATE_FILE" ] && [ -f "$STATE_FILE" ] && [ "$(cat "$STATE_FILE")" = "recovered" ]; then
            echo '{"title":"API密钥管理 - NEW CLI","url":"https://foxcode.rjj.cc/api-keys","bodySnippet":"余额基数"}'
          else
            echo '{"title":"Sign in to GitHub · GitHub","url":"https://github.com/login?return_to=https%3A%2F%2Fgithub.com%2Fsettings%2Fprofile","bodySnippet":"Sign in to GitHub"}'
          fi
        else
          echo '{"title":"API密钥管理 - NEW CLI","url":"https://foxcode.rjj.cc/api-keys","bodySnippet":"余额基数"}'
        fi
        ;;
      *)
        echo '{"hasChallenge":false,"hasLoginWall":false}'
        ;;
    esac
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

printf '%s\n' "$*" >>"${ASSISTED_STUB_LOG:?}"
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
lan_novnc_url: http://192.168.0.200:6081/vnc.html?autoconnect=1&resize=remote
OUT
    ;;
  *)
    echo "unexpected assisted command: $1" >&2
    exit 1
    ;;
esac
EOF

chmod +x "$TMP_DIR/browser-runtime-stub.sh" "$TMP_DIR/assisted-stub.sh"

cat >"$TMP_DIR/profile-resolution-stub.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

printf '%s\n' "$*" >>"${PROFILE_STUB_LOG:?}"
case "${1:-}" in
  resolve)
    if [ "${PROFILE_STUB_MODE:-ok}" = "ambiguous" ]; then
      exit 2
    fi
    printf '{"profile_dir":"%s","source":"identity-index"}\n' "${PROFILE_STUB_PROFILE_DIR:?}"
    ;;
  *)
    echo "unexpected profile command: $1" >&2
    exit 1
    ;;
esac
EOF
chmod +x "$TMP_DIR/profile-resolution-stub.sh"

ready_output="$(
  AGENT_BROWSER_RUNTIME_HELPER="$TMP_DIR/browser-runtime-stub.sh" \
  AGENT_BROWSER_ASSISTED_HELPER="$TMP_DIR/assisted-stub.sh" \
  AGENT_BROWSER_PROFILE_HELPER="$TMP_DIR/profile-resolution-stub.sh" \
  ASSISTED_STUB_LOG="$TMP_DIR/assisted.log" \
  PROFILE_STUB_LOG="$TMP_DIR/profile.log" \
  PROFILE_STUB_PROFILE_DIR="/tmp/resolved-profile" \
  RUNTIME_STUB_LOG_FILE="$TMP_DIR/runtime.log" \
  "$BASE_DIR/open-protected-page.sh" \
    --url 'https://foxcode.rjj.cc/api-keys' \
    --origin 'https://foxcode.rjj.cc' \
    --session-key foxcode-main
)"
printf '%s\n' "$ready_output" | grep -q '"status": "ready"'
printf '%s\n' "$ready_output" | grep -q '"targetId": "page-foxcode"'
if [ -f "$TMP_DIR/assisted.log" ]; then
  echo "assisted flow should not start for ready pages"
  exit 1
fi

login_output="$(
  RUNTIME_STUB_MODE="login-wall" \
  AGENT_BROWSER_RUNTIME_HELPER="$TMP_DIR/browser-runtime-stub.sh" \
  AGENT_BROWSER_ASSISTED_HELPER="$TMP_DIR/assisted-stub.sh" \
  AGENT_BROWSER_PROFILE_HELPER="$TMP_DIR/profile-resolution-stub.sh" \
  ASSISTED_STUB_LOG="$TMP_DIR/assisted.log" \
  PROFILE_STUB_LOG="$TMP_DIR/profile.log" \
  PROFILE_STUB_PROFILE_DIR="/tmp/resolved-profile" \
  RUNTIME_STUB_LOG_FILE="$TMP_DIR/runtime.log" \
  "$BASE_DIR/open-protected-page.sh" \
    --url 'https://foxcode.rjj.cc/api-keys' \
    --origin 'https://foxcode.rjj.cc' \
    --session-key foxcode-main
)"
printf '%s\n' "$login_output" | grep -q '"status": "needs-user"'
printf '%s\n' "$login_output" | grep -q 'http://127.0.0.1:6081/vnc.html'
printf '%s\n' "$login_output" | grep -q '"lanNovncUrl": "http://192.168.0.200:6081/vnc.html?autoconnect=1&resize=remote"'
grep -q '^start ' "$TMP_DIR/assisted.log"

rm -f "$TMP_DIR/assisted.log" "$TMP_DIR/runtime-state"
transient_output="$(
  RUNTIME_STUB_MODE="transient-login" \
  RUNTIME_STUB_STATE_FILE="$TMP_DIR/runtime-state" \
  AGENT_BROWSER_RUNTIME_HELPER="$TMP_DIR/browser-runtime-stub.sh" \
  AGENT_BROWSER_ASSISTED_HELPER="$TMP_DIR/assisted-stub.sh" \
  AGENT_BROWSER_PROFILE_HELPER="$TMP_DIR/profile-resolution-stub.sh" \
  ASSISTED_STUB_LOG="$TMP_DIR/assisted.log" \
  PROFILE_STUB_LOG="$TMP_DIR/profile.log" \
  PROFILE_STUB_PROFILE_DIR="/tmp/resolved-profile" \
  RUNTIME_STUB_LOG_FILE="$TMP_DIR/runtime.log" \
  "$BASE_DIR/open-protected-page.sh" \
    --url 'https://foxcode.rjj.cc/api-keys' \
    --origin 'https://foxcode.rjj.cc' \
    --session-key foxcode-main
)"
printf '%s\n' "$transient_output" | grep -q '"status": "needs-user"'
printf '%s\n' "$transient_output" | grep -q '"reason": "login-wall"'

wrong_page_output="$(
  RUNTIME_STUB_MODE="wrong-page" \
  AGENT_BROWSER_RUNTIME_HELPER="$TMP_DIR/browser-runtime-stub.sh" \
  AGENT_BROWSER_ASSISTED_HELPER="$TMP_DIR/assisted-stub.sh" \
  AGENT_BROWSER_PROFILE_HELPER="$TMP_DIR/profile-resolution-stub.sh" \
  ASSISTED_STUB_LOG="$TMP_DIR/assisted.log" \
  PROFILE_STUB_LOG="$TMP_DIR/profile.log" \
  PROFILE_STUB_PROFILE_DIR="/tmp/resolved-profile" \
  RUNTIME_STUB_LOG_FILE="$TMP_DIR/runtime.log" \
  "$BASE_DIR/open-protected-page.sh" \
    --url 'https://foxcode.rjj.cc/api-keys' \
    --origin 'https://foxcode.rjj.cc' \
    --session-key foxcode-main
)"
printf '%s\n' "$wrong_page_output" | grep -q '"status": "needs-user"'

same_origin_wrong_page_output="$(
  RUNTIME_STUB_MODE="same-origin-wrong-page" \
  AGENT_BROWSER_RUNTIME_HELPER="$TMP_DIR/browser-runtime-stub.sh" \
  AGENT_BROWSER_ASSISTED_HELPER="$TMP_DIR/assisted-stub.sh" \
  AGENT_BROWSER_PROFILE_HELPER="$TMP_DIR/profile-resolution-stub.sh" \
  ASSISTED_STUB_LOG="$TMP_DIR/assisted.log" \
  PROFILE_STUB_LOG="$TMP_DIR/profile.log" \
  PROFILE_STUB_PROFILE_DIR="/tmp/resolved-profile" \
  RUNTIME_STUB_LOG_FILE="$TMP_DIR/runtime.log" \
  "$BASE_DIR/open-protected-page.sh" \
    --url 'https://foxcode.rjj.cc/api-keys' \
    --origin 'https://foxcode.rjj.cc' \
    --session-key foxcode-main
)"
printf '%s\n' "$same_origin_wrong_page_output" | grep -q '"status": "needs-user"'
printf '%s\n' "$same_origin_wrong_page_output" | grep -q '"reason": "target-mismatch"'

recover_output="$(
  RUNTIME_STUB_MODE="recover-mismatch" \
  RUNTIME_STUB_STATE_FILE="$TMP_DIR/recover-state" \
  AGENT_BROWSER_RUNTIME_HELPER="$TMP_DIR/browser-runtime-stub.sh" \
  AGENT_BROWSER_ASSISTED_HELPER="$TMP_DIR/assisted-stub.sh" \
  AGENT_BROWSER_PROFILE_HELPER="$TMP_DIR/profile-resolution-stub.sh" \
  ASSISTED_STUB_LOG="$TMP_DIR/assisted.log" \
  PROFILE_STUB_LOG="$TMP_DIR/profile.log" \
  PROFILE_STUB_PROFILE_DIR="/tmp/resolved-profile" \
  RUNTIME_STUB_LOG_FILE="$TMP_DIR/runtime.log" \
  "$BASE_DIR/open-protected-page.sh" \
    --url 'https://foxcode.rjj.cc/api-keys' \
    --origin 'https://foxcode.rjj.cc' \
    --session-key foxcode-main
)"
printf '%s\n' "$recover_output" | grep -q '"status": "ready"'
grep -q '^stop --origin https://foxcode.rjj.cc --session-key foxcode-main$' "$TMP_DIR/runtime.log"

recover_login_output="$(
  RUNTIME_STUB_MODE="recover-wrong-login" \
  RUNTIME_STUB_STATE_FILE="$TMP_DIR/recover-login-state" \
  AGENT_BROWSER_RUNTIME_HELPER="$TMP_DIR/browser-runtime-stub.sh" \
  AGENT_BROWSER_ASSISTED_HELPER="$TMP_DIR/assisted-stub.sh" \
  AGENT_BROWSER_PROFILE_HELPER="$TMP_DIR/profile-resolution-stub.sh" \
  ASSISTED_STUB_LOG="$TMP_DIR/assisted.log" \
  PROFILE_STUB_LOG="$TMP_DIR/profile.log" \
  PROFILE_STUB_PROFILE_DIR="/tmp/resolved-profile" \
  RUNTIME_STUB_LOG_FILE="$TMP_DIR/runtime.log" \
  "$BASE_DIR/open-protected-page.sh" \
    --url 'https://foxcode.rjj.cc/api-keys' \
    --origin 'https://foxcode.rjj.cc' \
    --session-key foxcode-main
)"
printf '%s\n' "$recover_login_output" | grep -q '"status": "ready"'

running_output="$(
  RUNTIME_STUB_MODE="verify-fails-running" \
  AGENT_BROWSER_RUNTIME_HELPER="$TMP_DIR/browser-runtime-stub.sh" \
  AGENT_BROWSER_ASSISTED_HELPER="$TMP_DIR/assisted-stub.sh" \
  AGENT_BROWSER_PROFILE_HELPER="$TMP_DIR/profile-resolution-stub.sh" \
  ASSISTED_STUB_LOG="$TMP_DIR/assisted.log" \
  PROFILE_STUB_LOG="$TMP_DIR/profile.log" \
  PROFILE_STUB_PROFILE_DIR="/tmp/resolved-profile" \
  RUNTIME_STUB_LOG_FILE="$TMP_DIR/runtime.log" \
  "$BASE_DIR/open-protected-page.sh" \
    --url 'https://foxcode.rjj.cc/api-keys' \
    --origin 'https://foxcode.rjj.cc' \
    --session-key foxcode-main
)"
printf '%s\n' "$running_output" | grep -q '"status": "ready"'

grep -q '^resolve ' "$TMP_DIR/profile.log"
grep -q '^start --url https://foxcode.rjj.cc/api-keys --origin https://foxcode.rjj.cc --session-key foxcode-main --profile-dir /tmp/resolved-profile --mode gui$' "$TMP_DIR/runtime.log"

mkdir -p "$TMP_DIR/home/.agent-browser/profiles/foxcode.rjj.cc/Default"
mkdir -p "$TMP_DIR/home/.agent-browser/profiles/https___foxcode_rjj_cc/foxcode-main/Default"
touch "$TMP_DIR/home/.agent-browser/profiles/foxcode.rjj.cc/Default/Cookies"
touch "$TMP_DIR/home/.agent-browser/profiles/https___foxcode_rjj_cc/foxcode-main/Default/Login Data"
ambiguous_output="$(
  HOME="$TMP_DIR/home" \
  AGENT_BROWSER_RUNTIME_HELPER="$TMP_DIR/browser-runtime-stub.sh" \
  AGENT_BROWSER_ASSISTED_HELPER="$TMP_DIR/assisted-stub.sh" \
  ASSISTED_STUB_LOG="$TMP_DIR/assisted.log" \
  RUNTIME_STUB_LOG_FILE="$TMP_DIR/runtime.log" \
  "$BASE_DIR/open-protected-page.sh" \
    --url 'https://foxcode.rjj.cc/api-keys' \
    --origin 'https://foxcode.rjj.cc' \
    --session-key foxcode-main
)"
printf '%s\n' "$ambiguous_output" | grep -q '"reason": "ambiguous-profile"'
