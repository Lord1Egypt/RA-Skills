"""Persistent configuration management (JSON file at ~/.wayinvideo/config.json)."""

import os
import json
import copy

from wayinvideo.constants import DEFAULT_CONFIG

# ── File locations ───────────────────────────────────────────────────────────

CONFIG_DIR  = os.path.join(os.path.expanduser("~"), ".wayinvideo")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


# ── Dict helpers ─────────────────────────────────────────────────────────────

def _deep_merge(base, override):
    """Recursively merge *override* into a deep copy of *base*."""
    result = copy.deepcopy(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def get_nested(data, key_path, default=None):
    """Read a value from a nested dict using a dot-separated key path.

    Returns *default* when any segment of the path is missing.
    """
    keys = key_path.split(".")
    current = data
    for k in keys:
        if isinstance(current, dict) and k in current:
            current = current[k]
        else:
            return default
    return current


def key_exists(data, key_path):
    """Return True if every segment of the dot path exists in *data*."""
    keys = key_path.split(".")
    current = data
    for k in keys:
        if isinstance(current, dict) and k in current:
            current = current[k]
        else:
            return False
    return True


def set_nested(data, key_path, value):
    """Write a value into a nested dict, creating intermediate dicts as needed."""
    keys = key_path.split(".")
    current = data
    for k in keys[:-1]:
        if k not in current or not isinstance(current[k], dict):
            current[k] = {}
        current = current[k]
    current[keys[-1]] = value


def parse_value(text):
    """Parse a CLI string into bool / None / int / float / str."""
    low = text.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    if low in ("null", "none"):
        return None
    try:
        return int(text)
    except ValueError:
        pass
    try:
        return float(text)
    except ValueError:
        pass
    return text


# ── Load / Save ──────────────────────────────────────────────────────────────

def load_config():
    """Load the user config file and merge it on top of built-in defaults.

    Keys added in newer versions are automatically filled in from defaults.
    """
    config = copy.deepcopy(DEFAULT_CONFIG)
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as fh:
                user = json.load(fh)
            config = _deep_merge(config, user)
        except (json.JSONDecodeError, IOError):
            pass
    return config


def save_config(config):
    """Write the full config dict to disk."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as fh:
        json.dump(config, fh, indent=2, ensure_ascii=False)


def get_value(key_path):
    """Shortcut: load config and return a single value."""
    return get_nested(load_config(), key_path)


# ── Display ──────────────────────────────────────────────────────────────────

def format_tree(data, indent=0):
    """Render a config dict as an indented text tree (list of lines)."""
    lines = []
    prefix = "  " * indent
    for key in sorted(data.keys()):
        value = data[key]
        if isinstance(value, dict):
            lines.append(f"{prefix}{key}:")
            lines.extend(format_tree(value, indent + 1))
        else:
            lines.append(f"{prefix}{key} = {json.dumps(value)}")
    return lines