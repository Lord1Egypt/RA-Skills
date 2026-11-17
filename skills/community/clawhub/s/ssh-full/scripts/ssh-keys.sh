#!/usr/bin/env bash
# =============================================================================
# ssh-keys.sh — SSH key management via Vaultwarden
#
# Part of the ssh-executor skill for OpenClaw.
#
# Security model:
#   - Private keys are resolved from Vaultwarden and loaded into ssh-agent
#     (or, as fallback, written to a temp file that is cleaned on trap EXIT).
#     Without ssh-agent, a temp file IS created on disk — start ssh-agent to
#     avoid this. If killed with SIGKILL, the temp file persists (trap cannot
#     catch it). Prefer ssh-agent whenever possible.
#
# Usage:
#   ssh-keys.sh store <key-name> <path>         — Store a local key in the vault
#   ssh-keys.sh restore <key-name>              — Load a vault key into SSH agent
#   ssh-keys.sh restore-to-file <name> <path>   — Write vault key to a file
#   ssh-keys.sh list                            — List vault SSH keys
#   ssh-keys.sh agent-status                    — Show loaded agent keys
#   ssh-keys.sh cleanup [--force]               — List/remove stale temp key files
# =============================================================================
set -euo pipefail

VAULT_RESOLVER="${VAULT_RESOLVER_BIN:-/opt/data/bin/vault-resolver}"
ACTION="${1:-help}"

usage() {
  cat <<'EOF'
Usage:
  ssh-keys.sh store <key-name> <path>         — Store a private key in Vaultwarden
  ssh-keys.sh restore <key-name>              — Load a vault key into SSH agent
  ssh-keys.sh restore-to-file <name> <path>   — Write vault key to a specific file
  ssh-keys.sh list                            — List vault SSH keys
  ssh-keys.sh agent-status                    — Show loaded agent keys
  ssh-keys.sh cleanup                         — List stale temp key files
  ssh-keys.sh cleanup --force                 — Remove stale temp key files (shred)

Examples:
  ssh-keys.sh store prod-server ~/.ssh/id_rsa_prod
  ssh-keys.sh restore prod-server
  ssh-keys.sh restore-to-file prod-server ~/.ssh/id_rsa
  ssh-keys.sh agent-status

Notes:
  - store: reads the file, base64-encodes, writes to vault as ssh-<name>/ssh_private_key
  - Private keys are NEVER written to stdout, logs, or chat.
EOF
}

sanitize_name() {
  echo "$1" | sed 's/[^a-zA-Z0-9_-]/_/g'
}

# Resolve private key base64 from Vaultwarden. Prints base64 to stdout.
# Returns 0 on success, 1 on failure.
resolve_privkey_b64() {
  local safe_name="$1"
  local vault_item="ssh-$safe_name"
  python3 - "$safe_name" "$vault_item" <<'PY'
import json, subprocess, sys
safe = sys.argv[1]
vault = sys.argv[2]
va = "/opt/data/bin/vault-resolver"
for key in [f"{vault}/ssh_private_key", f"ssh-{safe}/ssh_private_key"]:
    inp = json.dumps({"ids": [key]})
    try:
        p = subprocess.run([va, "resolve"], input=inp.encode(), capture_output=True, timeout=15)
        r = json.loads(p.stdout.decode())
        v = r.get("values", {}).get(key, "")
        if v:
            print(v)
            sys.exit(0)
    except Exception:
        pass
print("")
sys.exit(1)
PY
}

# --- Store ---

cmd_store() {
  local key_name="$1"
  local key_path="$2"
  local safe_name
  safe_name="$(sanitize_name "$key_name")"
  local vault_item="ssh-$safe_name"

  if [[ ! -f "$key_path" ]]; then
    echo "ERROR: Key file not found: $key_path" >&2
    exit 1
  fi

  local priv_b64 pub_b64
  priv_b64="$(base64 -w0 < "$key_path")"
  local pub_path="${key_path}.pub"
  if [[ -f "$pub_path" ]]; then
    pub_b64="$(base64 -w0 < "$pub_path")"
  else
    pub_b64=""
  fi

  echo "Storing SSH key '$safe_name' in Vaultwarden..."
  if [[ -n "$pub_b64" ]]; then
    "$VAULT_RESOLVER" write "$vault_item" \
      ssh_private_key="$priv_b64" \
      ssh_public_key="$pub_b64" \
      description="SSH key: $safe_name (stored via ssh-keys.sh)"
  else
    "$VAULT_RESOLVER" write "$vault_item" \
      ssh_private_key="$priv_b64" \
      description="SSH key: $safe_name (no public key file found)"
  fi

  echo "✓ SSH key '$safe_name' stored in vault."
  echo "  Vault item: $vault_item"
  echo "  You can now safely delete the local file: rm $key_path"
}

