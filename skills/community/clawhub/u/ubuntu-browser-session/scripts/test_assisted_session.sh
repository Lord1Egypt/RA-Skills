#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
mkdir -p "$TMP_DIR/home"
export HOME="$TMP_DIR/home"

cat >"$TMP_DIR/runtime-stub.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

STATE_DIR="${RUNTIME_STUB_DIR:?}"
TARGETS_JSON="${RUNTIME_STUB_TARGETS_JSON:-}"
PAGE_URL="${RUNTIME_STUB_PAGE_URL:-https://example.com}"
PAGE_TITLE="${RUNTIME_STUB_PAGE_TITLE:-Example}"
PAGE_BODY="${RUNTIME_STUB_PAGE_BODY:-hello}"
LOG_FILE="${RUNTIME_STUB_LOG_FILE:-}"
if [ -z "$TARGETS_JSON" ]; then
  TARGETS_JSON='[{"id":"page-1","type":"page","url":"https://example.com"}]'
fi
command="${1:-}"
shift || true

if [ -n "$LOG_FILE" ]; then
  printf '%s %s\n' "$command" "$*" >>"$LOG_FILE"
fi

case "$command" in
  start)
    touch "$STATE_DIR/running"
    cat <<OUT
runtime: running
mode: gui
url: https://example.com
profile_dir: $STATE_DIR/profile
run_dir: $STATE_DIR/run
cdp_port: 19222
browser_pid: $$
xvfb_pid: 4242
display: :88
OUT
    ;;
  status)
    if [ -f "$STATE_DIR/running" ]; then
      cat <<OUT
runtime: running
mode: gui
url: https://example.com
profile_dir: $STATE_DIR/profile
run_dir: $STATE_DIR/run
cdp_port: 19222
browser_pid: $$
xvfb_pid: 4242
display: :88
OUT
    else
      cat <<OUT
runtime: stopped
mode: gui
url: https://example.com
profile_dir: $STATE_DIR/profile
run_dir: $STATE_DIR/run
cdp_port: 19222
browser_pid:
xvfb_pid:
display: :88
OUT
    fi
    ;;
  list-targets)
    if [ -f "$STATE_DIR/running" ]; then
      printf '%s\n' "$TARGETS_JSON"
    else
      echo '[]'
    fi
    ;;
  select-target)
    python3 - "$TARGETS_JSON" "$@" <<'PY'
import json
import sys
from urllib.parse import urlparse

targets_json = sys.argv[1]
args = sys.argv[2:]
origin = ""
target_url = ""
while args:
    key = args.pop(0)
    if key == "--origin":
        origin = args.pop(0)
    elif key == "--target-url":
        target_url = args.pop(0)
    elif key == "--targets-json":
        targets_json = args.pop(0)

targets = [target for target in json.loads(targets_json) if target.get("type") == "page"]

def host(value):
    parsed = urlparse(value)
    return parsed.netloc

def score(target):
    url = target.get("url", "")
    if target_url and url == target_url:
        return (0, url)
    if origin and url.startswith(origin):
        return (1, url)
    if origin and host(url) and host(url) == host(origin):
        return (2, url)
    return (9, url)

if targets:
    print(sorted(targets, key=score)[0].get("id", ""))
PY
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
    if [ ! -f "$STATE_DIR/verified" ]; then
      if [ "$check" = "challenge" ]; then
        echo '{"hasChallenge": true, "indicators": ["turnstile"], "title": "Verify you are human", "url": "https://example.com"}'
      elif [ "$check" = "login-wall" ]; then
        echo '{"hasLoginWall": true, "loginHits": ["Sign in"], "title": "Sign in", "url": "https://example.com/login"}'
      else
        printf '{"title": "Verify you are human", "url": "%s", "bodySnippet": "challenge"}\n' "$PAGE_URL"
      fi
    else
      if [ "$check" = "challenge" ]; then
        echo '{"hasChallenge": false, "indicators": [], "title": "Dashboard", "url": "https://example.com"}'
      elif [ "$check" = "login-wall" ]; then
        echo '{"hasLoginWall": false, "loginHits": [], "title": "Dashboard", "url": "https://example.com"}'
      else
        printf '{"title": "%s", "url": "%s", "bodySnippet": "%s"}\n' "$PAGE_TITLE" "$PAGE_URL" "$PAGE_BODY"
      fi
    fi
    ;;
  stop)
    rm -f "$STATE_DIR/running" "$STATE_DIR/verified"
    ;;
  *)
    echo "unknown command: $command" >&2
    exit 1
    ;;
