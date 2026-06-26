#!/usr/bin/env python3
"""
Validate config.json for remote-console.
Checks all required fields and tests connectivity.

Usage:
    python validate_config.py
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

# Add scripts dir to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config_loader import (
    DEFAULT_CONFIG_PATH,
    load_config,
    get_server_config,
    get_ssh_target,
    get_ttyd_config,
    list_projects,
)


def is_placeholder(value: str) -> bool:
    if not value:
        return True
    placeholders = [
        "your-server.com",
        "your-username",
        "example.com",
    ]
    return value in placeholders


def check_ttyd_installed(ttyd_path: str) -> bool:
    """Check if ttyd is installed at the specified path."""
    if Path(ttyd_path).exists():
        return True
    # Also check if it's in PATH
    return shutil.which(ttyd_path) is not None


def test_ssh_connection(server: dict) -> bool:
    """Test SSH connection using config."""
    ssh_target = get_ssh_target(server)

    # Build test command
    if server.get('ssh_alias'):
        # Using SSH alias
        cmd = ['ssh', ssh_target, '-o', 'BatchMode=yes',
               '-o', 'ConnectTimeout=5', 'echo', 'SSH_OK']
    else:
        # Using host:port:user
        cmd = ['ssh', '-p', str(server['port']),
               '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=5',
               f"{server['user']}@{server['host']}", 'echo', 'SSH_OK']

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        return 'SSH_OK' in result.stdout
    except (subprocess.TimeoutExpired, Exception):
        return False


def validate_config(config_path: Path = DEFAULT_CONFIG_PATH) -> tuple[list, list]:
    """
    Validate config and return (errors, warnings).
    """
    errors = []
    warnings = []

    print("Validating remote-console configuration...")
    print(f"Config file: {config_path}")
    print()

    # Check file exists
    if not config_path.exists():
        errors.append(f"Config file not found: {config_path}")
        return errors, warnings

    # Load config
    config = load_config(config_path)
    if config is None:
        errors.append("Failed to load config.json")
        return errors, warnings

    # Validate servers
    print("Checking servers...")
    servers = config.get('servers', {})
    if not servers:
        errors.append("No servers configured")
    else:
        for server_name, server in servers.items():
            host = server.get('host', '')
            user = server.get('user', '')
            port = server.get('port', 22)
            ssh_alias = server.get('ssh_alias', '')

            print(f"  [{server_name}]")

            if ssh_alias:
                print(f"    SSH alias: {ssh_alias}")
            else:
                if is_placeholder(host):
                    errors.append(f"Server '{server_name}' has placeholder host: {host}")
                else:
                    print(f"    Host: {host}")

                if is_placeholder(user):
                    errors.append(f"Server '{server_name}' has placeholder user: {user}")
                else:
                    print(f"    User: {user}")

                print(f"    Port: {port}")

    # Validate ttyd config
    print()
    print("Checking ttyd config...")
    ttyd_config = get_ttyd_config(config)
    ttyd_path = ttyd_config['path']
    ttyd_port = ttyd_config['port']

    print(f"  Path: {ttyd_path}")
    print(f"  Port: {ttyd_port}")
    print(f"  Options: {ttyd_config['options'] or '(none)'}")

    if not check_ttyd_installed(ttyd_path):
        errors.append(f"ttyd not found at: {ttyd_path}")
        print("  Install: scoop install ttyd (Windows) or sudo apt install ttyd (Linux)")
    else:
        print("  ✅ ttyd found")

    # Validate projects
    print()
    print("Checking projects...")
    projects = list_projects(config)
    if not projects:
        warnings.append("No projects configured")
        print("  No projects configured")
    else:
        for name, proj in projects.items():
            path = proj.get('path', '')
            print(f"  [{name}]")
            print(f"    Path: {path}")
            if not Path(path).exists():
                warnings.append(f"Project '{name}' path does not exist: {path}")
            else:
                print("    ✅ Path exists")

    # Check defaults
    print()
    print("Checking defaults...")
    defaults = config.get('defaults', {})
    default_cmd = defaults.get('command', '')
    default_server = defaults.get('server', '')

    print(f"  Default command: {default_cmd or '(not set)'}")
    print(f"  Default server: {default_server or '(not set)'}")

    commands = config.get('commands', {})
    if default_cmd and default_cmd not in commands:
        errors.append(f"Default command '{default_cmd}' not found in commands list")
    elif default_cmd:
        print(f"    → Resolves to: {commands.get(default_cmd)}")

    # Test SSH connection if no errors so far
    if not errors:
        print()
        print("Testing SSH connection...")
        server = get_server_config(config)
        ssh_target = get_ssh_target(server)
        print(f"  Target: {ssh_target}")

        if test_ssh_connection(server):
            print("  ✅ SSH connection successful")
        else:
            warnings.append("SSH connection test failed - verify key authentication is set up")
            print("  ❌ SSH connection failed")

    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description='Validate remote-console config')
    parser.add_argument('--config', type=Path, default=DEFAULT_CONFIG_PATH, help='Config file path')

    args = parser.parse_args()

    errors, warnings = validate_config(args.config)

    # Report results
    print()
    print("=" * 50)

    if errors:
        print("❌ ERRORS:")
        for err in errors:
            print(f"  [!] {err}")

    if warnings:
        print("⚠️  WARNINGS:")
        for warn in warnings:
            print(f"  [?] {warn}")

    if not errors and not warnings:
        print("✅ Configuration is valid!")
        sys.exit(0)
    elif errors:
        print()
        print("Please fix the errors above before using remote-console.")
        sys.exit(1)
    else:
        print()
        print("Configuration has warnings but should work.")
        sys.exit(0)


if __name__ == "__main__":
    main()