# --- Restore (to agent) ---

cmd_restore() {
  local key_name="$1"
  local safe_name
  safe_name="$(sanitize_name "$key_name")"

  echo "Retrieving SSH key '$safe_name' from Vaultwarden..." >&2

  local priv_b64
  priv_b64="$(resolve_privkey_b64 "$safe_name")" || {
    echo "ERROR: SSH key '$safe_name' not found in vault." >&2
    echo "  Try: ssh-keys.sh list" >&2
    exit 1
  }

  local tmp_key
  # Prefer /dev/shm (RAM-backed tmpfs), fallback to /tmp if unavailable
  if [[ -d /dev/shm ]] && [[ -w /dev/shm ]]; then
    tmp_key="$(mktemp /dev/shm/ssh-vault-XXXXXXXX)"
  else
    tmp_key="$(mktemp /tmp/ssh-vault-XXXXXXXX)"
  fi
  # Safety net: rm on any exit (shred happens explicitly in success/error paths)
  trap 'rm -f "${tmp_key:-}"' EXIT INT TERM HUP
  chmod 600 "$tmp_key"
  echo "$priv_b64" | base64 -d > "$tmp_key"

  # Try ssh-agent (openssh-client). If unavailable, print path and exit.
  if command -v ssh-add >/dev/null 2>&1; then
    if command -v ssh-keygen >/dev/null 2>&1; then
      ssh-keygen -l -f "$tmp_key" &>/dev/null || {
        shred -u "$tmp_key" 2>/dev/null; rm -f "$tmp_key"
        echo "ERROR: Retrieved data is not a valid SSH private key." >&2
        exit 1
      }
    fi

    if ssh-add "$tmp_key" 2>/dev/null; then
      local fingerprint=""
      command -v ssh-keygen >/dev/null 2>&1 && \
        fingerprint="$(ssh-keygen -lf "$tmp_key" 2>/dev/null | awk '{print $2}')"
      shred -u "$tmp_key" 2>/dev/null; rm -f "$tmp_key"
      echo "✓ SSH key '$safe_name' loaded into ssh-agent." >&2
      [[ -n "$fingerprint" ]] && echo "  Fingerprint: $fingerprint" >&2
      echo "  (temp key file securely wiped)" >&2
      exit 0
    fi
  fi

  # Fallback: no agent — leave temp file for Python backend
  echo "⚠️  SECURITY WARNING: ssh-agent not available." >&2
  echo "   Private key material written to temp file: $tmp_key" >&2
  echo "   This file WILL PERSIST if this process is interrupted (kill -9, crash)." >&2
  echo "   Start ssh-agent to avoid this fallback: eval \"\$(ssh-agent -s)\"" >&2
}

# --- Restore to file ---