esac
EOF
chmod +x "$TMP_DIR/runtime-stub.sh"

cat >"$TMP_DIR/profile-resolution-stub.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

case "${1:-}" in
  resolve)
    printf '%s\n' "$*" >>"${PROFILE_STUB_LOG:?}"
    if [ "${PROFILE_STUB_MODE:-ok}" = "ambiguous" ]; then
      exit 2
    fi
    printf '{"profile_dir":"%s","source":"site-registry"}\n' "${PROFILE_STUB_RESOLVED_PROFILE_DIR:?}"
    ;;
  write-identity)
    provider=""
    profile_dir=""
    source_origin=""
    source_session_key=""
    while [ "$#" -gt 0 ]; do
      case "$1" in
        --provider)
          provider="$2"
          shift 2
          ;;
        --profile-dir)
          profile_dir="$2"
          shift 2
          ;;
        --source-origin)
          source_origin="$2"
          shift 2
          ;;
        --source-session-key)
          source_session_key="$2"
          shift 2
          ;;
        *)
          shift
          ;;
      esac
    done
    python3 - "${PROFILE_STUB_IDENTITY_FILE:?}" "$provider" "$profile_dir" "$source_origin" "$source_session_key" <<'PY'
import json
import os
import sys

path, provider, profile_dir, source_origin, source_session_key = sys.argv[1:]
payload = {"providers": {}}
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
providers = payload.setdefault("providers", {})
providers[provider] = {
    "profile_dir": profile_dir,
    "source_origin": source_origin,
    "source_session_key": source_session_key,
}
with open(path, "w", encoding="utf-8") as handle:
    json.dump(payload, handle, indent=2, sort_keys=True)
    handle.write("\n")
PY
    ;;
  *)
    echo "unexpected profile command: $1" >&2
    exit 1
    ;;
esac
EOF
chmod +x "$TMP_DIR/profile-resolution-stub.sh"

mkdir -p "$TMP_DIR/runtime"
RUNTIME_STUB_DIR="$TMP_DIR/runtime" AGENT_BROWSER_RUNTIME_HELPER="$TMP_DIR/runtime-stub.sh" \
  AGENT_BROWSER_SELECT_TARGET_HELPER="$TMP_DIR/runtime-stub.sh" \
  "$BASE_DIR/assisted-session.sh" status --run-dir "$TMP_DIR" >/dev/null

PROFILE_STUB_LOG="$TMP_DIR/profile.log" \
PROFILE_STUB_RESOLVED_PROFILE_DIR="$TMP_DIR/resolved-profile" \
RUNTIME_STUB_DIR="$TMP_DIR/runtime" \
RUNTIME_STUB_LOG_FILE="$TMP_DIR/runtime.log" \
AGENT_BROWSER_RUNTIME_HELPER="$TMP_DIR/runtime-stub.sh" \
AGENT_BROWSER_SELECT_TARGET_HELPER="$TMP_DIR/runtime-stub.sh" \
AGENT_BROWSER_PROFILE_HELPER="$TMP_DIR/profile-resolution-stub.sh" \
  "$BASE_DIR/assisted-session.sh" start \
    --run-dir "$TMP_DIR/direct-assist" \
    --manifest-root "$TMP_DIR/direct-manifests" \
    --url "https://github.com/settings/profile" \
    --origin "https://github.com" \
    --session-key default >/dev/null
grep -q '^resolve --root '"$TMP_DIR"'/home/.agent-browser --manifest-root '"$TMP_DIR"'/direct-manifests --origin https://github.com --session-key default$' "$TMP_DIR/profile.log"
grep -q '^start --run-dir '"$TMP_DIR"'/home/.agent-browser/run/https___github_com/default --url https://github.com/settings/profile --origin https://github.com --session-key default --mode gui --profile-dir '"$TMP_DIR"'/resolved-profile$' "$TMP_DIR/runtime.log"

