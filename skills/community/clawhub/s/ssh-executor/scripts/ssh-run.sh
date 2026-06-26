#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# ssh-run.sh — Remote SSH command executor with safety guardrails
#
# Provenance:
#   Part of the ssh-executor skill for OpenClaw.
#   Source is bundled and fully reviewable.
#   Verify integrity via the .sha256 checksum in the release package.
#
# Security model:
#   - This script has broad remote-shell authority. Use only for
#     user-requested hosts with user-approved commands.
#   - The dangerous-command heuristic is best-effort and NOT exhaustive.
#   - Host validation should happen BEFORE calling this script;
#     confirm the target with the user first.
# =============================================================================

usage() {
  cat <<'EOF'
Usage:
  ssh-run.sh --host <host-or-alias> [--user <user>] [--port <port>] [--key <path>] \
             [--timeout <seconds>] [--config <ssh-config>] \
             [--host-key-checking <accept-new|yes|no>] [--confirm-dangerous] \
             -- '<remote command>'

  ssh-run.sh --list-aliases [--config <ssh-config>]

Notes:
  - Key-based auth only. Password prompts are disabled.
  - If --host is an SSH alias, omit --user/--port/--key and let ssh config resolve them.
  - JSON is printed to stdout with success, exit_code, stdout, stderr, and resolution metadata.
EOF
}

list_aliases() {
  local config_path="$1"
  if [[ ! -f "$config_path" ]]; then
    echo "[]"
    return 0
  fi
  python3 - "$config_path" <<'PY'
import json
import pathlib
import shlex
import sys

path = pathlib.Path(sys.argv[1])
aliases = []
for raw in path.read_text(encoding='utf-8', errors='replace').splitlines():
    line = raw.strip()
    if not line or line.startswith('#'):
        continue
    if line.lower().startswith('host '):
        parts = shlex.split(line, comments=False)
        for token in parts[1:]:
            if any(ch in token for ch in '*?!'):
                continue
            aliases.append(token)
print(json.dumps(sorted(dict.fromkeys(aliases)), ensure_ascii=False))
PY
}

is_dangerous_command() {
  # Best-effort heuristic: catches common destructive patterns.
  # This is NOT exhaustive — an empty check does NOT mean the command is safe.
  # Uses Python for reliable regex matching (avoids bash [[ =~ ]] escaping pitfalls).
  python3 - "$1" <<'PY'
import re
import sys

cmd = sys.argv[1].lower()

patterns = [
    r'(?:^|[;&|\s])(?:sudo|rm(?!\w)|mv\s|cp\s|chmod\s|chown\s|reboot(?!\w)|shutdown(?!\w)|poweroff(?!\w)|halt(?!\w)|init\s)',
    r'systemctl\s+(?:restart|stop|disable|start|reload|enable)',
    r'(?:apt[\s-]|apt-get[\s-]|dnf[\s-]|yum[\s-]|apk[\s-]|pacman[\s-]|dpkg\s|rpm\s+(?!-q)(?!-qa)(?!-qi)(?!-ql))',
    r'docker\s+(?:compose\s+down|rm|kill|stop|system\s+prune)',
    r'kubectl\s+delete',
    r'sed\s+-i',
    r'ip\s+(?:link\s+(?:set|down|delete)|addr\s+(?:add|del)|route\s+(?:add|del|replace))',
    r'(?:curl|wget)\s+.*(?:[|>])',
    r'(?:sh\s+-c|bash\s+-c)\s',
    r'chpasswd\s|passwd\s|usermod\s|groupmod\s|useradd\s|userdel\s',
    r'(?:>>?\s+\S+(?:\s|$)|>\||:>|echo\s+.*[>]|printf\s+.*[>])',
    r'(?:tee\s|truncate\s|dd\s|mkfs(?!\.\w+)|mkfs\.|fdisk\s|pvcreate\s|vgremove\s|lvremove\s)',
    r'(?:iptables\s|ufw\s|firewall-cmd\s|nmcli\s)',
    r'(?:eval\s|evals\s)',
]

for p in patterns:
    if re.search(p, cmd):
        sys.exit(0)  # 0 = true: command is dangerous
sys.exit(1)  # 1 = false: no match
PY
}

HOST=""
USER_NAME=""
PORT=""
KEY_PATH=""
TIMEOUT="30"
CONFIG_PATH="${HOME}/.ssh/config"
HOST_KEY_CHECKING=""
CONFIRM_DANGEROUS=0
LIST_ALIASES=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --host)
      HOST="${2:-}"
      shift 2
      ;;
    --user)
      USER_NAME="${2:-}"
      shift 2
      ;;
    --port)
      PORT="${2:-}"
      shift 2
      ;;
    --key)
      KEY_PATH="${2:-}"
      shift 2
      ;;
    --timeout)
      TIMEOUT="${2:-}"
      shift 2
      ;;
    --config)
      CONFIG_PATH="${2:-}"
      shift 2
      ;;
    --host-key-checking)
      HOST_KEY_CHECKING="${2:-}"
      shift 2
      ;;
    --confirm-dangerous)
      CONFIRM_DANGEROUS=1
      shift
      ;;
    --list-aliases)
      LIST_ALIASES=1
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    --)
      shift
      break
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ "$LIST_ALIASES" -eq 1 ]]; then
  list_aliases "$CONFIG_PATH"
  exit 0
