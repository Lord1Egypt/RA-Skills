#!/usr/bin/env python3
"""
ssh-client.py — SSH client using Paramiko with Vaultwarden-backed keys

Replaces the need for openssh-client binaries (ssh-agent, ssh-add, ssh-keygen).
Uses Paramiko for SSH connections + vault-resolver for private key retrieval.

Security model:
  - Private keys are resolved from Vaultwarden and held only in memory (not on disk).
  - Keys are never logged, printed, or written to any file.
  - Vault credentials never touch the SSH connection.
  - Host keys are verified by default (RejectPolicy). Unknown hosts are rejected
    unless --host-key-checking no is explicitly passed by the user.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from base64 import b64decode
from pathlib import Path
from typing import Optional

# Add paramiko from local install
sys.path.insert(0, os.path.expanduser("~/.openclaw/workspace/.ssh-pylib"))

import paramiko
import paramiko.rsakey
import paramiko.ed25519key
import paramiko.ecdsakey


VAULT_RESOLVER_DEFAULT = "/opt/data/bin/vault-resolver"

def _resolve_vault_bin() -> str:
    """Validate and resolve the vault binary path. Rejects non-executable or missing binaries."""
    import shutil
    vr = os.environ.get("VAULT_RESOLVER_BIN", VAULT_RESOLVER_DEFAULT)
    if "/" in vr:
        p = os.path.abspath(vr)
        if not os.path.isfile(p) or not os.access(p, os.X_OK):
            raise FileNotFoundError(f"VAULT_RESOLVER_BIN is not an executable file: {vr}")
        return p
    p = shutil.which(vr)
    if p is None:
        raise FileNotFoundError(f"VAULT_RESOLVER_BIN command not found in PATH: {vr}")
    return p
DANGEROUS_HEURISTICS = [
    r"(?:^|[;&|\s])(?:sudo|rm(?!\w)|mv\s|cp\s|chmod\s|chown\s|reboot(?!\w)|shutdown(?!\w)|poweroff(?!\w)|halt(?!\w)|init\s)",
    r"systemctl\s+(?:restart|stop|disable|start|reload|enable)",
    r"(?:apt[\s-]|apt-get[\s-]|dnf[\s-]|yum[\s-]|apk[\s-]|pacman[\s-]|dpkg\s|rpm\s+(?!-q)(?!-qa)(?!-qi)(?!-ql))",
    r"docker\s+(?:compose\s+down|rm|kill|stop|system\s+prune)",
    r"kubectl\s+delete",
    r"sed\s+-i",
    r"ip\s+(?:link\s+(?:set|down|delete)|addr\s+(?:add|del)|route\s+(?:add|del|replace))",
    r"(?:curl|wget)\s+.*(?:[|>])",
    r"(?:sh\s+-c|bash\s+-c)\s",
    r"chpasswd\s|passwd\s|usermod\s|groupmod\s|useradd\s|userdel\s",
    r"(?:>>?\s+\S+(?:\s|$)|>\||:>|echo\s+.*[>]|printf\s+.*[>])",
    r"(?:tee\s|truncate\s|dd\s|mkfs(?!\.\w+)|mkfs\.|fdisk\s|pvcreate\s|vgremove\s|lvremove\s)",
    r"(?:iptables\s|ufw\s|firewall-cmd\s|nmcli\s)",
    r"(?:eval\s)",
]


def is_dangerous(command: str) -> bool:
    """Check command against heuristic patterns."""
    cmd_lower = command.lower()
    for pattern in DANGEROUS_HEURISTICS:
        if re.search(pattern, cmd_lower):
            return True
    return False


def resolve_vault_key(key_name: str) -> tuple[Optional[str], Optional[str]]:
    """
    Resolve an SSH private key from Vaultwarden.
    Returns (private_key_pem, public_key_pem) or (None, None) if not found.
    """
    vault_key = f"ssh-{key_name}"
    input_data = json.dumps({
        "ids": [f"{vault_key}/ssh_private_key", f"{vault_key}/ssh_public_key"]
    })

    try:
        vr = _resolve_vault_bin()
        proc = subprocess.run(
            [vr, "resolve"],
            input=input_data.encode(),
            capture_output=True,
            timeout=25,
        )
        result = json.loads(proc.stdout.decode())
        priv_b64 = result.get("values", {}).get(f"{vault_key}/ssh_private_key")
        if not priv_b64:
            return None, None
        priv_pem = b64decode(priv_b64).decode("utf-8", errors="replace")

        pub_b64 = result.get("values", {}).get(f"{vault_key}/ssh_public_key")
        pub_pem = b64decode(pub_b64).decode("utf-8", errors="replace") if pub_b64 else None

        return priv_pem, pub_pem
    except Exception as e:
        print(
            json.dumps(
                {
                    "success": False,
                    "exit_code": 98,
                    "error": f"Failed to resolve vault key '{key_name}': {e}",
                    "host": "",
                    "command": "",
                }
            ),
            file=sys.stderr,
        )
        return None, None


def load_pkey_from_pem(pem_str: str, password: Optional[str] = None) -> paramiko.PKey:
    """Load a Paramiko key object from a PEM string (in-memory, no temp file)."""
    errors = []

    for key_class, name in [
        (paramiko.RSAKey, "RSA"),
        (paramiko.Ed25519Key, "Ed25519"),
        (paramiko.ECDSAKey, "ECDSA"),
    ]:
        try:
            from io import StringIO

            return key_class.from_private_key(StringIO(pem_str), password=password)
        except paramiko.SSHException as e:
            errors.append(f"{name}: {e}")
            continue
        except Exception as e:
            errors.append(f"{name}: {e}")
            continue

    raise ValueError(f"Could not parse private key. Tried: {'; '.join(errors)}")


def main():
    parser = argparse.ArgumentParser(
        description="SSH client with Vaultwarden-backed keys (Paramiko)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--host", required=True, help="Hostname or IP")
    parser.add_argument("--user", default=None, help="SSH username")
    parser.add_argument("--port", type=int, default=22, help="SSH port")
    parser.add_argument("--key", default=None, help="Path to private key file")
    parser.add_argument("--vault-key", default=None, help="Vaultwarden key name")
    parser.add_argument("--timeout", type=int, default=30, help="Connection timeout")
    parser.add_argument(
        "--confirm-dangerous",
        action="store_true",
        help="Allow dangerous commands",
    )
    parser.add_argument(
        "--host-key-checking",
        default="yes",
        choices=["yes", "no"],
        help="Host key verification: 'yes' (default, strict) or 'no' (auto-accept, unsafe)",
    )
    parser.add_argument("command", nargs=argparse.REMAINDER, help="Remote command")

    args = parser.parse_args()

    # Validate command
    if not args.command:
        print(json.dumps({
            "success": False, "exit_code": 99,
            "error": "No command specified",
            "host": args.host, "command": "",
        }))
        sys.exit(2)

    remote_command = " ".join(args.command) if isinstance(args.command, list) else args.command

    # Dangerous command check
    if is_dangerous(remote_command) and not args.confirm_dangerous:
        print(json.dumps({
            "success": False,
            "exit_code": 99,
            "dangerous": True,
            "heuristic_match": True,
            "error": "Command looks mutating or destructive. Re-run with --confirm-dangerous only after explicit user approval.",
            "host": args.host,
            "command": remote_command,
        }))
        sys.exit(99)

    # Resolve key
    pkey = None
    if args.vault_key:
        priv_pem, pub_pem = resolve_vault_key(args.vault_key)
        if priv_pem is None:
            print(json.dumps({
                "success": False,
                "exit_code": 98,
                "error": f"SSH key '{args.vault_key}' not found in Vaultwarden. Use: ssh-keys.sh store {args.vault_key} <path> first.",
                "host": args.host,
                "command": remote_command,
            }))
            sys.exit(98)
        try:
            pkey = load_pkey_from_pem(priv_pem)
        except ValueError as e:
            print(json.dumps({
                "success": False,
                "exit_code": 98,
                "error": f"Failed to parse vault key: {e}",
                "host": args.host,
                "command": remote_command,
            }))
            sys.exit(98)
    elif args.key:
        key_path = Path(args.key).expanduser()
        if not key_path.exists():
            print(json.dumps({
                "success": False, "exit_code": 98,
                "error": f"Key file not found: {args.key}",
                "host": args.host, "command": remote_command,
            }))
            sys.exit(98)
        pkey = paramiko.RSAKey.from_private_key_file(str(key_path))

    # Connect with host-key policy matching --host-key-checking
    client = paramiko.SSHClient()
    if args.host_key_checking == "no":
        # Explicitly unsafe — user has opted in
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    else:
        # Default: reject unknown hosts (strict), backed by real known_hosts
        client.set_missing_host_key_policy(paramiko.RejectPolicy())
        # Load system + user known_hosts so RejectPolicy can actually verify
        known_hosts_path = os.path.expanduser("~/.ssh/known_hosts")
        if os.path.isfile(known_hosts_path):
            client.load_host_keys(known_hosts_path)
        system_known = "/etc/ssh/ssh_known_hosts"
        if os.path.isfile(system_known):
            client.load_host_keys(system_known)

    try:
        connect_kwargs = {
            "hostname": args.host,
            "port": args.port,
            "username": args.user or os.environ.get("USER", "root"),
            "timeout": args.timeout,
        }
        if pkey:
            connect_kwargs["pkey"] = pkey

        client.connect(**connect_kwargs)

        # Execute
        stdin, stdout, stderr = client.exec_command(
            remote_command,
            timeout=args.timeout,
        )

        stdout_text = stdout.read().decode("utf-8", errors="replace")
        stderr_text = stderr.read().decode("utf-8", errors="replace")
        exit_code = stdout.channel.recv_exit_status()

        # Output JSON
        print(json.dumps({
            "success": exit_code == 0,
            "exit_code": exit_code,
            "dangerous": False,
            "host": args.host,
            "user": args.user,
            "port": args.port,
            "timeout": args.timeout,
            "command": remote_command,
            "stdout": stdout_text,
            "stderr": stderr_text,
        }))

    except paramiko.AuthenticationException as e:
        print(json.dumps({
            "success": False, "exit_code": 1,
            "error": f"Authentication failed: {e}",
            "host": args.host, "command": remote_command,
        }))
        sys.exit(1)
    except paramiko.SSHException as e:
        print(json.dumps({
            "success": False, "exit_code": 1,
            "error": f"SSH error: {e}",
            "host": args.host, "command": remote_command,
        }))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            "success": False, "exit_code": 1,
            "error": str(e),
            "host": args.host, "command": remote_command,
        }))
        sys.exit(1)
    finally:
        client.close()


if __name__ == "__main__":
    main()
