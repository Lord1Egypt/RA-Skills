#!/usr/bin/env bash
# =============================================================================
# ssh-run.sh — Remote SSH command executor with safety guardrails
#
# Provenance:
#   Part of the ssh-executor skill for OpenClaw.
#   Source is bundled and fully reviewable.
#
# Security model:
#   - This script has broad remote-shell authority. Use only for
#     user-requested hosts with user-approved commands.
#   - The dangerous-command heuristic is best-effort and NOT exhaustive.
#   - Host validation should happen BEFORE calling this script;
#     confirm the target with the user first.
#
# Backend:
#   - If openssh-client (ssh/ssh-add/ssh-agent) are available, uses the
#     native ssh binary via the traditional approach.
#   - Otherwise, falls back to a Python/Paramiko implementation that
#     supports vault-backed keys natively (no agent needed).
# =============================================================================

set -euo pipefail
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

Notes:
  - Key-based auth by default. Password auth available via --ssh-pass-vault, SSH_PASS, or --ssh-pass-ask (requires sshpass).
  - Password-based auth is a security tradeoff — prefer --vault-key or --key whenever possible.
  - SSH keys are never sent to stdout, logs, or chat. However, without ssh-agent, decrypted key material is briefly written to a temp file (see ssh-keys.sh header). Use ssh-agent to keep keys in memory only.
  - Use --vault-key <name> to load a private key from Vaultwarden.
  - If --host is an SSH alias, omit --user/--port/--key and let ssh config resolve them.
  - JSON is printed to stdout with success, exit_code, stdout, stderr, and resolution metadata.
  - Automatically selects backend: openssh-client (native) or Python+Paramiko (fallback).
  - Destructive commands and sudo require --confirm-dangerous for explicit user approval.
EOF
}

# ---------------------------------------------------------------------------
# Backend detection
# ---------------------------------------------------------------------------
has_ssh_client() {
  command -v ssh >/dev/null 2>&1 && command -v ssh-add >/dev/null 2>&1
}

# ---------------------------------------------------------------------------
# Native openssh-client backend (original impl, enhanced with --vault-key)
# ---------------------------------------------------------------------------
run_native() {
  local args=("$@")
  exec /usr/bin/env bash "$SCRIPT_DIR/ssh-run-native.sh" "${args[@]}"
}

# ---------------------------------------------------------------------------
# Paramiko Python backend (no openssh-client needed; vault keys built-in)
# ---------------------------------------------------------------------------
run_python() {
  # Convert shell flags to Python flags
  local HOST=""
  local USER=""
  local PORT=""
  local KEY=""
  local VAULT_KEY=""
  local TIMEOUT="30"
  local CONFIRM_DANGEROUS=0
  local LIST_ALIASES=0
  local args=("$@")

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --host) HOST="${2:-}"; shift 2 ;;
      --user) USER="${2:-}"; shift 2 ;;
      --port) PORT="${2:-}"; shift 2 ;;
      --key) KEY="${2:-}"; shift 2 ;;
      --vault-key) VAULT_KEY="${2:-}"; shift 2 ;;
      --timeout) TIMEOUT="${2:-}"; shift 2 ;;
      --config) shift 2 ;; # ignored in Python backend
      --host-key-checking) HOST_KEY_CHECKING="${2:-yes}"; shift 2 ;;
      --control-persist) shift 2 ;; # pass-through (used by native backend)
      --control-close) shift ;; # pass-through (used by native backend)
      --pty) shift ;; # pass-through (used by native backend)
      --sudo) shift ;; # pass-through (used by native backend)
      --sudo-pass-vault) shift 2 ;; # pass-through (used by native backend)
      --sudo-pass-ask) shift ;; # pass-through (used by native backend)
      --ssh-pass-vault) shift 2 ;; # pass-through (used by native backend)
      --ssh-pass-ask) shift ;; # pass-through (used by native backend)
      --confirm-dangerous) CONFIRM_DANGEROUS=1; shift ;;
      --list-aliases) LIST_ALIASES=1; shift ;;
      --help|-h) usage; exit 0 ;;
      --) shift; break ;;
      *) echo "Unknown argument: $1" >&2; usage >&2; exit 2 ;;
    esac
  done

  if [[ "$LIST_ALIASES" -eq 1 ]]; then
    echo "[]"
    exit 0
  fi

  local CMD="$*"
  if [[ -z "$HOST" || -z "$CMD" ]]; then
    usage >&2
    exit 2
  fi

  # Resolve SSH config alias (HostName, Port, User)
  local resolved_host="$HOST"
  local resolved_port="${PORT:-22}"
  local resolved_user="$USER"
  local config_path="${HOME}/.ssh/config"
  if [[ -f "$config_path" ]]; then
    eval "$(python3 - "$HOST" "$resolved_port" "$config_path" <<'PY'
import sys
target = sys.argv[1]
port = sys.argv[2]
cfg_path = sys.argv[3]

# Parse all host sections, preferring specific match over wildcard
hostname = ""
user = ""
matched = False
wildcard = False
with open(cfg_path) as f:
    for line in f:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.lower().startswith("host "):
            parts = stripped.split()
            names = parts[1:]
            if target in names:
                matched = True
                wildcard = False
            elif "*" in names and not matched:
                wildcard = True
            else:
                matched = False
                wildcard = False
            continue
        if (matched or wildcard) and stripped:
            key, _, val = stripped.partition(" ")
            key = key.lower()
            val = val.strip()
            if key == "hostname":
                hostname = val
            elif key == "port" and port in (["22", ""]):
                port = val
            elif key == "user" and not user:
                user = val
if hostname:
    target = hostname
if user:
    print(f'RESOLVED_USER="{user}"')
print(f'RESOLVED_HOST="{target}"')
print(f'RESOLVED_PORT="{port}"')
PY
    )"
  fi

  local py_args=(
    "--host" "$RESOLVED_HOST"
    "--port" "${RESOLVED_PORT:-22}"
    "--timeout" "$TIMEOUT"
  )
  [[ -n "${RESOLVED_USER:-$USER}" ]] && py_args+=( "--user" "${RESOLVED_USER:-$USER}" )
  [[ -n "$KEY" ]] && py_args+=( "--key" "$KEY" )
  [[ -n "$VAULT_KEY" ]] && py_args+=( "--vault-key" "$VAULT_KEY" )
  [[ -n "${HOST_KEY_CHECKING:-}" ]] && py_args+=( "--host-key-checking" "$HOST_KEY_CHECKING" )
  [[ "$CONFIRM_DANGEROUS" -eq 1 ]] && py_args+=( "--confirm-dangerous" )

  exec python3 "$SCRIPT_DIR/ssh-client.py" "${py_args[@]}" "$CMD"
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

for arg in "$@"; do
  [[ "$arg" == "--help" || "$arg" == "-h" ]] && { usage; exit 0; }
done

if [[ "$*" == *--list-aliases* ]]; then
  if has_ssh_client; then
    run_native "$@"
  else
    echo "[]"
    exit 0
  fi
  exit 0
fi

# Choose backend
# Native backend now handles vault keys via ssh-agent (ssh-keys.sh restore).
# Fall back to Python only when openssh-client is unavailable.
if has_ssh_client; then
  run_native "$@"
else
  run_python "$@"
fi
