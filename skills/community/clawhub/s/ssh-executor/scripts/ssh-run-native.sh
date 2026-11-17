#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# ssh-run-native.sh — Native openssh-client backend for ssh-executor
#
# Used by ssh-run.sh when openssh-client (ssh + ssh-add + ssh-agent) is
# available on the system. Otherwise, ssh-run.sh falls back to the
# Python/Paramiko backend.
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat <<'EOF'
Usage:
  ssh-run.sh --host <host-or-alias> [--user <user>] [--port <port>] [--key <path>] \
             [--vault-key <key-name>] \
             [--timeout <seconds>] [--config <ssh-config>] \
             [--host-key-checking <yes|no>] [--confirm-dangerous] \
             [--control-persist <seconds>] [--control-close] [--pty] \
             [--sudo --sudo-pass-vault <name>] \
             [--sudo-pass-ask] \
             [--ssh-pass-vault <name>] [--ssh-pass-ask] \
             -- '<remote command>'

  ssh-run.sh --list-aliases [--config <ssh-config>]
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
  python3 - "$1" <<'PY'
import re, sys
cmd = sys.argv[1].lower()
patterns = [
    r'(?:^|[;&|\s])(?:sudo|rm(?!\w)|mv\s|cp\s|chmod\s|chown\s|reboot(?!\w)|shutdown(?!\w)|poweroff(?!\w)|halt(?!\w)|init\s)',
    r'systemctl\s+(?:restart|stop|disable|start|reload|enable)',
    r'(?:apt[\s-]|apt-get[\s-]|dnf[\s-]|yum[\s-]|apk[\s-]|pacman[\s-]|dpkg\s|rpm\s+(?!-q)(?!-qa)(?!-qi)(?!-ql))',
    r'docker\s+(?:compose\s+down|rm|kill|stop|system\s+prune)',
    r'kubectl\s+delete', r'sed\s+-i',
    r'ip\s+(?:link\s+(?:set|down|delete)|addr\s+(?:add|del)|route\s+(?:add|del|replace))',
    r'(?:curl|wget)\s+.*(?:[|>])', r'(?:sh\s+-c|bash\s+-c)\s',
    r'chpasswd\s|passwd\s|usermod\s|groupmod\s|useradd\s|userdel\s',
    r'(?:>>?\s+\S+(?:\s|$)|>\||:>|echo\s+.*[>]|printf\s+.*[>])',
    r'(?:tee\s|truncate\s|dd\s|mkfs(?!\.\w+)|mkfs\.|fdisk\s|pvcreate\s|vgremove\s|lvremove\s)',
    r'(?:iptables\s|ufw\s|firewall-cmd\s|nmcli\s)', r'(?:eval\s|evals\s)',
]
for p in patterns:
    if re.search(p, cmd):
        sys.exit(0)
sys.exit(1)
PY
}

HOST=""
USER_NAME=""
PORT=""
KEY_PATH=""
VAULT_KEY=""
TIMEOUT="30"
CONFIG_PATH="${HOME}/.ssh/config"
HOST_KEY_CHECKING=""
CONFIRM_DANGEROUS=0
LIST_ALIASES=0
CONTROL_PERSIST="180"
CONTROL_CLOSE=0
PTY_MODE=0
SUDO_MODE=0
SUDO_PASS_VAULT=""
SUDO_PASS_ASK=0
SSH_PASS_VAULT=""
SSH_PASS_ASK=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --host) HOST="${2:-}"; shift 2 ;;
    --user) USER_NAME="${2:-}"; shift 2 ;;
    --port) PORT="${2:-}"; shift 2 ;;
    --key) KEY_PATH="${2:-}"; shift 2 ;;
    --vault-key) VAULT_KEY="${2:-}"; shift 2 ;;
    --timeout) TIMEOUT="${2:-}"; shift 2 ;;
    --config) CONFIG_PATH="${2:-}"; shift 2 ;;
    --host-key-checking) HOST_KEY_CHECKING="${2:-}"; shift 2 ;;
    --confirm-dangerous) CONFIRM_DANGEROUS=1; shift ;;
    --control-persist) CONTROL_PERSIST="${2:-180}"; shift 2 ;;
    --control-close) CONTROL_CLOSE=1; shift ;;
    --pty) PTY_MODE=1; shift ;;
    --sudo) SUDO_MODE=1; shift ;;
    --sudo-pass-vault) SUDO_PASS_VAULT="${2:-}"; shift 2 ;;
    --sudo-pass-ask) SUDO_PASS_ASK=1; shift ;;
    --ssh-pass-vault) SSH_PASS_VAULT="${2:-}"; shift 2 ;;
    --ssh-pass-ask) SSH_PASS_ASK=1; shift ;;
    --list-aliases) LIST_ALIASES=1; shift ;;
    --help|-h) usage; exit 0 ;;
    --) shift; break ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 2 ;;
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

