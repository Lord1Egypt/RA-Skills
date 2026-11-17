"""
Skill-side capability discovery.

Thin wrapper around the plugin's `list_capabilities` command — fetches
the categorised inventory and exposes it as Python data so the agent can
introspect at session start without re-parsing JSON each time.

Usage:
    from inventory import get_inventory, has_command, find_category

    inv = get_inventory()
    if has_command("inspect_grasshopper_definition"):
        ...

    cat = find_category("scene_summary")  # → "scene_analysis"

CLI:
    python3 inventory.py                 # pretty-print everything
    python3 inventory.py --category geometry
    python3 inventory.py --has find_nearby
"""

from __future__ import annotations

import json
import sys
from typing import Any, Dict, List, Optional

from rhino_client import RhinoClient


def _fetch(client: Optional[RhinoClient] = None) -> Dict[str, Any]:
    own_client = False
    if client is None:
        client = RhinoClient()
        client.connect()
        own_client = True
    try:
        return client.send_command("list_capabilities")
    finally:
        if own_client:
            client.disconnect()


def get_inventory(client: Optional[RhinoClient] = None) -> Dict[str, Any]:
    """Return the full plugin capability inventory.

    Shape (curated by the plugin, stable across patch versions):

        {
          "plugin_version": "0.2.8",
          "rhino_version":  "8.x.x (build ...)",
          "categories":     {"geometry": [...], "transforms": [...], ...},
          "native_command_allowlist": ["_Loft", "_Sweep1", ...],
          "scripting_paths": {"rhinoscriptsyntax": {...}, "rhinocommon": {...}},
          "preferences":    ["1. Typed command...", "2. batch_operations...", ...]
        }
    """
    return _fetch(client)


def list_categories(inv: Optional[Dict[str, Any]] = None) -> List[str]:
    inv = inv or get_inventory()
    return sorted((inv.get("categories") or {}).keys())


def commands_in(category: str, inv: Optional[Dict[str, Any]] = None) -> List[str]:
    inv = inv or get_inventory()
    return list((inv.get("categories") or {}).get(category, []))


def all_commands(inv: Optional[Dict[str, Any]] = None) -> List[str]:
    inv = inv or get_inventory()
    flat: List[str] = []
    for cmds in (inv.get("categories") or {}).values():
        flat.extend(cmds)
    return sorted(set(flat))


def has_command(name: str, inv: Optional[Dict[str, Any]] = None) -> bool:
    return name in all_commands(inv)


def find_category(name: str, inv: Optional[Dict[str, Any]] = None) -> Optional[str]:
    inv = inv or get_inventory()
    for cat, cmds in (inv.get("categories") or {}).items():
        if name in cmds:
            return cat
    return None


def native_allowlist(inv: Optional[Dict[str, Any]] = None) -> List[str]:
    inv = inv or get_inventory()
    return list(inv.get("native_command_allowlist") or [])


def is_native_allowed(command: str, inv: Optional[Dict[str, Any]] = None) -> bool:
    return command in native_allowlist(inv)


def _pretty_print(inv: Dict[str, Any]) -> None:
    print(f"RhinoClaw plugin {inv.get('plugin_version', '?')} on {inv.get('rhino_version', '?')}")
    print()
    print("Preference order:")
    for line in inv.get("preferences", []):
        print(f"  {line}")
    print()
    print("Categories (typed commands):")
    for cat in sorted((inv.get("categories") or {}).keys()):
        cmds = inv["categories"][cat]
        print(f"  [{cat}] ({len(cmds)})")
        for cmd in cmds:
            print(f"      - {cmd}")
    print()
    allow = inv.get("native_command_allowlist") or []
    print(f"Native command allowlist ({len(allow)}): {', '.join(allow)}")


def _main(argv: List[str]) -> int:
    if "--has" in argv:
        idx = argv.index("--has")
        if idx + 1 >= len(argv):
            print("--has requires a command name", file=sys.stderr)
            return 2
        target = argv[idx + 1]
        inv = get_inventory()
        cat = find_category(target, inv)
        if cat:
            print(f"YES — '{target}' is in category '{cat}'.")
            return 0
        print(f"NO — '{target}' is not exposed by this plugin.")
        return 1

    if "--category" in argv:
        idx = argv.index("--category")
        if idx + 1 >= len(argv):
            print("--category requires a name", file=sys.stderr)
            return 2
        cat = argv[idx + 1]
        inv = get_inventory()
        cmds = commands_in(cat, inv)
        if not cmds:
            print(f"No category '{cat}'. Known: {', '.join(list_categories(inv))}")
            return 1
        print(f"[{cat}] ({len(cmds)} commands)")
        for c in cmds:
            print(f"  - {c}")
        return 0

    if "--json" in argv:
        print(json.dumps(get_inventory(), indent=2))
        return 0

    _pretty_print(get_inventory())
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
