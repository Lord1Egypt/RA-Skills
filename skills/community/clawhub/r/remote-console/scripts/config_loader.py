#!/usr/bin/env python3
"""
Config loader for remote-console.
Provides unified config access for all scripts.
"""

import json
import sys
from pathlib import Path
from typing import Optional

# Default config path (relative to this script's parent directory)
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_CONFIG_PATH = SKILL_DIR / "config.json"


def load_config(config_path: Path = DEFAULT_CONFIG_PATH) -> Optional[dict]:
    """Load and parse config.json."""
    if not config_path.exists():
        return None
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Failed to parse config.json: {e}")
        return None


def get_server_config(config: dict) -> dict:
    """
    Get the default server config.
    Returns dict with: host, port, user, ssh_alias, ssh_target
    """
    default_server_name = config.get('defaults', {}).get('server', 'default')
    server = config.get('servers', {}).get(default_server_name, {})

    return {
        'host': server.get('host', ''),
        'port': server.get('port', 22),
        'user': server.get('user', ''),
        'ssh_alias': server.get('ssh_alias', ''),
        'name': server.get('name', default_server_name),
    }


def get_ssh_target(server: dict) -> str:
    """
    Get SSH target string.
    Uses ssh_alias if available, otherwise constructs user@host -p port.
    """
    if server.get('ssh_alias'):
        return server['ssh_alias']
    else:
        port = server.get('port', 22)
        user = server.get('user', '')
        host = server.get('host', '')
        if port == 22:
            return f"{user}@{host}"
        return f"-p {port} {user}@{host}"


def get_ttyd_config(config: dict) -> dict:
    """Get ttyd configuration."""
    ttyd = config.get('ttyd', {})
    return {
        'port': ttyd.get('port', 7681),
        'path': ttyd.get('path', 'ttyd'),
        'options': ttyd.get('options', ''),
    }


def get_project(config: dict, project_name: str) -> Optional[dict]:
    """Get project config by name."""
    project = config.get('projects', {}).get(project_name)
    if not project:
        return None

    # Resolve command
    command_name = project.get('command') or config.get('defaults', {}).get('command', 'claude')
    actual_command = config.get('commands', {}).get(command_name, command_name)

    return {
        'path': project.get('path', ''),
        'command': actual_command,
        'command_name': command_name,
    }


def list_projects(config: dict) -> dict:
    """List all configured projects."""
    return config.get('projects', {})


def get_default_command(config: dict) -> str:
    """Get default command name."""
    return config.get('defaults', {}).get('command', 'claude')


if __name__ == "__main__":
    # Test config loading
    config = load_config()
    if config:
        print("Config loaded successfully!")
        print(f"Server: {get_server_config(config)}")
        print(f"ttyd: {get_ttyd_config(config)}")
        print(f"Projects: {list(config.get('projects', {}))}")
        print(f"Config path: {DEFAULT_CONFIG_PATH}")
    else:
        print(f"Config not found at {DEFAULT_CONFIG_PATH}")
        sys.exit(1)
