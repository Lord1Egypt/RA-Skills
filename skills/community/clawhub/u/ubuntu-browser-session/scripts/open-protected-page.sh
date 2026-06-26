#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/runtime-common.sh"

usage() {
  cat <<'EOF'
Usage:
  open-protected-page.sh --url URL [options]

Options:
  --manifest-root DIR
  --origin URL
  --session-key KEY
  --url URL
EOF
}

die() {
  printf '[open-protected-page] ERROR: %s\n' "$*" >&2
  exit 1
}

require_arg() {
  local name="$1"
  local value="$2"
  [ -n "$value" ] || die "missing required argument: $name"
}

manifest_helper() {
  "${AGENT_BROWSER_MANIFEST_HELPER:-$SCRIPT_DIR/session-manifest.sh}" "$@"
}

runtime_helper() {
  "${AGENT_BROWSER_RUNTIME_HELPER:-$SCRIPT_DIR/browser-runtime.sh}" "$@"
}

assisted_helper() {
  "${AGENT_BROWSER_ASSISTED_HELPER:-$SCRIPT_DIR/assisted-session.sh}" "$@"
}

profile_helper() {
  "${AGENT_BROWSER_PROFILE_HELPER:-$SCRIPT_DIR/profile-resolution.sh}" "$@"
}

manifest_field() {
  local field="$1"
  local payload="$2"
  python3 - "$field" "$payload" <<'PY'
import json
import sys

payload = json.loads(sys.argv[2])
value = payload.get(sys.argv[1], "")
if isinstance(value, (dict, list)):
    import json as _json
    print(_json.dumps(value))
else:
    print(value)
PY
}

status_value() {
  local key="$1"
  local payload="$2"
  python3 - "$key" "$payload" <<'PY'
import sys

target = sys.argv[1]
for raw in sys.argv[2].splitlines():
    if ":" not in raw:
        continue
    key, value = raw.split(":", 1)
    if key.strip() == target:
        print(value.strip())
        break
PY
}

emit_result() {
  local kind="$1"
  local action="$2"
  local target_id="$3"
  local page_json="$4"
  local assisted_status="$5"
  local reason="$6"
  local cdp_port="$7"

  python3 - "$kind" "$action" "$target_id" "$page_json" "$assisted_status" "$reason" "$cdp_port" <<'PY'
import json
import sys

kind, action, target_id, page_json, assisted_status, reason, cdp_port = sys.argv[1:]
payload = {"status": kind, "action": action}
if target_id:
    payload["targetId"] = target_id
if cdp_port:
    try:
        payload["cdpPort"] = int(cdp_port)
    except ValueError:
        pass
if reason:
    payload["reason"] = reason
if page_json:
    page = json.loads(page_json)
    if page.get("url"):
        payload["url"] = page["url"]
    if page.get("title"):
        payload["title"] = page["title"]
    if page.get("bodySnippet"):
        payload["bodySnippet"] = page["bodySnippet"]
if assisted_status:
    for raw in assisted_status.splitlines():
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        if key.strip() == "novnc_url":
            payload["novncUrl"] = value.strip()
        if key.strip() == "lan_novnc_url":
            payload["lanNovncUrl"] = value.strip()
print(json.dumps(payload, ensure_ascii=False))
PY
}

page_field() {
  local payload="$1"
  local field="$2"
  python3 - "$payload" "$field" <<'PY'
import json
import sys

payload = json.loads(sys.argv[1])
value = payload.get(sys.argv[2], "")
print(value if isinstance(value, str) else "")
PY
}

page_matches_target() {
  local page_url="${1:-}"
  python3 - "$page_url" "${INITIAL_URL:-}" "${ORIGIN:-}" <<'PY'
import sys
from urllib.parse import urlparse, urlunparse

page_url, initial_url, origin = sys.argv[1:]

def normalize(value: str) -> str:
    raw = (value or "").strip()
    if not raw:
        return ""
    parsed = urlparse(raw)
    if not parsed.scheme or not parsed.netloc:
        return raw.rstrip("/")
    path = parsed.path or ""
    if path not in ("", "/"):
        path = path.rstrip("/")
    else:
        path = ""
    return urlunparse((
        parsed.scheme.lower(),
        parsed.netloc.lower(),
        path,
        parsed.params,
        parsed.query,
        "",
    ))

page = normalize(page_url)
initial = normalize(initial_url)
origin_value = normalize(origin)

if initial and initial != origin_value:
    raise SystemExit(0 if page == initial else 1)

if origin_value and (page == origin_value or page.startswith(origin_value + "/")):
    raise SystemExit(0)

raise SystemExit(1)
PY
}