assist_status="$(
  RUNTIME_STUB_DIR="$TMP_DIR/runtime" \
  AGENT_BROWSER_RUNTIME_HELPER="$TMP_DIR/runtime-stub.sh" \
  AGENT_BROWSER_SELECT_TARGET_HELPER="$TMP_DIR/runtime-stub.sh" \
  "$BASE_DIR/assisted-session.sh" status \
    --url "https://foxcode.rjj.cc/api-keys" \
    --origin "https://foxcode.rjj.cc" \
    --session-key "foxcode-main"
)"
printf '%s\n' "$assist_status" | grep -q "run_dir: $TMP_DIR/home/.agent-browser/assist/https___foxcode_rjj_cc/foxcode-main"

if RUNTIME_STUB_DIR="$TMP_DIR/runtime" AGENT_BROWSER_RUNTIME_HELPER="$TMP_DIR/runtime-stub.sh" \
  AGENT_BROWSER_SELECT_TARGET_HELPER="$TMP_DIR/runtime-stub.sh" \
  "$BASE_DIR/assisted-session.sh" capture --run-dir "$TMP_DIR" --manifest-root "$TMP_DIR/manifests" --origin "https://example.com" >/dev/null 2>&1; then
  echo "expected capture without a verified browser to fail"
  exit 1
fi

mkdir -p "$TMP_DIR/runtime"
touch "$TMP_DIR/runtime/running" "$TMP_DIR/runtime/verified"
RUNTIME_STUB_DIR="$TMP_DIR/runtime" AGENT_BROWSER_RUNTIME_HELPER="$TMP_DIR/runtime-stub.sh" \
  AGENT_BROWSER_SELECT_TARGET_HELPER="$TMP_DIR/runtime-stub.sh" \
  "$BASE_DIR/assisted-session.sh" capture --run-dir "$TMP_DIR" --manifest-root "$TMP_DIR/manifests" --origin "https://example.com" --block-reason login-wall >/dev/null
"$BASE_DIR/session-manifest.sh" show --root "$TMP_DIR/manifests" --origin "https://example.com" --session-key default | grep -q '"block_reason": "login-wall"'

RUNTIME_STUB_TARGETS_JSON='[
  {"id":"page-login","type":"page","url":"https://example.com/login"},
  {"id":"page-foxcode","type":"page","url":"https://foxcode.rjj.cc/api-keys"},
  {"id":"page-other","type":"page","url":"https://news.ycombinator.com"}
]' \
RUNTIME_STUB_PAGE_URL='https://foxcode.rjj.cc/api-keys' \
RUNTIME_STUB_PAGE_TITLE='Foxcode API Keys' \
RUNTIME_STUB_PAGE_BODY='keys' \
RUNTIME_STUB_DIR="$TMP_DIR/runtime" AGENT_BROWSER_RUNTIME_HELPER="$TMP_DIR/runtime-stub.sh" \
  AGENT_BROWSER_SELECT_TARGET_HELPER="$TMP_DIR/runtime-stub.sh" \
  "$BASE_DIR/assisted-session.sh" capture --run-dir "$TMP_DIR" --manifest-root "$TMP_DIR/fox-manifests" --origin "https://foxcode.rjj.cc" >/dev/null
"$BASE_DIR/session-manifest.sh" show --root "$TMP_DIR/fox-manifests" --origin "https://foxcode.rjj.cc" --session-key default | grep -q '"target_id": "page-foxcode"'

PROFILE_STUB_IDENTITY_FILE="$TMP_DIR/identity-profiles.json" \
RUNTIME_STUB_TARGETS_JSON='[
  {"id":"page-github","type":"page","url":"https://github.com/settings/profile"}
]' \
RUNTIME_STUB_PAGE_URL='https://github.com/settings/profile' \
RUNTIME_STUB_PAGE_TITLE='GitHub Settings' \
RUNTIME_STUB_PAGE_BODY='settings' \
RUNTIME_STUB_DIR="$TMP_DIR/runtime" \
AGENT_BROWSER_RUNTIME_HELPER="$TMP_DIR/runtime-stub.sh" \
AGENT_BROWSER_SELECT_TARGET_HELPER="$TMP_DIR/runtime-stub.sh" \
AGENT_BROWSER_PROFILE_HELPER="$TMP_DIR/profile-resolution-stub.sh" \
  "$BASE_DIR/assisted-session.sh" capture --run-dir "$TMP_DIR" --manifest-root "$TMP_DIR/github-manifests" --origin "https://github.com" >/dev/null
