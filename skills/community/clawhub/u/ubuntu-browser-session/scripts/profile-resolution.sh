#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/runtime-common.sh"

usage() {
  cat <<'EOF'
Usage:
  profile-resolution.sh resolve --origin URL [options]
  profile-resolution.sh show-identity --provider HOST [options]
  profile-resolution.sh write-identity --provider HOST --profile-dir DIR [options]

Options:
  --manifest-root DIR
  --origin URL
  --profile-dir DIR
  --provider HOST
  --root DIR
  --session-key KEY
  --source-origin URL
  --source-session-key KEY
EOF
}

die() {
  printf '[profile-resolution] ERROR: %s\n' "$*" >&2
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

identity_index_path() {
  printf '%s/index/identity-profiles.json\n' "$ROOT_DIR"
}

site_registry_helper() {
  "${AGENT_BROWSER_SITE_REGISTRY_HELPER:-$SCRIPT_DIR/site-session-registry.sh}" "$@"
}

provider_aliases_json() {
  local value="$1"
  local aliases=()
  mapfile -t aliases < <(provider_aliases "$value")
  python3 - "${aliases[@]}" <<'PY'
import json
import sys

print(json.dumps(sys.argv[1:]))
PY
}

profile_resolution_json() {
  python3 - <<'PY'
import json
import os
from urllib.parse import urlparse

origin = os.environ["ORIGIN"]
session_key = os.environ.get("SESSION_KEY", "default")
root_dir = os.environ["ROOT_DIR"]
explicit_profile = os.environ.get("PROFILE_DIR", "")
manifest_payload = os.environ.get("MANIFEST_PAYLOAD", "")
aliases = json.loads(os.environ.get("ALIASES_JSON", "[]"))

def host_from_origin(value: str) -> str:
    parsed = urlparse(value)
    return (parsed.netloc or value).lower()

def evidence_score(path: str) -> int:
    score = 0
    if os.path.exists(os.path.join(path, "Default", "Cookies")):
        score += 1
    if os.path.exists(os.path.join(path, "Default", "Login Data")):
        score += 1
    if os.path.exists(os.path.join(path, "Local State")):
        score += 1
    return score

if explicit_profile:
    print(json.dumps({"profile_dir": explicit_profile, "source": "explicit"}))
    raise SystemExit(0)

if manifest_payload:
    manifest = json.loads(manifest_payload)
    profile_dir = manifest.get("profile_dir") or ""
    if profile_dir:
        print(json.dumps({"profile_dir": profile_dir, "source": "manifest"}))
        raise SystemExit(0)

identity_path = os.path.join(root_dir, "index", "identity-profiles.json")
if aliases and os.path.exists(identity_path):
    try:
        with open(identity_path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except (json.JSONDecodeError, OSError):
        payload = {"providers": {}}
    providers = payload.get("providers", {})
    for alias in aliases:
        entry = providers.get(alias) or {}
        profile_dir = entry.get("profile_dir") or ""
        if profile_dir:
            print(json.dumps({
                "profile_dir": profile_dir,
                "source": "identity-index",
                "provider": alias,
                "source_origin": entry.get("source_origin"),
                "source_session_key": entry.get("source_session_key"),
            }))
            raise SystemExit(0)

host = host_from_origin(origin)
legacy_profile = os.path.join(root_dir, "profiles", host)
scoped_profile = os.path.join(root_dir, "profiles", os.environ["ORIGIN_KEY"], session_key)

legacy_exists = os.path.isdir(legacy_profile)
scoped_exists = os.path.isdir(scoped_profile)

if legacy_exists and scoped_exists:
    legacy_score = evidence_score(legacy_profile)
    scoped_score = evidence_score(scoped_profile)
    if legacy_score > scoped_score:
        print(json.dumps({"profile_dir": legacy_profile, "source": "legacy"}))
        raise SystemExit(0)
    if scoped_score > legacy_score:
        print(json.dumps({"profile_dir": scoped_profile, "source": "scoped"}))
        raise SystemExit(0)
    if legacy_score > 0:
        print(json.dumps({
            "error": "ambiguous-profile",
            "legacy_profile": legacy_profile,
            "scoped_profile": scoped_profile,
        }))
        raise SystemExit(2)
    print(json.dumps({"profile_dir": legacy_profile, "source": "legacy"}))
    raise SystemExit(0)

if legacy_exists:
    print(json.dumps({"profile_dir": legacy_profile, "source": "legacy"}))
    raise SystemExit(0)

print(json.dumps({"profile_dir": scoped_profile, "source": "scoped"}))
PY
}

cmd_resolve() {
  require_arg --origin "$ORIGIN"
  ORIGIN_KEY="$(origin_slug "$ORIGIN")"
  SITE_KEY="$(site_key "$ORIGIN")"
  ALIASES_JSON="$(provider_aliases_json "$ORIGIN")"
  MANIFEST_PAYLOAD="$(
    "$SCRIPT_DIR/session-manifest.sh" show --root "$MANIFEST_ROOT" --origin "$ORIGIN" --session-key "$SESSION_KEY" 2>/dev/null || true
  )"
  SITE_PAYLOAD="$(
    site_registry_helper resolve --root "$ROOT_DIR" --site "$SITE_KEY" --session-key "$SESSION_KEY" 2>/dev/null || true
  )"
  if [ -n "$SITE_PAYLOAD" ]; then
    python3 - "$SITE_PAYLOAD" <<'PY'
import json
import sys

payload = json.loads(sys.argv[1])
print(json.dumps({
    "profile_dir": payload["profile_dir"],
    "site": payload.get("site"),
    "session_key": payload.get("session_key"),
    "source": "site-registry",
}))
PY
    return 0
  fi
  export ORIGIN SESSION_KEY ROOT_DIR PROFILE_DIR MANIFEST_PAYLOAD ALIASES_JSON ORIGIN_KEY
  profile_resolution_json
}