if [[ -n "$HOST_KEY_CHECKING" && "$HOST_KEY_CHECKING" != "yes" && "$HOST_KEY_CHECKING" != "no" ]]; then
  echo "Invalid --host-key-checking value: $HOST_KEY_CHECKING (only 'yes' or 'no' allowed)" >&2
  exit 2
fi

# Default to strict host-key checking (never auto-trust unknown hosts)
if [[ -z "$HOST_KEY_CHECKING" ]]; then
  HOST_KEY_CHECKING="yes"
fi

# Explicit warning when user opts out of host-key verification
if [[ "$HOST_KEY_CHECKING" == "no" ]]; then
  echo "⚠️  SECURITY WARNING: Host-key checking disabled (--host-key-checking no)." >&2
  echo "   This connection is vulnerable to man-in-the-middle attacks." >&2
  echo "   Only proceed if you explicitly understand and accept this risk." >&2
fi

# Vault-backed key: load into ssh-agent
if [[ -n "$VAULT_KEY" ]]; then
  if ! "$SCRIPT_DIR/ssh-keys.sh" restore "$VAULT_KEY"; then
    python3 - "$VAULT_KEY" <<'PY'
import json, sys
key_name = sys.argv[1]
print(json.dumps({
    "success": False, "exit_code": 98,
    "error": f"Failed to restore SSH key '{key_name}' from Vaultwarden.",
    "host": "", "command": "",
}))
PY
    exit 98
  fi
fi

# ---------------------------------------------------------------------------
# SSH password resolution (used when no key is available)
# ---------------------------------------------------------------------------
resolve_ssh_pass() {
  local vault_name="$1"
  local vault_item="ssh-${vault_name}"
  python3 - "$vault_item" <<'PY'
import json, subprocess, sys, os, shutil
vault_item = sys.argv[1]
vr_raw = os.environ.get("VAULT_RESOLVER_BIN", "/opt/data/bin/vault-resolver")
# Validate: must be absolute path or findable in PATH
if "/" in vr_raw:
    vr = os.path.abspath(vr_raw)
    if not os.path.isfile(vr) or not os.access(vr, os.X_OK):
        print(f"ERROR: VAULT_RESOLVER_BIN is not an executable file: {vr_raw}", file=sys.stderr)
        sys.exit(1)
else:
    vr = shutil.which(vr_raw)
    if vr is None:
        print(f"ERROR: VAULT_RESOLVER_BIN command not found in PATH: {vr_raw}", file=sys.stderr)
        sys.exit(1)
inp = json.dumps({"ids": [f"{vault_item}/ssh_password"]})
try:
    p = subprocess.run([vr, "resolve"], input=inp.encode(), capture_output=True, timeout=15)
    r = json.loads(p.stdout.decode())
    v = r.get("values", {}).get(f"{vault_item}/ssh_password", "")
    if v:
        print(v)
        sys.exit(0)
except Exception as e:
    print(f"ERROR: vault-resolver failed: {e}", file=sys.stderr)
sys.exit(1)
PY
}

# Resolve SSH password if no key is configured
USE_SSHPASS=0
if [[ -z "$VAULT_KEY" && -z "$KEY_PATH" ]]; then
  if [[ -n "$SSH_PASS_VAULT" || -n "${SSH_PASS:-}" || "$SSH_PASS_ASK" -eq 1 ]]; then
    # ── Gate: password-based SSH auth requires explicit environment opt-in ──
    if [[ "${SSH_EXECUTOR_ALLOW_DANGEROUS:-0}" != "1" ]]; then
      python3 - "$HOST" "$REMOTE_COMMAND" <<'PY'
