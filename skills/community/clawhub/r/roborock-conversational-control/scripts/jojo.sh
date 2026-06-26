#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_FILE="${JOJO_CONFIG_FILE:-$SKILL_DIR/jojo.env}"

if [[ -f "$CONFIG_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$CONFIG_FILE"
fi

DEVICE_ID="${JOJO_DEVICE_ID:-}"
DEVICE_NAME="${JOJO_DEVICE_NAME:-jojo}"
ROBOROCK_BIN="${ROBOROCK_BIN:-}"

if [[ -z "$ROBOROCK_BIN" ]]; then
  if command -v roborock >/dev/null 2>&1; then
    ROBOROCK_BIN="$(command -v roborock)"
  elif [[ -x "$HOME/.local/bin/roborock" ]]; then
    ROBOROCK_BIN="$HOME/.local/bin/roborock"
  else
    echo "Could not find roborock CLI." >&2
    exit 1
  fi
fi

if [[ -z "$DEVICE_ID" ]]; then
  echo "Missing JOJO_DEVICE_ID. Set it in $CONFIG_FILE or your shell." >&2
  exit 1
fi

DRY_RUN=0
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=1
  shift
fi

usage() {
  cat <<'EOF'
Usage:
  jojo.sh status
  jojo.sh start
  jojo.sh pause
  jojo.sh stop
  jojo.sh home
  jojo.sh rooms
  jojo.sh room kitchen
  jojo.sh room "master bedroom"
  jojo.sh segment 17
  jojo.sh segment 17,21
EOF
}

run_cmd() {
  local -a cmd=("$@")
  if (( DRY_RUN )); then
    printf 'DRY RUN:'
    printf ' %q' "${cmd[@]}"
    printf '\n'
    return 0
  fi
  "${cmd[@]}"
}

normalize_label() {
  printf '%s' "$1" | tr '[:upper:]' '[:lower:]' | sed -E 's/[[:space:]]+/ /g; s/^ //; s/ $//'
}

env_room_json() {
  local tmpfile
  tmpfile="$(mktemp)"
  {
    printf '%s\n' '{'
    printf '  "device_name": "%s",\n' "$DEVICE_NAME"
    printf '  "device_id": "%s",\n' "$DEVICE_ID"
    printf '%s\n' '  "rooms": ['
    local first=1
    local var_name
    while IFS= read -r var_name; do
      local value label
      value="${!var_name}"
      [[ -n "$value" ]] || continue
      label="$(printf '%s' "${var_name#ROOM_}" | tr '[:upper:]' '[:lower:]' | tr '_' ' ')"
      if (( first )); then
        first=0
      else
        printf '%s\n' ','
      fi
      printf '    {"name": "%s", "segmentId": %s}' "$label" "$value"
    done < <(compgen -A variable ROOM_ | sort)
    printf '\n'
    printf '%s\n' '  ]'
    printf '%s\n' '}'
  } > "$tmpfile"
  python3 -m json.tool "$tmpfile"
  rm -f "$tmpfile"
}

lookup_room_id_from_env() {
  local target="$1"
  local var_name
  while IFS= read -r var_name; do
    local value label short
    value="${!var_name}"
    [[ -n "$value" ]] || continue
    label="$(printf '%s' "${var_name#ROOM_}" | tr '[:upper:]' '[:lower:]' | tr '_' ' ')"
    short="$label"
    if [[ "$label" == *" room" ]]; then
      short="${label% room}"
    fi
    if [[ "$target" == "$label" || "$target" == "$short" ]]; then
      printf '%s\n' "$value"
      return 0
    fi
  done < <(compgen -A variable ROOM_)
  return 1
}

lookup_room_id_live() {
  local target="$1"
  "$ROBOROCK_BIN" rooms --device_id "$DEVICE_ID" | python3 - "$target" <<'PY'
import json, sys

target = sys.argv[1].strip().lower()
data = json.load(sys.stdin)
rooms = data.get("rooms", [])

def norm(s: str) -> str:
    return " ".join(s.lower().split())

for room in rooms:
    raw = norm(str(room.get("rawName", "")))
    if raw == target:
        print(room["segmentId"])
        raise SystemExit(0)
    if raw.endswith(" room") and raw[:-5].strip() == target:
        print(room["segmentId"])
        raise SystemExit(0)
raise SystemExit(1)
PY
}

segment_params() {
  local raw="$1"
  raw="${raw// /}"
  printf '[%s]' "$raw"
}

command_name="${1:-help}"
shift || true

case "$command_name" in
  help|-h|--help)
    usage
    ;;
  status)
    run_cmd "$ROBOROCK_BIN" status --device_id "$DEVICE_ID"
    ;;
  start|clean|house)
    run_cmd "$ROBOROCK_BIN" command --device_id "$DEVICE_ID" --cmd app_start
    ;;
  pause)
    run_cmd "$ROBOROCK_BIN" command --device_id "$DEVICE_ID" --cmd app_pause
    ;;
  stop)
    run_cmd "$ROBOROCK_BIN" command --device_id "$DEVICE_ID" --cmd app_stop
    ;;
  home|dock|charge)
    run_cmd "$ROBOROCK_BIN" command --device_id "$DEVICE_ID" --cmd app_charge
    ;;
  rooms)
    if compgen -A variable ROOM_ >/dev/null 2>&1; then
      env_room_json
    else
      run_cmd "$ROBOROCK_BIN" rooms --device_id "$DEVICE_ID"
    fi
    ;;
  room)
    if [[ $# -lt 1 ]]; then
      echo "Missing room name." >&2
      exit 1
    fi
    room_name="$*"
    room_norm="$(normalize_label "$room_name")"
    room_id="$(lookup_room_id_from_env "$room_norm" || true)"
    if [[ -z "$room_id" ]]; then
      room_id="$(lookup_room_id_live "$room_norm" || true)"
    fi
    if [[ -z "$room_id" ]]; then
      echo "Unknown room: $room_name" >&2
      exit 1
    fi
    run_cmd "$ROBOROCK_BIN" command --device_id "$DEVICE_ID" --cmd app_segment_clean --params "$(segment_params "$room_id")"
    ;;
  segment)
    if [[ $# -lt 1 ]]; then
      echo "Missing segment id list." >&2
      exit 1
    fi
    run_cmd "$ROBOROCK_BIN" command --device_id "$DEVICE_ID" --cmd app_segment_clean --params "$(segment_params "$1")"
    ;;
  *)
    echo "Unknown command: $command_name" >&2
    usage >&2
    exit 1
    ;;
esac