grep -q '"github.com"' "$TMP_DIR/identity-profiles.json"
grep -q '"profile_dir": "'"$TMP_DIR"'/runtime/profile"' "$TMP_DIR/identity-profiles.json"
"$BASE_DIR/site-session-registry.sh" resolve --root "$TMP_DIR/home/.agent-browser" --site github.com --session-key default | grep -q '"profile_dir": "'"$TMP_DIR"'/runtime/profile"'

cat >"$TMP_DIR/identity-profiles.json" <<EOF
{
  "providers": {
    "github.com": {
      "profile_dir": "/stale/profile",
      "source_origin": "https://old.example",
      "source_session_key": "old"
    }
  }
}
EOF
PROFILE_STUB_IDENTITY_FILE="$TMP_DIR/identity-profiles.json" \
RUNTIME_STUB_TARGETS_JSON='[
  {"id":"page-github","type":"page","url":"https://github.com/settings/profile"}
]' \
RUNTIME_STUB_PAGE_URL='https://github.com/settings/profile' \
RUNTIME_STUB_PAGE_TITLE='GitHub Settings' \
RUNTIME_STUB_PAGE_BODY='settings' \
RUNTIME_STUB_DIR="$TMP_DIR/runtime" \
AGENT_BROWSER_RUNTIME_HELPER="$TMP_DIR/runtime-stub.sh" \
AGENT_BROWSER_SELECT_TARGET_HELPER="$TMP_DIR/runtime-stub.sh" \
AGENT_BROWSER_PROFILE_HELPER="$TMP_DIR/profile-resolution-stub.sh" \
  "$BASE_DIR/assisted-session.sh" capture --run-dir "$TMP_DIR" --manifest-root "$TMP_DIR/github-manifests" --origin "https://github.com" --session-key updated >/dev/null
grep -q '"source_session_key": "updated"' "$TMP_DIR/identity-profiles.json"

rm -f "$TMP_DIR/identity-profiles.json" "$TMP_DIR/runtime/verified"
if PROFILE_STUB_IDENTITY_FILE="$TMP_DIR/identity-profiles.json" \
  RUNTIME_STUB_DIR="$TMP_DIR/runtime" \
  AGENT_BROWSER_RUNTIME_HELPER="$TMP_DIR/runtime-stub.sh" \
  AGENT_BROWSER_SELECT_TARGET_HELPER="$TMP_DIR/runtime-stub.sh" \
  AGENT_BROWSER_PROFILE_HELPER="$TMP_DIR/profile-resolution-stub.sh" \
  "$BASE_DIR/assisted-session.sh" capture --run-dir "$TMP_DIR" --manifest-root "$TMP_DIR/github-manifests" --origin "https://github.com" >/dev/null 2>&1; then
  echo "expected capture with login wall to fail before writing identity metadata"
  exit 1
fi
test ! -f "$TMP_DIR/identity-profiles.json"
touch "$TMP_DIR/runtime/verified"

if RUNTIME_STUB_TARGETS_JSON='[
  {"id":"page-google","type":"page","url":"https://myaccount.google.com/"}
]' \
  RUNTIME_STUB_PAGE_URL='https://myaccount.google.com/' \
  RUNTIME_STUB_PAGE_TITLE='Google Account' \
  RUNTIME_STUB_PAGE_BODY='signed in' \
  RUNTIME_STUB_DIR="$TMP_DIR/runtime" \
  AGENT_BROWSER_RUNTIME_HELPER="$TMP_DIR/runtime-stub.sh" \
  AGENT_BROWSER_SELECT_TARGET_HELPER="$TMP_DIR/runtime-stub.sh" \
  "$BASE_DIR/assisted-session.sh" capture --run-dir "$TMP_DIR" --manifest-root "$TMP_DIR/drift-manifests" --origin "https://github.com" >/dev/null 2>&1; then
  echo "expected capture on an off-origin page to fail"
  exit 1
fi
if "$BASE_DIR/site-session-registry.sh" resolve --root "$TMP_DIR/home/.agent-browser" --site google.com --session-key default >/dev/null 2>&1; then
  echo "capture should not register an off-origin site session"
  exit 1
fi

