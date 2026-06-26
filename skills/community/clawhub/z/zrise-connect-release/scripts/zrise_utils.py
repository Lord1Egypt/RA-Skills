#!/usr/bin/env python3
"""
Zrise Utils - Common utilities for zrise-connect skill scripts.

Dynamically resolves workspace root based on skill installation path.
No hardcoded workspace names.

Usage:
    from zrise_utils import get_root, get_openclaw_config_path
    ROOT = get_root()
"""
import json
import pathlib
import ssl
import xmlrpc.client

# SSL context for macOS Python
_ssl_ctx = ssl.create_default_context()
_ssl_ctx.check_hostname = False
_ssl_ctx.verify_mode = ssl.CERT_NONE

# Workspace markers — directories/files that indicate a workspace root
_WORKSPACE_MARKERS = [
    'AGENTS.md', 'SOUL.md', 'USER.md', 'IDENTITY.md',
    'MEMORY.md', 'HEARTBEAT.md', 'TOOLS.md',
]

# Directories that mark a workspace root
_WORKSPACE_DIRS = ['state', 'memory', 'skills', 'config']

# Skill name — used to locate ourselves relative to the workspace
_SKILL_NAME = 'zrise-connect'


def get_root():
    """
    Get workspace root directory dynamically.

    Strategy: walk up from this file's location and find the first
    directory that looks like an OpenClaw workspace root.

    Expected layout:
        <workspace>/
        ├── skills/
        │   └── zrise-connect/
        │       └── scripts/
        │           └── zrise_utils.py   ← __file__ is here
        ├── AGENTS.md / SOUL.md / etc.
        └── state/

    Also handles:
        <workspace>/packages/<anything>/scripts/zrise_utils.py
        ~/.openclaw/skills/zrise-connect/scripts/zrise_utils.py
    """
    current = pathlib.Path(__file__).resolve()

    for parent in current.parents:
        # Check for workspace marker files
        has_markers = any((parent / m).exists() for m in _WORKSPACE_MARKERS)
        if has_markers:
            return parent

        # Check for workspace directories
        has_dirs = any((parent / d).exists() for d in _WORKSPACE_DIRS)
        if has_dirs and (parent / 'skills').exists():
            return parent

    # Fallback: walk up looking for 'skills' directory
    # Script is at .../skills/<skill>/scripts/zrise_utils.py
    # Workspace is .../skills/.. (2 levels up from scripts/)
    current_dir = current.parent  # scripts/
    skill_dir = current_dir.parent  # zrise-connect/
    skills_dir = skill_dir.parent  # skills/

    if skills_dir.name == 'skills':
        return skills_dir.parent  # workspace root

    # Last resort: 3 levels up from this file
    return current.parent.parent.parent


def get_openclaw_config_path():
    """Get path to openclaw.json config file."""
    # Always prefer ~/.openclaw/openclaw.json (global config)
    global_config = pathlib.Path.home() / '.openclaw' / 'openclaw.json'
    if global_config.exists():
        return global_config

    # Fallback: workspace root
    root = get_root()
    local = root / 'openclaw.json'
    if local.exists():
        return local

    # Last resort
    return global_config


def load_json(path):
    """Load JSON file with UTF-8 encoding."""
    path = pathlib.Path(path)
    if not path.is_absolute():
        path = get_root() / path
    if not path.exists():
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def connect_zrise():
    """
    Connect to Zrise via XML-RPC.

    Returns:
        tuple: (db, uid, secret, models, zrise_url)
    """
    config_path = get_openclaw_config_path()
    cfg = load_json(config_path)

    env = cfg['skills']['entries']['zrise-connect']['env']

    url = env['ZRISE_URL'].rstrip('/')
    db = env['ZRISE_DB']
    username = env['ZRISE_USERNAME']
    secret = env.get('ZRISE_API_KEY') or env.get('ZRISE_PASSWORD')

    # Ensure secret is string (not int from JSON)
    if secret is not None:
        secret = str(secret)

    common = xmlrpc.client.ServerProxy(url + '/xmlrpc/2/common', allow_none=True, context=_ssl_ctx)
    uid = common.authenticate(db, username, secret, {})

    if not uid:
        raise SystemExit('❌ Zrise authentication failed')

    models = xmlrpc.client.ServerProxy(url + '/xmlrpc/2/object', allow_none=True, context=_ssl_ctx)
    return db, uid, secret, models, url


def get_state_path(subpath=''):
    """Get path to state directory (relative to workspace root)."""
    root = get_root()
    state_path = root / 'state'

    if subpath:
        state_path = state_path / subpath

    # Ensure parent directory exists, not the file itself
    if state_path.suffix:  # Has file extension
        state_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        state_path.mkdir(parents=True, exist_ok=True)
    return state_path


def get_config_path(subpath=''):
    """Get path to config directory (relative to workspace root)."""
    root = get_root()

    if subpath:
        return root / 'config' / subpath
    return root / 'config'


def get_scripts_path(subpath=''):
    """Get path to scripts directory (relative to skill installation)."""
    # Scripts dir is next to this file
    scripts_dir = pathlib.Path(__file__).resolve().parent

    if subpath:
        return scripts_dir / subpath
    return scripts_dir


# Module-level constants
ROOT = get_root()
STATE_PATH = get_state_path()
CONFIG_PATH = get_config_path()
SCRIPTS_PATH = get_scripts_path()


if __name__ == '__main__':
    print('=== Zrise Utils Test ===')
    print(f'ROOT: {ROOT}')
    print(f'STATE_PATH: {STATE_PATH}')
    print(f'CONFIG_PATH: {CONFIG_PATH}')
    print(f'SCRIPTS_PATH: {SCRIPTS_PATH}')
    print(f'OpenClaw config: {get_openclaw_config_path()}')

    try:
        db, uid, secret, models, url = connect_zrise()
        print(f'✅ Connected to Zrise: {url} (uid={uid})')
    except Exception as e:
        print(f'⚠️  Connection test: {e}')
