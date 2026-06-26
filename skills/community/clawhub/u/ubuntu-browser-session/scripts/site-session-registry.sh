#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/runtime-common.sh"

usage() {
  cat <<'EOF'
Usage:
  site-session-registry.sh show --site SITE [options]
  site-session-registry.sh resolve --site SITE [--session-key KEY] [options]
  site-session-registry.sh write --site SITE --session-key KEY --profile-dir DIR --source-origin URL [options]

Options:
  --profile-dir DIR
  --root DIR
  --session-key KEY
  --site SITE
  --source-origin URL
EOF
}

die() {
  printf '[site-session-registry] ERROR: %s\n' "$*" >&2
  exit 1
}

require_arg() {
  local name="$1"
  local value="$2"
  [ -n "$value" ] || die "missing required argument: $name"
}

timestamp() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

registry_path() {
  printf '%s/index/site-sessions.json\n' "$ROOT_DIR"
}

safe_payload() {
  python3 - "$1" <<'PY'
import json
import os
import sys

path = sys.argv[1]
payload = {"sites": {}}
if os.path.exists(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except (json.JSONDecodeError, OSError):
        payload = {"sites": {}}
print(json.dumps(payload))
PY
}

cmd_show() {
  require_arg --site "$SITE"
  local path payload
  path="$(registry_path)"
  payload="$(safe_payload "$path")"
  python3 - "$payload" "$SITE" <<'PY'
import json
import sys

payload = json.loads(sys.argv[1])
site = sys.argv[2]
entry = payload.get("sites", {}).get(site)
if not entry:
    raise SystemExit(1)
print(json.dumps(entry, indent=2, sort_keys=True))
PY
}

cmd_resolve() {
  require_arg --site "$SITE"
  local path payload
  path="$(registry_path)"
  payload="$(safe_payload "$path")"
  python3 - "$payload" "$SITE" "${SESSION_KEY:-}" <<'PY'
import json
import sys

payload = json.loads(sys.argv[1])
site = sys.argv[2]
session_key = sys.argv[3] or ""
entry = payload.get("sites", {}).get(site)
if not entry:
    raise SystemExit(1)
sessions = entry.get("sessions", {})
resolved_key = session_key or entry.get("default_session") or ""
session = sessions.get(resolved_key)
if not session:
    raise SystemExit(1)
result = dict(session)
result["site"] = site
result["session_key"] = resolved_key
result["default_session"] = entry.get("default_session")
print(json.dumps(result, sort_keys=True))
PY
}

cmd_write() {
  require_arg --site "$SITE"
  require_arg --session-key "$SESSION_KEY"
  require_arg --profile-dir "$PROFILE_DIR"
  require_arg --source-origin "$SOURCE_ORIGIN"
  local path now payload
  path="$(registry_path)"
  now="$(timestamp)"
  mkdir -p "$(dirname "$path")"
  payload="$(safe_payload "$path")"
  python3 - "$path" "$payload" "$SITE" "$SESSION_KEY" "$PROFILE_DIR" "$SOURCE_ORIGIN" "$now" <<'PY'
import json
import sys

path, payload_raw, site, session_key, profile_dir, source_origin, now = sys.argv[1:]
payload = json.loads(payload_raw)
sites = payload.setdefault("sites", {})
entry = sites.setdefault(site, {"default_session": session_key, "sessions": {}})
entry.setdefault("default_session", session_key)
sessions = entry.setdefault("sessions", {})
sessions[session_key] = {
    "profile_dir": profile_dir,
    "source_origin": source_origin,
    "updated_at": now,
}
if not entry.get("default_session"):
    entry["default_session"] = session_key
with open(path, "w", encoding="utf-8") as handle:
    json.dump(payload, handle, indent=2, sort_keys=True)
    handle.write("\n")
PY
}

COMMAND="${1:-}"
[ -n "$COMMAND" ] || {
  usage
  exit 1
}
shift || true

ROOT_DIR="${ROOT_DIR:-$HOME/.agent-browser}"
SITE=""
SESSION_KEY=""
PROFILE_DIR=""
SOURCE_ORIGIN=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --root)
      ROOT_DIR="$2"
      shift 2
      ;;
    --site)
      SITE="$2"
      shift 2
      ;;
    --session-key)
      SESSION_KEY="$2"
      shift 2
      ;;
    --profile-dir)
      PROFILE_DIR="$2"
      shift 2
      ;;
    --source-origin)
      SOURCE_ORIGIN="$2"
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

case "$COMMAND" in
  show)
    cmd_show
    ;;
  resolve)
    cmd_resolve
    ;;
  write)
    cmd_write
    ;;
  *)
    usage
    exit 1
    ;;
esac
