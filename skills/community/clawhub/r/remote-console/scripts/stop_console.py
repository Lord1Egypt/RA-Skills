#!/usr/bin/env python3
"""
Stop remote console - kill ttyd and SSH tunnel.
Reads port from config.json instead of hardcoding.

Usage:
    python stop_console.py
    python stop_console.py --json
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


def stop_console(config_path: Path = DEFAULT_CONFIG_PATH) -> dict:
    """Stop ttyd and SSH tunnel."""
    result = {
        "ttyd_stopped": False,
        "ttyd_pids": [],
        "ssh_tunnel_stopped": False,
        "ssh_pids": [],
        "port": None
    }

    # Load config to get port
    config = load_config(config_path)
    if not config:
        print(f"Error: Could not load config from {config_path}")
        return result

    ttyd_config = get_ttyd_config(config)
    port = ttyd_config['port']
    result["port"] = port

    print(f"Stopping remote console (port {port})...")

    # Kill ttyd processes
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] and 'ttyd' in proc.info['name'].lower():
                pid = proc.info['pid']
                proc.kill()
                result["ttyd_pids"].append(pid)
                result["ttyd_stopped"] = True
                print(f"  Killed ttyd (PID: {pid})")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if not result["ttyd_pids"]:
        print("  No ttyd process found")

    # Kill SSH tunnel on the port
    for conn in psutil.net_connections():
        if conn.laddr and conn.laddr.port == port:
            try:
                proc = psutil.Process(conn.pid)
                if 'ssh' in proc.name().lower():
                    pid = conn.pid
                    proc.kill()
                    result["ssh_pids"].append(pid)
                    result["ssh_tunnel_stopped"] = True
                    print(f"  Killed SSH tunnel (PID: {pid})")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    if result["ssh_pids"]:
        print(f"  Closed SSH tunnel on port {port}")
    else:
        print(f"  No SSH tunnel found on port {port}")

    return result


def main():
    parser = argparse.ArgumentParser(description='Stop remote console')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--config', type=Path, default=DEFAULT_CONFIG_PATH, help='Config file path')

    args = parser.parse_args()

    result = stop_console(args.config)

    if result["ttyd_stopped"] or result["ssh_tunnel_stopped"]:
        print()
        print("✅ Remote console stopped")
    else:
        print()
        print("ℹ️  No services were running")

    if args.json:
        print()
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