mkdir -p "$TMP_DIR/override-run"
cat >"$TMP_DIR/override-run/assist.env" <<EOF
URL=https://example.com
RUN_DIR=$TMP_DIR/override-run
MANIFEST_ROOT=$TMP_DIR/wrong-root
NOVNC_PORT=6080
VNC_PORT=5900
PROFILE_DIR=$TMP_DIR/runtime/profile
EOF
RUNTIME_STUB_DIR="$TMP_DIR/runtime" AGENT_BROWSER_RUNTIME_HELPER="$TMP_DIR/runtime-stub.sh" \
  AGENT_BROWSER_SELECT_TARGET_HELPER="$TMP_DIR/runtime-stub.sh" \
  RUNTIME_STUB_PAGE_URL='https://override.example.com' \
  RUNTIME_STUB_PAGE_TITLE='Override Example' \
  RUNTIME_STUB_PAGE_BODY='override' \
  "$BASE_DIR/assisted-session.sh" capture --run-dir "$TMP_DIR/override-run" --manifest-root "$TMP_DIR/override-manifests" --origin "https://override.example.com" --session-key override-check >/dev/null
"$BASE_DIR/session-manifest.sh" show --root "$TMP_DIR/override-manifests" --origin "https://override.example.com" --session-key override-check | grep -q '"session_key": "override-check"'

RUNTIME_STUB_TARGETS_JSON='[
  {"id":"page-github","type":"page","url":"https://github.com/settings/profile"}
]' \
RUNTIME_STUB_PAGE_URL='https://github.com/settings/profile' \
RUNTIME_STUB_PAGE_TITLE='GitHub Settings' \
RUNTIME_STUB_PAGE_BODY='settings' \
RUNTIME_STUB_DIR="$TMP_DIR/runtime" \
AGENT_BROWSER_RUNTIME_HELPER="$TMP_DIR/runtime-stub.sh" \
AGENT_BROWSER_SELECT_TARGET_HELPER="$TMP_DIR/runtime-stub.sh" \
  "$BASE_DIR/assisted-session.sh" capture --run-dir "$TMP_DIR/override-run" --manifest-root "$TMP_DIR/override-manifests" --origin "https://github.com" --session-key root-check >/dev/null
test -f "$TMP_DIR/home/.agent-browser/index/identity-profiles.json"
test ! -f "$TMP_DIR/override-manifests/index/identity-profiles.json"
"$BASE_DIR/site-session-registry.sh" resolve --root "$TMP_DIR/home/.agent-browser" --site github.com --session-key root-check | grep -q '"session_key": "root-check"'

mkdir -p "$TMP_DIR/bin" "$TMP_DIR/runtime" "$TMP_DIR/novnc"
cat >"$TMP_DIR/bin/x11vnc" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' "$*" >"${ASSIST_STUB_STATE_DIR:?}/x11vnc.args"
sleep 30
EOF
cat >"$TMP_DIR/bin/websockify" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' "$*" >"${ASSIST_STUB_STATE_DIR:?}/websockify.args"
sleep 30
EOF
chmod +x "$TMP_DIR/bin/x11vnc" "$TMP_DIR/bin/websockify"

python3 -m http.server 5900 --bind 127.0.0.1 >/dev/null 2>&1 &
PORT_A_PID=$!
python3 -m http.server 6080 --bind 127.0.0.1 >/dev/null 2>&1 &
PORT_B_PID=$!
trap 'kill "$PORT_A_PID" "$PORT_B_PID" 2>/dev/null || true; rm -rf "$TMP_DIR"' EXIT

ASSIST_STUB_STATE_DIR="$TMP_DIR" \
AGENT_BROWSER_NOVNC_WEB_ROOT="$TMP_DIR/novnc" \
PATH="$TMP_DIR/bin:$PATH" \
RUNTIME_STUB_DIR="$TMP_DIR/runtime" \
AGENT_BROWSER_RUNTIME_HELPER="$TMP_DIR/runtime-stub.sh" \
AGENT_BROWSER_SELECT_TARGET_HELPER="$TMP_DIR/runtime-stub.sh" \
  "$BASE_DIR/assisted-session.sh" start --run-dir "$TMP_DIR/assist-run" --url "https://foxcode.rjj.cc/api-keys" >/dev/null

grep -Eq '(^| )-rfbport (590[1-9]|59[1-9][0-9]|6[0-9]{3,})( |$)' "$TMP_DIR/x11vnc.args"
grep -Eq '0.0.0.0:(608[1-9]|60[89][0-9]|6[1-9][0-9]{2,})' "$TMP_DIR/websockify.args"
"$BASE_DIR/assisted-session.sh" stop --run-dir "$TMP_DIR/assist-run" >/dev/null