cmd_restore_to_file() {
  local key_name="$1"
  local output_path="$2"
  local safe_name
  safe_name="$(sanitize_name "$key_name")"

  # Validate output path — reject system-critical directories
  local abs_path
  abs_path="$(realpath -m "$output_path" 2>/dev/null || echo "$output_path")"
  for forbidden in /etc /boot /sys /proc /dev /run; do
    if [[ "$abs_path" == "$forbidden" || "$abs_path" == "$forbidden/"* ]]; then
      echo "ERROR: Refusing to write private key to system directory: $output_path" >&2
      echo "       Use a path under /tmp/ or your home directory." >&2
      exit 1
    fi
  done

  # Warn if not in memory-backed filesystem
  if [[ "$abs_path" != /tmp/* && "$abs_path" != /dev/shm/* ]]; then
    echo "⚠️  WARNING: Output path is not in /tmp or /dev/shm (RAM-backed)." >&2
    echo "   The key file WILL persist across reboots at: $output_path" >&2
    echo "   Prefer /tmp/ for temporary key material." >&2
    echo "" >&2
  fi

  echo "⚠️  SECURITY WARNING: Writing decrypted private key to disk at $output_path" >&2
  echo "   This is a LAST RESORT. Prefer ssh-agent (cmd_restore) whenever possible." >&2
  echo "   The key file may persist if this process is interrupted." >&2
  echo "" >&2
  echo "Restoring SSH key '$safe_name' to $output_path..." >&2

  local priv_b64
  priv_b64="$(resolve_privkey_b64 "$safe_name")" || {
    echo "ERROR: SSH key '$safe_name' not found in vault." >&2
    exit 1
  }

  mkdir -p "$(dirname "$output_path")"
  echo "$priv_b64" | base64 -d > "$output_path"
  chmod 600 "$output_path"

  echo "✓ SSH key '$safe_name' written to $output_path"
}

# --- List ---

cmd_list() {
  echo "SSH keys stored in Vaultwarden:"
  echo ""
  echo "  (To discover keys, look for vault items named ssh-*)"
  echo ""
  echo "  To restore: ssh-keys.sh restore <key-name>"
  echo "  (e.g., vault item 'ssh-prod-server' → key name 'prod-server')"
}

# --- Cleanup ---

cmd_cleanup() {
  local force="${1:-}"
  local found=0

  echo "Scanning for stale temp key files..." >&2
  echo "" >&2

  for pat in "/dev/shm/ssh-vault-"* "/tmp/ssh-vault-"*; do
    [[ -f "$pat" ]] || continue
    found=$((found + 1))
    local age
    age="$(stat -c '%Y' "$pat" 2>/dev/null || echo '0')"
    local now
    now="$(date +%s)"
    local seconds_ago=$((now - age))
    local pretty_age
    if [[ $seconds_ago -lt 60 ]]; then
      pretty_age="${seconds_ago}s ago"
    elif [[ $seconds_ago -lt 3600 ]]; then
      pretty_age="$((seconds_ago / 60))m ago"
    elif [[ $seconds_ago -lt 86400 ]]; then
      pretty_age="$((seconds_ago / 3600))h ago"
    else
      pretty_age="$((seconds_ago / 86400))d ago"
    fi
    local size
    size="$(stat -c '%s' "$pat" 2>/dev/null || echo '?')"

    if [[ "$force" == "--force" ]]; then
      shred -u "$pat" 2>/dev/null && rm -f "$pat"
      echo "  ✓ Removed: $pat ($pretty_age, ${size}B)" >&2
    else
      echo "  $pat  ($pretty_age, ${size}B)" >&2
    fi
  done

  if [[ $found -eq 0 ]]; then
    echo "  No stale temp key files found." >&2
  elif [[ "$force" != "--force" ]]; then
    echo "" >&2
    echo "  Run 'ssh-keys.sh cleanup --force' to remove them." >&2
  fi
}

# --- Agent Status ---

cmd_agent_status() {
  if [[ -z "${SSH_AUTH_SOCK:-}" ]]; then
    echo "SSH agent is not running."
    echo "The Python/Paramiko backend does not need an agent — use --vault-key directly."
    exit 0
  fi

  echo "SSH agent socket: $SSH_AUTH_SOCK"
  echo ""
  if command -v ssh-add >/dev/null 2>&1; then
    ssh-add -l 2>&1 || echo "(no keys loaded)"
  else
    echo "(ssh-add not available)"
  fi
}

# --- Dispatch ---

case "$ACTION" in
  store)
    if [[ $# -lt 3 ]]; then
      echo "Usage: ssh-keys.sh store <key-name> <path>" >&2
      exit 2
    fi
    cmd_store "$2" "$3"
    ;;
  restore)
    if [[ $# -lt 2 ]]; then
      echo "Usage: ssh-keys.sh restore <key-name>" >&2
      exit 2
    fi
    cmd_restore "$2"
    ;;
  restore-to-file)
    if [[ $# -lt 3 ]]; then
      echo "Usage: ssh-keys.sh restore-to-file <key-name> <path>" >&2
      exit 2
    fi
    cmd_restore_to_file "$2" "$3"
    ;;
  list)
    cmd_list
    ;;
  agent-status)
    cmd_agent_status
    ;;
  cleanup)
    cmd_cleanup "${2:-}"
    ;;
  help|--help|-h)
    usage
    exit 0
    ;;
  *)
    echo "Unknown command: $ACTION" >&2
    usage >&2
    exit 2
    ;;
esac