cmd_show_identity() {
  require_arg --provider "$PROVIDER"
  local path
  path="$(identity_index_path)"
  [ -f "$path" ] || exit 1
  python3 - "$path" "$PROVIDER" <<'PY'
import json
import sys

with open(sys.argv[1], "r", encoding="utf-8") as handle:
    try:
        payload = json.load(handle)
    except json.JSONDecodeError:
        raise SystemExit(1)
entry = payload.get("providers", {}).get(sys.argv[2], {})
if not entry:
    raise SystemExit(1)
print(json.dumps(entry, sort_keys=True))
PY
}

cmd_write_identity() {
  require_arg --provider "$PROVIDER"
  require_arg --profile-dir "$PROFILE_DIR"
  require_arg --source-origin "$SOURCE_ORIGIN"
  require_arg --source-session-key "$SOURCE_SESSION_KEY"
  local path now
  path="$(identity_index_path)"
  now="$(timestamp)"
  mkdir -p "$(dirname "$path")"
  python3 - "$path" "$PROVIDER" "$PROFILE_DIR" "$SOURCE_ORIGIN" "$SOURCE_SESSION_KEY" "$now" <<'PY'
import json
import os
import sys

path, provider, profile_dir, source_origin, source_session_key, now = sys.argv[1:]
payload = {"providers": {}}
if os.path.exists(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except (json.JSONDecodeError, OSError):
        payload = {"providers": {}}
providers = payload.setdefault("providers", {})
providers[provider] = {
    "profile_dir": profile_dir,
    "source_origin": source_origin,
    "source_session_key": source_session_key,
    "updated_at": now,
}
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
MANIFEST_ROOT="${MANIFEST_ROOT:-$ROOT_DIR}"
ORIGIN=""
SESSION_KEY="default"
PROFILE_DIR=""
PROVIDER=""
SOURCE_ORIGIN=""
SOURCE_SESSION_KEY=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --root)
      ROOT_DIR="$2"
      shift 2
      ;;
    --manifest-root)
      MANIFEST_ROOT="$2"
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
    --profile-dir)
      PROFILE_DIR="$2"
      shift 2
      ;;
    --provider)
      PROVIDER="$2"
      shift 2
      ;;
    --source-origin)
      SOURCE_ORIGIN="$2"
      shift 2
      ;;
    --source-session-key)
      SOURCE_SESSION_KEY="$2"
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
  resolve)
    cmd_resolve
    ;;
  show-identity)
    cmd_show_identity
    ;;
  write-identity)
    cmd_write_identity
    ;;
  *)
    usage
    exit 1
    ;;
esac
