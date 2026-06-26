#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/runtime-common.sh"

usage() {
  cat <<'EOF'
Usage:
  session-manifest.sh list [--root DIR]
  session-manifest.sh path --origin URL [--session-key KEY] [--root DIR]
  session-manifest.sh write --origin URL --session-key KEY --state STATE --browser-pid PID [options]
  session-manifest.sh mark-stale --origin URL [--session-key KEY] --reason TEXT [--root DIR]
  session-manifest.sh show --origin URL [--session-key KEY] [--root DIR]
  session-manifest.sh index-show --origin URL [--root DIR]
  session-manifest.sh select --origin URL [--account-hint TEXT] [--task-scope TEXT] [--root DIR]

Options:
  --account-hint TEXT
  --block-reason TEXT
  --root DIR
  --session-key KEY
  --task-scope TEXT
EOF
}

die() {
  printf '[session-manifest] ERROR: %s\n' "$*" >&2
  exit 1
}

timestamp() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

require_arg() {
  local name="$1"
  local value="$2"
  [ -n "$value" ] || die "missing required argument: $name"
}

init_paths() {
  MANIFEST_ROOT="${MANIFEST_ROOT:-$HOME/.agent-browser}"
  ROOT_DIR="${ROOT_DIR:-$MANIFEST_ROOT}"
  MANIFEST_DIR="$ROOT_DIR/sessions"
  INDEX_DIR="$ROOT_DIR/index"
  mkdir -p "$MANIFEST_DIR" "$INDEX_DIR"
}

origin_key() {
  origin_slug "$1"
}

origin_dir() {
  printf '%s/%s\n' "$MANIFEST_DIR" "$(origin_key "$1")"
}

index_path() {
  printf '%s/%s.json\n' "$INDEX_DIR" "$(origin_key "$1")"
}

manifest_path() {
  local origin="$1"
  local session_key="$2"
  printf '%s/%s.json\n' "$(origin_dir "$origin")" "$session_key"
}

ensure_origin_dir() {
  mkdir -p "$(origin_dir "$1")"
}

rebuild_index() {
  local origin="$1"
  local origin_path
  local index_file
  origin_path="$(origin_dir "$origin")"
  index_file="$(index_path "$origin")"

  python3 - "$origin_path" "$index_file" <<'PY'
import json
import os
import sys

origin_dir = sys.argv[1]
index_file = sys.argv[2]
items = []
if os.path.isdir(origin_dir):
    for name in sorted(os.listdir(origin_dir)):
        if not name.endswith(".json"):
            continue
        path = os.path.join(origin_dir, name)
        try:
            with open(path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except FileNotFoundError:
            continue
        items.append({
            "session_key": data.get("session_key"),
            "account_hint": data.get("account_hint"),
            "task_scope": data.get("task_scope"),
            "state": data.get("state"),
            "browser_pid": data.get("browser_pid"),
            "last_verified_at": data.get("last_verified_at"),
            "path": path,
        })
with open(index_file, "w", encoding="utf-8") as handle:
    json.dump({"sessions": items}, handle, indent=2, sort_keys=True)
    handle.write("\n")
PY
}

cmd_list() {
  if [ ! -d "$MANIFEST_DIR" ]; then
    exit 0
  fi
  find "$MANIFEST_DIR" -mindepth 2 -maxdepth 2 -type f -name '*.json' | sort
}

cmd_path() {
  require_arg --origin "$ORIGIN"
  if [ -n "$SESSION_KEY" ]; then
    printf '%s\n' "$(manifest_path "$ORIGIN" "$SESSION_KEY")"
    return 0
  fi
  printf '%s\n' "$(origin_dir "$ORIGIN")"
}

cmd_write() {
  require_arg --origin "$ORIGIN"
  require_arg --session-key "$SESSION_KEY"
  require_arg --state "$STATE"
  require_arg --browser-pid "$BROWSER_PID"

  ensure_origin_dir "$ORIGIN"
  local path now created_at
  path="$(manifest_path "$ORIGIN" "$SESSION_KEY")"
  now="$(timestamp)"
  created_at="$now"
  if [ -f "$path" ]; then
    created_at="$(python3 - "$path" <<'PY'
import json
import sys
with open(sys.argv[1], "r", encoding="utf-8") as handle:
    data = json.load(handle)
print(data.get("created_at", ""))
PY
)"
    created_at="${created_at:-$now}"
  fi

  python3 - "$path" <<'PY'
import json
import os
import sys

path = sys.argv[1]
payload = {
    "origin": os.environ["ORIGIN"],
    "session_key": os.environ["SESSION_KEY"],
    "account_hint": os.environ.get("ACCOUNT_HINT") or None,
    "task_scope": os.environ.get("TASK_SCOPE") or None,
    "state": os.environ["STATE"],
    "browser_pid": int(os.environ["BROWSER_PID"]),
    "created_at": os.environ["CREATED_AT"],
    "last_verified_at": os.environ["NOW"],
}
optional_keys = [
    "BLOCK_REASON",
    "CDP_PORT",
    "CDP_URL",
    "WEBSOCKET_DEBUGGER_URL",
    "TARGET_ID",
    "PROFILE_DIR",
    "MODE",
    "DISPLAY_VALUE",
    "XVFB_DISPLAY",
    "XVFB_PID",
    "NOVNC_PORT",
]
field_map = {
    "BLOCK_REASON": "block_reason",
    "CDP_PORT": "cdp_port",
    "CDP_URL": "cdp_url",
    "WEBSOCKET_DEBUGGER_URL": "websocket_debugger_url",
    "TARGET_ID": "target_id",
    "PROFILE_DIR": "profile_dir",
    "MODE": "mode",
    "DISPLAY_VALUE": "display",
    "XVFB_DISPLAY": "xvfb_display",
    "XVFB_PID": "xvfb_pid",
    "NOVNC_PORT": "novnc_port",
}
int_fields = {"CDP_PORT", "XVFB_PID", "NOVNC_PORT"}
for key in optional_keys:
    value = os.environ.get(key)
    if value in (None, ""):
      continue
    payload[field_map[key]] = int(value) if key in int_fields else value
with open(path, "w", encoding="utf-8") as handle:
    json.dump(payload, handle, indent=2, sort_keys=True)
    handle.write("\n")
PY

  rebuild_index "$ORIGIN"
  cat "$path"
}