import json, sys
print(json.dumps({
    "success": False, "exit_code": 98,
    "error": "SSH password auth requires SSH_EXECUTOR_ALLOW_DANGEROUS=1. Set this env var to acknowledge the elevated risk of password-based authentication, then retry.",
    "host": sys.argv[1], "command": sys.argv[2],
}))
PY
      exit 98
    fi
  fi
  if [[ -n "$SSH_PASS_VAULT" ]]; then
    SSH_PASS="$(resolve_ssh_pass "$SSH_PASS_VAULT")" || {
      python3 - "$SSH_PASS_VAULT" "$HOST" "$REMOTE_COMMAND" <<'PY'
import json, sys
print(json.dumps({
    "success": False, "exit_code": 96,
    "error": f"Failed to resolve SSH password from vault: ssh-{sys.argv[1]}/ssh_password",
    "host": sys.argv[2], "command": sys.argv[3],
}))
PY
      exit 96
    }
    USE_SSHPASS=1
  elif [[ -n "${SSH_PASS:-}" ]]; then
    SSH_PASS="$SSH_PASS"
    USE_SSHPASS=1
  elif [[ "$SSH_PASS_ASK" -eq 1 ]]; then
    python3 - "$HOST" "$REMOTE_COMMAND" <<'PY'
import json, sys
print(json.dumps({
    "success": False, "exit_code": 96,
    "error": "SSH password required. Ask the user for the password, then retry with SSH_PASS environment variable set.",
    "host": sys.argv[1], "command": sys.argv[2],
}))
PY
    exit 96
  fi
fi

# ---------------------------------------------------------------------------
# Sudo password resolution from Vaultwarden
# ---------------------------------------------------------------------------
resolve_sudo_pass() {
  local vault_name="$1"
  local vault_item="sudo-${vault_name}"
  python3 - "$vault_item" <<'PY'
import json, subprocess, sys, os, shutil
vault_item = sys.argv[1]
vr_raw = os.environ.get("VAULT_RESOLVER_BIN", "/opt/data/bin/vault-resolver")
if "/" in vr_raw:
    vr = os.path.abspath(vr_raw)
    if not os.path.isfile(vr) or not os.access(vr, os.X_OK):
        print(f"ERROR: VAULT_RESOLVER_BIN is not an executable file: {vr_raw}", file=sys.stderr)
        sys.exit(1)
else:
    vr = shutil.which(vr_raw)
    if vr is None:
        print(f"ERROR: VAULT_RESOLVER_BIN command not found in PATH: {vr_raw}", file=sys.stderr)
        sys.exit(1)
inp = json.dumps({"ids": [f"{vault_item}/sudo_password"]})
try:
    p = subprocess.run([vr, "resolve"], input=inp.encode(), capture_output=True, timeout=15)
    r = json.loads(p.stdout.decode())
    v = r.get("values", {}).get(f"{vault_item}/sudo_password", "")
    if v:
        print(v)
        sys.exit(0)
except Exception as e:
    print(f"ERROR: vault-resolver failed: {e}", file=sys.stderr)
sys.exit(1)
PY
}

if [[ "$SUDO_MODE" -eq 1 ]]; then
  # ── Gate: sudo requires explicit environment opt-in ──
  if [[ "${SSH_EXECUTOR_ALLOW_DANGEROUS:-0}" != "1" ]]; then
    python3 - "$HOST" "$REMOTE_COMMAND" <<'PY'
