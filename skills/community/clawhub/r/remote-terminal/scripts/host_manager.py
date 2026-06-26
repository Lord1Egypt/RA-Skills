#!/usr/bin/env python3
"""
Host Manager - Manage remote host configurations

Usage:
    host_manager.py list
    host_manager.py add <name> <host> [--user USER] [--key KEY] [--tags TAGS]
    host_manager.py remove <name>
    host_manager.py show <name>
    host_manager.py test <name>

Examples:
    host_manager.py list
    host_manager.py add production 192.168.1.100 --user admin --key ~/.ssh/id_rsa --tags web,critical
    host_manager.py show production
    host_manager.py test production
    host_manager.py remove staging
"""

import argparse
import json
import sys
import subprocess
from pathlib import Path

HOSTS_FILE = Path.home() / ".qclaw" / "workspace" / "memory" / "hosts.json"


def load_hosts():
    """Load hosts configuration from file"""
    if HOSTS_FILE.exists():
        with open(HOSTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"hosts": {}}


def save_hosts(data):
    """Save hosts configuration to file"""
    HOSTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(HOSTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def list_hosts():
    """List all configured hosts"""
    data = load_hosts()
    hosts = data.get("hosts", {})
    
    if not hosts:
        print("No hosts configured.")
        print(f"\nConfig file: {HOSTS_FILE}")
        return
    
    print("Configured Hosts:")
    print("=" * 60)
    for name, config in hosts.items():
        host = config.get("host", "N/A")
        user = config.get("user", "N/A")
        method = config.get("method", "unknown")
        tags = ", ".join(config.get("tags", []))
        print(f"\n  {name}")
        print(f"    Host: {host}")
        print(f"    User: {user}")
        print(f"    Auth: {method}")
        if tags:
            print(f"    Tags: {tags}")


def add_host(name, host, user=None, key=None, password=None, tags=None):
    """Add or update a host configuration"""
    data = load_hosts()
    
    config = {
        "host": host,
        "method": "password" if password else ("ssh-key" if key else "ssh-config"),
    }
    
    if user:
        config["user"] = user
    if key:
        config["key"] = key
    if password:
        config["password"] = password  # Note: storing passwords is not recommended
    if tags:
        config["tags"] = [t.strip() for t in tags.split(",")]
    
    data["hosts"][name] = config
    save_hosts(data)
    
    print(f"✓ Host '{name}' added/updated successfully.")
    print(f"  Host: {host}")
    if user:
        print(f"  User: {user}")
    print(f"  Auth: {config['method']}")


def remove_host(name):
    """Remove a host configuration"""
    data = load_hosts()
    hosts = data.get("hosts", {})
    
    if name not in hosts:
        print(f"Error: Host '{name}' not found.")
        return False
    
    del data["hosts"][name]
    save_hosts(data)
    print(f"✓ Host '{name}' removed.")
    return True


def show_host(name):
    """Show details of a specific host"""
    data = load_hosts()
    hosts = data.get("hosts", {})
    
    if name not in hosts:
        print(f"Error: Host '{name}' not found.")
        return
    
    config = hosts[name]
    print(f"Host: {name}")
    print("=" * 40)
    for key, value in config.items():
        if key == "tags":
            value = ", ".join(value) if value else "none"
        print(f"  {key}: {value}")


def test_host(name):
    """Test connection to a host"""
    data = load_hosts()
    hosts = data.get("hosts", {})
    
    if name not in hosts:
        print(f"Error: Host '{name}' not found.")
        return False
    
    config = hosts[name]
    host = config.get("host", name)
    user = config.get("user", "")
    key = config.get("key")
    
    # Build SSH command
    ssh_cmd = ["ssh", "-o", "ConnectTimeout=5", "-o", "BatchMode=yes"]
    
    if key:
        ssh_cmd.extend(["-i", key])
    
    if user:
        ssh_cmd.append(f"{user}@{host}")
    else:
        ssh_cmd.append(host)
    
    ssh_cmd.append("echo 'Connection successful'")
    
    print(f"Testing connection to {name} ({host})...")
    
    try:
        result = subprocess.run(
            ssh_cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print(f"✓ Connection successful!")
            return True
        else:
            print(f"✗ Connection failed: {result.stderr.strip()}")
            return False
    
    except subprocess.TimeoutExpired:
        print("✗ Connection timed out.")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Manage remote host configurations")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # List command
    subparsers.add_parser("list", help="List all hosts")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add or update a host")
    add_parser.add_argument("name", help="Host name/alias")
    add_parser.add_argument("host", help="Hostname or IP address")
    add_parser.add_argument("--user", "-u", help="SSH username")
    add_parser.add_argument("--key", "-i", help="Path to SSH private key")
    add_parser.add_argument("--password", "-p", help="Password (not recommended)")
    add_parser.add_argument("--tags", "-t", help="Comma-separated tags")
    
    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a host")
    remove_parser.add_argument("name", help="Host name to remove")
    
    # Show command
    show_parser = subparsers.add_parser("show", help="Show host details")
    show_parser.add_argument("name", help="Host name")
    
    # Test command
    test_parser = subparsers.add_parser("test", help="Test connection to host")
    test_parser.add_argument("name", help="Host name")
    
    args = parser.parse_args()
    
    if args.command == "list":
        list_hosts()
    elif args.command == "add":
        add_host(args.name, args.host, args.user, args.key, args.password, args.tags)
    elif args.command == "remove":
        remove_host(args.name)
    elif args.command == "show":
        show_host(args.name)
    elif args.command == "test":
        test_host(args.name)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
