#!/usr/bin/env python3
"""
Bootstrap path setup and the rwlib import for rabbit-claude-md scripts.

Resolves the sibling engine skill `rabbit-writes` by walking up from this
file's own path rather than by arithmetic on the layout, so the skill
directory can move without editing the scripts inside it. Exits 2 with an
install hint when no rwlib is found anywhere above us.

Copied from skills/rabbit-reads/scripts/_bootstrap.py minus that skill's
reference-directory lookups, deliberately: two satellite skills should not
have two different ways to find the engine.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _walk_up(target, predicate=None):
    """Nearest ancestor of HERE (self included) where `target` exists, or None."""
    cur = HERE
    while True:
        cand = os.path.join(cur, target)
        if os.path.exists(cand):
            if predicate is None or predicate(cand):
                return cand
        parent = os.path.dirname(cur)
        if parent == cur:
            return None
        cur = parent


RWLIB_PARENT = _walk_up(os.path.join("rabbit-writes", "scripts"))
SKILLS_DIR = os.path.dirname(os.path.dirname(HERE))

# A scan.py beside these scripts wins over the sibling engine: the standalone
# skill zip vendors the engine next to the checker, the plugin layout does not.
# Either way claude_check ends up with one engine, never two disagreeing ones.
SCAN_PATH = os.path.join(HERE, "scan.py")
if not os.path.isfile(SCAN_PATH) and RWLIB_PARENT:
    SCAN_PATH = os.path.join(RWLIB_PARENT, "scan.py")

for path in (HERE, RWLIB_PARENT):
    if path and os.path.isdir(os.path.join(path, "rwlib")) and path not in sys.path:
        sys.path.insert(0, path)

try:
    from rwlib import cli_error
except (ImportError, ModuleNotFoundError) as exc:
    script_name = os.path.basename(sys.argv[0]) if sys.argv and sys.argv[0] else "script"
    engine_dir = os.path.join(SKILLS_DIR, "rabbit-writes")
    out = [
        "=" * 70,
        "FILE / I/O ERROR: Sibling engine skill `rabbit-writes` is missing.",
        "=" * 70,
        f"Script: {script_name}",
        "Parameter: 'rabbit-writes sibling skill' (expected type: directory path)",
        f"Provided Path: {engine_dir!r}",
        f"Details: {exc}",
        "\nVALID USAGE REQUIREMENT:",
        f"  Install `rabbit-writes` as a sibling directory under: {SKILLS_DIR}",
        f"  Expected structure: {SKILLS_DIR}/rabbit-writes/scripts/rwlib/",
        "=" * 70
    ]
    print("\n".join(out), file=sys.stderr)
    sys.exit(2)


__all__ = ["HERE", "SKILLS_DIR", "RWLIB_PARENT", "SCAN_PATH", "cli_error"]