resolve_single_path() {
  require_arg --origin "$ORIGIN"
  local path
  if [ -n "$SESSION_KEY" ]; then
    path="$(manifest_path "$ORIGIN" "$SESSION_KEY")"
    [ -f "$path" ] || die "manifest not found for origin/session-key"
    printf '%s\n' "$path"
    return 0
  fi

  mapfile -t matches < <(find "$(origin_dir "$ORIGIN")" -maxdepth 1 -type f -name '*.json' 2>/dev/null | sort)
  case "${#matches[@]}" in
    1)
      printf '%s\n' "${matches[0]}"
      ;;
    0)
      die "no manifests found for origin"
      ;;
    *)
      die "multiple manifests found; provide --session-key or use select"
      ;;
  esac
}

cmd_show() {
  local path
  path="$(resolve_single_path)"
  cat "$path"
}

cmd_index_show() {
  require_arg --origin "$ORIGIN"
  local file
  file="$(index_path "$ORIGIN")"
  if [ ! -f "$file" ]; then
    rebuild_index "$ORIGIN"
  fi
  cat "$file"
}

cmd_mark_stale() {
  require_arg --origin "$ORIGIN"
  require_arg --reason "$REASON"
  local path
  path="$(resolve_single_path)"
  python3 - "$path" <<'PY'
import json
import os
import sys

path = sys.argv[1]
with open(path, "r", encoding="utf-8") as handle:
    data = json.load(handle)
data["state"] = "stale"
data["stale_reason"] = os.environ["REASON"]
data["last_verified_at"] = os.environ["NOW"]
with open(path, "w", encoding="utf-8") as handle:
    json.dump(data, handle, indent=2, sort_keys=True)
    handle.write("\n")
PY
  rebuild_index "$ORIGIN"
  cat "$path"
}

filter_candidates() {
  python3 - <<'PY'
import json
import os
import sys

index_file = os.environ["INDEX_FILE"]
account_hint = os.environ.get("ACCOUNT_HINT") or ""
task_scope = os.environ.get("TASK_SCOPE") or ""
with open(index_file, "r", encoding="utf-8") as handle:
    payload = json.load(handle)
candidates = payload.get("sessions", [])
if account_hint:
    candidates = [item for item in candidates if item.get("account_hint") == account_hint]
if task_scope:
    candidates = [item for item in candidates if item.get("task_scope") == task_scope]
for item in candidates:
    print(json.dumps(item, sort_keys=True))
PY
}