fi

REMOTE_COMMAND="$*"

if [[ -z "$HOST" || -z "$REMOTE_COMMAND" ]]; then
  usage >&2
  exit 2
fi

if [[ -n "$HOST_KEY_CHECKING" && "$HOST_KEY_CHECKING" != "accept-new" && "$HOST_KEY_CHECKING" != "yes" && "$HOST_KEY_CHECKING" != "no" ]]; then
  echo "Invalid --host-key-checking value: $HOST_KEY_CHECKING" >&2
  exit 2
fi

# The heuristic pattern check catches obvious destructive commands but is NOT exhaustive.
# An empty check is not proof that a command is safe — it only means no known pattern matched.
# Always treat novel, chained, or obfuscated commands with caution.
if is_dangerous_command "$REMOTE_COMMAND" && [[ "$CONFIRM_DANGEROUS" -ne 1 ]]; then
  python3 - "$HOST" "$REMOTE_COMMAND" <<'PY'
import json
import sys
host, remote_command = sys.argv[1:]
print(json.dumps({
    "success": False,
    "exit_code": 99,
    "dangerous": True,
    "heuristic_match": True,
    "error": "Command looks mutating or destructive. Re-run with --confirm-dangerous only after explicit user approval.",
    "host": host,
    "command": remote_command,
}, ensure_ascii=False))
PY
  exit 99
fi

TARGET="$HOST"
if [[ -n "$USER_NAME" ]]; then
  TARGET="$USER_NAME@$HOST"
fi

SSH_ARGS=(
  -o BatchMode=yes
  -o PreferredAuthentications=publickey
  -o PasswordAuthentication=no
  -o ConnectTimeout="$TIMEOUT"
)

if [[ -n "$CONFIG_PATH" && -f "$CONFIG_PATH" ]]; then
  SSH_ARGS+=( -F "$CONFIG_PATH" )
fi
if [[ -n "$PORT" ]]; then
  SSH_ARGS+=( -p "$PORT" )
fi
if [[ -n "$KEY_PATH" ]]; then
  SSH_ARGS+=( -i "$KEY_PATH" )
fi
if [[ -n "$HOST_KEY_CHECKING" ]]; then
  SSH_ARGS+=( -o StrictHostKeyChecking="$HOST_KEY_CHECKING" )
fi

RESOLVED_FILE="$(mktemp)"
STDOUT_FILE="$(mktemp)"
STDERR_FILE="$(mktemp)"
cleanup() {
  rm -f "$RESOLVED_FILE" "$STDOUT_FILE" "$STDERR_FILE"
}
trap cleanup EXIT

set +e
ssh "${SSH_ARGS[@]}" -G "$TARGET" >"$RESOLVED_FILE" 2>/dev/null
RESOLVE_EXIT=$?
ssh "${SSH_ARGS[@]}" "$TARGET" "$REMOTE_COMMAND" >"$STDOUT_FILE" 2>"$STDERR_FILE"
EXIT_CODE=$?
set -e

python3 - "$EXIT_CODE" "$RESOLVE_EXIT" "$HOST" "$USER_NAME" "$PORT" "$TIMEOUT" "$HOST_KEY_CHECKING" "$REMOTE_COMMAND" "$RESOLVED_FILE" "$STDOUT_FILE" "$STDERR_FILE" <<'PY'
import json
import pathlib
import sys

exit_code = int(sys.argv[1])
resolve_exit = int(sys.argv[2])
host, user_name, port, timeout, host_key_checking, remote_command, resolved_file, stdout_file, stderr_file = sys.argv[3:]
stdout_text = pathlib.Path(stdout_file).read_text(encoding='utf-8', errors='replace')
stderr_text = pathlib.Path(stderr_file).read_text(encoding='utf-8', errors='replace')
resolved = {}
if resolve_exit == 0:
    for raw in pathlib.Path(resolved_file).read_text(encoding='utf-8', errors='replace').splitlines():
        if not raw.strip():
            continue
        key, _, value = raw.partition(' ')
        key = key.strip()
        value = value.strip()
        if key in {"hostname", "user", "port"} and value:
            resolved.setdefault(key, []).append(value)

# Security: key paths and ssh config paths are NOT included in output.
# Private-key paths are sensitive metadata that should not be
# exposed to chat, logs, or memory files.
result = {
    "success": exit_code == 0,
    "exit_code": exit_code,
    "dangerous": False,
    "host": host,
    "user": user_name or None,
    "port": int(port) if port else None,
    "timeout": int(timeout),
    "host_key_checking": host_key_checking or None,
    "command": remote_command,
    "resolved_hostname": (resolved.get("hostname") or [None])[0],
    "resolved_user": (resolved.get("user") or [None])[0],
    "resolved_port": int((resolved.get("port") or [0])[0]) if resolved.get("port") else None,
    "stdout": stdout_text,
    "stderr": stderr_text,
}
print(json.dumps(result, ensure_ascii=False))
PY
