#!/usr/bin/env python3
"""
Start remote console - ttyd + SSH tunnel.
Cross-platform replacement for start-console.ps1

Usage:
    python start_console.py <project_name>
    python start_console.py <project_name> -c <command>
    python start_console.py --path /path/to/project
"""

import argparse
import platform
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

# Add scripts dir to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    import psutil
except ImportError:
    print("Error: psutil not installed. Run: pip install psutil")
    sys.exit(1)

from config_loader import (
    DEFAULT_CONFIG_PATH,
    load_config,
    get_server_config,
    get_ssh_target,
    get_ttyd_config,
    get_project,
    list_projects,
)


def is_port_in_use(port: int) -> bool:
    """Check if port is in use (excluding TIME_WAIT)."""
    for conn in psutil.net_connections():
        if conn.laddr and conn.laddr.port == port:
            # TIME_WAIT means connection is closing, port is effectively free
            if conn.status != 'TIME_WAIT':
                return True
    return False


def is_ttyd_running() -> Optional[int]:
    """Check if ttyd is running, return PID or None."""
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] and 'ttyd' in proc.info['name'].lower():
                return proc.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None


def kill_ttyd():
    """Kill all ttyd processes."""
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] and 'ttyd' in proc.info['name'].lower():
                proc.kill()
                print(f"Killed existing ttyd (PID: {proc.info['pid']})")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue


