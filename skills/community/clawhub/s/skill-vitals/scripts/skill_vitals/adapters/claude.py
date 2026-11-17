"""Claude Code configuration evidence."""

import json
import os
from pathlib import Path


def read_host_config(home=None):
    """Return enabled plugins, skill usage, and the raw Claude configuration."""
    base = Path(home) if home is not None else Path(os.path.expanduser("~"))
    path = base / ".claude.json"
    if not path.is_file():
        return None, {}, None
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, json.JSONDecodeError):
        return None, {}, None

    enabled = set()
    found_key = False

    def absorb(value):
        nonlocal found_key
        if isinstance(value, dict):
            found_key = True
            enabled.update(key for key, on in value.items() if on)
        elif isinstance(value, list):
            found_key = True
            enabled.update(value)

    absorb(data.get("enabledPlugins"))
    for project in (data.get("projects") or {}).values():
        if isinstance(project, dict):
            absorb(project.get("enabledPlugins"))

    usage = data.get("skillUsage")
    return (enabled if found_key else set()), (usage or {}), data


def lookup_usage(usage: dict, name: str, namespace):
    """Resolve namespaced usage first, then the legacy bare Skill name."""
    keys = ([f"{namespace}:{name}"] if namespace else []) + [name]
    for key in keys:
        value = usage.get(key)
        if isinstance(value, dict):
            return int(value.get("usageCount", 0) or 0), value.get("lastUsedAt"), key
        if isinstance(value, int):
            return value, None, key
    return 0, None, None