page_ready() {
  local payload="$1"
  local page_url
  page_url="$(page_field "$payload" url)"
  page_loaded "$payload" || return 1
  page_matches_target "$page_url"
}

page_loaded() {
  local payload="$1"
  local page_url page_body

  page_url="$(page_field "$payload" url)"
  page_body="$(page_field "$payload" bodySnippet)"
  [ -n "$page_body" ] || return 1
  [ "$page_url" != "about:blank" ] || return 1
  [ -n "$page_url" ] || return 1
  return 0
}

page_mismatch() {
  local payload="$1"
  page_loaded "$payload" || return 1
  page_ready "$payload" && return 1
  return 0
}

resolve_cdp_port() {
  local status_output
  status_output="$(runtime_helper status --origin "$ORIGIN" --session-key "$SESSION_KEY" 2>/dev/null || true)"
  status_value cdp_port "$status_output"
}

select_existing_session() {
  local manifest selected_key

  if manifest="$(manifest_helper show --root "$MANIFEST_ROOT" --origin "$ORIGIN" --session-key "$SESSION_KEY" 2>/dev/null)"; then
    selected_key="$(manifest_field session_key "$manifest" || true)"
    if [ -n "$selected_key" ]; then
      SESSION_KEY="$selected_key"
      return 0
    fi
  fi

  if manifest="$(manifest_helper select --root "$MANIFEST_ROOT" --origin "$ORIGIN" 2>/dev/null)"; then
    selected_key="$(manifest_field session_key "$manifest" || true)"
    if [ -n "$selected_key" ]; then
      SESSION_KEY="$selected_key"
      return 0
    fi
  fi

  return 1
}

resolve_profile() {
  local resolved profile_dir
  resolved="$(
    profile_helper resolve \
      --root "$HOME/.agent-browser" \
      --manifest-root "$MANIFEST_ROOT" \
      --origin "$ORIGIN" \
      --session-key "$SESSION_KEY"
  )" || return $?
  profile_dir="$(manifest_field profile_dir "$resolved" || true)"
  [ -n "$profile_dir" ] || die "profile resolver returned no profile_dir"
  PROFILE_DIR="$profile_dir"
}

ensure_runtime() {
  local runtime_status_output

  if runtime_helper verify --manifest-root "$MANIFEST_ROOT" --origin "$ORIGIN" --session-key "$SESSION_KEY" >/dev/null 2>&1; then
    return 0
  fi

  runtime_status_output="$(runtime_helper status --origin "$ORIGIN" --session-key "$SESSION_KEY" 2>/dev/null || true)"
  if printf '%s\n' "$runtime_status_output" | grep -q '^runtime: running$'; then
    return 0
  fi

  resolve_profile || return $?
  runtime_helper start \
    --url "$INITIAL_URL" \
    --origin "$ORIGIN" \
    --session-key "$SESSION_KEY" \
    --profile-dir "$PROFILE_DIR" \
    --mode gui >/dev/null
}

recover_target_mismatch() {
  if [ -z "${PROFILE_DIR:-}" ]; then
    resolve_profile || return $?
  fi
  runtime_helper stop --origin "$ORIGIN" --session-key "$SESSION_KEY" >/dev/null 2>&1 || true
  runtime_helper start \
    --url "$INITIAL_URL" \
    --origin "$ORIGIN" \
    --session-key "$SESSION_KEY" \
    --profile-dir "$PROFILE_DIR" \
    --mode gui >/dev/null
}