import json, sys
print(json.dumps({
    "success": False, "exit_code": 98,
    "error": "sudo requires SSH_EXECUTOR_ALLOW_DANGEROUS=1. Set this env var to acknowledge the elevated risk of privileged execution, then retry with --confirm-dangerous.",
    "host": sys.argv[1], "command": sys.argv[2],
}))
PY
    exit 98
  fi

  # Resolve sudo password. Priority: 1) vault  2) env var  3) ask user

  if [[ -n "$SUDO_PASS_VAULT" ]]; then
    # ── Vault path ──
    SUDO_PASS="$(resolve_sudo_pass "$SUDO_PASS_VAULT")" || {
      python3 - "$SUDO_PASS_VAULT" "$HOST" "$REMOTE_COMMAND" <<'PY'
import json, sys
print(json.dumps({
    "success": False, "exit_code": 97,
    "error": f"Failed to resolve sudo password from vault: sudo-{sys.argv[1]}/sudo_password",
    "host": sys.argv[2], "command": sys.argv[3],
}))
PY
      exit 97
    }

  elif [[ -n "${SSH_SUDO_PASS:-}" ]]; then
    # ── Env var path (SSH_SUDO_PASS) ──
    SUDO_PASS="$SSH_SUDO_PASS"

  elif [[ "$SUDO_PASS_ASK" -eq 1 ]]; then
    # ── Ask path: signal LLM to prompt user ──
    python3 - "$HOST" "$REMOTE_COMMAND" <<'PY'
import json, sys
print(json.dumps({
    "success": False, "exit_code": 97,
    "error": "Sudo password required. Ask the user for the password, then retry with SSH_SUDO_PASS environment variable set.",
    "host": sys.argv[1], "command": sys.argv[2],
}))
PY
    exit 97

  else
    # ── No password source configured ──
    python3 - "$HOST" "$REMOTE_COMMAND" <<'PY'
import json, sys
print(json.dumps({
    "success": False, "exit_code": 97,
    "error": "--sudo requires a password source: --sudo-pass-vault <name>, SSH_SUDO_PASS env var, or --sudo-pass-ask.",
    "host": sys.argv[1], "command": sys.argv[2],
}))
PY
    exit 97
  fi

  # Sudo is inherently privileged — requires explicit --confirm-dangerous flag
  # CONFIRM_DANGEROUS is NOT auto-set; the user must pass --confirm-dangerous explicitly

  # Store original command for JSON output before wrapping
  ORIGINAL_COMMAND="$REMOTE_COMMAND"

  # Wrap command: base64-encode to avoid quote-escaping nightmares.
  # echo '<pass>' | sudo -S -p '' -- sh -c "$(echo '<b64>' | base64 -d)"
  ENCODED_CMD=$(printf '%s' "$REMOTE_COMMAND" | base64 -w0)
  REMOTE_COMMAND="echo '${SUDO_PASS}' | sudo -S -p '' -- sh -c \"\$(echo '${ENCODED_CMD}' | base64 -d)\""
else
  ORIGINAL_COMMAND="$REMOTE_COMMAND"
fi

# Dangerous command check
if is_dangerous_command "$REMOTE_COMMAND" && [[ "$CONFIRM_DANGEROUS" -ne 1 ]]; then
  python3 - "$HOST" "$REMOTE_COMMAND" <<'PY'
import json, sys
host, cmd = sys.argv[1:]
print(json.dumps({
    "success": False, "exit_code": 99, "dangerous": True, "heuristic_match": True,
    "error": "Command looks mutating or destructive. Re-run with --confirm-dangerous only after explicit user approval.",
    "host": host, "command": cmd,
}))
PY
  exit 99
fi

TARGET="$HOST"
[[ -n "$USER_NAME" ]] && TARGET="$USER_NAME@$HOST"

SSH_ARGS=(
  -o ConnectTimeout="$TIMEOUT"
)
[[ -f "$CONFIG_PATH" ]] && SSH_ARGS+=( -F "$CONFIG_PATH" )
[[ -n "$PORT" ]] && SSH_ARGS+=( -p "$PORT" )
[[ -n "$KEY_PATH" ]] && SSH_ARGS+=( -i "$KEY_PATH" )
[[ -n "$HOST_KEY_CHECKING" ]] && SSH_ARGS+=( -o StrictHostKeyChecking="$HOST_KEY_CHECKING" )
# When host-key checking is enabled, ensure UserKnownHostsFile points to a real file
# (configs with UserKnownHostsFile /dev/null would otherwise nullify strict checking)
if [[ "$HOST_KEY_CHECKING" == "yes" ]]; then
  KNOWN_HOSTS_FILE="${HOME}/.ssh/known_hosts"
  # Ensure the file exists (ssh refuses to use nonexistent UserKnownHostsFile)
  touch "$KNOWN_HOSTS_FILE" 2>/dev/null || true
  SSH_ARGS+=( -o "UserKnownHostsFile=${KNOWN_HOSTS_FILE}" )