def start_ssh_tunnel(server: dict, ttyd_port: int) -> bool:
    """Start SSH tunnel in background using config."""
    ssh_target = get_ssh_target(server)

    # Check if ssh_alias is used (simple target) or full host:port
    is_windows = platform.system() == 'Windows'

    if server.get('ssh_alias'):
        # Using SSH alias - simpler command
        ssh_args = [
            'ssh',
            '-R', f'{ttyd_port}:127.0.0.1:{ttyd_port}',
            ssh_target,
            '-N',
            # Don't use -f on Windows, CREATE_NO_WINDOW handles backgrounding
            *([] if is_windows else ['-f']),
            '-o', 'ServerAliveInterval=30',
            '-o', 'ServerAliveCountMax=3',
            '-o', 'ExitOnForwardFailure=yes',
        ]
    else:
        # Using host:port:user
        ssh_args = [
            'ssh',
            '-R', f'{ttyd_port}:127.0.0.1:{ttyd_port}',
            '-p', str(server['port']),
            f"{server['user']}@{server['host']}",
            '-N',
            *([] if is_windows else ['-f']),
            '-o', 'ServerAliveInterval=30',
            '-o', 'ServerAliveCountMax=3',
            '-o', 'ExitOnForwardFailure=yes',
        ]

    print(f"Starting SSH tunnel: {ssh_target}")

    try:
        # Start SSH in background
        if is_windows:
            subprocess.Popen(
                ssh_args,
                creationflags=subprocess.CREATE_NO_WINDOW,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        else:
            subprocess.Popen(
                ['nohup'] + ssh_args,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

        # Wait for tunnel to establish
        time.sleep(2)

        # Verify tunnel by checking if port is bound by ssh
        for conn in psutil.net_connections():
            if conn.laddr and conn.laddr.port == ttyd_port:
                try:
                    proc = psutil.Process(conn.pid)
                    if 'ssh' in proc.name().lower():
                        print(f"SSH tunnel established (PID: {conn.pid})")
                        return True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

        print("Warning: SSH tunnel may not be established (could not verify)")
        return True  # Continue anyway, might still work

    except Exception as e:
        print(f"Failed to start SSH tunnel: {e}")
        return False


def get_shell_command() -> tuple[str, list]:
    """Get shell command based on platform."""
    system = platform.system()
    if system == 'Windows':
        return 'pwsh', ['-NoExit', '-Command']
    else:
        return 'bash', ['-c']


def start_ttyd(ttyd_config: dict, project_path: str, command: str) -> bool:
    """Start ttyd in background using config."""
    port = ttyd_config['port']
    ttyd_path = ttyd_config['path']
    options = ttyd_config['options']

    shell, shell_args = get_shell_command()

    ttyd_args = [ttyd_path, '-p', str(port)]

    # Add options (split by space, preserve quoted strings)
    if options:
        import shlex
        ttyd_args.extend(shlex.split(options))

    # Add working directory
    ttyd_args.extend(['--cwd', project_path])

    # Add shell and command
    ttyd_args.append(shell)
    ttyd_args.extend(shell_args)
    ttyd_args.append(command)

    print(f"Starting ttyd: {ttyd_path} on port {port}")
    print(f"Working directory: {project_path}")
    print(f"Command: {command}")

    try:
        if platform.system() == 'Windows':
            subprocess.Popen(
                ttyd_args,
                creationflags=subprocess.CREATE_NO_WINDOW,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                cwd=project_path
            )
        else:
            subprocess.Popen(
                ttyd_args,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                cwd=project_path
            )

        time.sleep(1)

        # Verify ttyd started
        pid = is_ttyd_running()
        if pid:
            print(f"ttyd started (PID: {pid})")
            return True
        else:
            print("Warning: Could not verify ttyd started")
            return True  # Continue anyway

    except FileNotFoundError:
        print(f"Error: ttyd not found at {ttyd_path}")
        return False
    except Exception as e:
        print(f"Failed to start ttyd: {e}")
        return False


def start_console(
    project_name: Optional[str] = None,
    project_path: Optional[str] = None,
    command: Optional[str] = None,
    config_path: Path = DEFAULT_CONFIG_PATH,
    force: bool = False,
) -> bool:
    """Start remote console."""

    # Load config
    config = load_config(config_path)
    if config is None:
        print(f"Error: Config file not found: {config_path}")
        return False

    # Get ttyd config
    ttyd_config = get_ttyd_config(config)
    ttyd_port = ttyd_config['port']

    # Resolve project
    if project_path:
        # Use provided path directly
        final_path = str(Path(project_path).resolve())
        final_command = command or config.get('defaults', {}).get('command', 'claude')
        # Resolve command name to actual command
        actual_command = config.get('commands', {}).get(final_command, final_command)
    elif project_name:
        # Look up project by name
        project = get_project(config, project_name)
        if not project:
            print(f"Error: Project '{project_name}' not found in config")
            print(f"Available projects: {list(list_projects(config).keys())}")
            return False
        final_path = project['path']
        actual_command = project['command']
    else:
        print("Error: Must specify either project_name or project_path")
        return False

    # Verify project path exists
    if not Path(final_path).exists():
        print(f"Error: Project path does not exist: {final_path}")
        return False

    # Check if ttyd already running
    ttyd_pid = is_ttyd_running()
    if ttyd_pid and not force:
        print(f"ttyd is already running (PID: {ttyd_pid})")
        print("Use --force to kill and restart")
        return False
    elif ttyd_pid and force:
        kill_ttyd()
        time.sleep(1)

    # Check port availability
    if is_port_in_use(ttyd_port):
        print(f"Warning: Port {ttyd_port} is already in use")
        if not force:
            print("Use --force to proceed anyway")
            return False

    # Get server config
    server = get_server_config(config)

    # Start SSH tunnel
    if not start_ssh_tunnel(server, ttyd_port):
        print("Error: SSH tunnel failed to establish")
        return False

    # Start ttyd
    if not start_ttyd(ttyd_config, final_path, actual_command):
        print("Error: ttyd failed to start")
        return False

    # Success
    print()
    print("=" * 50)
    print("✅ Remote console started successfully!")
    print()
    print(f"🔗 Access URL: http://{server['host']}:{ttyd_port}")
    print(f"📁 Project: {project_name or final_path}")
    print(f"📂 Working directory: {final_path}")
    print(f"🚀 Command: {actual_command}")
    print("=" * 50)

    return True


def main():
    parser = argparse.ArgumentParser(
        description='Start remote console',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python start_console.py my-project
    python start_console.py my-project -c claude-bypass
    python start_console.py --path /path/to/project
    python start_console.py my-project --force
"""
    )
    parser.add_argument('project', nargs='?', help='Project name from config')
    parser.add_argument('--path', '-p', help='Project path (instead of project name)')
    parser.add_argument('-c', '--command', help='Command to run (default: from config)')
    parser.add_argument('--config', type=Path, default=DEFAULT_CONFIG_PATH, help='Path to config file')
    parser.add_argument('--force', '-f', action='store_true', help='Kill existing ttyd and restart')

    args = parser.parse_args()

    if not args.project and not args.path:
        # Show available projects
        config = load_config(args.config)
        if config:
            projects = list_projects(config)
            if projects:
                print("Available projects:")
                for name, proj in projects.items():
                    print(f"  - {name}: {proj.get('path', '')}")
                print()
                print("Usage: python start_console.py <project_name>")
            else:
                print("No projects configured in config.json")
        else:
            print(f"Config not found: {args.config}")
        sys.exit(1)

    success = start_console(
        project_name=args.project,
        project_path=args.path,
        command=args.command,
        config_path=args.config,
        force=args.force,
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