COMMAND_URL=""
ORIGIN=""
MANIFEST_ROOT=""
SESSION_KEY="default"
PROFILE_DIR=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --url)
      COMMAND_URL="$2"
      shift 2
      ;;
    --origin)
      ORIGIN="$2"
      shift 2
      ;;
    --manifest-root)
      MANIFEST_ROOT="$2"
      shift 2
      ;;
    --session-key)
      SESSION_KEY="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "unknown argument: $1"
      ;;
  esac
done

require_arg --url "$COMMAND_URL"
INITIAL_URL="$COMMAND_URL"
ORIGIN="${ORIGIN:-$(derive_origin "$INITIAL_URL")}"
MANIFEST_ROOT="${MANIFEST_ROOT:-$HOME/.agent-browser}"

select_existing_session || true
if ! ensure_runtime; then
  emit_result "needs-user" "open-novnc" "" "" "" "ambiguous-profile" ""
  exit 0
fi
CDP_PORT="$(resolve_cdp_port)"
RECOVERY_ATTEMPTED=0
for _attempt in 1 2 3 4 5; do
  TARGETS_JSON="$(runtime_helper list-targets --origin "$ORIGIN" --session-key "$SESSION_KEY")"
  TARGET_ID="$(
    runtime_helper select-target \
      --origin "$ORIGIN" \
      --target-url "$INITIAL_URL" \
      --targets-json "$TARGETS_JSON"
  )"

  CHALLENGE_JSON="$(runtime_helper check-page --origin "$ORIGIN" --session-key "$SESSION_KEY" --target-id "$TARGET_ID" --check challenge)"
  LOGIN_JSON="$(runtime_helper check-page --origin "$ORIGIN" --session-key "$SESSION_KEY" --target-id "$TARGET_ID" --check login-wall)"
  PAGE_JSON="$(runtime_helper check-page --origin "$ORIGIN" --session-key "$SESSION_KEY" --target-id "$TARGET_ID" --check page-info)"

  if [ "$RECOVERY_ATTEMPTED" -eq 0 ] && page_mismatch "$PAGE_JSON"; then
    if recover_target_mismatch; then
      RECOVERY_ATTEMPTED=1
      sleep 1
      continue
    fi
  fi
  if printf '%s' "$CHALLENGE_JSON" | grep -q '"hasChallenge": *true'; then
    break
  fi
  if printf '%s' "$LOGIN_JSON" | grep -q '"hasLoginWall": *true'; then
    break
  fi
  if page_ready "$PAGE_JSON"; then
    break
  fi
  sleep 1
done

if printf '%s' "$CHALLENGE_JSON" | grep -q '"hasChallenge": *true'; then
  assisted_helper start --url "$INITIAL_URL" --origin "$ORIGIN" --session-key "$SESSION_KEY" >/dev/null
  ASSISTED_STATUS="$(assisted_helper status --url "$INITIAL_URL" --origin "$ORIGIN" --session-key "$SESSION_KEY")"
  emit_result "needs-user" "open-novnc" "$TARGET_ID" "" "$ASSISTED_STATUS" "challenge" "$CDP_PORT"
  exit 0
fi

if printf '%s' "$LOGIN_JSON" | grep -q '"hasLoginWall": *true'; then
  assisted_helper start --url "$INITIAL_URL" --origin "$ORIGIN" --session-key "$SESSION_KEY" >/dev/null
  ASSISTED_STATUS="$(assisted_helper status --url "$INITIAL_URL" --origin "$ORIGIN" --session-key "$SESSION_KEY")"
  emit_result "needs-user" "open-novnc" "$TARGET_ID" "" "$ASSISTED_STATUS" "login-wall" "$CDP_PORT"
  exit 0
fi

if ! page_ready "$PAGE_JSON"; then
  assisted_helper start --url "$INITIAL_URL" --origin "$ORIGIN" --session-key "$SESSION_KEY" >/dev/null
  ASSISTED_STATUS="$(assisted_helper status --url "$INITIAL_URL" --origin "$ORIGIN" --session-key "$SESSION_KEY")"
  emit_result "needs-user" "open-novnc" "$TARGET_ID" "$PAGE_JSON" "$ASSISTED_STATUS" "target-mismatch" "$CDP_PORT"
  exit 0
fi

emit_result "ready" "report-page" "$TARGET_ID" "$PAGE_JSON" "" "" "$CDP_PORT"
