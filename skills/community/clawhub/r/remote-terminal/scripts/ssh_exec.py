#!/usr/bin/env python3
"""
SSH Executor - Execute commands on remote hosts via SSH

Usage:
    ssh_exec.py <host> <command> [--user USER] [--key KEY] [--password PASSWORD] [--log]

Examples:
    ssh_exec.py production "uptime"
    ssh_exec.py 192.168.1.100 "docker ps" --user admin --key ~/.ssh/id_rsa
    ssh_exec.py staging "systemctl status nginx" --log
"""

import argparse
import subprocess
import sys
import json
import os
from datetime import datetime
from pathlib import Path

LOG_FILE = Path.home() / ".qclaw" / "logs" / "remote-terminal.log"
HOSTS_FILE = Path.home() / ".qclaw" / "workspace" / "memory" / "hosts.json"

# Dangerous command patterns
DANGEROUS_PATTERNS = [
    r"\brm\s+-rf\s+/",
    r"\brm\s+-rf\s+~",
    r"\brm\s+-rf\s+\*",
    r"\bmkfs\b",
    r"\bdd\s+.*of=/dev/",
    r"\bshutdown\b",
    r"\breboot\b",
    r"\bpoweroff\b",
    r"\bhalt\b",
    r"\biptables\s+-F",
    r"\bufw\s+disable",
    r"\bDROP\s+DATABASE\b",
    r"\bTRUNCATE\s+TABLE\b",
    r">\s*/dev/sd[a-z]",
]


def load_hosts():
    """Load host configurations from hosts.json"""
    if HOSTS_FILE.exists():
        with open(HOSTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("hosts", {})
    return {}


def get_host_config(host):
    """Get host configuration by name or address"""
    hosts = load_hosts()
    if host in hosts:
        return hosts[host]
    return None


def is_dangerous(command):
    """Check if command matches dangerous patterns"""
    import re
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return True
    return False


def log_operation(host, command, output, exit_code):
    """Log the operation to file"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{host}] exit={exit_code} | {command}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)


def ssh_exec(host, command, user=None, key=None, password=None, log=False):
    """
    Execute command on remote host via SSH.
    
    Args:
        host: Hostname, IP, or alias
        command: Command to execute
        user: SSH username (optional)
        key: Path to SSH private key (optional)
        password: Password for authentication (optional)
        log: Whether to log the operation
    
    Returns:
        tuple: (stdout, stderr, exit_code)
    """
    # Check for host configuration
    host_config = get_host_config(host)
    
    if host_config:
        actual_host = host_config.get("host", host)
        user = user or host_config.get("user")
        key = key or host_config.get("key")
    else:
        actual_host = host
    
    # Build SSH command
    ssh_cmd = ["ssh"]
    
    # Add options
    ssh_cmd.extend(["-o", "StrictHostKeyChecking=accept-new"])
    ssh_cmd.extend(["-o", "ConnectTimeout=10"])
    
    if key:
        ssh_cmd.extend(["-i", os.path.expanduser(key)])
    
    # Build user@host
    if user:
        ssh_cmd.append(f"{user}@{actual_host}")
    else:
        ssh_cmd.append(actual_host)
    
    # Add command
    ssh_cmd.append(command)
    
    # Execute
    try:
        result = subprocess.run(
            ssh_cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if log:
            log_operation(host, command, result.stdout, result.returncode)
        
        return result.stdout, result.stderr, result.returncode
    
    except subprocess.TimeoutExpired:
        return "", "Connection timed out", -1
    except Exception as e:
        return "", str(e), -1


def ssh_exec_with_password(host, command, user, password, log=False):
    """Execute SSH command with password authentication using sshpass"""
    import getpass
    
    if not password:
        password = getpass.getpass(f"Password for {user}@{host}: ")
    
    ssh_cmd = [
        "sshpass", "-p", password,
        "ssh", "-o", "StrictHostKeyChecking=accept-new",
        "-o", "ConnectTimeout=10",
        f"{user}@{host}",
        command
    ]
    
    try:
        result = subprocess.run(
            ssh_cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if log:
            log_operation(host, command, result.stdout, result.returncode)
        
        return result.stdout, result.stderr, result.returncode
    
    except FileNotFoundError:
        return "", "sshpass not installed. Install with: apt install sshpass", -1
    except Exception as e:
        return "", str(e), -1


def main():
    parser = argparse.ArgumentParser(description="Execute commands on remote hosts via SSH")
    parser.add_argument("host", help="Hostname, IP, or alias")
    parser.add_argument("command", help="Command to execute")
    parser.add_argument("--user", "-u", help="SSH username")
    parser.add_argument("--key", "-i", help="Path to SSH private key")
    parser.add_argument("--password", "-p", help="Password for authentication")
    parser.add_argument("--log", "-l", action="store_true", help="Log the operation")
    parser.add_argument("--force", "-f", action="store_true", help="Skip danger check")
    
    args = parser.parse_args()
    
    # Check for dangerous commands
    if not args.force and is_dangerous(args.command):
        print("⚠️  DANGEROUS COMMAND DETECTED")
        print(f"   Command: {args.command}")
        print("   This operation could cause irreversible damage.")
        response = input("   Proceed? (yes/no): ")
        if response.lower() != "yes":
            print("   Operation cancelled.")
            sys.exit(1)
    
    # Execute
    if args.password:
        stdout, stderr, exit_code = ssh_exec_with_password(
            args.host, args.command, args.user or "root", args.password, args.log
        )
    else:
        stdout, stderr, exit_code = ssh_exec(
            args.host, args.command, args.user, args.key, None, args.log
        )
    
    # Output
    if stdout:
        print(stdout)
    if stderr:
        print(f"[stderr] {stderr}", file=sys.stderr)
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
