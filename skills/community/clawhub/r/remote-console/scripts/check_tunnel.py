#!/usr/bin/env python3
"""
Check if SSH tunnel and ttyd are running.
Reads port from config.json instead of hardcoding.

Usage:
    python check_tunnel.py
    python check_tunnel.py --json
"""

import argparse
import json
import sys
from pathlib import Path

# Add scripts dir to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    import psutil
except ImportError:
    print("Error: psutil not installed. Run: pip install psutil")
    sys.exit(1)

from config_loader import DEFAULT_CONFIG_PATH, load_config, get_ttyd_config


def check_tunnel(config_path: Path = DEFAULT_CONFIG_PATH) -> dict:
    """Check SSH tunnel and ttyd status."""
    result = {
        "ttyd_running": False,
        "ttyd_pid": None,
        "ssh_tunnel_active": False,
        "ssh_pid": None,
        "port": None,
        "status": "unknown"
    }

    # Load config to get port
    config = load_config(config_path)
    if not config:
        print(f"Error: Could not load config from {config_path}")
        return result

    ttyd_config = get_ttyd_config(config)
    port = ttyd_config['port']
    result["port"] = port

    # Check ttyd process (should be listening on local port)
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] and 'ttyd' in proc.info['name'].lower():
                result["ttyd_running"] = True
                result["ttyd_pid"] = proc.info['pid']
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Check SSH tunnel process
    # SSH tunnel doesn't listen locally - it forwards through the SSH connection
    # So we check if there's an SSH process with the correct tunnel parameters
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            name = proc.info.get('name', '')
            if name and 'ssh' in name.lower():
                cmdline = proc.info.get('cmdline', [])
                if cmdline:
                    cmdline_str = ' '.join(cmdline)
                    # Check if this SSH process is for our tunnel
                    if f'-R {port}:127.0.0.1:{port}' in cmdline_str or \
                       f'-R{port}:127.0.0.1:{port}' in cmdline_str or \
                       f'-R {port}:localhost:{port}' in cmdline_str or \
                       f'-R{port}:localhost:{port}' in cmdline_str:
                        result["ssh_tunnel_active"] = True
                        result["ssh_pid"] = proc.info['pid']
                        break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Determine status
    if result["ttyd_running"] and result["ssh_tunnel_active"]:
        result["status"] = "running"
    elif result["ttyd_running"] or result["ssh_tunnel_active"]:
        result["status"] = "partial"
    else:
        result["status"] = "stopped"

    return result


def print_status(result: dict):
    """Print human-readable status."""
    port = result["port"]

    if result["status"] == "running":
        print("✅ Status: RUNNING")
        print(f"   ttyd PID: {result['ttyd_pid']}")
        print(f"   SSH tunnel PID: {result['ssh_pid']} (port {port})")
    elif result["status"] == "partial":
        print("⚠️  Status: PARTIAL")
        if result["ttyd_running"]:
            print(f"   ttyd running (PID: {result['ttyd_pid']})")
        if result["ssh_tunnel_active"]:
            print(f"   SSH tunnel active (PID: {result['ssh_pid']})")
        if not result["ttyd_running"]:
            print("   ttyd NOT running")
        if not result["ssh_tunnel_active"]:
            print("   SSH tunnel NOT active")
    else:
        print("⏹️  Status: STOPPED")
        print("   No services running")


def main():
    parser = argparse.ArgumentParser(description='Check remote console status')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--config', type=Path, default=DEFAULT_CONFIG_PATH, help='Config file path')

    args = parser.parse_args()

    result = check_tunnel(args.config)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_status(result)
        print()
        print(json.dumps(result))  # Also output JSON for parsing


if __name__ == "__main__":
    main()