cmd_select() {
  require_arg --origin "$ORIGIN"
  local file selected_count line selected_path
  file="$(index_path "$ORIGIN")"
  if [ ! -f "$file" ]; then
    rebuild_index "$ORIGIN"
  fi
  mapfile -t selected < <(INDEX_FILE="$file" ACCOUNT_HINT="$ACCOUNT_HINT" TASK_SCOPE="$TASK_SCOPE" filter_candidates)
  selected_count="${#selected[@]}"
  if [ "$selected_count" -eq 0 ]; then
    die "no matching sessions found"
  fi
  if [ "$selected_count" -gt 1 ]; then
    die "multiple matching sessions found; provide --account-hint or --task-scope"
  fi
  selected_path="$(python3 - "${selected[0]}" <<'PY'
import json
import sys
print(json.loads(sys.argv[1])["path"])
PY
)"
  cat "$selected_path"
}

COMMAND="${1:-}"
[ -n "$COMMAND" ] || {
  usage
  exit 1
}
shift || true

ROOT_DIR=""
ORIGIN=""
SESSION_KEY=""
ACCOUNT_HINT=""
TASK_SCOPE=""
STATE=""
BROWSER_PID=""
REASON=""
BLOCK_REASON=""
CDP_PORT=""
CDP_URL=""
WEBSOCKET_DEBUGGER_URL=""
TARGET_ID=""
PROFILE_DIR=""
MODE=""
DISPLAY_VALUE=""
XVFB_DISPLAY=""
XVFB_PID=""
NOVNC_PORT=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --root)
      ROOT_DIR="$2"
      shift 2
      ;;
    --origin)
      ORIGIN="$2"
      shift 2
      ;;
    --session-key)
      SESSION_KEY="$2"
      shift 2
      ;;
    --account-hint)
      ACCOUNT_HINT="$2"
      shift 2
      ;;
    --task-scope)
      TASK_SCOPE="$2"
      shift 2
      ;;
    --state)
      STATE="$2"
      shift 2
      ;;
    --browser-pid)
      BROWSER_PID="$2"
      shift 2
      ;;
    --reason)
      REASON="$2"
      shift 2
      ;;
    --block-reason)
      BLOCK_REASON="$2"
      shift 2
      ;;
    --cdp-port)
      CDP_PORT="$2"
      shift 2
      ;;
    --cdp-url)
      CDP_URL="$2"
      shift 2
      ;;
    --websocket-debugger-url)
      WEBSOCKET_DEBUGGER_URL="$2"
      shift 2
      ;;
    --target-id)
      TARGET_ID="$2"
      shift 2
      ;;
    --profile-dir)
      PROFILE_DIR="$2"
      shift 2
      ;;
    --mode)
      MODE="$2"
      shift 2
      ;;
    --display)
      DISPLAY_VALUE="$2"
      shift 2
      ;;
    --xvfb-display)
      XVFB_DISPLAY="$2"
      shift 2
      ;;
    --xvfb-pid)
      XVFB_PID="$2"
      shift 2
      ;;
    --novnc-port)
      NOVNC_PORT="$2"
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

init_paths
NOW="$(timestamp)"
CREATED_AT="$NOW"
export ORIGIN SESSION_KEY ACCOUNT_HINT TASK_SCOPE STATE BROWSER_PID REASON BLOCK_REASON
export CDP_PORT CDP_URL WEBSOCKET_DEBUGGER_URL TARGET_ID PROFILE_DIR MODE DISPLAY_VALUE
export XVFB_DISPLAY XVFB_PID NOVNC_PORT NOW CREATED_AT

case "$COMMAND" in
  list)
    cmd_list
    ;;
  path)
    cmd_path
    ;;
  write)
    cmd_write
    ;;
  mark-stale)
    cmd_mark_stale
    ;;
  show)
    cmd_show
    ;;
  index-show)
    cmd_index_show
    ;;
  select)
    cmd_select
    ;;
  *)
    usage
    exit 1
    ;;
esac