fi

if [[ "$USE_SSHPASS" -eq 1 ]]; then
  # Password auth via sshpass
  SSH_ARGS+=(
    -o BatchMode=no
    -o PreferredAuthentications=password,keyboard-interactive
    -o PasswordAuthentication=yes
    -o PubkeyAuthentication=no
  )
  SSH_BIN="sshpass"
  export SSHPASS="$SSH_PASS"
else
  # Key-based auth (default)
  SSH_ARGS+=(
    -o BatchMode=yes
    -o PreferredAuthentications=publickey
    -o PasswordAuthentication=no
  )
  SSH_BIN="ssh"
fi

# SSH multiplexing: reuse connection socket to avoid audit-log spam
# One TCP handshake per ControlPersist window instead of one per command
SSH_ARGS+=(
  -o ControlMaster=auto
  -o "ControlPath=/tmp/ssh-mux-%r@%h:%p"
  -o "ControlPersist=${CONTROL_PERSIST}s"
)

# Force PTY allocation (needed for sudo in non-interactive sessions)
[[ "$PTY_MODE" -eq 1 ]] && SSH_ARGS+=( -t -t )

RESOLVED_FILE="$(mktemp)"
STDOUT_FILE="$(mktemp)"
STDERR_FILE="$(mktemp)"
cleanup() { rm -f "$RESOLVED_FILE" "$STDOUT_FILE" "$STDERR_FILE"; }
trap cleanup EXIT INT TERM HUP

set +e
$SSH_BIN "${SSH_ARGS[@]}" -G "$TARGET" >"$RESOLVED_FILE" 2>/dev/null
RESOLVE_EXIT=$?
$SSH_BIN "${SSH_ARGS[@]}" "$TARGET" "$REMOTE_COMMAND" >"$STDOUT_FILE" 2>"$STDERR_FILE"
EXIT_CODE=$?
set -e

# Close multiplexed connection socket on demand (clean audit trail)
if [[ "$CONTROL_CLOSE" -eq 1 ]]; then
  $SSH_BIN "${SSH_ARGS[@]}" -O exit "$TARGET" >/dev/null 2>&1 || true
fi

python3 - "$EXIT_CODE" "$RESOLVE_EXIT" "$HOST" "$USER_NAME" "$PORT" "$TIMEOUT" "$HOST_KEY_CHECKING" "$ORIGINAL_COMMAND" "$RESOLVED_FILE" "$STDOUT_FILE" "$STDERR_FILE" "$SUDO_MODE" "$USE_SSHPASS" <<'PY'
import json, pathlib, sys

exit_code = int(sys.argv[1])
resolve_exit = int(sys.argv[2])
host, user_name, port, timeout, host_key_checking, remote_command, resolved_file, stdout_file, stderr_file, sudo_mode, use_sshpass = sys.argv[3:]
stdout_text = pathlib.Path(stdout_file).read_text(encoding='utf-8', errors='replace')
stderr_text = pathlib.Path(stderr_file).read_text(encoding='utf-8', errors='replace')
resolved = {}
if resolve_exit == 0:
    for raw in pathlib.Path(resolved_file).read_text(encoding='utf-8', errors='replace').splitlines():
        raw = raw.strip()
        if not raw: continue
        key, _, value = raw.partition(' ')
        key, value = key.strip(), value.strip()
        if key in {"hostname", "user", "port"} and value:
            resolved.setdefault(key, []).append(value)

result = {
    "success": exit_code == 0,
    "exit_code": exit_code,
    "dangerous": False,
    "sudo": sudo_mode == "1",
    "auth_method": "password" if use_sshpass == "1" else "publickey",
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
    "backend": "native",
}
print(json.dumps(result, ensure_ascii=False))
PY
